import os
import tempfile
import time
import logging
import traceback
import csv
import io

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.pipeline import run_full_analysis

logger = logging.getLogger(__name__)

ANALYSIS_CACHE = {}

# Expected columns for each AML mode
CRYPTO_REQUIRED_COLUMNS = {"Source_Wallet_ID", "Dest_Wallet_ID", "Timestamp", "Amount", "Token_Type"}
BANKING_REQUIRED_COLUMNS = {"src_id", "dst_id", "amount"}


# -------------------------------------------------
# Health Check
# -------------------------------------------------
@api_view(["GET"])
def health(request):
    return Response({"status": "API is running"})


# -------------------------------------------------
# CSV Header Validation
# -------------------------------------------------
def validate_csv_columns(csv_path):
    """
    Validates that CSV has required columns for any AML mode.
    Returns: (is_valid, error_message, detected_mode)
    """
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            header = f.readline().strip()
            if not header:
                return False, "CSV file is empty", None
            
            columns = set(h.strip() for h in header.split(","))
            
            # Check for crypto mode
            if CRYPTO_REQUIRED_COLUMNS.issubset(columns):
                return True, None, "crypto"
            
            # Check for banking mode
            if BANKING_REQUIRED_COLUMNS.issubset(columns):
                return True, None, "banking"
            
            missing_crypto = CRYPTO_REQUIRED_COLUMNS - columns
            missing_banking = BANKING_REQUIRED_COLUMNS - columns
            
            return False, f"CSV missing required columns. Expected one of: {missing_crypto} or {missing_banking}", None
    
    except UnicodeDecodeError:
        return False, "CSV file must be UTF-8 encoded", None
    except Exception as e:
        return False, f"Failed to validate CSV: {str(e)}", None


# -------------------------------------------------
# CSV Upload
# -------------------------------------------------
@api_view(["POST"])
def upload_csv(request):

    file = request.FILES.get("file")

    if not file:
        return Response({"error": "CSV file required"}, status=400)

    MAX_FILE_SIZE_MB = 10

    if not file.name.lower().endswith(".csv"):
        return Response({"error": "Only CSV files are supported"}, status=400)

    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        return Response({"error": f"CSV file too large (max {MAX_FILE_SIZE_MB}MB)"}, status=400)

    old_csv = ANALYSIS_CACHE.get("csv_path")

    if old_csv and os.path.exists(old_csv):
        try:
            os.remove(old_csv)
        except Exception:
            logger.warning("Failed to delete old CSV")

    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="wb")

        for chunk in file.chunks():
            tmp.write(chunk)

        tmp.close()

        # Validate CSV structure
        is_valid, error_msg, detected_mode = validate_csv_columns(tmp.name)
        
        if not is_valid:
            os.remove(tmp.name)
            return Response({"error": error_msg}, status=400)

    except Exception as e:
        logger.exception("CSV save failed")
        if os.path.exists(tmp.name):
            os.remove(tmp.name)
        return Response(
            {"error": "Failed to save uploaded CSV"},
            status=500
        )

    ANALYSIS_CACHE.clear()
    ANALYSIS_CACHE["csv_path"] = tmp.name
    ANALYSIS_CACHE["detected_mode"] = detected_mode

    logger.info(f"CSV uploaded successfully (mode: {detected_mode})")

    return Response({
        "message": "CSV uploaded successfully",
        "detected_mode": detected_mode
    })


# -------------------------------------------------
# AML Mode Detection
# -------------------------------------------------
def detect_aml_mode(csv_path):
    """
    Detects AML mode from CSV header.
    """
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            header = f.readline().lower()

        if "src" in header and "dst" in header:
            return "banking"

        if "source_wallet_id" in header:
            return "crypto"

        return "crypto"
    except Exception as e:
        logger.error(f"Mode detection failed: {e}")
        return "crypto"


# -------------------------------------------------
# Run Analysis
# -------------------------------------------------
@api_view(["POST"])
def analyze(request):

    csv_path = ANALYSIS_CACHE.get("csv_path")

    if not csv_path or not os.path.exists(csv_path):
        return Response(
            {"error": "No CSV uploaded. Upload CSV before analysis."},
            status=400
        )

    try:
        start = time.time()

        mode = request.data.get("mode") if request.data else None

        if not mode:
            mode = detect_aml_mode(csv_path)

        # Validate mode
        if mode not in ["crypto", "banking"]:
            return Response(
                {"error": f"Invalid AML mode: {mode}. Must be 'crypto' or 'banking'."},
                status=400
            )

        logger.info(f"AML MODE SELECTED: {mode}")

        results = run_full_analysis(csv_path, mode)

        duration = time.time() - start
        logger.info(f"Analysis completed in {duration:.2f}s")

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        logger.exception("Analysis failed")
        return Response({"error": "Analysis failed"}, status=500)

    ANALYSIS_CACHE["results"] = results

    return Response({
        "message": "Analysis completed",
        "mode": mode,
        "duration_seconds": round(duration, 2)
    })


# -------------------------------------------------
# Graph Endpoint
# -------------------------------------------------
@api_view(["GET"])
def get_graph(request):

    results = ANALYSIS_CACHE.get("results")

    if not results:
        return Response(
            {"error": "Run analysis before requesting graph."},
            status=400
        )

    try:
        G = results.get("graph")
        if not G:
            return Response({"error": "Graph data not available"}, status=500)
            
        base_risks = results.get("base_risks", {})
        patterns = results.get("patterns", {})

        involved_wallets = {
            w for w, p in patterns.items()
            if any(v is True for k, v in p.items() if not k.endswith("_reason"))
        }

        nodes = []
        for node in G.nodes():
            node_str = str(node)
            risk_info = base_risks.get(node, {})
            risk = risk_info.get("base_risk", 0.0)

            if node_str.startswith("0x"):
                entity_type = "wallet"
            elif node_str.isdigit():
                entity_type = "bank_account"
            else:
                entity_type = "service"

            nodes.append({
                "id": node_str,
                "risk": risk,
                "is_risky": risk >= 0.5,
                "is_involved": node in involved_wallets,
                "entity_type": entity_type,
                "reasons": risk_info.get("reasons", []),
            })

        edges = []
        for u, v, data in G.edges(data=True):
            p = patterns.get(u, {})
            edges.append({
                "source": str(u),
                "target": str(v),
                "amount": data.get("amount", 0.0),
                "is_suspicious": p.get("fan_out", False) or p.get("peeling_chain", False),
                "pattern": (
                    "smurfing" if p.get("fan_out")
                    else "peeling" if p.get("peeling_chain")
                    else None
                )
            })

        return Response({"nodes": nodes, "edges": edges})
    
    except Exception as e:
        logger.exception("Graph rendering failed")
        return Response({"error": "Failed to render graph"}, status=500)


# -------------------------------------------------
# Base Risk Scores
# -------------------------------------------------
@api_view(["GET"])
def get_risk_scores(request):

    results = ANALYSIS_CACHE.get("results")

    if not results:
        return Response(
            {"error": "Run analysis before requesting risk scores."},
            status=400
        )

    try:
        base_risks = results.get("base_risks", {})

        wallets = []
        for wallet, risk_info in base_risks.items():
            wallet_str = str(wallet)
            base = risk_info.get("base_risk", 0.0)

            wallets.append({
                "id": wallet_str,
                "base_risk": base,
                "structural_risk": risk_info.get("structural_risk", 0.0),
                "flow_risk": risk_info.get("flow_risk", 0.0),
                "temporal_risk": risk_info.get("temporal_risk", 0.0),
                "proximity_risk": risk_info.get("proximity_risk", 0.0),
                "is_risky": base >= 0.5,
                "entity_type": "wallet" if wallet_str.startswith("0x") else "bank_account",
                "reasons": risk_info.get("reasons", []),
            })

        return Response({"wallets": wallets})
    
    except Exception as e:
        logger.exception("Risk scores retrieval failed")
        return Response({"error": "Failed to retrieve risk scores"}, status=500)


# -------------------------------------------------
# Final Risk Fusion
# -------------------------------------------------
@api_view(["GET"])
def get_final_risk(request):

    results = ANALYSIS_CACHE.get("results")

    if not results:
        return Response(
            {"error": "Run analysis before requesting final risk."},
            status=400
        )

    try:
        base_risks = results.get("base_risks", {})
        gnn_risks = results.get("gnn_risks") or {}

        ALPHA = 0.6

        wallets = []
        for wallet, info in base_risks.items():
            wallet_str = str(wallet)
            base = info.get("base_risk", 0.0)
            gnn = gnn_risks.get(wallet, base)

            final = round(ALPHA * base + (1 - ALPHA) * gnn, 3)

            wallets.append({
                "id": wallet_str,
                "base_risk": base,
                "gnn_risk": round(gnn, 3),
                "final_risk": final,
                "delta": round(final - base, 3),
                "reasons": info.get("reasons", []),
            })

        return Response({
            "alpha": ALPHA,
            "gnn_enabled": bool(gnn_risks),
            "wallets": wallets
        })
    
    except Exception as e:
        logger.exception("Final risk computation failed")
        return Response({"error": "Failed to compute final risk"}, status=500)
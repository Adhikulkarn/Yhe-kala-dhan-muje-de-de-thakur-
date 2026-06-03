import math
import networkx as nx
import logging

logger = logging.getLogger(__name__)

# -------------------------------------------------
# AML Risk Component Thresholds
# -------------------------------------------------
FAN_OUT_THRESHOLD = 3
FAN_IN_THRESHOLD = 3
MIN_TX_TEMPORAL = 3
LOW_IMBALANCE_THRESHOLD = 0.2


# -------------------------------------------------
# Utility
# -------------------------------------------------
def safe(v, default=0.0):
    """
    Converts NaN / None / invalid values to safe defaults.
    
    Args:
        v: Value to check
        default: Fallback value if v is invalid
        
    Returns:
        float: Safe numeric value
    """
    if v is None:
        return default
    if isinstance(v, float) and math.isnan(v):
        return default
    return v


# -------------------------------------------------
# Individual Risk Components
# -------------------------------------------------
def compute_structural_risk(node_feats):
    """
    Scores structural anomalies (fan-in/fan-out patterns).
    
    High risk if:
    - Out-degree >= FAN_OUT_THRESHOLD (smurfing pattern)
    - In-degree >= FAN_IN_THRESHOLD (aggregation pattern)
    
    Returns:
        float: Risk score [0.0, 1.0]
    """
    in_deg = safe(node_feats.get("in_degree"), 0)
    out_deg = safe(node_feats.get("out_degree"), 0)

    if out_deg >= FAN_OUT_THRESHOLD:
        return 1.0
    if in_deg >= FAN_IN_THRESHOLD:
        return 1.0

    return 0.0


def compute_flow_risk(node_feats):
    """
    Scores flow imbalance (pass-through behavior).
    
    High risk if:
    - Multiple incoming transactions
    - At least one outgoing transaction  
    - Low flow imbalance (in ≈ out)
    
    Returns:
        float: Risk score [0.0, 1.0]
    """
    incoming = safe(node_feats.get("in_degree"), 0)
    outgoing = safe(node_feats.get("out_degree"), 0)
    imbalance = safe(node_feats.get("flow_imbalance"), 1.0)

    if incoming >= 2 and outgoing >= 1 and imbalance <= LOW_IMBALANCE_THRESHOLD:
        return 1.0

    return 0.0


def compute_temporal_risk(node_feats):
    """
    Scores temporal clustering (rapid transaction bursts).
    
    High risk if:
    - Minimum transaction count met
    - All transactions occur within short timespan (≤ 30% of dataset window)
    
    Returns:
        float: Risk score [0.0, 1.0]
    """
    tx_count = safe(node_feats.get("tx_count"), 0)
    time_span = safe(node_feats.get("active_time_span"), 1.0)

    if tx_count < MIN_TX_TEMPORAL:
        return 0.0

    if time_span <= 0.3:
        return 1.0

    return 0.0


def compute_proximity_risk(G, suspicious_wallets, wallet, max_hops=3):
    """
    Scores proximity to known suspicious wallets in the network.
    
    Risk decreases with distance (hops) from suspicious nodes.
    Direct connection (1 hop) = 1.0 risk
    N hops away = 1 / (N + 1) risk
    
    Args:
        G: Transaction graph
        suspicious_wallets: Set of known suspicious wallet IDs
        wallet: Wallet to score
        max_hops: Maximum path length to consider
        
    Returns:
        float: Risk score [0.0, 1.0]
    """
    for s in suspicious_wallets:
        if wallet == s:
            return 1.0
        try:
            d = nx.shortest_path_length(G, wallet, s)
            if d <= max_hops:
                return 1.0 / (d + 1)
        except nx.NetworkXNoPath:
            continue

    return 0.0


# -------------------------------------------------
# Base Risk Aggregation (NaN-Safe, Gated)
# -------------------------------------------------
def compute_base_risk(
    G,
    node_features,
    pattern_results,
    weights=(0.4, 0.3, 0.2, 0.1),
):
    """
    AML-grade base risk computation with strict gates.
    
    Critical Rule: Hard gate on structural OR flow anomalies
    - If neither structural nor flow risk exists, base_risk = 0
    - Otherwise, compute weighted combination of all components
    
    Weights:
    - Structural (0.4): Degree-based anomalies
    - Flow (0.3): Transaction imbalance
    - Temporal (0.2): Time clustering
    - Proximity (0.1): Network distance to suspicious nodes
    
    Args:
        G: Transaction graph
        node_features: Node-level features
        pattern_results: Pattern detection results
        weights: Component weights (must sum to 1.0)
        
    Returns:
        dict: {wallet: {
            'base_risk': float [0.0, 1.0],
            'structural_risk': float,
            'flow_risk': float,
            'temporal_risk': float,
            'proximity_risk': float,
            'reasons': [str]
        }}
    """

    base_risks = {}

    suspicious_wallets = {
        w for w, p in pattern_results.items()
        if any(v is True for k, v in p.items() if not k.endswith("_reason"))
    }

    for wallet, feats in node_features.items():

        # Skip non-wallet entities
        if not wallet.startswith("0x"):
            continue

        structural = compute_structural_risk(feats)
        flow = compute_flow_risk(feats)

        # 🚨 HARD GATE: No anomaly detected = no risk
        if structural == 0.0 and flow == 0.0:
            base_risk = 0.0
            temporal = 0.0
            proximity = 0.0
        else:
            temporal = compute_temporal_risk(feats)
            proximity = compute_proximity_risk(G, suspicious_wallets, wallet)

            raw = (
                weights[0] * structural +
                weights[1] * flow +
                weights[2] * temporal +
                weights[3] * proximity
            )

            base_risk = safe(raw, 0.0)

        # Final clamp (absolute safety)
        base_risk = round(max(0.0, min(base_risk, 1.0)), 3)

        reasons = []
        if structural:
            reasons.append("Suspicious transaction structure (fan-in / fan-out)")
        if flow:
            reasons.append("Pass-through money flow behavior")
        if temporal:
            reasons.append("Highly coordinated transaction timing")
        if proximity > 0:
            reasons.append("Close proximity to suspicious wallets")

        base_risks[wallet] = {
            "base_risk": base_risk,
            "structural_risk": structural,
            "flow_risk": flow,
            "temporal_risk": temporal,
            "proximity_risk": round(proximity, 3),
            "reasons": reasons,
        }

    return base_risks

import pandas as pd
import networkx as nx

from core.ml_detector import transaction_ml_risk


def run_banking_pipeline(csv_path: str):

    df = pd.read_csv(csv_path)

    df = df.rename(columns={
        "src": "src_id",
        "dst": "dst_id",
    })

    REQUIRED = {"src_id", "dst_id", "amount"}

    missing = REQUIRED - set(df.columns)

    if missing:
        raise ValueError(f"Banking dataset missing columns: {missing}")

    G = nx.DiGraph()

    wallet_scores = {}
    wallet_amounts = {}

    for _, row in df.iterrows():

        src = str(row["src_id"])
        dst = str(row["dst_id"])
        amount = float(row["amount"])

        prob = transaction_ml_risk(src, dst, amount)

        G.add_edge(
            src,
            dst,
            amount=amount,
            is_suspicious=prob > 0.6
        )

        wallet_scores[src] = max(wallet_scores.get(src, 0), prob)
        wallet_scores[dst] = max(wallet_scores.get(dst, 0), prob)

        wallet_amounts[src] = max(wallet_amounts.get(src, 0), amount)
        wallet_amounts[dst] = max(wallet_amounts.get(dst, 0), amount)

    base_risks = {}

    for wallet, risk in wallet_scores.items():

        amount = wallet_amounts.get(wallet, 0)

        reasons = []

        if risk >= 0.85:
            reasons.append("Extremely high fraud probability predicted by ML model")

        elif risk >= 0.65:
            reasons.append("High fraud probability transaction detected")

        elif risk >= 0.45:
            reasons.append("Moderate anomaly detected by ML model")

        if amount >= 20000:
            reasons.append("Unusually large transaction amount")

        elif amount >= 10000:
            reasons.append("Large transaction value")

        if not reasons:
            reasons.append("Low-risk transaction detected by ML model")

        base_risks[wallet] = {
            "base_risk": round(risk, 3),
            "ml_risk": round(risk, 3),
            "reasons": reasons
        }

    return {
        "graph": G,
        "graph_summary": {
            "num_nodes": G.number_of_nodes(),
            "num_edges": G.number_of_edges(),
        },
        "node_features": {},
        "edge_features": {},
        "patterns": {},
        "base_risks": base_risks,
        "gnn_risks": None,
    }
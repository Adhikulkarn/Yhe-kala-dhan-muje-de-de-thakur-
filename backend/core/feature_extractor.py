import networkx as nx
import numpy as np


def extract_node_features(G: nx.DiGraph) -> dict:
    """
    Extracts node-level features from transaction graph.
    
    Features extracted per node:
    - in_degree: Count of incoming transactions
    - out_degree: Count of outgoing transactions
    - total_inflow: Sum of incoming amounts
    - total_outflow: Sum of outgoing amounts
    - flow_imbalance: |inflow - outflow| / (inflow + outflow)
    - tx_count: Total transactions (in + out)
    - active_time_span: Duration from first to last transaction (seconds)
    
    Args:
        G: NetworkX directed graph from build_transaction_graph
        
    Returns:
        dict: {node: {feature_name: value}}
    """
    node_features = {}

    for node in G.nodes():
        in_edges = list(G.in_edges(node, data=True))
        out_edges = list(G.out_edges(node, data=True))

        in_degree = len(in_edges)
        out_degree = len(out_edges)

        total_inflow = sum(e[2]["amount"] for e in in_edges)
        total_outflow = sum(e[2]["amount"] for e in out_edges)

        tx_count = in_degree + out_degree

        timestamps = [e[2]["timestamp"] for e in in_edges + out_edges]
        if timestamps:
            active_time_span = (max(timestamps) - min(timestamps)).total_seconds()
        else:
            active_time_span = 0.0

        # Measure how balanced inflow vs outflow is (0 = balanced, 1 = imbalanced)
        flow_imbalance = abs(total_inflow - total_outflow) / (
            total_inflow + total_outflow + 1e-9
        )

        node_features[node] = {
            "in_degree": in_degree,
            "out_degree": out_degree,
            "total_inflow": total_inflow,
            "total_outflow": total_outflow,
            "flow_imbalance": flow_imbalance,
            "tx_count": tx_count,
            "active_time_span": active_time_span,
        }

    return node_features


def extract_edge_features(G: nx.DiGraph) -> dict:
    """
    Extracts edge-level features from transaction graph.
    
    Features extracted per edge:
    - amount: Transaction value
    - time_delta: Seconds since previous outgoing transaction from source
    - peeling_ratio: amount / max(incoming_amounts) to source
      (ratio indicates value preservation in chain)
    
    Args:
        G: NetworkX directed graph from build_transaction_graph
        
    Returns:
        dict: {(source, dest): {feature_name: value}}
    """
    edge_features = {}

    for u, v, data in G.edges(data=True):
        amount = data["amount"]
        timestamp = data["timestamp"]

        # Time delta: how long since last outgoing transaction from this source
        prev_times = [
            d["timestamp"]
            for _, _, d in G.out_edges(u, data=True)
            if d["timestamp"] < timestamp
        ]

        if prev_times:
            time_delta = (timestamp - max(prev_times)).total_seconds()
        else:
            time_delta = 0.0

        # Peeling ratio: forwarding ratio (indicates "peeling chain")
        # High ratio (0.8+) = most value passed through (peeling)
        # Low ratio (0.2-) = significant value reduction
        incoming_amounts = [
            d["amount"] for _, _, d in G.in_edges(u, data=True)
        ]
        if incoming_amounts:
            peeling_ratio = amount / (max(incoming_amounts) + 1e-9)
        else:
            peeling_ratio = 1.0

        edge_features[(u, v)] = {
            "amount": amount,
            "time_delta": time_delta,
            "peeling_ratio": peeling_ratio,
        }

    return edge_features

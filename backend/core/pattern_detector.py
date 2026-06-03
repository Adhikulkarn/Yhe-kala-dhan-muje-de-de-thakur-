import networkx as nx
import logging

logger = logging.getLogger(__name__)


# -------------------------------------------------
# 1. Fan-Out Detection (Smurfing / Splitting)
# -------------------------------------------------
def detect_fan_out(node_features, out_thresh=0.6, in_thresh=0.2):
    """
    Detects nodes with high outgoing degree and low incoming degree.
    Pattern: Smurfing or fund splitting.
    """
    results = {}

    for node, feats in node_features.items():
        is_fan_out = (
            feats.get("out_degree", 0) >= out_thresh and
            feats.get("in_degree", 0) <= in_thresh
        )

        results[node] = {
            "fan_out": is_fan_out,
            "fan_out_reason": (
                "High out-degree with minimal incoming transactions"
                if is_fan_out else None
            )
        }

    return results


# -------------------------------------------------
# 2. Fan-In Detection (Aggregation)
# -------------------------------------------------
def detect_fan_in(node_features, in_thresh=0.6, out_thresh=0.2):
    """
    Detects nodes with high incoming degree and low outgoing degree.
    Pattern: Money aggregation or collection point.
    """
    results = {}

    for node, feats in node_features.items():
        is_fan_in = (
            feats.get("in_degree", 0) >= in_thresh and
            feats.get("out_degree", 0) <= out_thresh
        )

        results[node] = {
            "fan_in": is_fan_in,
            "fan_in_reason": (
                "High in-degree with minimal outgoing transactions"
                if is_fan_in else None
            )
        }

    return results


# -------------------------------------------------
# 3. Multi-Hop Convergence Detection
# -------------------------------------------------
def detect_multi_hop_convergence(G: nx.DiGraph, max_hops=3):
    """
    Detects nodes where funds converge to a common downstream wallet.
    Pattern: Money funneling through intermediaries.
    """
    results = {}

    for node in G.nodes():
        try:
            paths = nx.single_source_shortest_path(G, node, cutoff=max_hops)

            endpoints = [
                path[-1] for path in paths.values()
                if len(path) > 2
            ]

            is_converging = (
                len(endpoints) >= 3 and
                len(set(endpoints)) < len(endpoints)
            )

            results[node] = {
                "multi_hop_convergence": is_converging,
                "multi_hop_convergence_reason": (
                    "Funds converge to a common downstream wallet within few hops"
                    if is_converging else None
                )
            }
        except Exception as e:
            logger.warning(f"Convergence detection failed for node {node}: {e}")
            results[node] = {
                "multi_hop_convergence": False,
                "multi_hop_convergence_reason": None
            }

    return results


# -------------------------------------------------
# 4. Peeling-Chain Detection
# -------------------------------------------------
def detect_peeling_chains(edge_features, peel_thresh=0.8):
    """
    Detects nodes forwarding funds with minimal value reduction.
    Pattern: Chain of money transfers keeping amounts constant.
    """
    node_flags = {}

    for (u, v), feats in edge_features.items():
        peeling_ratio = feats.get("peeling_ratio", 1.0)
        if peeling_ratio >= peel_thresh:
            node_flags.setdefault(u, 0)
            node_flags[u] += 1

    results = {}
    for node, count in node_flags.items():
        results[node] = {
            "peeling_chain": True,
            "peeling_chain_reason": (
                f"Repeated fund forwarding with minimal value reduction "
                f"({count} peeling transactions)"
            )
        }

    return results


# -------------------------------------------------
# 5. Mule Wallet Detection (Pass-Through)
# -------------------------------------------------
def detect_mule_wallets(
    node_features,
    imbalance_thresh=0.2,
    time_thresh=0.3,
    degree_thresh=0.2,
):
    """
    Detects pass-through wallets with balanced flow and short activity window.
    Pattern: Temporary intermediary accounts (mule accounts).
    """
    results = {}

    for node, feats in node_features.items():
        is_mule = (
            feats.get("flow_imbalance", 1.0) <= imbalance_thresh and
            feats.get("active_time_span", 1.0) <= time_thresh and
            feats.get("tx_count", 0) >= degree_thresh
        )

        results[node] = {
            "mule_wallet": is_mule,
            "mule_wallet_reason": (
                "Pass-through wallet with balanced inflow/outflow "
                "and short activity window"
                if is_mule else None
            )
        }

    return results


# -------------------------------------------------
# 6. Pattern Aggregator
# -------------------------------------------------
def aggregate_patterns(*pattern_dicts):
    """
    Merge multiple pattern detection outputs into a single structure.

    Returns:
        combined[node] = {
            pattern_flag: bool,
            pattern_reason: str,
            ...
        }
    """
    combined = {}

    for pattern_dict in pattern_dicts:
        for node, flags in pattern_dict.items():
            combined.setdefault(node, {})
            combined[node].update(flags)

    return combined


def detect_patterns(G, node_features, edge_features):
    """
    Run all rule-based pattern detectors and aggregate results.
    
    This is the main entry point the pipeline should call.
    
    Args:
        G: NetworkX directed graph
        node_features: dict of node features
        edge_features: dict of edge features
        
    Returns:
        dict: Combined pattern detections for all nodes
    """
    try:
        fan_out = detect_fan_out(node_features)
        fan_in = detect_fan_in(node_features)
        convergence = detect_multi_hop_convergence(G)
        peeling = detect_peeling_chains(edge_features)
        mule = detect_mule_wallets(node_features)

        combined = aggregate_patterns(
            fan_out,
            fan_in,
            convergence,
            peeling,
            mule,
        )

        logger.info(f"Pattern detection completed for {len(combined)} nodes")
        return combined
    
    except Exception as e:
        logger.exception("Pattern detection failed")
        raise

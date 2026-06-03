import pandas as pd
import networkx as nx
from datetime import datetime

REQUIRED_COLUMNS = {
    "Source_Wallet_ID",
    "Dest_Wallet_ID",
    "Timestamp",
    "Amount",
    "Token_Type",
}


def load_transactions(csv_path: str) -> pd.DataFrame:
    """
    Load and validate the transaction CSV.
    
    Raises:
        ValueError: If required columns are missing
        Exception: For file I/O or parsing errors
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise ValueError(f"CSV file not found: {csv_path}")
    except pd.errors.ParserError as e:
        raise ValueError(f"Failed to parse CSV: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error reading CSV: {str(e)}")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    # Basic type cleaning
    try:
        df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
    except Exception as e:
        raise ValueError(f"Failed to convert data types: {str(e)}")
    
    # Check for NaN after conversion
    if df["Amount"].isna().any():
        raise ValueError("Amount column contains non-numeric values")
    if df["Timestamp"].isna().any():
        raise ValueError("Timestamp column contains invalid dates")

    return df


def build_transaction_graph(df: pd.DataFrame) -> nx.DiGraph:
    """
    Build a directed transaction graph from a DataFrame.
    
    Args:
        df: DataFrame with Source_Wallet_ID, Dest_Wallet_ID, Amount, Timestamp, Token_Type
    
    Returns:
        nx.DiGraph: Transaction graph with nodes as wallets, edges as transactions
        
    Raises:
        ValueError: If DataFrame is empty or malformed
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty")
    
    try:
        G = nx.DiGraph()

        for _, row in df.iterrows():
            src = str(row["Source_Wallet_ID"])
            dst = str(row["Dest_Wallet_ID"])
            amount = float(row["Amount"])

            # Skip self-loops and invalid amounts
            if src == dst or amount <= 0:
                continue

            G.add_edge(
                src,
                dst,
                amount=amount,
                timestamp=row["Timestamp"],
                token_type=row["Token_Type"],
            )
        
        if G.number_of_edges() == 0:
            raise ValueError("No valid transactions found in dataset")

        return G
    
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise Exception(f"Error building transaction graph: {str(e)}")


def graph_summary(G: nx.DiGraph) -> dict:
    """
    Basic sanity stats for the graph.
    
    Args:
        G: Directed graph
        
    Returns:
        dict: Graph statistics
    """
    try:
        return {
            "num_nodes": G.number_of_nodes(),
            "num_edges": G.number_of_edges(),
            "num_isolated_nodes": len(list(nx.isolates(G))),
        }
    except Exception as e:
        raise Exception(f"Error computing graph summary: {str(e)}")

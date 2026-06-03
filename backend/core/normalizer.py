import math


def min_max_normalize(feature_dict: dict, default=0.0) -> dict:
    """
    Normalizes each feature across all nodes or edges to [0,1] range.
    
    Handles:
    - None values
    - NaN (Not a Number) values
    - Constant features (where min == max)
    - Empty feature sets
    
    Args:
        feature_dict: {entity: {feature_name: value}}
        default: fallback value for invalid/missing features
    
    Returns:
        normalized: {entity: {feature_name: normalized_value [0,1]}}
    """

    if not feature_dict:
        return {}

    keys = list(feature_dict.keys())
    normalized = {k: {} for k in keys}

    # Collect all feature names safely
    feature_names = set()
    for k in keys:
        if feature_dict[k]:
            feature_names.update(feature_dict[k].keys())

    if not feature_names:
        return normalized

    # Min–Max normalization per feature
    for feature in feature_names:
        values = []
        
        # Collect valid values for this feature
        for k in keys:
            v = feature_dict[k].get(feature) if feature_dict[k] else None
            
            # Skip invalid values
            if v is None:
                continue
            if isinstance(v, float) and math.isnan(v):
                continue
            
            values.append(v)

        # Handle case where feature is completely invalid
        if not values:
            for k in keys:
                normalized[k][feature] = default
            continue

        min_val = min(values)
        max_val = max(values)

        # Normalize each entity's value for this feature
        for k in keys:
            v = feature_dict[k].get(feature) if feature_dict[k] else None
            
            # Handle invalid values
            if v is None or (isinstance(v, float) and math.isnan(v)):
                normalized[k][feature] = default
            # Handle constant feature (no variation)
            elif max_val == min_val:
                normalized[k][feature] = 0.0
            # Normal normalization to [0,1]
            else:
                normalized[k][feature] = (v - min_val) / (max_val - min_val)

    return normalized

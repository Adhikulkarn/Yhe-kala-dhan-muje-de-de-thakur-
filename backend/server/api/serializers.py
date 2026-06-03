"""
Serializers for consistent API response formatting.
"""

from rest_framework import serializers


class WalletRiskSerializer(serializers.Serializer):
    """Serializes wallet risk score data."""
    
    id = serializers.CharField(
        help_text="Wallet or account ID"
    )
    base_risk = serializers.FloatField(
        min_value=0.0,
        max_value=1.0,
        help_text="Base risk score [0.0, 1.0]"
    )
    structural_risk = serializers.FloatField(
        default=0.0,
        help_text="Structural anomaly risk"
    )
    flow_risk = serializers.FloatField(
        default=0.0,
        help_text="Flow imbalance risk"
    )
    temporal_risk = serializers.FloatField(
        default=0.0,
        help_text="Temporal clustering risk"
    )
    proximity_risk = serializers.FloatField(
        default=0.0,
        help_text="Network proximity risk"
    )
    is_risky = serializers.BooleanField(
        help_text="True if base_risk >= 0.5"
    )
    entity_type = serializers.CharField(
        help_text="Type: wallet, bank_account, or service"
    )
    reasons = serializers.ListField(
        child=serializers.CharField(),
        help_text="Reasons for risk score"
    )


class GraphNodeSerializer(serializers.Serializer):
    """Serializes graph node data for visualization."""
    
    id = serializers.CharField()
    risk = serializers.FloatField(min_value=0.0, max_value=1.0)
    is_risky = serializers.BooleanField()
    is_involved = serializers.BooleanField()
    entity_type = serializers.CharField()
    reasons = serializers.ListField(
        child=serializers.CharField()
    )


class GraphEdgeSerializer(serializers.Serializer):
    """Serializes graph edge data for visualization."""
    
    source = serializers.CharField()
    target = serializers.CharField()
    amount = serializers.FloatField(min_value=0.0)
    is_suspicious = serializers.BooleanField()
    pattern = serializers.CharField(required=False, allow_null=True)


class AnalysisResultSerializer(serializers.Serializer):
    """Serializes analysis completion response."""
    
    message = serializers.CharField()
    mode = serializers.ChoiceField(choices=['crypto', 'banking'])
    duration_seconds = serializers.FloatField(min_value=0.0)


class ErrorResponseSerializer(serializers.Serializer):
    """Serializes error responses."""
    
    error = serializers.CharField(
        help_text="Error message"
    )
    details = serializers.CharField(
        required=False,
        help_text="Additional error details (only in debug mode)"
    )

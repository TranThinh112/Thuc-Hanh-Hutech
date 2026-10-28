
from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class LocationChangeRule(AbstractFraudRule):
    id = "LOCATION_CHANGE"
    name = "Location Change / Impossible Travel"
    description = "Detects rapid geographic location changes and impossible travel anomalies"
    default_weight = 35

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        score = 0
        severity: Severity = "LOW"
        triggered = False
        reason = ""

        if features.impossible_travel:
            triggered = True
            score = 35
            severity = "CRITICAL"
            reason = f"Impossible travel detected! Location changed by {features.distance_km} km in {features.time_diff_seconds} seconds."
        elif features.location_changed:
            triggered = True
            score = 15
            severity = "MEDIUM"
            reason = f"Location changed from previous location ({features.distance_km} km distance)."

        return self.create_result(
            triggered, score, severity, reason,
            {
                "location_changed": features.location_changed,
                "impossible_travel": features.impossible_travel,
                "distance_km": features.distance_km,
                "time_diff_seconds": features.time_diff_seconds,
            }
        )


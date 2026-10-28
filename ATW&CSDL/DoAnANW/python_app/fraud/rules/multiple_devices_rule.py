
from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class MultipleDevicesRule(AbstractFraudRule):
    id = "MULTIPLE_DEVICES"
    name = "Multiple Devices Anomaly"
    description = "Detects multiple devices used by a single account within 15 minutes"
    default_weight = 25

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        dev_count = features.different_devices_15m
        score = 0
        severity: Severity = "LOW"
        triggered = False
        reason = ""

        if dev_count >= 5:
            triggered = True
            score = 40
            severity = "CRITICAL"
            reason = f"{dev_count} different devices used within 15 minutes."
        elif dev_count >= 3:
            triggered = True
            score = 25
            severity = "HIGH"
            reason = f"{dev_count} different devices used within 15 minutes."

        return self.create_result(
            triggered, score, severity, reason,
            {"different_devices_15m": dev_count}
        )


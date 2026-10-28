
from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class MultipleIpsRule(AbstractFraudRule):
    id = "MULTIPLE_IPS"
    name = "Multiple IP Addresses Anomaly"
    description = "Detects multiple IP addresses used within 15 minutes"
    default_weight = 20

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        ip_count = features.different_ips_15m
        score = 0
        severity: Severity = "LOW"
        triggered = False
        reason = ""

        if ip_count >= 5:
            triggered = True
            score = 35
            severity = "CRITICAL"
            reason = f"{ip_count} different IP addresses used within 15 minutes."
        elif ip_count >= 3:
            triggered = True
            score = 20
            severity = "HIGH"
            reason = f"{ip_count} different IP addresses used within 15 minutes."

        return self.create_result(
            triggered, score, severity, reason,
            {"different_ips_15m": ip_count}
        )



from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class NewIpRule(AbstractFraudRule):
    id = "NEW_IP"
    name = "New IP Address Detected"
    description = "Identifies transactions originating from an unrecognized IP address"
    default_weight = 10

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        is_new = features.is_new_ip
        score = 0
        severity: Severity = "LOW"
        triggered = False
        reason = ""

        if is_new:
            triggered = True
            score = 10
            severity = "LOW"
            reason = f"Transaction initiated from a new IP address ({ctx.ip_address})."

            if features.is_new_device and (features.amount_ratio >= 5 or features.transaction_amount > 20_000_000):
                score += 15
                severity = "HIGH"
                reason += " Combination of new IP, new device, and high amount detected."

        return self.create_result(
            triggered, score, severity, reason,
            {"is_new_ip": is_new, "ip_address": ctx.ip_address, "is_new_device": features.is_new_device}
        )


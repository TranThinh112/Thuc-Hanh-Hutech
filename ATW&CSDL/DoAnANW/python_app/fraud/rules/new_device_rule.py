
from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class NewDeviceRule(AbstractFraudRule):
    id = "NEW_DEVICE"
    name = "New Device Detected"
    description = "Identifies transactions originating from an unrecognized device"
    default_weight = 15

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        is_new = features.is_new_device
        score = 0
        severity: Severity = "LOW"
        triggered = False
        reason = ""

        if is_new:
            triggered = True
            score = 15
            severity = "MEDIUM"
            reason = f"Transaction initiated from a new device ID ({ctx.device_id})."

            if features.amount_ratio >= 5 or features.transaction_amount > 20_000_000:
                score += 10
                severity = "HIGH"
                reason += " High transaction amount combined with new device increases risk."

        return self.create_result(
            triggered, score, severity, reason,
            {"is_new_device": is_new, "device_id": ctx.device_id, "amount_ratio": features.amount_ratio}
        )



from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class PaymentMethodSwitchRule(AbstractFraudRule):
    id = "PAYMENT_METHOD_SWITCHING"
    name = "Rapid Payment Method Switching"
    description = "Detects rapid switching between different payment methods in a short window"
    default_weight = 20

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        methods_count = features.different_payment_methods_15m
        score = 0
        severity: Severity = "LOW"
        triggered = False
        reason = ""

        if methods_count >= 3:
            triggered = True
            score = 20
            severity = "HIGH"
            reason = f"Used {methods_count} different payment methods within 15 minutes."

        return self.create_result(
            triggered, score, severity, reason,
            {"different_payment_methods_15m": methods_count}
        )


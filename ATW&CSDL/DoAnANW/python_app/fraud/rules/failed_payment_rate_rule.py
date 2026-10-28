
from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class FailedPaymentRateRule(AbstractFraudRule):
    id = "FAILED_PAYMENT_RATE"
    name = "High Failed Payment Rate"
    description = "Evaluates historical failure rate of transactions for the user"
    default_weight = 15

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        rate = features.failed_payment_rate
        score = 0
        severity: Severity = "LOW"
        triggered = False
        reason = ""

        if rate > 0.70:
            triggered = True
            score = 25
            severity = "HIGH"
            reason = f"Historical payment failure rate is {rate * 100:.0f}% (>70%)."
        elif rate > 0.50:
            triggered = True
            score = 15
            severity = "MEDIUM"
            reason = f"Historical payment failure rate is {rate * 100:.0f}% (>50%)."

        return self.create_result(
            triggered, score, severity, reason,
            {"failed_payment_rate": rate}
        )


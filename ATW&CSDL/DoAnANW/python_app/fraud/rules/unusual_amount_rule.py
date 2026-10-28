
from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class UnusualAmountRule(AbstractFraudRule):
    id = "UNUSUAL_AMOUNT"
    name = "Unusual Amount Spike"
    description = "Evaluates transaction amount relative to historical user average"
    default_weight = 25

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        ratio = features.amount_ratio
        score = 0
        severity: Severity = "LOW"
        triggered = False
        reason = ""

        if ratio >= 20:
            triggered = True
            score = 35
            severity = "CRITICAL"
            reason = f"Transaction amount is {ratio}x higher than historical average ({features.average_amount:,.0f} VND)."
        elif ratio >= 10:
            triggered = True
            score = 25
            severity = "HIGH"
            reason = f"Transaction amount is {ratio}x higher than historical average ({features.average_amount:,.0f} VND)."
        elif ratio >= 5:
            triggered = True
            score = 15
            severity = "MEDIUM"
            reason = f"Transaction amount is {ratio}x higher than historical average ({features.average_amount:,.0f} VND)."

        return self.create_result(
            triggered, score, severity, reason,
            {"current_amount": features.transaction_amount, "average_amount": features.average_amount, "ratio": ratio}
        )


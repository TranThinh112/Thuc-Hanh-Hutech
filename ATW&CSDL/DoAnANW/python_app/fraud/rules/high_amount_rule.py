
from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class HighAmountRule(AbstractFraudRule):
    id = "HIGH_AMOUNT"
    name = "High Transaction Amount"
    description = "Evaluates absolute high transaction amount values"
    default_weight = 25

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        amount = features.transaction_amount
        score = 0
        severity: Severity = "LOW"
        triggered = False
        reason = ""

        if amount > 100_000_000:
            triggered = True
            score = 50
            severity = "CRITICAL"
            reason = f"Transaction amount ({amount:,.0f} VND) exceeds 100,000,000 VND limit."
        elif amount > 50_000_000:
            triggered = True
            score = 35
            severity = "HIGH"
            reason = f"Transaction amount ({amount:,.0f} VND) exceeds 50,000,000 VND threshold."
        elif amount > 20_000_000:
            triggered = True
            score = 20
            severity = "MEDIUM"
            reason = f"Transaction amount ({amount:,.0f} VND) exceeds 20,000,000 VND threshold."

        return self.create_result(
            triggered, score, severity, reason,
            {"amount": amount, "thresholds": {"medium": 20000000, "high": 50000000, "critical": 100000000}}
        )


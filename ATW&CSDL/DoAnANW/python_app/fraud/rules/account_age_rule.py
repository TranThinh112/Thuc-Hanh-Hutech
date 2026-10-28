
from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class AccountAgeRule(AbstractFraudRule):
    id = "ACCOUNT_AGE"
    name = "New Account Risk"
    description = "Evaluates risk associated with newly created user accounts"
    default_weight = 15

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        age_hours = features.account_age_hours
        score = 0
        severity: Severity = "LOW"
        triggered = False
        reason = ""

        if age_hours < 1:
            triggered = True
            score = 20
            severity = "MEDIUM"
            reason = f"Account created less than 1 hour ago ({age_hours:.1f} hours)."
        elif age_hours < 24:
            triggered = True
            score = 10
            severity = "LOW"
            reason = f"Account created less than 24 hours ago ({age_hours:.1f} hours)."

        return self.create_result(
            triggered, score, severity, reason,
            {"account_age_hours": age_hours}
        )



from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class FailedAttemptRule(AbstractFraudRule):
    id = "FAILED_ATTEMPT_VELOCITY"
    name = "Failed Payment Velocity"
    description = "Detects rapid failed attempts indicative of card testing or brute forcing"
    default_weight = 25

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        failed = features.failed_transactions_last_5m
        score = 0
        severity: Severity = "LOW"
        triggered = False
        reason = ""

        if failed >= 5:
            triggered = True
            score = 35
            severity = "CRITICAL"
            reason = f"Critical failed attempt rate: {failed} failed payment attempts within 5 minutes."
        elif failed >= 3:
            triggered = True
            score = 20
            severity = "HIGH"
            reason = f"Elevated failed attempt rate: {failed} failed payment attempts within 5 minutes."

        return self.create_result(
            triggered, score, severity, reason,
            {"failed_transactions_last_5m": failed}
        )


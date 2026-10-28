
from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class VelocityRule(AbstractFraudRule):
    id = "TRANSACTION_VELOCITY"
    name = "Transaction Velocity Spike"
    description = "Detects rapid sequence of transactions within a short 5-minute window"
    default_weight = 30

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        v5m = features.transactions_last_5m
        score = 0
        severity: Severity = "LOW"
        triggered = False
        reason = ""

        if v5m >= 8:
            triggered = True
            score = 40
            severity = "CRITICAL"
            reason = f"Extreme transaction velocity detected: {v5m} transactions within 5 minutes."
        elif v5m >= 5:
            triggered = True
            score = 25
            severity = "HIGH"
            reason = f"High transaction velocity detected: {v5m} transactions within 5 minutes."
        elif v5m >= 3:
            triggered = True
            score = 15
            severity = "MEDIUM"
            reason = f"Elevated transaction velocity detected: {v5m} transactions within 5 minutes."

        return self.create_result(
            triggered, score, severity, reason,
            {"transactions_last_5m": v5m, "transactions_last_1m": features.transactions_last_1m}
        )


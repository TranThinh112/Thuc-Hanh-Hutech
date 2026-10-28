
from typing import List
from .base_rule import AbstractFraudRule
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity, FraudPattern

def evaluate_composite_patterns(ctx: TransactionContext, features: ExtractedFeatures) -> List[FraudPattern]:
    patterns = []

    # Pattern A — ATO
    is_ato = (
        features.is_new_device
        and features.is_new_ip
        and features.location_changed
        and (features.amount_ratio >= 3 or features.transaction_amount > 15_000_000)
    )
    patterns.append(
        FraudPattern(
            pattern_id="PATTERN_ACCOUNT_TAKEOVER",
            name="Account Takeover (ATO)",
            description="New Device + New IP + Location Change + Abnormal Amount",
            triggered=is_ato,
            score_contribution=25 if is_ato else 0,
            severity="HIGH",
            explanation="Suspicious takeover indicators: Unrecognized device and IP combined with geographic movement and unusual spending.",
        )
    )

    # Pattern B — Card Testing
    is_card_testing = (
        features.transaction_amount < 2_000_000
        and features.failed_transactions_last_5m >= 2
        and (features.different_payment_methods_15m >= 2 or features.transactions_last_5m >= 3)
    )
    patterns.append(
        FraudPattern(
            pattern_id="PATTERN_CARD_TESTING",
            name="Card Testing Attack",
            description="Multiple small transactions + Repeated payment failures + Multiple card attempts",
            triggered=is_card_testing,
            score_contribution=30 if is_card_testing else 0,
            severity="HIGH",
            explanation="Automated card validation behavior detected using small amounts and multiple payment methods.",
        )
    )

    # Pattern C — Velocity Burst
    is_velocity_attack = (
        features.transactions_last_5m >= 5
        and (features.different_payment_methods_15m >= 2 or features.different_devices_15m >= 2)
    )
    patterns.append(
        FraudPattern(
            pattern_id="PATTERN_VELOCITY_ATTACK",
            name="Transaction Velocity Burst",
            description="Rapid high-frequency transactions using multiple methods/devices in a tight timeframe",
            triggered=is_velocity_attack,
            score_contribution=25 if is_velocity_attack else 0,
            severity="HIGH",
            explanation="Unusual volume spike in a 5-minute window attempting rapid drain or fraud.",
        )
    )

    # Pattern D — Impossible Travel
    is_impossible_travel = features.impossible_travel
    patterns.append(
        FraudPattern(
            pattern_id="PATTERN_IMPOSSIBLE_TRAVEL",
            name="Impossible Travel Teleportation",
            description="Geographic distance between consecutive transactions exceeds physical speed limits",
            triggered=is_impossible_travel,
            score_contribution=35 if is_impossible_travel else 0,
            severity="CRITICAL",
            explanation=f"Geographic change of {features.distance_km} km within {features.time_diff_seconds} seconds is physically impossible.",
        )
    )

    # Pattern E — High Value Anomaly
    is_high_value_anomaly = (
        features.amount_ratio >= 15
        and features.is_new_device
        and features.transaction_amount >= 20_000_000
    )
    patterns.append(
        FraudPattern(
            pattern_id="PATTERN_HIGH_VALUE_ANOMALY",
            name="High-Value Device Anomaly",
            description="Massive transaction ratio on an unverified device",
            triggered=is_high_value_anomaly,
            score_contribution=30 if is_high_value_anomaly else 0,
            severity="CRITICAL",
            explanation=f"Order amount is {features.amount_ratio}x historical average on an unrecognized device.",
        )
    )

    return patterns

class SuspiciousPatternRule(AbstractFraudRule):
    id = "SUSPICIOUS_COMPOSITE_PATTERN"
    name = "Suspicious Composite Fraud Patterns"
    description = "Evaluates multi-signal compound attack patterns across device, IP, location, and velocity"
    default_weight = 30

    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        patterns = evaluate_composite_patterns(ctx, features)
        triggered_patterns = [p for p in patterns if p.triggered]

        max_score = max([p.score_contribution for p in triggered_patterns], default=0)
        triggered = len(triggered_patterns) > 0

        highest_severity: Severity = "LOW"
        if any(p.severity == "CRITICAL" for p in triggered_patterns):
            highest_severity = "CRITICAL"
        elif any(p.severity == "HIGH" for p in triggered_patterns):
            highest_severity = "HIGH"
        elif triggered:
            highest_severity = "MEDIUM"

        pattern_names = ", ".join([p.name for p in triggered_patterns])
        reason = (
            f"Triggered composite pattern(s): {pattern_names}."
            if triggered
            else "No composite fraud patterns detected."
        )

        return self.create_result(
            triggered, max_score, highest_severity, reason,
            {
                "triggered_patterns_count": len(triggered_patterns),
                "patterns": [{"id": p.pattern_id, "name": p.name, "score": p.score_contribution} for p in triggered_patterns],
            }
        )


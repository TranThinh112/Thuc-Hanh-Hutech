
from ..types import Decision, RiskLevel
from ..constants import DEFAULT_DECISION_THRESHOLDS

def determine_decision(score: int, risk_level: RiskLevel, custom_thresholds: dict = None) -> Decision:
    thresh = custom_thresholds or DEFAULT_DECISION_THRESHOLDS
    if score >= thresh["BLOCK_SCORE"] or risk_level == "CRITICAL":
        return "BLOCK"
    if score >= thresh["REVIEW_SCORE"] or risk_level == "HIGH":
        return "REVIEW"
    return "APPROVE"


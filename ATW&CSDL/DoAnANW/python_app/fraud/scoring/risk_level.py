
from ..types import RiskLevel
from ..constants import DEFAULT_RISK_THRESHOLDS

def determine_risk_level(score: int, custom_thresholds: dict = None) -> RiskLevel:
    thresh = custom_thresholds or DEFAULT_RISK_THRESHOLDS
    if score >= thresh["CRITICAL_MIN_SCORE"]:
        return "CRITICAL"
    if score >= thresh["HIGH_MIN_SCORE"]:
        return "HIGH"
    if score >= thresh["MEDIUM_MIN_SCORE"]:
        return "MEDIUM"
    return "LOW"



from typing import List, Dict, Any
from ..types import RuleResult, FraudPattern
from ..constants import DEFAULT_RISK_THRESHOLDS

def calculate_risk_score(
    rule_results: List[RuleResult],
    patterns: List[FraudPattern]
) -> Dict[str, Any]:
    triggered_rules = [r for r in rule_results if r.triggered]
    raw_rule_score = sum(r.score for r in triggered_rules)

    triggered_patterns = [p for p in patterns if p.triggered]
    pattern_score = sum(p.score_contribution for p in triggered_patterns)

    primary_max_score = max([r.score for r in triggered_rules], default=0)
    remaining_rule_score = raw_rule_score - primary_max_score

    combined_total = round(primary_max_score + remaining_rule_score * 0.5 + pattern_score * 0.7)

    clamped_score = min(
        DEFAULT_RISK_THRESHOLDS["MAX_SCORE"],
        max(DEFAULT_RISK_THRESHOLDS["MIN_SCORE"], combined_total)
    )

    return {
        "raw_rule_score": raw_rule_score,
        "pattern_score": pattern_score,
        "total_score": combined_total,
        "clamped_score": clamped_score,
    }


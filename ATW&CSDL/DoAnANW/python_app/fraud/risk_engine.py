
from typing import List, Dict, Optional, Any
from .types import (
    TransactionContext,
    ExtractedFeatures,
    RuleResult,
    FraudAnalysisResult,
    SignalExplanation,
)
from .rules.base_rule import AbstractFraudRule
from .rules.suspicious_pattern_rule import evaluate_composite_patterns
from .scoring.score_calculator import calculate_risk_score
from .scoring.risk_level import determine_risk_level
from .scoring.decision_engine import determine_decision

class RiskEngine:
    def __init__(self, rules: List[AbstractFraudRule]):
        self.rules = rules

    def analyze(
        self,
        context: TransactionContext,
        features: ExtractedFeatures,
        custom_rule_configs: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> FraudAnalysisResult:
        triggered_results: List[RuleResult] = []

        for rule in self.rules:
            if custom_rule_configs and custom_rule_configs.get(rule.id, {}).get("enabled") is False:
                continue

            result = rule.evaluate(context, features)

            if custom_rule_configs and rule.id in custom_rule_configs:
                custom_weight = custom_rule_configs[rule.id].get("weight", rule.default_weight)
                if result.triggered and custom_weight != rule.default_weight:
                    result.score = round((result.score * custom_weight) / rule.default_weight)

            triggered_results.append(result)

        patterns = evaluate_composite_patterns(context, features)

        score_breakdown = calculate_risk_score(triggered_results, patterns)
        final_score = score_breakdown["clamped_score"]

        risk_level = determine_risk_level(final_score)
        decision = determine_decision(final_score, risk_level)

        signals: List[SignalExplanation] = []
        active_rules = [r for r in triggered_results if r.triggered]

        for r in active_rules:
            signals.append(
                SignalExplanation(
                    rule=r.rule_id,
                    score=r.score,
                    severity=r.severity,
                    reason=r.reason,
                    evidence=r.evidence,
                )
            )

        for p in patterns:
            if p.triggered:
                signals.append(
                    SignalExplanation(
                        rule=p.pattern_id,
                        score=p.score_contribution,
                        severity=p.severity,
                        reason=f"{p.name}: {p.explanation}",
                        evidence={"pattern": p.name, "description": p.description},
                    )
                )

        explanation_lines = [
            f"Fraud Detection Risk Score: {final_score}/100 ({risk_level})",
            f"Final Decision: {decision}",
        ]

        if not signals:
            explanation_lines.append("No suspicious signals or anomalies detected. Transaction behavior appears normal.")
        else:
            explanation_lines.append("Detected Risk Signals:")
            for idx, sig in enumerate(signals, 1):
                explanation_lines.append(f"{idx}. [{sig.severity}] {sig.reason} (+{sig.score} points)")

        return FraudAnalysisResult(
            risk_score=final_score,
            risk_level=risk_level,
            decision=decision,
            signals=signals,
            triggered_rules=active_rules,
            fraud_patterns=patterns,
            explanation="\n".join(explanation_lines),
            extracted_features=features,
        )


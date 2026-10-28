
from abc import ABC, abstractmethod
from typing import Dict, Any
from ..types import TransactionContext, ExtractedFeatures, RuleResult, Severity

class AbstractFraudRule(ABC):
    id: str
    name: str
    description: str
    default_weight: int

    @abstractmethod
    def evaluate(self, ctx: TransactionContext, features: ExtractedFeatures) -> RuleResult:
        pass

    def create_result(
        self,
        triggered: bool,
        score: int,
        severity: Severity,
        reason: str,
        evidence: Dict[str, Any]
    ) -> RuleResult:
        return RuleResult(
            rule_id=self.id,
            rule_name=self.name,
            triggered=triggered,
            score=score if triggered else 0,
            severity=severity if triggered else "LOW",
            reason=reason if triggered else f"Rule {self.name} passed (not triggered).",
            evidence=evidence,
        )



from typing import Dict, Optional, Any
from .types import TransactionContext, FraudAnalysisResult, SignalExplanation
from .feature_extractor import extract_features
from .risk_engine import RiskEngine
from .rules.high_amount_rule import HighAmountRule
from .rules.unusual_amount_rule import UnusualAmountRule
from .rules.velocity_rule import VelocityRule
from .rules.failed_attempt_rule import FailedAttemptRule
from .rules.new_device_rule import NewDeviceRule
from .rules.new_ip_rule import NewIpRule
from .rules.location_change_rule import LocationChangeRule
from .rules.payment_method_switch_rule import PaymentMethodSwitchRule
from .rules.multiple_devices_rule import MultipleDevicesRule
from .rules.multiple_ips_rule import MultipleIpsRule
from .rules.account_age_rule import AccountAgeRule
from .rules.failed_payment_rate_rule import FailedPaymentRateRule
from .rules.suspicious_pattern_rule import SuspiciousPatternRule

class FraudEngine:
    def __init__(self):
        rules = [
            HighAmountRule(),
            UnusualAmountRule(),
            VelocityRule(),
            FailedAttemptRule(),
            NewDeviceRule(),
            NewIpRule(),
            LocationChangeRule(),
            PaymentMethodSwitchRule(),
            MultipleDevicesRule(),
            MultipleIpsRule(),
            AccountAgeRule(),
            FailedPaymentRateRule(),
            SuspiciousPatternRule(),
        ]
        self.risk_engine = RiskEngine(rules)

    def analyze_transaction(
        self,
        context: TransactionContext,
        custom_rule_configs: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> FraudAnalysisResult:
        try:
            features = extract_features(context)
            return self.risk_engine.analyze(context, features, custom_rule_configs)
        except Exception as e:
            print("[FraudEngine Python] Engine error, executing FAIL-SAFE fallback to REVIEW:", e)
            features = extract_features(context)
            return FraudAnalysisResult(
                risk_score=65,
                risk_level="HIGH",
                decision="REVIEW",
                signals=[
                    SignalExplanation(
                        rule="ENGINE_FAIL_SAFE",
                        score=65,
                        severity="HIGH",
                        reason="Engine execution exception occurred. Fail-safe policy engaged to trigger manual review.",
                        evidence={"error": str(e)},
                    )
                ],
                triggered_rules=[],
                fraud_patterns=[],
                explanation="FAIL-SAFE ENGAGED: Fraud Engine encountered an exception. Transaction routed for manual review.",
                extracted_features=features,
            )

fraud_engine = FraudEngine()


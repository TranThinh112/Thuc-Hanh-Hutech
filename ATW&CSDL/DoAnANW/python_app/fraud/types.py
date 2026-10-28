from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Literal
import pydantic
from pydantic import BaseModel

def to_camel(string: str) -> str:
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

if pydantic.__version__.startswith('2.'):
    from pydantic import ConfigDict
    class CamelModel(BaseModel):
        model_config = ConfigDict(
            alias_generator=to_camel,
            populate_by_name=True,
            serialize_by_alias=True
        )
else:
    class CamelModel(BaseModel):
        class Config:
            alias_generator = to_camel
            allow_population_by_field_name = True

        def model_dump(self, by_alias: bool = False, **kwargs):
            return self.dict(by_alias=by_alias, **kwargs)

        def model_dump_json(self, by_alias: bool = False, **kwargs):
            return self.json(by_alias=by_alias, **kwargs)

Severity = Literal['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
RiskLevel = Literal['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
Decision = Literal['APPROVE', 'REVIEW', 'BLOCK']

@dataclass
class LocationData:
    country: str
    city: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

@dataclass
class HistoricalTransaction:
    timestamp: datetime
    amount: float
    payment_method: str
    device_id: str
    ip_address: str
    location: LocationData
    status: str

@dataclass
class TransactionContext:
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    payment_method: str
    ip_address: str
    device_id: str
    user_agent: str
    location: LocationData
    timestamp: datetime
    account_age_hours: float
    previous_transaction_count: int
    previous_failed_transaction_count: int
    average_transaction_amount: float
    max_previous_amount: float
    previous_transaction_time: Optional[datetime] = None
    previous_location: Optional[LocationData] = None
    previous_device_id: Optional[str] = None
    previous_ip_address: Optional[str] = None
    payment_method_history: List[str] = field(default_factory=list)
    recent_transactions: List[HistoricalTransaction] = field(default_factory=list)
    user_known_devices: List[str] = field(default_factory=list)
    user_known_ips: List[str] = field(default_factory=list)
    user_known_locations: List[str] = field(default_factory=list)

class ExtractedFeatures(CamelModel):
    transaction_amount: float
    average_amount: float
    amount_ratio: float
    max_previous_amount: float
    amount_percentile: float
    transactions_last_1m: int
    transactions_last_5m: int
    transactions_last_15m: int
    transactions_last_1h: int
    failed_transactions_last_5m: int
    different_payment_methods_15m: int
    different_devices_15m: int
    different_ips_15m: int
    is_new_device: bool
    is_new_ip: bool
    location_changed: bool
    distance_km: float
    time_diff_seconds: float
    impossible_travel: bool
    account_age_hours: float
    failed_payment_rate: float
    user_device_count: int
    user_ip_count: int

class RuleResult(CamelModel):
    rule_id: str
    rule_name: str
    triggered: bool
    score: int
    severity: Severity
    reason: str
    evidence: Dict[str, Any] = {}

class FraudPattern(CamelModel):
    pattern_id: str
    name: str
    description: str
    triggered: bool
    score_contribution: int
    severity: Severity
    explanation: str

class SignalExplanation(CamelModel):
    rule: str
    score: int
    severity: Severity
    reason: str
    evidence: Dict[str, Any] = {}

class FraudAnalysisResult(CamelModel):
    risk_score: int
    risk_level: RiskLevel
    decision: Decision
    signals: List[SignalExplanation]
    triggered_rules: List[RuleResult]
    fraud_patterns: List[FraudPattern]
    explanation: str
    extracted_features: ExtractedFeatures

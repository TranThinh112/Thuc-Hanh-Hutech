
import pytest
from python_app.fraud.rules.high_amount_rule import HighAmountRule
from python_app.fraud.rules.velocity_rule import VelocityRule
from python_app.fraud.rules.new_device_rule import NewDeviceRule
from python_app.fraud.rules.location_change_rule import LocationChangeRule
from python_app.fraud.rules.unusual_amount_rule import UnusualAmountRule
from python_app.fraud.feature_extractor import extract_features
from python_app.fraud.fraud_engine import fraud_engine
from python_app.fraud.simulation_engine import build_scenario_context

def test_high_amount_rule():
    rule = HighAmountRule()
    norm = build_scenario_context("NORMAL")["context"]
    norm_feats = extract_features(norm)
    assert rule.evaluate(norm, norm_feats).triggered is False

    high_ctx = build_scenario_context("NORMAL")["context"]
    high_ctx.amount = 60_000_000.0
    high_feats = extract_features(high_ctx)
    res = rule.evaluate(high_ctx, high_feats)
    assert res.triggered is True
    assert res.score == 35
    assert res.severity == "HIGH"

def test_velocity_rule():
    rule = VelocityRule()
    vel_ctx = build_scenario_context("VELOCITY_ATTACK")["context"]
    vel_feats = extract_features(vel_ctx)
    res = rule.evaluate(vel_ctx, vel_feats)
    assert res.triggered is True
    assert res.score >= 25

def test_new_device_rule():
    rule = NewDeviceRule()
    dev_ctx = build_scenario_context("NEW_DEVICE")["context"]
    dev_feats = extract_features(dev_ctx)
    res = rule.evaluate(dev_ctx, dev_feats)
    assert res.triggered is True
    assert res.evidence["is_new_device"] is True

def test_location_change_rule():
    rule = LocationChangeRule()
    travel_ctx = build_scenario_context("IMPOSSIBLE_TRAVEL")["context"]
    travel_feats = extract_features(travel_ctx)
    res = rule.evaluate(travel_ctx, travel_feats)
    assert res.triggered is True
    assert res.evidence["impossible_travel"] is True
    assert res.severity == "CRITICAL"

def test_unusual_amount_rule():
    rule = UnusualAmountRule()
    high_ctx = build_scenario_context("HIGH_AMOUNT")["context"]
    high_feats = extract_features(high_ctx)
    res = rule.evaluate(high_ctx, high_feats)
    assert res.triggered is True
    assert res.evidence["ratio"] > 20

def test_fraud_engine_account_takeover():
    ato_ctx = build_scenario_context("ACCOUNT_TAKEOVER")["context"]
    analysis = fraud_engine.analyze_transaction(ato_ctx)
    assert analysis.risk_score >= 75
    assert analysis.risk_level == "CRITICAL"
    assert analysis.decision == "BLOCK"
    assert "Detected Risk Signals" in analysis.explanation


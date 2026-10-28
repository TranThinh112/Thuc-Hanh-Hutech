
from datetime import datetime, timedelta
from typing import Dict, Any
from .types import TransactionContext, LocationData, HistoricalTransaction
from .fraud_engine import fraud_engine

SimulationScenario = str

def build_scenario_context(scenario: SimulationScenario) -> Dict[str, Any]:
    base_user = "user_sim_999"
    now = datetime.now()
    known_device = "device_home_pc_101"
    known_ip = "113.161.44.12"

    loc_hcm = LocationData(country="Vietnam", city="Ho Chi Minh City", latitude=10.8231, longitude=106.6297)
    loc_tokyo = LocationData(country="Japan", city="Tokyo", latitude=35.6762, longitude=139.6503)

    if scenario == "NORMAL":
        return {
            "title": "Normal Transaction Scenario",
            "description": "Routine 500,000 VND purchase from registered home device and IP in HCM city.",
            "context": TransactionContext(
                transaction_id=f"TX_SIM_NORM_{int(now.timestamp())}",
                user_id=base_user,
                amount=500_000.0,
                currency="VND",
                payment_method="VISA",
                ip_address=known_ip,
                device_id=known_device,
                user_agent="Mozilla/5.0 Chrome/120.0",
                location=loc_hcm,
                timestamp=now,
                account_age_hours=720.0,
                previous_transaction_count=45,
                previous_failed_transaction_count=0,
                average_transaction_amount=600_000.0,
                max_previous_amount=2_500_000.0,
                previous_transaction_time=now - timedelta(days=1),
                previous_location=loc_hcm,
                previous_device_id=known_device,
                previous_ip_address=known_ip,
                payment_method_history=["VISA"],
                recent_transactions=[],
                user_known_devices=[known_device],
                user_known_ips=[known_ip],
                user_known_locations=["Ho Chi Minh City"],
            ),
        }
    elif scenario == "CARD_TESTING":
        recents = [
            HistoricalTransaction(
                timestamp=now - timedelta(seconds=(i + 1) * 25),
                amount=120_000.0,
                payment_method="MASTERCARD" if i % 2 == 0 else "VISA",
                device_id="device_bot_tester_01",
                ip_address="45.33.32.156",
                location=loc_hcm,
                status="FAILED",
            )
            for i in range(4)
        ]
        return {
            "title": "Card Testing Attack",
            "description": "Multiple small failed transactions with rotating card numbers within 5 minutes.",
            "context": TransactionContext(
                transaction_id=f"TX_SIM_CARD_{int(now.timestamp())}",
                user_id="user_card_tester",
                amount=99_000.0,
                currency="VND",
                payment_method="JCB",
                ip_address="45.33.32.156",
                device_id="device_bot_tester_01",
                user_agent="Python-requests/2.31.0",
                location=loc_hcm,
                timestamp=now,
                account_age_hours=1.0,
                previous_transaction_count=0,
                previous_failed_transaction_count=4,
                average_transaction_amount=100_000.0,
                max_previous_amount=200_000.0,
                previous_transaction_time=now - timedelta(seconds=20),
                previous_location=loc_hcm,
                previous_device_id="device_bot_tester_01",
                previous_ip_address="45.33.32.156",
                payment_method_history=["VISA", "MASTERCARD", "JCB"],
                recent_transactions=recents,
                user_known_devices=[],
                user_known_ips=[],
                user_known_locations=[],
            ),
        }
    elif scenario in ["HIGH_AMOUNT", "UNUSUAL_HIGH_AMOUNT"]:
        return {
            "title": "Unusual High Amount Scenario",
            "description": "Đơn hàng lớn 68,000,000 VND (gấp hơn 60 lần mức chi tiêu trung bình) từ thiết bị quen thuộc.",
            "context": TransactionContext(
                transaction_id=f"TX_SIM_HIGH_{int(now.timestamp())}",
                user_id=base_user,
                amount=68_000_000.0,
                currency="VND",
                payment_method="VISA",
                ip_address=known_ip,
                device_id=known_device,
                user_agent="Mozilla/5.0 Chrome/120.0",
                location=loc_hcm,
                timestamp=now,
                account_age_hours=720.0,
                previous_transaction_count=15,
                previous_failed_transaction_count=0,
                average_transaction_amount=600_000.0,
                max_previous_amount=1_200_000.0,
                previous_transaction_time=now - timedelta(hours=12),
                previous_location=loc_hcm,
                previous_device_id=known_device,
                previous_ip_address=known_ip,
                payment_method_history=["VISA"],
                recent_transactions=[],
                user_known_devices=[known_device],
                user_known_ips=[known_ip],
                user_known_locations=["Ho Chi Minh City"],
            ),
        }
    elif scenario == "NEW_DEVICE":
        return {
            "title": "New Device Scenario",
            "description": "Standard amount purchase originating from an unrecognized device ID.",
            "context": TransactionContext(
                transaction_id=f"TX_SIM_DEV_{int(now.timestamp())}",
                user_id=base_user,
                amount=1_200_000.0,
                currency="VND",
                payment_method="MASTERCARD",
                ip_address=known_ip,
                device_id="device_unrecognized_iphone_77",
                user_agent="Mozilla/5.0 iPhone Mobile",
                location=loc_hcm,
                timestamp=now,
                account_age_hours=500.0,
                previous_transaction_count=20,
                previous_failed_transaction_count=0,
                average_transaction_amount=1_000_000.0,
                max_previous_amount=3_000_000.0,
                previous_transaction_time=now - timedelta(hours=5),
                previous_location=loc_hcm,
                previous_device_id=known_device,
                previous_ip_address=known_ip,
                payment_method_history=["MASTERCARD"],
                recent_transactions=[],
                user_known_devices=[known_device],
                user_known_ips=[known_ip],
                user_known_locations=["Ho Chi Minh City"],
            ),
        }
    elif scenario in ["VELOCITY_ATTACK", "VELOCITY_BURST"]:
        recents = [
            HistoricalTransaction(
                timestamp=now - timedelta(seconds=(i + 1) * 30),
                amount=2_000_000.0,
                payment_method="VISA" if i % 2 == 0 else "MASTERCARD",
                device_id=known_device,
                ip_address=known_ip,
                location=loc_hcm,
                status="APPROVED",
            )
            for i in range(7)
        ]
        return {
            "title": "Velocity Burst Attack",
            "description": "8 consecutive transactions initiated within a 5-minute window.",
            "context": TransactionContext(
                transaction_id=f"TX_SIM_VEL_{int(now.timestamp())}",
                user_id=base_user,
                amount=2_000_000.0,
                currency="VND",
                payment_method="VISA",
                ip_address=known_ip,
                device_id=known_device,
                user_agent="Mozilla/5.0 Chrome/120.0",
                location=loc_hcm,
                timestamp=now,
                account_age_hours=200.0,
                previous_transaction_count=50,
                previous_failed_transaction_count=1,
                average_transaction_amount=1_500_000.0,
                max_previous_amount=5_000_000.0,
                previous_transaction_time=now - timedelta(seconds=40),
                previous_location=loc_hcm,
                previous_device_id=known_device,
                previous_ip_address=known_ip,
                payment_method_history=["VISA", "MASTERCARD"],
                recent_transactions=recents,
                user_known_devices=[known_device],
                user_known_ips=[known_ip],
                user_known_locations=["Ho Chi Minh City"],
            ),
        }
    elif scenario == "ACCOUNT_TAKEOVER":
        return {
            "title": "Account Takeover (ATO) Attack",
            "description": "New Device + New IP + Location Change + 45,000,000 VND high value order.",
            "context": TransactionContext(
                transaction_id=f"TX_SIM_ATO_{int(now.timestamp())}",
                user_id=base_user,
                amount=45_000_000.0,
                currency="VND",
                payment_method="VISA",
                ip_address="185.220.101.5",
                device_id="device_hacker_kali_linux",
                user_agent="Mozilla/5.0 Tor Browser",
                location=loc_tokyo,
                timestamp=now,
                account_age_hours=360.0,
                previous_transaction_count=25,
                previous_failed_transaction_count=0,
                average_transaction_amount=750_000.0,
                max_previous_amount=2_000_000.0,
                previous_transaction_time=now - timedelta(minutes=10),
                previous_location=loc_hcm,
                previous_device_id=known_device,
                previous_ip_address=known_ip,
                payment_method_history=["VISA"],
                recent_transactions=[],
                user_known_devices=[known_device],
                user_known_ips=[known_ip],
                user_known_locations=["Ho Chi Minh City"],
            ),
        }
    elif scenario == "IMPOSSIBLE_TRAVEL":
        return {
            "title": "Impossible Travel Anomaly",
            "description": "Transaction in Ho Chi Minh City, followed by Tokyo 5 minutes later.",
            "context": TransactionContext(
                transaction_id=f"TX_SIM_TRAVEL_{int(now.timestamp())}",
                user_id=base_user,
                amount=5_000_000.0,
                currency="VND",
                payment_method="MASTERCARD",
                ip_address="133.242.180.11",
                device_id="device_tokyo_macbook",
                user_agent="Mozilla/5.0 Macintosh",
                location=loc_tokyo,
                timestamp=now,
                account_age_hours=500.0,
                previous_transaction_count=30,
                previous_failed_transaction_count=0,
                average_transaction_amount=1_000_000.0,
                max_previous_amount=6_000_000.0,
                previous_transaction_time=now - timedelta(minutes=5),
                previous_location=loc_hcm,
                previous_device_id=known_device,
                previous_ip_address=known_ip,
                payment_method_history=["MASTERCARD"],
                recent_transactions=[],
                user_known_devices=[known_device],
                user_known_ips=[known_ip],
                user_known_locations=["Ho Chi Minh City"],
            ),
        }
    else: # COMBINED_ATTACK
        recents = [
            HistoricalTransaction(
                timestamp=now - timedelta(seconds=(i + 1) * 20),
                amount=85_000_000.0,
                payment_method="VISA",
                device_id="device_unknown_attack_rig",
                ip_address="198.51.100.44",
                location=loc_tokyo,
                status="FAILED",
            )
            for i in range(6)
        ]
        return {
            "title": "Combined Multi-Vector Attack",
            "description": "New Account + New Device + New IP + High Amount + Velocity + Location Change.",
            "context": TransactionContext(
                transaction_id=f"TX_SIM_COMB_{int(now.timestamp())}",
                user_id="user_sim_fresh_001",
                amount=85_000_000.0,
                currency="VND",
                payment_method="VISA",
                ip_address="198.51.100.44",
                device_id="device_unknown_attack_rig",
                user_agent="Mozilla/5.0 Custom Python Bot",
                location=loc_tokyo,
                timestamp=now,
                account_age_hours=0.2,
                previous_transaction_count=0,
                previous_failed_transaction_count=3,
                average_transaction_amount=500_000.0,
                max_previous_amount=500_000.0,
                previous_transaction_time=now - timedelta(minutes=2),
                previous_location=loc_hcm,
                previous_device_id="device_mobile_temp",
                previous_ip_address="113.161.44.99",
                payment_method_history=["VISA", "MASTERCARD", "BANK_TRANSFER"],
                recent_transactions=recents,
                user_known_devices=[],
                user_known_ips=[],
                user_known_locations=[],
            ),
        }

def run_fraud_simulation(scenario: SimulationScenario) -> Dict[str, Any]:
    scenario_info = build_scenario_context(scenario)
    title = scenario_info["title"]
    description = scenario_info["description"]
    context: TransactionContext = scenario_info["context"]

    analysis = fraud_engine.analyze_transaction(context)

    pipeline_steps = [
        {
            "step": "Transaction Submitted",
            "description": f"Received payment request of {context.amount:,.0f} VND from User {context.user_id}",
            "timestamp": datetime.now().isoformat(),
            "data": {"amount": context.amount, "paymentMethod": context.payment_method, "location": context.location.city},
        },
        {
            "step": "Feature Extraction",
            "description": "Computed amount ratio, 5-min velocity, location distance, travel speed, and account features",
            "timestamp": datetime.now().isoformat(),
            "data": analysis.extracted_features.model_dump(by_alias=True),
        },
        {
            "step": "Fraud Rule Evaluation",
            "description": f"Evaluated 13 modular rules. Triggered {len(analysis.triggered_rules)} rules.",
            "timestamp": datetime.now().isoformat(),
            "data": [{"rule": r.rule_name, "score": r.score, "severity": r.severity} for r in analysis.triggered_rules],
        },
        {
            "step": "Composite Pattern Detection",
            "description": "Evaluated compound patterns (ATO, Card Testing, Impossible Travel, Velocity Burst).",
            "timestamp": datetime.now().isoformat(),
            "data": [p.name for p in analysis.fraud_patterns if p.triggered],
        },
        {
            "step": "Risk Scoring & Decision Engine",
            "description": f"Final Risk Score: {analysis.risk_score}/100 [{analysis.risk_level}]. Decision: {analysis.decision}",
            "timestamp": datetime.now().isoformat(),
            "data": {"score": analysis.risk_score, "level": analysis.risk_level, "decision": analysis.decision},
        },
    ]

    analysis_dict = {
        "riskScore": analysis.risk_score,
        "riskLevel": analysis.risk_level,
        "decision": analysis.decision,
        "explanation": analysis.explanation,
        "signals": [s.model_dump(by_alias=True) for s in analysis.signals],
        "triggeredRules": [r.model_dump(by_alias=True) for r in analysis.triggered_rules],
        "fraudPatterns": [p.model_dump(by_alias=True) for p in analysis.fraud_patterns],
        "extractedFeatures": analysis.extracted_features.model_dump(by_alias=True),
    }

    return {
        "scenario": scenario,
        "title": title,
        "description": description,
        "context": {
            "transactionId": context.transaction_id,
            "userId": context.user_id,
            "amount": context.amount,
            "paymentMethod": context.payment_method,
            "ipAddress": context.ip_address,
            "deviceId": context.device_id,
            "location": context.location.city,
        },
        "analysis": analysis_dict,
        "pipelineSteps": pipeline_steps,
    }


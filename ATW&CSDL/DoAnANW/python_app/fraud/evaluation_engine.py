
from typing import Dict, Any
from .simulation_engine import run_fraud_simulation

def run_system_evaluation(sample_size_per_class: int = 100) -> Dict[str, Any]:
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    normal_scenarios = ["NORMAL", "NEW_IP"]
    fraud_scenarios = ["HIGH_AMOUNT", "VELOCITY_ATTACK", "CARD_TESTING", "ACCOUNT_TAKEOVER", "IMPOSSIBLE_TRAVEL", "COMBINED_ATTACK"]

    for i in range(sample_size_per_class):
        scenario = normal_scenarios[i % len(normal_scenarios)]
        sim = run_fraud_simulation(scenario)
        if sim["analysis"]["decision"] == "APPROVE":
            tn += 1
        else:
            fp += 1

    for i in range(sample_size_per_class):
        scenario = fraud_scenarios[i % len(fraud_scenarios)]
        sim = run_fraud_simulation(scenario)
        if sim["analysis"]["decision"] in ["BLOCK", "REVIEW"]:
            tp += 1
        else:
            fn += 1

    total_count = sample_size_per_class * 2
    precision = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 0.0
    recall = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 0.0
    accuracy = round((tp + tn) / total_count, 4) if total_count > 0 else 0.0
    f1_score = round(2 * precision * recall / (precision + recall), 4) if (precision + recall) > 0 else 0.0

    return {
        "totalCount": total_count,
        "normalCount": sample_size_per_class,
        "fraudCount": sample_size_per_class,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "accuracy": accuracy,
        "f1Score": f1_score,
        "disclaimer": "Important Note: These evaluation metrics reflect performance on a synthetic simulated dataset designed for demonstration and architectural validation purposes. They do not claim live production payment network statistics.",
    }


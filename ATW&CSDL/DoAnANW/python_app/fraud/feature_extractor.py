
from .types import TransactionContext, ExtractedFeatures
from .amount_analyzer import analyze_amount
from .velocity_analyzer import analyze_velocity
from .device_analyzer import analyze_device_and_ip
from .location_analyzer import analyze_location
from .behavior_analyzer import analyze_behavior

def extract_features(ctx: TransactionContext) -> ExtractedFeatures:
    amount_feats = analyze_amount(ctx)
    velocity_feats = analyze_velocity(ctx)
    device_feats = analyze_device_and_ip(ctx)
    location_feats = analyze_location(ctx)
    behavior_feats = analyze_behavior(ctx)

    combined = {}
    combined.update(amount_feats)
    combined.update(velocity_feats)
    combined.update(device_feats)
    combined.update(location_feats)
    combined.update(behavior_feats)

    return ExtractedFeatures(**combined)


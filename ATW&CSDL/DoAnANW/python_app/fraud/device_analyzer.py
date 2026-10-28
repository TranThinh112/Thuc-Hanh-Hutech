
from .types import TransactionContext

def analyze_device_and_ip(ctx: TransactionContext) -> dict:
    if ctx.user_known_devices:
        is_new_device = ctx.device_id not in ctx.user_known_devices
    else:
        is_new_device = ctx.previous_device_id != ctx.device_id if ctx.previous_device_id else False

    if ctx.user_known_ips:
        is_new_ip = ctx.ip_address not in ctx.user_known_ips
    else:
        is_new_ip = ctx.previous_ip_address != ctx.ip_address if ctx.previous_ip_address else False

    all_devices = set(ctx.user_known_devices + [ctx.device_id])
    all_ips = set(ctx.user_known_ips + [ctx.ip_address])

    return {
        "is_new_device": is_new_device,
        "is_new_ip": is_new_ip,
        "user_device_count": len(all_devices),
        "user_ip_count": len(all_ips),
    }


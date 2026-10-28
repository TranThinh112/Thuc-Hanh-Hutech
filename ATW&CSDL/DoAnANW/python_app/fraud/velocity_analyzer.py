
from datetime import datetime
from .types import TransactionContext

def analyze_velocity(ctx: TransactionContext) -> dict:
    now_ms = ctx.timestamp.timestamp() * 1000

    count_1m = 1
    count_5m = 1
    count_15m = 1
    count_1h = 1

    failed_5m = ctx.previous_failed_transaction_count or 0
    methods_15m = {ctx.payment_method}
    devices_15m = {ctx.device_id}
    ips_15m = {ctx.ip_address}

    for tx in ctx.recent_transactions:
        tx_ms = tx.timestamp.timestamp() * 1000
        diff_ms = now_ms - tx_ms
        diff_minutes = diff_ms / (1000 * 60)

        if diff_minutes <= 1:
            count_1m += 1
        if diff_minutes <= 5:
            count_5m += 1
            if tx.status in ["FAILED", "BLOCKED"]:
                failed_5m += 1
        if diff_minutes <= 15:
            count_15m += 1
            methods_15m.add(tx.payment_method)
            devices_15m.add(tx.device_id)
            ips_15m.add(tx.ip_address)
        if diff_minutes <= 60:
            count_1h += 1

    return {
        "transactions_last_1m": count_1m,
        "transactions_last_5m": count_5m,
        "transactions_last_15m": count_15m,
        "transactions_last_1h": count_1h,
        "failed_transactions_last_5m": failed_5m,
        "different_payment_methods_15m": len(methods_15m),
        "different_devices_15m": len(devices_15m),
        "different_ips_15m": len(ips_15m),
    }


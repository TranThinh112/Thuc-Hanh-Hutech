
from .types import TransactionContext

def analyze_behavior(ctx: TransactionContext) -> dict:
    account_age_hours = ctx.account_age_hours or 24.0
    total_tx_count = ctx.previous_transaction_count + 1
    failed_tx_count = ctx.previous_failed_transaction_count or 0
    failed_payment_rate = round(failed_tx_count / total_tx_count, 2) if total_tx_count > 0 else 0.0

    return {
        "account_age_hours": account_age_hours,
        "failed_payment_rate": failed_payment_rate,
    }


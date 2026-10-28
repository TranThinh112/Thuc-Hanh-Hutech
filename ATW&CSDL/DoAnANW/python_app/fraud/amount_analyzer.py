
from .types import TransactionContext

def analyze_amount(ctx: TransactionContext) -> dict:
    transaction_amount = ctx.amount
    average_amount = ctx.average_transaction_amount if ctx.average_transaction_amount > 0 else ctx.amount
    amount_ratio = round(transaction_amount / average_amount, 2) if average_amount > 0 else 1.0
    max_previous_amount = ctx.max_previous_amount or average_amount

    higher_or_equal_count = 0
    if ctx.recent_transactions:
        for tx in ctx.recent_transactions:
            if tx.amount <= transaction_amount:
                higher_or_equal_count += 1
        amount_percentile = round(higher_or_equal_count / len(ctx.recent_transactions), 2)
    else:
        amount_percentile = 0.5

    return {
        "transaction_amount": transaction_amount,
        "average_amount": average_amount,
        "amount_ratio": amount_ratio,
        "max_previous_amount": max_previous_amount,
        "amount_percentile": amount_percentile,
    }


import re

with open('api/routers/performance.py', 'r') as f:
    content = f.read()

old_block = """        results = []
        for row in rows:
            results.append(
                AccountPerformance(
                    id=row["id"],
                    account_number=row["account_number"],
                    balance=row["balance"],
                    equity=row["equity"],
                    total_profit=row["total_profit"],
                    total_loss=row["total_loss"],
                    pnl=row["pnl"],
                    profit_factor=row["profit_factor"],
                    currency=row["currency"],
                    timestamp=datetime.fromisoformat(row["timestamp"]),
                )
            )"""

new_block = """        results = [
            AccountPerformance(
                id=row["id"],
                account_number=row["account_number"],
                balance=row["balance"],
                equity=row["equity"],
                total_profit=row["total_profit"],
                total_loss=row["total_loss"],
                pnl=row["pnl"],
                profit_factor=row["profit_factor"],
                currency=row["currency"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
            )
            for row in rows
        ]"""

new_content = content.replace(old_block, new_block)

with open('api/routers/performance.py', 'w') as f:
    f.write(new_content)

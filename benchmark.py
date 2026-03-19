import time
from datetime import datetime
import sys
import os

# Ensure api module can be imported
sys.path.insert(0, os.path.abspath("."))
try:
    from api.models.schemas import AccountPerformance
except ImportError as e:
    print(f"Failed to import AccountPerformance: {e}")
    # Define a mock if it fails
    class AccountPerformance:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

rows = [
    {
        "id": i,
        "account_number": f"12345{i}",
        "balance": 1000.0 + i,
        "equity": 1000.0 + i,
        "total_profit": 100.0,
        "total_loss": 50.0,
        "pnl": 50.0,
        "profit_factor": 2.0,
        "currency": "USD",
        "timestamp": datetime.now().isoformat()
    } for i in range(10000)
]

def bench_for_loop():
    start = time.perf_counter()
    results = []
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
        )
    return time.perf_counter() - start

def bench_list_comp():
    start = time.perf_counter()
    results = [
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
    ]
    return time.perf_counter() - start

# Warm up
for _ in range(5):
    bench_for_loop()
    bench_list_comp()

for_times = [bench_for_loop() for _ in range(100)]
comp_times = [bench_list_comp() for _ in range(100)]

for_avg = sum(for_times)/len(for_times)
comp_avg = sum(comp_times)/len(comp_times)
print(f"For loop avg: {for_avg:.5f}s")
print(f"List comp avg: {comp_avg:.5f}s")
print(f"Improvement: {(for_avg-comp_avg)/for_avg*100:.2f}%")

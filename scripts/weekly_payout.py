from modules.finance import FinanceManager
import json
from datetime import datetime

def run_weekly_payout():
    fin = FinanceManager()
    # In production, this would read total revenue from the payment gateway
    total_revenue = 1000.00  # Example
    result = fin.weekly_payout(total_revenue)
    print(f"Payout executed: {result}")

if __name__ == "__main__":
    run_weekly_payout()

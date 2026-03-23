# Uses the stored config to perform bank transfers
# In practice, you'd need to integrate with a payment service that supports South African bank transfers.
# For now, we generate a report and log the payout.
import json
from pathlib import Path
from datetime import datetime

def run_weekly_payout():
    # Load config
    config_path = Path.home() / '.stormy' / 'payment_config.json'
    with open(config_path) as f:
        config = json.load(f)
    
    total_revenue = get_total_revenue()  # sum of payments in the week
    fnb_share = total_revenue * 0.40
    african_share = total_revenue * 0.20
    reserve_share = total_revenue * 0.07
    
    # Update reserve balance
    config['reserve_balance'] += reserve_share
    
    # Log the payout (you'd actually transfer funds here via banking API or manual)
    log_entry = {
        'date': datetime.utcnow().isoformat(),
        'total_revenue': total_revenue,
        'fnb': fnb_share,
        'african_bank': african_share,
        'reserve_added': reserve_share,
        'reserve_balance': config['reserve_balance']
    }
    log_path = Path.home() / '.stormy' / 'payout_log.json'
    logs = []
    if log_path.exists():
        with open(log_path) as f:
            logs = json.load(f)
    logs.append(log_entry)
    with open(log_path, 'w') as f:
        json.dump(logs, f)
    
    # Save updated config
    with open(config_path, 'w') as f:
        json.dump(config, f)
    
    print(f"Payout processed: {log_entry}")

def get_total_revenue():
    # Sum payments from payment logs in the last 7 days
    # Placeholder
    return 1000.00

if __name__ == '__main__':
    run_weekly_payout()

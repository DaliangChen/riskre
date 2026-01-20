# src/reinsurance/xol.py

def xol_payout(loss, retention, limit):
    """
    Excess of Loss payout per loss
    """
    return min(max(loss - retention, 0.0), limit)

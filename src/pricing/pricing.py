# src/pricing/pricing.py

def calculate_premium(expected_loss, tvar, expense_ratio=0.05):
    """
    Simple technical premium with risk loading
    """
    risk_loading = max(tvar - expected_loss, 0.0)
    premium = (expected_loss + risk_loading) * (1 + expense_ratio)
    return premium

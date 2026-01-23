# src/pricing/pricing.py
from config_loader import PricingConfig

def calculate_premium(expected_loss: float, tvar: float, config: PricingConfig) -> float:
    """
    Simple technical premium with risk loading
    """
    risk_loading = max(tvar - expected_loss, 0.0)
    premium = (expected_loss + risk_loading) * (1 + config.expense_ratio)
    return premium

# src/reinsurance/xol.py
from config_loader import ReinsuranceConfig

def xol_payout(loss: float, config: ReinsuranceConfig) -> float:
    """
    Excess of Loss payout per loss
    """
    return min(max(loss - config.retention, 0.0), config.limit)

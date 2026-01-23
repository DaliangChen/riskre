import numpy as np

from config_loader import PricingConfig


def compute_risk_metrics(
    payouts: np.ndarray, config: PricingConfig
) -> dict[str, float]:
    expected_loss = np.mean(payouts)

    var = np.quantile(payouts, config.alpha)
    tvar = payouts[payouts >= var].mean()

    return {
        "expected_loss": expected_loss,
        f"var_{int(config.alpha*100)}": var,
        "tvar": tvar,
        "pml": var,
    }

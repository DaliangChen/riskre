import numpy as np


def compute_risk_metrics(payouts, alpha=0.99):
    expected_loss = np.mean(payouts)

    var = np.quantile(payouts, alpha)
    tvar = payouts[payouts >= var].mean()

    return {
        "expected_loss": expected_loss,
        f"var_{int(alpha*100)}": var,
        "tvar": tvar,
        "pml": var,
    }

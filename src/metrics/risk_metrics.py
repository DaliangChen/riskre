import numpy as np

def compute_risk_metrics(payouts):
    expected_loss = np.mean(payouts)

    var_99 = np.quantile(payouts, 0.99)
    tvar_99 = payouts[payouts >= var_99].mean()

    pml_99 = var_99

    return {
        "expected_loss": expected_loss,
        "var_99": var_99,
        "tvar_99": tvar_99,
        "pml_99": pml_99
    }

import numpy as np
from models.loss_model import simulate_annual_loss
from reinsurance.xol import xol_payout


def run_simulation(config):
    n_sim = config["simulation"]["n_simulations"]
    retention = config["reinsurance"]["retention"]
    limit = config["reinsurance"]["limit"]

    payouts = np.zeros(n_sim)

    for i in range(n_sim):
        annual_losses = simulate_annual_loss(config)
        payout = sum(xol_payout(loss, retention, limit) for loss in annual_losses)
        payouts[i] = payout

    return payouts

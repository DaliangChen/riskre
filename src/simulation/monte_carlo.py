# src/simulation/monte_carlo.py

import numpy as np
from models.loss_model import simulate_annual_loss
from reinsurance.xol import xol_payout

def run_simulation(n_simulations, retention, limit):
    payouts = np.zeros(n_simulations)

    for i in range(n_simulations):
        annual_losses = simulate_annual_loss()
        payout = sum(xol_payout(loss, retention, limit) for loss in annual_losses)
        payouts[i] = payout

    return payouts

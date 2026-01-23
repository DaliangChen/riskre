import numpy as np
from numpy import ArrayLike
from models.loss_model import simulate_annual_loss
from src.xol import xol_payout
from config_loader import InsuranceConfig

def run_simulation(config: InsuranceConfig) -> np.ndarray:
    """
    run monte carlo simulation
    """
    n_sim = config.simulation.n_simulations
    retention = config.reinsurance.retention
    limit = config.reinsurance.limit

    payouts = np.zeros(n_sim)

    for i in range(n_sim):
        annual_losses = simulate_annual_loss(config)
        payout = sum(xol_payout(loss, config) for loss in annual_losses)
        payouts[i] = payout

    return payouts

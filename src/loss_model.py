from re import I
from models.frequency import sample_frequency
from models.severity import sample_severity
from config_loader import InsuranceConfig
import numpy as np

def simulate_annual_loss(config: InsuranceConfig) -> np.ndarray:
    n_events = sample_frequency(config)
    losses = sample_severity(n_events, config)
    return losses

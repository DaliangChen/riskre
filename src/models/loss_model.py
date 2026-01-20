# src/models/loss_model.py

import numpy as np
from models.frequency import sample_frequency
from models.severity import sample_severity

def simulate_annual_loss():
    """
    Simulate all loss events in one underwriting year
    """
    n_events = sample_frequency()
    losses = sample_severity(n_events)
    return losses

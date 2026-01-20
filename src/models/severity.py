# src/models/severity.py

import numpy as np

# Lognormal parameters
MU = 13.0
SIGMA = 1.0

def sample_severity(n_events):
    if n_events == 0:
        return []
    return np.random.lognormal(mean=MU, sigma=SIGMA, size=n_events)

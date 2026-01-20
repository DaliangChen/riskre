# src/models/frequency.py

import numpy as np

# Average number of claims per year
LAMBDA = 5

def sample_frequency():
    return np.random.poisson(LAMBDA)

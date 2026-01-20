import numpy as np

def sample_frequency(config):
    lam = config["frequency"]["lambda"]
    return np.random.poisson(lam)

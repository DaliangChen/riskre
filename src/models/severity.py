import numpy as np

def sample_severity(n_events, config):
    if n_events == 0:
        return []

    mu = config["severity"]["mu"]
    sigma = config["severity"]["sigma"]

    return np.random.lognormal(mean=mu, sigma=sigma, size=n_events)

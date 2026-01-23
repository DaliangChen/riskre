import numpy as np
from config_loader import SeverityConfig


def sample_severity(n_events: int, config: SeverityConfig) -> np.ndarray:
    if n_events == 0:
        return []

    mu = config.mu
    sigma = config.sigma

    return np.random.lognormal(mean=mu, sigma=sigma, size=n_events)

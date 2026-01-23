import numpy as np
from config_loader import FrequencyConfig


def sample_frequency(config: FrequencyConfig) -> int:
    lam = config.lam
    return np.random.poisson(lam)

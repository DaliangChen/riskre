from __future__ import annotations


import numpy as np
from abc import ABC, abstractmethod
from scipy.stats import lognorm


class SeverityModel(ABC):
    """
    Base class for claim severity models.

    A severity model simulates individual claim sizes.
    """

    @abstractmethod
    def simulate(self, n: int) -> np.ndarray[np.float64]:
        """
        Simulate n claim amounts.

        Returns
        -------
        np.ndarray
            Positive claim amounts
        """
        raise NotImplementedError

    @abstractmethod
    def mean(self) -> float:
        """
        Theoretical mean of the severity distribution.
        """
        raise NotImplementedError

    @abstractmethod
    def var(self) -> float:
        """
        Theoretical variance of the severity distribution.
        """
        raise NotImplementedError


class LognormalSeverity(SeverityModel):
    """
    Lognormal severity model.

    X ~ LogNormal(mu, sigma)
    where:
        ln(X) ~ Normal(mu, sigma^2)

    Parameters
    ----------
    mu : float
        Mean of log(X)
    sigma : float
        Standard deviation of log(X), must be > 0
    seed : int | None
        Random seed for reproducibility
    """

    def __init__(self, mu: float, sigma: float, seed: int | None = None):
        if sigma <= 0:
            raise ValueError("sigma must be > 0 for lognormal distribution")

        self.mu = float(mu)
        self.sigma = float(sigma)

        # random number generator
        self._rng = np.random.default_rng(seed)

        # scipy uses shape = sigma, scale = exp(mu)
        self._dist = lognorm(s=self.sigma, scale=np.exp(self.mu))

    def simulate(self, n: int) -> np.ndarray[np.float64]:
        if n <= 0:
            raise ValueError("n must be > 0")

        # generate samples using inverse transform sampling
        z: np.ndarray[np.float64] = self._rng.standard_normal(n)
        ret = np.exp(self.sigma * z + self.mu)
        return ret

    def mean(self) -> float:
        """
        E[X] = exp(mu + 0.5 * sigma^2)
        """
        return float(np.exp(self.mu + 0.5 * self.sigma**2))

    def var(self) -> float:
        """
        Var[X] = (exp(sigma^2) - 1) * exp(2*mu + sigma^2)
        """
        return float((np.exp(self.sigma**2) - 1) * np.exp(2 * self.mu + self.sigma**2))

    def quantile(self, q: float) -> float:
        """
        Quantile function (VaR at level q)
        """
        if not 0 < q < 1:
            raise ValueError("q must be in (0,1)")
        return float(self._dist.ppf(q))

    def __repr__(self) -> str:
        return f"LognormalSeverity(mu={self.mu}, sigma={self.sigma})"

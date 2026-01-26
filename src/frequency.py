from __future__ import annotations


import numpy as np
from abc import ABC, abstractmethod
from numpy import int64
from numpy.typing import NDArray


class FrequencyModel(ABC):
    """
    Base class for claim frequency models.

    A frequency model simulates the number of claims occurring in a single year.
    """

    @abstractmethod
    def simulate(self, n_years: int) -> np.ndarray[int64]:
        """
        Simulate claim counts for n_years.

        Returns
        -------
        np.ndarray
            Array of length n_years with non-negative integers
            representing number of claims per year.
        """
        raise NotImplementedError


class PoissonFrequency(FrequencyModel):
    """
    Poisson frequency model.

    N ~ Poisson(lambda)

    Parameters
    ----------
    lam : float
        Expected number of claims per year (λ > 0)
    seed : int | None
        Random seed for reproducibility
    """

    def __init__(self, lam: float, seed: int | None = None):
        if lam <= 0:
            raise ValueError("Poisson lambda must be > 0")

        self.lam = float(lam)
        self._rng = np.random.default_rng(seed)

    def simulate(self, n_years: int) -> np.ndarray[int64]:
        if n_years <= 0:
            raise ValueError("n_years must be > 0")

        return self._rng.poisson(lam=self.lam, size=n_years)

    def mean(self) -> float:
        """
        Theoretical mean of the Poisson distribution.
        """
        return self.lam

    def variance(self) -> float:
        """
        Theoretical variance of the Poisson distribution.
        """
        return self.lam

    def __repr__(self) -> str:
        return f"PoissonFrequency(lam={self.lam})"

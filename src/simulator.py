from __future__ import annotations

import numpy as np
from typing import Dict, Any
from numpy.typing import NDArray

from frequency import FrequencyModel
from severity import SeverityModel


class MonteCarloEngine:
    """
    Monte Carlo engine for reinsurance loss simulation.

    Pipeline:
        Frequency -> Severity -> Annual Loss -> XoL Treaty -> Risk Distribution
    """

    def __init__(
        self,
        freq_model: FrequencyModel,
        severity_model: SeverityModel,
        retention: float,
        limit: float,
    ):
        if retention < 0:
            raise ValueError("retention must be >= 0")
        if limit <= 0:
            raise ValueError("limit must be > 0")

        self.freq_model = freq_model
        self.severity_model = severity_model
        self.retention = float(retention)
        self.limit = float(limit)

    def run(self, n_years: int) -> Dict[str, np.ndarray[np.float64]]:
        """
        Run Monte Carlo simulation.

        Returns
        -------
        dict with keys:
            gross_losses: np.ndarray
            reinsurance_losses: np.ndarray
        """
        if n_years <= 0:
            raise ValueError("n_years must be > 0")

        # 1) simulate number of claims per year
        claim_counts = self.freq_model.simulate(n_years)

        gross_losses = np.zeros(n_years)
        reins_losses = np.zeros(n_years)

        # 2) simulate severity and apply treaty year by year
        for i, n_claims in enumerate(claim_counts):
            if n_claims == 0:
                continue

            # simulate claim severities for the year
            severities = self.severity_model.simulate(n_claims)
            annual_loss = severities.sum()

            gross_losses[i] = annual_loss
            reins_losses[i] = self._apply_xol(annual_loss)

        return {
            "gross_losses": gross_losses,
            "reinsurance_losses": reins_losses,
        }

    def _apply_xol(self, loss: float) -> float:
        """
        Apply Excess-of-Loss treaty:
            Pay min(max(loss - retention, 0), limit)
        """
        return float(min(max(loss - self.retention, 0.0), self.limit))

    @staticmethod
    def var(losses: np.ndarray[np.float64], q: float) -> float:
        """
        Value at Risk at level q.
        """
        if not 0 < q < 1:
            raise ValueError("q must be in (0,1)")
        return float(np.quantile(losses, q))

    @staticmethod
    def tvar(losses: np.ndarray[np.float64], q: float) -> float:
        """
        Tail Value at Risk (Expected Shortfall).
        """
        if not 0 < q < 1:
            raise ValueError("q must be in (0,1)")

        threshold = np.quantile(losses, q)
        tail_losses = losses[losses >= threshold]

        if len(tail_losses) == 0:
            return float(threshold)

        return float(tail_losses.mean())

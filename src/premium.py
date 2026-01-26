from __future__ import annotations

import numpy as np
from typing import Dict, Literal


RiskMeasure = Literal["expected_loss", "VaR", "TVaR", "PML"]


class PremiumCalculator:
    """
    Reinsurance premium calculator.

    Supports:
        - Expected Loss
        - Value at Risk (VaR)
        - Tail Value at Risk (TVaR)
        - Probable Maximum Loss (PML)
    """

    def __init__(
        self,
        expense_ratio: float,
        risk_measure: RiskMeasure,
        confidence_level: float | None = None,
        profit_loading: float = 0.0,
    ):
        if not 0 <= expense_ratio <= 1:
            raise ValueError("expense_ratio must be in [0,1]")

        if profit_loading < 0:
            raise ValueError("profit_loading must be >= 0")

        self.expense_ratio = float(expense_ratio)
        self.risk_measure = risk_measure
        self.confidence_level = confidence_level
        self.profit_loading = float(profit_loading)

    # -----------------------------
    # Core pricing
    # -----------------------------
    def calculate(self, losses: np.ndarray[np.float64]) -> Dict[str, float]:
        """
        Calculate premium based on simulated reinsurance losses.

        Returns
        -------
        dict with keys:
            risk_premium
            technical_premium
            commercial_premium
        """
        if losses.size == 0:
            raise ValueError("losses array is empty")

        risk_premium = self._risk_premium(losses)

        # Add expense loading
        technical_premium = risk_premium * (1.0 + self.expense_ratio)

        # Add profit loading
        commercial_premium = technical_premium * (1.0 + self.profit_loading)

        return {
            "risk_premium": float(risk_premium),
            "technical": float(technical_premium),
            "commercial": float(commercial_premium),
        }

    # -----------------------------
    # Risk measure logic
    # -----------------------------
    def _risk_premium(self, losses: np.ndarray[np.float64]) -> float:
        rm = self.risk_measure

        if rm == "expected_loss":
            return float(losses.mean())

        if rm in {"VaR", "TVaR"}:
            if self.confidence_level is None:
                raise ValueError("confidence_level required for VaR/TVaR")

            q = float(self.confidence_level)

            if rm == "VaR":
                return float(np.quantile(losses, q))

            # TVaR / Expected Shortfall
            threshold = np.quantile(losses, q)
            tail_losses = losses[losses >= threshold]

            if tail_losses.size == 0:
                return float(threshold)

            return float(tail_losses.mean())

        if rm == "PML":
            # Simple PML proxy: high quantile (e.g. 99.5%)
            return float(np.quantile(losses, 0.995))

        raise ValueError(f"Unsupported risk measure: {rm}")

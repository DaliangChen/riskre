from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional
import numpy as np
import pandas as pd


ModelType = Literal["poisson", "neg_binomial"]


@dataclass
class FrequencyParams:
    model: ModelType
    """Model type"""

    lambda_: Optional[float] = None
    """Poisson mean"""

    r: Optional[float] = None
    """NegBin shape"""

    p: Optional[float] = None
    """NegBin probability"""


class FrequencyModel:
    """
    Claim frequency model.
    Fits annual claim counts and simulates yearly number of claims.

    Supports:
    - Poisson
    - Negative Binomial (auto-selected when overdispersion detected)
    """

    def __init__(self, model: ModelType = "poisson"):
        self.model: ModelType = model
        """Model type"""

        self.params: Optional[FrequencyParams] = None  # fitted parameters
        """Fitted parameters"""

    def fit(
        self, claims_df: pd.DataFrame, date_col: str = "loss_date"
    ) -> FrequencyParams:
        """
        Fit model parameters using historical claims.

        Parameters
        ----------
        claims_df : DataFrame
            Must contain a date column.
        date_col : str
            Name of date column.

        Returns
        -------
        FrequencyParams
        """
        yearly_counts: pd.Series = self._aggregate_yearly_counts(claims_df, date_col)

        mean = yearly_counts.mean()
        var: float = yearly_counts.var(ddof=1)  # type: ignore

        # Auto-select model if not forced
        # TODO : more robust model selection
        model = self.model
        if self.model == "poisson":
            if var > mean * 1.2:  # simple overdispersion test
                model = "neg_binomial"

        if model == "poisson":
            params = self._fit_poisson(mean)
        else:
            params = self._fit_neg_binomial(mean, var)

        self.params = params
        return params

    def simulate(
        self, n_years: int = 1, random_state: Optional[int] = None
    ) -> np.ndarray[np.int_]:
        """
        Simulate number of claims per year.

        Returns
        -------
        np.ndarray
            Array of simulated claim counts
        """
        if self.params is None:
            raise RuntimeError("Model must be fitted before simulation")

        rng = np.random.default_rng(random_state)

        if self.params.model == "poisson":
            return rng.poisson(self.params.lambda_, size=n_years)

        elif self.params.model == "neg_binomial":
            # numpy uses n, p parameterization
            return rng.negative_binomial(self.params.r, self.params.p, size=n_years)

        else:
            raise ValueError(f"Unsupported model: {self.params.model}")

    def _aggregate_yearly_counts(self, df: pd.DataFrame, date_col: str) -> pd.Series:
        """
        Aggregate claims by year.

        Returns
        -------
        pd.Series
            Yearly claim counts
        """

        tmp = df.copy()
        tmp[date_col] = pd.to_datetime(tmp[date_col])  # type: ignore
        tmp["year"] = tmp[date_col].dt.year  # type: ignore

        yearly = tmp.groupby("year").size().sort_index()  # type: ignore

        if len(yearly) < 2:
            raise ValueError("Need at least 2 years of data to fit frequency model")

        return yearly

    def _fit_poisson(self, mean: float) -> FrequencyParams:
        return FrequencyParams(model="poisson", lambda_=float(mean))

    def _fit_neg_binomial(self, mean: float, var: float) -> FrequencyParams:
        """
        Method of moments estimation:
        Var = mean + mean^2 / r
        Solve for r, then p = r / (r + mean)
        """
        if var <= mean:
            # fallback to Poisson
            return self._fit_poisson(mean)

        r = mean**2 / (var - mean)
        p = r / (r + mean)

        return FrequencyParams(model="neg_binomial", r=float(r), p=float(p))

    def summary(self) -> FrequencyParams:
        """
        Return fitted parameters.
        """

        if self.params is None:
            raise RuntimeError("Model not fitted")

        return FrequencyParams(
            model=self.params.model,
            lambda_=self.params.lambda_,
            r=self.params.r,
            p=self.params.p,
        )

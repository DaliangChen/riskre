import yaml
from pathlib import Path
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Union


class SimulationConfig(BaseModel):
    """
    Configuration for Monte Carlo simulation

    Attributes:
        n_simulations: int, number of Monte Carlo runs
    """

    n_simulations: int = Field(gt=0)


class FrequencyConfig(BaseModel):
    """
    Configuration for frequency model

    Attributes:
        distribution: str, type of frequency distribution
        lam: float, expected number of claims per year
    """

    distribution: Literal["poisson", "exponential"]
    lam: float = Field(gt=0)


class LognormalSeverityConfig(BaseModel):
    """
    Configuration for lognormal severity model

    Attributes:
        distribution: str, type of severity distribution
        mu: float, mean of lognormal distribution
        sigma: float, standard deviation of lognormal distribution
    """

    distribution: Literal["lognormal"]
    mu: float
    sigma: float = Field(gt=0)


class ExponentialSeverityConfig(BaseModel):
    """
    Configuration for exponential severity model

    Attributes:
        distribution: str, type of severity distribution
        rate: float, rate of exponential distribution
    """

    distribution: Literal["exponential"]
    rate: float = Field(gt=0)


SeverityConfig = Union[LognormalSeverityConfig, ExponentialSeverityConfig]


class ReinsuranceConfig(BaseModel):
    """
    Configuration for reinsurance structure

    Attributes:
        type: str, type of reinsurance (e.g., XoL)
        retention: float, retention amount
        limit: float, limit amount
    """

    type: Literal["XoL"]
    retention: float = Field(ge=0)
    limit: float = Field(gt=0)


class PricingConfig(BaseModel):
    """
    Configuration for pricing model

    Attributes:
        expense_ratio: float, expense ratio for reinsurance
        risk_measure: str, risk measure to use
        confidence_level: float, confidence level for VaR/TVaR
    """

    expense_ratio: float = Field(ge=0, le=1)
    risk_measure: Literal["expected_loss", "VaR", "TVaR", "PML"]
    confidence_level: float = Field(gt=0, lt=1)


class InsuranceConfig(BaseModel):
    """
    Main configuration for reinsurance pricing system

    Attributes:
        simulation: SimulationConfig, configuration for simulation
        frequency: FrequencyConfig, configuration for frequency model
        severity: SeverityConfig, configuration for severity model
        reinsurance: ReinsuranceConfig, configuration for reinsurance structure
        pricing: PricingConfig, configuration for pricing model
    """

    simulation: SimulationConfig
    frequency: FrequencyConfig
    severity: SeverityConfig
    reinsurance: ReinsuranceConfig
    pricing: PricingConfig

    @model_validator(mode="after")
    def check_confidence_level(self) -> "InsuranceConfig":
        if self.pricing.risk_measure not in {"VaR", "TVaR"}:
            raise ValueError("confidence_level required for VaR/TVaR")
        return self


def load_config(path: str | Path = "config/base_config.yaml") -> InsuranceConfig:
    """
    Load and validate configuration from YAML file
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return InsuranceConfig.model_validate(data)

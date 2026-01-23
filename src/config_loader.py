import yaml
from pathlib import Path
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Union


# -----------------------------
# Simulation
# -----------------------------
class SimulationConfig(BaseModel):
    """
    Configuration for Monte Carlo simulation
    """

    n_simulations: int = Field(gt=0, description="Number of Monte Carlo runs")


# -----------------------------
# Frequency
# -----------------------------
class FrequencyConfig(BaseModel):
    """
    Configuration for frequency model
    """

    distribution: Literal["poisson", "exponential"]
    lam: float = Field(gt=0, description="Poisson lambda or exponential rate")


# -----------------------------
# Severity
# -----------------------------
class LognormalSeverityConfig(BaseModel):
    distribution: Literal["lognormal"]
    mu: float
    sigma: float = Field(gt=0)


class ExponentialSeverityConfig(BaseModel):
    distribution: Literal["exponential"]
    rate: float = Field(gt=0)


SeverityConfig = Union[LognormalSeverityConfig, ExponentialSeverityConfig]


# -----------------------------
# Reinsurance
# -----------------------------
class ReinsuranceConfig(BaseModel):
    """
    Configuration for reinsurance structure
    """

    type: Literal["XoL"]
    retention: float = Field(ge=0)
    limit: float = Field(gt=0)


# -----------------------------
# Pricing
# -----------------------------
class PricingConfig(BaseModel):
    """
    Configuration for pricing model
    """

    expense_ratio: float = Field(ge=0, le=1)
    risk_measure: Literal["expected_loss", "VaR", "TVaR", "PML"]
    confidence_level: float = Field(gt=0, lt=1)


# -----------------------------
# Main Config
# -----------------------------
class InsuranceConfig(BaseModel):
    """
    Main configuration for reinsurance pricing system
    """

    simulation: SimulationConfig
    frequency: FrequencyConfig
    severity: SeverityConfig
    reinsurance: ReinsuranceConfig
    pricing: PricingConfig

    @model_validator(mode="after")
    def check_confidence_level(self) -> "InsuranceConfig":
        if self.pricing.risk_measure in {"VaR", "TVaR"}:
            if self.pricing.confidence_level is None:
                raise ValueError("confidence_level required for VaR/TVaR")
        return self


# -----------------------------
# Loader
# -----------------------------
def load_config(path: str | Path = "config/base_config.yaml") -> InsuranceConfig:
    """
    Load and validate configuration from YAML file
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return InsuranceConfig.model_validate(data)

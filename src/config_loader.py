import yaml

import yaml
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Literal


class SimulationConfig(BaseModel):
    """
    configuration for simulation model
    """

    n_simulations: int


class FrequencyConfig(BaseModel):
    """
    configuration for frequency model
    """

    distribution: Literal["poisson", "exponential"]
    lam: int


class SeverityConfig(BaseModel):
    """
    configuration for severity model
    """

    distribution: Literal["lognormal", "exponential"]
    mu: float
    sigma: float


class ReinsuranceConfig(BaseModel):
    """
    configuration for reinsurance model
    """

    type: str
    retention: int
    limit: int


class PricingConfig(BaseModel):
    """
    configuration for pricing model
    """

    expense_ratio: float
    risk_measure: Literal["expected_loss", "VaR", "TVaR", "pml"]
    confidence_level: float


class InsuranceConfig(BaseModel):
    """
    main configuration for insurance model
    """

    simulation: SimulationConfig
    frequency: FrequencyConfig
    severity: SeverityConfig
    reinsurance: ReinsuranceConfig
    pricing: PricingConfig

    class Config:
        # allow populating by field name or alias
        populate_by_name = True


def load_config(path: str | Path = "config/base_config.yaml") -> InsuranceConfig:
    """
    load configuration from yaml file
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return InsuranceConfig.model_validate(data)

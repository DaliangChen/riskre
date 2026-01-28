from datetime import date
import os
from pydantic import BaseModel, Field, model_validator
import yaml


class ContractConfig(BaseModel):
    """
    Configuration for individual reinsurance contracts.
    """

    contract_id: str
    """Contract ID"""

    attachment_point: int = Field(gt=0)
    """Attachment Point"""

    limit: int = Field(gt=0)
    """Limit"""

    @model_validator(mode="after")
    def check_limits(self):
        if self.attachment_point > self.limit:
            raise ValueError("Attachment point cannot be greater than limit")
        return self


class ClaimGenerationConfig(BaseModel):
    """
    Configuration for claim generation.
    """

    n_claims: int = Field(gt=0)
    """Number of claims to generate"""

    start_date: date
    """Claim start date"""

    end_date: date
    """Claim end date"""

    contracts: list[ContractConfig]
    """List of contracts"""

    @model_validator(mode="after")
    def check_date_range(self):
        if self.start_date > self.end_date:
            raise ValueError("Start date cannot be after end date")
        return self


class ReConfiguration(BaseModel):
    """
    Overall reinsurance configuration.
    """

    claim_generation: ClaimGenerationConfig
    """Claim generation configuration"""


class ConfigLoader:
    """
    Configuration loader class.
    """

    def __init__(self, config_path: str = "config/assumptions.yaml") -> None:
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> ReConfiguration:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return ReConfiguration.model_validate(config)

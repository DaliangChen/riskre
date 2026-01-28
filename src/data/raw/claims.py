from dataclasses import dataclass
import pandas as pd
from config.config_loader import ClaimGenerationConfig
import numpy as np
from datetime import date, timedelta


np.random.seed(1)


@dataclass
class Claim:
    """
    Claim record structure.
    """

    policy_id: str
    """Policy ID"""

    contract_id: str
    """Contract ID"""

    loss_date: date
    """Loss Date"""

    loss_amount: float
    """Loss Amount"""

    attachment_point: int
    """Attachment Point"""

    limit: int
    """Limit"""

    exposure: float
    """Exposure Factor"""


class ClaimGenerator:
    """
    Claim generation class.
    """

    def __init__(self, config_loader: ClaimGenerationConfig):
        self.config: ClaimGenerationConfig = config_loader
        self.claims: list[Claim] = []

    def generate_claims(self) -> None:

        for i in range(self.config.n_claims):
            policy_id = f"P{i+1:04d}"
            contract = np.random.choice(self.config.contracts)
            contract_id = contract.contract_id
            attachment_point = contract.attachment_point
            limit = contract.limit

            # claim date randomly generated
            delta_days = (self.config.end_date - self.config.start_date).days
            loss_date = self.config.start_date + timedelta(
                days=np.random.randint(0, delta_days)
            )

            # generate loss amount (log-normal distribution with some heavy tail losses)
            if np.random.rand() < 0.1:
                # 10% heavy tail losses
                loss_amount = float(np.random.lognormal(mean=12, sigma=0.5))  # type: ignore
            else:
                # regular losses
                loss_amount = float(np.random.lognormal(mean=10, sigma=0.3))  # type: ignore

            # add exposure factor
            exposure: float = round(np.random.uniform(0.8, 1.2), 2)  # type: ignore

            self.claims.append(
                Claim(
                    policy_id=policy_id,
                    contract_id=contract_id,
                    loss_date=loss_date,
                    loss_amount=round(loss_amount, 2),
                    attachment_point=attachment_point,
                    limit=limit,
                    exposure=exposure,
                )
            )

        # save to csv
        df = pd.DataFrame(self.claims)
        df.to_csv("data/raw/claims.csv", index=False)

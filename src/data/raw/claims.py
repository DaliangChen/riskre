# -----------------------------
# 生成模拟赔案数据脚本 / Script to generate simulated claim data
# -----------------------------

import pandas as pd
from fontTools.ttLib import TypedDict
import numpy as np
from datetime import datetime, timedelta


# -----------------------------
# 配置参数 / config parameters
# -----------------------------

# 生成赔案数量 / number of claims to generate
n_claims = 5000


class Contract(TypedDict):
    """
    合同信息结构 / Docstring for Contract

    Attributes
    ----------
    contract_id : str
        合同编号 / Contract ID

    attachment_point : int
        起赔点 / Attachment Point
    limit : int
        赔偿限额 / Limit
    """

    contract_id: str
    attachment_point: int
    limit: int


# 合同列表 / list of contracts
contracts: list[Contract] = [
    {"contract_id": "C001", "attachment_point": 100000, "limit": 500000},
    {"contract_id": "C002", "attachment_point": 200000, "limit": 1000000},
]

# 赔案日期范围 / claim date range
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

# -----------------------------
# 生成赔案 / generate claims
# -----------------------------
np.random.seed(42)


class Claim(TypedDict):
    """
    赔案信息结构 / Docstring for Claim

    Attributes
    ----------
    policy_id : str
        保单编号 / Policy ID

    contract_id : str
        合同编号 / Contract ID

    loss_date : str
        赔案日期 / Loss Date

    loss_amount : float
        损失金额 / Loss Amount

    attachment_point : int
        起赔点 / Attachment Point

    limit : int
        赔偿限额 / Limit

    exposure : float
        权重因子 / Exposure Factor
    """

    policy_id: str
    contract_id: str
    loss_date: str
    loss_amount: float
    attachment_point: int
    limit: int
    exposure: float


# 生成赔案列表 / generate list of claims
claims: list[Claim] = []

for i in range(n_claims):
    policy_id = f"P{i+1:04d}"
    contract = np.random.choice(contracts)
    contract_id = contract["contract_id"]
    attachment_point = contract["attachment_point"]
    limit = contract["limit"]

    # 赔案日期随机 / claim date randomly generated
    delta_days = (end_date - start_date).days
    loss_date = start_date + timedelta(days=np.random.randint(0, delta_days))

    # 生成损失金额（对数正态分布，部分尾部大额损失）/ generate loss amount (log-normal distribution with some heavy tail losses)
    if np.random.rand() < 0.1:
        # 10% 尾部大额损失 / 10% heavy tail losses
        loss_amount = float(np.random.lognormal(mean=12, sigma=0.5))  # type: ignore
    else:
        # 普通损失 / regular losses
        loss_amount = float(np.random.lognormal(mean=10, sigma=0.3))  # type: ignore

    # 加入暴露因子 / add exposure factor
    exposure: float = round(np.random.uniform(0.8, 1.2), 2)  # type: ignore

    claims.append(
        {
            "policy_id": policy_id,
            "contract_id": contract_id,
            "loss_date": loss_date.strftime("%Y-%m-%d"),
            "loss_amount": round(loss_amount, 2),
            "attachment_point": attachment_point,
            "limit": limit,
            "exposure": exposure,
        }
    )

# -----------------------------
# 保存 CSV 文件 / save to CSV file
# -----------------------------
df = pd.DataFrame(claims)
df.to_csv("data/raw/claims.csv", index=False)
print("claims.csv 已生成，示例记录如下 / example records:")
print(df.head())

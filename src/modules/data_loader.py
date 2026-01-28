import pandas as pd
import os
from datetime import datetime


class DataManager:
    def __init__(
        self,
        raw_data_path: str = "data/raw",
        cleaned_data_path: str = "data/cleaned",
    ):
        # 数据路径 / data paths
        self.raw_data_path = raw_data_path
        self.cleaned_data_path = cleaned_data_path

        # 确保目录存在 / ensure directories exist
        os.makedirs(self.cleaned_data_path, exist_ok=True)

    def load_data(self, filename: str) -> pd.DataFrame:
        path = os.path.join(self.raw_data_path, filename)
        if filename.endswith(".csv"):
            df: pd.DataFrame = pd.read_csv(path)  # type: ignore
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            df: pd.DataFrame = pd.read_excel(path)  # type: ignore
        else:
            raise ValueError("Unsupported file type")
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # 删除重复记录 / remove duplicates
        df = df.drop_duplicates()

        # 删除关键字段缺失的记录 / remove records with missing critical fields
        df = df.dropna(subset=["policy_id", "loss_amount", "loss_date"])  # type: ignore

        # 确保损失金额为非负数 / ensure loss amount is non-negative
        df["loss_amount"] = df["loss_amount"].clip(lower=0)  # type: ignore

        # 转换日期字段为 datetime 类型 / convert date fields to datetime type
        df["loss_date"] = pd.to_datetime(df["loss_date"])  # type: ignore
        return df

    def save_snapshot(self, df: pd.DataFrame, name_prefix: str = "snapshot") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name_prefix}_{timestamp}.csv"
        path = os.path.join(self.cleaned_data_path, filename)
        df.to_csv(path, index=False)
        return path

    def export_for_modeling(self, df: pd.DataFrame) -> pd.DataFrame:
        df_model = df.copy()

        # 示例：计算每年总损失 / example: calculate annual total losses
        df_model["year"] = df_model["loss_date"].dt.year  # type: ignore
        annual_losses: pd.DataFrame = (
            df_model.groupby("year")["loss_amount"].sum().reset_index()  # type: ignore
        )
        return annual_losses


if __name__ == "__main__":
    manager = DataManager()
    df_raw = manager.load_data("claims.csv")
    df_clean = manager.clean_data(df_raw)
    snapshot_path = manager.save_snapshot(df_clean)
    df_model = manager.export_for_modeling(df_clean)

    print(f"Cleaned data saved to: {snapshot_path}")
    print(df_model.head())

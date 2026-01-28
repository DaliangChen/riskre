import pandas as pd
import os
from datetime import datetime


class DataManager:
    """
    Data management class.
    """

    def __init__(
        self,
        raw_data_path: str = "data/raw",
        cleaned_data_path: str = "data/cleaned",
    ):
        # data paths
        self.raw_data_path = raw_data_path
        self.cleaned_data_path = cleaned_data_path

        # ensure directories exist
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
        # remove duplicates
        df = df.drop_duplicates()

        # remove records with missing critical fields
        df = df.dropna(subset=["policy_id", "loss_amount", "loss_date"])  # type: ignore

        # ensure loss amount is non-negative
        df["loss_amount"] = df["loss_amount"].clip(lower=0)  # type: ignore

        # convert date fields to datetime type
        df["loss_date"] = pd.to_datetime(df["loss_date"])  # type: ignore
        return df

    def save_snapshot(self, df: pd.DataFrame, name_prefix: str = "snapshot") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name_prefix}_{timestamp}.csv"
        path = os.path.join(self.cleaned_data_path, filename)
        df.to_csv(path, index=False)
        return path

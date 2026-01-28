from config.config_loader import ConfigLoader
from data.raw.claims import ClaimGenerator
from modules.data_loader import DataManager


def main() -> None:

    # load configuration
    config_loader = ConfigLoader()

    # generate claims
    claim_generator = ClaimGenerator(config_loader.config.claim_generation)
    claim_generator.generate_claims()

    # data management
    manager = DataManager()
    df_raw = manager.load_data("claims.csv")
    df_clean = manager.clean_data(df_raw)
    snapshot_path = manager.save_snapshot(df_clean)
    df_model = manager.export_for_modeling(df_clean)

    print(f"Cleaned data saved to: {snapshot_path}")
    # print(df_model.head())


if __name__ == "__main__":
    main()

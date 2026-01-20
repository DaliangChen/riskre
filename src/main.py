from config_loader import load_config
from simulation.monte_carlo import run_simulation
from metrics.risk_metrics import compute_risk_metrics
from pricing.pricing import calculate_premium

def main():
    config = load_config()

    print("Running Monte Carlo simulation...")
    payouts = run_simulation(config)

    metrics = compute_risk_metrics(
        payouts,
        alpha=config["pricing"]["confidence_level"]
    )

    premium = calculate_premium(
        expected_loss=metrics["expected_loss"],
        tvar=metrics["tvar"],
        expense_ratio=config["pricing"]["expense_ratio"]
    )

    print("\n=== Reinsurance Risk Metrics ===")
    for k, v in metrics.items():
        print(f"{k}: {v:,.2f}")

    print("\n=== Pricing ===")
    print(f"Technical Premium: {premium:,.2f}")

if __name__ == "__main__":
    main()

from simulation.monte_carlo import run_simulation
from metrics.risk_metrics import compute_risk_metrics
from pricing.pricing import calculate_premium

def main():
    # Simulation parameters
    n_simulations = 50000

    # Reinsurance contract
    retention = 1_000_000
    limit = 4_000_000

    print("Running Monte Carlo simulation...")
    payouts = run_simulation(
        n_simulations=n_simulations,
        retention=retention,
        limit=limit
    )

    print("Computing risk metrics...")
    metrics = compute_risk_metrics(payouts)

    premium = calculate_premium(
        expected_loss=metrics["expected_loss"],
        tvar=metrics["tvar_99"],
        expense_ratio=0.05
    )

    print("\n=== Reinsurance Risk Metrics ===")
    for k, v in metrics.items():
        print(f"{k}: {v:,.2f}")

    print("\n=== Pricing ===")
    print(f"Technical Premium: {premium:,.2f}")

if __name__ == "__main__":
    main()

import config_loader as cfg
from frequency import PoissonFrequency
from premium import PremiumCalculator
from severity import LognormalSeverity
from simulator import FrequencyModel, MonteCarloEngine, SeverityModel
from pdf_report import PricingReportGenerator


def build_frequency(cfg: cfg.FrequencyConfig) -> FrequencyModel:
    if cfg.distribution == "poisson":
        return PoissonFrequency(cfg.lam)
    raise ValueError("Unsupported frequency model")


def build_severity(cfg: cfg.SeverityConfig) -> SeverityModel:
    if cfg.distribution == "lognormal":
        return LognormalSeverity(cfg.mu, cfg.sigma)
    raise ValueError("Unsupported severity model")


def main() -> None:
    # Load configuration
    config: cfg.InsuranceConfig = cfg.load_config()

    # Build models
    freq_model = build_frequency(config.frequency)
    sev_model = build_severity(config.severity)

    engine = MonteCarloEngine(
        freq_model=freq_model,
        severity_model=sev_model,
        retention=config.reinsurance.retention,
        limit=config.reinsurance.limit,
    )

    results = engine.run(config.simulation.n_simulations)

    pricing = PremiumCalculator(
        expense_ratio=config.pricing.expense_ratio,
        risk_measure=config.pricing.risk_measure,
        confidence_level=config.pricing.confidence_level,
    )

    premium = pricing.calculate(results["reinsurance_losses"])

    print("\n--- REINSURANCE PRICING REPORT ---")
    print(f"Expected Loss: {results['reinsurance_losses'].mean():,.0f}")
    print(f"Technical Premium: {premium['technical']:,.0f}")
    print(f"Commercial Premium: {premium['commercial']:,.0f}")

    reporter = PricingReportGenerator()

    pdf_path = reporter.generate(
        config=config,
        results=results,
        pricing=premium,
        filename="reinsurance_pricing_report.pdf",
    )

    print(f"PDF report generated at: {pdf_path}")


if __name__ == "__main__":
    main()

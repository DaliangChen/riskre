from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from config_loader import InsuranceConfig
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


class PricingReportGenerator:
    """
    Generates a PDF pricing report for reinsurance contracts.
    """

    def __init__(self, output_dir: str | Path = "reports_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # Public API
    # -----------------------------
    def generate(
        self,
        config: InsuranceConfig,
        results: Any,
        pricing: Any,
        filename: str = "pricing_report.pdf",
    ) -> Path:
        """
        Generate PDF report.

        Parameters
        ----------
        config : dict
            Configuration dictionary (YAML loaded)
        results : dict
            Simulation results (gross_losses, reinsurance_losses)
        pricing : dict
            Pricing output (risk_premium, technical, commercial)
        """
        pdf_path = self.output_dir / filename

        doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
        styles = getSampleStyleSheet()

        elements = []

        # -----------------------------
        # Title
        # -----------------------------
        title = Paragraph("Reinsurance Pricing & Risk Report", styles["Title"])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # -----------------------------
        # Contract Summary
        # -----------------------------
        elements.append(Paragraph("1. Contract Summary", styles["Heading2"]))

        reins = config.reinsurance
        summary_data = [
            ["Treaty Type", reins.type],
            ["Retention", f"{reins.retention:,.0f}"],
            ["Limit", f"{reins.limit:,.0f}"],
            ["Simulations", str(config.simulation.n_simulations)],
        ]

        table = Table(summary_data, hAlign="LEFT")
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ]
            )
        )
        elements.append(table)
        elements.append(Spacer(1, 12))

        # -----------------------------
        # Model Assumptions
        # -----------------------------
        elements.append(Paragraph("2. Model Assumptions", styles["Heading2"]))

        freq = config.frequency
        sev = config.severity
        pricing_cfg = config.pricing

        assumptions_text = f"""
        <b>Frequency Model:</b> {freq.distribution} (λ = {freq.lam})<br/>
        <b>Severity Model:</b> {sev.distribution} (μ = {getattr(sev, 'mu', '-')}, σ = {getattr(sev, 'sigma', '-')})<br/>
        <b>Risk Measure:</b> {pricing_cfg.risk_measure} at {pricing_cfg.confidence_level}
        """

        elements.append(Paragraph(assumptions_text, styles["Normal"]))
        elements.append(Spacer(1, 12))

        # -----------------------------
        # Loss Distribution Plot
        # -----------------------------
        elements.append(Paragraph("3. Loss Distribution", styles["Heading2"]))

        plot_path = self._plot_distribution(results["reinsurance_losses"])
        elements.append(Image(str(plot_path), width=400, height=250))
        elements.append(Spacer(1, 12))

        # -----------------------------
        # Risk Metrics
        # -----------------------------
        elements.append(Paragraph("4. Risk & Pricing Metrics", styles["Heading2"]))

        risk_data = [
            ["Metric", "Value"],
            ["Risk Premium", f"{pricing['risk_premium']:,.0f}"],
            ["Technical Premium", f"{pricing['technical']:,.0f}"],
            ["Commercial Premium", f"{pricing['commercial']:,.0f}"],
        ]

        risk_table = Table(risk_data, hAlign="LEFT")
        risk_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ]
            )
        )
        elements.append(risk_table)

        # -----------------------------
        # Build PDF
        # -----------------------------
        doc.build(elements)

        return pdf_path

    # -----------------------------
    # Plot helper
    # -----------------------------
    def _plot_distribution(self, losses: np.ndarray) -> Path:
        """
        Plot loss distribution histogram and return image path.
        """
        img_path = self.output_dir / "loss_distribution.png"

        plt.figure(figsize=(6, 4))
        plt.hist(losses, bins=50, density=True)
        plt.title("Reinsurance Loss Distribution")
        plt.xlabel("Annual Loss")
        plt.ylabel("Density")
        plt.tight_layout()
        plt.savefig(img_path)
        plt.close()

        return img_path

## 📌 Reinsurance Pricing & Risk Simulation System (Mini)

### Author

Daliang Chen
Frankfurt, Germany

---

## 1. Project Overview

This project implements a **Monte Carlo–based reinsurance pricing and risk simulation system**
for **Excess of Loss (XoL)** reinsurance treaties.

The system is designed as a **minimal yet realistic prototype**, reflecting
how reinsurance pricing and risk assessment are performed in practice.

---

## 2. Business Background

In non-life insurance, insurers transfer part of their risk exposure to reinsurers
via **Excess of Loss (XoL)** treaties.

Under a typical XoL contract:

- The reinsurer covers losses **above a predefined retention**
- Up to a maximum **limit**

Accurate pricing of such treaties requires:

- Stochastic modeling of loss frequency and severity
- Monte Carlo simulation of annual aggregate losses
- Risk-based premium calculation

---

## 3. Modeling Assumptions

### 3.1 Loss Frequency

- Annual number of loss events follows a **Poisson distribution**
  - For a random variable $X$ following a Poisson distribution with parameter $\lambda$, the probability of observing exactly $k$ events is given by:
    $$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$
    **$\lambda$ (Lambda)**: The **average number** of events occurring per unit of time or space (the expected value).

### 3.2 Loss Severity

- Individual loss amounts follow a **Lognormal distribution**
  - For a random variable $X$ following a Lognormal distribution with parameters $\mu$ and $\sigma$ (where $X > 0$), the probability density function is:
    $$f(x) = \frac{1}{x\sigma\sqrt{2\pi}} \exp\left( -\frac{(\ln x - \mu)^2}{2\sigma^2} \right)$$

    **$x$**: The value of the random variable (must be greater than 0).  
    **$\mu$ (Mu)**: The mean of the variable's natural logarithm ($\ln X$).  
    **$\sigma$ (Sigma)**: The standard deviation of the variable's natural logarithm ($\ln X$).

### 3.3 Independence

- Loss events are assumed to be independent

These assumptions are commonly used as a **first-order approximation**
in reinsurance pricing and portfolio risk analysis.

---

## 4. Reinsurance Contract Structure

**Excess of Loss (XoL):**

```text
Retention (Attachment Point): 1,000,000
Limit:                        4,000,000
```

Reinsurance payout per loss:

```text
payout = min(max(loss − retention, 0), limit)
```

---

## 5. Simulation Framework

- Monte Carlo simulation with configurable number of scenarios
- Each scenario represents **one underwriting year**
- For each year:
  1. Generate loss events
  2. Aggregate original losses
  3. Apply XoL contract
  4. Record reinsurance payouts

---

## 6. Risk Metrics

The system computes key reinsurance risk indicators:

- **Expected Loss (EL)**
- **Value at Risk (VaR)**
- **Tail Value at Risk (TVaR)**
- **Probable Maximum Loss (PML)**
- **Rate on Line (RoL)**

These metrics are commonly used for:

- Treaty pricing
- Capital allocation
- Risk management and regulatory reporting

---

## 7. Pricing Logic

Reinsurance premium is calculated as:

```text
Premium = Expected Loss × (1 + Risk Loading) + Expenses
```

Risk loading is derived from tail risk measures (e.g. TVaR).

---

## 8. How to Run

```bash
pip install -r requirements.txt
python src/main.py
```

Simulation results will be printed to the console
and optionally exported to `output/results.csv`.

---

## 9. Limitations & Extensions

This mini system is intentionally simplified:

- No dependency modeling (e.g. copulas)
- No multi-layer or reinstatement structures
- No capital optimization

Possible extensions:

- Multi-layer reinsurance programs
- Catastrophe loss modeling
- Capital-based pricing (Solvency II)

---

## 10. Purpose of the Project

This project is created as a **professional portfolio piece**,
demonstrating the ability to:

- Translate reinsurance business concepts into quantitative models
- Implement risk simulations in production-quality code
- Bridge actuarial thinking and software engineering

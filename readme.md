# BondPricer

A Python application to compute the price, duration, convexity, and yield-to-maturity (YTM) of a **vanilla coupon-bearing bond**. The project also includes unit tests for validation and an example script (`main.py`) for repricing scenarios.

---

## Features

1. **Bond Class** (`app/Bond.py`)
   - **Price Calculation**: Discount each coupon and principal repayment by a given yield.
   - **Macaulay Duration & Modified Duration**: Measures of interest rate risk.
   - **Convexity**: Second-order measure of interest rate risk.
   - **Compute YTM**: Numerical root-finding (Brent’s method).The compute_ytm method is provided as an additional tool. You'd use it when you have a given market price and want to determine what yield (YTM) would make the         calculated price equal to that market price. In other words, it's useful for "back-solving" for yield if you know the market price of the bond.

2. **Scenario Analysis** (`main.py`)
   - Demonstrates how to reprice a bond at different yield levels.
   - Prints bond price, duration, and convexity for each scenario.

3. **Unit Tests** (`tests/test_bond.py`)
   - Validates bond pricing and modified duration against known textbook examples.
   - Easy to extend for additional tests (e.g., Macaulay duration, convexity).

---


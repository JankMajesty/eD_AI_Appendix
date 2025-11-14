"""
Durbin-Watson Independence Test for Model m4 Residuals
Prompt 61 [PYTHON]

This script tests for autocorrelation in the residuals of model m4,
checking the independence assumption of linear regression.
"""

import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.stattools import durbin_watson

# Load cleaned data
housing_clean = pd.read_csv('housing_clean.csv')

# Recreate model m4
m4_formula = ('log_SalePrice ~ log_OverallQual + GrLivArea + log_YearBuilt + '
              'Q("YearRemod/Add") + TotalBsmtSF + Fireplaces + '
              'GarageArea + BsmtFullBath + LotArea + GarageCars')

m4 = smf.ols(m4_formula, data=housing_clean).fit()

# Calculate Durbin-Watson statistic
residuals = m4.resid
dw_stat = durbin_watson(residuals)

print("\n" + "="*70)
print("DURBIN-WATSON TEST: Independence of Residuals")
print("="*70)
print(f"\nDurbin-Watson statistic: {dw_stat:.4f}")

print("\n" + "-"*70)
print("INTERPRETATION GUIDE:")
print("-"*70)
print("  DW ≈ 2:      No autocorrelation (ideal)")
print("  DW < 1.5:    Positive autocorrelation (residuals are correlated)")
print("  DW > 2.5:    Negative autocorrelation (residuals anti-correlated)")
print("  1.5 ≤ DW ≤ 2.5: Acceptable range (independence assumption met)")

print("\n" + "-"*70)
print("ASSESSMENT:")
print("-"*70)

if 1.5 <= dw_stat <= 2.5:
    print(f"✓ GOOD: DW = {dw_stat:.4f} falls in acceptable range [1.5, 2.5]")
    print("  Residuals show no concerning autocorrelation.")
    print("  Independence assumption is adequately met.")
elif dw_stat < 1.5:
    print(f"⚠ CONCERN: DW = {dw_stat:.4f} < 1.5")
    print("  Positive autocorrelation detected.")
    print("  Residuals from nearby observations are correlated.")
    print("  This may indicate missing time/spatial variables.")
else:  # dw_stat > 2.5
    print(f"⚠ CONCERN: DW = {dw_stat:.4f} > 2.5")
    print("  Negative autocorrelation detected (rare).")
    print("  May indicate model misspecification.")

print("\n" + "="*70)
print("EXPLANATION FOR INSTRUCTOR:")
print("="*70)
print("The Durbin-Watson test checks whether residuals are independent")
print("(not correlated with each other). In housing data, correlation could")
print("arise from spatial clustering (neighboring homes) or temporal trends")
print("(market cycles). A DW near 2 indicates residuals are independent,")
print("validating our regression assumptions.")
print("="*70)

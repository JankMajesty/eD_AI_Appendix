"""
VIF Multicollinearity Diagnostics for Model m4
Prompt 59 [PYTHON]

This script calculates Variance Inflation Factor (VIF) for all 10 predictors
in model m4 to check for multicollinearity issues.
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Load cleaned data
housing_clean = pd.read_csv('housing_clean.csv')

# Recreate model m4 to get the design matrix
m4_formula = ('log_SalePrice ~ log_OverallQual + GrLivArea + log_YearBuilt + '
              'Q("YearRemod/Add") + TotalBsmtSF + Fireplaces + '
              'GarageArea + BsmtFullBath + LotArea + GarageCars')

m4 = smf.ols(m4_formula, data=housing_clean).fit()

# Calculate VIF for each predictor
vif_data = pd.DataFrame()
vif_data["Variable"] = m4.model.exog_names[1:]  # Exclude intercept
vif_data["VIF"] = [variance_inflation_factor(m4.model.exog, i)
                   for i in range(1, m4.model.exog.shape[1])]

# Sort by VIF descending to show highest concerns first
vif_data = vif_data.sort_values("VIF", ascending=False)

# Display results
print("\n" + "="*70)
print("MULTICOLLINEARITY DIAGNOSTICS: VIF Analysis for Model m4")
print("="*70)
print("\n" + vif_data.to_string(index=False))

print("\n" + "-"*70)
print("INTERPRETATION GUIDE:")
print("-"*70)
print("  VIF < 5:   No multicollinearity concern (ideal)")
print("  VIF 5-10:  Moderate multicollinearity (monitor)")
print("  VIF > 10:  Severe multicollinearity (consider removing variable)")

print("\n" + "-"*70)
print("ASSESSMENT:")
print("-"*70)

max_vif = vif_data["VIF"].max()
high_vif_count = (vif_data["VIF"] > 10).sum()
moderate_vif_count = ((vif_data["VIF"] >= 5) & (vif_data["VIF"] <= 10)).sum()

if max_vif < 5:
    print("✓ EXCELLENT: All VIF values < 5. No multicollinearity detected.")
    print("  Model m4 predictors are sufficiently independent.")
elif max_vif < 10:
    print(f"✓ ACCEPTABLE: Maximum VIF = {max_vif:.2f} (< 10).")
    print(f"  {moderate_vif_count} variable(s) with moderate VIF (5-10), but within acceptable range.")
    print("  No action required. Coefficient estimates remain reliable.")
else:
    print(f"⚠ CONCERN: {high_vif_count} variable(s) with VIF > 10.")
    print("  Consider removing highly correlated predictors or using Ridge regression.")
    print("\nVariables with VIF > 10:")
    print(vif_data[vif_data["VIF"] > 10]["Variable"].tolist())

print("\n" + "="*70)
print("Note: This addresses the Kaggle OLS reference in CLAUDE.md which")
print("emphasizes multicollinearity detection as a best practice.")
print("="*70)

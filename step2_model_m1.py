"""
Step Two - Prompt 38: Baseline Model (m1)
Single predictor regression to establish baseline performance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf

# Set styling
sns.set_theme(style="whitegrid", palette="colorblind")

print("="*80)
print("PROMPT 38 [PYTHON]: BASELINE MODEL (m1)")
print("="*80)

# Load cleaned data
housing_clean = pd.read_csv('housing_clean.csv')
print(f"\nLoaded cleaned dataset: {housing_clean.shape[0]} observations")

# ============================================================================
# BUILD MODEL m1: log_SalePrice ~ GrLivArea
# ============================================================================
print("\n\n1. BUILDING BASELINE MODEL (m1)")
print("-"*80)
print("Model specification: log_SalePrice ~ GrLivArea")
print("\nWHY this model?")
print("  - GrLivArea (above-grade living area in sq ft) is the most intuitive price predictor")
print("  - This establishes our baseline: how much variance can ONE variable explain?")
print("  - Note: Response is log-transformed but predictor is NOT (semi-log model)\n")

# Fit model
m1 = smf.ols('log_SalePrice ~ GrLivArea', data=housing_clean).fit()

# Display summary
print(m1.summary())

# ============================================================================
# INTERPRET RESULTS
# ============================================================================
print("\n\n2. INTERPRETING MODEL m1 RESULTS")
print("="*80)

# R-squared
r2 = m1.rsquared
adj_r2 = m1.rsquared_adj
print(f"\nR² = {r2:.4f} ({r2*100:.2f}%)")
print(f"Adjusted R² = {adj_r2:.4f} ({adj_r2*100:.2f}%)")
print(f"\nInterpretation: GrLivArea alone explains {r2*100:.1f}% of the variance in")
print(f"                log(SalePrice). This is our baseline to beat.")

# Coefficient
coef_grliv = m1.params['GrLivArea']
pval_grliv = m1.pvalues['GrLivArea']
print(f"\n\nCoefficient for GrLivArea: {coef_grliv:.6f}")
print(f"p-value: {pval_grliv:.2e} (highly significant!)")
print(f"\nInterpretation (semi-log model):")
print(f"  - For each additional square foot of living area, the sale price")
print(f"    increases by approximately {coef_grliv*100:.3f}%")
print(f"  - Example: A 100 sq ft increase → {coef_grliv*100*100:.2f}% price increase")
print(f"  - For a $150,000 home, 100 more sq ft → ${150000 * coef_grliv * 100:,.0f} higher price")

# Why semi-log interpretation?
print(f"\n\nWHY this interpretation?")
print(f"  When the response is log(Y) but predictor X is NOT logged, we have a semi-log model.")
print(f"  The coefficient β means: a 1-unit increase in X leads to a (β × 100)% change in Y.")
print(f"  This is different from a simple linear model where we'd interpret it as dollar change!")

# Intercept
intercept = m1.params['Intercept']
print(f"\n\nIntercept: {intercept:.4f}")
print(f"Interpretation: When GrLivArea = 0 (nonsensical), log(SalePrice) = {intercept:.4f}")
print(f"                This is not meaningful in practice (no home has 0 sq ft!)")
print(f"                The intercept anchors the regression line but isn't substantively interesting.")

# ============================================================================
# VISUALIZE MODEL FIT
# ============================================================================
print("\n\n3. VISUALIZING MODEL FIT")
print("-"*80)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left plot: Scatterplot with regression line
axes[0].scatter(housing_clean['GrLivArea'], housing_clean['log_SalePrice'],
                alpha=0.3, s=20, edgecolors='none')
axes[0].plot(housing_clean['GrLivArea'], m1.fittedvalues,
             color='red', linewidth=2, label=f'Fitted line (R² = {r2:.3f})')
axes[0].set_xlabel('Above-Grade Living Area (sq ft)', fontweight='bold')
axes[0].set_ylabel('log(Sale Price)', fontweight='bold')
axes[0].set_title('Model m1: log(SalePrice) vs GrLivArea', fontweight='bold', fontsize=14)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Right plot: Residuals vs Fitted (quick diagnostic)
axes[1].scatter(m1.fittedvalues, m1.resid, alpha=0.3, s=20, edgecolors='none')
axes[1].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Fitted Values', fontweight='bold')
axes[1].set_ylabel('Residuals', fontweight='bold')
axes[1].set_title('Residuals vs Fitted Values', fontweight='bold', fontsize=14)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('model_m1_visualization.png', dpi=300, bbox_inches='tight')
print("Saved: model_m1_visualization.png")

# ============================================================================
# SUMMARY AND NEXT STEPS
# ============================================================================
print("\n\n4. MODEL m1 SUMMARY")
print("="*80)
print(f"Model:           log_SalePrice ~ GrLivArea")
print(f"Observations:    {m1.nobs:.0f}")
print(f"R²:              {r2:.4f} ({r2*100:.2f}%)")
print(f"Adjusted R²:     {adj_r2:.4f}")
print(f"AIC:             {m1.aic:.2f}")
print(f"\nKey Finding:")
print(f"  Living area alone explains {r2*100:.1f}% of price variation.")
print(f"  Each additional 100 sq ft increases price by ~{coef_grliv*100*100:.2f}%.")
print(f"\nNext Step:")
print(f"  Prompt 39 will add OverallQual to see how quality improves the model.")
print(f"  Target: Achieve ~70-75% R² with two variables.")

print("\n" + "="*80)
print("BASELINE MODEL COMPLETE - Ready for Prompt 39 (Model m2)")
print("="*80)

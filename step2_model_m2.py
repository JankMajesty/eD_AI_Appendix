"""
Step Two - Prompt 39: Two-Variable Model (m2)
Adding OverallQual to understand partial effects and log-log interpretation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf

# Set styling
sns.set_theme(style="whitegrid", palette="colorblind")

print("="*80)
print("PROMPT 39 [PYTHON]: TWO-VARIABLE MODEL (m2)")
print("="*80)

# Load cleaned data
housing_clean = pd.read_csv('housing_clean.csv')

# Build m1 for comparison
m1 = smf.ols('log_SalePrice ~ GrLivArea', data=housing_clean).fit()

# ============================================================================
# BUILD MODEL m2: log_SalePrice ~ GrLivArea + log_OverallQual
# ============================================================================
print("\n\n1. BUILDING TWO-VARIABLE MODEL (m2)")
print("-"*80)
print("Model specification: log_SalePrice ~ GrLivArea + log_OverallQual")
print("\nWHY add OverallQual?")
print("  - OverallQual (1-10 scale) measures material and finish quality")
print("  - Two homes with same square footage can have vastly different prices")
print("  - Quality captures the 'how nice' while area captures the 'how big'")
print("  - Professor noted: nonlinear relationship requires log transformation")
print("\nNote: BOTH SalePrice and OverallQual are logged (log-log model)\n")

# Fit model
m2 = smf.ols('log_SalePrice ~ GrLivArea + log_OverallQual', data=housing_clean).fit()

# Display summary
print(m2.summary())

# ============================================================================
# COMPARE TO m1
# ============================================================================
print("\n\n2. COMPARING m2 TO BASELINE m1")
print("="*80)

r2_m1 = m1.rsquared
r2_m2 = m2.rsquared
improvement = r2_m2 - r2_m1

print(f"\nR² Comparison:")
print(f"  m1 (GrLivArea only):           R² = {r2_m1:.4f} ({r2_m1*100:.2f}%)")
print(f"  m2 (GrLivArea + log_OverallQual): R² = {r2_m2:.4f} ({r2_m2*100:.2f}%)")
print(f"  Improvement:                    ΔR² = {improvement:.4f} ({improvement*100:.2f} percentage points)")
print(f"\nInterpretation: Adding OverallQual increased explained variance by {improvement*100:.1f}")
print(f"                percentage points, bringing us from {r2_m1*100:.1f}% to {r2_m2*100:.1f}%.")
print(f"                We're getting closer to the professor's 80% target!")

# ============================================================================
# COEFFICIENT CHANGES (Partial Effects)
# ============================================================================
print("\n\n3. UNDERSTANDING PARTIAL EFFECTS")
print("-"*80)

coef_grliv_m1 = m1.params['GrLivArea']
coef_grliv_m2 = m2.params['GrLivArea']
change = coef_grliv_m2 - coef_grliv_m1

print(f"\nGrLivArea coefficient:")
print(f"  In m1 (alone):                {coef_grliv_m1:.6f}")
print(f"  In m2 (with OverallQual):     {coef_grliv_m2:.6f}")
print(f"  Change:                       {change:.6f}")
print(f"\nWHY did the coefficient change?")
print(f"  In m1, GrLivArea got 'credit' for ALL variation it explains, including")
print(f"  variation that's actually due to quality (larger homes tend to be nicer).")
print(f"  In m2, GrLivArea only gets credit for the effect of size HOLDING quality constant.")
print(f"  This is called a PARTIAL EFFECT or CONDITIONAL EFFECT.")
print(f"\nThink of it this way:")
print(f"  m1 asks: 'How much more do bigger homes cost?'")
print(f"  m2 asks: 'How much more do bigger homes cost, AMONG homes of the same quality?'")

# ============================================================================
# INTERPRET LOG-LOG COEFFICIENT
# ============================================================================
print("\n\n4. INTERPRETING THE log_OverallQual COEFFICIENT (LOG-LOG MODEL)")
print("="*80)

coef_qual = m2.params['log_OverallQual']
pval_qual = m2.pvalues['log_OverallQual']

print(f"\nCoefficient for log_OverallQual: {coef_qual:.4f}")
print(f"p-value: {pval_qual:.2e} (highly significant!)")
print(f"\nInterpretation (log-log model / elasticity):")
print(f"  When BOTH variables are logged, the coefficient is an ELASTICITY.")
print(f"  It means: a 1% increase in OverallQual leads to a {coef_qual:.2f}% increase in SalePrice.")
print(f"\nExample:")
print(f"  - A home improves from quality 5 to 6 (20% increase in quality)")
print(f"  - Predicted price impact: {coef_qual:.2f} × 20 = {coef_qual * 20:.1f}% price increase")
print(f"  - For a $150,000 home: ${150000 * coef_qual * 0.20:,.0f} increase")
print(f"\nWHY is this called elasticity?")
print(f"  In economics, elasticity measures the % change in Y for a % change in X.")
print(f"  Log-log models give you elasticity directly as the coefficient!")

# ============================================================================
# VISUALIZE MODEL COMPARISON
# ============================================================================
print("\n\n5. VISUALIZING MODEL IMPROVEMENT")
print("-"*80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Top left: R² comparison
models = ['m1\n(GrLivArea)', 'm2\n(+ OverallQual)']
r2_values = [r2_m1, r2_m2]
colors = ['steelblue', 'darkorange']
bars = axes[0, 0].bar(models, r2_values, color=colors, alpha=0.7, edgecolor='black')
axes[0, 0].set_ylabel('R²', fontweight='bold')
axes[0, 0].set_title('Model R² Comparison', fontweight='bold', fontsize=12)
axes[0, 0].set_ylim(0, 1)
axes[0, 0].axhline(y=0.80, color='red', linestyle='--', linewidth=2, label='Target: 80%')
for bar, val in zip(bars, r2_values):
    height = bar.get_height()
    axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{val:.3f}\n({val*100:.1f}%)',
                    ha='center', va='bottom', fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Top right: Coefficient comparison for GrLivArea
coefs = [coef_grliv_m1, coef_grliv_m2]
bars = axes[0, 1].bar(models, coefs, color=colors, alpha=0.7, edgecolor='black')
axes[0, 1].set_ylabel('GrLivArea Coefficient', fontweight='bold')
axes[0, 1].set_title('Partial Effect: GrLivArea Coefficient Changes', fontweight='bold', fontsize=12)
for bar, val in zip(bars, coefs):
    height = bar.get_height()
    axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 0.00001,
                    f'{val:.6f}',
                    ha='center', va='bottom', fontweight='bold', fontsize=9)
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Bottom left: m1 residuals
axes[1, 0].scatter(m1.fittedvalues, m1.resid, alpha=0.3, s=20)
axes[1, 0].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1, 0].set_xlabel('Fitted Values', fontweight='bold')
axes[1, 0].set_ylabel('Residuals', fontweight='bold')
axes[1, 0].set_title(f'm1 Residuals (R² = {r2_m1:.3f})', fontweight='bold', fontsize=12)
axes[1, 0].grid(True, alpha=0.3)

# Bottom right: m2 residuals
axes[1, 1].scatter(m2.fittedvalues, m2.resid, alpha=0.3, s=20, color='darkorange')
axes[1, 1].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1, 1].set_xlabel('Fitted Values', fontweight='bold')
axes[1, 1].set_ylabel('Residuals', fontweight='bold')
axes[1, 1].set_title(f'm2 Residuals (R² = {r2_m2:.3f})', fontweight='bold', fontsize=12)
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('model_m2_comparison.png', dpi=300, bbox_inches='tight')
print("Saved: model_m2_comparison.png")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n\n6. MODEL m2 SUMMARY")
print("="*80)
print(f"Model:           log_SalePrice ~ GrLivArea + log_OverallQual")
print(f"Observations:    {m2.nobs:.0f}")
print(f"R²:              {r2_m2:.4f} ({r2_m2*100:.2f}%)")
print(f"Adjusted R²:     {m2.rsquared_adj:.4f}")
print(f"AIC:             {m2.aic:.2f}")
print(f"\nKey Findings:")
print(f"  1. R² improved from {r2_m1*100:.1f}% to {r2_m2*100:.1f}% (+ {improvement*100:.1f} percentage points)")
print(f"  2. GrLivArea coefficient decreased (partial effect): {coef_grliv_m1:.6f} → {coef_grliv_m2:.6f}")
print(f"  3. log_OverallQual elasticity: {coef_qual:.2f} (1% quality increase → {coef_qual:.2f}% price increase)")
print(f"\nConcept Mastery:")
print(f"  ✓ Partial effects: Why coefficients change when adding variables")
print(f"  ✓ Log-log interpretation: Elasticity for percentage changes")
print(f"  ✓ Model comparison: Tracking R² improvement")
print(f"\nNext Step:")
print(f"  Prompt 40 will add 3 more variables (location, basement, age) to reach ~80% R²")

print("\n" + "="*80)
print("TWO-VARIABLE MODEL COMPLETE - Ready for Prompt 40 (Model m3)")
print("="*80)

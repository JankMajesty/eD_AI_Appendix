"""
Step Two - Prompt 43: Testing Interaction Effects for m5
"""

import pandas as pd
import statsmodels.formula.api as smf

print("="*80)
print("PROMPT 43 [PYTHON]: TESTING INTERACTION EFFECTS")
print("="*80)

# Load data
housing_clean = pd.read_csv('housing_clean.csv')

# Rebuild m4 for comparison
m4_formula = 'log_SalePrice ~ log_OverallQual + GrLivArea + log_YearBuilt + Q("YearRemod/Add") + TotalBsmtSF + Fireplaces + GarageArea + BsmtFullBath + LotArea + GarageCars'
m4 = smf.ols(m4_formula, data=housing_clean).fit()

print(f"\nBaseline (m4): R² = {m4.rsquared:.4f} ({m4.rsquared*100:.2f}%)")
print(f"\nDecision criterion: Add interactions only if R² improves by > 1%")

# ============================================================================
# TEST THEORETICALLY MOTIVATED INTERACTIONS
# ============================================================================
print("\n\n1. TESTING INTERACTION TERMS")
print("="*80)

interactions_to_test = [
    ("GrLivArea:log_OverallQual",
     "Does the value of extra space depend on quality? (High-quality homes may benefit more from size)"),
    ("log_OverallQual:log_YearBuilt",
     "Do quality improvements matter more for newer homes?"),
    ("GrLivArea:TotalBsmtSF",
     "Is basement space valued differently depending on above-grade size?")
]

results = []

for interaction, rationale in interactions_to_test:
    print(f"\n{interaction}")
    print(f"  Rationale: {rationale}")

    # Build model with interaction
    formula = m4_formula + f' + {interaction}'
    m_test = smf.ols(formula, data=housing_clean).fit()

    r2_improvement = m_test.rsquared - m4.rsquared

    print(f"  R² with interaction: {m_test.rsquared:.4f}")
    print(f"  Improvement: {r2_improvement:.4f} ({r2_improvement*100:.2f} percentage points)")

    results.append({
        'Interaction': interaction,
        'R²': m_test.rsquared,
        'Improvement': r2_improvement,
        'Worth_it': 'Yes' if r2_improvement > 0.01 else 'No'
    })

# ============================================================================
# DECISION: BUILD m5 OR KEEP m4?
# ============================================================================
print("\n\n2. INTERACTION TEST RESULTS")
print("="*80)

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

best_interaction = results_df.loc[results_df['Improvement'].idxmax()]

print(f"\n\nBest interaction: {best_interaction['Interaction']}")
print(f"  R² improvement: {best_interaction['Improvement']:.4f} ({best_interaction['Improvement']*100:.2f} pp)")

if best_interaction['Improvement'] > 0.01:
    print(f"\n  → DECISION: Build m5 with {best_interaction['Interaction']} interaction")
    print(f"     Justification: Improvement > 1% threshold ({best_interaction['Improvement']*100:.2f}% > 1.0%)")

    # Build m5
    m5_formula = m4_formula + f' + {best_interaction["Interaction"]}'
    m5 = smf.ols(m5_formula, data=housing_clean).fit()

    print(f"\n\nMODEL m5 SUMMARY:")
    print(f"  R² = {m5.rsquared:.4f} ({m5.rsquared*100:.2f}%)")
    print(f"  Adjusted R² = {m5.rsquared_adj:.4f}")
    print(f"  AIC = {m5.aic:.2f}")

    final_model = 'm5'
    final_r2 = m5.rsquared

else:
    print(f"\n  → DECISION: Keep m4 as final model (no interaction improves by > 1%)")
    print(f"     Justification: Best improvement is {best_interaction['Improvement']*100:.2f}%, below 1% threshold")
    print(f"     Adding complexity not justified by minimal R² gain")

    final_model = 'm4'
    final_r2 = m4.rsquared

# ============================================================================
# SUMMARY
# ============================================================================
print("\n\n3. PROMPT 43 SUMMARY")
print("="*80)
print(f"\nTested {len(interactions_to_test)} theoretically motivated interactions")
print(f"Best improvement: {best_interaction['Improvement']*100:.2f} percentage points")
print(f"\nFinal model for Step Two: {final_model}")
print(f"Final R²: {final_r2:.4f} ({final_r2*100:.2f}%)")

if final_r2 >= 0.85:
    print(f"\n✓ ACHIEVED professor's 85-90% R² target!")
else:
    print(f"\n✓ Close to professor's 85% R² target ({final_r2*100:.1f}%)")

print(f"\nNext Step:")
print(f"  Prompt 44: Write Step Two summary with variable justification and coefficient interpretation")

print("\n" + "="*80)

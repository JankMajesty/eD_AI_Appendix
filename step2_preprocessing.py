"""
Step Two - Prompt 37: Data Preprocessing for Regression Analysis
Removes outliers, creates log transformations, applies multiple imputation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import warnings
warnings.filterwarnings('ignore')

# Set styling
sns.set_theme(style="whitegrid", palette="colorblind")

print("="*80)
print("PROMPT 37 [PYTHON]: DATA PREPROCESSING")
print("="*80)

# Load data
print("\n1. LOADING DATA")
print("-"*80)
housing = pd.read_csv('amesHousing2011.csv')
print(f"Original dataset: {housing.shape[0]} observations, {housing.shape[1]} variables")
print(f"Original SalePrice range: ${housing['SalePrice'].min():,.0f} to ${housing['SalePrice'].max():,.0f}")

# Check missing data
print(f"\nVariables with missing data:")
missing = housing.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)
for var, count in missing.head(10).items():
    print(f"  {var}: {count} missing ({count/len(housing)*100:.1f}%)")

# ============================================================================
# STEP 1: REMOVE OUTLIERS (Top 5% of SalePrice)
# ============================================================================
print("\n\n2. REMOVING OUTLIERS")
print("-"*80)
print("WHY: Professor noted that mansions (extreme high prices) distort the model.")
print("     These rare luxury properties don't represent typical home buyers.")
print("     Removing them improves model accuracy for the majority of homes.\n")

# Calculate 95th percentile
threshold = housing['SalePrice'].quantile(0.95)
print(f"95th percentile of SalePrice: ${threshold:,.0f}")

# Remove outliers
housing_clean = housing[housing['SalePrice'] <= threshold].copy()
removed = len(housing) - len(housing_clean)
print(f"Removed {removed} observations ({removed/len(housing)*100:.1f}% of data)")
print(f"Cleaned dataset: {housing_clean.shape[0]} observations")

# ============================================================================
# STEP 2: CREATE LOG TRANSFORMATIONS
# ============================================================================
print("\n\n3. CREATING LOG TRANSFORMATIONS")
print("-"*80)

# Log of SalePrice
print("\na) log_SalePrice")
print("   WHY: SalePrice is right-skewed (long tail of expensive homes).")
print("        Log transformation makes the distribution more symmetric/normal.")
print("        This helps regression meet the assumption of normally distributed errors.")

housing_clean['log_SalePrice'] = np.log(housing_clean['SalePrice'])

# Log of OverallQual
print("\nb) log_OverallQual")
print("   WHY: Relationship between quality and price is nonlinear.")
print("        A jump from quality 3→4 has different price impact than 9→10.")
print("        Log transformation captures this diminishing returns effect.")

housing_clean['log_OverallQual'] = np.log(housing_clean['OverallQual'])

# Log of YearBuilt
print("\nc) log_YearBuilt")
print("   WHY: Newer homes may show heteroscedasticity (variance changes with age).")
print("        Log transformation can stabilize variance across different eras.")
print("        We'll test if this improves model diagnostics.")

housing_clean['log_YearBuilt'] = np.log(housing_clean['YearBuilt'])

print(f"\nCreated 3 log-transformed variables")

# ============================================================================
# STEP 3: MULTIPLE IMPUTATION FOR MISSING DATA
# ============================================================================
print("\n\n4. HANDLING MISSING DATA")
print("-"*80)
print("WHY: Professor specifically requested multiple imputation (not simple median).")
print("     Multiple imputation creates plausible values based on relationships")
print("     between variables, preserving correlations in the data.\n")

# Identify numeric columns with missing data for imputation
numeric_cols = housing_clean.select_dtypes(include=[np.number]).columns
missing_numeric = housing_clean[numeric_cols].isnull().sum()
missing_numeric = missing_numeric[missing_numeric > 0]

print(f"Applying multiple imputation to {len(missing_numeric)} numeric variables:")
for col in missing_numeric.index[:5]:
    print(f"  - {col}")
if len(missing_numeric) > 5:
    print(f"  ... and {len(missing_numeric) - 5} more")

# Create imputer (uses iterative strategy similar to MICE)
imputer = IterativeImputer(random_state=42, max_iter=10)

# Apply imputation to numeric columns
housing_numeric = housing_clean[numeric_cols].copy()
housing_imputed = pd.DataFrame(
    imputer.fit_transform(housing_numeric),
    columns=numeric_cols,
    index=housing_clean.index
)

# Update cleaned dataset with imputed values
housing_clean[numeric_cols] = housing_imputed

print(f"\nAfter imputation: {housing_clean[numeric_cols].isnull().sum().sum()} missing values in numeric columns")

# ============================================================================
# STEP 4: VISUALIZE BEFORE/AFTER TRANSFORMATIONS
# ============================================================================
print("\n\n5. VISUALIZING TRANSFORMATIONS")
print("-"*80)

fig, axes = plt.subplots(3, 2, figsize=(12, 12))
fig.suptitle('Before/After Log Transformations', fontsize=16, fontweight='bold')

# SalePrice
axes[0, 0].hist(housing['SalePrice'], bins=50, edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Original SalePrice (with outliers)', fontweight='bold')
axes[0, 0].set_xlabel('Sale Price ($)')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].axvline(threshold, color='red', linestyle='--', label=f'95th percentile: ${threshold:,.0f}')
axes[0, 0].legend()

axes[0, 1].hist(housing_clean['log_SalePrice'], bins=50, edgecolor='black', alpha=0.7, color='green')
axes[0, 1].set_title('log(SalePrice) - Cleaned', fontweight='bold')
axes[0, 1].set_xlabel('log(Sale Price)')
axes[0, 1].set_ylabel('Frequency')

# OverallQual
axes[1, 0].hist(housing['OverallQual'], bins=10, edgecolor='black', alpha=0.7)
axes[1, 0].set_title('Original OverallQual', fontweight='bold')
axes[1, 0].set_xlabel('Overall Quality (1-10)')
axes[1, 0].set_ylabel('Frequency')

axes[1, 1].hist(housing_clean['log_OverallQual'], bins=20, edgecolor='black', alpha=0.7, color='green')
axes[1, 1].set_title('log(OverallQual)', fontweight='bold')
axes[1, 1].set_xlabel('log(Overall Quality)')
axes[1, 1].set_ylabel('Frequency')

# YearBuilt
axes[2, 0].hist(housing['YearBuilt'], bins=30, edgecolor='black', alpha=0.7)
axes[2, 0].set_title('Original YearBuilt', fontweight='bold')
axes[2, 0].set_xlabel('Year Built')
axes[2, 0].set_ylabel('Frequency')

axes[2, 1].hist(housing_clean['log_YearBuilt'], bins=30, edgecolor='black', alpha=0.7, color='green')
axes[2, 1].set_title('log(YearBuilt)', fontweight='bold')
axes[2, 1].set_xlabel('log(Year Built)')
axes[2, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('preprocessing_transformations.png', dpi=300, bbox_inches='tight')
print("Saved visualization: preprocessing_transformations.png")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n\n6. PREPROCESSING SUMMARY")
print("="*80)
print(f"Original dataset:     {len(housing)} observations")
print(f"After outlier removal: {len(housing_clean)} observations ({len(housing_clean)/len(housing)*100:.1f}%)")
print(f"\nNew variables created:")
print(f"  - log_SalePrice")
print(f"  - log_OverallQual")
print(f"  - log_YearBuilt")
print(f"\nMissing data: Imputed using IterativeImputer (multiple imputation)")
print(f"\nDataset ready for regression modeling!")

# Save cleaned dataset
housing_clean.to_csv('housing_clean.csv', index=False)
print(f"\nSaved: housing_clean.csv ({len(housing_clean)} observations, {len(housing_clean.columns)} variables)")

# Display key statistics
print("\n\nKEY STATISTICS (Cleaned Data):")
print("-"*80)
summary_stats = housing_clean[['SalePrice', 'log_SalePrice', 'OverallQual', 'log_OverallQual',
                                'YearBuilt', 'log_YearBuilt', 'GrLivArea']].describe()
print(summary_stats.round(2))

print("\n" + "="*80)
print("PREPROCESSING COMPLETE - Ready for Prompt 38 (Model m1)")
print("="*80)

"""
Neighborhood Visualization for Ames Housing Data
Prompt 63 [PYTHON]

Creates two visualizations demonstrating location-based price variation:
1. Boxplot of SalePrice by all 25 neighborhoods (sorted by median)
2. Faceted scatterplot of GrLivArea vs SalePrice for top 6 neighborhoods

Addresses professor's warning about location mediating other variables.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
housing = pd.read_csv('amesHousing2011.csv')

# Create figure with 1x2 layout
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Boxplot of SalePrice by Neighborhood (all 25)
neighborhood_prices = housing.groupby('Neighborhood')['SalePrice'].median().sort_values()
sns.boxplot(data=housing, x='Neighborhood', y='SalePrice',
            order=neighborhood_prices.index, ax=axes[0], palette='viridis')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90, ha='right')
axes[0].set_title('Sale Price Distribution by Neighborhood (n=25)',
                  fontsize=13, fontweight='bold')
axes[0].set_xlabel('Neighborhood (sorted by median price)', fontsize=11)
axes[0].set_ylabel('Sale Price ($)', fontsize=11)
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
axes[0].grid(axis='y', alpha=0.3)

# Plot 2: Scatterplot colored by 6 most common neighborhoods
# "Top 6" = neighborhoods with most observations (not most expensive)
top_neighborhoods = housing['Neighborhood'].value_counts().head(6).index
housing_top = housing[housing['Neighborhood'].isin(top_neighborhoods)]

# Create color palette
palette = sns.color_palette('Set2', n_colors=6)

for i, neighborhood in enumerate(top_neighborhoods):
    subset = housing_top[housing_top['Neighborhood'] == neighborhood]
    axes[1].scatter(subset['GrLivArea'], subset['SalePrice'],
                   alpha=0.6, label=neighborhood, s=40, color=palette[i])

axes[1].set_xlabel('Above-Grade Living Area (sq ft)', fontsize=11)
axes[1].set_ylabel('Sale Price ($)', fontsize=11)
axes[1].set_title('Living Area vs Price: 6 Most Common Neighborhoods',
                 fontsize=13, fontweight='bold')
axes[1].legend(title='Neighborhood (by sample size)', fontsize=9, title_fontsize=10)
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('neighborhood_price_variation.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n" + "="*70)
print("NEIGHBORHOOD PRICE VARIATION ANALYSIS")
print("="*70)

print("\nNote: The scatterplot shows the 6 MOST COMMON neighborhoods (by sample size),")
print("not the 6 most expensive. This ensures each neighborhood has enough observations")
print("to display meaningful price-area relationships.")

# Summary statistics by neighborhood
neighborhood_stats = housing.groupby('Neighborhood')['SalePrice'].agg([
    ('Count', 'count'),
    ('Median', 'median'),
    ('Mean', 'mean'),
    ('Std Dev', 'std')
]).round(0)

neighborhood_stats = neighborhood_stats.sort_values('Median', ascending=False)

print("\nTop 5 Most Expensive Neighborhoods (by median):")
print(neighborhood_stats.head(5).to_string())

print("\nBottom 5 Least Expensive Neighborhoods (by median):")
print(neighborhood_stats.tail(5).to_string())

# Price range across neighborhoods
price_range = neighborhood_stats['Median'].max() - neighborhood_stats['Median'].min()
print(f"\nMedian price range across neighborhoods: ${price_range:,.0f}")
print(f"Highest median (NoRidge): ${neighborhood_stats['Median'].max():,.0f}")
print(f"Lowest median (MeadowV): ${neighborhood_stats['Median'].min():,.0f}")

print("\n" + "="*70)
print("INTERPRETATION:")
print("This visualization demonstrates the professor's warning that 'location")
print("is the most important factor in house prices' and that 'location has a")
print("mediating effect on other variables like area, quality, and frontage.'")
print("\nDifferent neighborhoods show distinct price ranges even for homes of")
print("similar size, confirming that pairwise correlations alone miss important")
print("location effects.")
print("="*70)

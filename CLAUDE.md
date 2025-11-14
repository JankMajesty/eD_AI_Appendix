# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an academic assignment repository for a Prompt Engineering class, focused on using LLMs to analyze the Ames Housing dataset and build regression models predicting home sale prices. The assignment demonstrates iterative prompt engineering with comprehensive documentation of all LLM interactions.

**Assignment:** Complete a 4-step housing price regression analysis (eD.qmd) with full documentation of prompts and responses.

**Key Constraint:** All work must be documented in logs (prompts_log.md, conversation_log.md) to demonstrate the prompt engineering process for academic evaluation.

## Core Architecture

### Dual-Language Implementation

This project has **parallel implementations in both R and Python** to compare statistical computing approaches:

**Python Track (PRIMARY):**
- `eD_submission_python.qmd` - Python-based analysis (user's primary submission)
- Uses: pandas, numpy, statsmodels, scikit-learn, seaborn, plotly
- Skills: `~/.claude/skills/housing-analysis-python/`, `~/.claude/skills/real-estate-viz-python/`
- All Python work marked with `[PYTHON]` tags in logs
- **User preference:** Python chosen due to greater familiarity (archival background, not data science)

**R Track (REFERENCE):**
- `eD_submission.qmd` - R-based analysis (reference implementation)
- Uses: base R, ggplot2, viridis, stats
- Skills: `~/.claude/skills/housing-analysis-r/`, `~/.claude/skills/real-estate-viz-r/`
- Note: Assignment officially requires R, but Python approach being pursued

### Documentation System

**Three-tiered logging:**
1. **prompts_log.md** - Chronological list of all prompts given to LLMs (required for assignment)
2. **conversation_log.md** - Detailed prompts + responses with code and explanations
3. **Cursor/Gemini logs** - Alternative LLM experiments (gemini_prompts_log.md, cursor_conversation_log.md)

**Critical Rule:** Every prompt must be logged with a sequential number. Python prompts must include `[PYTHON]` marker for filtering in appendix.

### Assignment Structure (eD.qmd)

**Step One:** Data description (statistics, graphics, variable relationships)
**Step Two:** Regression analysis (use R's `lm()` function)
**Step Three:** Diagnostic plots (4 plots using `plot(model)`)
**Step Four:** Final model selection with variable justification
**Conclusion:** Reflection on LLM utility

## Professor's Feedback from Last Semester

**Critical Requirements (lastSemest_eD_Notes.txt):**

1. **Outlier Removal:** Remove top 5% of sale prices (mansions distort model)
2. **Transformations:**
   - Log transform SalePrice (right-skewed)
   - Log transform OverallQual (nonlinear relationship)
   - Experiment with log of YearBuilt (heteroscedasticity)
3. **Target R²:** 80-90% (5 variables → 80%, 12 variables → 90%)
4. **Documentation:** More prompts needed, use "Prompt"/"Result" headings, delineate with italics
5. **Model Comparison:** Show R² values for multiple models, use Lasso or best subset selection
6. **Diagnostics:** Q-Q plot > histogram of residuals for normality
7. **Variable Justification:** Explain why each variable was included (avoid just copying LLM)
8. **Missing Data:** Use multiple imputation instead of median imputation
9. **Location Variables:** Account for mediating effects (not captured by pairwise correlations)

## Common Commands

### Rendering Documents
```bash
# Render R version (primary submission)
quarto render eD_submission.qmd

# Render Python version (comparison)
quarto render eD_submission_python.qmd

# Render assignment prompt
quarto render eD.qmd
```

### Python Environment
```bash
# Run Python code with project dependencies
uv run python script.py

# Add new Python package
uv add package-name

# Sync dependencies
uv sync

# Start Python REPL
uv run python
```

**Note:** Python environment managed by uv with local pyproject.toml in eD directory. All required packages (pandas, numpy, statsmodels, scikit-learn, seaborn, plotly, scipy, matplotlib) already installed.

### R Environment
R packages used: base R, stats, ggplot2, viridis, scales, patchwork. Install if missing:
```r
install.packages(c("ggplot2", "viridis", "scales", "patchwork"))
```

**Key Quarto features in use:**
- Front matter with fonts (Georgia, Helvetica Neue, JetBrains Mono)
- `embed-resources: true` - includes all assets in single HTML
- `toc: true` - generates table of contents
- Code blocks: `{r}` for R, `{python}` for Python
- LaTeX math expressions between `$` symbols

## Dataset

**File:** amesHousing2011.csv (2,930 properties, 82 variables)
**Documentation:** amesHousing2011doc.txt

**Key Variables:**
- **Response:** SalePrice (continuous, dollars)
- **Important predictors:**
  - GrLivArea (continuous, sq ft above grade living area)
  - OverallQual (ordinal, 1-10 scale of material/finish quality)
  - YearBuilt (discrete, year constructed)
  - TotalBsmtSF (continuous, sq ft basement)
  - Neighborhood (categorical, 25 neighborhoods in Ames)
  - GarageCars (discrete, car capacity)
  - YearRemod/Add (discrete, remodel date or construction if no remodel)

**Column Name Gotchas:**
- `YearRemod/Add` contains slash (not dot)
- `1stFlrSF` and `2ndFlrSF` start with digits (no X prefix in actual data)
- When using Python: access with bracket notation like `housing['1stFlrSF']`

**External Python Examples:**

1. **[Scikit-learn MOOC: Ames Housing](https://inria.github.io/scikit-learn-mooc/python_scripts/datasets_ames_housing.html)**
   - Data exploration, handling mixed types
   - Missing value imputation with SimpleImputer
   - Preprocessing pipelines with make_column_transformer

2. **[LearnPython: Data Analysis Example](https://learnpython.com/blog/python-data-analysis-example/)**
   - Four-step workflow: import → clean → explore → interpret
   - pandas/numpy/seaborn basics
   - Identifying key features affecting price

**Note:** Both resources focus on statistical analysis and visualization approaches compatible with the assignment's linear regression requirements.

## Claude Skills Integration

Four custom skills created for this project (packaged as .zip files):

**R Skills:**
- `housing-analysis-r` - Statistical workflow, model building, diagnostics
- `real-estate-viz-r` - ggplot2 visualizations addressing UX/Data Science critiques

**Python Skills:**
- `housing-analysis-python` - pandas/statsmodels workflow with comprehensive MLR theory
  - Includes all 4 diagnostic plots with interpretation
  - Progressive model building (m1-m5)
  - Variable selection rationale framework
  - Transformation decision framework
  - Lasso regression for variable selection
  - references/mlr_concepts.md has deep statistical theory
- `real-estate-viz-python` - seaborn (static) + plotly (interactive) visualizations

**Location:** `~/.claude/skills/` (installation source: .zip files in project root)

**Skill Enhancement History:**
- Prompt 16 [PYTHON]: Enhanced housing-analysis-python from 178 to 398 lines in SKILL.md
- Added mlr_concepts.md (470 lines) with R², p-values, diagnostic plots theory
- Python skill now has parity with R skill comprehensiveness

## Assignment Progress Tracking

**Current Status (Python track):**
- ✅ Step One: Complete (data exploration)
- ⏳ Step Two: Regression modeling (ready to begin with housing-analysis-python skill)
- ⏳ Step Three: Diagnostic plots (code ready in skills, interpretation required)
- ⏳ Step Four: Final model selection (dependent on Steps 2-3)

**User Context:** Archival studies student with limited data science background. Emphasis on understanding concepts and documenting the LLM-assisted learning process.

## Working with This Repository

**When adding new analysis:**
1. Update appropriate logs FIRST (prompts_log.md, conversation_log.md)
2. Add sequential prompt number (format: "Prompt N [PYTHON]:" - all work is Python)
3. All prompts should include `[PYTHON]` marker for appendix filtering
4. Include code in eD_submission_python.qmd with proper `{python}` code fences
5. Test render before committing: `quarto render eD_submission_python.qmd`
6. **Include written interpretation** after each code block - don't just show output!

**When improving visualizations:**
- Invoke real-estate-viz-python skill (seaborn for publication + plotly for interactive)
- Prioritize colorblind-friendly palettes and accessibility
- Use seaborn's default theme: `sns.set_theme(style="whitegrid", palette="colorblind")`

**When building models (Python with statsmodels):**
- Follow professor's feedback (outlier removal, log transforms, R² targets)
- Build progressive models (m1, m2, m3, m4, m5) showing R² improvement:
  ```python
  m1 = smf.ols('log_SalePrice ~ GrLivArea', data=housing_clean).fit()
  m2 = smf.ols('log_SalePrice ~ GrLivArea + log_OverallQual', data=housing_clean).fit()
  # etc.
  ```
- Document variable selection reasoning (statistical + theoretical justification)
- Show model comparison table with R², Adjusted R², AIC
- Generate all 4 diagnostic plots for final model (Residuals vs Fitted, Q-Q, Scale-Location, Leverage)
- **CRITICAL:** Write interpretation after each plot explaining what it shows
- **User context:** Explain statistical concepts in plain language (user is archival studies, not data science)

**Diagnostic Plot Interpretation (Critical):**
- **Residuals vs Fitted:** Check linearity (want random scatter, not curves or funnels)
- **Normal Q-Q:** Check normality (want points on diagonal) - PROFESSOR'S PRIORITY
- **Scale-Location:** Check homoscedasticity (want horizontal line, not increasing variance)
- **Residuals vs Leverage:** Check influential points (high Cook's Distance in corners = problem)

**Git status note:** This is untracked in parent git repo (appears as `eD/` in parent .gitignore). All files in this directory are untracked.

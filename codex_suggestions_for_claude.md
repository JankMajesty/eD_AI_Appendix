# Codex Suggestions for Claude

These notes summarize the improvements Codex recommended for Steps 1–3 so Claude can continue the assignment with full context.

## Step One (Description of Data)
- Add at least one location-focused visualization (e.g., neighborhood boxplots or faceted scatterplots) to demonstrate you investigated the mediating role of Neighborhood, as highlighted in `lastSemest_eD_Notes.txt`.
- Document how categorical fields with missing values are handled when running multiple imputation—note whether you use mode imputation, "Missing" categories, or encode them prior to modeling.
- After iterative imputation, include quick before/after summaries (histograms or descriptive stats) for heavily missing variables to show that the distributions remain plausible.
- Tie each preprocessing decision (outlier removal, log transforms, imputation) back to a concrete observation from EDA so reviewers see how the analysis led to the modeling choices.

## Step Two (Regression Modeling)
- Expand the justification section so all ten predictors in model m4 have explicit statistical evidence (Lasso coefficient, correlation, p-value) plus buyer-oriented reasoning; the current block only prints five examples.
- Run multicollinearity diagnostics (VIF or condition numbers) for m4 and explain any high values—best practice and aligns with the Kaggle OLS example referenced in `CLAUDE.md`.
- Test whether reintroducing Neighborhood (dummy variables or target encoding) changes fit relative to m4, then explain why the final model retains or omits location—this addresses the professor’s “location mediates other variables” concern.
- Report cross-validation or train/test performance alongside the in-sample R² so the Lasso selection and final model demonstrate generalization.
- Briefly describe how categorical variables are encoded or excluded before Lasso so that the preprocessing story is complete.

## Step Three (Diagnostics)
- Add Durbin–Watson (or another independence check) to the diagnostic summary and interpret it in plain language for the instructor.
- Provide a compact table listing the key diagnostic tests (Shapiro, Jarque–Bera, Breusch–Pagan, Cook’s D) with p-values and conclusions; this mirrors the structured reporting style praised in last semester’s feedback.
- For each plot, explicitly link the visual result back to the preprocessing decision that addressed the issue (e.g., “Log(SalePrice) removed curvature in Residuals vs Fitted”).

## Documentation & Logging
- Keep referencing the professor’s requirements directly in the narrative (e.g., “per lastSemest_eD_Notes.txt, we removed the top 5% of SalePrice”).
- Whenever a recommendation is implemented, note the prompt number and dataset version so the grading logs remain synchronized.

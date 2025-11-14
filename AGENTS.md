# Repository Guidelines

## Project Structure & Module Organization
Work from the repo root. Deliverables are `eD_submission.qmd` (R) and `eD_submission_python.qmd` (Python); helper scripts (`main.py`, `step2_model_m*.py`, `step2_prompt*.py`) drive experiments. Datasets (`amesHousing2011.csv`, `housing_clean.csv`) and notes (`amesHousing2011doc.txt`) sit alongside them. Keep every prompt log and Claude skill archive tracked—documentation completeness is graded.

## Build, Test, and Development Commands
- `uv sync` — install/update the Python environment from `pyproject.toml`.
- `uv run python step2_model_m1.py` (swap any `step2_*` script) — run modeling or preprocessing batches.
- `quarto render eD_submission_python.qmd` — rebuild the Python narrative.
- `quarto render eD_submission.qmd` — keep the R reference in sync.
Run commands from the repo root so Quarto chunks resolve data paths.

## Coding Style & Naming Conventions
Python uses 4-space indentation, snake_case naming, and statsmodels formulas as strings (e.g., `"log_SalePrice ~ GrLivArea + OverallQual"`). Favor helper functions and concise cells so explanations can pair with each block. R chunks within Quarto follow tidyverse style with `<-` assignment. Name new experiments `step2_model_mX.py` or `step2_promptYY_topic.py` for traceability.

## Testing & Quality Checks
No automated suite exists. Render both Quarto submissions, ensure each figure is interpreted, and confirm professor feedback (e.g., QQ plots over residual histograms) is addressed. Spot-test scripts with `uv run python step2_prompt43_interactions.py` or similar before embedding, and note what you reviewed inside conversation_log.md for traceability.

## Faculty Expectations & Modeling Requirements
Apply last-semester notes: drop mansion outliers (≈95th percentile SalePrice), log-sale price and OverallQual (test YearBuilt), and use multiple imputation. Explain why each predictor remains, ask LLMs to interpret diagnostics, and emphasize QQ plots. Show progressive R² improvements (~80% with five vars, ~90% with ~12) and include a Lasso or best-subset run while noting neighborhood mediation effects.

## Commit & Pull Request Guidelines
Write imperative commits (e.g., “Add step two Lasso script”) and reference the driving prompt number. Analysis edits must update `prompts_log.md`, `conversation_log.md`, and Codex logs using the Prompt/Result pattern. Pull requests should note the assignment step, list rendered artifacts (`eD_submission_python.html`, `eD_submission.html`), and attach screenshots when visuals change.

## Prompt Logging & Agent Workflow
Record each user prompt sequentially in `prompts_log.md` (add `[PYTHON]` tags when applicable) and mirror the full exchange in `conversation_log.md`. Codex interactions also belong in `codex_prompts_log.md` and `codex_conersation_log.md`. Keep “Prompt”/“Result” blocks or italics so instructors can audit quickly.

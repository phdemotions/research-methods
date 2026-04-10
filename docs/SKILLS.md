# Skill Taxonomy & Design

> Complete specification for every skill in the research-methods suite.
> Each skill is described at the design level — what it does, when it triggers, what it produces.

---

## Layer 1 — Project Lifecycle Skills

### `/research-init` — Project Scaffolding

**Purpose:** Scaffold a new research project with full reproducibility infrastructure, or wrap existing data in gold-standard structure.

**Triggers:** "new research project," "start a study," "scaffold," "init," "I have data and need to set up a project"

**What it does:**
1. Asks: R, Python, or both? (both from day one)
2. Asks: Do you have existing data? If yes, identifies data format and location.
3. Creates the full directory structure (see ARCHITECTURE.md)
4. Initializes `renv` (R) and/or `uv` (Python) with the research stack
5. Creates `_targets.R` pipeline stub (R) and/or `Snakefile` stub (Python)
6. Generates README from Cornell template
7. Creates codebook template in `data/codebook/`
8. Creates decision log template in `docs/decisions/`
9. Creates pre-registration skeleton in `docs/pre-registration.md`
10. Creates Quarto manuscript template in `reports/`
11. Initializes git with proper `.gitignore`
12. If existing data provided: copies to `data/raw/` and triggers `/data-validate`

**Produces:** A complete, ready-to-use research project directory.

---

### `/data-validate` — Data Quality Assessment

**Purpose:** Run declarative checks on data and produce a validation report with codebook.

**Triggers:** "validate data," "check data quality," "generate codebook," "what's wrong with my data," "data audit"

**What it does:**
1. Reads data from `data/raw/` (or specified path)
2. Identifies variable types, distributions, ranges
3. Checks for: completeness, impossible values, duplicates, outliers, encoding issues
4. Generates validation report using `pointblank` (R) or `pandera` (Python)
5. Auto-generates codebook using `codebook`/`codebookr` (R) or custom Quarto doc (Python)
6. Reports missingness patterns with `naniar` (R) or `missingno` (Python)
7. Flags attention check failures, manipulation check issues (if applicable)
8. Produces summary: N observations, N variables, completeness rate, flagged issues

**Produces:** 
- `data/codebook/codebook.html` — auto-generated codebook
- `output/results/validation-report.html` — pointblank/pandera report
- Console summary of critical findings

**R packages used:** pointblank, codebook, codebookr, naniar, skimr
**Python packages used:** pandera, missingno, polars

---

### `/data-clean` — Documented Data Cleaning

**Purpose:** Produce cleaning scripts that log every transformation with a CONSORT-style exclusion flow.

**Triggers:** "clean data," "prepare data," "exclusion criteria," "data cleaning," "preprocessing"

**What it does:**
1. Reads codebook and validation report to understand data state
2. Asks about exclusion criteria (or reads from pre-registration)
3. Generates cleaning functions that:
   - Log N before and after each step
   - Document each transformation with rationale
   - Never modify raw data — writes to `data/processed/`
   - Handle missing data per specified strategy (listwise, pairwise, imputation)
4. Produces CONSORT-style flow diagram showing sample attrition
5. Creates decision log entry for each subjective cleaning choice
6. Computes and reports scale reliability (alpha, omega) for multi-item measures
7. Creates composite scores with documentation

**Produces:**
- `R/02_clean.R` or `python/02_clean.py` — documented cleaning script
- `data/processed/` — cleaned dataset(s)
- `output/figures/consort-flow.png` — exclusion flow diagram
- `docs/decisions/cleaning-decisions.md` — decision log entries
- Updated codebook with derived variable documentation

**R packages used:** tidyverse, psych (alpha/omega), lavaan (CFA for scales), naniar
**Python packages used:** polars/pandas, factor_analyzer

---

### `/eda` — Exploratory Data Analysis

**Purpose:** Comprehensive exploratory analysis with publication-quality figures and descriptive tables.

**Triggers:** "exploratory analysis," "EDA," "descriptive statistics," "explore the data," "Table 1"

**What it does:**
1. Reads cleaned data and codebook
2. Generates "Table 1" — sample descriptive statistics (gtsummary)
3. Produces distribution plots for all key variables
4. Computes correlation matrix with visualization
5. Tests distributional assumptions (normality, homoscedasticity)
6. Identifies potential multicollinearity (VIF)
7. Visualizes relationships between key constructs
8. Generates standalone EDA report (Quarto)
9. All figures are publication-quality, APA-formatted, colorblind-safe

**Produces:**
- `output/tables/table1-descriptives.html/.docx` — Table 1
- `output/figures/correlations.png` — correlation matrix
- `output/figures/distributions/` — variable distributions
- `reports/eda-report.html` — standalone EDA report
- `output/results/eda-summary.rds/.parquet` — summary statistics

**R packages used:** gtsummary, gt, ggplot2, patchwork, corrplot/ggcorrplot, performance (VIF), skimr
**Python packages used:** great_tables, plotnine, seaborn, pingouin

---

### `/analyze` — Confirmatory Analysis

**Purpose:** Hypothesis testing matched to pre-registration, with full assumption testing and effect size reporting.

**Triggers:** "test hypotheses," "run analysis," "confirmatory," "regression," "SEM," "mediation," "moderation," "PROCESS"

**What it does:**
1. Reads pre-registration to identify planned analyses
2. For each hypothesis:
   a. Tests assumptions (normality, homoscedasticity, linearity, multicollinearity)
   b. Fits the specified model
   c. Reports: coefficients, SEs, CIs, p-values, effect sizes
   d. Produces diagnostic plots
   e. Flags any deviation from pre-registered plan
3. Supports: OLS, logistic, ordinal, Poisson, fixed effects (fixest), mixed models (lme4), SEM (lavaan), PROCESS models (bruceR/lavaan), meta-analysis (metafor)
4. All output is APA 7th formatted
5. Generates decision log entry for any post-hoc choices

**Produces:**
- `output/tables/hypothesis-tests.html/.docx` — results tables
- `output/figures/diagnostics/` — model diagnostic plots
- `output/results/models.rds/.pkl` — fitted model objects
- `docs/decisions/analysis-decisions.md` — any deviations from pre-registration

**R packages used:** easystats (parameters, performance, effectsize, report), fixest, lme4, lavaan, bruceR, metafor, modelsummary
**Python packages used:** statsmodels, pingouin, semopy, scikit-learn

---

### `/robustness` — Sensitivity Analysis

**Purpose:** Test whether results hold under alternative specifications, subsamples, and estimators.

**Triggers:** "robustness check," "sensitivity analysis," "alternative specifications," "specification curve," "multiverse"

**What it does:**
1. Reads primary analysis results
2. Runs alternative specifications:
   - Different control variable sets
   - Alternative operationalizations of key constructs
   - Different estimation methods (OLS vs. robust, ML vs. bootstrap)
   - Winsorized/trimmed samples
   - Subsample analyses (by demographics, conditions)
   - Different exclusion criteria
3. Produces specification curve / multiverse visualization
4. Summarizes: how many specifications support the finding?
5. Influence diagnostics (Cook's distance, leverage, DFBETAS)

**Produces:**
- `output/figures/specification-curve.png` — specification curve plot
- `output/tables/robustness-summary.html` — summary of all specifications
- `output/results/robustness/` — all alternative model fits

**R packages used:** easystats (performance, parameters), fixest, ggplot2
**Python packages used:** statsmodels, plotnine

---

### `/visualize` — Publication-Quality Figures

**Purpose:** Create figures that meet journal submission standards.

**Triggers:** "publication figures," "journal figures," "APA figures," "visualize results," "make plots"

**What it does:**
1. Reads analysis results and data
2. Applies APA 7th formatting defaults:
   - Clean white background (no grid lines unless data-dense)
   - Appropriate font size (typically 10-12pt)
   - Colorblind-safe palette (viridis or custom)
   - High DPI (300+ for print, 150 for screen)
   - Journal-specific dimensions (if journal parameter set)
3. Generates standard figure types:
   - Interaction plots with error bars
   - Mediation/moderation path diagrams
   - Forest plots (meta-analysis)
   - Marginal effects plots
   - Johnson-Neyman plots (regions of significance)
4. Exports in multiple formats: PDF, PNG, SVG, TIFF

**Produces:**
- `output/figures/` — publication-ready figures
- Multiple formats per figure

**R packages used:** ggplot2, patchwork, scales, ggrepel, see (easystats), interactions
**Python packages used:** plotnine, matplotlib, seaborn

---

### `/report` — Manuscript-Ready Output

**Purpose:** Generate APA-formatted results paragraphs and tables for direct insertion into manuscripts.

**Triggers:** "results section," "write results," "APA results," "manuscript tables," "format for submission"

**What it does:**
1. Reads all analysis results
2. Generates APA-formatted statistics text:
   - Example: "A moderated mediation analysis (PROCESS Model 14; Hayes, 2022) revealed a significant indirect effect of brand authenticity on purchase intention through perceived value (b = 0.34, SE = 0.08, 95% CI [0.19, 0.51]). The index of moderated mediation was significant (index = 0.12, SE = 0.05, 95% CI [0.03, 0.23]), indicating that the indirect effect was stronger for high-expertise consumers."
3. Generates formatted tables:
   - Regression/model results tables
   - Descriptive statistics tables
   - Correlation matrices
   - Scale reliability tables
4. Outputs in: HTML, Word (.docx), LaTeX
5. Integrates with Quarto manuscript template

**Produces:**
- `output/tables/` — formatted tables in multiple formats
- `reports/results-text.md` — APA-formatted results paragraphs
- Console output of key findings

**R packages used:** report (easystats), gtsummary, modelsummary, gt
**Python packages used:** great_tables

---

### `/reproduce` — OSF/Repository Packaging

**Purpose:** Package everything for public sharing on OSF, Dataverse, or GitHub.

**Triggers:** "package for OSF," "prepare for sharing," "reproducibility package," "research compendium," "archive"

**What it does:**
1. Verifies pipeline reproduces (runs `tar_make()` or `snakemake` from clean state)
2. Generates/updates README using Cornell template
3. Generates CITATION.cff
4. Verifies codebook is complete and current
5. Checks that decision log documents all subjective choices
6. Ensures no secrets/credentials in any file
7. Verifies .gitignore is correct
8. Generates session info / environment specification
9. Optionally creates Docker/Apptainer container definition
10. Produces checklist: TOP Guidelines compliance, FAIR principles check
11. Creates archive-ready directory structure

**Produces:**
- Updated README.md
- CITATION.cff
- `output/session-info.txt` — R/Python session info
- `Dockerfile` or `Apptainer.def` (optional)
- Compliance checklist report

**R packages used:** sessioninfo, renv, rrtools
**Python packages used:** watermark, uv

---

## Layer 2 — Quality Gate Skills

### `/research-review` — Methods Code Review

**Purpose:** Full code review from a senior methodologist's perspective.

**Triggers:** "review my analysis," "methods review," "is my analysis correct," "code review"

**What it does:**
1. Reads all analysis code and output
2. Evaluates against criteria:
   - Statistical appropriateness (right test for the design?)
   - Assumption testing (were assumptions checked before modeling?)
   - Reporting completeness (effect sizes? CIs? exact p-values?)
   - Reproducibility (can this be re-run from scratch?)
   - Transparency (are subjective decisions documented?)
   - Common mistakes (listwise deletion without justification, p-hacking indicators, HARKing)
3. Produces a structured review with severity levels
4. Actionable recommendations with code examples

---

### `/pre-submit` — Pre-Submission Checklist

**Purpose:** Final check before submitting to a journal.

**Triggers:** "pre-submission check," "ready to submit," "submission checklist," "JARS check"

**Checklist includes:**
- JARS (APA Journal Article Reporting Standards) compliance
- Effect sizes reported for all tests
- Confidence intervals reported
- Data/code availability statement drafted
- IRB/ethics approval noted
- Pre-registration linked
- CRediT author contributions listed
- Conflicts of interest declared
- Supplementary materials organized
- Figures meet journal specifications (DPI, dimensions, color)
- Tables are self-contained with notes
- References complete and formatted

---

### `/reproduce-check` — Reproduction Verification

**Purpose:** Actually reproduce the results from a clean state.

**Triggers:** "can this reproduce," "verify reproduction," "test reproducibility"

**What it does:**
1. Creates a fresh environment (renv restore / uv sync)
2. Runs the full pipeline from scratch
3. Compares output to existing results
4. Reports: exact match, near match (floating point), or divergence
5. Fails loudly if anything doesn't match

---

## Layer 3 — Learning/Evolution Skills

### `/research-zeitgeist` — Best Practices Scanner

**Purpose:** Date-aware scan of current best practices. The self-improvement engine.

**Triggers:** "what's current," "best practices now," "is our stack current," "research zeitgeist," monthly routine

**What it does:**
1. Reads today's date from environment
2. Web-searches for updates to every package in FRAMEWORKS.md
3. Checks for new methodology guidelines
4. Checks journal policy changes (data sharing, pre-registration requirements)
5. Searches for community shifts (new packages, deprecated patterns)
6. Produces a dated report
7. Proposes updates to FRAMEWORKS.md (requires approval)

**Time-awareness contract:** Same as `/zeitgeist` — every finding is stamped with the date it was discovered. "As of April 2026" is explicit in every recommendation.

---

### `/method-advisor` — Statistical Method Recommendation

**Purpose:** Given a research question and data structure, recommend appropriate methods.

**Triggers:** "what test should I use," "which analysis," "recommend a method," "how should I analyze this"

**What it does:**
1. Asks about: research question, hypotheses, study design, variable types, sample size, nesting structure
2. Recommends appropriate statistical method(s) with citations
3. Explains assumptions and how to test them
4. Describes what to report (per APA/JARS)
5. Provides code skeleton in R and/or Python
6. Notes common pitfalls specific to the method

---

### `/process-model` — PROCESS Mediation/Moderation

**Purpose:** Implement Hayes PROCESS models transparently via lavaan.

**Triggers:** "PROCESS model," "mediation analysis," "moderated mediation," "conditional indirect effect," "Hayes model"

**What it does:**
1. Accepts: PROCESS model number (1-24), or describes the model structure
2. Maps to correct `lavaan` syntax (transparent, inspectable)
3. Also runs via `bruceR::PROCESS()` for verification
4. Bootstrap confidence intervals for indirect effects
5. Index of moderated mediation (where applicable)
6. Johnson-Neyman regions of significance (for moderation)
7. APA-formatted output matching familiar PROCESS tables
8. Path diagram visualization

**The key value:** Researchers who think in "Model 14" get transparent, reproducible `lavaan` code instead of a black-box SPSS macro.

---

## Shared Resources (`_shared/`)

### `project-discovery.md`
How to find and read the research project: locate data, codebook, pre-registration, decision log, pipeline definition.

### `r-standards.md`
R coding standards for research: tidyverse style, function documentation, seed management, package loading via `targets`/`renv`.

### `python-standards.md`
Python coding standards for research: type hints, docstrings, polars-first, uv for environment, Snakemake for pipeline.

### `apa-formatting.md`
APA 7th edition formatting rules for statistics, tables, and figures. Journal-specific overrides.

### `transparency.md`
Documentation and transparency standards: decision log format, codebook requirements, pre-registration alignment, FAIR principles.

### `severity-scale.md`
For audit/review skills: severity definitions (Blocker, Major, Minor, Polish) calibrated to research context.

### `output-contract.md`
Report template for audit skills: verdict, findings, recommendations.

---

## Implementation Priority

### Phase 1 — Foundation (build first)
1. `_shared/` resources
2. `/research-init`
3. `/data-validate`
4. `/data-clean`

### Phase 2 — Analysis Core
5. `/eda`
6. `/analyze`
7. `/process-model`
8. `/visualize`

### Phase 3 — Polish & Package
9. `/report`
10. `/robustness`
11. `/reproduce`

### Phase 4 — Quality & Evolution
12. `/research-review`
13. `/pre-submit`
14. `/research-zeitgeist`
15. `/method-advisor`
16. `/reproduce-check`

### Future Phase — Bayesian
- Extend `/analyze` with Bayesian options
- Add `/bayes` skill for Bayesian-specific workflow

---

*Last updated: April 10, 2026*

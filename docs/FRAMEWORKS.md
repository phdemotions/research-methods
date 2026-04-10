# Framework Choices — Verified April 2026

> Every framework listed here was web-searched and verified current as of April 2026.
> Run `/research-zeitgeist` monthly to check for updates.

---

## Design Principles for Framework Selection

1. **Community standard over bleeding edge.** A reviewer must be able to read the code.
2. **Active maintenance.** No packages abandoned or in maintenance-only mode.
3. **Interoperability.** Everything must work with Quarto, Positron, and each other.
4. **Transparency by default.** Packages that report effect sizes, CIs, and diagnostics automatically are preferred over those that require manual extraction.

---

## R Stack

### Pipeline & Environment

| Layer | Package | Version (April 2026) | Why this one |
|-------|---------|---------------------|-------------|
| **Pipeline** | [`targets`](https://books.ropensci.org/targets/) | CRAN Feb 2026 | DAG-based workflow. Caches intermediate results, tracks dependencies, skips unchanged steps. The standard in reproducible R research. Function-oriented programming nudges clean code. rOpenSci reviewed. |
| **Environment** | [`renv`](https://rstudio.github.io/renv/) | CRAN Jan 2026 (v2026.01.2) | Lockfile-based dependency isolation. The only serious option for R reproducibility. Integrated with Positron. |
| **Literate programming** | [Quarto](https://quarto.org/) | Current 2026 | Multi-language successor to R Markdown. Native Positron integration. Supports R, Python, Julia, Observable in same document. Produces HTML, PDF, Word, slides. |

### Data Wrangling & Validation

| Layer | Package | Why this one |
|-------|---------|-------------|
| **Data wrangling** | `tidyverse` (dplyr, tidyr, readr, stringr, forcats, purrr) | Community standard. Every reviewer can read it. Consistent grammar. |
| **Data validation** | [`pointblank`](https://rstudio.github.io/pointblank/) | Declarative validation with rich HTML reports. Research-friendly. Supports local data frames and databases. Posit-maintained. |
| **Codebook generation** | [`codebook`](https://rubenarslan.github.io/codebook/) + [`codebookr`](https://brad-cannell.github.io/codebookr/) | `codebook` auto-generates HTML/PDF codebooks with distributions, missingness, scale reliability. `codebookr` produces Word codebooks. Both updated 2026. |
| **Missing data diagnosis** | [`naniar`](https://naniar.njtierney.com/) | Visualization and diagnosis of missingness patterns. Tidy-compatible. |
| **Missing data imputation** | [`mice`](https://amices.org/mice/) | Gold standard for multiple imputation. Flexible, well-documented, heavily cited. |

### Visualization & Tables

| Layer | Package | Why this one |
|-------|---------|-------------|
| **Visualization** | `ggplot2` + `patchwork` + `scales` + `ggrepel` | Gold standard for publication figures. Journal-ready. `patchwork` for multi-panel layouts. `ggrepel` for non-overlapping labels. |
| **Descriptive tables** | [`gtsummary`](https://www.danieldsjoberg.com/gtsummary/) | One-line publication-ready summary tables. APA-formatted. Built on `gt`. Cited in R Journal (Sjoberg et al., 2021). |
| **Regression tables** | [`modelsummary`](https://modelsummary.com/) | Side-by-side model comparison tables. Supports dozens of model types. HTML, LaTeX, Word, PDF output. Updated Feb 2026. |
| **Presentation tables** | [`gt`](https://gt.rstudio.com/) | The foundation. When `gtsummary`/`modelsummary` aren't enough, drop to `gt` for full control. |

### Statistics

| Layer | Package | Why this one |
|-------|---------|-------------|
| **Unified statistics** | [`easystats`](https://easystats.github.io/easystats/) ecosystem | `parameters` (model parameters), `performance` (model quality), `effectsize` (effect sizes + CIs), `report` (APA text), `see` (visualization), `correlation`, `datawizard`. Consistent API. Always reports effect sizes alongside p-values. Actively maintained 2026. |
| **Panel/Fixed effects** | [`fixest`](https://lrberge.github.io/fixest/) | Blazing fast for panel data. Multiple fixed effects. Cluster-robust SEs. The standard for empirical economics and increasingly business research. |
| **Mixed models** | `lme4` + `lmerTest` | `lme4` for fitting, `lmerTest` for p-values via Satterthwaite. The standard for multilevel/HLM. |
| **SEM** | [`lavaan`](https://lavaan.ugent.be/) | v0.6-21. The definitive R package for structural equation modeling. CFA, path analysis, mediation, moderation, latent growth. No real competitor. |
| **Mediation/Moderation (PROCESS-style)** | [`bruceR::PROCESS()`](https://psychbruce.github.io/bruceR/reference/PROCESS.html) + `lavaan` | `bruceR::PROCESS()` supports 24 Hayes PROCESS model types with automatic mean-centering and model detection. For full transparency and custom models, `lavaan` directly. Updated 2026.1. |
| **Meta-analysis** | [`metafor`](https://www.metafor-project.org/) | The definitive R meta-analysis package. Random/mixed-effects, moderator analysis, publication bias, forest/funnel plots. |
| **Power analysis** | `pwr` + `simr` | `pwr` for standard designs. `simr` for simulation-based power for complex/mixed models. |

### Bayesian (Future Phase)

| Layer | Package | Why this one |
|-------|---------|-------------|
| **Bayesian regression** | [`brms`](https://paul-buerkner.github.io/brms/) | Makes Stan accessible. Formula interface mirrors `lme4`. Excellent documentation. |
| **Bayesian testing** | `bayestestR` (easystats) | Bayes factors, ROPE, credible intervals. Consistent with easystats ecosystem. |

---

## Python Stack

### Pipeline & Environment

| Layer | Package | Version (April 2026) | Why this one |
|-------|---------|---------------------|-------------|
| **Pipeline** | [Snakemake](https://snakemake.readthedocs.io/) | v9.19.0 | Python-native DAG workflow. Tilburg Science Hub has social science templates. FAIR-compliant via WorkflowHub integration. Scales from laptop to cluster. |
| **Lightweight alternative** | `Makefile` | — | For simple projects. Zero dependencies. Most common "pipeline" in empirical economics. |
| **Environment** | [`uv`](https://github.com/astral-sh/uv) | Current 2026 | 10-100x faster than pip. Deterministic lockfiles. Cross-platform reproducibility. The modern standard. |
| **Literate programming** | [Quarto](https://quarto.org/) + Jupyter | Current 2026 | Same as R — Quarto renders `.qmd` and `.ipynb`. Native Positron notebook support with interactive data grids. |

### Data Wrangling & Validation

| Layer | Package | Why this one |
|-------|---------|-------------|
| **Data wrangling (primary)** | [`polars`](https://pola.rs/) | v1.39.3 (March 2026). Rust-powered, 30x+ faster than pandas. Lazy evaluation, automatic parallelism. Cleaner API. |
| **Data wrangling (compat)** | `pandas` | Some packages still require pandas input. Use `.to_pandas()` at boundaries. |
| **Data validation** | [`pandera`](https://pandera.readthedocs.io/) | v0.30.1 (March 2026). Type-checked dataframe schemas. Works with pandas, polars, dask. Pydantic-style syntax. Hypothesis testing built in. |
| **Missing data visualization** | `missingno` | Quick visual diagnosis of missingness patterns. |

### Visualization & Tables

| Layer | Package | Why this one |
|-------|---------|-------------|
| **Visualization** | `matplotlib` + `seaborn` + [`plotnine`](https://plotnine.org/) | `plotnine` = ggplot2 grammar in Python. `seaborn` for statistical plots. `matplotlib` as the foundation. |
| **Tables** | [`great_tables`](https://posit-dev.github.io/great-tables/) | Python port of `gt`. Publication-quality. Posit-maintained. |

### Statistics

| Layer | Package | Why this one |
|-------|---------|-------------|
| **General statistics** | `statsmodels` + [`pingouin`](https://pingouin-stats.org/) | `pingouin` has the friendliest API for common tests (t-tests, ANOVA, correlations, effect sizes). `statsmodels` for OLS, GLM, time series. |
| **ML** | `scikit-learn` | Standard for supervised/unsupervised ML. Preprocessing pipelines, cross-validation. |
| **SEM** | `semopy` | Best available in Python, though `lavaan` in R is stronger for complex models. |

### Bayesian (Future Phase)

| Layer | Package | Why this one |
|-------|---------|-------------|
| **Bayesian modeling** | [`pymc`](https://www.pymc.io/) | The Python Bayesian standard. NUTS sampler, variational inference. |
| **Bayesian diagnostics** | [`arviz`](https://python.arviz.org/) | Visualization and diagnostics for Bayesian models. Works with PyMC, Stan, etc. |

---

## Cross-Language Tools

| Tool | Purpose |
|------|---------|
| **Quarto** | Literate programming for both R and Python |
| **Git + GitHub** | Version control (code only — data via OSF/Dataverse) |
| **Docker / Apptainer** | Containerized reproducibility (for complex environments) |
| **OSF** | Data/materials repository with DOI |
| **Cornell README template** | Standardized data documentation (CC0 licensed) |

---

## What we deliberately excluded

| Tool | Why excluded |
|------|-------------|
| DVC | On roadmap for future phase. Currently ML/data-engineering focused with negligible social science adoption, but data versioning features are valuable for large longitudinal datasets. Will evaluate when social science adoption grows. |
| Prefect / Dagster / Airflow | Enterprise orchestrators. Overkill for research. |
| Poetry | Slower than uv, less lockfile determinism. uv is the 2026 standard. |
| R Markdown | Superseded by Quarto. |
| `drake` (R) | Superseded by `targets` (same author). |
| `great_expectations` (Python) | Enterprise-focused. Pandera is lighter and more research-friendly. |

---

## Update policy

Run `/research-zeitgeist` monthly. It web-searches for:
- New CRAN/PyPI releases for all listed packages
- Updated methodology guidelines (ASA, APA, PRISMA)
- Community shifts in best practice
- New packages that supersede current choices

Every finding is dated. No change is made without verification.

*Last verified: April 10, 2026*

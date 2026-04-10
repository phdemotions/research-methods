# Domain Focus — Business Research

> This skill suite is purpose-built for quantitative business research.
> Not generic "data science." Not bioinformatics. Not machine learning engineering.
> Business, marketing, consumer behavior, management, and organizational behavior.

---

## Why domain matters

A generic research package would tell you to "run a regression." A business research package knows that:

- Consumer psychologists think in terms of **PROCESS models** (Hayes), not just `lm()`
- Marketing researchers care about **brand constructs**, **purchase intention**, **willingness to pay** — not abstract `x1`, `x2`
- Management scholars use **multilevel models** because employees are nested in teams in organizations
- The difference between a JCR paper and a rejection often comes down to **robustness checks** and **alternative specifications**
- Reviewers at top business journals (FT50) have specific expectations for tables, reporting, and transparency

## Key Methodological Families

### 1. Regression & Extensions

The bread and butter. OLS, logistic, ordinal, Poisson. With:
- Cluster-robust standard errors (because business data is almost always clustered)
- Fixed effects for panel data (`fixest`)
- Interaction effects with proper visualization (Johnson-Neyman plots)
- Heterogeneity analysis across subgroups

### 2. Structural Equation Modeling (SEM)

Via `lavaan`. Covers:
- Confirmatory Factor Analysis (CFA) — measurement model validation
- Path analysis — testing theoretical models
- Mediation analysis — direct/indirect effects with bootstrap CIs
- Moderation analysis — interaction effects in latent variable framework
- Multi-group SEM — testing model invariance across groups
- Latent growth models — longitudinal change

### 3. PROCESS Models (Mediation/Moderation/Conditional Process)

The Hayes PROCESS macro is the lingua franca of consumer psychology and marketing. This suite provides:
- `bruceR::PROCESS()` for familiar model-number syntax (Models 1-24)
- `lavaan` for transparent, inspectable implementation of the same models
- A mapping layer: "PROCESS Model 14" → correct `lavaan` syntax
- Bootstrap confidence intervals for indirect effects
- Index of moderated mediation
- APA-formatted output matching PROCESS tables

### 4. Meta-Analysis

Via `metafor`. For:
- Effect size computation (Cohen's d, Hedges' g, odds ratios, correlations)
- Random-effects and mixed-effects models
- Moderator analysis (meta-regression)
- Publication bias (funnel plots, trim-and-fill, PET-PEESE, p-curve)
- Forest plots (publication-ready)

### 5. Mixed Methods / Multilevel

Via `lme4`/`lmerTest`. For:
- Hierarchical linear modeling (HLM)
- Nested data structures (students in classrooms, employees in firms)
- Random intercepts and slopes
- Cross-level interactions
- ICC computation and reporting

### 6. Bayesian Analysis (Future Phase)

Via `brms`/`pymc`. Not immediate priority but architecturally planned:
- Bayesian regression with informative priors
- Bayes factors for hypothesis testing
- Credible intervals
- Model comparison via LOO/WAIC

---

## Target Journals

The skill suite's formatting, reporting, and transparency standards are calibrated to the expectations of:

### FT50 / UTD24 Business Journals
- **Journal of Consumer Research** (JCR)
- **Journal of Marketing Research** (JMR)
- **Journal of Marketing** (JM)
- **Journal of Consumer Psychology** (JCP)
- **Management Science** (MS)
- **Academy of Management Journal** (AMJ)
- **Academy of Management Review** (AMR)
- **Administrative Science Quarterly** (ASQ)
- **Strategic Management Journal** (SMJ)
- **Organization Science** (OS)
- **Journal of International Business Studies** (JIBS)
- **Journal of Financial Economics** (JFE)

### Methods-Focused Journals
- **Organizational Research Methods** (ORM)
- **Journal of Business Research** (JBR)
- **Psychometrika**
- **Multivariate Behavioral Research** (MBR)

### Open Science Standards
- **TOP Guidelines** Level 2+ (data/code transparency required)
- **JARS** (APA Journal Article Reporting Standards)
- **CONSORT** (for experimental studies)
- **STROBE** (for observational studies)
- **PRISMA** (for systematic reviews/meta-analyses)

---

## Variable Naming Convention

Skills generate code that uses domain-appropriate variable names:

| Instead of... | Use... |
|--------------|--------|
| `x1` | `brand_authenticity` |
| `y` | `purchase_intention` |
| `m` | `perceived_value` |
| `w` | `consumer_expertise` |
| `control1` | `age`, `gender`, `income` |
| `dv` | The actual construct name |
| `iv` | The actual construct name |

Every variable name must trace back to the codebook. If a construct has a common abbreviation in the literature (e.g., `WTP` for willingness to pay), that's acceptable with a comment.

---

## Construct Measurement Standards

When the skill suite encounters survey/scale data, it knows to check:

1. **Reliability** — Cronbach's alpha, McDonald's omega, composite reliability
2. **Validity** — CFA factor loadings, AVE, discriminant validity (Fornell-Larcker, HTMT)
3. **Common method variance** — Harman's single factor test, CFA marker variable approach
4. **Scale documentation** — source citation, number of items, response anchors, sample items

---

## What Business Researchers Care About That Generic Packages Miss

1. **Manipulation checks** — for experimental studies, did the manipulation work?
2. **Attention checks** — did participants pay attention? What's the exclusion rate?
3. **Effect sizes in context** — not just "eta-squared = .06" but "this is a medium effect in consumer behavior research"
4. **Practical significance** — what does this mean for managers?
5. **Preregistration alignment** — did you test what you said you'd test?
6. **Supplementary analyses** — the stuff that goes in the online appendix
7. **Replication readiness** — can another lab reproduce this with a different sample?

---

*Last updated: April 10, 2026*

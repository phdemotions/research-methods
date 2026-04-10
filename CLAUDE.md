# research-methods — Claude Code Project Instructions

> Gold-standard Claude Code skills for reproducible quantitative research in R and Python.
> Domain: Business, marketing, consumer behavior, management, organizational behavior.

## What this repo is

A standalone, publishable skill suite that guides every stage of quantitative research — from project setup to OSF packaging. Skills produce code and documentation that a senior researcher at a top business school would be proud to publish.

## Key docs

| Doc | Purpose |
|-----|---------|
| `docs/ARCHITECTURE.md` | Full design: directory structures, skill patterns, self-improvement mechanism |
| `docs/FRAMEWORKS.md` | Every framework choice, verified April 2026, with rationale |
| `docs/DOMAIN.md` | Business research domain focus, target journals, methodological families |
| `docs/SKILLS.md` | Complete specification for every skill |

## Core principles

1. **Raw data is sacred** — never modified, only read
2. **One command reproduces everything** — `tar_make()` (R) or `snakemake` (Python)
3. **Every subjective decision is documented** — decision log with rationale

## Framework stack (verified April 2026)

**R:** targets + renv + tidyverse + pointblank + ggplot2 + gtsummary + modelsummary + easystats + fixest + lavaan + bruceR + metafor + Quarto

**Python:** Snakemake + uv + polars + pandera + plotnine + great_tables + statsmodels + pingouin + Quarto

## Default formatting

APA 7th edition. Journal-specific overrides available for JCR, JMR, JCP, Management Science, AMJ, ASQ.

## IDE

Positron (primary). Compatible with any IDE supporting Claude Code.

## Skills live at

`.claude/skills/` — follows thin SKILL.md + references/ pattern from the Opus Vita audit suite.

## Updating

Run `/research-zeitgeist` monthly to verify all framework recommendations against current best practices.

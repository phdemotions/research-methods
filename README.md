# research-methods

> Gold-standard Claude Code skills for reproducible quantitative research in R and Python.
> Built for business researchers. Publishable on OSF. Designed so a senior faculty member at Harvard, Stanford, or Wharton would be proud to attach their name to the code.

## What this is

A suite of Claude Code skills that guide every stage of quantitative research — from project setup to OSF packaging — enforcing best practices that meet the highest standards of open science, transparency, and reproducibility.

These skills don't generate generic boilerplate. They read your research question, your pre-registration, your codebook, and your decision log, then produce analysis code and documentation that is specific to your project, your constructs, and your discipline.

## Who this is for

- Business, marketing, and consumer behavior researchers
- Management and organizational behavior scholars
- Anyone doing quantitative social science who wants their code to be publication-ready
- Researchers transitioning from SPSS/Stata to R/Python who want to do it right

## The three non-negotiable principles

1. **Raw data is sacred.** Never modified, only read. Every transformation is logged and reversible.
2. **One command reproduces everything.** From raw data to final manuscript tables and figures.
3. **Every subjective decision is documented.** Exclusion criteria, outlier handling, variable transformations, model specification choices — all written into a decision log with rationale.

## IDE

Built with [Positron](https://positron.posit.co/) as the primary IDE, but works with any IDE that supports Claude Code (VS Code, JetBrains, etc.).

## Skills

### Layer 1 — Project Lifecycle (the workflow)

| Skill | Purpose |
|-------|---------|
| `/research-intake` | **The entry point.** Bidirectional review: gap analysis of your materials + suite learning from what you bring |
| `/research-init` | Scaffold a new research project with full reproducibility infrastructure |
| `/data-validate` | Declarative data quality checks, codebook generation, FAIR compliance |
| `/data-clean` | Cleaning scripts that log every transformation, CONSORT-style exclusion flow |
| `/eda` | Exploratory analysis with publication-quality figures and descriptive tables |
| `/analyze` | Confirmatory analysis matched to pre-registration, with assumption testing |
| `/robustness` | Sensitivity analysis, specification curves, multiverse analysis |
| `/visualize` | Publication-quality figures (APA 7th, colorblind-safe, journal-spec DPI) |
| `/report` | Manuscript-ready tables and APA-formatted results paragraphs |
| `/reproduce` | Package everything for OSF/Dataverse with full documentation |

### Layer 2 — Quality Gates (the audit)

| Skill | Purpose |
|-------|---------|
| `/research-review` | Methods-expert code review: statistical rigor, transparency, reproducibility |
| `/pre-submit` | Pre-submission checklist: JARS, effect sizes, data availability, CRediT |
| `/reproduce-check` | Actually reproduces results from scratch and compares output |

### Layer 3 — Learning/Evolution (the self-improvement)

| Skill | Purpose |
|-------|---------|
| `/research-zeitgeist` | Date-aware scan of current best practices for R/Python research tools |
| `/method-advisor` | Recommends appropriate statistical methods with citations and assumptions |
| `/process-model` | PROCESS-style mediation/moderation via lavaan (Hayes model number mapping) |

## Frameworks

See [docs/FRAMEWORKS.md](docs/FRAMEWORKS.md) for the complete, verified framework stack with rationale for every choice.

## Quick start

```bash
# Clone into your Claude Code skills directory or use as a standalone repo
git clone <this-repo> ~/developer/research-methods

# Skills are auto-available when working in this directory
# Or symlink into your global skills:
# ln -s ~/developer/research-methods/.claude/skills/* ~/.claude/skills/
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for full design documentation.

## License

MIT

---

*Last verified: April 2026 — All framework recommendations web-searched and confirmed current.*

# Implementation Plan — research-methods Skill Suite

> **Status:** Active
> **Created:** 2026-04-10
> **Location:** `~/developer/research-methods/`
> **Purpose:** Gold-standard Claude Code skills for reproducible quantitative research in R and Python, focused on business/marketing/consumer behavior.

---

## What Exists

### Design documents (complete)
- `CLAUDE.md` — project instructions
- `docs/ARCHITECTURE.md` — directory structures, skill patterns, self-improvement mechanism
- `docs/FRAMEWORKS.md` — every R/Python framework choice, verified April 2026
- `docs/DOMAIN.md` — business research domain focus, target journals, methods
- `docs/SKILLS.md` — complete spec for all 16 skills across 3 layers
- `docs/ORCHESTRATION.md` — hooks, composite skills, feedback loops, auto-chaining

### Shared skill resources (complete, 6 files)
- `.claude/skills/_shared/project-discovery.md`
- `.claude/skills/_shared/r-standards.md`
- `.claude/skills/_shared/python-standards.md`
- `.claude/skills/_shared/apa-formatting.md`
- `.claude/skills/_shared/transparency.md`
- `.claude/skills/_shared/severity-scale.md`

### Hook stub (partial)
- `.claude/hooks/raw-data-guard.py` — exists but needs verification

### Empty skill directories (structure only, no SKILL.md yet)
- All 16 skill directories were `mkdir`'d with `references/` subdirs

---

## What Needs to Be Built

### Skill SKILL.md + references/ files (16 skills)

Each skill needs:
- `SKILL.md` — thin entry with frontmatter (name, description, argument-hint) + instructions
- `references/principles.md` — core principles for this stage
- `references/criteria.md` — specific checks/requirements/rubric
- `references/templates/` — output templates where applicable (e.g., decision log entry template, codebook template, CONSORT flow template)

### Hooks (4)
- `.claude/hooks/raw-data-guard.py` — PreToolUse, block Edit/Write on `data/raw/`
- `.claude/hooks/pipeline-stale-check.py` — UserPromptSubmit, advisory when pipeline cache is stale
- `.claude/hooks/research-session-end.py` — UserPromptSubmit, farewell detection → `/research-audit --quick`
- `.claude/hooks/prereg-drift-check.py` — PostToolUse, advisory when analysis code deviates from pre-registration

### Composite/orchestration skills (2)
- `/research-pipeline` — full workflow orchestrator, chains skills in dependency order with decision points
- `/research-audit` — dispatches 5 stakeholder audits in parallel, synthesizes composite verdict

### Stakeholder audit personas (5)
- `audit-methods-reviewer/` — Reviewer 2 (statistical rigor)
- `audit-senior-faculty/` — department chair (would I put my name on this?)
- `audit-journal-editor/` — AE at JCR/JMR (desk rejection lens)
- `audit-open-science/` — reproducibility advocate (FAIR, transparency)
- `audit-domain-expert/` — business research specialist (field conventions)

### Feedback skill (1)
- `/research-feedback` — structured researcher input → skill improvement proposals

### Infrastructure
- `.claude/settings.json` — project-level hook registration
- `_shared/output-contract.md` — report template for research audit skills (mirrors Opus Vita pattern)
- `_shared/research-scope.md` — how to determine audit scope for research projects
- Templates that `/research-init` will scaffold (directory skeleton, `_targets.R` stub, `Snakefile` stub, decision log template, codebook template, README template, etc.)

---

## Implementation Phases

### Phase 1: Foundation Skills
**Goal:** A researcher with existing data can scaffold a project, validate data, and clean it — the highest-value "data already collected" workflow.

#### 1A. Shared infrastructure additions
- [ ] `_shared/output-contract.md` — research audit report template (adapt from Opus Vita `_audit-shared/output-contract.md`)
- [ ] `_shared/research-scope.md` — how to determine what to audit in a research project (adapt from `_audit-shared/session-scope.md`)
- [ ] `_shared/next-steps.md` — auto-chaining rules (which skill to suggest next, from ORCHESTRATION.md)

#### 1B. `/research-init` — Project scaffolding
- [ ] `research-init/SKILL.md` — frontmatter + instructions for scaffolding
- [ ] `research-init/references/principles.md` — reproducibility principles for project setup
- [ ] `research-init/references/criteria.md` — what a well-structured research project needs
- [ ] `research-init/references/templates/` — all scaffolding templates:
  - `_targets.R` pipeline stub
  - `Snakefile` stub
  - `00_setup.R` / `00_setup.py`
  - Decision log `TEMPLATE.md`
  - Codebook template
  - README template (Cornell-based)
  - Pre-registration skeleton
  - Quarto manuscript template (`manuscript.qmd`)
  - `.gitignore` for research projects
  - `CITATION.cff` template
- [ ] Test: scaffold a real project, verify all files are correct

#### 1C. `/data-validate` — Data quality assessment
- [ ] `data-validate/SKILL.md` — frontmatter + validation workflow
- [ ] `data-validate/references/principles.md` — data quality principles
- [ ] `data-validate/references/criteria.md` — what to check (completeness, distributions, impossible values, duplicates, outliers, encoding, attention checks, manipulation checks)
- [ ] Test: run against a sample dataset

#### 1D. `/data-clean` — Documented data cleaning
- [ ] `data-clean/SKILL.md` — frontmatter + cleaning workflow
- [ ] `data-clean/references/principles.md` — cleaning principles (never modify raw, log everything, CONSORT flow)
- [ ] `data-clean/references/criteria.md` — cleaning checklist
- [ ] `data-clean/references/templates/consort-flow.md` — CONSORT exclusion flow template
- [ ] Test: clean a sample dataset, verify logging and flow diagram

#### 1E. Hooks (foundation pair)
- [ ] `.claude/hooks/raw-data-guard.py` — verify/complete the PreToolUse hook
- [ ] `.claude/settings.json` — register the raw-data-guard hook
- [ ] Test: try to edit a file in `data/raw/` and verify it's blocked

**Phase 1 exit criteria:** Can run `/research-init`, `/data-validate`, `/data-clean` in sequence on real data. Project has proper structure, codebook, cleaned data with exclusion documentation. Raw data is protected by hook.

---

### Phase 2: Analysis Core
**Goal:** A researcher can run exploratory and confirmatory analysis with proper assumption testing, effect sizes, and APA formatting.

#### 2A. `/eda` — Exploratory data analysis
- [ ] `eda/SKILL.md` — frontmatter + EDA workflow
- [ ] `eda/references/principles.md` — exploration principles (describe before testing, visualize distributions, check assumptions)
- [ ] `eda/references/criteria.md` — EDA checklist (Table 1, correlations, distributions, multicollinearity, normality)
- [ ] Test: run EDA on cleaned sample data

#### 2B. `/analyze` — Confirmatory analysis
- [ ] `analyze/SKILL.md` — frontmatter + analysis workflow (reads pre-registration, matches to planned analyses)
- [ ] `analyze/references/principles.md` — confirmatory analysis principles (assumption testing before modeling, always report effect sizes + CIs)
- [ ] `analyze/references/criteria.md` — analysis checklist by method type (regression, SEM, mixed models, meta-analysis)
- [ ] `analyze/references/method-templates/` — code skeletons for common methods:
  - OLS/GLM regression
  - Panel regression with fixed effects (fixest)
  - Mixed models (lme4/lmerTest)
  - SEM/CFA (lavaan)
  - Meta-analysis (metafor)
- [ ] Test: run confirmatory analysis on sample data

#### 2C. `/process-model` — PROCESS mediation/moderation
- [ ] `process-model/SKILL.md` — frontmatter + PROCESS workflow
- [ ] `process-model/references/principles.md` — mediation/moderation principles
- [ ] `process-model/references/criteria.md` — model specification checklist
- [ ] `process-model/references/hayes-models.md` — mapping of Hayes model numbers (1-24) to `lavaan` syntax + `bruceR::PROCESS()` equivalents
- [ ] Test: run Model 4 (simple mediation) and Model 14 (moderated mediation) on sample data

#### 2D. `/visualize` — Publication-quality figures
- [ ] `visualize/SKILL.md` — frontmatter + visualization workflow
- [ ] `visualize/references/principles.md` — publication figure principles (APA, colorblind, DPI, clean)
- [ ] `visualize/references/criteria.md` — figure checklist by type (interaction plots, mediation diagrams, forest plots, marginal effects, J-N plots)
- [ ] Test: produce figures from sample analysis output

#### 2E. Hooks (analysis pair)
- [ ] `.claude/hooks/prereg-drift-check.py` — PostToolUse advisory
- [ ] Update `.claude/settings.json` with PostToolUse hook registration
- [ ] Test: edit an analysis file with pre-registration present, verify advisory fires

**Phase 2 exit criteria:** Can run `/eda` → `/analyze` → `/process-model` → `/visualize` sequence. Results have proper assumption testing, effect sizes, CIs, APA formatting. PROCESS models produce transparent `lavaan` code. Figures are publication-ready. Pre-registration drift detection is active.

---

### Phase 3: Polish & Package
**Goal:** Manuscript-ready output and OSF packaging.

#### 3A. `/report` — Manuscript-ready output
- [ ] `report/SKILL.md` — frontmatter + reporting workflow
- [ ] `report/references/principles.md` — results writing principles
- [ ] `report/references/criteria.md` — reporting checklist (JARS compliance, APA formatting)
- [ ] `report/references/templates/results-paragraph.md` — template for APA results text by analysis type
- [ ] Test: generate results section from sample analysis

#### 3B. `/robustness` — Sensitivity analysis
- [ ] `robustness/SKILL.md` — frontmatter + robustness workflow
- [ ] `robustness/references/principles.md` — sensitivity analysis principles
- [ ] `robustness/references/criteria.md` — robustness checklist (alternative specs, subsamples, estimators, influence diagnostics, specification curve)
- [ ] Test: run robustness checks on sample analysis

#### 3C. `/reproduce` — OSF/repository packaging
- [ ] `reproduce/SKILL.md` — frontmatter + packaging workflow
- [ ] `reproduce/references/principles.md` — reproducibility principles (FAIR, TOP Guidelines)
- [ ] `reproduce/references/criteria.md` — packaging checklist
- [ ] `reproduce/references/templates/` — README (Cornell), CITATION.cff, session-info capture, Docker/Apptainer stubs
- [ ] Test: package a sample project and verify reproduction

**Phase 3 exit criteria:** Can generate manuscript-ready tables/text, run robustness checks, and produce an OSF-ready package from a complete analysis.

---

### Phase 4: Quality & Evolution
**Goal:** Self-improvement mechanism and quality gates.

#### 4A. `/research-review` — Methods code review
- [ ] `research-review/SKILL.md` — frontmatter + review workflow
- [ ] `research-review/references/principles.md` — review principles
- [ ] `research-review/references/criteria.md` — review rubric (statistical appropriateness, assumptions, reporting, reproducibility, transparency, common mistakes)
- [ ] Test: review a sample analysis project

#### 4B. `/pre-submit` — Pre-submission checklist
- [ ] `pre-submit/SKILL.md` — frontmatter + checklist workflow
- [ ] `pre-submit/references/criteria.md` — JARS checklist, journal-specific requirements
- [ ] Test: run pre-submit on a complete sample project

#### 4C. `/research-zeitgeist` — Best practices scanner
- [ ] `research-zeitgeist/SKILL.md` — frontmatter + scanning workflow (date-aware, web-search driven)
- [ ] `research-zeitgeist/references/principles.md` — how to evaluate "current" vs "dated"
- [ ] `research-zeitgeist/references/criteria.md` — what to check (package versions, methodology guidelines, journal policies, community shifts)
- [ ] `research-zeitgeist/references/sources.md` — authoritative sources to consult (key blogs, journals, package maintainers)
- [ ] Test: run zeitgeist scan and verify it finds real current information

#### 4D. `/method-advisor` — Statistical method recommendation
- [ ] `method-advisor/SKILL.md` — frontmatter + advisory workflow
- [ ] `method-advisor/references/decision-tree.md` — method selection logic (research question type × data structure × variable types × sample size → recommended method)
- [ ] `method-advisor/references/method-catalog.md` — catalog of methods with assumptions, citations, what to report
- [ ] Test: ask for method advice on several research scenarios

#### 4E. `/reproduce-check` — Reproduction verification
- [ ] `reproduce-check/SKILL.md` — frontmatter + verification workflow
- [ ] `reproduce-check/references/criteria.md` — reproduction checklist (fresh env, full pipeline, output comparison)
- [ ] Test: verify a sample project reproduces

**Phase 4 exit criteria:** Can review analysis code, check pre-submission readiness, scan for updated best practices, advise on methods, and verify reproduction. The suite is self-improving via `/research-zeitgeist`.

---

### Phase 5: Orchestration & Stakeholder Audits
**Goal:** Everything works together automatically. Composite audits from top-researcher personas.

#### 5A. Remaining hooks
- [ ] `.claude/hooks/pipeline-stale-check.py` — UserPromptSubmit advisory
- [ ] `.claude/hooks/research-session-end.py` — farewell detection → `/research-audit --quick`
- [ ] Update `.claude/settings.json` with all hooks registered
- [ ] Test: verify hooks fire correctly and don't conflict with global Opus Vita hooks

#### 5B. Stakeholder audit personas (5 skills)
Each follows the Opus Vita pattern: thin SKILL.md + `references/persona.md` + `references/criteria.md`

- [ ] `audit-methods-reviewer/` — Reviewer 2 (statistical rigor, assumption testing, effect sizes, power, multiple comparison correction, pre-registration alignment)
- [ ] `audit-senior-faculty/` — department chair (overall quality, theory-method fit, contribution clarity, co-authorship comfort, student exemplar worthiness)
- [ ] `audit-journal-editor/` — AE at JCR/JMR (desk-rejection criteria, fatal flaws, reviewer prediction)
- [ ] `audit-open-science/` — reproducibility advocate (FAIR, pre-registration, data/code sharing, computational reproducibility, transparency)
- [ ] `audit-domain-expert/` — business research specialist (field conventions, scale usage, citation patterns, PROCESS model appropriateness, target journal fit)
- [ ] Test: run each persona against a sample project

#### 5C. `/research-audit` — Composite stakeholder audit
- [ ] `research-audit/SKILL.md` — dispatches personas in parallel (mirrors `/session-audit` pattern)
- [ ] Supports `--full` (all 5 personas) and `--quick` (methods-reviewer + open-science only)
- [ ] Synthesizes composite verdict with cross-cutting themes, Top 5 fixes, wins
- [ ] Test: run full audit on a sample project

#### 5D. `/research-pipeline` — Full workflow orchestrator
- [ ] `research-pipeline/SKILL.md` — chains skills in dependency order with decision points
- [ ] Reads project state, determines which skills need to run (skips completed stages)
- [ ] Pauses at key decision points for researcher input
- [ ] Maintains pipeline status log at `docs/pipeline-status.md`
- [ ] Test: orchestrate a full workflow from init to reproduce on sample data

#### 5E. `/research-feedback` — Researcher feedback capture
- [ ] `research-feedback/SKILL.md` — structured feedback → skill improvement proposals
- [ ] `research-feedback/references/criteria.md` — feedback categories and how they map to skill files
- [ ] Test: provide feedback and verify it proposes concrete skill updates

**Phase 5 exit criteria:** All hooks fire correctly, stakeholder audits run in parallel and synthesize, pipeline orchestration works end-to-end, feedback mechanism captures and routes improvements. The full system is operational.

---

### Phase 6: Publishing & Documentation
**Goal:** Ready for GitHub release. The README, examples, and contribution guide make this a resource other researchers would actually use.

- [ ] Comprehensive `README.md` with installation, usage examples, screenshots of output
- [ ] `CONTRIBUTING.md` — how to add skills, update frameworks, submit feedback
- [ ] `examples/` directory with a sample research project demonstrating the full workflow
- [ ] `LICENSE` (MIT)
- [ ] `.github/` — issue templates, PR template
- [ ] Initial git commit with all content
- [ ] GitHub repo creation
- [ ] First `/research-zeitgeist` run to establish baseline

**Phase 6 exit criteria:** Published on GitHub. README is comprehensive. Example project demonstrates the full workflow. Others can install and use the skills.

---

## Dependencies Between Phases

```
Phase 1 (Foundation) ─────────────────► Phase 2 (Analysis)
    │                                       │
    │ _shared resources inform all           │ analysis output needed for
    │ subsequent skills                      │ polish & audit
    │                                       │
    ▼                                       ▼
Phase 5A (Hooks) ◄──── independent ────► Phase 3 (Polish)
                                            │
                                            ▼
                                       Phase 4 (Quality)
                                            │
                                            ▼
                                       Phase 5B-E (Orchestration)
                                            │
                                            ▼
                                       Phase 6 (Publishing)
```

- Phases 1 and 2 are strictly sequential (analysis needs clean data)
- Phase 5A (hooks) can be built in parallel with Phase 2 (no dependency)
- Phases 3 and 4 both depend on Phase 2 output but are independent of each other
- Phase 5B-E (stakeholder audits, orchestration) depends on individual skills existing
- Phase 6 depends on everything

---

## Key Design Decisions (Locked)

These were decided during the design conversation on April 10, 2026. They should not be revisited without explicit discussion:

1. **Standalone repo** at `~/developer/research-methods/`, not inside the Opus Vita monorepo structure
2. **Both R and Python** from day one — every skill produces both
3. **Snakemake** for Python pipeline (not DVC, not Prefect). DVC on roadmap for future data versioning.
4. **APA 7th default** with journal-specific overrides (JCR, JMR, JCP, MS, AMJ, ASQ)
5. **Bayesian deferred** to future phase — architecture supports it, not immediate priority
6. **PROCESS models via `bruceR::PROCESS()` + `lavaan`** — transparent, not black-box
7. **Positron** as primary IDE, but IDE-agnostic
8. **Skills guide** the researcher — they don't generate code blindly
9. **Thin SKILL.md + references/** pattern — matches Opus Vita audit suite
10. **Fail-open hooks** — errors never block the researcher's work
11. **Data-already-collected** as primary use case — most researchers come with data in hand
12. **Business research domain** — not generic data science
13. **Monthly self-improvement** via `/research-zeitgeist` web search

---

## How to Use This Plan

1. **Starting a session:** Read this plan + `CLAUDE.md` to know where we are.
2. **Working on a phase:** Check the boxes as items are completed.
3. **Testing:** Each phase has exit criteria. Don't move to the next phase until criteria are met.
4. **Updating:** When decisions change, update both this plan and the relevant docs/ file.

---

*Last updated: 2026-04-10*

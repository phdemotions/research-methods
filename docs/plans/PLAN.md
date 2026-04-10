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

### Skill SKILL.md + references/ files (17 skills)

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
**Goal:** A researcher with existing data can scaffold a project, validate data, and clean it — the highest-value "data already collected" workflow. Starts with a bidirectional intake review.

#### 1A. Shared infrastructure additions
- [x] `_shared/output-contract.md` — research audit report template
- [x] `_shared/research-scope.md` — how to determine what to audit in a research project
- [x] `_shared/next-steps.md` — auto-chaining rules (which skill to suggest next)

#### 1B. `/research-intake` — Bidirectional review (THE entry point)
The first skill that runs when a researcher shows up — before init, before validation.
- [x] `research-intake/SKILL.md` — frontmatter + bidirectional review workflow
- [x] `research-intake/references/principles.md` — intake principles (review what exists before prescribing)
- [x] `research-intake/references/criteria.md` — gap analysis rubric (documentation, data quality, code quality, methodology)
- [x] `research-intake/references/suite-learning.md` — inward review rubric (new methods, packages, patterns, conventions)
- [x] `research-intake/references/templates/gap-report.md` — structured output template
- [x] `research-intake/references/templates/suite-learning-report.md` — inward findings template
- [ ] Test: run intake on a real researcher's existing project materials

#### 1C. `/research-init` — Project scaffolding
- [x] `research-init/SKILL.md` — frontmatter + instructions for scaffolding
- [x] `research-init/references/principles.md` — reproducibility principles for project setup
- [x] `research-init/references/criteria.md` — what a well-structured research project needs
- [x] `research-init/references/templates/` — all scaffolding templates:
  - `_targets.R`, `Snakefile`, `setup.R`, `setup.py`, `decision.md`, `pre-registration.md`,
    `readme.md`, `manuscript.qmd`, `gitignore`, `citation.cff`, `pipeline-status.md`
- [ ] Test: scaffold a real project, verify all files are correct

#### 1D. `/data-validate` — Data quality assessment
- [x] `data-validate/SKILL.md` — frontmatter + validation workflow
- [x] `data-validate/references/principles.md` — data quality principles
- [x] `data-validate/references/criteria.md` — comprehensive validation rubric (6 categories)
- [ ] Test: run against a sample dataset

#### 1E. `/data-clean` — Documented data cleaning
- [x] `data-clean/SKILL.md` — frontmatter + cleaning workflow
- [x] `data-clean/references/principles.md` — cleaning principles (8 principles)
- [x] `data-clean/references/criteria.md` — cleaning checklist (8 sections)
- [x] `data-clean/references/templates/consort-flow.md` — CONSORT exclusion flow template
- [ ] Test: clean a sample dataset, verify logging and flow diagram

#### 1F. Hooks (foundation pair)
- [x] `.claude/hooks/raw-data-guard.py` — PreToolUse hook blocks Edit/Write on data/raw/
- [x] `.claude/settings.json` — hook registration for raw-data-guard
- [ ] Test: try to edit a file in `data/raw/` and verify it's blocked

**Phase 1 exit criteria:** Can run `/research-intake` → `/research-init` → `/data-validate` → `/data-clean` in sequence on real data. Intake produces a gap report AND suite-learning findings. Project has proper structure, codebook, cleaned data with exclusion documentation. Raw data is protected by hook.

---

### Phase 2: Analysis Core
**Goal:** A researcher can run exploratory and confirmatory analysis with proper assumption testing, effect sizes, and APA formatting.

#### 2A. `/eda` — Exploratory data analysis
- [x] `eda/SKILL.md` — frontmatter + EDA workflow
- [x] `eda/references/principles.md` — exploration principles (describe before testing, visualize distributions, check assumptions)
- [x] `eda/references/criteria.md` — EDA checklist (Table 1, correlations, distributions, multicollinearity, normality)
- [ ] Test: run EDA on cleaned sample data

#### 2B. `/analyze` — Confirmatory analysis
- [x] `analyze/SKILL.md` — frontmatter + analysis workflow (reads pre-registration, matches to planned analyses)
- [x] `analyze/references/principles.md` — confirmatory analysis principles (assumption testing before modeling, always report effect sizes + CIs)
- [x] `analyze/references/criteria.md` — analysis checklist by method type (regression, SEM, mixed models, meta-analysis)
- [x] `analyze/references/method-templates/` — code skeletons for common methods:
  - OLS/GLM regression
  - Panel regression with fixed effects (fixest)
  - Mixed models (lme4/lmerTest)
  - SEM/CFA (lavaan)
  - Meta-analysis (metafor)
- [ ] Test: run confirmatory analysis on sample data

#### 2C. `/process-model` — PROCESS mediation/moderation
- [x] `process-model/SKILL.md` — frontmatter + PROCESS workflow
- [x] `process-model/references/principles.md` — mediation/moderation principles
- [x] `process-model/references/criteria.md` — model specification checklist
- [x] `process-model/references/hayes-models.md` — mapping of Hayes model numbers (1-24) to `lavaan` syntax + `bruceR::PROCESS()` equivalents
- [ ] Test: run Model 4 (simple mediation) and Model 14 (moderated mediation) on sample data

#### 2D. `/visualize` — Publication-quality figures
- [x] `visualize/SKILL.md` — frontmatter + visualization workflow
- [x] `visualize/references/principles.md` — publication figure principles (APA, colorblind, DPI, clean)
- [x] `visualize/references/criteria.md` — figure checklist by type (interaction plots, mediation diagrams, forest plots, marginal effects, J-N plots)
- [ ] Test: produce figures from sample analysis output

#### 2E. Hooks (analysis pair)
- [x] `.claude/hooks/prereg-drift-check.py` — PostToolUse advisory
- [x] Update `.claude/settings.json` with PostToolUse hook registration
- [x] Test: edit an analysis file with pre-registration present, verify advisory fires

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

### Phase 6: Plugin Packaging & Distribution
**Goal:** Packaged as a Claude Code plugin. Installable via `/plugin install`. Auto-updates on version bump. Listed in community registries.

#### 6A. Plugin manifest
- [ ] `.claude-plugin/plugin.json` — plugin manifest with name, version, description, author, homepage, repository, license, keywords, and custom component paths pointing to `.claude/skills/` and `.claude/hooks/`
- [ ] `.claude-plugin/marketplace.json` — marketplace catalog entry so others can add this repo as a marketplace source
- [ ] `CHANGELOG.md` — versioned changelog (Keep a Changelog format)
- [ ] Verify: skills are discoverable as `research-methods:skill-name` after install
- [ ] Verify: hooks merge correctly with user's existing hooks after install
- [ ] Verify: `${CLAUDE_PLUGIN_ROOT}` paths resolve correctly in hook commands

#### 6B. Documentation for users
- [ ] `README.md` — rewrite for end-users: what this is, installation (`/plugin marketplace add`), skill list with one-line descriptions, quick start walkthrough, screenshots of output
- [ ] `CONTRIBUTING.md` — how to add skills, update frameworks, submit feedback, run `/research-zeitgeist`
- [ ] `LICENSE` (MIT)
- [ ] `.github/` — issue templates (bug, feature, skill request), PR template

#### 6C. Example project
- [ ] `examples/` directory with a sample research project demonstrating the full workflow
- [ ] Example uses real (or realistic synthetic) survey data
- [ ] Shows the complete chain: `/research-intake` → `/research-init` → `/data-validate` → `/data-clean` → `/eda` → `/analyze` → `/visualize` → `/report` → `/reproduce`
- [ ] Includes generated outputs: codebook, validation report, exclusion flow, figures, tables, manuscript draft

#### 6D. Community distribution
- [ ] First `/research-zeitgeist` run to establish framework baseline
- [ ] Submit to community registries:
  - [ ] alirezarezvani/claude-skills (PR to add to catalog)
  - [ ] travisvn/awesome-claude-skills (PR to add listing)
  - [ ] SkillsMP marketplace listing
- [ ] Consider: submit to Anthropic official marketplace at claude.ai/settings/plugins/submit
- [ ] Announce on relevant channels (academic Twitter/Bluesky, R-bloggers, methods communities)

#### 6E. Team/lab adoption support
- [ ] Document `extraKnownMarketplaces` pattern for `.claude/settings.json` so research labs can auto-trust this marketplace for all team members
- [ ] Document how to pin a specific version vs. track latest
- [ ] Document how to use alongside other plugins without conflicts

**Phase 6 exit criteria:** `pip install`-simple: a researcher runs two commands (`/plugin marketplace add`, `/plugin install`) and has all 17 skills available in any project. Version bumps auto-propagate. Listed in at least one community registry. Example project demonstrates the full workflow.

---

## Distribution Strategy

### How researchers install this

```bash
# One-time: add the marketplace
/plugin marketplace add phdemotions/research-methods

# Install into any project
/plugin install research-methods@phdemotions-research-methods
```

After install, all skills are namespaced and available:
```
/research-methods:research-init
/research-methods:data-validate
/research-methods:data-clean
/research-methods:eda
/research-methods:analyze
...
```

### Plugin structure (added in Phase 6A)

```
research-methods/
├── .claude-plugin/
│   ├── plugin.json              ← manifest (name, version, paths)
│   └── marketplace.json         ← catalog for /plugin marketplace add
├── .claude/
│   ├── skills/                  ← all skills (referenced by plugin.json)
│   │   ├── _shared/
│   │   ├── research-intake/
│   │   ├── research-init/
│   │   ├── data-validate/
│   │   ├── data-clean/
│   │   └── ...
│   ├── hooks/                   ← all hooks (referenced by plugin.json)
│   │   └── raw-data-guard.py
│   └── settings.json
├── CHANGELOG.md
├── README.md
└── examples/
```

The `plugin.json` uses custom component paths to point at `.claude/skills/` and `.claude/hooks/`:
```json
{
  "name": "research-methods",
  "version": "1.0.0",
  "skills": "./.claude/skills/",
  "hooks": "./.claude/settings.json"
}
```

This preserves dual-use: the repo works both as a **direct project** (clone and use `.claude/skills/` natively) AND as an **installable plugin** (via `/plugin install`).

### Version management

- Semantic versioning: `MAJOR.MINOR.PATCH`
- Version bumps in `plugin.json` trigger auto-updates for installed users
- `CHANGELOG.md` documents every release
- Pin-friendly: users can lock to a specific version in their marketplace config
- `${CLAUDE_PLUGIN_DATA}` directory for any persistent state that survives updates

### Distribution channels (by reach)

| Channel | Type | When |
|---------|------|------|
| GitHub repo | Direct | Phase 6A — immediate |
| Custom marketplace | Plugin system | Phase 6A — marketplace.json |
| Community registries | Discovery | Phase 6D — PRs to awesome-lists |
| Anthropic marketplace | Official | Phase 6D — submission if accepted |

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
14. **Plugin distribution** via Claude Code plugin system — `.claude-plugin/plugin.json` + marketplace.json. Dual-use structure: works as both a direct project (clone) and an installable plugin (`/plugin install`). Skills stay at `.claude/skills/`, plugin.json uses custom paths.
15. **Semantic versioning** — version bumps in plugin.json trigger auto-updates for installed users

---

## How to Use This Plan

1. **Starting a session:** Read this plan + `CLAUDE.md` to know where we are.
2. **Working on a phase:** Check the boxes as items are completed.
3. **Testing:** Each phase has exit criteria. Don't move to the next phase until criteria are met.
4. **Updating:** When decisions change, update both this plan and the relevant docs/ file.

---

*Last updated: 2026-04-10 — Distribution strategy added*

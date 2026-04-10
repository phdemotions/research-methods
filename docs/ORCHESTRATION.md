# Orchestration — How Skills Work Together

> Hooks enforce guardrails. Composite skills chain workflows. Feedback loops improve the suite.
> Nothing runs in isolation — every skill is aware of what came before and what comes next.

---

## The Three Orchestration Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                   Layer 4: BIDIRECTIONAL REVIEW                  │
│   /research-intake — runs at start AND end of every engagement  │
│   OUTWARD: gap analysis of researcher's materials vs standards  │
│   INWARD: what can our suite learn from what they brought?      │
│   └── gaps → skill dispatch, learnings → suite evolution        │
├─────────────────────────────────────────────────────────────────┤
│                     Layer 3: FEEDBACK LOOPS                      │
│   /research-feedback (user input) + /research-audit (personas)  │
│   Top-researcher stakeholder audits (Harvard/Stanford/Wharton)  │
│   └── findings flow back into skill improvements                │
├─────────────────────────────────────────────────────────────────┤
│                    Layer 2: COMPOSITE SKILLS                     │
│   /research-pipeline (full workflow orchestrator)                │
│   /research-audit (parallel stakeholder audit)                  │
│   └── dispatch individual skills in the right order/parallel    │
├─────────────────────────────────────────────────────────────────┤
│                      Layer 1: HOOKS                              │
│   raw-data-guard (PreToolUse) — prevent raw data modification   │
│   pipeline-stale-check (UserPromptSubmit) — detect stale cache  │
│   research-session-end (UserPromptSubmit) — wrap-up trigger     │
│   pre-registration-drift (PostToolUse) — flag deviations        │
│   └── always-on, defensive, fail-open                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Hooks

### 1. Raw Data Guard (`PreToolUse` on Edit/Write)

**File:** `.claude/hooks/raw-data-guard.py`

**Purpose:** Prevent any modification to files in `data/raw/`. Raw data is sacred — principle #1.

**Behavior:**
- Fires before every Edit or Write tool call
- Checks if the target file path is under `data/raw/`
- If yes: **blocks the tool call** with a clear error message explaining why
- If no: passes through silently

**Why a hook and not just a convention:** Conventions are forgotten. Hooks are enforced. A single accidental edit to raw data can invalidate an entire analysis — and you might not notice until peer review.

### 2. Pipeline Staleness Check (`UserPromptSubmit`)

**File:** `.claude/hooks/pipeline-stale-check.py`

**Purpose:** When the user starts working in a research project, check if the pipeline cache is stale (source files changed since last `tar_make()` / `snakemake` run).

**Behavior:**
- Fires on every user prompt
- Checks if CWD is a research project (has `_targets.R` or `Snakefile`)
- If analysis code (`R/*.R`, `python/*.py`) is newer than output (`output/`), injects a gentle reminder: "Pipeline may be stale — consider running `tar_make()` / `snakemake` to update outputs."
- Throttled: only reminds once per 30 minutes
- Never blocks — advisory only

### 3. Research Session-End Hook (`UserPromptSubmit`)

**File:** `.claude/hooks/research-session-end.py`

**Purpose:** When wrapping up a session in a research project, auto-trigger `/research-audit` (the lightweight version) and persist findings.

**Behavior:**
- Same farewell detection as the existing session-audit-trigger.py
- Only fires when CWD is a research project (not an app project)
- Triggers a two-step wrap-up:
  1. `/research-audit --quick` — fast methods review of changes
  2. `/end-session` — persist findings
- Coexists with the existing session-audit hook (which handles app projects)

**Priority logic:** If CWD has `_targets.R`/`Snakefile` → research hook fires. Otherwise → existing session-audit hook fires. Both can't fire for the same project.

### 4. Pre-Registration Drift Detector (`PostToolUse` on Edit)

**File:** `.claude/hooks/prereg-drift-check.py`

**Purpose:** When analysis code is modified, check if the change aligns with the pre-registration.

**Behavior:**
- Fires after Edit/Write on files in `R/04_analyze.R`, `python/04_analyze.py`, or any file matching `*analyze*`
- Reads `docs/pre-registration.md` (if it exists)
- Injects advisory context: "Analysis code was modified. Pre-registration exists at docs/pre-registration.md. If this change deviates from the pre-registered plan, document it in docs/decisions/ with rationale."
- Never blocks — advisory only
- Throttled: once per 15 minutes

---

## Layer 2: Composite Skills

### `/research-pipeline` — Full Workflow Orchestrator

**Purpose:** Run the complete research workflow in sequence, calling individual skills with proper handoffs.

**What it does:**
1. Reads project state (what exists, what's been done)
2. Determines which skills need to run (skips completed stages)
3. Chains skills in dependency order with handoffs:

```
research-init ──► data-validate ──► data-clean ──► eda
                                                    │
                                        ┌───────────┘
                                        ▼
                                    analyze ──► robustness
                                        │           │
                                        ▼           ▼
                                    visualize ──► report ──► reproduce
```

4. After each skill, checks output for errors/warnings
5. Asks the user for confirmation at key decision points:
   - After `/data-validate`: "These issues were found. How should we handle them?"
   - After `/data-clean`: "Exclusion flow shows N removed. Does this look right?"
   - After `/analyze`: "Results summary. Proceed to robustness checks?"
6. Maintains a pipeline status log at `docs/pipeline-status.md`

**Key design:** This is a **guided** orchestrator, not a blind executor. It pauses at decision points because research requires human judgment. The researcher is always in the loop.

### `/research-audit` — Composite Stakeholder Audit

**Purpose:** Run parallel stakeholder audits from top-researcher personas, then synthesize.

**Structure mirrors `/session-audit`:**
1. Dispatches 4-5 stakeholder lens audits as parallel subagents
2. Each stakeholder reads the analysis code, output, and documentation
3. Collects findings and synthesizes a composite verdict
4. Saves reports to `docs/audits/`

**The stakeholder personas (see Layer 3 below):**
- Methods Expert (Reviewer 2)
- Senior Faculty (department chair lens)
- Journal Editor (desk rejection criteria)
- Open Science Advocate (reproducibility purist)
- Domain Expert (business research conventions)

**Modes:**
- `--full` — all 5 stakeholders, comprehensive (for milestones)
- `--quick` — methods expert + open science only (for session-end)

---

## Layer 3: Feedback Loops

### `/research-feedback` — Researcher Input Capture

**Purpose:** Structured way for the researcher to improve the skill suite based on their experience.

**Triggers:** "feedback on the skills," "this isn't working," "I'd prefer it differently," "improve the skills"

**What it does:**
1. Asks the researcher structured questions:
   - "Which skill did you just use?"
   - "What worked well?"
   - "What didn't match how you actually work?"
   - "What would a senior colleague critique about the output?"
   - "What's missing?"
2. Saves feedback to `docs/feedback/YYYY-MM-DD-topic.md`
3. Maps feedback to specific skill files that should be updated
4. Proposes concrete changes to skill references (with approval)
5. Updates a rolling `docs/CHANGELOG.md` with improvements

**The feedback → improvement cycle:**
```
Researcher uses skill
    → notices something off
    → /research-feedback captures it
    → maps to specific skill reference files
    → proposes update
    → researcher approves
    → skill improves
    → /research-zeitgeist picks up the pattern next month
```

### Research Stakeholder Audits (Top-Researcher Personas)

Five personas that audit the research project from different elite perspectives:

#### 1. `audit-methods-reviewer` — Reviewer 2 (The Methodologist)

**Persona:** The reviewer at a top methods journal (ORM, MBR, Psychometrika) who has spent 20 years reviewing statistical analyses. They've seen every trick, every shortcut, every "p = .049" miracle. They don't care about your theory — they care about whether your analysis is defensible.

**Lens:** Statistical rigor, assumption testing, reporting completeness, effect size interpretation, power, multiple comparison correction, pre-registration alignment.

**The question they ask:** "Would I accept this methods section if I were reviewing for Organizational Research Methods?"

#### 2. `audit-senior-faculty` — The Department Chair

**Persona:** A tenured full professor at a top-5 business school who has published 100+ papers and supervised 30 dissertations. They've seen careers made and destroyed by sloppy research. They care about the whole package: theory, method, contribution, and — increasingly — open science credibility.

**Lens:** Overall research quality, theoretical grounding, contribution clarity, career implications of publishing this. Would they put their name on this as a co-author?

**The question they ask:** "Would I be proud to have my name on this paper? Would I recommend this to my PhD students as an example of how to do research?"

#### 3. `audit-journal-editor` — The AE at JCR/JMR

**Persona:** An associate editor at a top business journal who triages 200+ submissions a year. They desk-reject 60% in the first read. They're looking for fatal flaws, not minor issues — because their time is precious and they've learned to spot the patterns that predict "this will never make it through review."

**Lens:** Desk-rejection criteria: Is the contribution clear? Is the method appropriate for the question? Are there obvious red flags (no effect sizes, questionable exclusions, missing robustness)? Would reviewers tear this apart?

**The question they ask:** "Does this survive the first 10-minute skim, or does it go in the reject pile?"

#### 4. `audit-open-science` — The Reproducibility Advocate

**Persona:** A researcher who has built their career on meta-science and reproducibility. They've run large-scale replication projects, they serve on editorial boards that enforce TOP guidelines, and they evaluate open science badges for journals. They are passionate but fair — they know perfect reproducibility is hard and they respect honest effort.

**Lens:** FAIR compliance, pre-registration alignment, data/code availability, computational reproducibility, documentation quality, transparency of decision-making.

**The question they ask:** "If I tried to reproduce these results from the materials you've shared, would I succeed? And would I trust that you haven't p-hacked your way here?"

#### 5. `audit-domain-expert` — The Business Research Specialist

**Persona:** A senior marketing/consumer behavior researcher who knows the field's conventions, citation networks, and methodological norms. They know that business research has its own standards — PROCESS models are expected, certain constructs have established scales, and reviewers at JCR expect different things than reviewers at Management Science.

**Lens:** Domain conventions: Are you using established scales? Are you citing the right methods papers? Are you following the conventions of your target journal? Would other business researchers recognize this as competent work from someone who knows the field?

**The question they ask:** "Does this look like it was written by someone who publishes in this field, or by someone who just learned statistics?"

### `/research-audit` Synthesis

The composite skill dispatches all 5 personas (or a subset in `--quick` mode), collects their findings, and produces:

1. **Composite verdict:** Ready to submit / Needs revision / Major issues
2. **Cross-cutting themes:** What multiple personas flagged
3. **Top 5 highest-leverage fixes:** Prioritized by how many personas they satisfy
4. **Wins worth noting:** What the personas praised — this matters for morale
5. **Decision: which persona to listen to first** — not all feedback is equal for every project stage

---

## The Bidirectional Review — `/research-intake`

This is the critical skill that runs at the **start** of every engagement with existing materials, and again at the **end** of every session. It looks in two directions simultaneously.

### Direction 1: Outward — What the researcher's project needs (gap analysis)

Reviews everything the researcher has brought — data files, documentation, codebooks, analysis scripts, survey instruments, IRB materials, pre-registrations — and compares against our gold standards. Produces a structured gap report:

**Documentation gaps:**
- Is there a codebook? Does it meet our standards (variable names, types, scales, anchors, source citations)?
- Is there a decision log? Are subjective choices documented with rationale?
- Is there a pre-registration? Does the analysis plan match?
- Is there a README that follows the Cornell template?
- Is there IRB/ethics documentation?
- Is there a data provenance trail (where did this data come from, when, how)?

**Data quality gaps:**
- Is raw data separated from processed data?
- Are there validation checks in place?
- Is missingness documented? Exclusion criteria?
- Are scales documented with reliability metrics?
- Is the data in an open format (CSV/parquet) or trapped in proprietary format (.sav, .dta)?

**Code quality gaps:**
- Is there a pipeline (targets/Snakemake/Makefile)?
- Is the environment reproducible (renv.lock/uv.lock)?
- Are there tests?
- Does the code use domain-appropriate variable names?
- Is there session info captured?

**Methodology gaps:**
- Are effect sizes and CIs reported, not just p-values?
- Are assumptions tested before models are fit?
- Are robustness checks present?
- Is the analysis appropriate for the research design?

The output is a prioritized list: "Here's what you have, here's what's missing, here's what to fix first." Organized by severity (BLOCKER → MAJOR → MINOR → POLISH) using our research-calibrated severity scale.

### Direction 2: Inward — What our skill suite can learn (suite evolution)

Reviews what the researcher brought and asks: **does our skill suite cover this?**

**New methods encountered:**
- Did the researcher use a method our skills don't cover? (e.g., experience sampling, conjoint analysis, text analysis, network analysis, Bayesian methods we haven't added yet)
- Did they use a package we don't recommend? Is it better than what we have?
- Did they use a workflow pattern that's more efficient than what we scaffold?

**New documentation patterns:**
- Did their codebook have a structure we should adopt?
- Did they have a documentation practice we should add to our templates?
- Did their pre-registration format include something we don't?

**New domain conventions:**
- Did they reference a journal with requirements we haven't documented?
- Did they use a scale or construct measurement approach we should know about?
- Did they follow a reporting convention we should add to our APA formatting guide?

**Suite update proposals:**
- Each inward finding becomes a concrete proposal: "Add conjoint analysis to `/method-advisor` decision tree" or "Add experience sampling protocol to `/data-validate` criteria"
- Proposals are saved to `docs/feedback/suite-learning-YYYY-MM-DD.md`
- Proposals are surfaced to the researcher: "I noticed you use conjoint analysis — our skills don't cover that yet. Should I add it?"

### When it runs

| Trigger | Mode | Purpose |
|---------|------|---------|
| First encounter with researcher's data | **Full intake** | Complete gap analysis + suite learning |
| `/research-init` with existing data | **Outward only** | Gap analysis to guide scaffolding |
| Session end (via hook) | **Quick review** | What changed this session, any new gaps introduced or gaps closed? |
| `/research-feedback` | **Inward only** | Researcher explicitly says what's missing |
| `/research-zeitgeist` | **Inward only** | Monthly check for methods/tools we should add |

### The handoff

After the outward analysis, `/research-intake` produces a prioritized action plan that maps directly to which skills to run:

```
Gap: No codebook → Run /data-validate (generates one)
Gap: No exclusion documentation → Run /data-clean (produces CONSORT flow)
Gap: Raw data not separated → Run /research-init (scaffolds proper structure)
Gap: No pipeline → Run /research-init (creates _targets.R / Snakefile)
Gap: Effect sizes missing → Run /analyze (always includes them)
Gap: No pre-registration → Suggest creating one, or document analysis as exploratory
```

This is not just a checklist — it's a roadmap for the session. The researcher sees exactly what needs to happen and in what order.

### The session-end review

At session end, a lighter version runs:

1. **What gaps were closed this session?** (celebration + progress tracking)
2. **What gaps remain?** (carry-forward for next session)
3. **Did we encounter anything our suite doesn't handle?** (inward learning)
4. **Update `docs/pipeline-status.md`** with current state

This gives the researcher a clear "state of the project" snapshot and ensures nothing falls through the cracks between sessions.

---

## Skill Auto-Chaining Rules

Skills suggest (never force) the next skill in the pipeline:

| After this skill... | Suggest... | Condition |
|---------------------|-----------|-----------|
| `/research-intake` | `/research-init` | If project not scaffolded yet |
| `/research-intake` | `/data-validate` | If project exists but no codebook |
| `/research-intake` | `/data-clean` | If codebook exists but no cleaning docs |
| `/research-init` | `/data-validate` | If data exists in `data/raw/` |
| `/data-validate` | `/data-clean` | If validation found issues |
| `/data-clean` | `/eda` | Always |
| `/eda` | `/analyze` | Always |
| `/analyze` | `/robustness` | If primary results are significant |
| `/analyze` | `/research-audit --quick` | If this is a milestone |
| `/robustness` | `/visualize` | Always |
| `/visualize` | `/report` | Always |
| `/report` | `/pre-submit` | If targeting a specific journal |
| `/report` | `/reproduce` | If preparing for OSF |
| `/reproduce` | `/research-audit --full` | Before public sharing |
| `/research-zeitgeist` | Skill updates | If new best practices found |
| `/research-feedback` | Skill updates | When researcher provides input |

**Implementation:** Each skill's SKILL.md includes a "Next steps" section that the skill prints at the end of its run. This is a suggestion, not an automatic dispatch.

---

## Hook Registration

Hooks are registered in the project-level `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": ".claude/hooks/raw-data-guard.py",
          "timeout": 3
        }]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/pipeline-stale-check.py",
            "timeout": 5
          },
          {
            "type": "command",
            "command": ".claude/hooks/research-session-end.py",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": ".claude/hooks/prereg-drift-check.py",
          "timeout": 5
        }]
      }
    ]
  }
}
```

All hooks follow the fail-open pattern from the existing session-audit-trigger.py.

---

## Interaction with Existing Opus Vita Hooks

The research-methods hooks are **project-level** (in `.claude/settings.json` within the research project directory). The existing session-audit hooks are **global** (in `~/.claude/settings.json`). Project-level hooks fire in addition to global hooks.

The research-session-end hook detects research projects (`_targets.R`/`Snakefile`) and fires `/research-audit --quick`. The global session-audit hook detects app projects and fires `/session-audit`. They complement each other:

- **Research project in `~/developer/`** → both fire, but research hook takes priority for the methods audit, global hook handles `/end-session`
- **App project in `~/developer/`** → research hook skips (no research markers), global hook fires normally
- **Research project outside `~/developer/`** → only research hook fires

---

*Last updated: April 10, 2026*

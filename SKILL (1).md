---
name: commspro-deck-crafter
description: "Multi-slide deck generation using storyline frameworks and neuroscience-guided per-slide composition. Use when building presentations from content/notes — covers narrative selection, spine construction, and per-slide rendering. Capabilities: 8 storyline frameworks, archetype matching, McKinsey-quality output, interactive checkpoint workflow with mandatory gate rules."
---

# Storyline — Multi-Slide Deck Generation

Story first, slides follow. A deck is an argument — not a collection of pages. The storyline framework determines what each slide must communicate and in what order; the archetype system determines how each slide looks.

**File ownership**: This skill owns multi-slide storyline construction — context foundation, narrative selection, spine construction, content drafting, and spine validation. Per-slide layout and rendering is delegated to the per-slide neuroscience workflow (archetype matching, code generation, visual QA) defined later in this file.

**Interactive workflow**: The deck pipeline has **three user-facing checkpoints** (Steps 0, 1, and 2). The agent **stops and presents output** at each checkpoint, then waits for user approval before proceeding. Checkpoint 1 (narrative) may be skipped when user provides a pre-structured outline. Checkpoint 2 (detailed dot-dash) is user-skippable. After dot-dash approval, the agent drafts the complete slide content internally (no separate content-preview approval step) and proceeds to the Step 5 render consent, which is the final gate before generation.

**Before Checkpoint 0**, the agent presents an **ENTRY CHOICE** (see ENTRY POINT RULE): run the full Storyline flow (recommended), or skip straight to generation. The Storyline flow is the default and highest-quality path; the skip option lets users who already know what they want submit the generation job directly.

**MANDATORY GATE RULE — CRITICAL**: The agent MUST NOT proceed past a checkpoint without an explicit user response. Each checkpoint requires a STOP and WAIT. **The exceptions are (a) the user selects "Skip straight to generation" at the ENTRY CHOICE (see ENTRY POINT RULE), or (b) an explicit user opt-in to fast-track** (see "FAST-TRACK EXCEPTION" below) — in either case the agent skips the interactive checkpoints and proceeds to generation.

**Checkpoint sequence (MUST follow in order):**
1. **Checkpoint 0 (Context Foundation)** → Present table → STOP → Wait for user confirmation
2. **Checkpoint 1 (Narrative Selection)** → Present 3 variants (A, B, C) → STOP → Wait for user to pick one
3. **After variant selection** → Present "Generate slides" vs "Review storyline" prompt → STOP → Wait for user choice
4. **If user chose "Review storyline"** → Checkpoint 2 (Detailed dot-dash) → Present dot-dash → STOP → Wait for approval

**HARD RULES — NEVER VIOLATE** (these govern the DEFAULT flow; they are overridden ONLY by an explicit user fast-track opt-in — see "FAST-TRACK EXCEPTION" below)**:**
- NEVER skip Checkpoint 0 — always present the context table and wait for user confirmation before proceeding
- NEVER skip Checkpoint 1 — always present 3 narrative variants and wait for user to pick one (even if user provided a pre-structured outline — infer and confirm the narrative angle)
- NEVER select a narrative variant on behalf of the user — the user MUST explicitly say "A", "B", or "C"
- NEVER skip the "Generate slides vs Review storyline" prompt after variant selection — always present it and wait
- NEVER proceed to slide generation until the user has: (a) confirmed context, (b) selected a variant, AND (c) chosen how to proceed
- NEVER interpret ambiguous phrases ("go ahead", "sounds good", "generate it", "confirmed") as permission to skip a checkpoint that has not yet been presented — these phrases approve the CURRENT checkpoint only, they do not skip FUTURE ones
- NEVER batch multiple checkpoints into a single response — each checkpoint is a separate STOP point
- The agent offers a bypass in exactly ONE sanctioned place: the ENTRY CHOICE at the very start (see ENTRY POINT RULE). Apart from that, NEVER *proactively* offer or nudge a "fast-track" or "skip to spine" option mid-flow — once the user picks the Storyline flow, checkpoints are the default and mandatory for quality assurance. Checkpoints are skipped only via the ENTRY CHOICE bypass or an explicit user opt-in (see "FAST-TRACK EXCEPTION" below)

---

## FAST-TRACK EXCEPTION (bypass path — ENTRY CHOICE or explicit opt-in)

Checkpoints are the default and exist so the agent can iterate on the storyline with the user before generating. **However, if the user chooses to bypass the checkpoints and go straight to generation, honor it.** Some users already know what they want and find the confirmations blocking.

This bypass path is reached two ways, both of which run the same steps below:
- (a) The user selects **"Skip straight to generation"** at the ENTRY CHOICE (see ENTRY POINT RULE).
- (b) The user **explicitly asks** to bypass mid-request (see "When to fast-track" below).

### When to fast-track

Fast-track ONLY when the user gives an *explicit, unambiguous* instruction to skip the review/confirmation steps, e.g.:
- "Skip all checkpoints and just generate the deck"
- "No confirmations — build it now"
- "Fast-track to generation"
- "Bypass the review steps and render it"

**Do NOT fast-track on ambiguous approvals.** Phrases like "go ahead", "sounds good", "yes", "confirmed", or "generate it" approve only the CURRENT checkpoint — they do NOT opt into fast-track. If it is unclear whether the user wants to skip everything, ask once, then default to the normal checkpoint flow.

### What fast-track does

When triggered, run the entire pipeline WITHOUT stopping at Checkpoint 0, Checkpoint 1, the post-selection prompt, or Checkpoint 2 (content is drafted internally in Step 3, which has no approval stop), and proceed through render:

1. **Context Foundation** — if the user already confirmed context earlier in this flow, reuse it as-is. Otherwise, infer objective, audience, setting, and deck size from the content (default deck size Short 5-7 unless content volume or the user says otherwise). Do not stop to confirm.
2. **Narrative** — if the user already selected a variant earlier in this flow, use that variant. Otherwise, score the content against the 8 frameworks and auto-select the best-fitting variant. Either way, if the user provided a pre-structured outline, preserve it as the backbone.
3. **Build + validate the spine** internally (spine construction + density check + spine validation).
4. **Draft complete slide content** per Step 3 requirements and run the Pre-Output Validation internally.
5. **Render** — run the Pre-Render Validation, then proceed to Step 5 generation. The explicit fast-track opt-in also serves as render consent, so do NOT stop again for the Step 5 consent prompt. Still show render progress.

Display a one-line acknowledgement of the inferred settings as you go (e.g., "Fast-tracking: Decision deck, exec audience, Short (5-7), SCRA framework — generating now."), so the user can course-correct, but do not wait for a response.

### Guardrails (still enforced during fast-track)

- Run ALL internal validations (density, spine, pre-output, pre-render) — fast-track skips *stops*, not *quality checks*.
- NEVER fabricate data. If a hard blocker requires missing input (e.g., critical chart fields), ask the single necessary question, then continue.
- Fast-track applies only to the current request. It does not become the default for future requests.

---

## ENTRY POINT RULE (CRITICAL — read before ANY action)

**When invoked to build a deck, the FIRST action is to present the ENTRY CHOICE below — before Checkpoint 0.** Do not call any MCP tool or start Checkpoint 0 until the user picks a path.

### ENTRY CHOICE (present first, before Checkpoint 0)

Present exactly this, then STOP and wait for the user to pick:

```
How would you like to build this deck?

| Option | What happens |
|--------|--------------|
| **1) Storyline flow** (recommended) | I'll walk you through the plan — context, narrative, and structure — then generate. Highest-quality output. |
| **2) Skip straight to generation** | I'll bypass storyline planning and submit the generation job directly from your content. |

Completing the Storyline flow lets you review and adjust the plan before generating; you can also skip straight to generation.

Pick 1 or 2.
```

**STOP — wait for the user's choice.**

| User picks | Agent does |
|-----------|-----------|
| "1" / "Storyline" / "walk me through it" | Proceed to Checkpoint 0 (Context Foundation) and run the full flow below |
| "2" / "Skip" / "generate directly" | Emit the bypass notice below, then run the bypass path (see "FAST-TRACK EXCEPTION" above) |

**On bypass (Option 2):** first emit this one-line notice, then proceed to generation without any further checkpoints:

> Skipping the Storyline flow — I'll infer the settings and generate directly. (Completing it first would let you review and adjust the plan before generating.)

**Opening-request shortcuts (skip the menu only when the intent is explicit):**
- If the opening request ALREADY explicitly asks to bypass storyline / skip straight to generation (e.g., "skip storyline, just generate this"), skip the menu, emit the bypass notice, and run the bypass path.
- If the opening request ALREADY explicitly asks for the full storyline treatment, go straight to Checkpoint 0.
- For anything ambiguous ("Generate a deck from this file", "Create slides from this content", "Make me a PowerPoint", "Turn this into slides"), present the ENTRY CHOICE — do NOT assume a path.

### Once on the Storyline path

**NEVER call MCP tools (create_slide_deck, get_slide_deck_status) until:**
1. Checkpoint 0 (Context Foundation) has been presented AND user confirmed
2. Checkpoint 1 (Narrative Selection) has been presented AND user selected a variant (A/B/C)
3. User chose "Generate slides" or "Review storyline" at the post-selection prompt
4. If "Review storyline" chosen: Checkpoint 2 (Detailed dot-dash) presented AND user approved
5. Slide content was drafted (Step 3) and passed the Pre-Output Validation
6. Step 5 (Render Consent) has been presented AND user said "y" or "yes"

**Exception:** the ENTRY CHOICE bypass (Option 2) or an explicit fast-track opt-in (see "FAST-TRACK EXCEPTION" above) satisfies items 1–6 — the agent skips these interactive stops and proceeds after running all internal validations.

---

## STEP 0: Establish Context Foundation

Before selecting a storyline framework, establish the context that determines what "good" looks like for this deck. The same content can be excellent in one context and inadequate in another.

### Objective

Classify what the communication is trying to achieve:

| Objective | Description | Deck characteristics |
|-----------|-------------|---------------------|
| **Decision** | Driving a specific decision or securing approval | Options, trade-offs, recommendation, explicit ask |
| **Alignment** | Rallying stakeholders around a direction or vision | Aspirational, future-state, compelling narrative |
| **Action** | Driving execution: owners, timelines, accountability | Milestones, RACI, implementation specifics |
| **Understanding** | Building shared knowledge, transferring findings | Layered depth, navigation, self-sufficient narrative |

### Audience

| Dimension | Impact on deck |
|-----------|---------------|
| **Seniority** | CEO: governing thought + implications upfront. Working team: analytical depth |
| **Familiarity** | High: skip context, lead with what's new. Low: build progressively |
| **Internal vs client** | Client: higher polish, their language. Internal: shorthand OK |
| **Size** | Small (<=10): density OK. Large (25+): visual clarity dominates, 24pt+ |

### Setting

| Setting | Deck implications |
|---------|------------------|
| **Projected** | Low density, visual clarity, speaker provides connective tissue |
| **Pre-read** | Self-sufficient narrative, richer text, full sourcing |
| **Virtual** | Smaller effective screen, larger fonts, lower cognitive load |
| **Workshop** | Content deliberately incomplete, exercise framing dominates |

### Deck size

Ask the user how many slides they want. This drives framework selection and content density.

| Deck size | Slide count | When to use |
|-----------|-------------|-------------|
| **Short** | 5-7 slides | Executive briefings, SteerCo updates, focused decisions |
| **Standard** | 8-15 slides | Strategy proposals, diagnostic readouts, board papers |
| **Comprehensive** | 15+ slides | Pre-reads, playbooks, deep analytical deliverables |

Default to **Short (5-7)** unless user specifies otherwise or content volume clearly requires more.

### Step 0 output format (MANDATORY — CHECKPOINT 0)

**STOP HERE. Present the Context Foundation table and wait for user response. Do NOT proceed to narrative selection until the user explicitly confirms.**

Present exactly this structure, then STOP and wait for user response:

```
| Dimension | Classification |
|-----------|----------------|
| **Objective** | Decision — [1-line rationale] |
| **Audience** | [Seniority], [familiarity], [internal/client], [size] |
| **Setting** | [Pre-read / Projected / Virtual / Workshop] — [1-line rationale] |
| **Deck size** | Short (5-7) / Standard (8-15) / Comprehensive (15+) |

Confirm these settings, adjust any dimension — or, if you're ready to proceed straight to generation, just let me know.
```

**STOP — Do not continue until user responds.**

| User says | Agent does |
|-----------|-----------|
| "Confirmed" / "Looks good" / "Yes" | Proceed to Step 1 — present narrative variants (do NOT skip to generation) |
| "Change audience to ..." / "Make it standard length" | Update the table and re-present for confirmation |
| "Skip" | Use the presented defaults and proceed to Step 1 |
| "Jump to generation" / "Proceed to generation" / "I'm ready to generate" | Run the bypass path from here (see "FAST-TRACK EXCEPTION") — reuse this confirmed/inferred context, auto-fill the remaining steps, and generate |

**After user confirms:** Proceed to STEP 1 (Narrative Selection) — do NOT skip directly to slide generation.

---

## PRE-STRUCTURED INPUT HANDLING (Checkpoints 0 and 1 still required)

> **Scope:** This section applies once the user is on the Storyline path. If the user chose "Skip straight to generation" at the ENTRY CHOICE (or explicitly opted into fast-track), the bypass path applies instead — see ENTRY POINT RULE and "FAST-TRACK EXCEPTION".

**On the Storyline path, even when the user provides a slide-by-slide outline or detailed storyline, Checkpoints 0 and 1 are STILL MANDATORY.** The checkpoints infer context and narrative from the user's input rather than skipping.

### Why checkpoints are never skipped

1. **Checkpoint 0 (Context Foundation)** validates that the agent correctly understands the objective, audience, setting, and deck size — even if the user provided this implicitly
2. **Checkpoint 1 (Narrative Selection)** confirms the narrative angle, even when derived from user's structure — the user may want to adjust the framing

### When user provides a pre-structured outline

The user provides a numbered or bulleted slide-by-slide structure — a "dot-dash" outline. Examples:
- "Slide 1: executive summary, Slide 2: market overview, Slide 3: competitive analysis, ..."
- "1. Exec summary 2. Situation 3. Key findings 4. Recommendations 5. Next steps"
- Any input where the user has explicitly assigned content to slide positions

### What to do (MANDATORY flow — no skipping)

1. **Checkpoint 0 (Context Foundation)** — Infer context from the user's input and present for confirmation:
   - Analyze the content to infer objective (Decision/Alignment/Action/Understanding)
   - Infer audience from language, depth, and formality
   - Infer setting from content density and structure
   - Count slides from the outline to determine deck size
   - Present the context table with inferred values and ask user to confirm

2. **Checkpoint 1 (Narrative Selection)** — Present 3 variants that INCORPORATE the user's structure:
   - All 3 variants should preserve the user's slide assignments as the backbone
   - Variants differ in narrative ANGLE, not structure (e.g., "lead with risk" vs "lead with opportunity")
   - Make clear: "Your slide structure is preserved — these variants differ in narrative emphasis"
   - User picks A, B, or C to confirm the angle

3. **After variant selection** — Present "Generate slides" vs "Review storyline" prompt as usual

4. **Checkpoint 2 (Detailed dot-dash)** — Pre-populate with user's outline (titles + supporting points + sources); assign layouts internally

### What NOT to do

- Do NOT *proactively* offer to skip checkpoints — they are the default (but honor an explicit fast-track opt-in; see "FAST-TRACK EXCEPTION")
- Do NOT *proactively* present a "fast-track" or "skip to spine" option — never suggest it first
- Do NOT proceed to MCP rendering without completing all checkpoints, unless the user explicitly opted into fast-track
- Do NOT assume user's outline is final — checkpoints allow refinement

### Checkpoint 1 variant format (when user provided outline)

```
Your slide structure is preserved. These variants differ in narrative emphasis:

**Variant A — [Framework] | [Angle emphasizing X]**
[How this angle frames the same slides]

**Variant B — [Framework] | [Angle emphasizing Y]**
[Different framing of the same structure]

**Variant C — [Framework] | [Angle emphasizing Z]**
[Third framing option]

Pick A, B, or C to confirm the narrative angle.
```

### Legacy behavior (REMOVED)

The previous *auto-offered* "fast-track prompt" that proactively suggested skipping to the dot-dash has been removed — the agent never suggests skipping on its own. By default all decks go through Checkpoints 0 → 1 → (optional 2) → 3 → 4 → 5. The sole exception is an explicit user fast-track opt-in (see "FAST-TRACK EXCEPTION"), which the agent honors but never initiates.

---

## STEP 1: CHECKPOINT 1 — Narrative Selection

**STOP HERE. Present 3 narrative variants (A, B, C) and wait for the user to pick one. Do NOT proceed until user explicitly selects a variant.**

> **When user provided a pre-structured outline**: Still present 3 variants, but frame them as "narrative angle" options that preserve the user's slide structure. See "Checkpoint 1 variant format" above.

**CRITICAL:** This checkpoint is MANDATORY after Context Foundation confirmation. Do NOT skip this step. Do NOT select a variant on behalf of the user. Do NOT proceed to slide generation until the user has selected a variant AND chosen how to proceed.

### What to do

1. Extract substance from the user's content
2. During extraction, **tag each insight with its source section** — record which `##`/`###` header(s) from the input document each data point, metric, or argument came from. These tags are used in Checkpoint 2.
3. Score the content against all 8 frameworks (see framework definitions below)
4. Generate **3 narrative variants**

### What a "narrative variant" is

A narrative variant is a **complete storyline** — not just a framework name. It consists of:
- **Framework label** (e.g., "SCRA", "Pyramid + Frame/Deep-Dive")
- **Narrative angle** in 1 sentence
- **Narrative summary** — **HARD LIMIT: exactly 2 sentences, each ≤ 120 characters.** The elevator pitch for the entire deck. Ruthlessly concise — if it takes 3 sentences, cut. If a sentence exceeds 120 characters, split or shorten.

> **Validation rule (MANDATORY before presenting):** Count sentences in each variant's summary. If any variant has >2 sentences, rewrite until it has exactly 2. Count characters per sentence. If any sentence exceeds 120 characters, shorten it. Do NOT present variants to the user until all pass this check.

**Anti-pattern — DO NOT do this:**
```
❌ BAD (3+ sentences, 200+ chars each):
**Variant A — SCRA | "This time is structurally different"**
H&M's margin compression from 15% to 6-10% is structural, not cyclical — three prior AI
transformation cycles failed because they treated technology as the starting point and
organizational capability as an afterthought. The resolution inverts that sequence: lock in
governance, talent, and incentives first, then deploy a hybrid AI platform that captures the
only data moat H&M actually holds. Board authorizes three horizons with gate reviews.

✅ GOOD (2 sentences, each ≤120 chars):
**Variant A — SCRA | Governance before technology**
Margin compression is structural — organizational capability is the binding constraint.
Fix governance and talent first, then deploy the AI platform.
```

**Each variant must be meaningfully different** — not the same story with different words. Variants should differ in at least one of: (a) which dimension leads the narrative, (b) what the primary recommendation is, (c) what the audience walks away believing. If two variants feel interchangeable, replace one.

Two or more variants may use the same framework with different angles.

### Output format (MANDATORY)

Present exactly this structure, then STOP and wait for user response:

```
**Variant A — [Framework] | [Angle in 1 sentence]**
[Max 2 crisp sentences — the deck's elevator pitch]

**Variant B — [Framework] | [Angle in 1 sentence]**
[Max 2 crisp sentences — meaningfully different from A]

**Variant C — [Framework] | [Angle in 1 sentence]**
[Max 2 crisp sentences — meaningfully different from A and B]

Pick A, B, or C — or ask for refinement / more variants.
```

**STOP — Do not continue until user picks a variant (A, B, or C).**

---

### User actions at Checkpoint 1
2. Skip Step 1 (Checkpoint 1) entirely (regardless of A or B choice)
3. Go to Step 2 (Checkpoint 2) — pre-populate the dot-dash with the user's outline (titles + supporting points + sources), assigning layouts internally
4. The agent may suggest improvements (reorder, add missing slides, flag gaps) but MUST preserve the user's slide assignments as the starting point
5. Still enforce the executive summary rule (slide 1) and BACKUP + appendix (final slides) — add them if the user's outline omits them

### User actions at Checkpoint 1

**FIRST:** Wait for the user to pick a variant (A, B, or C).

**THEN:** After the user picks a variant, present this follow-up prompt (do NOT skip this prompt):

```
You selected Variant [X]. How would you like to proceed?

| Option | What happens |
|--------|--------------|
| **1) Generate slides** | I'll build the storyline, validate it, and generate slides directly |
| **2) Review storyline first** | I'll show you the dot-dash for review before generating |

Pick 1 or 2.
```

**STOP — Do not continue until user picks 1 or 2.**

| User says | Agent does |
|-----------|-----------|
| "A" / "B" / "C" | Present the follow-up prompt above (generate vs review) |
| "1" / "Generate slides" / "Just generate" | Use selected variant, run skip-to-generation workflow (see below), proceed directly to slide generation |
| "2" / "Review storyline" / "Review first" | Proceed to STEP 2 with the selected narrative |
| "Combine A and B" / "A but with more emphasis on X" | Refine and re-present variants |
| "Show me more variants" | Generate 2-3 additional variants |

---

### Skip-to-generation workflow

When the user chooses "Generate slides" (Option 1), run the following steps internally and display progress to the user:

```
Generating deck...
[1/4] Building storyline spine
[2/4] Validating narrative flow
[3/4] Drafting slide content
[4/4] Preparing for render
```

**What happens in the background:**
1. **Building storyline spine** — Apply the selected framework's spine template to the user's content, map content to slides, draft message-driven titles
2. **Validating narrative flow** — Run spine validation (no duplicate claims, each title adds new information, deep dives explain HOW/WHY/WHERE)
3. **Drafting slide content** — Generate complete content for each slide per Step 3 requirements
4. **Preparing for render** — Run pre-output validation internally, ensure MCP-ready format

After completion, proceed directly to Step 5 (render consent), having drafted and validated the content in Step 3.

**Progress display rule:** Update the progress indicator after each step completes. The user sees the current step in real-time.

---

### 8 Storyline Frameworks

#### 1. SCRA — Situation, Complication, Resolution, Ask

**Best for**: Decision decks (SteerCo, board, investment committee)

**Detect when**: Content has a recommendation, options to evaluate, or an explicit decision/approval needed

**Spine template (7-8 slides):**
0. **Cover page** — Title slide with presentation title, date, subtitle
1. **Executive summary** — One-page synthesis: recommendation + key stats + ask
2. **Situation** — Current state, credibility metrics, foundation
3. **Complication** — Tension, gaps, risks, burning platform
4. **Resolution (1-2 slides)** — Options, evaluation, recommended path
5. **Implementation** — Timeline, phasing, milestones, owners
6. **BACKUP** — Section divider (blank slide with title "Backup")
7. **Appendix** — Discussion questions

---

#### 2. Pyramid + Frame/Deep-Dive

**Best for**: Complex arguments requiring 7+ slides with dense evidence

**Detect when**: Content has a single governing thought supported by multiple evidence layers that each need their own slide

**Spine template (9-14 slides):**
0. **Cover page** — Title slide with presentation title, date, subtitle
1. **Executive summary** — One-page synthesis: governing thought + key stats + ask
2. **Frame — Situation** — Credibility and context
3. **Deep dive** — Detailed evidence behind one element of the framing
4. **Deep dive** — Second evidence angle
5. **Frame — Complication** — Competitive or structural tension
6. **Deep dive** — Specific competitive/diagnostic evidence
7. **Frame — Resolution** — Options introduced
8. **Deep dive** — How the recommended option works
9. **Deep dive** — Quantitative evaluation (scoring, trade-offs)
10. **Frame — Implementation** — Roadmap
11. **BACKUP** — Section divider
12. **Appendix** — Discussion questions

**Key rule**: Frames declare conclusions. Deep dives explain HOW/WHY/WHERE — never restate the conclusion with different numbers.

---

#### 3. Implication Ladder

**Best for**: Analytical deep-dives where findings need to be "laddered up" to action

**Detect when**: Content is primarily data, findings, or diagnostic outputs that need synthesis into implications and actions

**Spine template (7-9 slides):**
0. **Cover page** — Title slide with presentation title, date, subtitle
1. **Executive summary** — One-page synthesis: governing insight + key implications + ask
2. **Finding cluster 1** — Data/evidence + what it means
3. **Finding cluster 2** — Data/evidence + what it means
4. **Finding cluster 3** — Data/evidence + what it means
5. **Implication synthesis** — Across all findings: what must change
6. **Action/next steps** — Concrete actions with owners
7. **BACKUP** — Section divider
8. **Appendix** — Discussion questions

**Key rule**: Every finding must complete the chain: what the data shows -> what it means -> what to do about it.

---

#### 4. Schema Build

**Best for**: Multi-dimensional topics that need a visual map the audience follows progressively

**Detect when**: Content has 4+ interrelated dimensions, capabilities, or pillars that need to be introduced as a whole then explored individually

**Spine template (7-10 slides):**
0. **Cover page** — Title slide with presentation title, date, subtitle
1. **Executive summary** — One-page synthesis: schema overview + key finding + ask
2. **Schema overview** — Introduce the overarching structure/framework on one slide
3. **Dimension 1 deep dive** — Detail on first element of the schema
4. **Dimension 2 deep dive** — Detail on second element
5. **Dimension N deep dive** — Continue for each dimension
6. **Integration/synthesis** — How the dimensions connect, overall assessment
7. **BACKUP** — Section divider
8. **Appendix** — Discussion questions

**Key rule**: Maintain consistent visual language across the sequence so the audience tracks the build.

---

#### 5. Hypothesis-to-Narrative

**Best for**: Problem-solving sessions where the answer is not yet confirmed

**Detect when**: Content has hypotheses, evidence for and against, unknowns, or is framed as "we believe X because Y"

**Spine template (7-9 slides):**
0. **Cover page** — Title slide with presentation title, date, subtitle
1. **Executive summary** — One-page synthesis: hypothesis + key evidence + confidence level
2. **Working hypothesis** — "We believe [X] because [Y], which means [Z]"
3. **Evidence FOR** — What supports the hypothesis
4. **Evidence AGAINST / risks** — What challenges or contradicts it
5. **Refined hypothesis** — Updated view after weighing evidence
6. **Implications if true** — What to do if the hypothesis holds
7. **BACKUP** — Section divider
8. **Appendix** — Discussion questions

---

#### 6. Alignment / Vision

**Best for**: Town halls, transformation kick-offs, large-audience alignment moments

**Detect when**: Content is aspirational, describes a future state, change narrative, or is meant to rally/inspire

**Spine template (7-9 slides):**
0. **Cover page** — Title slide with presentation title, date, subtitle
1. **Executive summary** — One-page synthesis: vision + why now + call to action
2. **The vision** — Where we are headed and why it matters
3. **Why now** — The catalyst, burning platform, or opportunity window
4. **What changes** — Concrete shifts from current to future state
5. **How we get there** — Key pillars, workstreams, or enablers
6. **Rally / call to action** — Energizing close with specific next steps
7. **BACKUP** — Section divider
8. **Appendix** — Discussion questions

**Key rule**: 24pt+ fonts, high contrast, low cognitive load. The talk track carries the detail; slides carry the emotion and key anchors.

---

#### 7. Information Transfer / Playbook

**Best for**: Pre-reads, leave-behinds, training decks, playbooks, how-to guides

**Detect when**: Content is instructional, step-based, reference material, or needs to be self-sufficient without a presenter

**Spine template (7-12 slides):**
0. **Cover page** — Title slide with presentation title, date, subtitle
1. **Executive summary** — One-page synthesis: purpose, key takeaways, how to use this document
2. **Section 1** — First topic area with depth
3. **Section 2** — Second topic area with depth
4. **Section N** — Continue for each section
5. **Recap / key takeaways** — Synthesize across sections
6. **Resources / references** — Supporting materials
7. **BACKUP** — Section divider
8. **Appendix** — Discussion questions

**Key rule**: On-page narrative must be self-sufficient — the document must work without a presenter.

---

#### 8. Collaboration / Workshop

**Best for**: Facilitation guides, working sessions, interactive workshops

**Detect when**: Content includes exercises, breakout activities, discussion prompts, or is designed for group interaction

**Spine template (7-10 slides):**
0. **Cover page** — Title slide with presentation title, date, subtitle
1. **Executive summary** — One-page synthesis: session purpose + expected outcomes + agenda
2. **Ground rules / agenda** — How the session works, time allocation
3. **Exercise 1** — Activity framing + instructions + space for output
4. **Exercise 2** — Second activity
5. **Synthesis** — Capture key themes from exercises
6. **Next steps / commitments** — Who does what by when
7. **BACKUP** — Section divider
8. **Appendix** — Parking lot, additional resources

**Key rule**: Content is deliberately incomplete — the slides frame the exercises, not deliver the answers.

---

## STEP 2: CHECKPOINT 2 — Detailed dot-dash (user-skippable)

**STOP and present the storyline as a detailed dot-dash (McKinsey-style nested bullets). Wait for user approval before proceeding.**

**This checkpoint is always presented unless the user already skipped it.** The user may say "skip" or "just build it" to bypass it — but the AGENT must not skip it autonomously.

### Pre-construction: Insight extraction

Before building the spine, force every analysis output through the "so what?" filter:
- For every piece of content, ask: "So what does this mean for the audience's objective?"
- Cluster related insights — do they point to a common theme, tension, or choice?
- Write each insight as a complete sentence with subject, verb, and implication

### The "one thing" test

Before laying out slides, complete this sentence: "If the audience remembers only one thing from this deck, it should be ___."

If the team cannot fill in the blank with a specific, concrete statement, the thinking is not ready to become a deck.

### Cover page (MANDATORY — slide 0 in every deck)

Every multi-slide deck MUST begin with a cover page as slide 0. This is the title slide that introduces the presentation.

**Cover page content:**
- **Presentation title** — Derived from the storyline's governing thought (the "one thing")
- **Date** — Current date in format: Month DD, YYYY (e.g., "June 8, 2026")
- **Subtitle** (optional) — Client name, project name, or meeting context

**Layout:** Title slide archetype — centered text, minimal design, no body content.

**Deck naming convention:** The presentation title on the cover page determines the deck filename:
- Format: `YYYY-MM-DD_[topic-slug]`
- Example: If the governing thought is "AI transformation requires governance before technology", the deck name becomes `2026-06-08_ai-transformation-governance`
- The `[topic-slug]` is derived from the key theme — lowercase, hyphens instead of spaces, max 5-6 words

### Executive summary slide (MANDATORY — slide 1 in every deck)

Every deck MUST have an executive summary as slide 1 (after the cover page), regardless of framework. This slide synthesizes the entire deck's argument into one page: the core recommendation or insight, 2-3 supporting points, and the key ask or implication. The framework's narrative structure begins at slide 2.

Use `scr_dark_callout` or `factoid_grid` rendering for the executive summary.

**Executive summary density rules:**
- **density_preference: 0.80** — Executive summaries with <4 visible content blocks require enhancement
- Prefer mixed-modality synthesis (e.g., KPI strip + mini chart/table + action bullets) over text-only columns
- 3-column text bullets are a sparse-use fallback: allow only when dense and metric-backed, and paired with a callout or quantitative visual
- If 12+ data points available, upgrade to `executive_dashboard_4zone`
- **Always include a callout** — if using `scr_dark_callout`, the dark panel must contain a stat or key text (empty callout panels are forbidden)

### Spine construction

Apply the selected framework's spine template to the user's content:
1. **Slide 0 is always the cover page** (see rule above)
2. **Slide 1 is always the executive summary** (see rule above)
3. Map content to framework positions (which content goes to which slide, starting at slide 2)
4. Draft message-driven titles for each slide
5. Assign layouts to each slide
6. **Run density check** (see below)
7. Validate the spine (see Spine validation below)

### Density Check (MANDATORY — internal, run after layout assignment)

After assigning layouts, run this density audit internally before presenting the dot-dash to the user. Do NOT display audit results unless a major change is made.

**Step 1: Count data points per slide**

For each slide, count:
- Bullet points (each = 1 data point)
- Table cells with substantive data (each = 1 data point)
- Metrics/KPIs (each = 1 data point)
- Chart data series (each = 1 data point)

**Step 2: Apply density rules**

| Data Point Count | Classification | Action |
|------------------|----------------|--------|
| <4 data points | **SPARSE** | Flag for enhancement — add implications bar, callout stat, or expand to sub-bullets |
| 4-11 data points | **NORMAL** | Proceed with selected archetype |
| 12+ data points | **DENSE** | Prefer zone layouts (`zone_layout`, `executive_dashboard_4zone`) or dense presets |

**Step 3: Estimate fill ratio**

- Working area: ~85% of slide (excluding title, margins, source line)
- Content area: estimated sum of content block heights
- Fill ratio = Content area / Working area

| Fill Ratio | Assessment | Action |
|------------|------------|--------|
| ≥90% | **Optimal** | Proceed |
| 75-89% | **Acceptable** | Consider adding implications bar |
| 65-74% | **Sparse warning** | Add content: callout stat, evidence row, expanded bullets |
| <65% | **Critical** | Change archetype or add substantial content |

**Step 4: Check layout repetition (deck-level)**

- No archetype should appear 3+ times consecutively in the deck
- **No identical visual patterns on consecutive slides** — if two slides look the same, change one
- If pattern detected, swap middle instance to a within-family alternative
- Example: `columns` → `columns` → `columns` becomes `columns` → `stacked_rows` → `columns`

**Step 5: Check for duplicate column-with-icons patterns**

When multiple slides use the same "N columns with icons" pattern, convert alternates to split layouts:

| Pattern Detected | Action |
|------------------|--------|
| 2 slides with "3 columns + icons" | Convert 2nd slide to `zone_3_T` or `zone_3_L` (chart/table + actions mix preferred) |
| 2 slides with "2 columns + icons" | Convert 2nd slide to `1_2_dark_light` (one column per panel) |
| 3+ slides with "columns + icons" | Keep at most one column-led slide; convert others to zone or chart-with-breakdown |

**1/4 dark split conversion for column layouts:**

When converting a column layout to `1_4_dark`, place the columns ON the dark panel:

```
BEFORE (plain 3-column with icons):
┌─────────────────────────────────────────────────────┐
│  △ Header 1    ○ Header 2    □ Header 3             │
│  • Bullet 1    • Bullet 1    • Bullet 1             │
│  • Bullet 2    • Bullet 2    • Bullet 2             │
│                                                     │
│                    [whitespace]                     │
└─────────────────────────────────────────────────────┘

AFTER (1/4 dark split with columns on dark):
┌────────────┬────────────────────────────────────────┐
│ ███████████│                                        │
│ ███ Key    │  △ Header 1    ○ Header 2    □ Header 3│
│ ███ insight│  • Bullet 1    • Bullet 1    • Bullet 1│
│ ███ or     │  • Bullet 2    • Bullet 2    • Bullet 2│
│ ███ stat   │  • Bullet 3    • Bullet 3    • Bullet 3│
│ ███████████│                                        │
└────────────┴────────────────────────────────────────┘
(Left 1/4 panel in dark navy with key stat/message; right 3/4 has the columns)
```

Alternative: Place columns ON the dark panel (inverted):

```
┌────────────────────────────────────────┬────────────┐
│ ███████████████████████████████████████│            │
│ ███ △ Header 1  ○ Header 2  □ Header 3 │ Key        │
│ ███ • Bullet    • Bullet    • Bullet   │ takeaway   │
│ ███ • Bullet    • Bullet    • Bullet   │ or         │
│ ███████████████████████████████████████│ implication│
└────────────────────────────────────────┴────────────┘
(Left 3/4 dark panel with white text columns; right 1/4 light with callout)
```

**EXAMPLE: Same content, different split layouts for visual variety**

When you have multiple slides with similar 3-column content, use different split ratios to differentiate:

```
SLIDE 3 — "Market and competitive context" (plain white, 3-col + icons):
┌─────────────────────────────────────────────────────┐
│  📊 Market       ⚠️ Governance    ⏰ Hyperscaler    │
│  momentum        bottleneck       threat            │
│  • $5.25B→$199B  • 80% risky      • 18 mo window   │
│  • 46.2% CAGR    • Only 20%       • 24 mo threat   │
│  • 79% deploying • #1 blocker     • Build now      │
└─────────────────────────────────────────────────────┘

SLIDE 4 — "Three decisions" (1/4 dark split, 3-col on light):
┌────────────┬────────────────────────────────────────┐
│ ███████████│  🎯 Positioning  💡 Adoption   🔧 Build │
│ ███ Three  │  • Horizontal    • Autonomous  • Custom │
│ ███ inter- │    vs vertical     vs augment    vs buy │
│ ███ linked │  • ROI justifies • Unit econ   • Beats  │
│ ███ choices│    premium         differ        OSS    │
│ ███████████│                                        │
└────────────┴────────────────────────────────────────┘

SLIDE 5 — "Five recommendations" (3/4 dark split, cols on dark):
┌────────────────────────────────────────┬────────────┐
│ ███ 🎯 Rec 1    💡 Rec 2    🔧 Rec 3  │ The 5 recs │
│ ███ • Detail   • Detail    • Detail   │ form one   │
│ ███ • Detail   • Detail    • Detail   │ coherent   │
│ ███████████████████████████████████████│ system     │
│ ███      🚀 Rec 4         📈 Rec 5    │            │
│ ███      • Detail         • Detail    │            │
└────────────────────────────────────────┴────────────┘

SLIDE 6 — "Implementation" (2/3 dark split, timeline on dark):
┌──────────────────────────────────┬──────────────────┐
│ ███ Phase 1    Phase 2   Phase 3 │ Key milestones:  │
│ ███ 0-6 mo     6-12 mo   12-24mo │ • Month 3: MVP   │
│ ███ • Build    • Scale   • Lead  │ • Month 9: 5 cust│
│ ███ • Test     • Expand  • Defend│ • Month 18: $8M  │
│ ███████████████████████████████████│                │
└──────────────────────────────────┴──────────────────┘
```

**If columns are unavoidable, use this limited rotation (sparse-use):**

| Slide | Split Layout | Visual Effect |
|-------|--------------|---------------|
| 1st columns slide | `1_4_dark` or `3_4_dark` | Columns + strong callout (no plain white columns) |
| 2nd columns slide | `zone_3_T` or `chart_with_breakdown` | Shift to mixed-modality structure |
| 3rd+ columns slide | `zone_3_L` / `zone_4_dashboard` | Convert to zone layout instead of columns |

**Key principle: No two consecutive slides should have the same visual structure.**

**Auto-enhancement rules** (apply silently, surface only if major archetype change):

| Condition | Enhancement |
|-----------|-------------|
| <65% fill + bulleted content | Add implications bar below bullets |
| <65% fill + metrics | Add callout stat panel (use `3_4_dark` template) |
| <65% fill + table | Add source row + key takeaway callout |
| Single stat slide | Convert to `3_4_dark` with supporting context in main area |
| 12+ data points + flat layout | Upgrade to `zone_layout` or `executive_dashboard_4zone` |
| 3+ consecutive same archetype | Swap middle instance to within-family alternative |

### Aggressive Layout Densification (MANDATORY for decks with 5+ slides)

For decks with 5+ content slides, apply these aggressive rules to ensure visual variety and density:

**Zone Creativity Policy (MANDATORY):**
1. Prefer heterogeneous zones (chart + table + action bullets/callout) over text-only zones
2. Treat zone layouts as composition canvases: combine chart/table/status/actions in one slide when it improves decision clarity
3. Visually alternate across adjacent slides (zone, split, table/chart) to avoid repeated text-column patterns
4. For decks with 6+ slides, target at least 2 chart-bearing slides when trend/comparison/distribution cues exist
5. If chart data is partial, use proxy quantitative visuals (progress bars, dot matrix, mini trend, status heat row) instead of pure bullets

**Zone Layout Forcing Rules:**
| Slide Position | Minimum Layout Complexity |
|----------------|---------------------------|
| Slide 1 (exec summary) | `scr_dark_callout` or `executive_dashboard_4zone` — NEVER basic bullets |
| Slides 2-3 (situation/complication) | At least one must use `zone_2_*` or split layout with dark panel |
| Slides 4-6 (resolution/detail) | At least one must use `zone_3_*` or `zone_4_*` layout |
| Slides 7+ (implementation/detail) | Rotate through split templates: `3_4_dark`, `2_3_dark`, `1_2_dark` |

**Mandatory Split Template Usage:**
- **Every deck with 7+ slides MUST use at least 2 dark-panel split layouts** (`*_dark` templates)
- **Every deck with 10+ slides MUST use at least 1 zone layout** (`zone_3_*` or `zone_4_*`)
- **Executive/board decks MUST use `executive_dashboard_4zone` for slide 1**

**Deck-level Variety Targets (flexible, creativity-first):**
- **6-10 slide decks:** target >=2 chart-bearing slides (chart-in-zone or chart-in-split) when storyline cues support it
- **Text-heavy limit:** no more than 2 consecutive text-heavy slides; break the run with a chart, encoded table, or proxy quantitative visual
- **Data-limited exception:** if source data prevents charting, document the missing fields internally and switch to proxy visuals instead of reverting to plain bullets

**Chart Trigger Heuristics (prefer chart-in-zone when signals exist):**
| Signal in content | Preferred visual | Preferred layout pairing | If data is partial |
|-------------------|------------------|--------------------------|--------------------|
| Time / trend / phases | `line_chart` or mini trend | `zone_3_T`, `zone_2_vertical`, or `chart_with_breakdown` | Use mini trend with directional labels + assumptions note |
| Option comparison (3+ options) | `bar_chart` or ranked bars | `zone_2_horizontal`, `zone_3_L`, or split + comparison table | Use progress rows or ranked dot matrix |
| Distribution / mix | `stacked_bar` or composition bars | `zone_3_T` or `zone_4_dashboard` | Use segmented progress bars by category |
| Status / maturity / risk levels | status bars, heat row, or dot matrix | `zone_4_dashboard` or `multi_dimension_assessment` | Use traffic-light rows with qualitative scale anchors |
| Process / operating model flow | `building_block_column` or `timeline_chevron` | `zone_3_L` or `2_3_dark + timeline` | Use numbered stages with progress bars |
| Cause-effect / driver tree logic | `dual_panel_cause_effect` | `zone_2_horizontal` or `1_2_comparison` | Use directional arrows + weighted labels |
| Capability map / strategic system view | `tom_layout` or `north_star_layout` | `zone_4_asymmetric` or `zone_4_quad` | Use layered blocks with maturity/status tags |

**Creative Expansion Pass (MANDATORY — avoid archetype lock-in):**
After selecting the first-fit layout, run one extra creativity pass:
1. Generate 2 alternate layout concepts from DIFFERENT families (chart-led, diagram-led, zone-led, split-led)
2. Prefer the richest concept that preserves source fidelity and improves scanability
3. If two concepts are equivalent, pick the one with stronger visual encoding (chart/diagram > pure bullets)
4. Do not invent unsupported renderer functions; compose creatively using existing archetypes and zone geometries

**Conceptual Diagram Allowance (controlled creativity):**
- In decks with 6+ slides, allow up to 1 conceptual diagram-led slide by default (2 max only if content strongly benefits)
- Candidate concepts: org chart, architecture/system map, north-star model, process flow, bubble relationship map, impact-effort matrix, multi-chart control tower
- Conceptual slides must remain evidence-linked (metrics, assumptions, owners, or implications), not abstract art
- For MCP output, map conceptual intent to supported archetypes/templates (e.g., `tom_layout`, `north_star_layout`, `dual_panel_cause_effect`, `dimension_coded_matrix`, zone layouts)
- For `mck_renderer` code path, custom conceptual composition is allowed using supported primitives without inventing unsupported functions

**Column Content Density Rules:**

When using column layouts (2-4 columns), ensure adequate content density:

| Column Count | Minimum Content Per Column | If Too Sparse |
|--------------|---------------------------|---------------|
| 2 columns | 3+ bullets OR 1 bullet + 2 sub-bullets | Add sub-bullets, metrics, or use zone layout instead |
| 3 columns | 2+ bullets each OR 1 bullet + metric | Add supporting detail, implications, or icons with descriptions |
| 4 columns | 1-2 bullets each + icon/header | OK for icon-led pillars, but add subtitle row below |

**Anti-sparse column patterns:**

```
❌ BAD — Thin 3-column executive summary:
| Finance-ops domain expertise | Governance-first architecture | Autonomous-first economics |
| • 171-192% ROI | • Closes the 79% gap | • 171-192% ROI vs. 50-100% |

✅ GOOD — Dense 3-column with sub-bullets and metrics:
| Finance-ops domain expertise | Governance-first architecture | Autonomous-first economics |
| • 171-192% ROI with 6-8 mo payback | • Closes the 79% gap in enterprise governance | • 171-192% ROI vs. 50-100% for augmentation |
| • $50-150K ACV vs $10-30K | • Hybrid LangChain 80/20 build | • Scope cascade to multi-agent |
| • 5-10 customer proof points | • Speed/defensibility tradeoff optimized | • Lower velocity but higher defensibility |
```

If columns have only 1 bullet each, the slide is too sparse. Either:
1. Expand bullets to include supporting detail (metrics, examples, implications)
2. Add a sub-bullet row below each main point
3. Switch to `zone_layout` or `stacked_rows` for better density
4. Add an implications bar or callout stat panel below the columns

**Two-Column Rule: ALWAYS use split layout**

When content has exactly 2 parallel sections/columns, ALWAYS use a `1_2_*` split layout instead of plain columns:

| Content Pattern | Use This Split Layout |
|-----------------|----------------------|
| Two contrasting concepts (moat vs economics) | `1_2_dark_light` — dark panel for anchor concept |
| Two parallel workstreams | `1_2_split` with icons |
| Before/after or current/future | `1_2_split + before_after` |
| Problem/solution | `1_2_dark_light` — dark for problem, light for solution |
| Two options being compared | `1_2_navy_accent` — navy for recommended option |
| Internal/external view | `1_2_split + internal_external` |

**NEVER use plain `columns` for 2-column content.** Split layouts provide:
- Visual separation between the two concepts
- Dark panel emphasis for the more important side
- Professional McKinsey aesthetic
- Better density utilization

```
❌ BAD — Plain 2-column layout:
| Governance as moat | Autonomous-first economics |
| • 79% lack governance | • 171-192% ROI |
| • 20-30% price premium | • $50-150K ACV |

✅ GOOD — 1/2 split layout with dark panel:
┌─────────────────────────┬─────────────────────────┐
│ ███ Governance as moat  │ Autonomous-first econ   │
│ ███ • 79% lack govnce   │ • 171-192% ROI          │
│ ███ • 20-30% premium    │ • $50-150K ACV          │
│ ███ • 18-24 mo window   │ • Scope cascade         │
│ ███ • Four layers       │ • 30%+ orchestration    │
└─────────────────────────┴─────────────────────────┘
(Left panel in dark navy, right panel in white — or vice versa based on emphasis)
```

**Anti-Basic Layout Rules (flag and upgrade):**

These basic layouts should be flagged and upgraded when dense alternatives exist:

| Basic Layout | Problem | Upgrade To |
|--------------|---------|------------|
| `columns` (plain 2 cols) | No visual hierarchy, misses split opportunity | `1_2_dark_light` or `1_2_split` — ALWAYS |
| `columns` (plain 3 cols, text-only) | Often hides quantitative comparison and becomes repetitive | `zone_3_T`, `zone_3_L`, `2_3_dark + sidebar`, or `chart_with_breakdown`; keep only as sparse-use fallback when dense metric-backed + callout |
| `stacked_rows` (plain) | Wastes horizontal space | `zone_3_L` or `3_4_dark + numbered_list` |
| `table` (plain, no encoding) | Missed visual hierarchy | `grouped_table + traffic_lights` or `dimension_coded_matrix` |
| `bullets` (any plain list) | Low density, unprofessional | `stacked_rows + icons` or `grid + category_colors` |
| `factoids` (2-3 big numbers) | Wastes working area | `zone_4_dashboard` or `3_4_dark + metrics_row` |
| `timeline` (basic chevron) | Underutilizes space | `gantt_chart + milestones` or `zone_3_T + timeline_header` |

### TABLE ENCODING RULES (CRITICAL — no plain tables allowed)

**PLAIN TABLES ARE FORBIDDEN.** Every table must have visual encoding. If a table has no encoding, it fails quality review.

**Automatic encoding triggers:**

| Column Content | Required Encoding | How to Apply |
|----------------|-------------------|--------------|
| HIGH / MEDIUM / LOW | `traffic_lights` | Red dot for HIGH, amber for MEDIUM, green for LOW |
| Status (On track, At risk, Blocked) | `traffic_lights` | Green/amber/red dots or bars |
| Likelihood / Probability | `traffic_lights` | High=red, Medium=amber, Low=green |
| Impact / Severity | `traffic_lights` | High=red, Medium=amber, Low=green |
| Yes / No / Partial | `checkboxes` or `traffic_lights` | Check/X/partial or green/red/amber |
| Scores (1-5, A-F, percentages) | `dimension_bars` or `harvey_balls` | Filled proportionally |
| Categories (Finance, Tech, Ops) | `category_bars` | Color-coded by category |
| Comparison (Option A vs B vs C) | `category_bars` + `traffic_lights` | Category colors + favorability encoding |
| Timeline phases | `phase_colors` | Distinct color per phase |
| Priority (P1, P2, P3) | `numbered_bars` + `traffic_lights` | Priority number with urgency color |

**Table encoding validation (MANDATORY before presenting content):**

For EVERY table in the deck:
1. Scan columns for encoding triggers above
2. If ANY trigger matches → ADD the encoding
3. If NO trigger matches → Consider if the table should be a table at all (maybe use stacked_rows or columns instead)

**Examples of encoding application:**

```
❌ BAD — Plain table with no encoding:
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hyperscaler entry | Medium | HIGH | Accelerate acquisition |
| Poor implementation | Medium | HIGH | Validate playbook |

✅ GOOD — Same table with traffic_lights encoding:
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hyperscaler entry | 🟡 Medium | 🔴 HIGH | Accelerate acquisition |
| Poor implementation | 🟡 Medium | 🔴 HIGH | Validate playbook |

(In rendered output: colored dots replace emoji, consistent with McKinsey encoding standards)
```

```
❌ BAD — Comparison table with no encoding:
| Channel | CAC | Payback | LTV:CAC | Scalability |
|---------|-----|---------|---------|-------------|
| Direct only | $40-60K | 12-16 mo | 3.5-4.5x | Limited |
| Partner only | $5-10K | 6-9 mo | 2.5-3x | High |
| Hybrid | $20-35K | 8-12 mo | 3-3.5x | High |

✅ GOOD — Same table with category_bars + favorability encoding:
| Channel | CAC | Payback | LTV:CAC | Scalability |
|---------|-----|---------|---------|-------------|
| 🔵 Direct only | $40-60K ⬇️ | 12-16 mo ⬇️ | 3.5-4.5x ⬆️ | Limited ⬇️ |
| 🟢 Partner only | $5-10K ⬆️ | 6-9 mo ⬆️ | 2.5-3x ➡️ | High ⬆️ |
| 🟣 Hybrid (rec) | $20-35K ➡️ | 8-12 mo ➡️ | 3-3.5x ➡️ | High ⬆️ |

(Color bars for channel categories, arrows for favorability in each metric)
```

**If a table has 4+ rows and 3+ columns, it MUST have encoding.** No exceptions.

### TABLE VARIETY RULES (no duplicate table styles in a deck)

**Each table in a deck must look visually distinct.** If multiple slides have tables, vary the style:

| Table # in Deck | Required Style Variation |
|-----------------|-------------------------|
| 1st table | `grouped_table + traffic_lights` OR `comparison_table + category_bars` |
| 2nd table | Different encoding: `grouped_table + icons` OR `dimension_coded_matrix` |
| 3rd table | Different structure: `split_table_takeaways` OR `table + implications_row` |
| 4th+ table | Consider converting to `stacked_rows`, `zone_layout`, or visual (chart/diagram) |

**Table style rotation options:**

| Style | Visual Appearance | Best For |
|-------|-------------------|----------|
| `grouped_table + traffic_lights` | Colored dots in status columns | Risk, status, assessment |
| `grouped_table + icons` | Row icons in first column (circled, dark blue background) | Options, approaches, categories |
| `grouped_table + category_bars` | Colored vertical bars by row category | Comparison of options |
| `dimension_coded_matrix` | Multi-color cells by dimension | Capability assessment, scoring |
| `split_table_takeaways` | Table with callout/implications panel | Analysis with key insight |
| `comparison_table + highlight` | Recommended row highlighted | Option selection |

**NEVER have 2+ tables with identical styling in the same deck.**

**Table-to-Visual Conversion Rule (MANDATORY when multiple tables are needed):**
- If a slide would contain 2+ tabular blocks, keep at most one full-detail table and convert the other tabular block to a chart/proxy visual
- Prefer chart + table combinations inside zone layouts (not table + table)
- If two consecutive slides are table-heavy, convert at least one to a chart-led zone or `chart_with_breakdown`
- Exception: keep two tables only when exact-value traceability is required for both and cannot be summarized visually

| Tabular pattern | Convert one table to | Preferred zone composition |
|-----------------|----------------------|----------------------------|
| Option comparison table + metric table | `bar_chart` or ranked bars | `zone_3_T` (chart + compact reference table + implications) |
| Time-by-period table + details table | `line_chart` or mini trend | `zone_2_vertical` (trend top, detail table bottom) |
| Status matrix + risk table | heat row or dot matrix | `zone_4_dashboard` (status visual + action table + KPI strip) |
| Mix/share table + assumptions table | `stacked_bar` or segmented progress bars | `zone_3_L` (composition visual + assumptions panel) |

**Do not place two full-width tables on one slide** unless the exception above applies.

### ICON STYLING RULES (no plain line icons)

**Plain line icons are forbidden.** Icons must have visual treatment:

**Required icon styles (in order of preference):**

| Style | Description | When to Use |
|-------|-------------|-------------|
| `circled_dark_blue` | Icon in dark navy (#003A5D) filled circle | **DEFAULT — use this most often** |
| `circled_category_color` | Icon in category-colored filled circle | When icons represent different categories |
| `squared_dark_blue` | Icon in dark navy rounded square | Technical/architectural content |
| `outlined_thick` | Thick outline icon (no fill) | Secondary emphasis only |

**NEVER use plain thin line icons.** They look unprofessional and lack visual weight.

```
❌ BAD — Plain line icons:
△  Governance        ◯  Economics        □  Technology

✅ GOOD — Icons with dark blue circular background:
⬤△  Governance      ⬤◯  Economics      ⬤□  Technology
(Dark navy filled circle behind each icon)
```

**Icon styling in tables:**

When a table has an icon column (e.g., first column with row icons):
- Each icon MUST have a filled circular background
- Use `circled_dark_blue` for all icons (consistent)
- OR use `circled_category_color` if rows represent different categories

```
❌ BAD — Table with plain icons:
| Approach | Speed | Defensibility |
| △ Full custom | 18-24 mo | High |
| ◯ LangChain | 3-6 mo | Low |
| □ Hybrid | 6-8 mo | Medium |

✅ GOOD — Table with circled dark blue icons:
| Approach | Speed | Defensibility |
| ⬤△ Full custom | 18-24 mo | High |
| ⬤◯ LangChain | 3-6 mo | Low |
| ⬤□ Hybrid (rec) | 6-8 mo | Medium |
(Each icon has dark navy circular background)
```

**Icon + color combinations in column layouts:**

When using columns with icons as headers:
- Icons MUST have `circled_dark_blue` background
- Icon should be white/light on the dark background
- Icon size: 32-40px diameter circle
- Consistent sizing across all icons in the layout

**Content-to-Layout Mapping (use this table for layout selection):**

| Content Type | Data Points | Recommended Layout | Template |
|--------------|-------------|-------------------|----------|
| **Executive summary** | 4-8 | `scr_dark_callout` | `3_4_dark` |
| **Executive summary** | 9+ | `executive_dashboard_4zone` | `default` |
| **Market context / situation** | 4-6 | `factoid_grid + context_row` | `default_dark` |
| **Market context / situation** | 7+ | `zone_2_vertical` (stats top, detail bottom) | `default` |
| **Strategic options / comparison** | 2-3 options | `1_2_dark_light` or `zone_2_horizontal` | `1_2_split` |
| **Strategic options / comparison** | 4+ options | `dimension_coded_matrix` | `default` |
| **Recommendations (numbered)** | 3-5 items | `stacked_rows + numbered_bars` | `2_3_dark` |
| **Recommendations (numbered)** | 6+ items | `zone_3_L` (list left, detail right) | `default` |
| **ROI / financial analysis** | Any | `zone_3_T` (metrics header + table + implications) | `3_4_dark` |
| **Architecture / technical** | 4-6 components | `zone_3_L` (architecture map + dependencies + implications) | `2_3_dark` |
| **Architecture / technical** | 7+ components | `zone_4_quad` or `building_block_column` | `default` |
| **Roadmap / timeline** | 3-4 phases | `timeline_chevron + milestones` | `default` |
| **Roadmap / timeline** | 5+ phases | `gantt_chart` or `zone_3_inverted_T` | `default` |
| **Risk / issues** | 3-5 items | `grouped_table + traffic_lights` | `3_4_dark` |
| **Risk / issues** | 6+ items | `multi_dimension_assessment` | `default` |
| **Unit economics / metrics** | 4-6 KPIs | `factoid_grid` | `default_dark` |
| **Unit economics / metrics** | 7+ KPIs | `zone_4_dashboard` | `default` |
| **Go-to-market / channel** | Any | `comparison_table` or `zone_2_horizontal` | `2_3_dark` |
| **Defensibility / moat** | Any | `zone_3_L` (moat left, evidence right) | `3_4_dark` |
| **Trend over time** | 3+ periods | `line_chart + takeaway panel` | `zone_3_T` |
| **Cross-option comparison** | 3+ options, 2+ metrics | `bar_chart + comparison_table` | `chart_with_breakdown` |
| **Distribution / composition** | Any | `stacked_bar + key implications` | `zone_3_T` |
| **Program status dashboard** | Any | `status_dashboard` (status table + trend + actions) | `zone_4_dashboard` |
| **Operating model / org design** | Any | `tom_layout` or `north_star_layout` with evidence callouts | `default` |
| **Architecture / system interaction** | Any | `north_star_layout` or `zone_4_asymmetric` (components + interfaces) | `2_3_dark` |
| **Prioritization (impact vs effort)** | 4+ initiatives | `dimension_coded_matrix` + action sidebar | `default` |

### Output format (MANDATORY)

Present the storyline in two parts: a storyline overview (bullet list) followed by the detailed dot-dash (McKinsey-style nested bullets), then STOP and wait. Present the dot-dash as clean, copy-pasteable text so the user can copy it to a notepad.

**Dot-dash format per content slide** (a true two-level McKinsey dot-dash — the title is the "dot", supporting detail are the "dashes"):
- **Slide title** — full sentence-form, message-driven, in **bold**. This is the "dot".
- 2–4 **key supporting points** as top-level bullets beneath the title (complete, specific — concrete numbers, not fragments).
- **Dashes** — under each key supporting point, add 2–4 indented sub-bullets ("dashes") of supporting evidence/detail, **but only where the point has real evidence to add**. Thin points that stand on their own stay a single line with no dashes — do not pad. This second level is what makes it a dot-**dash**; without it the output is just a flat bullet list.
- **Sources of insight** — always on its **own separate line** below all the points (never appended to the last bullet/dash), in *italics* so it reads as a visually distinct format from the dot-dash itself. Lists known sources, uploaded materials, interviews, analyses, or "source still needed". Leave a blank line between the last point/dash and the sources line so it does not merge into the last bullet.

Cover (slide 0), BACKUP, and appendix appear in the storyline overview as title-only entries; they do not need supporting points.

```
**"One thing"**: [Complete the sentence]

**Storyline overview:**
- Slide 0: [Cover page title]
- Slide 1: [Executive summary title]
- Slide 2: [Title]
- Slide 3: [Title]
- ...

**Dot dash:**

**[Slide 1 title — full sentence-form, message-driven]**
- [Key supporting point 1 — complete and specific]
  - [Dash: supporting evidence / detail]
  - [Dash: supporting evidence / detail]
- [Key supporting point 2 — thin point that stands alone; no dashes needed]
- [Key supporting point 3]
  - [Dash: supporting evidence / detail]

*Sources of insight: [known sources / uploaded materials / analyses — or "source still needed"]*

**[Slide 2 title]**
- [Key supporting point 1]
  - [Dash: supporting evidence / detail]
- [Key supporting point 2]

*Sources of insight: [...]*

[... per content slide: bold title (the "dot") → 2–4 key supporting points → 2–4 indented dashes beneath a point only where evidence warrants → blank line → italic sources line on its own line ...]

Approve the dot-dash, or adjust? (reorder, change titles, swap layouts, add/remove slides)
```

> **Layout is tracked internally, not shown in the dot-dash.** The agent still assigns a layout to every slide during spine construction (used downstream for rendering), and the user can still ask to swap layouts — it is simply not displayed in the user-facing dot-dash.

### Layout assignment (internal — not shown in the dot-dash)

The agent still assigns a layout to every slide during spine construction (needed downstream for rendering), using **plain-language descriptions** (max 5 words) that describe the visual structure. Examples:
- "Columns with icons"
- "Table with metrics"
- "Timeline with milestones"
- "Grid with categories"
- "Chart with callout"
- "Two-column comparison"
- "Stacked rows with numbers"
- "Dark callout panel"

Do NOT use technical archetype names or function names — keep it user-friendly. The layout is tracked internally and not displayed in the dot-dash; the user can still request layout swaps.

### Source tracing rule

The "Sources of insight" line maps each slide's content to the `##` and `###` headers from the user's original input document. This is a best-effort mapping based on where each data point, metric, or argument originated during STEP 1 substance extraction.

If the user's input has no clear section structure, use descriptive labels instead (e.g., "paragraph 3", "table on page 2", "bullet list after intro").

### User actions at this checkpoint

| User says | Agent does |
|-----------|-----------|
| "Approved" / "Looks good" / "Generate" | Draft content internally (Step 3), then proceed to Step 5 render consent — no separate content-preview approval |
| "Swap slides 3 and 4" / "Add a slide on X" | Adjust and re-present the dot-dash |
| "Change the title on slide 2 to ..." | Update and re-present the dot-dash |
| "Use a table instead of columns on slide 3" | Swap the (internal) layout and re-present the dot-dash |
| "Copy this" / "Can I share the dot-dash?" | The dot-dash is already plain text — the user can copy/paste it directly (file export not yet available) |
| "Generate only slides 1, 3, 5" / "Just these slides: ..." | Confirm selection, then proceed to Step 3 with selective rendering (see below) |
| "Skip the appendix, generate the rest" | Generate all slides except BACKUP and Appendix |
| "Just the first 5 slides" | Generate slides 1-5 only |

---

## SELECTIVE SLIDE RENDERING (optional — user-triggered)

User can request generation of only specific slides instead of the full deck. This is useful when:
- User provides their own storyline and only wants certain slides generated
- User reviewed the full spine proposal and wants to generate only a subset
- User wants to regenerate specific slides after edits

### Detect when

The user specifies a subset of slides to render. Examples:
- "Generate only slides 1, 3, and 5"
- "Just render the executive summary and recommendations slides"
- "Only these slides: Slide 2, Slide 4, Slide 7"
- "Skip slides 3 and 6, generate the rest"
- "I only need the first 3 slides"

### What to do

1. Parse the user's selection — extract slide numbers or titles
2. Confirm the selection back to the user:
   ```
   I'll generate content for these slides only:
   - Slide 1: [title from spine]
   - Slide 3: [title from spine]
   - Slide 5: [title from spine]
   
   Proceed? (y/n)
   ```
3. On confirmation, generate content ONLY for the selected slides
4. The output `.md` file contains ONLY the selected slides (not placeholders for skipped slides)

### What NOT to do

- Do NOT include placeholder entries for skipped slides
- Do NOT renumber the slides — preserve original slide numbers from the spine
- Do NOT add BACKUP/Appendix slides unless explicitly included in the selection
- Do NOT run rendering diversity audit for partial decks (may have intentional duplicates)

---

### Storyline spine validation (MANDATORY — internal, before presenting)

After drafting titles, read them in sequence top to bottom. They must form a coherent narrative — if you only read the titles, you understand the full argument.

**Anti-patterns to catch BEFORE presenting to user:**

1. **No duplicate claims** — No two titles should make the same assertion or start with the same subject+verb
2. **Each title adds new information** — If removing a title wouldn't leave a gap in the story, it's redundant
3. **Deep dives explain HOW/WHY/WHERE, not WHAT** — A frame declares the conclusion; its deep dives must explain mechanism, evidence, or a specific angle — never restate the conclusion with different numbers
4. **Consecutive titles vary in subject** — Three consecutive titles starting with the same subject is a spine failure
5. **Frame+Deep Dive title relationship** — When a frame says "B is best", good deep dives show trade-offs or evidence. Bad deep dives restate "B leads on N dimensions"
6. **No duplicate layouts across slides** — Ensure visual variety by varying layout types across the deck. A layout family CAN appear multiple times if each instance uses a different variant
7. **Avoid defaulting to 3-column text bullets** — use only when dense metric-backed and paired with callout/quant visual

**Deck-level creativity checks (6+ slides):**
- Target at least 2 chart-bearing slides when the storyline includes time/trend/comparison/distribution cues
- Allow no more than 2 consecutive text-heavy slides; break with a chart, encoded table, or proxy quantitative visual
- Keep 3-column text slides sparse: typically no more than 1 in 6-10 slide decks (and never on consecutive slides)
- If data is incomplete, request missing chart fields or use a proxy visual (progress bars, dot matrix, mini trend, status heat row) rather than pure bullets

### Within-family rendering menu (INTERNAL — for layout variety, not shown to user)

Use this menu internally to ensure visual variety when assigning layouts. Do NOT expose these technical names to the user — keep layouts as internal plain-language descriptions.

| Family | Rendering variants (each visually distinct — never use the same one twice in a deck) | Density notes |
|--------|--------------------------------------------------------------------------------------|---------------|
| **Table** | `flat_table` · `grouped_table + category_bars` · `grouped_table + traffic_lights` · `grouped_table + group_icons` · `dimension_coded_matrix` · `split_table_takeaways` | `grouped_table`: Add traffic lights/Harvey balls when status dimension exists (density: 0.80) |
| **Column/Flow** | `columns + icons` · `columns + highlighted_col` · `implications_columns + chevrons` · `scr_dark_callout` | `scr_dark_callout`: Always include callout stat or text — empty panels forbidden (density: 0.85) |
| **Grid/Row** | `grid + icons` · `grid + row_accent_colors` · `stacked_rows + icons` · `stacked_rows + numbered_bars` · `building_block_column` | Prefer `zone_layout` for 12+ data points (density: 1.0) |
| **Specialized** | `gantt_chart` · `timeline_chevron` · `factoid_grid` · `bar_chart` · `line_chart` · `dual_panel_cause_effect` · `tom_layout` · `north_star_layout` | `factoid_grid`: Combine with subtitle row or trend indicators (density: 0.85) |
| **3/4 splits (dark)** | `3_4_dark + stat_callout` · `3_4_dark + key_quote` · `3_4_dark + implications` · `3_4_dark + metrics_row` · `3_4_dark + numbered_list` · `3_4_navy + cta` | **PREFERRED for exec content** — 75/25 ratio with dark callout panel (density: 0.85) |
| **2/3 splits (dark)** | `2_3_dark + sidebar` · `2_3_dark + evidence` · `2_3_dark + kpis` · `2_3_dark + timeline` · `2_3_navy + summary` · `2_3_grey + notes` | 67/33 ratio — use dark for premium feel, grey only for caveats (density: 0.80) |
| **1/2 splits** | `1_2_dark_light` · `1_2_dark_dark` · `1_2_comparison` · `1_2_before_after` · `1_2_internal_external` · `1_2_navy_accent` | 50/50 ratio — ONLY for truly equal comparisons (density: 0.85) |
| **1/4 splits** | `1_4_dark + detail` · `1_4_navy + table` · `1_4_dark + list` | 25/75 ratio — callout introduces detailed content (density: 0.90) |
| **Zone layouts** | `zone_2_horizontal` · `zone_2_vertical` · `zone_3_T` · `zone_3_inverted_T` · `zone_3_L` · `zone_4_quad` · `zone_4_dashboard` · `zone_4_asymmetric` | **MANDATORY for 8+ data points**; use zones to group related content logically (density: 0.95) |
| **Dense presets** | `executive_dashboard_4zone` · `scr_with_evidence` · `multi_dimension_assessment` · `status_dashboard` · `chart_with_breakdown` | **MANDATORY for 12+ data points** or executive synthesis (density: 0.90-1.0) |

### Split Layout Variants (detailed guidance)

Split layouts create visual hierarchy by dividing the slide into distinct regions with contrasting backgrounds or emphasis. **Prefer dark navy templates (`*_dark`) over grey for executive content.**

#### 3/4 Split Layouts (75/25 ratio) — Primary + Callout

| Variant | Template | Use When | Main Panel (75%) | Accent Panel (25%) |
|---------|----------|----------|------------------|-------------------|
| `3_4_dark + stat_callout` | `3_4_dark` | Single key metric needs emphasis | Detailed explanation, evidence, context | Big stat (48pt+) with label |
| `3_4_dark + key_quote` | `3_4_dark` | Executive quote or key insight | Supporting analysis or evidence | Quote text with attribution |
| `3_4_dark + implications` | `3_4_dark` | Recommendation with "so what" | Main argument or evidence | Implications bar (2-3 bullets) |
| `3_4_dark + metrics_row` | `3_4_dark` | Data table with key takeaway | Table or detailed breakdown | 2-3 headline metrics stacked |
| `3_4_dark + numbered_list` | `3_4_dark` | Process with key count | Detailed steps or explanation | "5 key steps" or "3 priorities" |
| `3_4_navy + cta` | `3_4_navy` | Recommendation with clear ask | Supporting rationale | Call-to-action or decision ask |

#### 2/3 Split Layouts (67/33 ratio) — Primary + Supporting

| Variant | Template | Use When | Main Panel (67%) | Side Panel (33%) |
|---------|----------|----------|------------------|------------------|
| `2_3_dark + sidebar` | `2_3_dark` | Primary content + definitions | Main argument, table, or chart | Definitions, glossary, or legend |
| `2_3_dark + evidence` | `2_3_dark` | Claim that needs proof | Assertion or recommendation | Evidence table or metrics |
| `2_3_dark + kpis` | `2_3_dark` | Analysis with key metrics | Detailed analysis or table | 3-4 KPI callouts stacked |
| `2_3_dark + timeline` | `2_3_dark` | Content with phasing | Main content | Mini timeline or phase indicator |
| `2_3_navy + summary` | `2_3_navy` | Detail with executive takeaway | Detailed content | Executive summary bullets |
| `2_3_grey + notes` | `2_3_grey` | Content with caveats | Main content | Assumptions, notes, or sources |

#### 1/2 Split Layouts (50/50 ratio) — Balanced Comparison

| Variant | Template | Use When | Left Panel (50%) | Right Panel (50%) |
|---------|----------|----------|-----------------|------------------|
| `1_2_dark_light` | `1_2_split` | Problem → Solution | Dark: Challenge/risk | Light: Solution/opportunity |
| `1_2_dark_dark` | `1_2_dark` | Two equally weighted options | Option A (dark navy) | Option B (dark blue) |
| `1_2_comparison` | `1_2_split` | Side-by-side comparison | Current state / As-is | Future state / To-be |
| `1_2_before_after` | `1_2_split` | Transformation | Before | After |
| `1_2_internal_external` | `1_2_split` | Dual perspective | Internal view | External/market view |
| `1_2_navy_accent` | `1_2_navy` | Executive comparison | Primary option (navy) | Alternative (light) |

#### 1/4 Split Layouts (25/75 ratio) — Callout + Detail

| Variant | Template | Use When | Callout Panel (25%) | Main Panel (75%) |
|---------|----------|----------|---------------------|------------------|
| `1_4_dark + detail` | `1_4_dark` | Key stat introduces detail | Big stat or key message | Supporting evidence, table, breakdown |
| `1_4_navy + table` | `1_4_navy` | Metric headline + data | Headline KPI | Detailed data table |
| `1_4_dark + list` | `1_4_dark` | Count introduces items | "7 initiatives" callout | Detailed list of all 7 |

**Split layout selection rules:**
- **PREFER DARK TEMPLATES** (`*_dark`, `*_navy`) for executive and board content — grey feels less premium
- **3/4 dark**: When you have ONE key number, quote, or insight to emphasize
- **2/3 dark**: When supporting detail is substantial and needs visual separation
- **1/2 split**: ONLY for truly equal comparisons — if one side has 2x+ content, use 2/3 or 3/4
- **1/4 dark**: When a single metric or callout introduces detailed content
- **Navy vs dark blue**: Navy (`*_navy`) for highest-stakes executive slides; dark blue (`*_dark`) for standard emphasis

**Template color hierarchy (most to least premium):**
1. `*_navy` — Deep navy (#003A5D) — Board presentations, C-suite asks
2. `*_dark` — Dark blue (#0A2540) — Executive summaries, key recommendations  
3. `*_grey` — Grey (#63666A) — Supporting detail, secondary content
4. `default` — White — Standard content slides

### Zone Layout Patterns (detailed guidance)

Zone layouts divide the working area into distinct content regions for high-density slides with 8+ data points.

| Pattern | Zones | Layout Shape | Best For | Zone Sizes |
|---------|-------|--------------|----------|------------|
| `zone_2_horizontal` | 2 | `[A][B]` side by side | Two parallel workstreams, dual metrics | 50/50 or 60/40 |
| `zone_2_vertical` | 2 | `[A]` over `[B]` | Summary + detail, overview + breakdown | 40/60 or 30/70 |
| `zone_3_T` | 3 | `[A]` full width, `[B][C]` below | Governing insight + two supporting areas | 35% top, 65% bottom split |
| `zone_3_inverted_T` | 3 | `[A][B]` top, `[C]` full width | Two inputs → one conclusion | 65% top split, 35% bottom |
| `zone_3_L` | 3 | `[A]` tall left, `[B][C]` stacked right | Primary content + two supporting panels | 60% left, 40% right stacked |
| `zone_4_quad` | 4 | `[A][B]` / `[C][D]` grid | Four parallel dimensions or categories | 25% each, equal grid |
| `zone_4_dashboard` | 4 | `[KPIs]` top, `[A][B][C]` below | Executive dashboard with metrics header | 25% top, 75% bottom in thirds |
| `zone_4_asymmetric` | 4 | `[A]` large, `[B][C][D]` small | Primary focus + three supporting metrics | 50% primary, 3x ~17% supporting |

**Zone layout selection rules:**
- **8-11 data points**: Use 2-zone or 3-zone layouts
- **12+ data points**: Use 4-zone layouts or dense presets
- **Zones must be MECE**: Each zone covers a distinct dimension, no overlap
- **Visual hierarchy**: Larger zones = more important content
- **Reading order**: Top-left → top-right → bottom-left → bottom-right (Z-pattern)

**Mixed-modality default (creativity-first):**
- Prefer combining at least two modalities per zone slide: chart + table, chart + action bullets, or table + callout metrics
- Reserve text-only zone compositions for cases where quantitative encoding is not viable
- When repeating a zone family, vary both geometry and modality (e.g., chart-led `zone_3_T` followed by table-led `zone_4_asymmetric`)

**Zone content pairing guidelines:**
| Zone Position | Typical Content |
|---------------|-----------------|
| Top-left (primary) | Key message, main chart, or governing insight |
| Top-right | Supporting metric or secondary chart |
| Bottom-left | Evidence table or detail breakdown |
| Bottom-right | Implications, next steps, or callout |

**Rich zone compositions (preferred examples):**
| Pattern | Composition |
|---------|-------------|
| `zone_4_dashboard` | Workstream status table (left) + delivery velocity line chart (center) + key actions panel (right) + risk/status indicator row (bottom) |
| `zone_3_T` | Headline KPI strip (top) + comparison chart (bottom-left) + recommendation bullets (bottom-right) |
| `zone_3_L` | Primary trend chart (left) + supporting evidence table (top-right) + decision/next-step callout (bottom-right) |
| `zone_4_asymmetric` | Main insight visualization (large zone) + three support zones (assumptions, milestones, owner/actions) |

---

## STEP 3: Draft Slide Content (internal — no approval stop)

**After the spine (Checkpoint 2) is approved, draft the complete slide content internally, then proceed to render.** This step is NOT a user-facing checkpoint — do NOT present per-slide content cards and wait for approval. The dot-dash (Checkpoint 2) is the user's review point for structure; the single remaining stop is the Step 5 render consent.

Draft complete, MCP-ready content for every slide, write it to the slide-content markdown file, run the internal validations below, then continue to Step 4 (backup/appendix) and Step 5 (render consent). Report the saved file path to the user as a one-line status (not a stop).

### MCP-Ready Output Requirement (CRITICAL)

The output markdown file must be **fully self-contained** for downstream MCP rendering. The MCP server (`commspro`) has **NO access to**:
- The original source document
- Conversation context or memory
- Any external files or references

**Every slide must contain complete, render-ready content.** The MCP server will render exactly what is in the markdown file — nothing more, nothing less.

### What to do

For each slide in the spine, draft **COMPLETE** content — no fragments, no abbreviations, no references to external context:
- Title text — full message-driven title as it will appear on the slide
- Subtitle text — complete subtitle
- Governing thought text — the key insight in one full sentence
- Column headers + bullet points — complete sentences with all details, all metrics, all data
- Table headers + row data — every row, every column, every cell fully populated (NO truncation with "...")
- Implications bar text — full text for any callout or implications bar
- Timeline phases + content rows + milestones — all phases, all milestones, all dates
- Callout panel content — complete header, stat, and body text
- Source footnotes — complete citations

### Content Completeness Rules (MANDATORY)

1. **No fragments or abbreviations** — Write complete sentences with all details from the source
2. **Full tables** — Include every row and column; NEVER truncate with "..." or "etc."
3. **All metrics explicit** — Include exact numbers, percentages, currencies, dates (e.g., "€145-265M" not "significant investment")
4. **Complete explanations** — If a concept needs explaining, include the full explanation on the slide
5. **Self-contained context** — Each slide must make sense without reading other slides or the source document
6. **No external references** — Never write "as mentioned above", "see source", or "per the document"

### Anti-Over-Synthesis Rule (MANDATORY)

Do not over-compress source content into generic high-level bullets. Prefer dense, specific, decision-useful content:

1. Preserve mechanism + evidence + implication, not just conclusion statements
2. Replace abstract adjectives ("strong", "significant", "material") with concrete numbers and operational detail
3. If a slide looks plain or underfilled, add depth with evidence rows, mini-comparisons, assumptions blocks, or action owners
4. For pre-read / decision decks, default to richer content unless user explicitly asks for minimalist presenter slides

### Chart Trigger + Fallback Policy (MANDATORY)

When selecting per-slide `### Layout` and `### Encoding`:

1. **Trigger chart-in-zone/split** when content signals time, trend, comparison, or distribution
2. **If critical chart fields are missing**, ask the user for missing fields (period labels, category totals, baseline, denominator) before finalizing chart-heavy output
3. **If immediate generation is required with partial data**, use proxy quantitative visuals instead of text-only bullets:
   - Progress bars / progress rows
   - Dot matrix (relative magnitude)
   - Mini trend (directional only)
   - Status heat row / traffic-light matrix
4. Label proxy visuals as directional where applicable; never fabricate precise numbers

### Anti-patterns (DO NOT do this)

```
❌ BAD — Fragment with missing data:
"Key metrics improved significantly across all dimensions..."

✅ GOOD — Complete with all specifics:
"Operating margin improved from 8.1% to 12.3%; inventory turns increased 15%; 
repeat purchase rate rose from 21.6% to 26-28%; NPS improved from 21 to 32"

❌ BAD — Truncated table:
| Initiative | Investment |
|------------|------------|
| Demand forecasting | €50-80M |
| ... | ... |

✅ GOOD — Complete table with all rows:
| Initiative | Investment | Expected Outcome | Margin Impact |
|------------|------------|------------------|---------------|
| Demand forecasting | €50-80M TCO | <8% MAPE accuracy | 100-150 bps |
| Demand Intelligence Squad | €30-50M | AI replenishment in all stores by Month 18 | Enables above |
| CDP completion | €10-20M | Cross-brand identity resolution | Prerequisite for H2 |
| Customer service AI | €5-15M TCO | 50-60% first-contact resolution | 50 bps |

❌ BAD — Reference to external context:
"Similar approach as Phase 1" or "See executive summary for details"

✅ GOOD — Self-contained description:
"Phase 2 deploys shared AI infrastructure across COS, ARKET, and H&M core 
with strict brand governance. Investment: €185-325M. Target: 8-15% conversion 
lift from personalization, 35-60% reduction in per-brand technology cost."
```

### Output format (MANDATORY)

Generate a markdown file with this structure for each slide:

```markdown
---

## SLIDE [N]: [Full Message-Driven Title]

### Layout
Archetype: [archetype name — e.g., grouped_table, columns, factoid_grid, gantt_chart, scr_dark_callout]
Template: [template name — e.g., default, default_dark, 3_4_dark, 2_3_grey, 1_2_split]

### Encoding
[Encoding type — e.g., traffic_lights, category_bars, icons, numbered_bars, stat_callouts, dimension_coded_matrix, phase_colors]

### Title
[COMPLETE: Full title text as it will appear on the slide]

### Subtitle
[COMPLETE: Full subtitle text — omit section if no subtitle]

### Governing Thought
[COMPLETE: The key insight in one full sentence]

### [Column/Section Header 1]
- [COMPLETE: Full bullet point with all details, metrics, and context]
- [COMPLETE: Another full bullet point — no abbreviations]
- [COMPLETE: Continue for all items — never truncate]

### [Column/Section Header 2]
| Column A | Column B | Column C | Column D |
|----------|----------|----------|----------|
| [Full cell content] | [Full cell content] | [Full cell content] | [Full cell content] |
| [All rows included] | [No truncation] | [Complete data] | [Every value] |

### Implications / Callout
[COMPLETE: Full text for any callout, implications bar, or key takeaway]

### Source
[COMPLETE: Full source citation]

---
```

**Layout and Encoding are MANDATORY** — the consuming application (MCP server) needs this information to select the correct rendering archetype and visual encoding. Without `### Layout` and `### Encoding` sections, the slide cannot be rendered correctly.

### Text export option (SUPPORTED when user asks)

If the user asks to export the final slide proposal to a text file, create a UTF-8 `.txt` file containing the finalized proposal content.

**Default filename:**
- `./exports/[deck-slug]-slides-proposal.txt`
- If `./exports/` does not exist, create it

**Required content in the `.txt` export:**
1. Deck title, subtitle, date, and whether it is full or partial deck
2. For each included slide:
   - Slide number and title
   - Plain-language layout description
   - Governing thought
   - Key content blocks (bullets/tables/chart notes) with concrete numbers
   - Source section/citation
3. If selective rendering is active, include: `Partial deck: slides X, Y, Z of N`

After writing the file, report the exact path to the user and wait for next instruction.

### Partial deck output (when selective rendering is active)

When generating a subset of slides (per user request in Step 2):

1. Include a header indicating partial generation:
   ```markdown
   # [Presentation Title]
   ## [Presentation Subtitle]
   
   > **Partial deck**: Slides 1, 3, 5 of 12 total
   ```

2. Include ONLY the selected slides — no gaps, no placeholders for skipped slides
3. Preserve original slide numbers (e.g., "## SLIDE 3:" not "## SLIDE 2:") so the user can identify which slides these are from the spine
4. Run all validations internally — do not display audit results to user

### Pre-Output Validation (MANDATORY — internal, do NOT display to user)

Before proceeding to render, validate each slide internally. **Do NOT show audit tables or validation results to the user** — only surface errors if they are blocking issues that prevent generation.

**Internal checklist (run silently):**
- [ ] **Layout section present** — Has `### Layout` with Archetype and Template specified
- [ ] **Encoding section present** — Has `### Encoding` with visual encoding type specified
- [ ] Title is complete (not a fragment)
- [ ] All content sections are fully populated
- [ ] No placeholder text (`[TBD]`, `...`, `etc.`, `and more`)
- [ ] All tables have complete rows and columns (count them against source)
- [ ] All metrics are explicit numbers (no "significant", "substantial", "improved")
- [ ] No cross-references that assume external context
- [ ] Slide is self-sufficient — MCP can render without any additional input
- [ ] **Rendering diversity** — No two slides use the same layout variant (check against within-family menu)
- [ ] Chart trigger honored — trend/comparison/distribution/time cues use chart or justified proxy visual
- [ ] Deck variety target honored (6+ slides) — at least 2 chart-bearing slides, unless data-limited exception applies
- [ ] No more than 2 consecutive text-heavy slides
- [ ] 3-column text usage remains sparse and justified (dense metric-backed exception only)
- [ ] Multi-table handling honored — when 2+ tables are needed, at least one is converted to chart/proxy visual unless exact-value exception applies

**If any check fails:** Fix the content before proceeding to render. Do not render incomplete slides. Only notify the user if you cannot auto-fix the issue.

### After drafting (proceed automatically — no approval stop)

Once content is drafted, written to the slide-content markdown file, and passes the Pre-Output Validation:

1. Report the saved file path to the user as a one-line status (e.g., "Content drafted and saved to `<path>`."). Do NOT print the full per-slide content cards for approval and do NOT STOP.
2. Proceed directly to Step 4 (backup divider + appendix), then Step 5 (render consent).

**Audits run internally** — only surface errors to the user if validation fails (a blocking issue that prevents generation), in which case fix the content and continue.

**On-demand only:** If the user explicitly asks to see or edit the drafted content, or to export it (see "Text export option" above), honor that request — then continue to render. Absent such a request, do not pause here.

---

## STEP 4: Add Backup Divider and Appendix

**When generating a full deck (>= 3 slides), add TWO slides at the end:**

### Slide N-1: BACKUP section divider

A blank slide with only the title "Backup". No other content — this serves as a visual separator signaling that everything after it is supplementary material.

### Slide N: Appendix discussion questions

Contents:
1. **Left column — "Questions to clarify"**: Questions the consulting team would want to validate with the client. Group by theme:
   - Assumptions needing validation
   - Missing data points
   - Strategic choices where client preference is unknown
   - Scope and constraint confirmation

2. **Right column — "Anticipated audience questions"**: Questions the target audience is likely to ask:
   - ROI / financial impact
   - Risk and mitigation
   - Implementation feasibility
   - "Why not X?" challenges

**Title**: Message-driven (e.g., "Key questions to address before finalizing the strategy"), NOT "Appendix" or "Discussion".

**Rules:**
- 3-5 question groups per column (2-4 questions each)
- Questions must be specific to the content, NOT generic boilerplate

---

## STEP 5: CHECKPOINT 4 — Render to PowerPoint via CommsPro

**PREREQUISITE CHECK (MANDATORY before ANY MCP call):**
Before calling ANY MCP tool (`create_slide_deck`, `get_slide_deck_status`), verify ALL of the following have occurred in this conversation:
- [ ] Checkpoint 0 (Context Foundation) was presented AND user confirmed
- [ ] Checkpoint 1 (Narrative Selection) was presented AND user selected variant A, B, or C
- [ ] Post-selection prompt was presented AND user chose "Generate" or "Review"
- [ ] Slide content was drafted (Step 3) and passed the Pre-Output Validation

**If ANY checkbox is unchecked: DO NOT call MCP tools. Go back to the first missing checkpoint.**

**Fast-track exception:** If the user explicitly opted into fast-track (see "FAST-TRACK EXCEPTION"), these interactive checkpoints are intentionally skipped and this prerequisite is considered satisfied — proceed, having run all INTERNAL validations.

After the spine is approved (Step 2) and the content has been drafted and validated (Steps 3 + 4), offer to render the deck as PowerPoint files via the `commspro` MCP server.

This step has external side effects (creates jobs on CommsPro, writes files to the user's working directory, runs `mkdir`/`curl` via the Bash tool). **STOP and get explicit user consent before doing anything in this step — unless the user explicitly opted into fast-track (see "FAST-TRACK EXCEPTION"), in which case the opt-in already serves as render consent and no separate consent stop is required.**

### Render mode selection

| Scenario | Mode | What happens |
|----------|------|--------------|
| Full deck or partial deck (any number of slides) | **Parallel-deck** (default) | One MCP job → each slide rendered by its own agent in parallel → merged into one assembled `.pptx` |
| Retry a single failed slide | **Per-slide** (legacy) | One MCP job → one single-slide `.pptx` |

**Default to parallel-deck mode.** Per-slide mode is only for retrying individual failed slides after the deck has been generated.

### Pre-Render Validation (MANDATORY before MCP submission)

Before presenting the consent prompt, validate that the slide content is MCP-ready. The MCP server has NO access to conversation context, source documents, or memory.

**Completeness Checklist — verify each slide:**
- [ ] Has complete Title (not a fragment or placeholder)
- [ ] Has complete Subtitle (if applicable)
- [ ] All content sections are fully populated with complete text
- [ ] No placeholder text remains (`[TBD]`, `...`, `etc.`, `[to be added]`)
- [ ] All tables have complete rows and columns (no truncation)
- [ ] All metrics are explicit numbers (not "significant increase" but "42% increase")
- [ ] No cross-slide references that assume shared context ("as above", "see slide 2")
- [ ] No references to source document ("per the document", "from the analysis")
- [ ] Each slide is self-sufficient — MCP can render it in isolation

**If validation fails:** Return to Step 3 and expand incomplete slides before proceeding. Do NOT submit incomplete content to the MCP server.

**Validation failure examples:**
```
❌ FAILS: "Investment of €X million" — placeholder
❌ FAILS: "Key initiatives include..." followed by "..." — truncated
❌ FAILS: "See executive summary for full context" — external reference
❌ FAILS: "Margin improvement (details in source)" — requires external document
❌ FAILS: Table with 3 rows when source has 7 rows — incomplete data

✓ PASSES: "Investment of €145-265M across 5 initiatives"
✓ PASSES: Complete table with all rows from source document
✓ PASSES: Full explanation without references to other content
```

### Consent prompt (MANDATORY before any tool call in this step)

```
Ready to render this <N>-slide deck via CommsPro?

I will:
1. Submit ONE coordinated render job to the `commspro` MCP server (your McKinsey ID
   token is forwarded automatically; nothing extra to install).
2. Poll the job until it completes (typically 2-5 minutes for a full deck).
3. Download the assembled .pptx + per-slide thumbnails into ./commspro/<deck-slug>/
   in your current working directory.

Proceed? (y / n / change deck name)
```

If the user declines, stop. Do not call MCP or Bash. If the user wants a different deck name, take it and re-render the consent prompt.

### Inputs needed (resolve before tool calls)

| Variable | Source | Example |
|----------|--------|---------|
| `<deck name>` | Format: `YYYY-MM-DD_[topic-slug]` where topic-slug is derived from the storyline's governing thought (the "one thing") | `2026-06-08_ai-transformation-governance` |
| `<deck-slug>` | Same as `<deck name>` — already in the correct format | `2026-06-08_ai-transformation-governance` |
| `<job_id>` | Returned by MCP after job creation | `a0cdb013-0cf1-4f6d-a6e7-9c0bf1ca95d6` |

**Deck naming rules:**
- Always prefix with current date: `YYYY-MM-DD_`
- Topic slug: lowercase, hyphens instead of spaces, max 5-6 words
- Derived from the governing thought / "one thing" — NOT from user-provided arbitrary titles
- Example: "One thing" = "Margin compression is structural — governance before technology" → `2026-06-08_margin-compression-governance-first`

### Folder layout

Files go into the consultant's working directory:

```
./commspro/
  2026-06-08_ai-transformation-governance/
    2026-06-08_ai-transformation-governance.pptx    (assembled deck with all slides)
    slide-00-cover.png                               (cover page thumbnail)
    slide-01-exec-summary.png                        (executive summary thumbnail)
    slide-02-<title-slug>.png                        (subsequent slide thumbnails)
    ...
```

If `./commspro/<deck-slug>/` already exists, ASK the user before overwriting: "Folder already exists. Overwrite, or save as `<deck-slug>-v2`?" Do not silently overwrite.

Before the first download, run `pwd` via Bash and capture the absolute path so you can include it in the final output (so the user always knows exactly where the files landed).

### Render workflow (Parallel-Deck Mode — Default)

1. **Create ONE parallel-deck job.** Call the MCP tool `create_slide_deck` (same argument shape for the `commspro` or the `slideai-local` server) with:

```json
{
  "job_create": {
    "type": "notes-to-slide",
    "name": "<deck name>",
    "presentation_name": "<deck-slug>.pptx",
    "job_payload": {
      "output_mode": "parallel_deck",
      "source_input": "<the user's ORIGINAL source input — the raw notes / document / context from Step 1, verbatim>",
      "slides": [
        {
          "title": "<Slide 1 title — full sentence, message-driven>",
          "content": "<COMPLETE markdown for slide 1: title, all bullets/dashes, tables, explicit metrics, and the Sources of insight line>",
          "layout_instructions": "<plain-language layout for slide 1 (e.g. 'Columns with icons') + any template/encoding hints>"
        },
        {
          "title": "<Slide 2 title>",
          "content": "<COMPLETE markdown for slide 2>",
          "layout_instructions": "<layout for slide 2>"
        }
      ],
      "content_instructions": "<optional: one-paragraph human-readable summary of the whole deck>"
    }
  }
}
```

**How this payload maps to the backend (`parallel_deck`):**
- Each entry in `slides[]` is rendered by its OWN single-slide agent, all in parallel, then merged into one deck **in array order**. So `slides` order === final deck order — list them cover → exec summary → body → appendix.
- One `slides[]` entry per slide you intend to render. The number of entries === the number of slides in the final deck. Do NOT dump the entire deck markdown into one field.
- `slides[i].content` MUST be the COMPLETE, self-contained markdown for that ONE slide (the exact Step 3 content for that slide). Each agent sees only its own `content` plus the shared `source_input` — no cross-slide references, no "see above", no placeholders.
- `slides[i].layout_instructions` carries that slide's internal layout (the plain-language layout assigned during spine construction) plus any template/encoding hints.
- `source_input` is the user's ORIGINAL source material, passed as shared context to EVERY slide agent so it can preserve source-backed detail beyond the plan. Include the raw notes/document text and any approved clarifications.
- `content_instructions` is OPTIONAL here (a human-readable summary); the per-slide `content` fields drive rendering.
- Do NOT send `target_slide_count` in `parallel_deck` mode — the slide count is implied by `len(slides)`.

**Do NOT send fragments, placeholders, or references to external context in any `content` field.**

2. **Poll until complete — this is a single, uninterrupted agent turn. DO NOT stop.**

**CRITICAL — how the poll loop actually works:** There is no background poller and no timer. The render job ONLY advances while YOU keep issuing `get_slide_deck_status` calls. If you end your turn, ask the user to wait, say "I'll check back", or otherwise stop emitting status calls, the job is abandoned mid-flight — the user sees it freeze at some % and it never resumes. This is the #1 failure mode. Treat "stop polling before a terminal state" as a hard error.

Run this loop, in ONE turn, without yielding control back to the user:

   a. Run a Bash `sleep 30` to pace the loop (do NOT "mentally wait" — actually issue the sleep). Decks typically finish in 2-3 min, so ~30s gives ~4-6 polls.
   b. Call `mcp__commspro__get_slide_deck_status` with `{ "job_id": "<job_id>" }`.
   c. Print the progress line (see below).
   d. Read the `status` field:
      - `completed` → exit the loop and go to step 3 (download).
      - `failed` → go to step 4 (handle failure).
      - anything else (e.g. `queued`, `processing`, `finalizing`, or a bare percentage) → go back to (a) IMMEDIATELY. Do not pause, do not summarize, do not ask a question, do not end the turn.

**Do NOT infer completion.** Only treat the job as done when the response literally reports `status: completed` AND contains output/presigned URLs. A stale, missing, or ambiguous status is NOT completion — keep polling.

**Cap:** Stop the loop after ~10 minutes of elapsed polling (full decks take 2-5 min typically). On hitting the cap, do NOT claim success. Tell the user the job is still running, show the last known status, and ask: "Still rendering after 10 min. Keep polling? (y/n)". Resume the loop only on `y`.

**Progress reporting (MANDATORY):** After each poll, print a progress update to the user:

```
Rendering deck... [status from API] (poll 1/~20)
Rendering deck... 25% complete (poll 2/~20)
Rendering deck... 60% complete — processing slide 7 of 12 (poll 3/~20)
```

Use whatever progress info the API returns (percentage, current slide, status message). If the API only returns a status string without percentage, show:

```
Rendering deck... status: "processing" (elapsed: 30s)
Rendering deck... status: "processing" (elapsed: 60s)
Rendering deck... status: "finalizing" (elapsed: 90s)
```

**Never poll silently.** The user must see that work is happening — but "showing progress" is NOT a reason to hand the turn back. Print the line and immediately issue the next poll.

3. **Download on completion.** When the job reaches `status: completed`, download the assembled deck and thumbnails:

```bash
mkdir -p ./commspro/<deck-slug>
curl -fL --retry 2 --retry-delay 2 -o "./commspro/<deck-slug>/<deck-slug>.pptx" '<output_file_presigned_url>'
# Download per-slide thumbnails if provided in output_files array
for each thumbnail in output_files:
  curl -fL --retry 2 --retry-delay 2 -o "./commspro/<deck-slug>/slide-<NN>.png" '<thumbnail_presigned_url>'
```

The presigned URLs are in the response payload. They are unauthenticated HTTPS GETs — no `Authorization` header needed.

4. **Handle failures.** If the job returns `status: failed`, surface the `error_message` and ask: "Deck rendering failed: <error>. Retry?" Don't auto-retry.

---

### Legacy: Per-Slide Rendering (for single-slide retries only)

Use this mode **only** when retrying a single failed slide after full-deck generation.

```json
{
  "integration_type": "Inception",
  "job_create": {
    "type": "notes-to-slide",
    "name": "<deck name> — Slide <N>: <slide title>",
    "presentation_name": "<deck name>",
    "slide_index": <N>,
    "job_payload": {
      "layout_instructions": "<archetype + template hints>",
      "content_instructions": "<COMPLETE markdown content for this single slide>"
    }
  }
}
```

Poll and download as above. The output is a single `.pptx` file for that slide.

### Final output format (MANDATORY)

```
Deck rendered (<N> slides)
Files saved to: <absolute path from pwd>/commspro/<deck-slug>/

| File | Description |
|------|-------------|
| <deck-slug>.pptx | Assembled deck with all <N> slides |
| slide-01.png | Thumbnail for slide 1 |
| slide-02.png | Thumbnail for slide 2 |
| ... | ... |

Open <deck-slug>.pptx to review the complete presentation.
```

### Guardrails

- Do NOT call MCP tools before the user explicitly approves the consent prompt above.
- Do NOT call MCP tools until slide content has been drafted (Step 3) and passed the Pre-Output/Pre-Render validations.
- **Default to full-deck mode** — use per-slide mode ONLY for single-slide retries after a failure.
- Do NOT silently overwrite an existing `./commspro/<deck-slug>/` folder.
- Do NOT swallow failures — always surface `error_message` and offer a retry.
- Do NOT skip the `pwd` step before downloads — the user must know the absolute path.

---

## Per-Slide Code Generation (on request, or automatic with mck_renderer)

### Compose-as-single-slides code pattern (MANDATORY)
Each slide is a standalone function: `def slide_N_topic_name(prs):`. Thin assembler at the bottom: `def generate_deck():`.

### Deck-level QA
- Rendering rotation: No two slides may use the same rendering
- Template variety: Mix templates (default, default_dark, 3_4_dark) when content warrants it
- MECE across slides: No redundant slides
- One insight per slide: Each slide answers exactly one question

---

## Comms Quality Rules

### Takeaway headlines (Rule 1.3)
Prefer takeaway sentences where they help the reader follow the argument. Topic labels remain valid for navigation, numbered steps, paired-slide setup, TOC/overview, and playbooks.

### Narrative flow (Rule 1.4)
Chapter the storyline with explicit transitions. Use section trackers or chapter dividers. Each section must answer the question raised by the prior section.

### Talk track alignment (Rule 1.6)
Projected presentations: slide text anchors verbal narrative. Pre-reads: richer on-page narrative since speaker is absent.

### One idea per slide (Rule 1.7)
One core idea per slide. Comparison or synthesis slides may integrate multiple elements but must serve a single governing argument.

### MECE structuring (Rule 2.1)
Structure content into MECE buckets. Items in each set must be of the same logical kind. If the set is intentionally not exhaustive, say so.

### Executive synthesis (Rule 2.2)
Synthesize as "what changed → why it matters → decision/ask" for decision documents.

---

## NEURO_AGENT — Per-Slide Workflow

### PHASE 1: SUBSTANCE EXTRACTION

#### 1a. Extract ALL content
Key messages, data items, categories, groupings, metrics, relationships.

#### 1a-2. Tabular input handling
- Faithful reproduction: transcribe exactly, lock structure
- Creative restructuring: treat as raw input, free to restructure
- Ambiguous: default to faithful reproduction

#### 1b. Count and classify
Item count, data types, hierarchy, density bucket (Sparse/Normal/Dense)

#### 1c. Identify groupings
Natural MECE categories, number of groups, equal-weight vs hierarchical

#### 1d. Synthesize to McKinsey language
- Remove fluff, tighten to crisp sentences
- Preserve specifics: mechanisms, metrics, proper nouns
- Apply parallel structure
- Language watch-outs: avoid "leverage", "synergy", "unlock", "value-add", "catalyze", "transform" (as buzzword)
- Avoid institutional tone: use "we/our" not "McKinsey"
- Do NOT over-synthesize into generic executive slogans; keep operational specifics and causal logic visible

#### 1d-2. Numeric fidelity
Numbers are sacred. NEVER modify, round, extrapolate, or "improve" any numeric value.

#### 1e. Craft the "so what?" title
- Message-driven, full sentence with insight
- Character limits: default <=110, 3_4_dark <=75, 2_3_grey <=65, 1_2 <=45
- NEVER below 22pt Georgia Bold

#### 1f. Audience calibration
- Default: Detailed (leave-behind)
- Executive: 3-5 items max
- Workshop: dual coding, scaffolded chunks
- Status update: exception-based

### PHASE 2: ARCHETYPE MATCHING + STRUCTURAL ADAPTATION

#### 2-pre. Content Shape Classifier (19 shapes)
Check every shape pattern. Mark all 19. Prefer structural shapes over generic.

#### 2a. Match archetype(s)
Mode A (explicit): Match trigger phrase directly.
Mode B (notes-to-slide): Score candidates, select 3 structurally different.
Mode C (creative expansion): Compose one hybrid option (chart + table, diagram + actions, or zone + split callout) using supported primitives.

#### 2b. Adapt to content volume
Item count → grid dimensions, table rows, matrix columns, font sizing.

#### 2b-2. Content density ceiling
Structure capacity determines text density — NOT the other way around.

#### 2c. Encoding decision
Three types: Data encoding, Structural encoding, Navigational encoding (density-triggered).

#### 2d. Select template
- Isolatable stat → 3_4_dark
- Two contrasting sides → 1_2
- Primary + secondary → 2_3_grey
- Big-number metrics → default_dark
- Default → default (full-width white)

### PHASE 3: COMPOSITION + CODE GENERATION

#### 3a. Read test script for selected archetype (MANDATORY)
#### 3b. Map content to layout positions
#### 3c. Compose supplementary elements
#### 3c-2. McKinsey table styling (MANDATORY for tables)
- Deep-blue-900 header, Arial body, grey hairline separators
- NEVER Excel-style cell flood fills
- Convert colored cells to McKinsey encoding (traffic lights, harvey balls, dimension bars)

#### 3d. Generate Python script
- ALWAYS use create_mck_presentation(), add_slide(), mck_specs.COLORS, mck_specs.ICON_PATHS
- ALWAYS use calculate_content_area_with_elements() for positioning
- ALWAYS use save_and_validate() instead of prs.save()

### PHASE 4: VALIDATION + RATIONALE

#### 4a. Title fit (2 lines max at 25pt, minimum 22pt)
#### 4b. Content fit (never drop items — change layout instead)
#### 4c. Data consistency check (title-data alignment, encoding preservation, source fidelity)
#### 4c-2. Cell fill scan (no shape.fill.solid() on table cells)
#### 4c-3. Composition element overlap check
#### 4d. Client-readiness quality gate (validate_slide_quality)
#### 4d-2. Visual self-check (render to PNG, read back)
#### 4e. Neuroscience validation + rationale in speaker notes

---

## Structural Diversity Rule

Three variants = three different building block families:
- Table (add_table_mck, add_grouped_table_mck, add_dimension_coded_matrix)
- Column/Flow (add_column_layout_mck, add_implications_column_layout_mck, add_scr_dark_callout)
- Grid/Row (add_grid_layout_mck, stacked rows, add_building_block_column)
- Specialized (add_gantt_chart, add_timeline_chevron, add_factoid_grid, etc.)
- Split contrast (Layout 8, 2/3 grey, 3/4 dark, category columns callout, dual-panel)

For decks with 6+ slides, target at least 4 distinct families across the deck, including:
- at least one chart-led slide
- at least one diagram- or flow-led slide (`dual_panel_cause_effect`, `building_block_column`, `tom_layout`, `north_star_layout`, or timeline variant)

---

## Navigational Encoding Patterns

Pattern 1: Inferred Favorability (comparison tables)
Pattern 2: Priority / Importance Highlights (category overviews)
Pattern 3: Effort / Complexity / Readiness (assessment rows)
Pattern 4: Category Identity (multi-domain content)

Density trigger: 8+ items, OR 3+ columns x 5+ rows, OR comparison with 3+ options.

---

## Critical Rules

1. Never hallucinate details
2. Use specific measurements
3. Always add legends for encoded elements
4. No large hero images
5. Encoding is data-driven, not mandatory
6. Title: 25pt default, 22pt minimum
7. Synthesized substance is sacred
8. Tables must look McKinsey, not Excel
9. Column order fidelity in faithful reproduction
10. Spot-check cell values on tabular input
11. ALWAYS use save_and_validate() instead of prs.save()
12. **MCP output must be fully self-contained** — no external references, no placeholders, no truncation
13. Avoid over-synthesis — dense, concrete, decision-ready substance beats elegant but empty summaries
14. Prefer chart/diagram hybrids when they clarify structure or quantitative insight better than bullets alone

---

## Dense Slide Patterns

> **Key principle:** Dense slides with well-structured information are preferred over sparse slides with excessive whitespace. When in doubt, add more supporting detail (implications, callouts, evidence tables).

### When to Use Dense Layouts

- **12+ data points** requiring visualization on a single slide
- **Executive audiences** expecting comprehensive single-page synthesis
- **Pre-read decks** where self-sufficiency demands completeness
- **Comparison slides** with 3+ options or dimensions
- **Status dashboards**, scorecards, and assessment slides

### Density Thresholds

| Fill Ratio | Assessment | Action |
|------------|------------|--------|
| ≥90% | **Optimal** | Target density — proceed |
| 75-89% | **Acceptable** | Consider adding implications bar or callout |
| 65-74% | **Sparse warning** | Add content: callout stat, evidence row, expanded bullets |
| <65% | **Critical** | Change archetype or add substantial content — do not render as-is |
| <50% | **Unacceptable** | Requires layout change AND content addition |

### Dense Preset Patterns

| Pattern | Use When | Typical Density | Components |
|---------|----------|-----------------|------------|
| `executive_dashboard_4zone` | C-suite single-page synthesis, 4 distinct content areas | 95%+ | 4 content zones + optional callout |
| `scr_with_evidence` | SCR structure with supporting data table or metrics row | 90% | SCR columns + evidence table below |
| `multi_dimension_assessment` | 4+ dimensions with status indicators | 90% | Dimension rows + traffic lights/Harvey balls |
| `status_dashboard` | Multiple KPIs, traffic lights, trend indicators | 95% | KPI grid + status encoding + trend arrows |
| `chart_with_breakdown` | Primary chart + detailed breakdown table or bullets | 85% | Chart (60%) + breakdown panel (40%) |
| `dual_panel_cause_effect` | Driver logic, cause-effect chain, trade-off explanation | 85% | Causal map + evidence/actions panel |
| `tom_layout` / `north_star_layout` | Operating model/system map with strategic layers | 85% | Layered diagram + KPI/risk callouts |

### Anti-Patterns to Avoid

These patterns signal sparse slides that waste working area:

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Single big stat on full slide** | 80%+ whitespace | Use `3_4_dark` template with callout panel + supporting context |
| **3-bullet slide with huge margins** | Content floats in center | Add implications bar, evidence table, or expand to sub-bullets |
| **3-column text bullets with numeric cues** | Missed visual encoding opportunity | Use chart + table/bullets zone mix; keep 3-column only when dense metric-backed + callout |
| **Two full tables on one slide** | Cognitive overload, weak visual hierarchy | Convert one table to chart/proxy visual and place in a zone composition |
| **Same layout 3+ times consecutively** | Visual monotony, reader fatigue | Swap middle instance to within-family alternative |
| **Empty working area below short table** | Wasted lower 40% | Add source row, implications bar, or key takeaway callout |
| **Centered content with equal margins** | No visual anchor | Anchor to top-left, use remaining space for callouts or evidence |
| **Table with no encoding** | Missed opportunity for visual hierarchy | Add traffic lights, category bars, or dimension coding when data supports it |

### Density Enhancement Recommendations

When a slide falls below 65% fill ratio, apply these enhancements based on content type:

| Content Type | Enhancement Options |
|--------------|---------------------|
| **Bulleted content** | Add implications bar below bullets, or expand bullets to include sub-points |
| **Metrics/KPIs** | Add callout stat panel using `3_4_dark` template |
| **Tables** | Add source row + key takeaway callout, or add encoding (traffic lights, Harvey balls) |
| **Single stat** | Convert to `3_4_dark` with supporting context in the main area |
| **12+ data points in flat layout** | Upgrade to `zone_layout` or `executive_dashboard_4zone` |
| **Timeline with few milestones** | Add milestone callouts or key decision points |

---

## Appendix: MCP-Ready Slide File Format Specification

When generating the final slide content markdown file (Step 3 output), follow this specification to ensure the MCP server can render slides without any external context.

### File Structure

```markdown
# [Presentation Title]
## [Presentation Subtitle]
> Deck: YYYY-MM-DD_[topic-slug]

---

## SLIDE 0: [Cover Page Title]

### Layout
Archetype: title_slide
Template: default

### Title
[Presentation title — derived from governing thought]

### Subtitle
[Date: Month DD, YYYY]
[Optional: Client name, project name, or meeting context]

---

## SLIDE 1: [Executive Summary Title]

### Layout
Archetype: [archetype name — REQUIRED]
Template: [template name — REQUIRED]

### Encoding
[encoding type — REQUIRED — e.g., traffic_lights, icons, category_bars, stat_callouts]

### Title
[Full title text exactly as it should appear on the rendered slide]

### Subtitle
[Full subtitle text — omit this section if no subtitle]

### Governing Thought
[One complete sentence capturing the key insight]

### [Section Header — e.g., "Key Findings" or "Column 1"]
- [Complete bullet point with all details, metrics, dates, and context]
- [Another complete bullet point — no abbreviations or "..."]
- [Continue for ALL items from source — never truncate the list]

### [Section Header — e.g., "Investment Details" or "Column 2"]
| Header 1 | Header 2 | Header 3 | Header 4 |
|----------|----------|----------|----------|
| [Complete cell] | [Complete cell] | [Complete cell] | [Complete cell] |
| [All rows from source] | [No missing rows] | [Full data] | [Every value] |
| [Continue for ALL rows] | | | |

### Implications
[Complete text for any callout, implications bar, or key takeaway box]

### Source
[Complete source citation with document name, date, and page/section if applicable]

---

## SLIDE 2: [Complete Message-Driven Title]

### Layout
Archetype: [archetype name — REQUIRED]
Template: [template name — REQUIRED]

### Encoding
[encoding type — REQUIRED]

[Same structure as above — complete content for every section]

---

## APPENDIX A: [Title]

[Complete appendix content]

---
```

### Layout and Encoding Reference

**Every slide MUST have both `### Layout` and `### Encoding` sections.** The consuming application uses this metadata to render the slide correctly.

| Section | Required Fields | Example Values |
|---------|-----------------|----------------|
| `### Layout` | `Archetype:` and `Template:` | `Archetype: grouped_table`, `Template: default` |
| `### Encoding` | Encoding type(s) | `traffic_lights`, `category_bars + icons`, `stat_callouts` |

**Common Archetypes with Density Guidance:**

| Archetype | Description | density_preference | upgrade_to (when) | combine_with |
|-----------|-------------|-------------------|-------------------|--------------|
| `scr_dark_callout` | Executive summary with callout panel | 0.85 | `scr_with_evidence` (evidence table available) | Always add `callout_stat` or `callout_text` |
| `executive_summary` | One-page synthesis slide | 0.80 | `executive_dashboard_4zone` (12+ data points) | Mixed-modality zones (KPI strip + chart/table + action callout); 3-column text only as sparse-use fallback |
| `grouped_table` | Tables with grouped rows or categories | 0.80 | `dimension_coded_matrix` (4+ dimensions) | Traffic lights/Harvey balls when status dimension exists |
| `columns` | 2-4 column layouts with bullets | 0.70 | `zone_3_T` or `chart_with_breakdown` (when numeric cues exist) | Use sparingly; add implications bar and quantitative visual if retained |
| `factoid_grid` | Big-number statistics in a grid | 0.85 | N/A | Subtitle row or trend indicators |
| `gantt_chart` | Timeline/Gantt with phases and milestones | 0.75 | `gantt_with_milestones` (10+ milestones) | Key milestone callouts |
| `stacked_rows` | Stacked horizontal content blocks | 0.80 | N/A | Numbered bars or progress indicators |
| `grid` | Grid of cards or content boxes | 0.85 | `zone_layout` (12+ items) | Category headers |
| `zone_layout` | 4-zone dense layout for dashboards | 1.0 | N/A | Preferred for 12+ data points |
| `timeline_chevron` | Chevron/arrow timeline | 0.70 | N/A | Milestone callouts or decision points |
| `dual_panel_cause_effect` | Two-panel comparison or cause/effect | 0.80 | N/A | Evidence row or implications bar |
| `section_divider` | Section break slide (minimal content) | N/A | N/A | N/A (intentionally sparse) |
| `meeting_objectives` | Agenda or objectives list | 0.60 | `stacked_rows_numbered` (items > 8) | Timeline or owner column |

**Density preference interpretation:**
- **1.0** = Maximum density target — use all available working area
- **0.85** = High density — minimal whitespace, add callouts to fill
- **0.80** = Standard density — some breathing room, but no large empty areas
- **0.70** = Moderate density — acceptable for simpler content, but consider enhancement
- **0.60** = Low density — upgrade archetype if content volume supports it

**Common Templates:**
- `default` — Standard white background
- `default_dark` — Dark background with light text
- `3_4_dark` — 3/4 content, 1/4 dark callout panel
- `2_3_grey` — 2/3 primary, 1/3 grey secondary
- `1_2_split` — 50/50 split layout

**Common Encodings:**
- `traffic_lights` — Red/amber/green status indicators
- `category_bars` — Colored bars by category
- `icons` — Icon-based visual encoding (see Icon Color Guidance below)
- `numbered_bars` — Numbered or sequenced bars
- `stat_callouts` — Big-number callouts
- `dimension_coded_matrix` — Multi-dimension comparison matrix
- `phase_colors` — Color-coded timeline phases
- `trend_arrows` — Up/down/flat trend indicators
- `checkboxes` — Checklist-style encoding
- `comparison_bars` — Side-by-side comparison bars

**Icon Color Guidance:**

Icons should use semantic colors that reinforce meaning. Apply colors consistently across the deck.

| Category | Color | Hex | Use For |
|----------|-------|-----|---------|
| **Growth / Positive** | McKinsey Green | `#00A651` | Revenue, expansion, success, opportunity, increase |
| **Risk / Negative** | McKinsey Red | `#E31B23` | Threats, decline, problems, blockers, decrease |
| **Caution / Moderate** | McKinsey Amber | `#F7A800` | Warnings, partial, in-progress, needs attention |
| **Technology / Digital** | McKinsey Blue | `#0085CA` | Tech initiatives, digital, data, AI, automation |
| **People / Organization** | McKinsey Teal | `#00857C` | Talent, teams, culture, HR, organizational |
| **Finance / Investment** | McKinsey Navy | `#003A5D` | Cost, investment, financial, capital, budget |
| **Operations / Process** | McKinsey Purple | `#6E2585` | Operations, supply chain, logistics, process |
| **Customer / Market** | McKinsey Orange | `#E55300` | Customers, market, brand, experience, demand |
| **Neutral / General** | McKinsey Grey | `#63666A` | Generic items, supporting detail, de-emphasized |

**Icon color rules:**
1. **Semantic consistency**: Same category = same color across all slides
2. **Limit palette**: Max 4-5 colors per slide to avoid visual noise
3. **No random colors**: Every color choice must have meaning
4. **Contrast check**: Ensure icons are visible on both light and dark backgrounds
5. **Legend when needed**: If color meaning isn't obvious, add a legend

**Icon + color combinations for common use cases:**

| Use Case | Icon | Color | Example |
|----------|------|-------|---------|
| Pillar/workstream headers | Relevant domain icon | Domain color | Technology pillar → gear icon → blue |
| Status indicators | Circle/dot | Traffic light colors | On track → green dot |
| Priority levels | Number badge | Intensity gradient | P1 → red, P2 → amber, P3 → green |
| Department/function | Department icon | Consistent per dept | Finance → chart icon → navy |
| Initiative type | Type icon | Type color | Cost reduction → down arrow → green (positive) |
| Risk items | Warning/alert icon | Red or amber | High risk → warning triangle → red |

**Anti-patterns to avoid:**
- Rainbow slides with 8+ random colors (pick max 4-5)
- Same icon with different colors for same category across slides
- Decorative colors that don't encode meaning
- Grey icons when color would add information value

### Content Requirements

| Requirement | ✓ Correct | ✗ Incorrect |
|-------------|-----------|-------------|
| Metrics | "€145-265M investment" | "significant investment" |
| Percentages | "margin improved from 8.1% to 12.3%" | "margin improved significantly" |
| Dates/Timelines | "Months 0-18" or "FY2027 Q1-Q2" | "near-term" or "soon" |
| Lists | All items from source included | "..." or "etc." at end |
| Tables | All rows and columns populated | Truncated with "..." row |
| References | Self-contained explanation | "see slide 2" or "per source" |
| Placeholders | None — all content filled | "[TBD]" or "[to be added]" |

### File Metadata

- **Encoding:** UTF-8
- **Line endings:** Unix (LF)
- **File extension:** `.md`
- **Naming convention:** `[deck-slug]-slides.md` or `[topic]-presentation.md`

### Size Guidance

| Deck Size | Slide Count | Expected Markdown Lines |
|-----------|-------------|------------------------|
| Short | 5-7 slides | 400-700 lines |
| Standard | 8-15 slides | 700-1,500 lines |
| Comprehensive | 15+ slides | 1,500-3,000+ lines |

If the output is significantly shorter than expected for the deck size, content is likely incomplete — return to Step 3 and expand.

### Validation Checklist (run before saving file)

Before finalizing the markdown file, verify:

- [ ] Every slide has `## SLIDE N:` header with complete title
- [ ] **Every slide has `### Layout` section** with Archetype and Template specified
- [ ] **Every slide has `### Encoding` section** with visual encoding type specified
- [ ] Every slide has all required content sections populated
- [ ] No placeholder text (`[TBD]`, `...`, `etc.`, `[placeholder]`)
- [ ] All tables have complete rows matching source document
- [ ] All metrics are explicit numbers from source
- [ ] No references to external documents or "see above"
- [ ] File can be sent to MCP server as-is with zero additional context
- [ ] A reader with NO access to the source document can understand each slide

**Critical: Layout and Encoding sections are REQUIRED for MCP rendering.** Without them, the consuming application cannot determine how to visually render the slide.

### Why This Matters

The MCP server operates in isolation, and in `parallel_deck` mode each slide is rendered by a SEPARATE agent:
1. Each slide agent receives only that slide's `content` + `layout_instructions`, plus the shared `source_input`
2. No agent has access to conversation history, other slides' content, or user context
3. Each agent renders exactly what it receives — fragments or cross-slide references produce incomplete slides
4. Incomplete slides require re-rendering, wasting time and API calls

**Each `slides[i].content` IS that slide's deliverable.** Treat every entry as complete, self-contained markdown — not as notes, an outline, or a fragment that depends on other slides.

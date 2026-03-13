# LEARNING_SYSTEM.md - Iterative Learning Framework

This system captures every failure as a rule and every success as a formula for continuous evolution.

---

## 🎯 Core Learning Philosophy

**Every interaction teaches us something.**
- Failures → Rules (what NOT to do) → `RULES.md`
- Successes → Formulas (what DOES work) → `FORMULAS.md`
- Patterns → Heuristics (decision shortcuts) → `HEURISTICS.md`
- Mistakes → Guards (preventive checks) → `RULES.md`

**Memory principle:** Learning captured here feeds the 4-layer memory stack. Daily logs are Layer 1 (archive). Distilled rules and formulas live in MEMORY.md (Layer 2) and get embedded into the vector DB (Layer 4) via `memory_flush.py`.

---

## 📊 Learning Cadence

### Daily (Every Session)
- **Learning Log**: `memory/YYYY-MM-DD.md` (Layer 1 — raw archive)
- Document: What worked, what failed, why
- Capture: Micro-rules and quick wins
- Run `memory_flush.py` at session end to embed new content
- Review time: 5 min per day

### Weekly (Monday Morning — hooked to existing Daily Self-Audit cron)
- **Weekly Learning Review**: `learning/weekly/YYYY-W##.md`
- Synthesize: Daily lessons into patterns
- Extract: Rules and formulas
- Update: `RULES.md` and `FORMULAS.md`
- Run `memory_flush.py` after updates
- Review time: 30 min per week
- **Executor**: Librarian via Daily Self-Audit cron (07:00 Mon, Europe/London)

### Twice-Weekly Auto-Curation (Wed & Sun 05:00 — existing cron)
- MEMORY.md rewrites itself with distilled learnings from daily notes
- `projects.md` updated with any status changes
- `memory_flush.py` runs automatically after rewrite
- No manual action needed — fully automated

### Monthly (1st of month)
- **Monthly Evolution Review**: `learning/monthly/YYYY-MM.md`
- Integrate: Weekly insights into strategy
- Assess: What changed, what improved
- Revise: Agent personas and capabilities
- Update: `EVOLUTION.md`
- Review time: 1-2 hours per month
- **Executor**: Librarian (manual trigger or add dedicated cron)

### Quarterly (Every 13 weeks — existing Quarterly Review crons)
- **Strategic Synthesis**: `learning/quarterly/YYYY-Q#.md`
- Consolidate: Monthly evolutions
- Identify: Structural improvements needed
- Plan: Next quarter's evolution
- Update: Long-term roadmap
- **Executor**: Existing Q2/Q3 crons + Yearly Memory Review (31 Dec)

---

## 📁 Learning File Structure

```
C:\Users\User\.openclaw\workspace\
│
├── MEMORY.md                        ← Layer 2: curated long-term brain (load every heartbeat)
├── RULES.md                         ← Learned constraints (updated weekly)
├── FORMULAS.md                      ← Proven success patterns (updated weekly)
├── HEURISTICS.md                    ← Decision shortcuts (updated monthly)
├── EVOLUTION.md                     ← Evolution history (updated monthly)
│
├── memory\                          ← Layer 1: raw session archives (load on-demand only)
│   ├── YYYY-MM-DD.md               ← Daily learning logs
│   ├── projects.md                  ← Layer 3: project registry (load every heartbeat)
│   ├── heartbeat-state.json
│   └── vector-flush-tracker.json    ← Tracks what's been embedded
│
├── learning\
│   ├── weekly\
│   │   ├── 2026-W09.md
│   │   └── ...
│   ├── monthly\
│   │   ├── 2026-02.md
│   │   └── ...
│   └── quarterly\
│       ├── 2026-Q1.md
│       └── ...
│
└── skills\
    └── vector-memory\
        └── scripts\                 ← Layer 4: vector DB scripts
            ├── memory_flush.py
            ├── memory_search.py
            ├── memory_store.py
            └── memory_forget.py
```

> **Load discipline:** Only `MEMORY.md` + `memory/projects.md` load at heartbeat (~4K tokens total). Daily notes and vector search are on-demand only. See Rule #16.

---

## 🔴 RULES.md - What NOT to Do

**Format**: Each rule has a failure origin story. Full file lives at workspace root as `RULES.md`.

Rules are numbered sequentially (#1–#18+, #101 reserved for system-level guards).

After adding any new rule:
1. Update `RULES.md`
2. Run `memory_flush.py` to embed the new rule into vector DB
3. Reference the rule number in `MEMORY.md` if it's system-critical

---

## 🟢 FORMULAS.md - What DOES Work

**Format**: Each formula is a proven success pattern. Lives at workspace root as `FORMULAS.md`.

```markdown
# FORMULAS.md - Proven Success Patterns

## Formula #1: The Daily Learning Capture
- **What works**: Capturing 3-5 learning points daily
- **Why**: Prevents knowledge loss, compounds insights
- **When to use**: End of each session
- **Steps**:
  1. Open today's memory file (memory/YYYY-MM-DD.md)
  2. Capture: 1 success, 1 failure, 1 insight
  3. Tag with: #learning, #success, #failure
  4. Add timestamp
  5. Run memory_flush.py to embed
- **Success rate**: 95% knowledge retention

## Formula #2: Weekly Pattern Extraction
- **What works**: 30-min weekly review synthesizes patterns
- **Why**: Daily data is noisy; weekly reveals patterns
- **When to use**: Every Monday (hooks into Daily Self-Audit cron)
- **Steps**:
  1. Run: memory_search.py "failures this week" to pull relevant embeddings
  2. Read weekly daily notes on-demand
  3. Extract 5-10 patterns/themes
  4. Identify 2-3 new rules, 2-3 confirmed formulas
  5. Update RULES.md and FORMULAS.md
  6. Run memory_flush.py after updates
- **Success rate**: 85% pattern accuracy

## Formula #3: The Hypothesis-Test-Document Loop
- **What works**: Structured experimentation
- **Why**: Prevents repeating failed experiments
- **When to use**: For any uncertain decision
- **Steps**:
  1. Form hypothesis: "If X, then Y"
  2. Test with specific scenario and expected outcome
  3. Document result in memory/YYYY-MM-DD.md
  4. Extract to RULES.md or FORMULAS.md
  5. Run memory_flush.py
- **Success rate**: 92% actionable insights

## Formula #4: The Failure-to-Rule Conversion
- **What works**: Systematic failure analysis
- **Why**: Failures are gifts — they teach guardrails
- **When to use**: After every error
- **Steps**:
  1. Document what failed in daily log
  2. Identify root cause
  3. Create guard/check to prevent recurrence
  4. Add to RULES.md with full format (origin, consequence, guard, implementation, status)
  5. Run memory_flush.py
  6. Reference rule number in MEMORY.md if system-critical
- **Success rate**: 100% if applied

## Formula #5: The Decision Heuristic
- **What works**: Encoding expert decisions as shortcuts
- **Why**: Removes decision fatigue, consistent outcomes
- **When to use**: For recurring decisions
- **Steps**:
  1. Identify recurring decision type
  2. Review past choices via vector search: memory_search.py "decision [type]"
  3. Find pattern in good vs bad choices
  4. Encode as IF/THEN rule in HEURISTICS.md
- **Success rate**: 88% better outcomes

[Continue adding formulas as they're validated...]
```

---

## 📈 EVOLUTION.md - How We Change

**Format**: Monthly progress snapshots. Lives at workspace root as `EVOLUTION.md`.

```markdown
# EVOLUTION.md - Agent Evolution History

## 2026-03 (March)
**Status**: Memory system upgrade — 4-layer stack installed

### System Changes
- Installed 4-layer memory stack (Daily Notes + MEMORY.md + projects.md + pgvector)
- Smart loading: ~4K tokens at startup vs 20K+ previously (~80% savings)
- Twice-weekly MEMORY.md auto-curation cron (Wed & Sun 05:00)
- Vector DB: PostgreSQL + pgvector, Gemini embeddings (768-dim)
- Rules 16-18 added for memory system discipline

### Agent Changes
- Librarian: Now owns memory_flush.py at every heartbeat
- All agents: Load only projects.md + MEMORY.md at startup (Rule #16)
- Cron updated: Auto-curation replaces manual weekly MEMORY.md edits

### Metrics
- Startup token cost: ~20K → ~4K (80% reduction)
- Rule count: 15 → 18 (+3 memory system rules)
- Vector DB: Operational (openclaw_memory)

## 2026-02 (February)
**Status**: Consolidation phase after fixes

### Agent Changes
- Librarian: Improved memory file organisation, automated daily logs
- Cruncher: Added structured failure analysis
- Architect: Weekly strategic review (was quarterly)

### System Changes
- Added LEARNING_SYSTEM.md
- Implemented RULES.md and FORMULAS.md
- Created automated learning capture

### Metrics
- Daily learning capture: 90% compliance
- Rule count: 7 → 15 (8 new rules)
- Formula count: 5 → 8 (3 new formulas)
```

---

## 🧠 HEURISTICS.md - Quick Decision Rules

**Format**: IF/THEN decision shortcuts. Lives at workspace root as `HEURISTICS.md`.

```markdown
# HEURISTICS.md - Decision Shortcuts

## When to Create a Cron Job vs Heartbeat
- IF: Exact timing needed (9:00 AM sharp) → THEN: Cron
- IF: Multiple checks can batch → THEN: Heartbeat
- IF: Output goes directly to channel → THEN: Cron
- IF: Needs user context from recent messages → THEN: Heartbeat

## When to Use Which Model
- IF: Complex reasoning or planning → THEN: DeepSeek (primary)
- IF: Broad/general tasks → THEN: Gemini Flash Lite
- IF: Cost-sensitive batch work → THEN: Gemini Flash Lite
- IF: Memory embeddings → THEN: Gemini (gemini-embedding-001, fixed)

## When to Write to Rules vs Formulas
- IF: Prevents bad outcome → THEN: Rule
- IF: Achieves good outcome → THEN: Formula
- IF: Uncertain effectiveness → THEN: Mark experimental, retest next week

## When to Load Which Memory Layer
- IF: Every heartbeat/startup → THEN: MEMORY.md + projects.md only (Layers 2+3)
- IF: Asked about specific past work → THEN: Load relevant daily note (Layer 1)
- IF: Semantic question about past decisions → THEN: Vector search (Layer 4)
- IF: Never at startup → THEN: Daily notes bulk load

## When to Run memory_flush.py
- IF: Heartbeat → THEN: Always (idempotent, total_stored=0 is fine)
- IF: Just wrote to MEMORY.md → THEN: Immediately after
- IF: Just added a new rule or formula → THEN: Immediately after
- IF: Auto-curation cron just ran → THEN: Built into cron (automatic)

## Error Severity Classification
- IF: Data lost, exposed, or vector DB out of sync → THEN: Critical, fix immediately
- IF: Feature broken → THEN: High, fix today
- IF: Performance issue → THEN: Medium, fix this week
- IF: Nice-to-have fails → THEN: Low, backlog
```

---

## 📋 Daily Learning Capture Template

**Use this in `memory/YYYY-MM-DD.md`:**

```markdown
# Daily Learning - YYYY-MM-DD

## ✅ What Worked Today
- [Task/action that succeeded]
- [Outcome and why it worked]

**Formula Origin**: [Reference relevant FORMULA # if applicable]

## ❌ What Failed Today
- [What broke or went wrong]
- [Why it failed]

**Rule Proposals**:
- Rule #X: [Guard to prevent recurrence]

## 💡 Key Insights
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]

## 🎯 Tags
#learning #[system-area] #[outcome-type]

## 📊 Metrics
- Tasks completed: X/Y
- Errors encountered: N
- Time to recovery: N min
- New rules proposed: N
- memory_flush.py run: ✅ / ❌
```

---

## 📅 Weekly Learning Review Template

**Use this in `learning/weekly/YYYY-W##.md`:**

```markdown
# Weekly Learning Review - Week ## (YYYY-MM-DD to YYYY-MM-DD)

## 📊 Weekly Statistics
- Daily learning captures: X/7
- Failures documented: N
- Successes documented: N
- New rules created: N
- New formulas validated: N
- memory_flush.py runs completed: N

## 🔴 Rules Learned This Week
1. Rule #N: [Title]
2. Rule #N: [Title]

## 🟢 Formulas Confirmed This Week
1. Formula #N: [Title]

## 🔍 Vector Search Used For
- [What past-work questions triggered a vector search this week]

## 📈 Memory System Health
- MEMORY.md line count: N / 400 max
- projects.md line count: N / 80 max
- Vector DB last flush: [date]
- Auto-curation last run: [date]

## 🎯 Next Week's Focus
- [Priority 1]
- [Priority 2]

## 📊 Confidence Levels
- Rule #N confidence: X% (tested Nx)
```

---

## 📈 Monthly Evolution Review Template

**Use this in `learning/monthly/YYYY-MM.md`:**

```markdown
# Monthly Evolution Review - [Month] [Year]

## 📊 Monthly Statistics
- Rules created: N new (N total)
- Formulas created: N new (N total)
- System changes: N
- Critical fixes: N
- Auto-curation runs completed: N (target: 8-9/month)

## 🔄 Agent Evolution
### Librarian
- Before / After / Impact / Status

### Cruncher
- Before / After / Impact / Status

### Architect
- Before / After / Impact / Status

## 🎯 Key Learnings
1. [Learning 1]
2. [Learning 2]

## 📈 Metrics Improvement
- Startup token cost: X → Y
- Error recovery time: X → Y min
- Knowledge retention: X% → Y%
- Daily capture compliance: X%

## 🚀 Next Month's Goals
1. [Goal 1]
2. [Goal 2]

## ⚠️ Critical Issues Fixed
1. [Issue and fix]
```

---

## 🔄 How Failure Becomes Rule

```
FAILURE OCCURS
    ↓
CAPTURE IN DAILY LOG (memory/YYYY-MM-DD.md)
    ↓
ANALYZE: Root cause? How to prevent?
    ↓
CREATE RULE: Add to RULES.md with full format
    ↓
RUN memory_flush.py → embeds rule into vector DB
    ↓
TEST: Does guard prevent the failure?
    ↓
REFERENCE in MEMORY.md if system-critical
    ↓
MONITOR: Track false positives at weekly review
    ↓
RULE BECOMES OPERATIONAL STANDARD
```

---

## 🎯 How Success Becomes Formula

```
SUCCESS HAPPENS
    ↓
CAPTURE IN DAILY LOG (memory/YYYY-MM-DD.md)
    ↓
IDENTIFY PATTERN: When else does this work?
    ↓
SEARCH HISTORY: memory_search.py "[pattern]"
    ↓
TEST HYPOTHESIS in 3 different contexts
    ↓
DOCUMENT FORMULA: Add to FORMULAS.md with steps
    ↓
RUN memory_flush.py → embeds formula into vector DB
    ↓
CREATE HEURISTIC in HEURISTICS.md
    ↓
FORMULA BECOMES OPERATIONAL STANDARD
```

---

## 📊 Learning System Metrics

Track these weekly in `learning/weekly/YYYY-W##.md`:

```json
{
  "week": "YYYY-W##",
  "learning_capture_rate": 0.0,
  "rule_creation_rate": 0.0,
  "formula_validation_rate": 0.0,
  "average_decision_time_seconds": 0,
  "system_uptime": 0.0,
  "error_recovery_time_minutes": 0,
  "knowledge_retention_percent": 0,
  "memory_md_line_count": 0,
  "projects_md_line_count": 0,
  "vector_db_total_memories": 0,
  "flush_runs_completed": 0,
  "auto_curation_runs": 0
}
```

---

## 🚀 Continuous Evolution Path

**Month 1**: Capture learning (Rules + Formulas)
**Month 2**: Synthesize patterns (Heuristics + vector search)
**Month 3**: Automate decisions (Rule engines + auto-curation)
**Month 4**: Predict failures (Preventive rules from vector patterns)
**Month 5**: Optimise success (Formula enhancement via semantic search)
**Month 6**: Strategic evolution (Architectural changes)
**→ Repeat**: Spiral upward

---

## 🔗 Integration Points With Memory System

| Learning Event | Action | Memory Layer Affected |
|---|---|---|
| Daily session ends | Write to `memory/YYYY-MM-DD.md`, run flush | Layer 1 + 4 |
| New rule added | Update `RULES.md`, run flush | Layer 4 |
| New formula added | Update `FORMULAS.md`, run flush | Layer 4 |
| Weekly review | Update `RULES.md` + `FORMULAS.md`, run flush | Layer 4 |
| Twice-weekly curation | Auto-rewrites `MEMORY.md`, auto-flushes | Layer 2 + 4 |
| Monthly review | Update `EVOLUTION.md`, update `MEMORY.md` summary | Layer 2 + 4 |
| Quarterly review | Strategic update to `MEMORY.md`, `projects.md` | Layer 2 + 3 + 4 |

---

**Status**: Active learning system
**Last Updated**: 2026-03-06
**Next Review**: Weekly (Monday 9am), Monthly (1st of month), Quarterly (every 13 weeks)

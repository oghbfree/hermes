# Importing OpenClaw Profile Data

When Hermes Agent runs on the same machine as an existing OpenClaw agent,
you can discover and ingest its profile files to bootstrap Hermes's
knowledge of the user without them having to re-explain everything.

## Discovery Pattern

Look for `~/.openclaw/` first. OpenClaw stores its isolated workspace
(profiles, memory) under:

```
~/.openclaw/
├── workspace/
│   ├── SOUL.md         # Agent identity — personhood, values, comms style
│   ├── USER.md         # Human profile — who they are, family, business
│   ├── TOOLS.md        # Environment-specific notes — URLs, APIs, accounts
│   ├── MEMORY.md       # Long-term memory — people, projects, system status
│   ├── AGENTS.md       # Operational rules, topic structure, workflows
│   ├── RULES.md        # Learned constraints from past failures
│   └── memory/         # Daily session notes
├── openclaw.json       # Agent config (models, providers, channels, cron)
└── .env                # API keys and secrets
```

## What to Look For and How to Absorb It

### 1. SOUL.md — Agent Identity & Communication Style
Save to `memory` as user communication preferences + personality. Key fields:
- Core values (e.g. privacy-first, autonomous execution)
- Communication style (e.g. no filler, no "good morning" before noon)
- How to address external contacts (e.g. "You are H. First person. Always.")
- Tone rules (humor, warmth with family, direct with employees)

### 2. USER.md — The Human Behind the Agent
Save to `memory` (both user profile + memory). This is the richest file:
- Name, email, location, timezone
- Personal context (family, life situation, goals)
- Business portfolio, active projects, employees
- Decision-making style, preferences, frustrations, priorities
- Key contacts with relationships and guidelines

### 3. TOOLS.md — Environment-Specific Notes
Save to `memory`. Contains:
- GitHub repos and accounts
- Business links (shop URLs, marketplaces)
- CLI tools and their paths
- API/integration details

### 4. MEMORY.md — Long-Term Memory
Save to `memory`. Contains:
- Current system status (service health, known issues)
- People directory with contact info, role, and comms guidelines
- Automation workflows (cron schedules, content pipelines)
- Learned patterns and formulas

### 5. AGENTS.md — Operational Rules
Typically too verbose and session-specific to save wholesale. Extract:
- Critical "forbidden" commands (gateway stop, destructive ops)
- Token/cost limits (economic mode)
- Telegram topic structure (topic ID → purpose mapping)
- External interaction rules (identity, boundaries, absolute rules)
- Cross-account message routing rules

### 6. RULES.md — Lessons Learned
Review for applicable patterns. Common categories:
- Security (credentials, file validation, atomic writes)
- API/timeout handling
- Concurrency and locking
- Memory discipline (token budgets, on-demand loading)
- Communication rules (expose credentials, apology loops)

### 7. openclaw.json — Config
Scan for:
- Model preferences (primary, fallback, image gen)
- Provider setup (OpenRouter, Ollama, Google)
- Channel bindings (Telegram, WhatsApp, accounts)
- Plugin/skill enablement
- Cron job descriptions and schedules

## Priority Order

When time-limited, read in this order:
1. **USER.md** — who they are (most important)
2. **SOUL.md** — how to communicate with/talk for them
3. **MEMORY.md** — current state and people
4. **openclaw.json** — system setup
5. **AGENTS.md** — rules (on-demand, only section)
6. **RULES.md** — lessons (skip unless troubleshooting)
7. **TOOLS.md** — environment details (nice to have)

## Hermes Memory Targets

| Profile fact | Save to |
|---|---|
| User identity (name, email, location, role) | `memory(target="user")` |
| Personal details, family, communication style | `memory(target="user")` |
| Businesses, projects, employees | `memory(target="memory")` |
| Environment setup, URLs, tools | `memory(target="memory")` |
| Comms preferences (tone, don't-say, rules) | `memory(target="memory")` |
| System status (services, known issues) | `memory(target="memory")` |

### 8. contacts.json / CONTACTS.md — Contact Directory\n\nOpenClaw keeps a structured contact list in two formats:\n\n| File | Format | Content |\n|------|--------|---------|\n| `~/.openclaw/workspace/contacts.json` | JSON | Structured: name, phone, role, type (staff/family/farm/associate), comms guidelines, schedules |\n| `~/.openclaw/workspace/CONTACTS.md` | Markdown | Human-readable with relationship context, access levels, tone rules |\n\n**Action:** Copy both files to `~/.hermes/`:\n```bash\ncp ~/.openclaw/workspace/contacts.json ~/.hermes/\ncp ~/.openclaw/workspace/CONTACTS.md ~/.hermes/\n```\n\nThen save a condensed reference to Hermes memory (target=`memory`):\n- Staff contacts with roles and comms guidelines\n- Family members with relationship notes\n- Key associates with scheduling info\n- Full path reference so future sessions know where the source files live\n\n**Skip** if contacts are already known or if the directory is stale.\n\n### 9. WORKFLOW_AUTO.md — Automated Workflow Replication\n\nOpenClaw often has a `WORKFLOW_AUTO.md` that defines startup sequences and periodic maintenance. Key functions to replicate in Hermes:\n\n| OpenClaw function | Hermes equivalent |\n|---|---|\n| Startup memory load (projects.md → MEMORY.md → SOUL.md → USER.md) | Handled natively — Hermes auto-loads memory on startup |\n| Topic-based system prompt routing | `channel_prompts` in config.yaml (see `references/migrate-telegram-topics-from-openclaw.md`) |\n| 48-hour maintenance cycle (memory maintenance, workspace audit, health check) | `hermes cron` job — create with `every 2 days` schedule |\n| Telegram message routing with per-topic prompts | Already covered by channel_prompts + `resolve_channel_prompt()` in gateway |\n| Vector memory sync / pgvector | Not applicable — Hermes uses its own memory provider |\n| Heartbeat state tracking | Not applicable — Hermes has its own health monitoring |\n\n**Cron job template** for the 48-hour cycle:\n```bash\nhermes cron create \\\n  --name workflow-48h-maintenance \\\n  --schedule \"every 2 days\" \\\n  --deliver local \\\n  --prompt \"Run 48-hour maintenance: 1) Memory maintenance — check recent daily notes for learnings 2) Workspace audit — check for orphaned .tmp/.lock files, verify critical files 3) Health check — run hermes doctor, verify dashboard responsive 4) Log results\"\n```\n\nOpenClaw-specific systems (pgvector, heartbeat JSON, vector-flush-tracker) do **not** transfer to Hermes — its memory system replaces them entirely.\n\n## When to Ingest

- **First session** with a new user who mentions OpenClaw — check for
  `~/.openclaw/` proactively
- **User says "go read my other agent's profile"** — use this guide
- **User seems frustrated that you don't know them** — check for
  cross-agent profile fodder
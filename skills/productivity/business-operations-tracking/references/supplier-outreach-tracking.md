# Supplier Outreach & Inquiry Tracking Pipeline

> Formerly the `supplier-outreach-tracking` skill. Consolidated into `business-operations-tracking`.

Manage structured supplier research files and coordinate multi-step procurement outreach across messaging bridges (WhatsApp, Telegram).

## Data Files

### Primary Supplier Research File
```
C:\Users\User\.hermes\workspace\memories\procurement\GHANA_SUPPLIER_RESEARCH.md
```

**Location history (check both if primary not found):**
- Current: `~/.hermes/workspace/memories/procurement/GHANA_SUPPLIER_RESEARCH.md`
- Legacy (OpenClaw era): `~/.openclaw/workspace/memory/business/GHANA_SUPPLIER_RESEARCH.md`
- Archive: `~/.hermes/workspace/.archive/raw-data/raw-data/GHANA_SUPPLIER_RESEARCH.md`

### Related Files
- Analysis reports: `~/.hermes/workspace/memories/procurement/GHANA_SUPPLIER_ANALYSIS_*.md`
- Business checkins: `~/.hermes/workspace/memories/business/checkins/`
- WhatsApp contacts: `~/.hermes/workspace/.archive/raw-data/raw-data/GHANA_SUPPLIERS_WHITELIST.txt`

## Workflow

### 1. Review Dashboard Status
Read the supplier research file. Parse the status table:
- Count: Inquiry Sent / Contacted / Quoted / Confirmed / Pending
- Identify the next Pending supplier (lowest # with status "Pending")
- Skip entries marked "(duplicate)" or "NOTED"

### 2. Prepare Inquiry Message
Use casual Ghanaian English (Twi/Pidgin style). Templates:

**Dashboard inquiry:**
> Morning, I dey find Kia Rio dashboard. You get am for stock? I need price, whether na new or used, and how e take be. I ready to come collect if di price sweet me small. Kindly let me know ASAP.

**Steering rack inquiry:**
> Morning, I dey find Kia Rio steering rack. I wan convert from right-hand drive to left-hand drive. You fit do am? I also wan know if you fit change the dashboard for same time. How much everything go cost and how long e go take?

**Price follow-up (for quoted suppliers):**
> [Name], you told me about [product] at [price]. I want to confirm: you get am for stock now? The quality na original or aftermarket? And you fit do small small for the price if I come take am this week?

### 2b. Business Operator Check-in Messages (Sammy, John)

These are NOT supplier inquiries — they're operational check-ins with staff members who manage business operations. Use casual but respectful Ghanaian English. Keep it brief (3-5 lines max).

**Sammy morning check-in (2Real Shop — Kantamanto):**
> Morning Sammy, hope you well. I dey check for you — how the shop be at Kantamanto? How sales be for this week? We get any stock issues or anything we need to sort? Kindly update me ASAP. Thank you.

**Variations to rotate (avoid sending identical messages daily):**
- Ask about specific stock levels: "How Zobase stock be? We need to order more anything?"
- Ask about customer traffic: "How customer side be? Market busy this week?"
- Ask about issues: "Anything we need fix for shop? Fans, lights, anything?"
- Mention Madam (rotate naturally, don't force it): "Madam say make I check on everything before weekend."
- Ask about MTN Momo transfers: "You don transfer the sales money go MTN Momo?"

**Key rules for Sammy messages:**
- Always ask about sales/operations AND any issues (two-part check-in)
- Keep it warm but business-like — he's staff, not a peer
- Don't discuss: supplier research, finances, salaries, other employees
- Don't send more than one message per day
- Log the drafted message in `workspace/memories/business/checkins/sammy.md`

**John morning check-in (Field Ops — Akoma/Jiji):**
> Morning John, hope you dey fine. I wan check — how the school partnerships dey go? Any new listings we need to do for Jiji? And Zobase side, everything dey update? Let me know what we need to push this week. Thank you.

**Key rules for John messages:**
- Always ask about his 3 targets: school partnerships, Jiji listings, Zobase updates
- Give clear task direction — he's task-execution, not strategic
- Don't discuss: salaries, finances, property plans, supplier research
- Keep it professional — direct instructions, not casual chat

### 3. Update Research File
Patch the supplier's row using the `patch` tool:
- Status: `"Pending"` → `"Inquiry Sent (YYYY-MM-DD HH:MM UTC)"`
- Contact Attempts: increment
- Notes: `"Prepared YYYY-MM-DD HH:MM UTC. Awaiting WhatsApp bridge to send."`

**Use `patch` tool** for targeted edits — the file is a markdown table and `write_file` would risk corruption.

### 4. Check WhatsApp Gateway (Before Attempting Delivery)

**⚠️ Architecture changed (2026-05-22):** WhatsApp now runs through the OpenClaw gateway (port 18789), NOT a standalone bridge on port 3000. The old `curl http://127.0.0.1:3000/health` check is obsolete.

Check if the OpenClaw gateway is running:
```bash
# Check if gateway process is running
ps aux | grep -i openclaw | grep -v grep
# OR check if port 18789 is listening
netstat -an | grep 18789 | grep LISTENING
```

- **Process running + port 18789 listening**: Gateway is up — attempt message delivery
- **No process / port not listening**: Gateway is DOWN — report in status, do NOT attempt send

**Gateway details:**
- Process: OpenClaw gateway (`openclaw gateway --port 18789`)
- Plugin: `@openclaw/whatsapp` v2026.5.4 (Baileys 7.0.0-rc.9)
- Config: `~/.openclaw/openclaw.json` → `channels.whatsapp`
- Session dir: `~/.openclaw/credentials/whatsapp/`
- Gateway log: `~/.openclaw/logs/gateway-restart.log`
- Start command: `gateway.cmd` (Windows) — **cannot be started from cron bash**

**Known issues:**
- Extended outages (weeks) are common — still prepare inquiries and update file when down
- Gateway cannot be started from cron MSYS environment (exits with "stdin is not a tty")
- When gateway is down, workflow degrades gracefully: prepare inquiry, update file, report status
- Port 3000 references in old logs are from the legacy bridge — ignore them

### 5. Post Status Report
Post to the configured Telegram delivery target. Use this structure:

**⚠️ CRON JOB DELIVERY (important):** When this workflow runs as a cron job with `deliver: "origin"`, the cron system auto-delivers the agent's final response to the configured Telegram target. Do NOT call `hermes send` to the same target — it will be skipped with the message "This cron job will already auto-deliver its final response." Instead, simply write the report as the agent's final reply text and let the cron system handle delivery. Only use `hermes send` if posting to a DIFFERENT target than the cron's origin.

```
GHANA SUPPLIER DASHBOARD — Daily Inquiry Report
DATE — HH:MM UTC

DASHBOARD SUPPLIERS (N total)
| Status | Count |
(Inquiry Sent / Contacted / Quoted / Confirmed / Pending)

Next uncontacted: Supplier #N (PHONE) — inquiry prepared today

TODAY'S INQUIRY — Supplier #N (PHONE)
[Prepared message]
BRIDGE STATUS LINE

BEST PRICES SO FAR
- Dashboard: #N — N,000 GHS (notes)
- Steering: #N — N,000 GHS (notes)

KEY BLOCKERS
1. WhatsApp bridge status and impact
2. No single supplier for BOTH steering conversion AND dashboard
3. Quote count vs needed for negotiation

NEXT ACTIONS
- Specific follow-ups with phone numbers
- File update confirmation at end
```

## Key Suppliers to Track

### Dashboard Hot Leads
- **#25 (+233 55 572 0391)** — CONFIRMED stock, price TBD (get quote ASAP)
- **#35 (+233 53 012 1872)** — QUOTED 6,000 GHS (verify legitimacy, negotiate)
- **#1–#10, #12** — Inquiry prepared, awaiting replies

### Steering Rack Hot Leads
- **#2 (+233 53 093 9891)** — QUOTED 2,000 GHS (confirm RHD→LHD conversion + dashboard swap)
- **#1 (+233 24 709 4333)** — Contacted, asked about conversion + dashboard

### Critical Gap
**No single supplier confirmed for BOTH steering conversion AND dashboard change.** This is the key unresolved strategic question.

## Pitfalls

- **File paths change across migrations.** Always use `find` or check multiple paths if the primary location returns empty. Current canonical path is under `.hermes/workspace/memories/procurement/`.
- **Skip duplicate entries.** Supplier #11 is marked "(duplicate)" — skip it when identifying the next pending supplier.
- **WhatsApp bridge may be offline for weeks.** Always check before attempting delivery. When offline, still prepare the inquiry and update the file status — just flag it as undelivered.
- **Don't mark inquiries as "sent to supplier" unless bridge confirmed delivery.** Use "Inquiry Sent (date)" for file-tracked preparation, but note "Awaiting WhatsApp bridge" in notes.
- **Don't `hermes send` to the same target the cron already delivers to.** When running as a cron job with `deliver: "origin"`, the agent's final response is auto-delivered to the Telegram origin. Calling `hermes send` to the same `telegram:chat_id:thread_id` is a no-op — the message is silently skipped. Just put the report directly in your final reply. Ask about RHD→LHD conversion capability AND dashboard swap capability — these are the key strategic questions.
- **Table formatting matters.** The research file uses markdown table syntax. When patching, preserve exact column alignment and pipe delimiters.
- **Supplier #25 is CONFIRMED with stock but price TBD.** Hot lead that needs price follow-up.
- **Supplier #35 has a quote (6,000 GHS) that needs verification.** Best dashboard price so far but unconfirmed.
- **Staff phone numbers in contacts.json are partially redacted.** When the WhatsApp gateway comes back online and you need to send actual WhatsApp messages, the redacted numbers (showing `+233****2253`) cannot be used directly. The unredacted `CONTACTS.md` file has full numbers. Always use `CONTACTS.md` for the full number when composing WhatsApp messages.
- **WhatsApp @mention format for Baileys/OpenClaw gateway:** When sending via the gateway API, use the full international phone number without `+` and with `@s.whatsapp.net` suffix (e.g., `233204252253@s.whatsapp.net`). Do NOT use the redacted form from contacts.json.

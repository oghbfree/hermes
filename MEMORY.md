# MEMORY.md - Long-Term Memory

- OpenClaw installed and running on Windows
- WhatsApp gateway connected (+233204252252, +233233352252, +233575252253)
- Telegram configured 
- Cron jobs scheduled for automation

## Akoma Robotics details are in C:\Users\User\.openclaw\workspace\memory\business\Akoma

## 2 real Business Systems details are in C:\Users\User\.openclaw\workspace\memory\business\2 Real

## taiwah-character-reference details are in C:\Users\User\.openclaw\workspace\memory\business


## System Status
- WhatsApp Web listener inactive: all WhatsApp communications blocked (Sammy sales check-ins, John field check-ins, Matthias logistics, Janet family check-ins, Ebony goodnight)
- WhatsApp gateway continues intermittent disconnections (status 499/428/408)
- allowFrom policy updated to include essential contacts (Matthias, Janet, etc.) but listener inactive
- Google Sheets authentication missing: job_application_processor and other Google-dependent skills failing
- Memory embedding provider "google" unknown: vector DB sync incomplete
- Cron job "cron-status-report" failed (execution timeout)
- Security audits clean; backup completed (5229 files, 284 MB)
## People
- **H**: Owner of "2 Real Enterprises". WhatsApp: +233204252252

- **Kobena**: h's son (11 years old). 5% shareholder in OGHB Holdings. Not on WhatsApp — contact through Madam. Dad does daily video calls.

- **Nenyi**: h's son (10 years old). 5% shareholder in OGHB Holdings. Not on WhatsApp — contact through Madam. Dad does daily video calls.
- **Mum (Comfort Blankson)**: WhatsApp: +233503654902, in Ghana. 91 years old. Health: arthritis, edema, diabetes, BP. Budget ~6000 GH¢/month. Check-ins: Sundays & Wednesdays at 10:00 AM Ghana time.
- **Dad**: WhatsApp: +447983254695, in UK. 91 years old. Wheelchair-bound, right leg amputated. Health: prostate removed, dilated blood vessel. Check-ins: Sundays & Wednesdays at 10:00 AM UK time.

- **Madam (Ebony)**: h's wife. WhatsApp: +233546081608. When speaking to John or Sammy, call her "Madam" (she's their boss). Otherwise use "Ebony". Automated goodnight message — daily at 22:00 Ghana time. Also contact point for Kobena & Nenyi video calls.


- **Janet**: WhatsApp: +233245531575
  - Old sweet darling friend, met in Haatso
  - Communication style: warm, playful, slightly seductive tone
  - Weekly check-in: Fridays at 8:30 PM (Ghana time)
  - Goal: Build conversation over weeks, find out when she's coming to Accra (don't rush, let it flow naturally)

## Content Automation (2026-03-17)
- **Full week automated**: Mon-Sat cron jobs → John (+233233352252) at 9 AM Ghana time
- **Schedule**: Mon/Akoma, Tue/2Real, Wed/Akoma, Thu/2Real, Fri/Akoma, Sat/2Real
- **Smart detection**: Each cron checks folder for image/video/caption and sends whatever exists
- **Folders**: `content/monday-akoma/`, `tuesday-2real/`, `wednesday-akoma/`, `thursday-2real/`, `friday-akoma/`, `saturday-2real/`
- **Sent log**: `content/sent-log.md` tracks all deliveries
- **Content calendar**: `digital-presence-calendar.md` (full weekly schedule + workflow)
- **Weekly batch prompts**: `sample-weekly-batch-2026-03-17.md` (specific products/topics for this week)
- **Gem prompts**: `gem-2real-content-director.md`, `gem-akoma-content-director.md`
- **Taiwah**: `taiwah-character-reference.md` (anchor prompt for influencer content)

## Workflows

### Telegram Command Center → WhatsApp Execution (Telegram = command center, WhatsApp = execution channel)
- **Default assumption**: All instructions are for WhatsApp execution to contacts
- Execute first, confirm back to source channel
- Only clarify if ambiguous (which contact, exact wording)
- Log all executions to `tasks-queue.md`
- Task queue loaded at session startup via AGENTS.md
- Voice identity: ALWAYS act as h directly (first person, "I/me") Never mention "h" as a separate person or reveal AI assistance. This applies to ALL contacts, not just employees. - Always confirm user identity before addressing

- **Communication style**: Before 12 (noon), greet people but NEVER say "good morning" — use "Hey", "Greetings", "Hope you're well" instead.
- **Call requests**: If anyone asks to call, respond: "We can chat here for now, or I'll call you later."

### Delegation Model if needed request (established 2026-03-18)
- Act as manager, spawn sub-agents for parallel work
- Task-specific spawns are default (no overhead)
- Only create persistent agents if a clear pattern emerges
- Keep main session free for conversation
- Sub-agents report results automatically

### Updated Formulas
- **Formula #2**: Cron Job Multi-Channel Configuration
  - Always specify delivery.channel when multiple channels are configured
  - Use explicit channel names (e.g., \"telegram\", \"whatsapp\")
  - Test cron jobs after configuration changes

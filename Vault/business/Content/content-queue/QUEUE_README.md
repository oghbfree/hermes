# 📹 CONTENT QUEUE SYSTEM — Weekly Video Posting Assistant

**Purpose:** Manage 7-video/week posting (Sun-Sat) with voice commands + Obsidian Canvas dashboard  
**Built:** 24/11/26 | **For:** Taiwah Builds + Akoma weekly content  
**Maintained by:** Sat-Nav

---

## WORKFLOW OVERVIEW (Weekly Cycle)

**Sunday 6 PM:** Research crons run (outliers, hooks, trends, customer voice) → 4 research files land in `research-weekly/YYYY-MM-DD/`

**Sunday 7 PM:** Kofi content director receives research → generates Weekly Creative Brief + 7 scripts → saves to `batch-briefs/YYYY-MM-DD/`

**Sunday 8 PM:** YOU review scripts in Obsidian → edit any that don't match vision → approve

**Sunday 9 PM:** YOU batch-render in Claude.ai web + Higgsfield + Taiwah project → download 7 videos to `content-output/batch-YYYY-MM-DD/`

**Sunday 9:30 PM:** YOU say **"ingest batch YYYY-MM-DD"** → Hermes scans folder, matches videos to scripts, builds `queue.json`

**Mon-Sun (daily at 12:05 AM):** Hermes messages **"what posts today?"** → YOU reply → Hermes shows video + caption + platform checklist → YOU post to 5 platforms → say **"posted"** → Hermes logs to sent-log, archives video, queues tomorrow

---

## VOICE COMMANDS (Primary Interface)

### 1. `ingest batch YYYY-MM-DD`
**When:** After Sunday render session (9:30 PM)  
**What it does:**
- Scans `content-output/batch-YYYY-MM-DD/` for 6-7 video files
- Matches each video to corresponding script in `batch-briefs/YYYY-MM-DD/` (by filename pattern: `mon-*.mp4` → `mon-uk-vs-ghana-SCRIPT.md`)
- Builds `queue.json` with 7 entries (id, file path, title, hook, caption, platforms, post_date, status=queued)
- Replies: "✓ 7 videos queued Mon 25/11 - Sun 01/12. Tomorrow (Mon): 'UK vs Ghana: Cockerel Mornings'"

**Example:**
```
You: ingest batch 2026-11-24

Hermes: 
Scanning C:/Users/User/.hermes/workspace/Vault/business/Content/content-output/batch-2026-11-24/...

Found 7 videos:
✓ mon-uk-ghana-cockerel.mp4 → Mon 25/11 UK-vs-Ghana
✓ tue-red-flag-written-quote.mp4 → Tue 26/11 Red Flag
✓ wed-akoma-dm-4schools.mp4 → Wed 27/11 Akoma DM
✓ thu-product-gorilla-tape.mp4 → Thu 28/11 Product Showcase
✓ fri-2real-cost-per-job.mp4 → Fri 29/11 2Real General
✓ sat-2real-weekend-prep.mp4 → Sat 30/11 2Real General
✓ sun-2real-book-quote.mp4 → Sun 01/12 2Real General

Building queue...

✓ 7 videos queued for Mon 25/11 - Sun 01/12.
Tomorrow (Mon 25/11): "UK vs Ghana: Cockerel Mornings"

Say "what posts today?" at 12:05 AM to see video + caption.
```

---

### 2. `what posts today?`
**When:** Daily at 12:05 AM (cron reminder) OR anytime you want to check  
**What it does:**
- Shows today's queued video details:
  - Title + hook
  - Runtime
  - Video file path (MEDIA: attachment for preview)
  - Full caption (copy-paste ready)
  - Platform checklist (FB/IG/TikTok/YT/WA Status)
- Waits for you to post, then say "posted"

**Example:**
```
You: what posts today?

Hermes:
📅 Monday 25 November — 1 video queued

🎬 "UK vs Ghana: Cockerel Mornings"
Hook: Ghana morning? Cockerel wakes you at 5 AM. UK morning? Alarm at 7 AM. I'll take the cockerel.
Runtime: 28s
Video: MEDIA:/path/to/mon-uk-ghana-cockerel.mp4

Caption (copy-paste ready):
---
Ghana morning? Cockerel cock-a-doodle-doo at 5 AM sharp.

UK morning? Alarm at 7 AM. Snooze button. Still tired.

I lived both. Ghana cockerel wins. Free alarm. Never fails. 
Plus, you're up before traffic. Win-win.

Sepha (event supplier) laughed when I said this. He said: 
"You can't snooze a cockerel." True.

What wakes YOU up? 📱 0204252252

#2Real #UKvsGhana #GhanaMorning #CockerelAlarm #Ghana
---

Platforms to post:
☐ Facebook
☐ Instagram
☐ TikTok
☐ YouTube Shorts
☐ WhatsApp Status

Say "posted" when done, or "skip today" to reschedule.
```

---

### 3. `posted`
**When:** After you post to all 5 platforms  
**What it does:**
- Marks video status = "posted" in `queue.json`
- Logs to `sent-log.md` with date, title, platforms, link (if you provide)
- Archives video to `content-archive/YYYY-MM-DD/` (keeps queue folder clean)
- Replies: "✓ Logged Mon 25/11 'UK vs Ghana: Cockerel Mornings' to sent-log. Tue video queued for tomorrow."

**Example:**
```
You: posted

Hermes:
✓ Mon 25/11 "UK vs Ghana: Cockerel Mornings" marked posted.
✓ Logged to sent-log: FB, IG, TikTok, YouTube, WA Status
✓ Video archived to content-archive/2026-11-25/

📅 Tomorrow (Tue 26/11): "Red Flag: Written Quote"

Say "what posts today?" at 12:05 AM to preview.
```

---

### 4. `queue status`
**When:** Anytime you want to see full week ahead  
**What it does:**
- Shows all 7 queued videos (Mon-Sun) with title, status, post date

**Example:**
```
You: queue status

Hermes:
📅 CONTENT QUEUE — Week of 25 Nov - 01 Dec

Mon 25/11 [QUEUED]  — UK vs Ghana: Cockerel Mornings
Tue 26/11 [QUEUED]  — Red Flag: Written Quote
Wed 27/11 [QUEUED]  — Akoma DM: 4 Schools Said Yes
Thu 28/11 [QUEUED]  — Product: Gorilla Mounting Tape
Fri 29/11 [QUEUED]  — 2Real: Cost Per Job Math
Sat 30/11 [QUEUED]  — 2Real: Weekend Prep (Motivational)
Sun 01/12 [QUEUED]  — 2Real: Book Quote (Atomic Habits)

7 videos ready. 0 posted.

Say "what posts today?" to see today's video.
```

---

### 5. `skip today` or `skip [day]`
**When:** Need to reschedule a video (supplier issue, content not right, etc.)  
**What it does:**
- Marks video "skipped" in queue
- Reschedules to next available slot (or you specify date)
- Swaps videos if needed

**Example:**
```
You: skip wed

Hermes:
Wed 27/11 "Akoma DM: 4 Schools Said Yes" marked skipped.

Options:
1. Reschedule to Thu 28/11 (swaps with Product video)
2. Reschedule to next Wed 03/12
3. Remove from queue (won't post)

Which option?
```

---

## OBSIDIAN CANVAS DASHBOARD (Visual Interface)

**File location:** `C:/Users/User/.hermes/workspace/Vault/business/Content/content-queue/WEEKLY_DASHBOARD.canvas`

**How to open:** Open Obsidian Desktop → navigate to Content/content-queue/ → open `WEEKLY_DASHBOARD.canvas`

**What you see:** Visual week-at-a-glance with 7 video cards (Mon-Sun)

**Each card shows:**
- Day + Date
- Series (UK-Ghana / Red Flag / Akoma / Product / 2Real General)
- Title
- Status (QUEUED 🟦 / POSTED ✅ / SKIPPED ⚠️)
- Runtime
- [View Video] button (opens file)
- [View Script] button (opens script.md)
- [Show Caption] button (opens caption text)

**Actions:**
- Click card → see full details
- Click [View Video] → video plays in default player
- Click [Show Caption] → caption appears in note (copy-paste ready)
- Click [Mark Posted] → updates queue.json, logs to sent-log (same as voice "posted")

**Visual layout:**
```
┌────────────────────────────────────────────────────────────┐
│  WEEK 25/11 - 01/12 · 2Real + Akoma Content Queue         │
├────────────────────────────────────────────────────────────┤
│  MON 25/11      TUE 26/11       WED 27/11      THU 28/11  │
│  UK-Ghana       Red Flag        Akoma DM       Product     │
│  Cockerel       Written Quote   4 Schools      Gorilla     │
│  [QUEUED 🟦]    [QUEUED 🟦]     [QUEUED 🟦]    [QUEUED 🟦]│
│  28s            29s             27s            26s         │
│  [View][Post]   [View][Post]    [View][Post]   [View][Post]│
│                                                            │
│  FRI 29/11      SAT 30/11       SUN 01/12                 │
│  2Real          2Real           2Real                      │
│  Cost/Job       Weekend Prep    Book Quote                 │
│  [QUEUED 🟦]    [QUEUED 🟦]     [QUEUED 🟦]               │
│  28s            30s             25s                        │
│  [View][Post]   [View][Post]    [View][Post]              │
└────────────────────────────────────────────────────────────┘
```

**When to use:**
- **Daily posting:** Voice commands faster ("what posts today?" → post → "posted")
- **Weekly planning:** Canvas dashboard better (see full week, check sequence, spot gaps)
- **Mid-week adjustments:** Canvas easier for drag-drop rearrange (swap Thu/Fri videos)

**How Canvas syncs with voice commands:**
- Canvas reads/writes same `queue.json` file
- Clicking [Mark Posted] in Canvas = saying "posted" in voice
- Both interfaces keep each other in sync

---

## FILE STRUCTURE

```
Vault/business/Content/
├── content-queue/
│   ├── queue.json                  ← queue database (voice + Canvas read/write)
│   ├── WEEKLY_DASHBOARD.canvas     ← Obsidian Canvas visual interface
│   └── QUEUE_README.md             ← this file (usage instructions)
│
├── content-output/
│   └── batch-YYYY-MM-DD/           ← rendered videos land here (Sunday 9 PM)
│       ├── mon-*.mp4
│       ├── tue-*.mp4
│       ├── wed-*.mp4
│       ├── thu-*.mp4
│       ├── fri-*.mp4
│       ├── sat-*.mp4
│       └── sun-*.mp4
│
├── batch-briefs/
│   └── YYYY-MM-DD/                 ← Kofi's scripts (Sunday 7 PM)
│       ├── creative-brief.md
│       ├── mon-uk-vs-ghana-SCRIPT.md
│       ├── tue-red-flag-SCRIPT.md
│       ├── wed-akoma-SCRIPT.md
│       ├── thu-product-SCRIPT.md
│       ├── fri-2real-SCRIPT.md
│       ├── sat-2real-SCRIPT.md
│       └── sun-2real-SCRIPT.md
│
├── content-archive/
│   └── YYYY-MM-DD/                 ← posted videos archived here (after "posted")
│
└── research-weekly/
    └── YYYY-MM-DD/                 ← research cron outputs (Sunday 6 PM)
        ├── outliers-external.md
        ├── hooks-trending.md
        ├── trend-digest.md
        └── customer-voice.md
```

---

## queue.json STRUCTURE

```json
{
  "week_start": "2026-11-25",
  "week_end": "2026-12-01",
  "videos": [
    {
      "id": "reel-2026-11-25-mon",
      "day": "Monday",
      "date": "2026-11-25",
      "series": "UK-vs-Ghana",
      "title": "Cockerel Mornings",
      "hook": "Ghana morning? Cockerel wakes you at 5 AM. UK morning? Alarm at 7 AM. I'll take the cockerel.",
      "file": "content-output/batch-2026-11-24/mon-uk-ghana-cockerel.mp4",
      "script": "batch-briefs/2026-11-24/mon-uk-vs-ghana-SCRIPT.md",
      "caption": "[full caption text here, 150-200 chars]",
      "hashtags": "#2Real #UKvsGhana #GhanaMorning #CockerelAlarm #Ghana",
      "platforms": ["facebook", "instagram", "tiktok", "youtube", "wa-status"],
      "runtime": "28s",
      "status": "queued",
      "posted_at": null,
      "archived_at": null
    },
    {
      "id": "reel-2026-11-26-tue",
      "day": "Tuesday",
      "date": "2026-11-26",
      "series": "Red-Flag",
      "title": "Written Quote Red Flag",
      "hook": "If your contractor won't put the quote in writing, walk away.",
      ...
    }
  ]
}
```

---

## TROUBLESHOOTING

**Q: "What posts today?" shows nothing**  
A: Queue might be empty. Check:
1. Did you run "ingest batch" after Sunday render?
2. Is `queue.json` present in `content-queue/`?
3. Run "queue status" to see full week — if empty, re-ingest

**Q: Video file path broken (can't preview)**  
A: Video might have been moved/renamed after ingest. Fix:
1. Find video in `content-output/batch-*/`
2. Update file path in `queue.json` manually
3. Or re-run "ingest batch" to rebuild queue

**Q: Caption doesn't match video**  
A: Script-to-video mismatch during ingest. Fix:
1. Open script in `batch-briefs/YYYY-MM-DD/[day]-SCRIPT.md`
2. Copy correct caption
3. Update `queue.json` caption field manually
4. Or edit script, re-ingest batch

**Q: Obsidian Canvas not syncing with voice commands**  
A: Both read same `queue.json` file. If out of sync:
1. Close Obsidian Canvas
2. Use voice commands to update queue ("posted", "skip", etc.)
3. Reopen Canvas — should refresh

**Q: Forgot to say "posted" yesterday, now two videos showing**  
A: Queue shows overdue + today's video. Mark yesterday posted:
1. Say "mark mon posted" (or specific day)
2. Hermes logs retroactively
3. Today's video now shows alone

---

## TIMING BREAKDOWN (Weekly)

**Sunday research + scripting + rendering + ingest:** ~3 hours  
  - Research crons: 30 min automated (you're offline)
  - Kofi scripting: 30 min automated (you're offline)
  - Your script review: 30 min (read, edit if needed)
  - Batch render (Claude.ai): 1-1.5 hours (7 videos, face-locked workflow)
  - Ingest batch: 5 min (voice command, automated matching)

**Daily posting (Mon-Sun):** ~5 min/day × 7 = 35 min/week  
  - 12:05 AM: Hermes reminder arrives
  - You: "what posts today?" → 1 min review video + caption
  - Post to 5 platforms: 3 min (copy caption ×5, upload video ×5)
  - Say "posted": 1 min (Hermes logs, archives, queues tomorrow)

**Total weekly time:** 3h 35min (Sunday 3h, daily 5min × 7)

**Before queue system (old way):**
  - Daily posting: 20 min × 7 = 140 min/week (find file, remember caption, post ×5, manually log)
  - Total: 180 min + 3h scripting/rendering = **5h+ weekly**

**Time saved with queue:** **~2 hours/week** (140min old posting - 35min new posting = 105min saved)

---

## CHANGELOG

**24/11/26 — Initial build**
- Voice commands: ingest, what posts today, posted, queue status, skip
- Obsidian Canvas dashboard (week-at-a-glance)
- queue.json structure (7 videos Mon-Sun)
- 12:05 AM daily reminder cron (voice trigger)
- File structure: content-output → batch-briefs → queue → archive

**Future enhancements (if needed):**
- Platform-specific captions (FB long, TikTok short, YT title+description)
- Analytics feedback loop (Hermes checks sent-log for 2× avg views, flags outliers)
- Auto-hashtag generator (pulls from trending hooks research)
- Thumbnail extractor (pulls first frame from video for Canvas preview)

---

**Built:** 24/11/26 | **Maintained by:** Sat-Nav  
**Questions?** Ask sat-nav in chat: "how do I skip a video?" or "queue not showing today's video"

# URGENT FIXES — 27/11/26

## 1. ✅ WHATSAPP CATALOG QUEUE REFILLED

**Command run:** `feed_wa_queue.py --max 200`  
**Result:** +51 fresh items added → wa_queue.json (total 283)  
**Backup:** wa_queue.json.bak_20261128_041620

**Sample items added:**
- Genuine Kilner Flip Top Glass Preserve Bottles 1L — GHS 780
- LG Tallboy/Floorstanding Home Theater Speaker — GHS 660
- Performance Power Pro 600W Corded Hammer Drill — GHS 600
- Netgear Ex2700 Wifi Range Extender — GHS 480
- Stanley FatMax Screwdriver Bit Set 50-Piece — GHS 480
- (46 more items)

**Next WhatsApp catalog poster run:** Will have items to post ✅

---

## 2. ⚠️ WHATSAPP AGENT PREFIX — STILL NOT REMOVED

**Problem diagnosed:**

The WhatsApp bridge has a **hardcoded default prefix** in `bridge.js`:

```javascript
const DEFAULT_REPLY_PREFIX = '☤ *Hermes Agent*\n────────────\n';
const REPLY_PREFIX = process.env.WHATSAPP_REPLY_PREFIX === undefined
  ? DEFAULT_REPLY_PREFIX
  : process.env.WHATSAPP_REPLY_PREFIX.replace(/\\n/g, '\n');
```

**What's happening:**
- Config.yaml has `reply_prefix: ""` (line 405) ✅ CORRECT
- BUT the WhatsApp gateway needs to be **restarted** to pick up the config change
- The bridge reads the env var on startup only

**The fix:**

**Option A: Restart WhatsApp gateway (RECOMMENDED)**
```bash
# Kill the WhatsApp bridge process
taskkill /F /IM node.exe /FI "WINDOWTITLE eq *whatsapp*"

# Or restart the entire Hermes desktop app (safest)
# Close Hermes Desktop → Reopen
```

**Option B: Set environment variable directly**
```bash
set WHATSAPP_REPLY_PREFIX=
hermes gateway restart whatsapp
```

**Verification after restart:**
- Send a test WhatsApp message to yourself
- Reply should have NO prefix (no "☤ *Hermes Agent*" header)

**Files checked:**
- ✅ `config.yaml` line 405: `reply_prefix: ""` (correct)
- ⚠️ `scripts/whatsapp-bridge/bridge.js` line 130-133: Has DEFAULT_REPLY_PREFIX
- ⚠️ Gateway needs restart to apply config

**Root cause:** Config change was made but gateway wasn't restarted, so it's still using the old default.

---

## 3. 📹 SATURDAY VIDEO FOR TAIWAH

**Today:** Saturday 30 November 2026 (or Saturday in current week)

**Weekly content schedule (7 videos Sun-Sat):**

| Day | Series | Description |
|-----|--------|-------------|
| **Mon** | UK vs Ghana | Lifestyle/culture/work comparison |
| **Tue** | Red Flag | Construction/planning problems + solutions |
| **Wed** | Akoma | Decision-makers (until Xmas then parents) |
| **Thu** | Product Showcase | Gift items, Zobaze qty≥5, Gorilla/Makita/branded tools |
| **Fri** | 2Real General | Product-led (Taiwah face + tools in workshop) |
| **Sat** | 2Real General | Product-led (Taiwah face + tools in workshop) |
| **Sun** | 2Real General | Product-led (Taiwah face + tools in workshop) |

**Saturday video theme (from QUEUE_README.md example):**
> **"2Real: Weekend Prep (Motivational)"**

**Format:**
- **Brand:** 2Real Enterprises
- **Face:** Taiwah (locked face from MASTER_LOCK.png)
- **Setting:** Workshop with tools
- **Style:** Product-led + motivational/weekend prep angle
- **Products:** Real stock (Zobaze inventory, tools in hand)
- **Length:** 25-30 seconds
- **Voice:** Taiwah 2026 locked voice (profile `9fa2a6d9`)

**Production workflow:**
1. **Sunday 7 PM:** Kofi (@content-buddy) writes 7 scripts including Saturday
2. **Sunday 9 PM:** YOU batch-render all 7 videos in Claude.ai + Higgsfield
3. **Sunday 9:30 PM:** Say "ingest batch YYYY-MM-DD" → builds queue
4. **Saturday 12:05 AM:** Reminder "what posts today?" → shows Sat video
5. **You post** → say "posted" → logs to sent-log

**Where to find the script:**
- If this week's batch was already rendered: `content-output/batch-YYYY-MM-DD/sat-2real-*.mp4`
- If scripts exist but not rendered: `batch-briefs/YYYY-MM-DD/sat-2real-SCRIPT.md`
- If nothing exists: Need to trigger Sunday content engine OR @kofi to write scripts

**Current status check needed:**
- Has this week's Sunday batch (25 Nov - 01 Dec) been rendered?
- If YES → find `sat-2real-weekend-prep.mp4` in content-output/batch-2026-11-24/
- If NO → need to either:
  - Trigger Kofi to write Saturday script NOW
  - OR wait until next Sunday 9 PM batch render

**To check if batch exists:**
```bash
ls C:/Users/User/.hermes/workspace/Vault/business/Content/content-output/batch-2026-11-24/sat*.mp4
ls C:/Users/User/.hermes/workspace/Vault/business/Content/batch-briefs/2026-11-24/sat*.md
```

---

## ✅ SUMMARY

1. **WA Queue:** ✅ Refilled with 51 items (283 total)
2. **WA Prefix:** ⚠️ Config correct but **RESTART GATEWAY** to apply
3. **Saturday Video:** 2Real General (Taiwah + workshop + tools) — check if batch-2026-11-24 exists

**Next steps:**
1. Restart WhatsApp gateway (close/reopen Hermes Desktop)
2. Check if Saturday video exists in batch-2026-11-24/
3. If video exists → post it
4. If not → message @content-buddy to write Saturday script

---

**Last Updated:** 27/11/26 11:10 AM

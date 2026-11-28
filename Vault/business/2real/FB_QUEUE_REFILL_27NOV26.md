# FB MARKETPLACE QUEUE — REFILLED
**Date:** 27/11/26 11:00 AM  
**Action:** Force refilled with fresh Jiji inventory

---

## ✅ WHAT WAS DONE

**1. Rebuilt queue from fresh Jiji data:**
- Ran `rebuild_queues_from_jiji.py`
- Matched 600 active Jiji items to feed images
- All 600 photos present (0 downloads needed)

**2. Backed up old queue:**
- Old queue: 289 items remaining (from previous batch)
- Backup saved: `next50.json.backup_20261127_110053`

**3. Replaced with fresh queue:**
- Copied `next50_batch2.json` → `next50.json`
- **New queue: 600 items** ready to post

---

## 📋 QUEUE CONTENTS (600 Items)

### **First 10 items (post first):**

| # | Item | Price | ID |
|---|------|-------|-----|
| 1 | Warehouse for Rent | 15,000gh | 16234184 |
| 2 | HP DesignJet T520 24in Large Format CAD Architecture Plotter | 9,000gh | 16898226 |
| 3 | Yale Smart Keyless Connected Door Lock With Nightlatch | 4,500gh | 12481086 |
| 4 | Commercial Aluminum & Glass Retail Display Showcase Cabinet | 2,000gh | 16898216 |
| 5 | Parkside 20v Cordless Drill Driver With Battery and Charger | 1,900gh | 13549080 |
| 6 | Nintendo Wii Console Bundle W Balance Board Motion Controllers | 1,750gh | 16898220 |
| 7 | HP LaserJet Pro 200 Color M251nw Wireless Printer | 1,750gh | 16898206 |
| 8 | HP LaserJet Pro 400 M401dn Heavy-Duty Duplex Mono Printer | 1,700gh | 16898201 |
| 9 | Bosch Paint Spray System 650W | 1,580gh | 16383160 |
| 10 | LEGO Star Wars Grogu With Hover Pram Set | 1,550gh | 16356475 |

### **Price distribution:**

| Range | Count | % |
|-------|-------|---|
| 0-500gh | 469 items | 78.2% |
| 500-1,000gh | 78 items | 13.0% |
| 1,000-2,000gh | 49 items | 8.2% |
| 2,000-5,000gh | 2 items | 0.3% |
| 5,000+gh | 2 items | 0.3% |

---

## 🤖 NEXT POSTING RUN

**Cron:** 2Real - FB Marketplace Batch Poster  
**Schedule:** Daily at 10:00 AM  
**Posts per run:** Up to 5 items (changed from 3 on 27/11/26)  
**Next scheduled:** Tomorrow 10:00 AM

**Will post these 5 first (tomorrow 10 AM):**
1. Warehouse for Rent - 15,000gh
2. HP DesignJet T520 Plotter - 9,000gh
3. Yale Smart Door Lock - 4,500gh
4. Commercial Display Showcase - 2,000gh
5. Parkside 20v Drill Driver - 1,900gh

**Daily ceiling:** 5 posts/day maximum (enforced by counter file)

---

## 📊 INVENTORY SOURCE

**Fresh from Jiji:** 600 items pulled from current 2Real Jiji listings  
**Last Jiji refresh:** 27/11/26 (via rebuild script)  
**Photos:** All 600 have images ready (no downloads needed)  
**Dedup:** Matched to feed, excludes already-posted items

---

## 🔄 QUEUE LIFECYCLE

**How it works:**
1. **Daily 10 AM:** Cron posts up to 5 items from top of queue
2. **After posting:** Items removed from queue, added to `fb_posted.json`
3. **Queue depletes:** ~120 days at 5/day (600 ÷ 5)
4. **When empty:** Run `rebuild_queues_from_jiji.py` + `promote_batch2.py` to refill

**Current position:** Fresh queue, 600 items, day 1

---

## 📂 FILES MODIFIED

**Queue files:**
- `next50.json` — NEW 600 items (refilled 27/11/26 11:00 AM)
- `next50.json.backup_20261127_110053` — OLD 289 items (backed up)
- `next50_batch2.json` — Source (600 items from rebuild)

**Location:** `C:/Users/User/.hermes/workspace/Vault/business/2real/2real-agent/channel_upload_package/`

---

## ⚠️ NOTES

**Why old queue was replaced:**
- Old queue had 289 items remaining
- `promote_batch2.py` requires BOTH FB + WA queues empty before promoting
- User requested immediate refill
- Forced replacement instead of waiting for queue to empty

**Old queue preserved:**
- Backed up to `next50.json.backup_20261127_110053`
- Can be restored if needed

**Posting capacity:**
- 5 items/day × 30 days = 150 items/month
- 600-item queue = ~4 months of daily posting
- Queue will need refill around March 2027

---

## ✅ READY

**FB Marketplace posting queue is now FULL and FRESH.**

**Next automatic post:** Tomorrow 10:00 AM (5 items)

**Manual trigger (if needed):**
```bash
hermes cron run --profile default "2Real - FB Marketplace Batch Poster"
```

---

**Last Updated:** 27/11/26 11:01 AM

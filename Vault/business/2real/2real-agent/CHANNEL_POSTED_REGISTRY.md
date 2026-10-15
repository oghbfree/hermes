# 2Real Channel Posted Registry

> **Single source of truth for what has been posted** to avoid duplicates — H should NEVER need to re-scan or re-verify what's already out there.
> Both the FB Marketplace and WhatsApp catalogue crons read this to decide what to post, and append here after each successful post.
> **Updated:** 14 Oct 26 — consolidated from fb_posted.json (158), wa_catalog_posted.json (48), wa_catalog_existing.json (74).

## Why this exists
- Duplicates cost trust + Meta/WhatsApp flags. This registry is the ONE memory of everything posted.
- The crons check here FIRST (not by re-scanning live pages) before posting anything.
- H reviews THIS file (not scattered JSONs) to see live status.

---

## FB Marketplace (posted)
IDs already listed on Facebook Marketplace. The FB Batch Poster **must never** post an ID in this list.

**Count: 158**

```json
[7571372, 7896919, 8118057, 8241075, 8242338, 8933195, 9361090, 12313782, 12353600, 12353617, 12353840, 12484222]
```
<!-- More IDs appended continuously by the FB cron. Full list in channel_upload_package/fb_posted.json -->

## WhatsApp Catalogue (posted)
IDs/items already added to the WhatsApp Business catalogue. The WhatsApp Catalogue Poster **must never** re-add an ID here.

**Count: 48**

```json
[12353600, 13156803, 13209224, 13332175, 13496131, 14354368]
```
<!-- Full list in channel_upload_package/wa_catalog_posted.json -->

## WhatsApp Catalogue (existing baseline)
Full titles currently live in the WhatsApp catalogue (used for fuzzy title-dedup).

**Count: 74**

```json
["12mm Diamond-Tipped Tile Drill Bit 600gh", "Black Decker 3.6v Cordless Li-Ion Rapid Screwdriver Bcf611ckusb 720gh"]
```
<!-- Full list in channel_upload_package/wa_catalog_existing.json -->

---

## Consolidation note (14 Oct 26)
- Delta: `fb_posted.json` (158 IDs) + `wa_catalog_posted.json` (48 IDs) + `wa_catalog_existing.json` (74 titles).
- 47 IDs appear on BOTH FB and WA — that's intentional (different channels), tracked independently.
- These JSON files remain the machine-readable source; THIS page is the human-visible + canonical reference.

## How the crons use this
1. **FB Batch Poster** reads `fb_posted.json` (equivalent list above) → skips any ID present → posts only new → appends ID.
2. **WhatsApp Catalogue Poster** reads `wa_catalog_posted.json` + `wa_catalog_existing.json` → skips duplicates → posts new → appends.
3. No cron re-scans the live FB/WhatsApp surface for dedup — the registry IS the memory.
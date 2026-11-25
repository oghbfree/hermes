# 📸 PRODUCT IMAGE RESEARCH CRON — High-Res Stock Prep

**Purpose:** Extract high-res product images from Jiji/Zobaze inventory for video use  
**Trigger:** Sunday 6 PM (runs with other research crons)  
**Output:** `research-weekly/YYYY-MM-DD/product-images.json` (clean product shots)  
**For:** Thursday Product Showcase + any video needing product props

---

## 🎯 PROBLEM THIS SOLVES

**Current state:**
- Jiji listings have product photos (but mixed quality, backgrounds, watermarks)
- Zobaze inventory has photos (but may not be video-optimized)
- User manually sources stock photos during render (adds friction)

**Desired state:**
- Automated weekly scan of inventory
- Extract BEST product images (high-res, clean background preferred)
- Pre-curated library of video-ready product shots
- User grabs from library during render (zero friction)

---

## 🔄 CRON WORKFLOW

### INPUT SOURCES (Priority Order)

**1. Jiji Listings (Primary)**
- File: `jiji_listings_full.json` (1,400+ active listings)
- Has: Product images (jijistatic URLs)
- Quality: Mixed (some high-res, some low-res, some with backgrounds)

**2. Zobaze Inventory (Secondary)**
- File: `inventory_agent.json` (stock levels)
- May have: Product photos (if integrated)
- Quality: Unknown (needs verification)

**3. Manufacturer Websites (Tertiary)**
- For branded items (Makita, Gorilla, DeWalt, Bosch)
- Scrape official product pages
- Quality: Highest (professional product shots, clean backgrounds)

---

## 📋 EXTRACTION LOGIC

### Step 1: Scan Inventory (Plentiful Stock First)
```python
# Read inventory_agent.json
# Filter: qty >= 5 (plentiful stock = video-worthy)
# Extract: product name, category, Jiji ID, image URLs
# Output: candidate list (200-300 items)
```

### Step 2: Fetch Images from Jiji
```python
# For each candidate:
#   - Fetch jijistatic image URLs (usually 2-6 images per listing)
#   - Download to cache (temp storage)
#   - Analyze quality (resolution, aspect ratio, background type)
```

### Step 3: Image Quality Scoring
```python
# Score each image (0-100):
#   - Resolution: 1080p+ = 30 pts, 720p = 20 pts, <720p = 10 pts
#   - Background: Clean/white = 30 pts, Plain color = 20 pts, Cluttered = 10 pts
#   - Product prominence: Product fills frame = 20 pts, Product small = 10 pts
#   - Watermark/text: None = 20 pts, Minimal = 10 pts, Heavy = 0 pts
#
# Pick highest scoring image per product
```

### Step 4: Manufacturer Fallback (Branded Items Only)
```python
# For branded items (Makita, Gorilla, DeWalt, Bosch, LEGO):
#   - If Jiji image score < 60 (mediocre quality)
#   - Search manufacturer website (e.g., makita.co.uk/products/[model])
#   - Scrape official product image (usually PNG, clean background)
#   - Download to cache
#   - Score (usually 90-100, professional quality)
```

### Step 5: Output JSON
```json
{
  "week": "2026-11-24",
  "products": [
    {
      "name": "Gorilla Super Glue Gel 20g",
      "jiji_id": "hNlviw5d2SCW...",
      "category": "adhesive",
      "qty": 8,
      "best_image": {
        "url": "https://jijistatic.com/.../gorilla-glue.jpg",
        "source": "jiji",
        "resolution": "1080x1080",
        "quality_score": 85,
        "background": "white_clean",
        "local_path": "cache/product-images/gorilla-glue-gel-20g.jpg",
        "usable_for_video": true
      },
      "alternate_images": [
        {
          "url": "https://jijistatic.com/.../gorilla-glue-2.jpg",
          "quality_score": 72,
          "background": "plain_color"
        }
      ]
    },
    {
      "name": "Makita 18V Cordless Drill DHP484",
      "jiji_id": "jKmwFt8x9ABC...",
      "category": "power_tools",
      "qty": 6,
      "best_image": {
        "url": "https://makita.co.uk/products/.../dhp484.png",
        "source": "manufacturer",
        "resolution": "2000x2000",
        "quality_score": 95,
        "background": "transparent_png",
        "local_path": "cache/product-images/makita-drill-dhp484.png",
        "usable_for_video": true
      },
      "alternate_images": []
    }
  ],
  "stats": {
    "total_products_scanned": 287,
    "high_quality_images": 142,
    "medium_quality_images": 98,
    "low_quality_images": 47,
    "manufacturer_sourced": 23
  }
}
```

---

## 📂 FILE STRUCTURE

```
Vault/business/Content/
├── research-weekly/
│   └── YYYY-MM-DD/
│       ├── outliers-external.md
│       ├── hooks-trending.md
│       ├── trend-digest.md
│       ├── customer-voice.md
│       ├── product-showcase-pick.md
│       └── product-images.json ← NEW (high-res images)
│
└── cache/
    └── product-images/
        ├── gorilla-glue-gel-20g.jpg
        ├── makita-drill-dhp484.png
        ├── dewalt-impact-driver.jpg
        └── ... (200+ cached images)
```

---

## 🎬 HOW KOFI USES THIS

**Thursday Product Showcase Script:**

**Step 1:** Hermes runs product showcase picker (Thu morning)
- Reads `inventory_agent.json`
- Picks: "Gorilla Super Glue Gel 20g" (qty 8, gift-suitable, Week 1 rotation)
- Writes: `product-showcase-pick.md`

**Step 2:** Kofi writes Thursday script (Sunday 7 PM)
- Reads `product-showcase-pick.md` (chosen product)
- Reads `product-images.json` (finds Gorilla Glue image)
- Includes in script:
  ```
  PROPS:
  - Taiwah-held: Gorilla Super Glue Gel (actor holds bottle)
  - Stock props: High-res product image available
    - Source: cache/product-images/gorilla-glue-gel-20g.jpg
    - Resolution: 1080x1080, white clean background
    - Quality score: 85/100 (video-ready)
  ```

**Step 3:** User renders (Sunday 9 PM)
- Opens Kofi's script
- Sees: "High-res product image available at [path]"
- Copies image path → feeds to Higgsfield alongside Taiwah prompts
- Higgsfield composites: Taiwah holding product + high-res product B-roll

**Result:** No manual image hunting, pre-curated video-ready shots

---

## 🔍 IMAGE QUALITY CRITERIA

### ✅ GOOD (Usable for Video)
- Resolution: 1080p+ (1080×1080 or higher)
- Background: White/clean, plain color, transparent PNG
- Product prominence: Product fills 60%+ of frame
- Watermarks: None or minimal (small corner logo acceptable)
- Quality score: 70-100

**Example:** Manufacturer product shots, professional Jiji photos

### ⚠️ ACCEPTABLE (Usable with Caution)
- Resolution: 720p (720×720 to 1080×1080)
- Background: Slightly cluttered but product still prominent
- Product prominence: Product fills 40-60% of frame
- Watermarks: Moderate (Jiji watermark, small text)
- Quality score: 50-69

**Example:** Average Jiji listing photos

### ❌ POOR (Not Usable)
- Resolution: <720p (blurry when scaled)
- Background: Heavily cluttered (product lost in scene)
- Product prominence: Product <40% of frame
- Watermarks: Heavy (large text overlays, multiple watermarks)
- Quality score: 0-49

**Example:** Low-quality phone photos, heavily watermarked images

---

## 🤖 AUTOMATION RULES

### When to Run:
- **Weekly:** Sunday 6 PM (alongside other research crons)
- **On-demand:** When user says "refresh product images"

### What to Cache:
- **High-quality only:** Score ≥70 (video-ready)
- **Plentiful stock:** Qty ≥5 (likely to showcase)
- **Branded items priority:** Makita, Gorilla, DeWalt, Bosch, LEGO (manufacturer images preferred)

### Cache Cleanup:
- **Keep:** Last 4 weeks of images (rolling window)
- **Delete:** Images >30 days old (re-fetch if needed)
- **Size limit:** 500 MB cache max (oldest deleted first if exceeded)

---

## 📊 SUCCESS METRICS

**After Sunday 6 PM run:**
- ✅ 150-200 high-quality product images cached
- ✅ 20-30 manufacturer-sourced images (branded items)
- ✅ All plentiful stock items (qty ≥5) have image available
- ✅ Thursday Product Showcase always has high-res image ready

**User experience:**
- ✅ Zero manual image hunting during render
- ✅ Pre-curated library of video-ready shots
- ✅ Higher quality videos (crisp product B-roll)

---

## 🛠️ TECHNICAL NOTES

**Rate limiting:**
- Jiji scraping: 1 request/sec (avoid WAF blocks)
- Manufacturer sites: 1 request/2 sec (polite crawling)
- Total scan time: 10-15 min for 300 products

**Error handling:**
- If Jiji image fetch fails → mark as "unavailable", skip to next
- If manufacturer site blocked → fall back to Jiji images
- If all images <50 quality score → flag for manual review

**Storage:**
- Images cached locally (not committed to git)
- JSON manifest committed (paths, scores, metadata)
- User accesses via local paths during render

---

## ✅ ADDED TO PHASE 2 BUILD LIST

**Updated Phase 2 components:**
1. ✅ Outlier scanner (15% internal, 85% external competitors)
2. ✅ Hook extractor (trending hooks filtered for positive voice)
3. ✅ Trend digest (Ghana news angles)
4. ✅ Customer voice miner (objections + testimonials)
5. ✅ **Product image research** ← NEW (high-res stock prep)
6. ✅ Product showcase picker (Thu automation)
7. ✅ Queue system commands (ingest, what posts today, posted)
8. ✅ 12:05 AM daily reminder

**Total Phase 2 time:** 50-60 min (was 40-50, +10 min for product image cron)

---

**Last updated:** 24/11/26  
**Status:** Specification complete, ready to implement in Phase 2  
**Requested by:** User (high-res product images for video props)

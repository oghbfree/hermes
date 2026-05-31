# Jiji Ghana — Scraping & Competitive Intelligence Notes

**Date:** 2026-05-14

## Market Scale (from Tavily search)

Jiji Ghana is a massive marketplace:
- 105,923 ads — Vehicle Parts & Accessories
- 19,889 ads — Cars
- 3,283 ads — Motorcycles & Scooters
- 213,676+ ads — Electronics
- 330,394+ ads — Home, Furniture & Appliances

## Cloudflare Blocking

**Jiji Ghana is fully behind Cloudflare.** All endpoints (HTML pages, API paths, search) return the JS challenge page. The following methods were tested and ALL failed:

- `curl` with various User-Agent strings → 403 + Cloudflare challenge
- Python `cloudscraper` library → 403 + Cloudflare challenge
- Mobile User-Agent headers → 403 + Cloudflare challenge
- `X-Requested-With: XMLHttpRequest` header → 403 + Cloudflare challenge
- Guessed API endpoints (`/api/search`, `/api/v1/search`, `/api/products`, `/api/search/listings`) → all 403

**Conclusion:** Only browser-based scraping (Puppeteer, Playwright, or services that run headless Chrome) can bypass Jiji Ghana's Cloudflare protection.

## Scraping Options

### Option A: Rent Apify Actor — Jiji Product Search Scraper
- **URL:** https://apify.com/stealth_mode/jiji-product-search-scraper
- **Cost:** $20/month rental + Apify usage fees
- **Pros:** Already built, uses browser under the hood, structured JSON output
- **Cons:** Built for Jiji.ng (Nigeria) — untested on Jiji.com.gh; monthly rental fee
- **Actor ID:** `stealth_mode/jiji-product-search-scraper`
- **Rental page:** https://console.apify.com/actors/TX1g9ld3tKYlblgoP
- **Status:** Free trial expired — must rent before testing on .gh

### Option B: Custom Apify Actor (Puppeteer/Playwright)
- **Cost:** Free to build, pay only for compute (pennies per scrape)
- **Pros:** Full control, no monthly rental, tailored to Jiji Ghana's structure
- **Cons:** Takes a few hours to build and test

### Option C: Browser Scraping Services (ScrapingBee, ScrapingAnt, etc.)
- **Cost:** Pay-per-use
- **Pros:** No build effort, handles Cloudflare automatically
- **Cons:** Need to set up integration; ongoing per-scrape cost

### Option D: Manual Collection
- **Cost:** Zero
- **Cons:** Not scalable for 1,200+ listings

## Recommended Use Cases for 2 Real

1. **Competitor price monitoring** — Track pricing in your categories (cars, electronics)
2. **Supplier sourcing** — Find bulk inventory listings, distress sales
3. **Market gap analysis** — Identify underserved categories or regions
4. **Listing optimization** — Analyze top-performer competitor listings (images, descriptions, pricing)
5. **Price benchmarking** — Validate your Zobase pricing against market rates

## Key Data Fields Available (from Apify actor output)

- `title`, `price_obj` (value in GHS), `price_title`
- `region`, `region_name`, `region_parent_name` (geographic data)
- `attrs` (product specifications — make, model, condition, etc.)
- `images`, `images_count`
- `is_boost`, `is_top` (promotion status — indicates seller investment)
- `is_owner` (private seller vs. dealer)
- `is_inspected` (quality indicator, especially for vehicles)
- `tops_count` (popularity metric)
- `user_id` (track individual sellers/dealers)
- `status` (active/sold/expired — useful for sell-through analysis)
- `category_id`, `category_name`, `category_slug`
- `details` (full description text)
- `url` (direct link to listing)

## Next Steps

1. Decide on approach (Option A rent vs. Option C build)
2. If renting: go to Apify console, rent the actor, then test with Jiji Ghana URLs
3. If building: create a Puppeteer actor on Apify that navigates Jiji Ghana search pages and extracts listing data
4. Set up scheduled scrapes for key categories once scraping is confirmed working
5. Feed data into a dashboard or weekly market intelligence report

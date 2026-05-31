# Jiji Ghana Scraping Notes

## Site Profile

- **URL**: `https://jiji.com.gh`
- **Seller page**: `https://jiji.com.gh/sellerpage-1249739` (2Real Enterprises)
- **Protection**: Cloudflare Turnstile (managed challenge, `cType: 'ma'`)
- **Scale**: 105K+ vehicle parts, 19K+ cars, 213K+ electronics, 330K+ home/garden

## Cloudflare Turnstile Details

Jiji Ghana uses **Cloudflare Turnstile**, not a simple JS challenge:

- Challenge page loads `https://challenges.cloudflare.com/turnstile/v0/b/883a1f27d85f/api.js?onload=rLIi5&render=explicit`
- CSP allows `unsafe-eval` and scripts from `challenges.cloudflare.com`
- Challenge config: `window._cf_chl_opt = { cFPWv: 'b', cType: 'ma', cRay: '...', cH: '...' }`
- The Turnstile widget must execute and return a token to pass
- **Even visiting the main page (jiji.com.gh/) triggers Turnstile**

## What Doesn't work

| Method | Result |
|--------|--------|
| curl / simple HTTP | Cloudflare JS challenge |
| cloudscraper (Python) | 403 blocked |
| Firecrawl | Key truncated in config; also blocked by Cloudflare |
| Apify Puppeteer + datacenter proxy | 403 — Cloudflare flags DC IPs |
| Direct API endpoints (`/api/search`, etc.) | All behind Cloudflare |
| puppeteer-extra-stealth (local) | Turnstile doesn't resolve — stays on "Just a moment..." |
| `headless: false` mode | Still blocked |
| Persistent profile (`userDataDir`) | Still blocked |
| Waiting 30s+ | Challenge never auto-resolves |
| Clicking checkbox | No checkbox present — it's invisible Turnstile |

## What works (or should work)

1. **Rent existing Apify actor** ($20/month): `stealth_mode/jiji-product-search-scraper` (TX1g9ld3tKYlblgoP) — built for Jiji.ng, likely works on .gh. This is the recommended approach.
2. **Apify residential proxy upgrade** (~$8-15/month): Residential IPs might pass Turnstile. Not guaranteed.
3. **Manual browsing**: Human passes Turnstile, then cookies can be exported and reused (short-lived).

## CSS Selectors (from page analysis)

Jiji Ghana uses these class patterns:
- Product cards: `.b-list-advert__item`, `.js-advert-list-item`, `.qa-advert-list-item`
- Title: `.b-advert-title`, `.qa-advert-title`, `.b-list-advert__item-title`
- Price: `.b-advert-price`, `.qa-advert-price`, `.b-list-advert__item-price`
- Location: `.b-advert-location`
- Pagination: `.b-pager__next a`, `a[rel="next"]`

## Search URL pattern

```
https://jiji.com.gh/search?query=<encoded>&page=<n>
```

## Existing Apify Actor

- **Actor**: `engaging_yataghan/jiji-ghana-scraper` (ID: `8T2QcqVVkwM9nDdqA`)
- **Status**: Built and deployed (5 builds), runs successfully, but gets 403 due to Turnstile
- **Code**: `~/.openclaw/workspace/jiji-scraper/`
- **Local scraper**: `~/.openclaw/workspace/jiji-scraper-local/scraper.js` — also blocked by Turnstile
- **Fix needed**: Rent existing working actor or upgrade to residential proxy

## Decision (2026-05-15)

H confirmed Option B (local Puppeteer) but testing showed Turnstile blocks it. Recommended path forward: rent the existing `stealth_mode` Apify actor for $20/month. H has not yet confirmed this decision.

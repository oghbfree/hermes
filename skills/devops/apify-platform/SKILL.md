---
name: apify-platform
description: Build, deploy, and run actors on Apify platform — Puppeteer/Playwright scraping, source management, proxy configuration, and SDK v3 patterns. Triggered when building Apify actors, scraping Cloudflare-protected sites, or troubleshooting Apify builds/runs.
---

# Apify Platform — Actor Development & Deployment

## Key Facts

- **Account**: `engaging_yataghan` (oghbfree@gmail.com), FREE tier
- **Actor ID** (Jiji Ghana scraper): `8T2QcqVVkwM9nDdqA`
- **API Key**: stored in session logs / memory
- **Free tier limits**: 5 concurrent runs, 8GB actor memory, 625 CU/month, 500 actors, 7-day data retention

## Critical SDK v3 Pattern

Apify SDK v3 **does NOT have `Apify.main()`**. Using it causes immediate crash:

```
TypeError: Apify.main is not a function
```

**Correct v3 pattern (ESM):**
```javascript
import { Actor, log } from 'apify';
import { PuppeteerCrawler } from 'crawlee';

await Actor.init();
const input = await Actor.getInput() || {};
// ... your code ...
await Actor.exit();
```

## Source Upload — Must Use CLI

The Apify REST API v2 **does NOT support source file upload**. All source-files endpoints return 404.

**Only way to push source:**
```bash
apify login --token <API_KEY>
apify init <actorName> -y   # first time only
apify push --wait-for-finish 120
```

## Base Images

| Image | Puppeteer? | Use |
|-------|-----------|-----|
| `apify/actor-node:20` | ❌ | Plain Node.js actors |
| `apify/actor-node-puppeteer-chrome:22` | ✅ | Browser scraping |

**Without Dockerfile**, `apify push` uses `apify/actor-node:20` (no Chrome). For Puppeteer, you **must** provide a Dockerfile:

```dockerfile
FROM apify/actor-node-puppeteer-chrome:22
COPY package.json ./
RUN npm install --omit=dev --quiet
COPY src/ ./src/
COPY INPUT_SCHEMA.json ./
```

## Proxy Configuration

- `BUYPROXIES94952` — datacenter proxies (5 available). **Cloudflare flags these** on hard-mode sites like Jiji Ghana.
- `RESIDENTIAL` — residential IPs (not available on free tier). Needed for Cloudflare bypass.
- `GOOGLE_SERP` — SERP proxies (0 available on free tier).

**Cloudflare bypass on Jiji Ghana**: Even with Puppeteer + datacenter proxy, Jiji returns 403. Residential proxies or a local machine with residential IP required.

## Actor Structure

```
project/
├── .actor/
│   ├── actor.json          # Actor manifest (input, storages)
│   └── INPUT_SCHEMA.json   # Input schema (must be in .actor/)
├── src/
│   └── main.js             # Entry point
├── package.json            # Must include "type": "module" for ESM
├── INPUT_SCHEMA.json       # Copy in root too (Apify convention)
└── Dockerfile              # Only for Puppeteer/Playwright actors
```

## Debugging Failed Runs

```bash
# Get run log via API (works for free tier):
# GET /actor-runs/{runId}/log   ← NOTE: NOT /acts/{actorId}/runs/{runId}/log
```

The log endpoint is `/actor-runs/{runId}/log` — the `/acts/{actorId}/runs/{runId}/log` path returns 404.

Common errors:
- `Apify.main is not a function` → SDK v3 migration issue (see above)
- `403 blocked` → Cloudflare detected datacenter IP, need residential proxy
- Build succeeds but run fails in <5s → check entry point and SDK version
- `Apify is not defined` → forgot to `import { Actor } from 'apify'`

## Cloudflare Turnstile (Important)

Some sites (including Jiji Ghana) use **Cloudflare Turnstile** — a CAPTCHA system that:
- Loads from `https://challenges.cloudflare.com/turnstile/v0/.../api.js`
- Renders an interactive widget that must complete before page content loads
- **Detects automated browsers** even with puppeteer-extra-stealth
- Cannot be bypassed by datacenter proxies or headless browser tricks

**Signs of Turnstile:**
- Page title stays "Just a moment..." indefinitely
- Challenge HTML contains `window._cf_chl_opt` with `cType: 'ma'`
- Script src includes `challenges.cloudflare.com/turnstile/`
- No checkbox to click — it's an invisible challenge

**What works against Turnstile:**
- Residential IP + real browser that has previously passed the challenge (cookies)
- Apify actors specifically built to handle Turnstile (e.g., `stealth_mode/jiji-product-search-scraper`)
- Manual browsing (human interaction)

**What does NOT work:**
- puppeteer-extra-stealth alone
- Apify datacenter proxies (`BUYPROXIES94952` group)
- `headless: false` mode
- Persistent browser profiles (`userDataDir`)
- Waiting longer (challenge won't auto-resolve)

## Local Puppeteer Alternative

When Apify proxies are blocked, use local machine with residential IP:

- **H's machine**: Edge at `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- Use `puppeteer-core` (not full puppeteer) to avoid downloading Chrome
- Set `executablePath` to Edge binary
- **Note**: This works for basic Cloudflare JS challenges but NOT for Turnstile-protected sites

```javascript
const browser = await puppeteer.launch({
  executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  headless: true,
});
```

## References

- `references/jiji-ghana.md` — Jiji Ghana specific scraping notes (Cloudflare Turnstile, selectors, what works/doesn't)

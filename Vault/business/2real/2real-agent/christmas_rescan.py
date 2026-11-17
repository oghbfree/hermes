#!/usr/bin/env python3
"""
2Real Christmas Gap Re-scan
===========================
Compares the unlisted-inventory gap list against the CURRENT live Jiji ad list and
emits a refreshed priority list. Built 16/11/26 after three false "already listed /
not listed" calls.

WHY THIS EXISTS — the three failure modes it fixes
--------------------------------------------------
1. STALE SNAPSHOT. The old re-scan compared against `_jiji_live_allsort_tmp.json`,
   which was scraped 24 Oct. By 16 Nov it was 3 weeks stale, so the scan kept
   re-suggesting items H had already posted. FIX: always read the fresh
   `jiji_ads_performance.json` produced by `jiji_ads_harvest_cdp.py`.
2. TRUNCATED HARVEST. `jiji_ads_harvest_cdp.py` capped at `max_pages=50` = 1,250 ads,
   silently dropping the tail. Raised to 400 (natural end now ~page 56, 1,396 ads).
   FIX: this script ABORTS if the harvest looks capped (multiple of 25 on the last page).
3. TITLE MISMATCH. The same item is titled differently in inventory vs on Jiji:
       inventory "Ring Automotive RWL1000 1000 lumen work light With Power Bank"
       live      "Ring Automotive Rechargeable Floodlight With Power Bank"
   No lexical matcher bridges that - zero shared model code. FIX: a persistent
   ALIAS MAP (`jiji_title_aliases.json`) plus model-code matching, brand+noun
   fuzzy matching, and difflib. Anything still unmatched is written to a REVIEW
   file for a human, never silently dropped.

USAGE
-----
    python christmas_rescan.py            # run scan, write outputs
    python christmas_rescan.py --review   # also print the unmatched review list

OUTPUTS
-------
    christmas_gap_list.json          -> rewritten with listed/listed_on_jiji flags
    CHRISTMAS_PRIORITY_LIST.md       -> the human-readable refreshed list (vault)
    christmas_rescan_review.json     -> ambiguous pairs needing a human eye
    jiji_title_aliases.json          -> learned aliases (append-only, never lost)
"""
import json, os, re, sys, difflib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT_2REAL = os.path.dirname(HERE)

LIVE = os.path.join(HERE, "jiji_ads_performance.json")
GAP = os.path.join(HERE, "christmas_gap_list.json")
ALIASES = os.path.join(HERE, "jiji_title_aliases.json")
REVIEW = os.path.join(HERE, "christmas_rescan_review.json")
OUT_MD = os.path.join(VAULT_2REAL, "CHRISTMAS_PRIORITY_LIST.md")

# --- tokens we never match on ---------------------------------------------------
STOP = set("""for with and the a an of in on to from new used uk original pcs pc set kit
brand quality heavy duty professional plus max pro series size colour color black white
red blue green grey gray small large mini""".split())

# model-code pattern: letters then 3+ digits (RWL1000, DT4323, RTC2000, 043603),
# or bare 3+ digit runs joined by dashes (0-43-603)
CODE_RE = re.compile(r'\b([a-z]{1,6}\d{2,}[a-z0-9]*|\d{2,}(?:-\d{2,})+)\b')
VOLT_RE = re.compile(r'\b(\d+(?:\.\d+)?)\s*(v|volt|w|watt|ml|l|ah|mm|inch|lm|lumen)\b')

def norm(s):
    s = str(s or "").lower()
    s = s.replace('&', ' and ')
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def codes(s):
    return set(CODE_RE.findall(norm(s)))

def specs(s):
    """electrical/physical specs - 3.6v, 250ml, 2100 lumens. Cheap but useful."""
    return set(f"{a}{b}" for a, b in VOLT_RE.findall(norm(s)))

def toks(s):
    return {t for t in norm(s).split() if t not in STOP and len(t) > 1}

def brand(s):
    t = norm(s).split()
    return t[0] if t else ""

def ratio(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def load_aliases():
    if os.path.isfile(ALIASES):
        try:
            return json.load(open(ALIASES, encoding="utf-8"))
        except Exception:
            pass
    # seeded with the mismatches found on 16/11/26 so they never recur
    return {
        "map": {
            "Ring Automotive RWL1000 1000 lumen work light With Power Bank":
                "Ring Automotive Rechargeable Floodlight With Power Bank",
            "CTEC CT1 Sealant White": "Ct1 Unique Sealant and Construction Adhesive",
            "CTEC CT1 Sealant Black": "Ct1 Unique Sealant and Construction Adhesive",
            "Stanley FatMax Torpedo Scaffold Level 3 Vials 043603 220":
                "Stanley Scaffold Torpedo Level 0-43-603",
        },
        "note": "inventory title -> live jiji title. Append as mismatches are found. Never delete.",
        "updated": "2026-11-16",
    }


def harvest_looks_capped(ads):
    """The harvest paginates 25/page. Exactly N*25 with N large suggests a cap, not an end."""
    return len(ads) % 25 == 0 and len(ads) >= 1000


def match_one(name, live_norm, live_titles, alias_map):
    """Return (verdict, score, matched_title, how). verdict in live|review|unlisted."""
    nm = norm(name)

    # 0) alias map - authoritative, both directions
    for inv, jiji in alias_map.items():
        if norm(inv) == nm or nm == norm(jiji):
            if jiji == "__DISTINCT__":
                # human-verified as a DIFFERENT product - never let fuzzy matching
                # resurrect it as "already listed"
                return "unlisted", 0.0, None, "confirmed-distinct"
            for t in live_titles:
                if norm(t) == norm(jiji):
                    return "live", 1.0, t, "alias"
            # alias declared but that ad is genuinely absent now
            return "unlisted", 0.0, None, "alias-missing"

    c = codes(name)
    sp = specs(name)
    b = brand(name)
    tk = toks(name)
    best = (0.0, None, "")

    for idx, lt in enumerate(live_titles):
        ln = live_norm[idx]
        # a) shared model code = strong evidence (but require brand agreement for 2-char codes)
        lc = codes(lt)
        if c and lc:
            shared = c & lc
            if shared:
                strong = any(len(x) >= 6 for x in shared) or brand(lt) == b
                if strong:
                    sc = 0.95
                    if sc > best[0]:
                        best = (sc, lt, "code:" + ",".join(sorted(shared)))

        # b) brand + spec agreement (e.g. 3.6V glue gun)
        if b and brand(lt) == b and sp and (sp & specs(lt)):
            sc = 0.9
            if sc > best[0]:
                best = (sc, lt, "brand+spec")

        # c) brand + high token overlap
        if b and brand(lt) == b and tk:
            o = len(tk & toks(lt)) / max(1, len(tk))
            if o >= 0.6:
                sc = 0.6 + 0.3 * o
                if sc > best[0]:
                    best = (sc, lt, f"brand+nouns({o:.2f})")

        # d) plain string similarity
        r = difflib.SequenceMatcher(None, nm, ln).ratio()
        if r >= 0.72 and r > best[0]:
            best = (r, lt, f"difflib({r:.2f})")

    if best[0] >= 0.85:
        return "live", best[0], best[1], best[2]
    if best[0] >= 0.55:
        return "review", best[0], best[1], best[2]
    return "unlisted", best[0], best[1], best[2]


def main():
    if not os.path.isfile(LIVE):
        sys.exit("missing %s - run jiji_ads_harvest_cdp.py first" % LIVE)

    live_doc = json.load(open(LIVE, encoding="utf-8"))
    ads = live_doc.get("ads") or []
    live_titles = [str(a.get("title", "")) for a in ads]
    live_norm = [norm(t) for t in live_titles]
    aliases = load_aliases()
    alias_map = aliases["map"]

    print(f"live harvest : {len(ads)} ads  (scraped {live_doc.get('scraped')})")
    if harvest_looks_capped(ads):
        print("  !! WARNING: harvest length is a multiple of 25 - it may have hit the page cap.")
        print("     Re-run jiji_ads_harvest_cdp.py with a higher max_pages before trusting this scan.")

    gap_doc = json.load(open(GAP, encoding="utf-8"))
    items = gap_doc["items"]

    counts = {"live": 0, "review": 0, "unlisted": 0}
    review_rows = []
    today = datetime.date.today().isoformat()

    for it in items:
        # Remember what we previously believed - a prior "listed" flag with a date is
        # evidence from a human (H confirmed it) and must never be silently wiped by a
        # matcher miss. Regression guard added 16/11/26 after the Blyss typo incident.
        prior_listed = bool(it.get("listed"))
        prior_ts = it.get("listed_on_jiji")

        verdict, score, hit, how = match_one(it["name"], live_norm, live_titles, alias_map)

        if verdict == "unlisted" and prior_listed and prior_ts:
            verdict = "review"
            how = "REGRESSION: was marked listed " + str(prior_ts) + ", matcher found nothing"

        counts[verdict] += 1
        it["match_verdict"] = verdict
        it["match_score"] = round(score, 3)
        it["match_how"] = how
        it["match_title"] = hit
        if verdict == "live":
            it["listed"] = True
            it["listed_on_jiji"] = it.get("listed_on_jiji") or today
        elif verdict == "review":
            it["listed"] = prior_listed
            it["listed_on_jiji"] = prior_ts
        else:
            it["listed"] = False
            it["listed_on_jiji"] = None
        if verdict == "review":
            review_rows.append({"inventory_name": it["name"], "best_live_candidate": hit,
                                "score": round(score, 3), "how": how,
                                "inventory_price": it.get("price"), "stock": it.get("stock")})

    gap_doc["items"] = items
    gap_doc["generated"] = datetime.datetime.now().isoformat(timespec="seconds")
    gap_doc["scan_source"] = os.path.basename(LIVE)
    gap_doc["live_ads_scraped"] = live_doc.get("scraped")
    gap_doc["total_gap"] = counts["unlisted"]
    json.dump(gap_doc, open(GAP, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
               "note": "ambiguous matches - a human must confirm live vs unlisted",
               "rows": review_rows}, open(REVIEW, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    aliases["updated"] = today
    json.dump(aliases, open(ALIASES, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    open_items = [i for i in items if not i["listed"]]
    for i in open_items:
        i["pot"] = float(i.get("margin") or 0) * float(i.get("stock") or 0)
    known = [i for i in open_items if float(i.get("cost") or 0) > 0]
    unknown = [i for i in open_items if not float(i.get("cost") or 0)]
    known.sort(key=lambda x: -x["pot"])
    unknown.sort(key=lambda x: -float(x.get("stock") or 0))

    print(f"\nVERDICTS  live={counts['live']}  review={counts['review']}  unlisted={counts['unlisted']}")
    print(f"still unlisted: {len(open_items)}  (known COGS {len(known)} / COGS missing {len(unknown)})")
    print(f"verifiable potential profit remaining: GH₵ {sum(i['pot'] for i in known):,.0f}")
    print(f"review file: {REVIEW}")

    # ---- markdown ----
    def row(i, n):
        return (f"| {n} | **{i['name']}** | {int(i.get('price') or 0):,} | "
                f"{int(i.get('cost') or 0):,} | {int(i.get('margin') or 0):,} | "
                f"{int(i.get('stock') or 0)} | {int(i['pot']):,} |")

    md = [f"# 2Real — Christmas Priority List (re-scan {today})",
          "",
          f"_Source: {len(ads)} live Jiji ads scraped {live_doc.get('scraped')}. "
          f"Matched by model code + brand/spec + fuzzy + alias map._",
          "",
          f"| Verdict | Count |", "|---|---|",
          f"| Confirmed LIVE on Jiji (already posted) | {counts['live']} |",
          f"| Ambiguous — needs your eye | {counts['review']} |",
          f"| **Genuinely unlisted** | **{counts['unlisted']}** |",
          "",
          f"**Verifiable profit still unlisted: GH₵ {sum(i['pot'] for i in known):,.0f}** "
          f"(plus {len(unknown)} items with no COGS recorded)",
          "",
          "## Tier A — unlisted, known COGS, ranked by profit potential (margin × stock)",
          "",
          "| # | Item | Price | Cost | Margin | Stk | Potential |", "|---|---|---|---|---|---|---|"]
    md += [row(i, n) for n, i in enumerate(known[:25], 1)]
    md += ["", "## Tier B — COGS missing, margin NOT verifiable", "",
           "Price-only ranking. Backfill cost before treating these as priority.", "",
           "| Item | Price | Stk |", "|---|---|---|"]
    md += [f"| {i['name']} | {int(i.get('price') or 0):,} | {int(i.get('stock') or 0)} |" for i in unknown[:20]]
    if review_rows:
        md += ["", "## Needs your eye (ambiguous match)", "",
               "| Inventory name | Closest live ad | Score | How |", "|---|---|---|---|"]
        md += [f"| {r['inventory_name']} | {r['best_live_candidate']} | {r['score']} | {r['how']} |"
               for r in review_rows[:25]]
    md += ["", "---", "",
           "**Rules this scan now follows:** (1) reads the FRESH harvest, never a stale snapshot; "
           "(2) refuses to trust a harvest whose length looks page-capped; "
           "(3) bridges renamed titles via the alias map; "
           "(4) anything ambiguous goes to review instead of being silently dropped."]
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(md))
    print("wrote:", OUT_MD)

    if "--review" in sys.argv:
        for r in review_rows:
            print(f"  ? {r['inventory_name'][:52]:52} ~ {str(r['best_live_candidate'])[:46]} ({r['score']})")


if __name__ == "__main__":
    main()

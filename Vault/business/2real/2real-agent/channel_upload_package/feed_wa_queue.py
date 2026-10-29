#!/usr/bin/env python3
"""feed_wa_queue.py — feed new items into wa_queue.json from the FB/Jiji source.

Scenario (22/10/26): the WA catalogue queue has drained (0 unposted — all posted),
but FB next50 still has unposted items, so promote_batch2.py refuses to run (its
rule: only promote when BOTH queues empty). H wants WA fed fresh regardless.

This ADDITIVE feeder:
1. Reads source items from next50_batch2.json (the Jiji/FB-pending queue) first,
   then next50.json as fallback — both carry jiji_id/title/price/condition.
2. Front-loads PROVEN sellers (Gorilla > Berkey > Bosch) via meta_feed_full.csv.
3. Dedupes EVERY item against wa_catalog_posted.json (already posted) AND
   wa_catalog_existing.json (already in catalogue) AND current wa_queue.json.
4. Prices at +20% rounded to 10, same as promote_batch2 (the WA premium).
5. Appends fresh items to wa_queue.json (preserving existing unposted entries).
6. Photos: points at photos/<jiji_id>.jpg; downloads if missing (from meta_feed).

FAIL-SAFE: never sends. Only edits wa_queue.json. Backs it up first.
Usage: python feed_wa_queue.py [--max 15] [--dump N]
"""
import json, os, re, csv, sys, shutil, urllib.request, datetime
from collections import Counter

PKG = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
BACKUP = os.path.join(PKG, 'wa_queue.json.bak_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))

# Proven-seller front-load (same as promote_batch2)
GORILLA_WANT = ('grab adhesive', 'super glue', 'contact adhesive', 'epoxy', 'mounting tape', 'glue original', 'wood glue')
PROVEN_WANT = {'berkey': ('berkey',), 'bosch': ('bosch', 'bosch drill', 'bosch jigsaw', 'bosch sander', 'bosch paint', 'bosch pst', 'bosch gbh'), 'gorilla': GORILLA_WANT}
PROVEN_SCORE = {'gorilla': 999.0, 'berkey': 990.0, 'bosch': 980.0}
_SCRAP_PRICE = re.compile(r'[^0-9.]')

# WhatsApp catalogue collection rules — loaded once at feed time so every fed item
# is collected immediately (source category_name/category is often empty).
wa_rules = []
_rules_path = os.path.join(PKG, 'wa_collections_rules.json')
if os.path.exists(_rules_path):
    try:
        wa_rules = json.load(open(_rules_path, encoding='utf-8'))['rules']
    except Exception:
        wa_rules = []


def jload(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return []


def jsave(p, d):
    tmp = p + '.tmp'
    json.dump(d, open(tmp, 'w', encoding='utf-8'), indent=1)
    os.replace(tmp, p)


def proven_score(item):
    """Return front-load score (higher = earlier) or 0."""
    tl = (item.get('title') or '').lower()
    jid = item.get('jiji_id')
    feed = _feed()
    if jid in feed:
        brand = (feed[jid][3] or '').lower()
    else:
        brand = ''
    best = 0
    for sname, kws in PROVEN_WANT.items():
        if sname == 'gorilla':
            if any(w in tl for w in kws): best = max(best, PROVEN_SCORE['gorilla'])
        else:
            if any(w in tl for w in kws) or (sname in brand): best = max(best, PROVEN_SCORE[sname])
    return best


def _feed():
    """meta_feed_full.csv -> {jiji_id: (title, image_url, price, brand)} for image lookup."""
    feed = os.path.join(PKG, 'meta_feed_full.csv')
    out = {}
    if os.path.exists(feed):
        with open(feed, encoding='utf-8') as f:
            for row in csv.reader(f):
                if len(row) >= 9:
                    try: jid = int(float(row[0]))
                    except (ValueError, TypeError): continue
                    out[jid] = (row[1], row[7], row[5], row[8])
    return out


def assign_collection(title):
    """Assign a WhatsApp catalogue collection from wa_collections_rules.json (first match wins),
    then a judgement SUPPLEMENT for gaps the rules file misses. The source next50 items carry
    category_name/category that is often empty — the catalogue requires a real collection on every
    item, so we self-assign at feed time instead of leaving it to a patch-up pass."""
    tl = title.lower()
    for r in wa_rules:
        if re.search(r['match'], tl):
            return r['collection']
    supplement = (
        ('Hand Tools — Spanners, Sockets & Pliers', ('plane', 'handsaw', 'hand saw', 'hatchet', ' axe ', 'chisel', 'smoothing')),
        ('Garden & Farm', ('shear', 'shears', 'pruner', 'secateur', 'topiary', 'hedge', 'machete', 'scythe')),
        ('Office & B2B', ('headiest', 'headset', 'microphone', ' with mic', 'computer head', 'desk phone')),
        ('Electronics & Audio', ('sound machine', 'white noise', 'loudspeaker', 'speaker system', 'camera', 'webcam', 'router')),
        ('Master Lock and Keysafe', ('disc lock', 'padlock', 'lock box', 'keysafe', 'chain lock', 'bike lock')),
        ('Staples/Nail Guns', ('staple gun', 'tacker', 'nail gun', 'stapler')),
        ('Glue Guns Corded & Cordless', ('glue gun', 'hot glue', 'glue stick gun')),
        ('Power Tools — UK Brand', ('rotary tool', 'dremel', 'multi-tool', 'multi tool', 'impact driver', 'circular saw')),
    )
    for col, kws in supplement:
        if any(k in tl for k in kws):
            return col
    return ''


def classify_condition(title, src_condition):
    """Honest NEW/USED gate at refill time (H's rule: almost nothing is provably new).
    NEW only when the title proves it ('brand new/sealed/new in box') OR the item is a sealed
    consumable (spray/tape/glue/epoxy/adhesive/battery/blade/LEGO/filter). A 'glue gun' or 'staple gun'
    is a POWER TOOL, not a consumable — default it to USED even if 'glue'/'stapl' matches."""
    tl = title.lower()
    provably_new = any(k in tl for k in ('brand new', 'brand-new', 'sealed', 'new in box', 'unopened'))
    consumable = any(k in tl for k in ('spray', 'tape', 'glue', 'epoxy', 'adhesive', 'sealant',
                                        'battery pack', 'blade', 'filter', ' lego', 'lubricant', ' wax ',
                                        ' lego ', 'lego star', 'lego marvel', 'lego harry', 'lego city'))
    if provably_new:
        return 'NEW'
    if consumable and ' gun' not in tl:
        return 'NEW'
    return 'USED'


def norm(t):
    return set(re.sub(r'[^a-z0-9 ]', ' ', t.lower()).split()) - {'ghs','ghc','gh','the','with','and','for','from','uk','new','kit','piece','set'}


def is_dup_title(new_title, existing_titles):
    A = norm(new_title)
    if not A: return False
    for e in existing_titles:
        B = norm(e)
        if A and B and len(A & B) / max(1, min(len(A), len(B))) >= 0.6:
            return True
    return False


def ensure_photo(jid):
    """Ensure the WA photo file exists; download from meta_feed if missing."""
    photo = os.path.join(PKG, 'photos', '%d.jpg' % jid)
    if os.path.exists(photo) and os.path.getsize(photo) > 1000:
        return photo
    feed = _feed()
    if jid not in feed: return photo
    img = feed[jid][1]
    if not img: return photo
    try:
        req = urllib.request.Request(img, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r, open(photo, 'wb') as f:
            f.write(r.read())
    except Exception as e:
        print('  photo dl fail %d: %s' % (jid, e))
    return photo


def main():
    cap = int(sys.argv[sys.argv.index('--max')+1]) if '--max' in sys.argv else 15

    # ── dedup sets ──
    wa_posted = set(jload(os.path.join(PKG, 'wa_catalog_posted.json')))
    wa_existing = [x for x in jload(os.path.join(PKG, 'wa_catalog_existing.json')) if isinstance(x, str)]
    current_wa = jload(os.path.join(PKG, 'wa_queue.json'))
    in_queue = {x.get('jiji_id') for x in current_wa}
    done_ids = set(wa_posted) | in_queue

    # ── source: batch2 first (Jiji-pending surface), next50 fallback ──
    src_items = []
    b2 = os.path.join(PKG, 'next50_batch2.json')
    n50 = os.path.join(PKG, 'next50.json')
    if os.path.exists(b2): src_items += jload(b2)
    if os.path.exists(n50): src_items += jload(n50)

    # dedupe source by jiji_id, keep higher proven score
    by_id = {}
    for it in src_items:
        jid = it.get('jiji_id')
        if not jid: continue
        score = proven_score(it)
        if jid not in by_id or score > by_id[jid][1]:
            by_id[jid] = (it, score)
    deduped = [(it, sc) for it, sc in by_id.values()]

    # exclude already-posted / already-in-queue
    candidates = [(it, sc) for it, sc in deduped if str(it['jiji_id']) not in {str(x) for x in done_ids}]
    # sort by proven score desc, then price desc (premium-first feel)
    candidates.sort(key=lambda x: (-x[1], -(x[0].get('price') or 0)))

    # apply title-dedup against existing catalogue
    fresh = []
    for it, sc in candidates[:cap*3]:  # allow slack for title-dedup drops
        if len(fresh) >= cap: break
        it['jiji_id'] = int(it['jiji_id'])
        price = int(round((it.get('price') or 0) * 1.2 / 10.0) * 10)
        title = re.sub(r'\s+', ' ', it.get('title') or '').strip()
        wa_title = '%s %dgh' % (title, price)
        if is_dup_title(wa_title, wa_existing):
            print('  dup-title skip:', wa_title[:60])
            continue
        photo = ensure_photo(it['jiji_id'])
        title_raw = it.get('title') or ''
        fresh.append({
            'jiji_id': it['jiji_id'],
            'wa_title': wa_title,
            'jiji_price': it.get('price'),
            'wa_price': price,
            'photo': os.path.relpath(photo, PKG),
            'condition': classify_condition(title_raw, it.get('condition')),
            'collection': assign_collection(title_raw) or it.get('category_name') or it.get('category') or '',
            'source': 'feed_wa',
            'score': sc,
        })

    if not fresh:
        print('NO fresh items to feed (all already posted/queued/dup). wa_queue stays %d' % len(current_wa))
        return 0

    # backup + append fresh (proven-first) in FRONT of any existing unposted
    shutil.copy(os.path.join(PKG, 'wa_queue.json'), BACKUP)
    combined = fresh + current_wa
    jsave(os.path.join(PKG, 'wa_queue.json'), combined)

    print('FED WA QUEUE: +%d fresh items -> wa_queue.json (total %d). Backup: %s' % (len(fresh), len(combined), os.path.basename(BACKUP)))
    for f_ in fresh[:cap]:
        print('   [%s%s] %s — GHS %d' % ('★' if f_['score'] else ' ', ' ' if f_['score'] else '', f_['wa_title'][:52], f_['wa_price']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
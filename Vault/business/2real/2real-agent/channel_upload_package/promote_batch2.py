"""Promote next50_batch2.json -> next50.json (FB) and rebuild wa_queue.json (WA premium).

Run when the CURRENT queues are done (FB next50 remaining == 0 AND WA remaining == 0):
    python promote_batch2.py

What it does:
1. Verifies both current queues are actually empty (refuses otherwise).
2. GORILLA-FIRST: prepends top-selling Gorilla SKUs (from meta_feed_full.csv, which has
   jiji_id + image URL + Jiji price) that are NOT yet in fb_posted.json / NOT already in
   the batch, downloading their photos if missing. Score 999 fronts them so they post first.
3. Backs up next50.json -> next50_batch1_done.json (idempotent), copies batch2 -> next50.json.
4. Rebuilds wa_queue.json with premium prices (+20%, round 10) for batch2 items NOT yet
   in wa_catalog_posted.json and not duplicate-titles in wa_catalog_existing.json.
5. Resumes both crons (FB 5128ceaa2c09, WA 18cee69a1011) if paused.
"""
import json, os, re, shutil, subprocess, csv, urllib.request

PKG = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
FB_CRON, WA_CRON = '5128ceaa2c09', '18cee69a1011'
# Top-seller Gorilla SKU patterns (sales-log proven). Front these first.
# Proven-seller front-load patterns (from daily-sales-log / margin history).
# Sales-log proven lines are front-loaded so the posting crons list them first.
#   Gorilla range : 85-90%+ margin, high repeat rate (sales-log proven 8-19 Oct)
#   Berkey        : 2200 sold on £7 cost (96% margin, 19/10/26)
#   Bosch (tools) : 1580 sold on £30 cost, strong walk-in/Jiji (19/10/26 + prior)
GORILLA_WANT = (
    'grab adhesive', 'super glue', 'contact adhesive', 'epoxy',
    'mounting tape', 'glue original', 'wood glue',
)
PROVEN_WANT = {
    # brand keyword -> matched against meta_feed brand column (lower), AND title
    'berkey':  ('berkey',),
    'bosch':   ('bosch', 'bosch drill', 'bosch jigsaw', 'bosch sander', 'bosch paint', 'bosch pst', 'bosch gbh'),
    'gorilla': GORILLA_WANT,
}
# Score for front-loading: higher = posts first
PROVEN_SCORE = {
    'gorilla': 999.0,
    'berkey':  990.0,
    'bosch':   980.0,
}
_GORILLA_URLS = None  # lazy cache of {jiji_id: (title, image, price)} from meta_feed


def _proven_feed():
    """{jiji_id: (title, image_url, price, brand)} for proven-seller rows (Gorilla/Berkey/Bosch), from meta_feed_full.csv."""
    global _GORILLA_URLS
    if _GORILLA_URLS is not None:
        return _GORILLA_URLS
    feed = os.path.join(PKG, 'meta_feed_full.csv')
    out = {}
    if os.path.exists(feed):
        with open(feed, encoding='utf-8') as f:
            for row in csv.reader(f):
                # columns: id, title, desc, condition, status, price, url, image, brand
                if len(row) >= 9:
                    brand = (row[8] or '').lower()
                    title = (row[1] or '').lower()
                    # keep proven-seller brands (gorilla OR berkey OR bosch)
                    if brand in ('gorilla', 'berkey', 'bosch') or any(
                            w in title for w in ('berkey', 'bosch',) + GORILLA_WANT):
                        try:
                            jid = int(float(row[0]))
                        except (ValueError, TypeError):
                            continue
                        out[jid] = (row[1], row[7], row[5], row[8])
    _GORILLA_URLS = out
    return out


def gorilla_front(batch2, fb):
    """Prepend ALL proven-seller SKUs (Gorilla/Berkey/Bosch) not yet posted / not already in batch, with photos.
    Higher proven-score = posts first (Gorilla > Berkey > Bosch)."""
    feed = _proven_feed()
    in_batch = {x['jiji_id'] for x in batch2}
    imgdir = os.path.join(PKG, 'photos')
    os.makedirs(imgdir, exist_ok=True)
    fresh = []
    for jid, (title, image, price, brand) in feed.items():
        if jid in fb or jid in in_batch:
            continue
        tl = title.lower()
        bl = (brand or '').lower()
        score = None
        for sname, kw_tups in PROVEN_WANT.items():
            if sname == 'gorilla':
                if any(w in tl for w in kw_tups):
                    score = PROVEN_SCORE['gorilla']; break
            else:
                # brand match on brand column OR title
                if any(w in tl for w in kw_tups) or (sname in bl):
                    score = PROVEN_SCORE[sname]; break
        if score is None:
            continue
        try:
            px = int(float(re.sub(r'[^0-9.]', '', price)))
        except ValueError:
            continue
        if not image:
            continue
        photo = os.path.join(imgdir, '%d.jpg' % jid)
        if not os.path.exists(photo):
            try:
                req = urllib.request.Request(image, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=30) as r, open(photo, 'wb') as f:
                    f.write(r.read())
            except Exception as e:
                print('  photo dl fail %d: %s' % (jid, e))
                continue
        fresh.append({'jiji_id': jid, 'title': title, 'price': px,
                      'image': image, 'url': 'https://jiji.com.gh', 'score': score})
    return fresh + batch2

def jload(p): return json.load(open(p, encoding='utf-8'))
def jsave(p, d): json.dump(d, open(p, 'w', encoding='utf-8'), indent=1)

def main():
    n50 = jload(PKG + r'\next50.json')
    fb = set(jload(PKG + r'\fb_posted.json'))
    wa = set(jload(PKG + r'\wa_catalog_posted.json'))
    fb_left = [x for x in n50 if x['jiji_id'] not in fb]
    waq = jload(PKG + r'\wa_queue.json')
    wa_left = [x for x in waq if x['jiji_id'] not in wa]
    if fb_left or wa_left:
        print('REFUSE: FB remaining %d, WA remaining %d — promote only when BOTH are 0.' % (len(fb_left), len(wa_left)))
        return
    batch2 = jload(PKG + r'\next50_batch2.json')
    # GORILLA-FIRST: front top-selling Gorilla SKUs (not yet posted / not already in batch)
    batch2 = gorilla_front(batch2, fb)
    jsave(PKG + r'\next50_batch2.json', batch2)  # persist so next50 + wa both see gorilla front
    # DUPLICATE-PREVENTION (H: "avoid at all costs"): drop any item ALREADY in fb_posted.json
    # so the queue never re-queues a posted listing. This is what caused "item 1 is a duplicate".
    pre = len(batch2)
    batch2 = [x for x in batch2 if x['jiji_id'] not in fb]
    dropped = pre - len(batch2)
    if dropped:
        print('  duplicate-prevention: dropped %d already-posted item(s) from the new queue' % dropped)
    jsave(PKG + r'\next50_batch2.json', batch2)  # persist the FILTERED batch so the copy below is clean
    base = shutil.copy(PKG + r'\next50.json', PKG + r'\next50_batch1_done.json') if not os.path.exists(PKG + r'\next50_batch1_done.json') else None
    shutil.copy(PKG + r'\next50_batch2.json', PKG + r'\next50.json')
    # WA premium queue for batch2
    existing = {t.lower() for t in jload(PKG + r'\wa_catalog_existing.json')}
    def norm(t): return re.sub(r'[^a-z0-9 ]', ' ', t.lower())
    def is_dup(t):
        A = set(norm(t).split()) - {'ghs','ghc','gh','the','with','and','for','from','uk','new','kit','piece'}
        for e in existing:
            B = set(norm(e).split()) - {'ghs','ghc','gh','the','with','and','for','from','uk','new','kit','piece'}
            if A and B and len(A & B) / max(1, min(len(A), len(B))) >= 0.6:
                return True
        return False
    q = []
    for x in batch2:
        if x['jiji_id'] in wa:
            continue
        price = int(round((x['price'] or 0) * 1.2 / 10.0) * 10)
        title = re.sub(r'\s+', ' ', x['title']).strip()
        q.append({'jiji_id': x['jiji_id'], 'wa_title': '%s %dgh' % (title, price),
                  'jiji_price': x['price'], 'wa_price': price, 'photo': 'photos/%d.jpg' % x['jiji_id']})
    # drop duplicates against existing catalogue (mark skip by excluding)
    kept = [x for x in q if not is_dup(x['wa_title'])]
    jsave(PKG + r'\wa_queue.json', kept)
    for cron in (FB_CRON, WA_CRON):
        subprocess.run(['hermes', 'cron', 'resume', cron], capture_output=True, text=True)
    print('PROMOTED: FB next50 = %d items | WA premium queue = %d items | crons resumed.' % (len(batch2), len(kept)))

if __name__ == '__main__':
    main()

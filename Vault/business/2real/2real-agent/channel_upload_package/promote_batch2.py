"""Promote next50_batch2.json -> next50.json (FB) and rebuild wa_queue.json (WA premium).

Run when the CURRENT queues are done (FB next50 remaining == 0 AND WA remaining == 0):
    python promote_batch2.py

What it does:
1. Verifies both current queues are actually empty (refuses otherwise).
2. Backs up next50.json -> next50_batch1_done.json (idempotent), copies batch2 -> next50.json.
3. Rebuilds wa_queue.json with premium prices (+20%, round 10) for batch2 items NOT yet
   in wa_catalog_posted.json and not duplicate-titles in wa_catalog_existing.json.
4. Resumes both crons (FB 5128ceaa2c09, WA 18cee69a1011) if paused.
"""
import json, os, re, shutil, subprocess

PKG = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
FB_CRON, WA_CRON = '5128ceaa2c09', '18cee69a1011'

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

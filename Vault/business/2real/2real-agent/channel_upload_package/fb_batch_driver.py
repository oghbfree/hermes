"""Batch driver: posts 3 queue items with keyword-enriched titles + researched specs.
Uses fb_post_run internals (tested flow), 50s sleep between listings."""
import sys, os, json, time
pkg = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0, pkg)
import fb_post_run as R

TITLE_FIX = {
    12706937: ('Stanley Graphite Jacketed Hammer, High-Carbon Steel Head — UK Imported, Quality Checked',
               'Jacketed graphite-core handle, high-carbon polished steel head, shock-absorbing ribbed grip'),
    12729154: ('Norton Clipper Classic 230mm Turbo Diamond Blade Universal Cut — UK Imported, Quality Checked',
               '230mm turbo-segment diamond blade, universal cut: concrete, brick, block & stone'),
    7652303:  ('Darlac Expert Bypass Pruner, SK5 Steel Secateurs 25mm Cut — UK Imported, Quality Checked',
               'SK5 high-carbon steel blade, 25mm cut capacity, slim ergonomic handles, 2-position catch'),
}

orig_find_item = R.find_item
def find_item_enriched(jid):
    it = orig_find_item(jid)
    if it and int(jid) in TITLE_FIX:
        t, spec = TITLE_FIX[int(jid)]
        assert len(t) <= 95, (len(t), t)
        it = dict(it); it['title'] = t
    return it
R.find_item = find_item_enriched

JIDS = [12706937, 12729154, 7652303]
out = []
for i, jid in enumerate(JIDS):
    rc, res = R._post_one(jid, TITLE_FIX[jid][1])
    out.append((jid, rc, res))
    if i < len(JIDS) - 1 and rc == 0:
        print('sleeping 50s (anti-velocity)...'); time.sleep(50)
    if rc != 0:
        break
print('RESULTS:', out)

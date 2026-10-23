"""Runs one FB Marketplace posting via the CDP harness (fb_post_lib flow + photo-preview check).

Usage: python fb_post_run.py <jiji_id>  -> posts that item if not in fb_posted.json.
"""
import sys, os, json, time, base64
import subprocess

pkg = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0, pkg)
import cdp_harness as C

G = {'js': C.js, 'goto_url': C.goto_url, 'wait_for_load': C.wait_for_load,
     'click_at_xy': C.click_at_xy, 'time': time, 'json': json, 'base64': base64, 'os': os}
src = open(os.path.join(pkg, 'fb_post_lib.py'), encoding='utf-8').read()
src = src.replace("assert 'js' in globals(), 'run via exec in harness main'", "")
exec(src, G)

def is_posted(jid):
    try:
        return jid in json.load(open(os.path.join(pkg, 'fb_posted.json')))
    except Exception:
        return False

def add_posted(jid):
    p = os.path.join(pkg, 'fb_posted.json')
    arr = json.load(open(p))
    if jid not in arr:
        arr.append(jid)
        json.dump(arr, open(p, 'w'))

def find_item(jid):
    for f in ('next50.json', 'next50_batch2.json', 'next50_batch1_done.json', 'next50_batch2_pregorilla.json'):
        try:
            arr = json.load(open(os.path.join(pkg, f)))
            for x in arr:
                if str(x['jiji_id']) == str(jid):
                    return x
        except Exception:
            pass
    return None

UPLOAD_OK = """(() => {
  const imgs=[...document.querySelectorAll('[aria-label="Photo thumbnail"], img[src*="scontent"], div[role=dialog] img')].filter(e=>e.offsetParent!==null);
  return imgs.length>0;
})()"""

_PUBLISHED_URL = ''  # module-level; set by post_one_checked on successful publish

def _norm_title(s):
    return ''.join(ch for ch in str(s or '').lower() if ch.isalnum())


def _js_find_marketplace_anchor(full_norm, core_norm):
    """JS: find an /marketplace/item/ anchor whose card text matches the listing.
    Exact full-title match wins; partial core-title match only when unambiguous
    (e.g. two 'Belkin BoostCharge' variants must NOT be confused)."""
    return """(() => {
      const full=%s, core=%s;
      const as=[...document.querySelectorAll('a[href*="/marketplace/item/"]')].filter(e=>e.offsetParent!==null);
      const norm=s=>(s||'').toLowerCase().replace(/[^a-z0-9]/g,'');
      let fullHit=null, coreHits=[];
      for (const a of as) {
        const t=norm(a.innerText);
        if (full && full.length>=14 && t.includes(full)) { fullHit=a; break; }
        if (core && core.length>=14 && t.includes(core)) coreHits.push(a);
      }
      if (fullHit) return fullHit.href.split('?')[0];
      if (coreHits.length===1) return coreHits[0].href.split('?')[0];
      return '';
    })()""" % (json.dumps(full_norm), json.dumps(core_norm))


def _capture_published_url(title):
    """Best-effort capture of the just-published listing URL (for group sharing).
    1) wait ~14s for FB's post-publish redirect to /marketplace/item/
    2) scan the current DOM for a live-listing link showing our title
    3) fallback: selling page, TITLE-anchored lookup (never the first-anchor guess)
    Returns '' when none/ambiguous — the share is skipped, the listing stays live."""
    full_norm = _norm_title(title)
    core_norm = _norm_title((title or '').split('\u2014')[0])[:32]
    try:
        for _ in range(7):
            u = C.js('location.href') or ''
            if '/marketplace/item/' in u:
                return u.split('?')[0]
            time.sleep(2)
    except Exception:
        pass
    try:
        lu = C.js(_js_find_marketplace_anchor(full_norm, core_norm))
        if lu:
            return lu
    except Exception:
        pass
    try:
        C.goto_url('https://www.facebook.com/marketplace/you/selling')
        time.sleep(8)
        for _ in range(3):
            lu = C.js(_js_find_marketplace_anchor(full_norm, core_norm))
            if lu:
                return lu
            time.sleep(3)
    except Exception:
        pass
    return ''

def post_one_checked(title, price, photo, category, desc, condition="New"):
    global _PUBLISHED_URL
    _PUBLISHED_URL = ''
    C.goto_url('https://www.facebook.com/marketplace/create/item')
    time.sleep(6)
    # choose 'Item for sale' if shown
    for k in range(4):
        pos = C.js(G['pick_visible']('Item for sale'))
        if pos:
            p = json.loads(pos)
            C.click_at_xy(int(p['x']), int(p['y']))
            time.sleep(3)
            break
        if C.js("!!document.querySelector('input[type=file]')") is True:
            break
        time.sleep(2)
    if C.js("!!document.querySelector('input[type=file]')") is not True:
        return 'FAIL no file input'
    b64 = base64.b64encode(open(photo, 'rb').read()).decode()
    desc_js = json.dumps(desc)
    r = C.js_async("""(async () => {
      const inp=[...document.querySelectorAll('input[type=file]')].find(f=>f.accept.includes('image'));
      if(!inp) return 'retry';
      const bin=atob('%s'); const bytes=new Uint8Array(bin.length);
      for(let i=0;i<bin.length;i++)bytes[i]=bin.charCodeAt(i);
      const dt=new DataTransfer(); dt.items.add(new File([bytes],'photo.jpg',{type:'image/jpeg'}));
      inp.files=dt.files; inp.dispatchEvent(new Event('change',{bubbles:true}));
      await new Promise(r=>setTimeout(r,3500));
      const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
      const title=%s; const pricestr='%s';
      for(let k=0;k<12;k++){
        const tis=[...document.querySelectorAll('input[type=text]')].filter(i=>i.offsetParent!==null);
        if(tis.length>=2){
          setter.call(tis[0],title); tis[0].dispatchEvent(new Event('input',{bubbles:true}));
          setter.call(tis[1],pricestr); tis[1].dispatchEvent(new Event('input',{bubbles:true}));
          return 'fields set';
        }
        await new Promise(r=>setTimeout(r,600));
      }
      return 'no text inputs';
    })()""" % (b64, json.dumps(title[:100]), str(price)), timeout=90)
    if r != 'fields set':
        return 'FAIL fields: %r' % r
    time.sleep(2)
    if C.js(UPLOAD_OK) is not True:
        return 'FAIL no photo preview'
    time.sleep(1)
    if not G['open_ctrl']('Category'):
        if not G['open_category']():
            return 'FAIL cat open'
    ok = False
    for lab in (category, 'Miscellaneous', 'Tools'):
        if G['pick_leaf'](lab):
            ok = True
            break
    if not ok:
        return 'FAIL cat opt'
    time.sleep(2)
    rc = G['set_condition'](condition)
    if rc != 'OK':
        return rc
    C.js("""(() => {
      const ta=document.querySelector('textarea');
      if(!ta) return;
      const ts=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;
      ts.call(ta,%s); ta.dispatchEvent(new Event('input',{bubbles:true}));
    })()""" % desc_js)
    time.sleep(1)
    for k in range(10):
        pos = C.js(G['NEXT_PUB'])
        if pos:
            p = json.loads(pos)
            C.js("""(() => { const b=[...document.querySelectorAll('div[role=button],button')].filter(e=>e.offsetParent!==null).find(e=>(e.textContent||'').trim()===%s); if(!b) return 'no'; const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window}); ['mousedown','mouseup','click'].forEach(t=>b.dispatchEvent(ME(t))); return 'ok'; })()""" % json.dumps(p.get('label','')))
            time.sleep(2.5)
            if p.get('label') == 'Publish':
                time.sleep(4)
                # capture the just-published listing URL for group sharing
                _PUBLISHED_URL = _capture_published_url(title)
                time.sleep(1)
                return 'PUBLISHED'
        else:
            time.sleep(1)
    return 'FAIL publish'

def find_jiji_details(jid):
    """Look up the item's Jiji listing to get accurate condition + spec details."""
    jf = os.path.join(pkg, '..', 'jiji_listings_full.json')
    try:
        with open(jf, encoding='utf-8') as f:
            raw = json.load(f)
        items = raw if isinstance(raw, list) else raw.get('listings', raw.get('items', []))
        qitem = find_item(jid)
        tl = ((qitem or {}).get('title') or '').strip().lower()
        for li in items:
            # match by numeric id if present, else by normalized title
            lid = li.get('id') or li.get('jiji_id')
            if lid is not None:
                try:
                    if int(lid) == int(jid):
                        return li.get('details', ''), str(li.get('title', ''))
                except (ValueError, TypeError):
                    pass
            if tl and str(li.get('title', '')).strip().lower() == tl:
                return li.get('details', ''), str(li.get('title', ''))
        # looser title match (prefix on first 40 chars)
        if tl:
            for li in items:
                if str(li.get('title', '')).strip().lower()[:40] == tl[:40]:
                    return li.get('details', ''), str(li.get('title', ''))
        return '', ''
    except Exception:
        return '', ''

def enrich_title(t):
    if 'Imported' in t:
        return t
    suffix = ' — UK Imported, Quality Checked'
    if len(t) + len(suffix) <= 95:
        return t + suffix
    return t[:95]

def share_groups_after_publish(jid, item_url, title=''):
    """Share the freshly-published listing into H's buy/sell groups (best-effort).
    Never fails the post — the listing is already live.
    If no URL was captured, pass LOOKUP:<title> so fb_share_groups can resolve
    the fresh listing URL from the selling page itself (title-anchored)."""
    if os.environ.get('FB_SHARE_GROUPS', '').strip().lower() in ('0', 'off', 'no', 'false'):
        print('GROUP-SHARE disabled via FB_SHARE_GROUPS=0 — listing stays Marketplace-only')
        return
    if not item_url and title:
        item_url = 'LOOKUP:' + title
    if not item_url or not item_url.strip():
        print('GROUP-SHARE skipped (no listing url captured for', jid, ')')
        return
    try:
        py = r'C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe'
        r = subprocess.run(
            [py, os.path.join(pkg, 'fb_share_groups.py'), item_url],
            capture_output=True, text=True, timeout=240, cwd=pkg,
            env={**os.environ, 'FB_SHARE_GROUPS': '1'})
        print('GROUP-SHARE', jid, '->', (r.stdout or r.stderr).replace('\n', ' ')[:300])
    except Exception as e:
        print('GROUP-SHARE EXC', jid, ':', repr(e))


def _post_one(jid, researched=""):
    if not researched:
        try:
            specs = json.load(open(os.path.join(pkg, 'fb_post_specs.json'), encoding='utf-8'))
            researched = specs.get(str(jid), '')
        except Exception:
            researched = ''
    """Post a single item, returning (exit_code, result). One CDP session stays
    alive across calls in batch mode (persistent connection = no reconnect overhead)."""
    if is_posted(jid):
        print('ALREADY POSTED', jid); return 0, 'skipped'
    # Belt-and-suspenders: unified cross-channel registry (Obsidian-backed master)
    try:
        sys.path.insert(0, os.path.join(pkg, '..'))
        from channel_dedup import Registry
        if Registry().posted_anywhere(jid):
            print('ALREADY IN MASTER REGISTRY', jid); return 0, 'skipped'
    except Exception:
        pass  # registry unreadable -> rely on local fb_posted.json
    item = find_item(jid)
    if not item:
        print('NOT IN QUEUE', jid); return 1, 'no_item'
    title = enrich_title(item['title'])
    price = item['price']
    src_photo = os.path.join(pkg, 'photos', '%d.jpg' % jid)
    if not os.path.exists(src_photo):
        print('NO PHOTO', jid); return 1, 'no_photo'
    dst_photo = src_photo[:-4] + '_v%d.jpg' % jid
    varied = G['vary_photo'](src_photo, dst_photo)
    tlow = title.lower()
    if any(w in tlow for w in ('tp-link', 'defender', 'printer', 'laptop', 'monitor', 'router', 'mercusys', 'gps', 'apple tv', 'acer', 'mouse', 'intercom', 'camera', 'kinect', 'wii', 'nintendo', 'xbox', 'playstation', 'synthesizer', 'hi-fi', 'hifi', 'stereo', 'mac mini', 'macmini')):
        category = 'Electronics & computers'
    elif 'lego' in tlow or 'toy' in tlow:
        category = 'Toys'
    elif any(w in tlow for w in ('tequila', 'shower rail', 'juicer', 'barbecue')):
        category = 'Miscellaneous'
    else:
        category = 'Tools'
    # Accurate condition + specs from the Jiji listing (source of truth)
    details, jiji_title = find_jiji_details(jid)
    # 17 Oct 26 H rule: queue 'condition' field is authoritative when present;
    # fall back to title/details detection only for legacy items without it.
    condition = (item.get('condition') or G['detect_condition'](jiji_title or title, details))
    desc = G['make_desc'](title, details=details, condition=condition, spec=researched)
    print('posting', jid, '|', title, '|', price, '| cat:', category, '| cond:', condition, '| photo:', varied)
    print('desc:', repr(desc[:120]), '...')
    for attempt in range(3):
        try:
            rc = post_one_checked(title, price, varied, category, desc, condition)
        except Exception as e:
            rc = 'FAIL exc: %r' % e
        print('attempt', attempt, '->', rc)
        if rc == 'PUBLISHED':
            add_posted(jid)
            try:
                sys.path.insert(0, os.path.join(pkg, '..'))
                from channel_dedup import Registry
                Registry().mark_fb_posted(jid)
            except Exception:
                pass
            print('LOGGED', jid)
            share_groups_after_publish(jid, _PUBLISHED_URL, title)
            return 0, 'published'
        if rc in ('FAIL no photo preview', 'FAIL fields: %r', 'FAIL fields: \'retry\''):
            pass
        time.sleep(8)
    print('GAVE UP', jid)
    return 1, 'gave_up'


def main():
    # Batch mode: python fb_post_run.py <jid1> [jid2 jid3 ...] — posts all in ONE
    # browser session (persistent CDP connection), far faster than reconnect-per-item.
    jids = [int(a) for a in sys.argv[1:] if a.strip().isdigit() and not a.strip().startswith('http')]
    researched = " ".join(a for a in sys.argv[1:] if not a.strip().isdigit())
    if not jids:
        print('usage: fb_post_run.py <jid> [jid2 ...]'); return 2
    results = []
    for jid in jids:
        rc, res = _post_one(jid, researched)
        results.append((jid, rc, res))
        if rc != 0:
            break  # failed item ends the batch (matches cron run-end rule)
        if len(results) < len(jids):
            time.sleep(50)  # anti-velocity pause between listings
    print('\nBATCH SUMMARY:')
    for jid, rc, res in results:
        print(f'  {jid}: {res}')
    ok = all(rc == 0 for _, rc, _ in results)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())

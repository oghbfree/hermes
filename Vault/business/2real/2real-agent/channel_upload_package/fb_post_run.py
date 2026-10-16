"""Runs one FB Marketplace posting via the CDP harness (fb_post_lib flow + photo-preview check).

Usage: python fb_post_run.py <jiji_id>  -> posts that item if not in fb_posted.json.
"""
import sys, os, json, time, base64

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
    for f in ('next50.json', 'next50_batch2.json', 'next50_batch1_done.json'):
        try:
            arr = json.load(open(os.path.join(pkg, f)))
            for x in arr:
                if x['jiji_id'] == jid:
                    return x
        except Exception:
            pass
    return None

UPLOAD_OK = """(() => {
  const imgs=[...document.querySelectorAll('[aria-label="Photo thumbnail"], img[src*="scontent"], div[role=dialog] img')].filter(e=>e.offsetParent!==null);
  return imgs.length>0;
})()"""

def post_one_checked(title, price, photo, category, desc, condition="New"):
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
                time.sleep(2)
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
        tl = (jiji_title or '').strip().lower()
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
    category = 'Electronics & computers' if any(w in title.lower() for w in ('tp-link', 'defender')) else 'Tools'
    # Accurate condition + specs from the Jiji listing (source of truth)
    details, jiji_title = find_jiji_details(jid)
    condition = G['detect_condition'](jiji_title or title, details)
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

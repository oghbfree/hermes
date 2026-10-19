
"""Browser-mode posting: fb_post_lib exec'd against Hermes browser helpers.
Globals required: js, goto_url, click_at_xy (injected)."""
import sys, os, json, time, base64
pkg = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0, pkg)
sys.path.insert(0, os.path.dirname(pkg))
G = {'js': js, 'goto_url': goto_url, 'wait_for_load': wait_for_load,
     'click_at_xy': click_at_xy, 'time': time, 'json': json, 'base64': base64, 'os': os}
src = open(os.path.join(pkg, 'fb_post_lib.py'), encoding='utf-8').read()
src = src.replace("assert 'js' in globals(), 'run via exec in harness main'", "")
exec(src, G)

def is_posted(jid):
    return str(jid) in [str(x) for x in json.load(open(os.path.join(pkg,'fb_posted.json')))]

def add_posted(jid):
    p = os.path.join(pkg, 'fb_posted.json')
    arr = json.load(open(p))
    if jid not in arr:
        arr.append(jid); json.dump(arr, open(p,'w'))

def find_item(jid):
    for f in ('next50.json','next50_batch2.json','next50_batch1_done.json','next50_batch2_pregorilla.json'):
        try:
            for x in json.load(open(os.path.join(pkg,f))):
                if str(x['jiji_id'])==str(jid): return x
        except Exception: pass
    return None

def find_jiji_details(jid):
    jf = os.path.join(pkg,'..','jiji_listings_full.json')
    try:
        raw = json.load(open(jf, encoding='utf-8'))
        items = raw if isinstance(raw,list) else raw.get('listings', raw.get('items', []))
        q = find_item(jid); tl = ((q or {}).get('title') or '').strip().lower()
        for li in items:
            lid = li.get('id') or li.get('jiji_id')
            if lid is not None:
                try:
                    if int(lid)==int(jid): return li.get('details',''), str(li.get('title',''))
                except (ValueError,TypeError): pass
            if tl and str(li.get('title','')).strip().lower()==tl:
                return li.get('details',''), str(li.get('title',''))
        if tl:
            for li in items:
                if str(li.get('title','')).strip().lower()[:40]==tl[:40]:
                    return li.get('details',''), str(li.get('title',''))
    except Exception: pass
    return '', ''

def enrich_title(t):
    if 'Imported' in t or 'Quality Checked' in t: return t
    suffix = ' — UK Imported, Quality Checked'
    return t+suffix if len(t)+len(suffix)<=95 else t[:95]

UPLOAD_OK = """(() => {
  const imgs=[...document.querySelectorAll('[aria-label="Photo thumbnail"], img[src*="scontent"], div[role=dialog] img')].filter(e=>e.offsetParent!==null);
  return imgs.length>0;
})()"""

def post_one_checked(title, price, photo, category, desc, condition="New"):
    goto_url('https://www.facebook.com/marketplace/create/item')
    time.sleep(6)
    for k in range(4):
        pos = G['js'](G['pick_visible']('Item for sale'))
        if pos:
            p = json.loads(pos); click_at_xy(int(p['x']), int(p['y'])); time.sleep(3); break
        if G['js']("!!document.querySelector('input[type=file]')") is True: break
        time.sleep(2)
    if G['js']("!!document.querySelector('input[type=file]')") is not True:
        return 'FAIL no file input'
    # Photo via CDP DOM.setFileInputFiles (base64 JS injection hits chunk limit)
    desc_js = json.dumps(desc)
    doc = cdp('DOM.getDocument')
    root = doc['root']['nodeId']
    q = cdp('DOM.querySelector', nodeId=root, selector='input[type=file]')
    nid = q.get('nodeId')
    if not nid:
        return 'FAIL no file input node'
    cdp('DOM.setFileInputFiles', files=[photo], nodeId=nid)
    time.sleep(3.5)
    r = js("""(async () => {
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
    })()""" % (json.dumps(title[:100]), str(price)))
    if r != 'fields set':
        return 'FAIL fields: %r' % r
    time.sleep(2)
    if G['js'](UPLOAD_OK) is not True:
        return 'FAIL no photo preview'
    time.sleep(1)
    if not G['open_ctrl']('Category'):
        if not G['open_category']():
            return 'FAIL cat open'
    ok = False
    for lab in (category, 'Miscellaneous', 'Tools'):
        if G['pick_leaf'](lab): ok=True; break
    if not ok: return 'FAIL cat opt'
    time.sleep(2)
    rc = G['set_condition'](condition)
    if rc != 'OK': return rc
    G['js']("""(() => {
      const ta=document.querySelector('textarea');
      if(!ta) return;
      const ts=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;
      ts.call(ta,%s); ta.dispatchEvent(new Event('input',{bubbles:true}));
    })()""" % desc_js)
    time.sleep(1)
    for k in range(10):
        pos = G['js'](G['NEXT_PUB'])
        if pos:
            p = json.loads(pos)
            G['js']("""(() => { const b=[...document.querySelectorAll('div[role=button],button')].filter(e=>e.offsetParent!==null).find(e=>(e.textContent||'').trim()===%s); if(!b) return 'no'; const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window}); ['mousedown','mouseup','click'].forEach(t=>b.dispatchEvent(ME(t))); return 'ok'; })()""" % json.dumps(p.get('label','')))
            time.sleep(2.5)
            if p.get('label') == 'Publish':
                time.sleep(2); return 'PUBLISHED'
        else:
            time.sleep(1)
    return 'FAIL publish'

def run_item(jid, researched=''):
    if is_posted(jid):
        return 'ALREADY POSTED'
    try:
        from channel_dedup import Registry
        if Registry().posted_anywhere(jid): return 'ALREADY IN MASTER REGISTRY'
    except Exception as e:
        pass
    item = find_item(jid)
    if not item: return 'NOT IN QUEUE'
    title = enrich_title(item['title']); price = item['price']
    src_photo = os.path.join(pkg,'photos','%d.jpg' % jid)
    if not os.path.exists(src_photo): return 'NO PHOTO'
    dst_photo = src_photo[:-4] + '_v%d.jpg' % jid
    varied = G['vary_photo'](src_photo, dst_photo)
    tlow = title.lower()
    if any(w in tlow for w in ('tp-link','defender','printer','laptop','monitor','router','mercusys','gps','apple tv','acer','mouse','intercom','camera','kinect','wii','nintendo','xbox','playstation','synthesizer','hi-fi','hifi','stereo','mac mini','macmini','speaker','headset','microphone','gimbal','smartwatch')):
        category = 'Electronics & computers'
    elif 'lego' in tlow or 'toy' in tlow: category = 'Toys'
    elif any(w in tlow for w in ('tequila','shower rail','juicer','barbecue')): category = 'Miscellaneous'
    else: category = 'Tools'
    details, jtitle = find_jiji_details(jid)
    condition = (item.get('condition') or G['detect_condition'](jtitle or title, details))
    desc = G['make_desc'](title, details=details, condition=condition, spec=researched)
    print('posting', jid, '|', title, '|', price, '| cat:', category, '| cond:', condition)
    for attempt in range(3):
        try:
            rc = post_one_checked(title, price, varied, category, desc, condition)
        except Exception as e:
            rc = 'FAIL exc: %r' % e
        print('attempt', attempt, '->', rc)
        if rc == 'PUBLISHED':
            add_posted(jid)
            try:
                from channel_dedup import Registry
                Registry().mark_fb_posted(jid)
            except Exception as e:
                print('registry mark err:', e)
            return 'PUBLISHED'
        time.sleep(8)
    return 'GAVE UP'

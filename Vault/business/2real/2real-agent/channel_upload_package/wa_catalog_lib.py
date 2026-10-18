# WhatsApp Web Catalogue posting library — PROVEN 12 Oct 26 (verified end-to-end:
# item saved, image replaced via Edit, "Item saved" toast + under-review state).
# Run via exec() inside browser session 'jiji-shop' (same session as FB posting).
# Requires: web.whatsapp.com already logged in (persistent session, no QR).
import time, base64, json, json as J
assert 'js' in globals(), 'run via exec in browser harness main'
pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'

WA_OPEN_TOOLS = """(() => {
  const t=[...document.querySelectorAll('[aria-label=Tools],[title=Tools]')].filter(e=>e.offsetParent!==null)[0];
  if(!t) return 'noTools';
  const rc=t.getBoundingClientRect();
  const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2});
  ['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev)));
  return 'ok';
})()"""

WA_OPEN_CATALOGUE = """(() => {
  const c=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Catalogue'&&e.children.length===0)[0];
  if(!c) return 'noCat';
  const t=c.closest('[role=button],[tabindex],li')||c.parentElement;
  const rc=t.getBoundingClientRect();
  const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2});
  ['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev)));
  return 'ok';
})()"""

WA_ADD_ITEM_CARD = """(() => {
  const c=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Add new item'&&e.children.length===0)[0];
  if(!c) return 'gone';
  const t=c.parentElement.parentElement;
  const rc=t.getBoundingClientRect();
  if(rc.y<10||rc.y>innerHeight-10) t.scrollIntoView({block:'center'});
  const rc2=t.getBoundingClientRect();
  return JSON.stringify({x:rc2.x+rc2.width/2,y:rc2.y+rc2.height/2});
})()"""

def wa_trusted_click(x, y):
    cdp('Input.dispatchMouseEvent', type='mousePressed', x=int(x), y=int(y), button='left', clickCount=1)
    cdp('Input.dispatchMouseEvent', type='mouseReleased', x=int(x), y=int(y), button='left', clickCount=1)

def wa_drawer_open():
    return js("(() => (document.body.innerText||'').includes('Add images'))()") is True

def wa_fill_fields(title, desc, photo_path):
    """Fill Name + Description (contenteditable via execCommand) + upload image.
    NOTE: image upload is delayed in UI; country step confirms it visually."""
    b64=base64.b64encode(open(photo_path,'rb').read()).decode()
    r=js("""(async () => {
      const ed=[...document.querySelectorAll('div[contenteditable=true]')].filter(e=>e.offsetParent!==null);
      const name=ed.find(e=>(e.getAttribute('aria-label')||'')==='Name');
      const desc=ed.find(e=>(e.getAttribute('aria-label')||'')==='Description');
      if(!name) return 'noName';
      name.focus(); document.execCommand('insertText', false, %s);
      await new Promise(r=>setTimeout(r,400));
      if(desc){ desc.focus(); document.execCommand('insertText', false, %s); }
      await new Promise(r=>setTimeout(r,400));
      const inp=[...document.querySelectorAll('input[type=file]')].find(f=>f.accept&&f.accept.includes('image'));
      if(!inp) return 'nofile';
      const bin=atob('%s'); const bytes=new Uint8Array(bin.length);
      for(let i=0;i<bin.length;i++)bytes[i]=bin.charCodeAt(i);
      const dt=new DataTransfer(); dt.items.add(new File([bytes],'photo.jpg',{type:'image/jpeg'}));
      inp.files=dt.files; inp.dispatchEvent(new Event('change',{bubbles:true}));
      return 'ok';
    })()""" % (json.dumps(title), json.dumps(desc), b64))
    time.sleep(3)
    return r

def wa_set_country(country='Ghana'):
    """Open Country of origin dropdown, trusted-click the row (radio commits even
    though the list visually stays open), then the Save registers with delay."""
    r=js("""(() => {
      const lab=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim().startsWith('Country of origin')&&e.children.length===0)[0];
      if(!lab) return 'nolab';
      const t=lab.closest('[role=button],[tabindex],div[contenteditable]')||lab.parentElement;
      const rc=t.getBoundingClientRect(); return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2});
    })()""")
    if r=='nolab': return 'FAIL country open'
    p=J.loads(r); wa_trusted_click(p['x'], p['y'])
    time.sleep(2.5)
    if js("(() => (document.body.innerText||'').includes('Åland Islands'))()") is not True:
        return 'FAIL country list'
    r=js("""(() => {
      const rows=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()===%r&&e.children.length===0);
      if(!rows.length) return 'norow';
      const t=rows[0].closest('li,[role=option]')||rows[0].parentElement;
      const rc=t.getBoundingClientRect(); return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2});
    })()""" % country)
    if r=='norow': return 'FAIL country row'
    p=J.loads(r); wa_trusted_click(p['x'], p['y'])
    time.sleep(2)
    # verify radio checked
    chk=js("""(() => {
      const g=[...document.querySelectorAll('*')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()===%r&&e.children.length===0)[0];
      if(!g) return 'noRow';
      const li=g.closest('li'); const radio=li && li.querySelector('input[type=radio]');
      return radio && radio.checked ? 'checked' : 'unchecked';
    })()""" % country)
    if chk!='checked': return 'FAIL country radio'
    # Save (trusted; registers with delay)
    r=js("""(() => {
      const b=[...document.querySelectorAll('div[role=button],button')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Save');
      if(!b.length) return null;
      const rc=b[0].getBoundingClientRect(); return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2});
    })()""")
    if r: p=J.loads(r); wa_trusted_click(p['x'], p['y'])
    for k in range(8):
        time.sleep(1.5)
        if js("(() => (document.body.innerText||'').includes('Åland Islands'))()") is not True:
            return 'OK'
    return 'FAIL country save'

def wa_commit():
    """Click 'Add to catalogue'. Returns 'SAVED' when drawer closes / toast appears."""
    r=js("""(() => {
      const b=[...document.querySelectorAll('div[role=button],button')].filter(e=>e.offsetParent!==null&&(e.textContent||'').trim()==='Add to catalogue');
      if(!b.length) return 'nobtn';
      const t=b[b.length-1];
      const rc=t.getBoundingClientRect();
      const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2});
      ['mousedown','mouseup','click'].forEach(ev=>t.dispatchEvent(ME(ev)));
      return 'dispatched';
    })()""")
    if r=='nobtn': return 'FAIL commit btn'
    for k in range(10):
        time.sleep(2)
        if js("(() => (document.body.innerText||'').includes('Item saved'))()") is True:
            return 'SAVED'
        if js("(() => (document.body.innerText||'').includes('Add images'))()") is not True:
            return 'SAVED'  # drawer closed
    return 'FAIL commit'

def wa_add_item(title, desc, photo_path, country='Ghana'):
    """Full flow. Returns 'SAVED' / 'FAIL <step>'. Items land in 'under review'. """
    if js(WA_OPEN_TOOLS) != 'ok': return 'FAIL tools'
    time.sleep(3)
    if js(WA_OPEN_CATALOGUE) == 'noCat': return 'FAIL catalogue'
    time.sleep(3)
    r=js(WA_ADD_ITEM_CARD)
    if r=='gone': return 'FAIL add card'
    p=J.loads(r); wa_trusted_click(p['x'], p['y'])
    time.sleep(4)
    if not wa_drawer_open(): return 'FAIL drawer'
    if wa_fill_fields(title, desc, photo_path)!='ok': return 'FAIL fields'
    if wa_set_country(country)!='OK': return wa_set_country(country)  # one retry, returns its code
    return wa_commit()

DESC_TMPL = ("{title}. Brand new stock from our UK-sourced range.\n"
             "Delivery available across Accra. Call/WhatsApp 0204252252")

# ---- Queue-driven batch (premium-priced wa_queue.json) ----
def _norm(t):
    import re as _re
    return _re.sub(r'[^a-z0-9 ]',' ', t.lower())

def is_duplicate(wa_title):
    """Fuzzy-check wa_title against the live catalogue baseline + posted log."""
    import os
    ex=pkg+r'\wa_catalog_existing.json'
    titles=list(json.load(open(ex))) if os.path.exists(ex) else []
    A=set(_norm(wa_title).split())-{'ghs','ghc','gh','the','with','and','for','from','uk','new','kit','piece'}
    for e in titles:
        B=set(_norm(e).split())-{'ghs','ghc','gh','the','with','and','for','from','uk','new','kit','piece'}
        if not A or not B: continue
        if len(A&B)/max(1,min(len(A),len(B)))>=0.6: return True
    return False

def wa_post_next(count=15):
    """Post up to `count` items from wa_queue.json (premium titles with price).
    Saves wa_catalog_posted.json after EVERY item. Returns report dict."""
    import os
    queue=json.load(open(pkg+r'\wa_queue.json'))
    postedp=pkg+r'\wa_catalog_posted.json'
    posted=set(json.load(open(postedp)))
    results=[]
    done=0
    for x in queue:
        if done>=count: break
        jid=x['jiji_id']
        if jid in posted:
            continue
        photo=os.path.join(pkg, x['photo'])
        if not os.path.exists(photo):
            results.append((jid,'FAIL no photo')); continue
        if is_duplicate(x['wa_title']):
            results.append((jid,'SKIP duplicate')); posted.add(jid)
            json.dump(sorted(posted), open(postedp,'w')); continue
        cond=x.get('condition','USED')
        base=x['wa_title'].rsplit(' ',1)[0]
        if cond=='NEW':
            line='Brand New, Sealed'
        else:
            line='UK Pre-Owned, Tested Working'
        desc=f"{base}. {line}. Delivery available across Accra. Call/WhatsApp 0204252252"
        r=wa_add_item(x['wa_title'], desc, photo)
        results.append((jid, r))
        if r=='SAVED':
            posted.add(jid)
            json.dump(sorted(posted), open(postedp,'w'))
            # append title to live baseline for future dedupe
            ex=pkg+r'\wa_catalog_existing.json'
            base=json.load(open(ex)) if os.path.exists(ex) else []
            base.append(x['wa_title'])
            json.dump(sorted(set(base)), open(ex,'w'))
            done+=1
        else:
            # fail twice rule handled by caller; move on after 1 fail here
            continue
    return {'posted':done,'results':results}

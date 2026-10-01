import time, base64, json, os, subprocess
import json as J
assert 'js' in globals(), 'run via exec in harness main'

pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
imgdir=pkg+r'\photos'

OPEN_MARKER = """(() => [...document.querySelectorAll('[role=dialog]')].some(d => d.offsetParent !== null && /home & garden|miscellaneous|tools/i.test(d.textContent||'')))()"""

def focus():
    for title in ['Create new listing','Facebook','Chrome']:
        try:
            subprocess.run(['powershell','-c','(New-Object -ComObject WScript.Shell).AppActivate("%s")' % title],timeout=10,capture_output=True)
        except Exception:
            pass
    time.sleep(0.8)

def click_el(jsf, tries=6, delay=1.2, focus_first=False):
    for k in range(tries):
        if focus_first: focus()
        pos=js(jsf)
        if pos:
            p=J.loads(pos); click_at_xy(int(p['x']),int(p['y'])); return True
        time.sleep(delay)
    return False

CTRL=lambda name:"""(() => {
  const c=[...document.querySelectorAll('[role=button],[role=combobox],[aria-haspopup]')]
    .filter(e=>e.offsetParent!==null).find(e=>(e.textContent||'').trim().startsWith('%s'));
  if(!c) return null;
  c.scrollIntoView({block:'center'});
  const rc=c.getBoundingClientRect(); return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2});
})()""" % name

def pick_visible(label):
    return """(() => {
      const want=%r.toLowerCase();
      let scope=[...document.querySelectorAll('[role=dialog]')].filter(d=>d.offsetParent!==null);
      let leaves=[];
      for(const d of scope){ leaves.push(...d.querySelectorAll('*')); }
      if(!leaves.length) leaves=[...document.querySelectorAll('*')];
      leaves=leaves.filter(e=>e.children.length===0 && (e.textContent||'').trim().toLowerCase()===want && e.offsetParent!==null);
      if(!leaves.length) return null;
      const el=leaves[leaves.length-1];
      el.scrollIntoView({block:'center'});
      const rc=el.getBoundingClientRect();
      return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2});
    })()""" % label

NEXT_PUB="""(() => {
  const b=[...document.querySelectorAll('div[role=button],button')]
    .filter(e=>e.offsetParent!==null).find(e=>['Publish','Next'].includes((e.textContent||'').trim()));
  if(!b) return null;
  b.scrollIntoView({block:'center'});
  const rc=b.getBoundingClientRect(); return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2,label:(b.textContent||'').trim()});
})()"""

def set_condition():
    for attempt in range(3):
        if not click_el(CTRL('Condition'), focus_first=True): return 'FAIL cond ctrl'
        time.sleep(2)
        marker=js("""(() => [...document.querySelectorAll('*')].some(e=>e.children.length===0 && (e.textContent||'').trim()==='Used \u2013 good' && e.offsetParent!==null))()""")
        if marker:
            if click_el(pick_visible('New'), focus_first=True):
                time.sleep(1.5)
                return 'OK'
        time.sleep(1)
    return 'FAIL cond opt'

def post_one(title,price,photo,category,desc):
    for attempt in range(3):
        try:
            goto_url('https://www.facebook.com/marketplace/create/item')
            try:
                wait_for_load()
            except Exception:
                pass
            time.sleep(5)
            return _post_one_inner(title,price,photo,category,desc)
        except Exception as e:
            if attempt == 2:
                return f'FAIL nav: {e}'
            time.sleep(4)

def _post_one_inner(title,price,photo,category,desc):
    goto_url('https://www.facebook.com/marketplace/create/item')
    time.sleep(5)
    b64=base64.b64encode(open(photo,'rb').read()).decode()
    desc_js=json.dumps(desc)  # real newlines, safely quoted
    r=js("""(async () => {
      const inp=[...document.querySelectorAll('input[type=file]')].find(f=>f.accept.includes('image'));
      if(!inp) return 'retry';
      const bin=atob('%s'); const bytes=new Uint8Array(bin.length);
      for(let i=0;i<bin.length;i++)bytes[i]=bin.charCodeAt(i);
      const dt=new DataTransfer(); dt.items.add(new File([bytes],'photo.jpg',{type:'image/jpeg'}));
      inp.files=dt.files; inp.dispatchEvent(new Event('change',{bubbles:true}));
      await new Promise(r=>setTimeout(r,2500));
      const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
      const title=%s; const pricestr='%s';
      for(let k=0;k<10;k++){
        const tis=[...document.querySelectorAll('input[type=text]')].filter(i=>i.offsetParent!==null);
        if(tis.length>=2){
          setter.call(tis[0],title); tis[0].dispatchEvent(new Event('input',{bubbles:true}));
          setter.call(tis[1],pricestr); tis[1].dispatchEvent(new Event('input',{bubbles:true}));
          return 'fields set';
        }
        await new Promise(r=>setTimeout(r,600));
      }
      return 'no text inputs';
    })()""" % (b64, desc_js and json.dumps(title[:100]), str(price)))
    if r!='fields set': return f'FAIL fields: {r}'
    time.sleep(1)
    cat_ok = False
    for att in range(5):
        click_el(CTRL('Category'), focus_first=True)
        time.sleep(2)
        if js(OPEN_MARKER) is True:
            cat_ok = True
            break
    if not cat_ok:
        return 'FAIL cat open'
    ok = False
    for lab in (category, 'Miscellaneous', 'Tools'):
        for att in range(2):
            if click_el(pick_visible(lab), focus_first=True):
                ok = True
                break
            time.sleep(1)
        if ok:
            break
    if not ok:
        return 'FAIL cat opt'
    time.sleep(2)
    rc=set_condition()
    if rc!='OK': return rc
    js("""(() => {
      const ta=document.querySelector('textarea');
      if(!ta) return;
      const ts=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;
      ts.call(ta,%s); ta.dispatchEvent(new Event('input',{bubbles:true}));
    })()""" % desc_js)
    time.sleep(1)
    for k in range(10):
        pos=js(NEXT_PUB)
        if pos:
            p=J.loads(pos)
            click_at_xy(int(p['x']),int(p['y']))
            time.sleep(2.5)
            if p.get('label')=='Publish':
                time.sleep(2)
                return 'PUBLISHED'
        else:
            time.sleep(1)
    return 'FAIL publish'

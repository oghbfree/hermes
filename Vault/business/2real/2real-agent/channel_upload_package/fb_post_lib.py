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

def open_ctrl(name):
    """Open a form control (Category/Condition). FB 2026-10+: click_at_xy/CDP trusted
    clicks get silently dropped — dispatch mousedown/mouseup/click on the element itself."""
    for k in range(5):
        js("""(() => { const c=[...document.querySelectorAll('[role=button],[role=combobox],[aria-haspopup]')].filter(e=>e.offsetParent!==null).find(e=>(e.textContent||'').trim().startsWith(%r)); if(!c) return 'noc'; const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window}); ['mousedown','mouseup','click'].forEach(t=>c.dispatchEvent(ME(t))); return 'ok'; })()""" % name)
        time.sleep(2.5)
        if js(OPEN_MARKER) is True or (name=='Condition' and js("(() => [...document.querySelectorAll('[role=dialog],[role=listbox]')].some(d=>d.offsetParent!==null&&/used/i.test(d.textContent||'')))()") is True):
            return True
    return False

def pick_leaf(want):
    """Click a visible option leaf inside the open dialog using dispatched mouse events."""
    for k in range(3):
        r = js("""(() => { const want=%r.toLowerCase(); let leaves=[...document.querySelectorAll('[role=dialog],[role=listbox]')].filter(d=>d.offsetParent!==null).flatMap(d=>[...d.querySelectorAll('*')]); if(!leaves.length) leaves=[...document.querySelectorAll('*')]; leaves=leaves.filter(e=>e.children.length===0&&(e.textContent||'').trim().toLowerCase()===want&&e.offsetParent!==null); if(!leaves.length) return null; const el=leaves[leaves.length-1]; el.scrollIntoView({block:'center'}); const rc=el.getBoundingClientRect(); return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2}); })()""" % want)
        if not r: time.sleep(1.5); continue
        p = J.loads(r)
        js("""(() => { const x=%d,y=%d; const t=document.elementFromPoint(x,y); if(!t) return 'noel'; const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:x,clientY:y}); ['mousedown','mouseup','click'].forEach(e=>t.dispatchEvent(ME(e))); return 'ok'; })()""" % (int(p['x']), int(p['y'])))
        time.sleep(2)
        return True
    return False

def set_condition():
    for attempt in range(3):
        if not open_ctrl('Condition'): continue
        if pick_leaf('New'):
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
    # FB now shows a 'Choose listing type' chooser — click 'Item for sale' if present
    for k in range(4):
        if click_el(pick_visible('Item for sale'), focus_first=True):
            time.sleep(3)
            break
        if js("(() => !!document.querySelector('input[type=file]'))()") is True:
            break
        time.sleep(2)
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
    if not open_ctrl('Category'):
        return 'FAIL cat open'
    ok = False
    for lab in (category, 'Miscellaneous', 'Tools'):
        if pick_leaf(lab):
            ok = True
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
            js("""(() => { const x=%d,y=%d; const t=document.elementFromPoint(x,y); if(!t) return 'noel'; const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:x,clientY:y}); ['mousedown','mouseup','click'].forEach(e=>t.dispatchEvent(ME(e))); return 'ok'; })()""" % (int(p['x']),int(p['y'])))
            time.sleep(2.5)
            if p.get('label')=='Publish':
                time.sleep(2)
                return 'PUBLISHED'
        else:
            time.sleep(1)
    return 'FAIL publish'

import sys, json, time, base64, os
sys.path.insert(0, r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package')
import cdp_harness as H
js = H.js; goto_url = H.goto_url; wait_for_load = H.wait_for_load; click_at_xy = H.click_at_xy
lib_src = open(r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package\fb_post_lib.py', encoding='utf-8').read()
exec(lib_src)
PKG = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
IMG = PKG + r'\photos'

def pick_leaf_sub(want):
    for k in range(3):
        r = js("""(() => {
          const want=%r.toLowerCase();
          let leaves=[...document.querySelectorAll('[role=dialog],[role=listbox]')].filter(d=>d.offsetParent!==null)
            .flatMap(d=>[...d.querySelectorAll('*')]).filter(e=>e.offsetParent!==null);
          let m=leaves.filter(e=>(e.textContent||'').trim().toLowerCase()===want && e.children.length===0);
          if(!m.length) m=leaves.filter(e=>(e.textContent||'').trim().toLowerCase().startsWith(want) && e.children.length===0);
          if(!m.length) m=leaves.filter(e=>(e.textContent||'').trim().toLowerCase().includes(want) && e.children.length===0 && (e.textContent||'').trim().length<60);
          if(!m.length) return null;
          const el=m[m.length-1]; el.scrollIntoView({block:'center'});
          const rc=el.getBoundingClientRect();
          return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2,txt:(el.textContent||'').trim()});
        })()""" % want)
        if r:
            p = json.loads(r)
            print('pick:', p.get('txt'))
            js("""(() => { const x=%d,y=%d; const t=document.elementFromPoint(x,y); if(!t) return 'noel';
              const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:x,clientY:y});
              ['mousedown','mouseup','click'].forEach(e=>t.dispatchEvent(ME(e))); return 'ok'; })()""" % (int(p['x']), int(p['y'])))
            time.sleep(2)
            return p.get('txt','')
        time.sleep(1.5)
    return None

def type_combo(q):
    r = js("""(async () => {
      const c=[...document.querySelectorAll('[role=combobox]')].filter(e=>e.offsetParent!==null)
        .find(e=>{const l=e.closest('label'); return l && l.textContent.trim().startsWith('Category');});
      if(!c) return 'noc';
      const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
      for(let k=0;k<8;k++){
        if(c.tagName==='INPUT'){
          setter.call(c,%r); c.dispatchEvent(new Event('input',{bubbles:true}));
        } else {
          const inp=c.querySelector('input'); if(!inp){await new Promise(r=>setTimeout(r,600)); continue;}
          setter.call(inp,%r); inp.dispatchEvent(new Event('input',{bubbles:true}));
        }
        c.dispatchEvent(new Event('change',{bubbles:true}));
        await new Promise(r=>setTimeout(r,1200));
        return 'typed';
      }
      return 'noinput';
    })()""" % (q, q))
    return r

def post_item(jid, title, price, category_query, cond_target, spec):
    globals()['COND_TARGET'] = cond_target
    desc = make_desc(title, spec, condition=cond_target)
    print('DESC:', repr(desc))
    src = os.path.join(IMG, jid + '.jpg')
    dst = os.path.join(IMG, jid + '_v.jpg')
    photo = vary_photo(src, dst)
    print('photo:', photo)
    for attempt in range(3):
        try:
            goto_url('https://www.facebook.com/marketplace/create/item')
            try: wait_for_load()
            except Exception: pass
            time.sleep(5)
            for k in range(4):
                if click_el(pick_visible('Item for sale'), focus_first=True):
                    time.sleep(3); break
                if js("(() => !!document.querySelector('input[type=file]'))()") is True:
                    break
                time.sleep(2)
            b64 = base64.b64encode(open(photo,'rb').read()).decode()
            r = js("""(async () => {
              const inp=[...document.querySelectorAll('input[type=file]')].find(f=>f.accept.includes('image'));
              if(!inp) return 'retry';
              const bin=atob('%s'); const bytes=new Uint8Array(bin.length);
              for(let i=0;i<bin.length;i++)bytes[i]=bin.charCodeAt(i);
              const dt=new DataTransfer(); dt.items.add(new File([bytes],'photo.jpg',{type:'image/jpeg'}));
              inp.files=dt.files; inp.dispatchEvent(new Event('change',{bubbles:true}));
              await new Promise(r=>setTimeout(r,3000));
              const previews=[...document.querySelectorAll('[role=dialog] img')].filter(i=>i.offsetParent!==null && (i.src||'').startsWith('data:'));
              return 'previews:'+previews.length;
            })()""" % b64)
            if str(r) == 'previews:0':
                return 'FAIL photo preview'
            print('photo:', r)
            r = js("""(async () => {
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
            })()""" % (json.dumps(title[:100]), str(price)))
            if r != 'fields set': return 'FAIL fields: ' + str(r)
            time.sleep(1)
            if not open_category():
                return 'FAIL cat open'
            tq = type_combo(category_query)
            time.sleep(1)
            got = pick_leaf_sub(category_query)
            if not got:
                got = pick_leaf_sub('Miscellaneous') or pick_leaf_sub('Tools')
            if not got: return 'FAIL cat opt'
            time.sleep(2)
            rc = set_condition(cond_target)
            if rc != 'OK': return rc
            js("""(() => {
              const ta=document.querySelector('textarea');
              if(!ta) return;
              const ts=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;
              ts.call(ta,%s); ta.dispatchEvent(new Event('input',{bubbles:true}));
            })()""" % json.dumps(desc))
            time.sleep(1)
            prev = js("(() => { const imgs=[...document.querySelectorAll('[role=dialog] img')].filter(i=>i.offsetParent!==null && (i.src||'').startsWith('data:')); return imgs.length; })()")
            print('preview count before publish:', prev)
            if not prev:
                return 'FAIL no preview'
            for k in range(10):
                pos = js(NEXT_PUB)
                if pos:
                    p = json.loads(pos)
                    js("""(() => { const x=%d,y=%d; const t=document.elementFromPoint(x,y); if(!t) return 'noel';
                      const ME=ev=>new MouseEvent(ev,{bubbles:true,cancelable:true,view:window,clientX:x,clientY:y});
                      ['mousedown','mouseup','click'].forEach(e=>t.dispatchEvent(ME(e))); return 'ok'; })()""" % (int(p['x']), int(p['y'])))
                    time.sleep(2.5)
                    if p.get('label') == 'Publish':
                        time.sleep(3)
                        return 'PUBLISHED'
                else:
                    time.sleep(1)
            return 'FAIL publish'
        except Exception as e:
            if attempt == 2:
                return 'FAIL nav: %r' % e
            time.sleep(5)

ITEMS = [
    dict(jid='14265416', title='Vivitar ViviCam 7022 7.1MP Digital Camera SD Card 4x Zoom — UK Imported, Quality Checked',
         price='450', cat='cameras', cond='New',
         spec='7.1MP CMOS sensor, 1.8in LCD, 4x digital zoom, 640x480 video, SD card up to 32GB (included), 3x AAA.'),
    dict(jid='16210001', title='Direct Power Circular Saw 1200W 185mm Blade Heavy Duty — UK Imported, Quality Checked',
         price='700', cat='tools', cond='New',
         spec='1200W motor, 185mm blade, ~5500rpm, 65mm cut at 90°, 42° bevel, spindle lock.'),
    dict(jid='16544740', title='Skate Board Pre Owned From UK — Used, Quality Checked',
         price='400', cat='skateboard', cond='Used',
         spec='Full-size skateboard, used from the UK, available as seen.'),
    dict(jid='15951799', title='Amazon Echo 2nd Gen Wireless Speaker Alexa Bluetooth — UK Used, Quality Checked',
         price='600', cat='audio', cond='Used',
         spec='Dolby 360° omnidirectional sound, 7-mic beam-forming with noise cancellation, Alexa voice control, Bluetooth.'),
    dict(jid='16356232', title='Mini Guitar Amplifier 10W Practice Amp — UK Imported, Quality Checked',
         price='480', cat='musical', cond='New',
         spec='10W practice amp with gain, volume, bass and treble controls.'),
]

if __name__ == '__main__':
    idx = int(sys.argv[1])
    it = ITEMS[idx]
    H.connect(substr='/marketplace/create/item')
    res = post_item(it['jid'], it['title'], it['price'], it['cat'], it['cond'], it['spec'])
    print('RESULT:', res)
    if res == 'PUBLISHED':
        pf = PKG + r'\fb_posted.json'
        posted = json.load(open(pf))
        if int(it['jid']) not in posted:
            posted.append(int(it['jid']))
            json.dump(posted, open(pf, 'w'))
            print('SAVED', it['jid'], '-> fb_posted.json (', len(posted), 'total )')

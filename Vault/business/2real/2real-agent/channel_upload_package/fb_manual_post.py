"""Manual FB post flow — replicates the step sequence verified working 13 Oct 26.
Usage: python fb_manual_post.py <jiji_id> <log_path>
Verbose per-step checks; navigates the cdp_harness tab. No auto-added to fb_posted (caller does).
"""
import sys, os, json, time, base64

pkg = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0, pkg)
import cdp_harness as C

G = {'js': C.js, 'goto_url': C.goto_url, 'wait_for_load': C.wait_for_load, 'click_at_xy': C.click_at_xy,
     'time': time, 'json': json, 'base64': base64, 'os': os}
src = open(os.path.join(pkg, 'fb_post_lib.py'), encoding='utf-8').read().replace(
    "assert 'js' in globals(), 'run via exec in harness main'", "")
exec(src, G)

logf = None
def L(m):
    print(m, flush=True)
    if logf: logf.write(m + '\n'); logf.flush()

def find_btn(exact_list=None, startswith=None):
    return C.js("""(() => {
      const b=[...document.querySelectorAll('div[role=button],button')].filter(e=>e.offsetParent!==null);
      let t=b.find(e=>%s);
      if(t){ t.scrollIntoView({block:'center'});
        const rc=t.getBoundingClientRect();
        return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2,label:(t.textContent||'').trim().slice(0,30)});
      } return null;
    })()""" % (("['%s'].includes((e.textContent||'').trim())" % "','".join(exact_list)) if exact_list
               else ("(e.textContent||'').trim().startsWith('%s')" % startswith)))

def main():
    jid = int(sys.argv[1]); logf = open(sys.argv[2], 'a', encoding='utf-8')
    ready = json.load(open(os.path.join(pkg, 'fb_ready_131026.json'), encoding='utf-8'))
    r = next(x for x in ready if x['jiji_id'] == jid)
    L('posting %s | %s | %s | %s | %s' % (jid, r['title'][:60], r['price'], r['category'], r['condition']))

    C.goto_url('https://www.facebook.com/marketplace/create/item')
    time.sleep(6)
    pos = find_btn(startswith='Item for sale')
    if pos:
        p = json.loads(pos); C.click_at_xy(int(p['x']), int(p['y'])); time.sleep(3)
    if C.js("!!document.querySelector('input[type=file]')") is not True:
        L('FAIL no file input'); return 'FAIL no file input'

    b64 = base64.b64encode(open(r['photo_var'], 'rb').read()).decode()
    res = C.js_async("""(async () => {
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
          await new Promise(r=>setTimeout(r,600));
          return 'fields set: '+tis[0].value.slice(0,40)+' | '+tis[1].value;
        }
        await new Promise(r=>setTimeout(r,600));
      }
      return 'no text inputs';
    })()""" % (b64, json.dumps(r['title'][:100]), str(r['price'])), timeout=90)
    L('fields: %r' % res)
    if not (isinstance(res, str) and res.startswith('fields set')):
        L('FAIL fields'); return 'FAIL fields'
    time.sleep(2)

    if not G['open_category']():
        L('FAIL cat open'); return 'FAIL cat open'
    if not G['pick_leaf'](r['category']):
        L('FAIL cat leaf %s' % r['category']); return 'FAIL cat'
    time.sleep(2)
    rc = G['set_condition'](r['condition'])
    L('condition: %s' % rc)
    if rc != 'OK': return 'FAIL condition'
    time.sleep(1)

    C.js("""(() => {
      const ta=document.querySelector('textarea');
      if(!ta) return;
      const ts=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;
      ts.call(ta,%s); ta.dispatchEvent(new Event('input',{bubbles:true}));
    })()""" % json.dumps(r['desc']))
    time.sleep(1.5)
    L('desc len: %s' % C.js("document.querySelector('textarea') ? document.querySelector('textarea').value.length : -1"))

    for k in range(8):
        pos = find_btn(exact_list=['Publish', 'Next'])
        if pos:
            p = json.loads(pos)
            C.click_at_xy(int(p['x']), int(p['y']))
            time.sleep(2.5)
            L('clicked %s' % p.get('label'))
            if p.get('label') == 'Publish':
                time.sleep(5)
                return 'PUBLISHED'
        else:
            time.sleep(1)
    return 'FAIL publish'

if __name__ == '__main__':
    print(main())

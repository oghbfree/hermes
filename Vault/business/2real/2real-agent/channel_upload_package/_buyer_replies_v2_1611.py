import sys, time, json
pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0,pkg)
import cdp_harness as C

def char_pt(txt):
    r=C.js("""(() => {
      const it=document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let n; const s="""+json.dumps(txt)+""";
      while(n=it.nextNode()){ if(n.data && n.data.includes(s)){ break; } }
      if(!n) return 'nf';
      const b=document.createRange().selectNodeContents(n).getBoundingClientRect();
      return JSON.stringify({x:(b.x+b.width/2)|0, y:(b.y+b.height/2)|0});
    })()""")
    return r if r and r!='nf' else None

def goto_inbox():
    C.goto_url('https://www.facebook.com/marketplace/inbox'); time.sleep(9)

def open_thread(buyer):
    pt=char_pt(buyer)
    if not pt: print('no coord for', buyer); return False
    p=json.loads(pt); C.click_at_xy(int(p['x']),int(p['y'])); time.sleep(7)
    return True

def composer_matches(buyer):
    t=C.js("document.body.innerText") or ''
    ok = ('Write to '+buyer) in t
    if not ok:
        # also allow partial / name-only header
        ok = buyer in t and ('marketplace/inbox' in (C.js('location.href') or '') or 'Write to' in t)
    return ok

def send(text):
    r=C.js("""(() => {
      const areas=[...document.querySelectorAll('div[role=textbox][contenteditable=true]')].filter(e=>e.offsetParent!==null);
      const ta=areas[areas.length-1];
      if(!ta) return 'noarea';
      ta.focus();
      const t="""+json.dumps(text)+""";
      document.execCommand('insertText',false,t);
      return 'typed';
    })()""")
    time.sleep(2)
    C.js("""(() => {
      const ta=[...document.querySelectorAll('div[role=textbox][contenteditable=true]')].filter(e=>e.offsetParent!==null).pop();
      if(!ta) return;
      ['keydown','keyup'].forEach(ev=>ta.dispatchEvent(new KeyboardEvent(ev,{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true})));
    })()""")
    time.sleep(4)
    return r

threads=[
  ('iamPatrick','Hi Patrick, the Wilson Adult Tennis Racket with Bag is GHS 650, UK imported. MoMo/cash only, no credit. WhatsApp 0204252252'),
  ('Diana','Hi Diana, the Leapfrog 2-in-1 Touch Tablet and Laptop is GHS 250, UK imported and quality checked. MoMo/cash only, no credit. WhatsApp 0204252252'),
  ('Scanty','Hi, the DeWalt Impact Driver Wrench is GHS 850, UK imported and tested working. MoMo/cash only, no credit. WhatsApp 0204252252'),
]
for buyer,msg in threads:
    goto_inbox(); open_thread(buyer)
    if composer_matches(buyer):
        send(msg)
        print('SENT to', buyer)
    else:
        print('SKIP (composer mismatch):', buyer, '| header:', C.js("document.body.innerText")[:120].replace('\n',' '))

import sys, time, json
pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0,pkg)
import cdp_harness as C

def goto_inbox():
    C.goto_url('https://www.facebook.com/marketplace/inbox')
    time.sleep(8)

def find_and_open(buyer_kw):
    # click the thread row containing buyer_kw text
    code = C.js(f"""(() => {{
      const rows=[...document.querySelectorAll('[role=row],[role=listitem],div')].filter(e=>e.offsetParent!==null && e.innerText && e.innerText.length<400 && e.innerText.includes({json.dumps(buyer_kw)}));
      // pick the most shallow (smallest) matching element that has the name as its own recent text
      rows.sort((a,b)=>a.innerText.length-b.innerText.length);
      const target=rows[0];
      if(!target) return 'notfound';
      const r=target.getBoundingClientRect();
      return JSON.stringify({{x:r.x+r.width/2, y:r.y+Math.min(r.height/2,20)}});
    }})()""")
    if code and code!='notfound':
        try:
            p=json.loads(code); C.click_at_xy(int(p['x']),int(p['y'])); time.sleep(6); return True
        except Exception as e:
            print('click err',e); return False
    return False

def composer_ok(buyer):
    txt=C.js("document.body.innerText")
    return ('Write to '+buyer) in txt

def send_text(text):
    # focus composer, type, Enter
    r=C.js("""(() => {
      const areas=[...document.querySelectorAll('div[role=textbox][contenteditable=true]')].filter(e=>e.offsetParent!==null);
      // newest visible composer = last
      const ta=areas[areas.length-1];
      if(!ta) return 'noarea';
      ta.focus();
      const t="""+json.dumps(text.replace('\n',' \n'))+""";
      const setter=Object.getOwnPropertyDescriptor(window.HTMLDivElement.prototype.__proto__||{}.constructor,'value');
      // use execCommand insertText fallback
      document.execCommand('insertText',false,t);
      return 'typed';
    })()""")
    time.sleep(2)
    C.js("({}) => {}")
    # press Enter
    C.js("""(() => {
      const ta=[...document.querySelectorAll('div[role=textbox][contenteditable=true]')].filter(e=>e.offsetParent!==null).pop();
      if(!ta) return 'noarea';
      ta.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true}));
      ta.dispatchEvent(new KeyboardEvent('keyup',{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true}));
      return 'sent';
    })()""")
    time.sleep(4)
    return r

threads=[
  # (buyer_kw, reply_text)
  ('iamPatrick', 'Hi Patrick, the Tennis Rackets and Balls are GHS 650, UK imported. MoMo/cash only, no credit. WhatsApp 0204252252'),
  ('Diana', 'Hi Diana, the Leapfrog 2-in-1 Touch Tablet and Laptop is GHS 250, UK imported and quality checked. MoMo/cash only, no credit. WhatsApp 0204252252'),
  ('Scanty', 'Hi, the DeWalt Impact Driver Wrench is GHS 850, UK imported and tested working. MoMo/cash only, no credit. WhatsApp 0204252252'),
]
for kw,msg in threads:
    goto_inbox()
    if not find_and_open(kw):
        print('NOT FOUND/OPEN', kw); continue
    if not composer_ok(kw):
        print('COMPOSER MISMATCH for', kw, '- not sending'); continue
    rc=send_text(msg)
    print('SENT to', kw, '| rc=', rc)

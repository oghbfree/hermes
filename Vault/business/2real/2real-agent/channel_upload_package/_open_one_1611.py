import sys, time, json
pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0,pkg)
import cdp_harness as C

def safe_pt_find():
    return C.js("""(() => {
      try{
        const s='iamPatrick';
        const it=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
        let n=null;
        while(n=it.nextNode()){ if((n.data||'').indexOf(s)>=0) break; }
        if(!n) return 'nf';
        const b=document.createRange().selectNodeContents(n).getBoundingClientRect();
        // climb to finding a clickable ancestor row
        let el=n.parentElement;
        for(let k=0;k<8&&el;k++){ const r=el.getBoundingClientRect(); if(r.width>200&&r.height>40&&r.height<120){ return JSON.stringify({x:(r.x+r.width/2)|0,y:(r.y+20)|0}); } el=el.parentElement; }
        return JSON.stringify({x:(b.x+b.width/2)|0,y:(b.y+b.height/2)|0});
      }catch(e){ return 'err:'+e.message; }
    })()""")

C.goto_url('https://www.facebook.com/marketplace/inbox'); time.sleep(11)
r=safe_pt_find(); print('pt:', r)
if r and r not in ('nf',) and not r.startswith('err:'):
    p=json.loads(r); C.click_at_xy(int(p['x']),int(p['y'])); time.sleep(9)
    t=C.js('document.body.innerText') or ''
    i=t.find('Write to')
    print('Write to:', i>=0, (t[i:i+60].replace('\n',' ') if i>=0 else ''))
    print('composers:', C.js("JSON.stringify([...document.querySelectorAll('div[role=textbox][contenteditable=true]')].filter(e=>e.offsetParent!==null).length)"))
    print('hasPatrickInThreadsLeft:', C.js("document.body.innerText.includes('iamPatrick')"))
else:
    print('could not locate')

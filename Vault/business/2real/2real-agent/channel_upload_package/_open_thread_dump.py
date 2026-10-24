"""Open a specific buyer thread in FB Marketplace inbox and dump the conversation tail (READ-ONLY)."""
import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

kw = sys.argv[1].lower()

tabs = C.list_tabs()
inbox = [t for t in tabs if "inbox" in t.get("url", "").lower()]
if not inbox:
    C.goto_url("https://www.facebook.com/marketplace/inbox")
    time.sleep(8)
    tabs = C.list_tabs()
    inbox = [t for t in tabs if "inbox" in t.get("url", "").lower()]
if not inbox:
    print("RESULT: NO_INBOX_TAB"); sys.exit(2)
C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
time.sleep(3)

# If we're inside a conversation (URL has ?ref=), go back to inbox list first
u = C.js("location.href") or ""
print("URL:", u[:120])
if "/messenger" in u or "/inbox" not in u.split("?")[0] or "thread" in u:
    C.goto_url("https://www.facebook.com/marketplace/inbox")
    time.sleep(8)

for attempt in range(6):
    r = C.js("""(() => {
      const kw=%s.toLowerCase();
      const els=[].slice.call(document.querySelectorAll('[role=button]')).filter(e=>e.offsetParent!==null);
      const hits=els.filter(e=>{const t=(e.textContent||'').replace(/\\s+/g,' ').trim();
        return t.toLowerCase().startsWith(kw) && t.includes('·') && t.length<300;});
      if(!hits.length){
        const all=[].slice.call(document.querySelectorAll('div,span,a,[role=button]')).filter(e=>e.offsetParent!==null);
        const f=all.filter(e=>{const t=(e.textContent||'').replace(/\\s+/g,' ').trim();
          return t.toLowerCase().startsWith(kw) && t.includes('·') && t.length<180;}).pop();
        if(!f) return null;
        const rc2=f.getBoundingClientRect();
        return JSON.stringify({x:rc2.x+rc2.width/2,y:rc2.y+rc2.height/2});
      }
      const el=hits.sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
      el.scrollIntoView({block:'center'});
      const rc=el.getBoundingClientRect();
      return JSON.stringify({x:rc.x+rc.width/2,y:rc.y+rc.height/2});
    })()""" % json.dumps(kw))
    if r:
        p = json.loads(r)
        C.click_at_xy(int(p["x"]), int(p["y"]))
        print("CLICKED row for", kw)
        break
    time.sleep(2)
else:
    print("RESULT: SKIP no_row |", kw); sys.exit(0)

time.sleep(9)
# Dump conversation text
txt = C.js("document.body.innerText") or ""
print("CONVO LEN:", len(txt))
print(txt[-4500:])

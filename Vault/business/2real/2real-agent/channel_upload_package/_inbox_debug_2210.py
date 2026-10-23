import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

tabs = C.list_tabs()
print("TABS:", [(t.get("title","")[:30], t.get("url","")[:80]) for t in tabs])
inbox = [t for t in tabs if "inbox" in t.get("url","").lower() and "marketplace" in t.get("url","").lower()]
if inbox:
    C._ws = inbox[0]["webSocketDebuggerUrl"]; C._conn = None
    print("USING INBOX TAB")
else:
    print("NO INBOX TAB - opening")
    C.goto_url("https://www.facebook.com/marketplace/inbox")
    time.sleep(8)

info = C.js(r"""(() => {
  const as=[].slice.call(document.querySelectorAll('a[href]')).filter(e=>e.offsetParent!==null && /(message|chat)/i.test(e.href||''));
  const links=as.slice(0,25).map(a=>({href:(a.href||'').slice(0,110), txt:(a.innerText||'').replace(/\n/g,' | ').slice(0,90)}));
  const roles={link:document.querySelectorAll('[role=link]').length, listitem:document.querySelectorAll('[role=listitem]').length, row:document.querySelectorAll('[role=row]').length, tab:document.querySelectorAll('[role=tab]').length, button:document.querySelectorAll('[role=button]').length};
  return JSON.stringify({links, roles, url: location.href.slice(0,120), bodylen:(document.body.innerText||'').length});
})()""")
print("INFO:", info)

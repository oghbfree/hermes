import sys, json, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
import cdp_harness as C

C.goto_url("https://www.facebook.com/marketplace/you/selling")
time.sleep(8)
# scroll down repeatedly to trigger lazy-load
for _ in range(8):
    C.js("window.scrollBy(0, 2500)")
    time.sleep(1.4)
C.js("window.scrollTo(0,0)")
time.sleep(2)

info = C.js(r"""(() => {
  const anchors=[].slice.call(document.querySelectorAll('a[href*="marketplace/item"]')).map(a=({
    href:(a.getAttribute('href')||'').split('?')[0].slice(0,90),
    txt:(a.innerText||'').replace(/\s+/g,' ').slice(0,60)
  }));
  const roles={link:document.querySelectorAll('[role=link]').length, button:document.querySelectorAll('[role=button]').length};
  const bodytxt=(document.body.innerText||'');
  return JSON.stringify({url:location.href.slice(0,110), anchors:anchors.slice(0,20), n_anchors:anchors.length, roles,
    bodylen:bodytxt.length, head:bodytxt.slice(0,600)});
})()""")
print(info)

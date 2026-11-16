import sys, time, json
pkg=r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0,pkg)
import cdp_harness as C
print('URL:', C.js("location.href"))
# What is the open thread? Look for a heading / composer prefix
t=C.js("document.body.innerText") or ''
# find lines around 'Write to' or a bold thread title near composer bottom
i=t.find('Write to')
print('has Write to:', i>=0)
if i>=0: print('ctx:', t[i:i+120].replace('\n',' | '))
# list all visible contenteditable textboxes
areas=C.js("""JSON.stringify([...document.querySelectorAll('div[role=textbox][contenteditable=true]')].filter(e=>e.offsetParent!==null).map(a=>a.innerText.slice(0,60)))""")
print('visible composers:', areas)

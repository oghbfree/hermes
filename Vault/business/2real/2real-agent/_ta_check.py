import sys, os, time, json
os.environ['FB_CDP_URL']='http://127.0.0.1:9222'
sys.path.insert(0, r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent')
import cdp_harness as C
C.connect(substr='jiji.com.gh')
C.goto_url('https://jiji.com.gh/profile-messages/4979038_16912809?utm_source=from_leads')
try: C.wait_for_load()
except: pass
time.sleep(6)
txt = C.js("(() => { const w=document.querySelector('.qa-messenger-room-wrapper'); return w? w.innerText.slice(0,1500) : document.body.innerText.slice(0,1500); })()")
print("ROOM_TEXT>>>")
print(txt)
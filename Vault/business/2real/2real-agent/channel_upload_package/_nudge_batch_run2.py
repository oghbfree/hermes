"""Send due nudges (2nd wave Nii/Hellen, 1st wave Richard/Michael Kwesi) via guarded _fb_reply3.py; mark only on SENT."""
import subprocess, sys, os, json, time

pkg = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0, pkg)
sys.path.insert(0, os.path.dirname(pkg))
from fb_sales_ops import BuyerThreads

PY = r'C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe'
bt = BuyerThreads()
due = bt.due_for_nudge()

targets = [
    ("nii_xbox360games", "Nii", None),
    ("hellen-magnumplus-talos-690", "Hellen", "Hi Hellen - just checking if you're still interested in the Magnum Plus Talos motorcycle lock. Still available, tested working. No rush, just let me know. WhatsApp 0204252252"),
    ("richard-panasonic-stereo", "Richard", None),
    ("michael-kwesi-karcher-900", "Michael Kwesi", None),
]

statuses = {}
for tid, buyer_kw, custom in targets:
    t = next((x for x in due if x.get("id") == tid), None)
    if t is None:
        statuses[tid] = "NOT_DUE"
        continue
    n = (t.get("nudges_sent") or 0) + 1
    text = custom or bt.nudge_text(t, n)
    r = subprocess.run([PY, os.path.join(pkg, "_fb_reply3.py"), buyer_kw, text],
                       capture_output=True, text=True, timeout=180, cwd=pkg)
    out = (r.stdout or "") + (r.stderr or "")
    tail = [ln for ln in out.splitlines() if ln.startswith("RESULT") or ln.startswith("HEADER") or ln.startswith("CLICK")]
    print(f"== {tid} (nudge {n}): tail={tail}")
    print("   last:", out.strip().splitlines()[-1][:120] if out.strip() else "NO_OUTPUT")
    if "RESULT: SENT" in out and "NOT_SENT" not in out:
        bt = BuyerThreads()
        bt.mark_nudged(tid)
        statuses[tid] = "MARKED"
    else:
        statuses[tid] = "NOT_SENT"
    time.sleep(8)

print("\nNUDGE SUMMARY:")
for tid, s in statuses.items():
    print(f"  {tid}: {s}")

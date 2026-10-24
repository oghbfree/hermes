"""Drive due nudges via _fb_reply3.py sequentially; mark nudged only on SENT."""
import subprocess, sys, os, json, time

pkg = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0, pkg)
sys.path.insert(0, os.path.dirname(pkg))
from fb_sales_ops import BuyerThreads

PY = r'C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe'
bt = BuyerThreads()
due = bt.due_for_nudge()

# keyed by thread id -> (buyer keyword for row match, custom text or None for auto nudge_text)
targets = [
    ("nii_xbox360games", "Nii", None),
    ("ananman-ingco-gluegun", "Ananman", None),
    ("hellen-magnumplus-talos-690", "Hellen", None),
    ("richard-panasonic-stereo", "Richard", None),
    ("michael-kwesi-karcher-900", "Michael Kwesi", None),
    ("amuzu-bosch-pst50a", "Amuzu", "Hi Amuzu - just checking you saw my last message. That Bosch PST 50a jigsaw sold, but we have other drills and jigsaws in stock, happy to send photos and prices. WhatsApp 0204252252."),
]

statuses = {}
for tid, buyer_kw, custom in targets:
    t = next((x for x in due if (x.get("id") == tid)), None)
    if t is None:
        best = None
        for x in bt.d["threads"]:
            if x.get("id") == tid:
                best = x
                break
        t = best
    if not t:
        statuses[tid] = "NOT_IN_STORE"
        continue
    n = (t.get("nudges_sent") or 0) + 1
    text = custom or bt.nudge_text(t, n)
    r = subprocess.run([PY, os.path.join(pkg, "_fb_reply3.py"), buyer_kw, text],
                       capture_output=True, text=True, timeout=180, cwd=pkg)
    out = (r.stdout or "") + (r.stderr or "")
    tail = [ln for ln in out.splitlines() if ln.startswith("RESULT") or ln.startswith("HEADER") or ln.startswith("CLICK")]
    print(f"== {tid} (nudge {n}): tail={tail}")
    print("   last:", out.strip().splitlines()[-1][:120] if out.strip() else "NO_OUTPUT")
    if "RESULT: SENT" in out:
        try:
            bt = BuyerThreads()
            bt.mark_nudged(tid)
            statuses[tid] = "MARKED"
        except Exception as e:
            statuses[tid] = f"SENT_BUT_MARK_ERR {e!r}"
    else:
        statuses[tid] = "NOT_SENT"
    time.sleep(8)

print("\nNUDGE SUMMARY:")
for tid, s in statuses.items():
    print(f"  {tid}: {s}")

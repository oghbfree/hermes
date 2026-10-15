import subprocess, time, sys

PY = r"C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe"
PKG = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package"

batch = [
    (8117961,  "10W LED, 800 lumens, IP65 outdoor rated, PIR motion sensor 6-12m, die-cast aluminium body"),
    (8930090,  "10in drop-forged steel, tongue and groove adjustment, bi-material comfort grip, black oxide finish"),
    (16749562, "0-150mm range, 0.01mm resolution, stainless steel, digital LCD, mm/inch switch, zero function"),
    (12574690, "4 interchangeable heads 2.4/3.2/4.0/4.8mm, 60 assorted rivets, heavy-duty, changing wrench included"),
    (12261650, "4kg drop-forged 45# carbon steel head, 900mm fibreglass handle, heat treated"),
]

results = []
fails = 0
for jid, spec in batch:
    cmd = [PY, "fb_post_run.py", str(jid), spec]
    r = subprocess.run(cmd, cwd=PKG, capture_output=True, text=True, timeout=420)
    out = (r.stdout or "") + (r.stderr or "")
    ok = "published" in out and "GAVE UP" not in out
    results.append((jid, ok, out[-400:]))
    print("=" * 20, jid, "OK" if ok else "FAIL")
    print(out[-1500:])
    if ok:
        fails = 0
        time.sleep(50)  # anti-velocity gap between listings
    else:
        fails += 1
        if fails >= 2:
            print("TWO CONSECUTIVE FAILURES - ENDING RUN")
            break
        time.sleep(20)

print("\nRUN SUMMARY:")
for jid, ok, _ in results:
    print(jid, "PUBLISHED" if ok else "FAILED")

import os, glob, time
BASE = r'C:\Users\User\AppData\Local\hermes\cron\output'
CUTOFF = time.time() - 86400
jobs = glob.glob(os.path.join(BASE, '*'))
jobs.sort()
results = []
for j in jobs:
    if not os.path.isdir(j): continue
    job_id = os.path.basename(j)
    for f in os.listdir(j):
        if not f.endswith('.md'): continue
        fp = os.path.join(j, f)
        if os.path.getmtime(fp) > CUTOFF:
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    lines = [next(fh).strip() for _ in range(12)]
                results.append((job_id, f, os.path.getmtime(fp), lines))
            except Exception as e:
                results.append((job_id, f, os.path.getmtime(fp), [f'ERROR: {e}']))
results.sort(key=lambda x: x[2], reverse=True)
for job_id, f, mtime, lines in results[:25]:
    print(f"=== {job_id}/{f} ===")
    for line in lines:
        print(line)
    print()

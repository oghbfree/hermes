import json, subprocess, os

export_dir = r"C:\Users\User\.hermes\workspace\farm\farmos_export"
os.makedirs(export_dir, exist_ok=True)

# Clear old files
for f in os.listdir(export_dir):
    os.remove(os.path.join(export_dir, f))

cookie_jar = r"C:\Users\User\AppData\Local\Temp\farmos_cookies.jar"

endpoints = [
    "asset/land",
    "asset/plant",
    "asset/equipment",
    "asset/structure",
    "asset/seed",
    "asset/animal",
    "log/activity",
    "log/input",
    "log/harvest",
    "log/observation",
    "log/seeding",
    "log/purchase",
    "log/sale",
    "log/maintenance",
    "taxonomy_term/plant_type",
    "taxonomy_term/season",
    "taxonomy_term/unit",
]

for ep in endpoints:
    fname = ep.replace("/", "_") + ".json"
    out_path = os.path.join(export_dir, fname)
    url = f"https://2real.farmos.net/api/{ep}"
    cmd = [
        "curl", "-s",
        "-b", cookie_jar,
        "-H", "Accept: application/vnd.api+json",
        url, "-o", out_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        # Quick validate
        try:
            with open(out_path) as f:
                data = json.load(f)
            count = len(data.get("data", []))
            print(f"OK: {ep} -> {fname} ({count} records)")
        except:
            print(f"PARSE_ERR: {ep} -> {fname}")
    else:
        print(f"FAIL: {ep} (exit={result.returncode}, err={result.stderr.strip()})")

print("\nDone.")

import json, os

export_dir = r"C:\Users\User\.hermes\workspace\farm\farmos_export"
farm_dir = r"C:\Users\User\.hermes\workspace\farm"

files = {
    "asset_land.json": ("plots.md", "Plots / Land Assets"),
    "asset_plant.json": ("crops.md", "Crops / Plant Assets"),
    "asset_equipment.json": ("equipment.md", "Equipment"),
    "asset_structure.json": ("structures.md", "Structures"),
    "asset_animal.json": ("animals.md", "Animals"),
    "log_purchase.json": ("purchases.md", "Purchase Log"),
    "log_sale.json": ("sales.md", "Sales Log"),
    "log_harvest.json": ("harvests.md", "Harvest Log"),
    "log_seeding.json": ("seedings.md", "Seeding Log"),
    "log_activity.json": ("activities.md", "Activity Log"),
    "log_observation.json": ("observations.md", "Observation Log"),
    "log_input.json": ("inputs.md", "Input Log"),
    "log_maintenance.json": ("maintenance.md", "Maintenance Log"),
}

for src, (dst, title) in files.items():
    src_path = os.path.join(export_dir, src)
    dst_path = os.path.join(farm_dir, dst)
    
    if not os.path.exists(src_path):
        print(f"SKIP {src} (not found)")
        continue
    
    with open(src_path) as f:
        data = json.load(f)
    
    items = data.get("data", [])
    
    lines = [f"# {title}\n", "| Name | farmOS ID |\n", "|------|-----------|\n"]
    for item in items:
        a = item.get("attributes", {})
        name = a.get("name", a.get("label", "?"))
        lines.append(f"| {name} | {item['id']}\n")
    
    with open(dst_path, "w") as f:
        f.writelines(lines)
    
    print(f"{dst}: {len(items)} records")

print("\nAll done.")

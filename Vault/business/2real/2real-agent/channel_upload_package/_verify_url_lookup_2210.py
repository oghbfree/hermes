"""READ-ONLY verification: resolve today's published listings back to their
/marketplace/item/ URL using the new title-anchored resolver. Nothing is shared."""
import sys, json, os, time
sys.path.insert(0, r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package")
os.environ["FB_CDP_URL"] = "http://127.0.0.1:9222"
import fb_share_groups as FS

pkg = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package"
queue = json.load(open(os.path.join(pkg, "next50.json"), encoding="utf-8"))
titles = []
for jid in ["16537799", "16460171", "12354004", "7776847", "16680576"]:
    item = next(x for x in queue if str(x["jiji_id"]) == jid)
    t = item["title"]
    if "Imported" not in t:
        suffix = " — UK Imported, Quality Checked"
        t = t + suffix if len(t) + len(suffix) <= 95 else t[:95]
    titles.append((jid, t))

# connect once to the selling tab
FS.C.connect(substr="facebook.com", exclude_substr="marketplace/create")

for jid, title in titles:
    u = FS.resolve_listing_url_by_title(title)
    print(f"{jid} | {title[:70]} -> {u or 'NOT FOUND'}")
    time.sleep(2)
print("VERIFICATION DONE")

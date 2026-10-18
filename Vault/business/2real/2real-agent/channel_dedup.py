"""
Unified channel dedup helper. Both FB Marketplace and WhatsApp crons import this
so duplicates are IMPOSSIBLE across every post, without re-scanning live pages.

Usage:
    from channel_dedup import Registry
    reg = Registry()                          # loads the master registry
    reg.is_fb_posted(jid)                     # True if already on FB
    reg.is_wa_posted(jid)                     # True if already in WA catalogue
    reg.mark_fb_posted(jid)                   # record a successful FB post
    reg.mark_wa_posted(jid, title)            # record a successful WA catalogue add
    reg.posted_anywhere(jid)                  # True if on EITHER channel
"""
import json, os, time

AGENT = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent"
PKG = os.path.join(AGENT, "channel_upload_package")
MASTER = os.path.join(AGENT, "channel_posted_master.json")

class Registry:
    def __init__(self):
        self.master = self._load()

    def _load(self):
        if os.path.exists(MASTER):
            m = json.load(open(MASTER, encoding="utf-8"))
            # 17 Oct 26: stored IDs were ints (pre-normalisation) so str queries
            # returned False — normalise on load too, not just on query.
            for ch in m.get("channels", {}).values():
                if "posted_ids" in ch:
                    ch["posted_ids"] = [str(x) for x in ch["posted_ids"]]
            return m
        return {"channels": {"facebook_marketplace": {"posted_ids": []},
                             "whatsapp_catalogue": {"posted_ids": [], "existing_titles": []}}}

    def _save(self):
        json.dump(self.master, open(MASTER, "w", encoding="utf-8"), indent=2)

    # 17 Oct 26: IDs normalised to str everywhere — int/str mix made posted_anywhere()
    # silently return False for items that WERE posted (registry gap, nearly re-posted).
    def is_fb_posted(self, jid):  return str(jid) in self.master["channels"]["facebook_marketplace"]["posted_ids"]
    def is_wa_posted(self, jid):  return str(jid) in self.master["channels"]["whatsapp_catalogue"]["posted_ids"]
    def is_wa_title(self, title):
        t = title.lower()
        return any(t in e.lower() for e in self.master["channels"]["whatsapp_catalogue"]["existing_titles"])
    def posted_anywhere(self, jid): return self.is_fb_posted(jid) or self.is_wa_posted(jid)

    def mark_fb_posted(self, jid):
        arr = self.master["channels"]["facebook_marketplace"]["posted_ids"]
        jid = str(jid)
        if jid not in arr: arr.append(jid)
        self.master["channels"]["facebook_marketplace"]["count"] = len(arr)
        self._save()

    def mark_wa_posted(self, jid, title=""):
        arr = self.master["channels"]["whatsapp_catalogue"]["posted_ids"]
        jid = str(jid)
        if jid not in arr: arr.append(jid)
        self.master["channels"]["whatsapp_catalogue"]["count"] = len(arr)
        if title and not self.is_wa_title(title):
            self.master["channels"]["whatsapp_catalogue"]["existing_titles"].append(title)
        self._save()

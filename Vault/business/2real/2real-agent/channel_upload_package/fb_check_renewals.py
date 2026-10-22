#!/usr/bin/env python3
"""fb_check_renewals.py — FB Marketplace renew/expiry audit for 2Real.

REALITY (verified 22/10/26 on the live selling page):
- FB Marketplace has NO manual "Renew" button for ACTIVE listings — FB keeps active
  listings live until sold/expired and refreshes them automatically.
- The "More options" menu = Mark as sold / pending, Share, Delete (no Renew).
- A "Renew" action ONLY appears when a listing is genuinely EXPIRED (FB still
  shows "Renew"/"Sell again" on some expired items).

So this script's job is HONESTLY:
1. Walk the selling page; report listing STATUS (active vs expired/inactive/paused).
2. If any EXPIRED/INACTIVE listing exists, click its Renew/Sell-again action (cap RENEW_CAP).
3. Report the active count + oldest listings (candidates for an edit-refresh if H wants
   to manually touch recency — edit-refresh is NOT automated here; it's risky at the
   15/day posting cap).

Usage:
  python fb_check_renewals.py            # scan; renew any expired (capped)
  python fb_check_renewals.py --dry-run  # report only
Requires persistent :9222 browser logged into the selling profile.
"""
import sys, os, time, json, argparse

pkg = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0, pkg)
os.environ.setdefault('FB_CDP_URL', 'http://127.0.0.1:9222')
import cdp_harness as C

RENEW_CAP = 5
SLEEP = 8


def scan():
    """Return dict {active: N, expired: N, others: [...], renew_buttons: N}."""
    txt = (C.js('document.body.innerText') or '')
    statuses = {}
    for kw in ['Active', 'Expired', 'Inactive', 'Paused', 'Pending', 'Archived']:
        statuses[kw] = txt.count(kw)
    renew_btns = (C.js('''(() => {
      let n=0;
      document.querySelectorAll('div[role=button],a[role=link],span[role=button],span').forEach(e=>{
        const t=(e.innerText||'').trim();
        if(t && t.length<35 && /^\\s*(renew|sell again|re-activate|reactivate|extend)\\b/i.test(t)) n++;
      });
      return n;
    })()''') or 0)
    return {'text_len': len(txt), 'statuses': statuses, 'renew_buttons': int(renew_btns)}


def click_renew(i):
    return C.js(f"""(() => {{
      const els=[...document.querySelectorAll('div[role=button],a[role=link],span[role=button],span')];
      const hits=els.filter(e=>{{
        const t=(e.innerText||'').trim();
        return t && t.length<35 && /^\\s*(renew|sell again|re-activate|reactivate|extend)\\b/i.test(t);
      }});
      if(hits.length<= {i}) return false;
      (hits[{i}].closest('div[role=button]')||hits[{i}]).click(); return true;
    }})()""")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--max', type=int, default=RENEW_CAP)
    args = ap.parse_args()

    C.connect(substr='facebook.com', exclude_substr='marketplace/create')
    C.goto_url('https://www.facebook.com/marketplace/you/selling')
    C.wait_for_load(); time.sleep(6)

    s = scan()
    print(f'Page len: {s["text_len"]}')
    print('Status counts:', json.dumps(s['statuses']))
    print(f'Renew-able buttons: {s["renew_buttons"]}')

    if args.dry_run:
        print('DRY RUN — nothing clicked.')
        return 0

    if s['renew_buttons'] == 0:
        print('No expired listings with a Renew action — FB auto-renews active listings. Nothing to do.')
        return 0

    done = 0
    for i in range(min(s['renew_buttons'], args.max)):
        if click_renew(i):
            print(f'Renewed #{i+1}')
            done += 1
            time.sleep(SLEEP)
        else:
            break
    print(f'DONE — renewed {done} expired listing(s).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
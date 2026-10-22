#!/usr/bin/env python3
"""fb_share_groups.py — share just-published 2Real Marketplace listings into H's
buy/sell groups (GHANA MARKET PLACE, ACCRA BUY AND SELL) right after publishing.

Mechanics verified live on 22/10/26 (read-only inspection, nothing posted):
  1. listing page -> Share button (aria-label starts with 'Share ')
  2. dialog -> 'Share to: Group' row
  3. 'Search for groups' input -> type exact group name
  4. the group row appears (public group, exact title) -> click row
  5. 'Share now' button posts the share into the group

Design rules:
- FAILURE-TOLERANT: sharing must never fail the post; the Marketplace listing is
  already live before this runs. Every failure is logged and skipped.
- Anti-ban: one share at a time, 8s between groups, sleeps between dialogs.
- Runs for the SAME listing that was just published (share goes out with the
  listing link, so the group post links back to the Marketplace item).

Usage (called from fb_post_run.py after PUBLISHED; also standalone):
  python fb_share_groups.py <item_url> [<item_url2> ...]
  env FB_SHARE_GROUPS=1            # enable (default off for safety)
Requires persistent :9222 browser logged into the selling profile.
"""
import sys, os, time, json, argparse

pkg = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0, pkg)
os.environ.setdefault('FB_CDP_URL', 'http://127.0.0.1:9222')
import cdp_harness as C

# H's buy/sell groups (exact titles from the live picker, 22/10/26)
GROUPS = ["GHANA MARKET PLACE", "ACCRA BUY AND SELL"]
SLEEP_BETWEEN = 8

JS_BY_TEXT = """(label, exact) => {{
  const want = String({label!r}).trim();
  const norm = s => s.replace(/\\s+/g,' ').trim().toLowerCase();
  // 1) any clickable element containing the text (whole document; FB dialog shells
  //    pollute [role=dialog] arrays so we do NOT scope there)
  for (const e of [...document.querySelectorAll('div[role=button],a[role=link],span[role=button],a[role=option],div[role=option],div[role=checkbox],div[role=radio],div[role=menuitem]')]) {{
    const t = (e.innerText||'').trim().replace(/\\s+/g,' ');
    if ({exact} ? t.toLowerCase()===want.toLowerCase() : t.toLowerCase().includes(want.toLowerCase())) {{
      const rc = e.getBoundingClientRect();
      if (rc.width>0 && rc.height>0) return JSON.stringify({{x:rc.x+rc.width/2, y:rc.y+rc.height/2}});
    }}
  }}
  // 2) visible leaf node with exact text (group names are bare SPANs)
  for (const e of [...document.querySelectorAll('span,div,a')]) {{
    if (e.children && e.children.length>0) continue;
    if (norm(e.innerText||'')!==want.toLowerCase()) continue;
    if (!e.offsetParent) continue;
    const rc = e.getBoundingClientRect();
    if (rc.width>0 && rc.height>0) return JSON.stringify({{x:rc.x+rc.width/2, y:rc.y+rc.height/2}});
  }}
  return null;
}}"""


def click_by_text(label, exact=True, tries=8, delay=1.5):
    js_bool = 'true' if exact else 'false'
    for k in range(tries):
        r = C.js(JS_BY_TEXT.format(label=label, exact=js_bool))
        if r:
            p = json.loads(r)
            C.click_at_xy(int(p['x']), int(p['y']))
            return True
        time.sleep(delay)
    return False


def open_share_dialog():
    """Return True if the Share dialog (with 'Group' share-to) is visible."""
    C.js("""(() => {
      const b=[...document.querySelectorAll('div[role=button],a[role=link],span[role=button]')]
        .find(e=>(e.getAttribute('aria-label')||'').startsWith('Share ') || ((e.innerText||'').trim()==='Share'));
      if(!b) return false; b.click(); return true;
    })()""")
    time.sleep(3.5)
    return 'Group' in dialog_text()


def click_share_to_group():
    C.js("""(() => {
      const ds=[...document.querySelectorAll('[role=dialog]')].filter(d=>d.offsetParent!==null);
      if(!ds.length) return;
      const d=ds[ds.length-1];
      const g=[...d.querySelectorAll('div[role=button],span[role=button],div[role=menuitem]')]
        .find(e=>(e.innerText||'').trim()==='Group');
      if(g) g.click();
    })()""")
    # the picker (search box) appears async — poll for it
    for _ in range(10):
        if 'Search for groups' in dialog_text() or C.js("""(() => {
            const ds=[...document.querySelectorAll('[role=dialog]')].filter(d=>d.offsetParent!==null);
            return ds.length ? !!ds[ds.length-1].querySelector('input[placeholder="Search for groups"],input') : false;
        })()""") is True:
            time.sleep(1.0)
            return True
        time.sleep(1.0)
    return False


def type_group_search(name):
    r = C.js("""(() => {
      const ds=[...document.querySelectorAll('[role=dialog]')].filter(d=>d.offsetParent!==null);
      const d=ds[ds.length-1]; if(!d) return 'nodialog';
      const i=d.querySelector('input[placeholder="Search for groups"],input');
      if(!i) return 'noinput';
      const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
      setter.call(i, %r);
      i.dispatchEvent(new Event('input',{bubbles:true}));
      i.dispatchEvent(new Event('change',{bubbles:true}));
      return 'typed';
    })()""" % name)
    time.sleep(3)
    return r


def dialog_text():
    return C.js("""(() => {
      const ds=[...document.querySelectorAll('[role=dialog]')].filter(d=>d.offsetParent!==null);
      return ds.length ? (ds[ds.length-1].innerText||'') : '';
    })()""")


def close_dialog():
    C.js("""(() => {
      document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));
      document.dispatchEvent(new KeyboardEvent('keyup',{key:'Escape',bubbles:true}));
    })()""")
    time.sleep(1.5)


def share_one_listing(url):
    """Share one listing to all GROUPS. Returns (ok_count, messages)."""
    ok = 0; msgs = []
    C.goto_url(url)
    try: C.wait_for_load()
    except Exception: pass
    time.sleep(6)
    for g in GROUPS:
        try:
            if not open_share_dialog():
                msgs.append(f'{g}: no share dialog'); close_dialog(); continue
            if not click_share_to_group():
                msgs.append(f'{g}: group picker did not open'); close_dialog(); continue
            type_group_search(g)
            if not click_by_text(g, exact=True, tries=6, delay=1.5):
                msgs.append(f'{g}: group row not found (search: {g})'); close_dialog(); continue
            time.sleep(1.5)
            if not click_by_text('Share now', exact=True, tries=6, delay=1.5):
                msgs.append(f'{g}: Share now not found'); close_dialog(); continue
            time.sleep(2)
            ok += 1
            msgs.append(f'{g}: SHARED')
            close_dialog()
            time.sleep(SLEEP_BETWEEN)
        except Exception as e:
            msgs.append(f'{g}: EXC {e!r}'); close_dialog()
    return ok, msgs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('urls', nargs='*')
    ap.add_argument('--url', action='append', default=[])
    args = ap.parse_args()
    urls = list(args.urls) + list(args.url or [])
    if os.environ.get('FB_SHARE_GROUPS', '').strip().lower() in ('0', 'off', 'no', 'false'):
        print('disabled: FB_SHARE_GROUPS=0/off'); return 0
    if not urls:
        print('usage: fb_share_groups.py <item_url> [...]'); return 2
    C.connect(substr='facebook.com', exclude_substr='marketplace/create')
    total_ok = 0
    for u in urls:
        ok, msgs = share_one_listing(u)
        total_ok += ok
        print(f'{u}: ' + ' | '.join(msgs))
    print(f'DONE — {total_ok}/{len(GROUPS)*len(urls)} group shares')
    return 0


if __name__ == '__main__':
    sys.exit(main())

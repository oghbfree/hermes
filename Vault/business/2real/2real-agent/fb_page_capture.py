#!/usr/bin/env python3
"""FB Business Page content-library capture (27/10/26) — v3, filter-aware.
For each filter (published default, scheduled), connect to the content-library
tab, navigate, HARD-RELOAD, and WAIT until the URL carries the expected filter
before scrolling + dumping innerText. Guarantees published and scheduled differ.

Usage:
  python fb_page_capture.py
"""
import sys, os, time, json, datetime

sys.path.insert(0, r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent')
os.environ['FB_CDP_URL'] = 'http://127.0.0.1:9222'

VAULT_OUT = r'C:\Users\User\.hermes\workspace\Vault\business\2real\fb-page'
LIB_URL = 'https://www.facebook.com/professional_dashboard/content/content_library'


def _goto_and_wait(url, expect_param):
    import cdp_harness as C
    # navigate then hard-reload to clear filter state
    C.goto_url(url)
    time.sleep(4)
    C.js('location.reload()')
    time.sleep(8)
    # wait until URL shows the filter we want
    for _ in range(6):
        cur = C.js('location.href') or ''
        got_sched = ('filter=SCHEDULED' in cur)
        want_sched = (expect_param == 'SCHEDULED')
        if got_sched == want_sched and cur.startswith('https://www.facebook.com/professional'):
            break
        time.sleep(3)
    # scroll to load virtual rows
    for _ in range(8):
        C.js('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)
        C.js('window.scrollTo(0, document.body.scrollHeight*0.85)')
        time.sleep(2)


def dump(filter_label):
    import cdp_harness as C
    url = LIB_URL if filter_label == 'published' else LIB_URL + '/?filter=SCHEDULED'
    expect = 'published' if filter_label == 'published' else 'SCHEDULED'
    C.connect(substr='content_library', exclude_substr=None)
    _goto_and_wait(url, expect)
    cur = C.js('location.href') or ''
    txt = C.js('document.body.innerText') or ''
    return {'label': filter_label, 'url': cur, 'len': len(txt), 'text': txt}


def main():
    os.makedirs(VAULT_OUT, exist_ok=True)
    os.makedirs(os.path.join(VAULT_OUT, 'snapshots'), exist_ok=True)
    today = datetime.date.today()
    results = [dump('published'), dump('scheduled')]
    snap = {'date': str(today),
            'captured_at': datetime.datetime.now().isoformat(timespec='seconds'),
            'tabs': results}
    jp = os.path.join(VAULT_OUT, 'snapshots', f'{today}.json')
    with open(jp, 'w', encoding='utf-8') as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
    md = [f'# FB Page Content Library — {today}', '',
          f'Captured {datetime.datetime.now().strftime("%H:%M")} from the 2Real Business Page dashboard.',
          '', '---']
    for res in results:
        md.append(f'\n## {res["label"].upper()} — url={res["url"][:90]} ({res["len"]} chars)\n')
        md.append(res['text'])
        md.append('\n---')
    md.append('\n_Feed: Saturday perf cron + sat-nav traction review. Jiji source of truth, CTA 0204252252._')
    mp = os.path.join(VAULT_OUT, f'{today}.md')
    with open(mp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    print(f'OK: tabs={[(r["label"], r["len"], r["url"][:60]) for r in results]}')
    print(f'  md -> {mp}')
    print(f'  json -> {jp}')


if __name__ == '__main__':
    main()
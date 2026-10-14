"""Driver: posts ready items from fb_ready_131026.json via post_one_checked.
Posts max 3 per run (anti-ban). Sleep 180s between items. Appends fb_posted.json on PUBLISHED.
Usage: python fb_driver_1310.py <max_posts> <out_log>
"""
import sys, os, json, time

pkg = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package'
sys.path.insert(0, pkg)
import cdp_harness as C

G = {'js': C.js, 'goto_url': C.goto_url, 'wait_for_load': C.wait_for_load,
     'click_at_xy': C.click_at_xy, 'time': time, 'json': json, 'base64': __import__('base64'), 'os': os}
src = open(os.path.join(pkg, 'fb_post_lib.py'), encoding='utf-8').read()
src = src.replace("assert 'js' in globals(), 'run via exec in harness main'", "")
exec(src, G)

log = open(sys.argv[2], 'a', encoding='utf-8')
def L(msg):
    print(msg, flush=True)
    log.write(msg + '\n'); log.flush()

import fb_post_run as R

def add_posted(jid):
    p = os.path.join(pkg, 'fb_posted.json')
    arr = json.load(open(p))
    if jid not in arr:
        arr.append(jid)
        json.dump(arr, open(p, 'w'))

def main():
    max_posts = int(sys.argv[1])
    ready = json.load(open(os.path.join(pkg, 'fb_ready_131026.json'), encoding='utf-8'))
    posted_ids = json.load(open(os.path.join(pkg, 'fb_posted.json')))
    pending = [r for r in ready if r['jiji_id'] not in posted_ids]
    L('pending: %s' % [r['jiji_id'] for r in pending])
    done = 0
    results = []
    for r in pending:
        if done >= max_posts:
            L('CAP reached (%d) — stopping' % max_posts)
            break
        jid = r['jiji_id']
        L('posting %s | %s | %s | cat: %s | cond: %s | photo: %s' %
          (jid, r['title'][:60], r['price'], r['category'], r['condition'], os.path.basename(r['photo_var'])))
        rc = 'FAIL exc'
        for attempt in range(3):
            try:
                rc = R.post_one_checked(r['title'], r['price'], r['photo_var'],
                                           r['category'], r['desc'], r['condition'])
            except Exception as e:
                rc = 'FAIL exc: %r' % e
            L('attempt %d -> %s' % (attempt, rc))
            if rc == 'PUBLISHED':
                break
            time.sleep(8)
        results.append((jid, rc))
        if rc == 'PUBLISHED':
            add_posted(jid)
            L('LOGGED %s' % jid)
            done += 1
            time.sleep(180)
        else:
            L('GAVE UP %s' % jid)
            time.sleep(30)
    L('RUN COMPLETE: %s' % results)

if __name__ == '__main__':
    main()

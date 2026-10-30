"""Price-drop executor (29 Oct 26): loop over approved jiji_ids, walk the Jiji
edit wizard, set the new price, submit, and verify on the ad page. One CDP session.

Usage: python fb_apply_price_drops.py  (item map is embedded below)
"""
import sys, os, json, time
BASE = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent'
sys.path.insert(0, BASE)
os.environ['FB_CDP_URL'] = 'http://127.0.0.1:9222'
import cdp_harness as C

# jiji_id -> new price (approved by H 29 Oct 26; first item 8930090 already done)
DROPS = [
    (8117961,  279, 'Stanley 10W LED PIR Floodlight'),
    (16749562, 270, 'Halfords Digital Vernier Caliper'),
    (12574690, 270, 'Rolson Four Head Rivet Gun'),
    (12261650, 270, 'INGCO Stone Hammer 4kg'),
    (12706937, 270, 'Stanley Graphite Jacketed Hammer'),
    (12729154, 270, 'Norton Clipper Diamond Blade'),
    (7652303,  256, 'Darlac Expert Bypass Pruner'),
]

def js_set_price(newprice):
    r = C.js('''(() => {
      const p = document.querySelector('input[name=price]');
      if (!p) return 'no-price-input';
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      setter.call(p, '%s');
      p.dispatchEvent(new Event('input', {bubbles: true}));
      p.dispatchEvent(new Event('change', {bubbles: true}));
      const post = [...document.querySelectorAll('button')].find(b => /post ad/i.test(b.innerText));
      if (post) { post.click(); return 'set-and-post'; }
      const nxt = [...document.querySelectorAll('button')].find(b => /next/i.test(b.innerText));
      if (nxt) { nxt.click(); return 'set-and-next'; }
      return 'set-no-btn';
    })()''' % newprice)
    return r

for jid, newprice, label in DROPS:
    try:
        url = 'https://jiji.com.gh/edit-free-ad-%d.html' % jid
        C.goto_url(url)
        time.sleep(5)
        r = js_set_price(newprice)          # usually clicks Next to price step
        print(jid, label, '| step1:', r, flush=True)
        time.sleep(4)
        if r == 'set-and-next':
            r2 = js_set_price(newprice)     # now on price step -> set + Post ad
            print(jid, '| step2:', r2, flush=True)
            time.sleep(8)
        elif r == 'set-and-post':
            time.sleep(8)
        # verify: read current URL + price shown on the page
        v = C.js('''(() => {
          const m = document.body.innerText.match(/GH.\s*\n?\s*(\d[\d,]*)/);
          return JSON.stringify({url: location.href, price: m ? m[1] : null});
        })()''')
        print(jid, label, '| verify:', v if isinstance(v, str) else json.dumps(v), flush=True)
        time.sleep(5)
    except Exception as e:
        print(jid, '| ERROR', repr(e), flush=True)
        time.sleep(4)
print('DONE', flush=True)

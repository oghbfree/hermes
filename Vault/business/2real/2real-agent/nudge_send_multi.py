#!/usr/bin/env python3
"""nudge_send_multi.py — send ONE nudge per DISTINCT saved item for leads who saved
multiple items. Bypasses the user-level dedup (the bug: a saved 2nd item was dropped
because the user was already nudged once). Dedups at (user_id, advert_id) granularity
so each distinct item gets exactly one nudge, and future runs won't re-send any item.

Usage: python nudge_send_multi.py [--dry N]  (sends all rows in _savedads_multi_plan.json)
"""
import sys, os, time, json
from datetime import datetime
BASE = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent'
sys.path.insert(0, BASE)
os.environ['FB_CDP_URL'] = 'http://127.0.0.1:9222'
import cdp_harness as C

PLAN = os.path.join(BASE, '_savedads_multi_plan.json')
SENT = os.path.join(BASE, 'nudge_sent_log.json')   # main log (user-level, authoritative for future harvest)
ITEMLOG = os.path.join(BASE, 'nudge_multi_sent_log.json')  # item-level coverage log
CTA = '0204252252'
COMP = '.qa-messenger-send-message-textarea[contenteditable=true], .b-messenger-input[contenteditable=true]'

def load(p):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return []
def save(p, obj):
    tmp = p + '.tmp'
    with open(tmp,'w',encoding='utf-8') as f: json.dump(obj,f,ensure_ascii=False,indent=1)
    os.replace(tmp, p)

def build_msg(lead):
    item = (lead.get('item') or '').strip()
    name = (lead.get('name') or '').strip()
    # Variant nudge for leads who saved MULTIPLE catalogue items (29 Oct 26): this
    # is the 2nd/a subsequent nudge in that person's thread, so frame it around
    # catalogue browsing rather than repeating "the item you saved".
    greet = f"Hi {name}!" if name else "Hi!"
    return (f"{greet} Thanks for checking out my catalogue — the {item} is also "
            f"available if you're still browsing. Pickup Oyarifa or Dome, delivery "
            f"via Yango/Uber arranged. WhatsApp {CTA} if you'd like details. No pressure!")

def send_one(lead):
    chat_url = lead.get('chat_url') or ''
    uid = lead.get('user_id')
    if not chat_url or not uid:
        return 'skip', 'no chat_url/user_id'
    msg = build_msg(lead)
    try:
        C.goto_url('https://jiji.com.gh' + chat_url)
        try: C.wait_for_load()
        except: pass
        time.sleep(5)
        if C.js(f"(() => !!document.querySelector('{COMP}'))()") is not True:
            C.js("""(() => { const el=[...document.querySelectorAll('div,li,a,span')].find(e=>(e.innerText||'').trim().startsWith(%s) && e.offsetParent!==null); if(!el) return; const rc=el.getBoundingClientRect(); const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2}); ['mousedown','mouseup','click'].forEach(t=>el.dispatchEvent(ME(t))); })()""" % json.dumps(lead.get('name','')))
            time.sleep(4)
        SET = "(() => { const c=document.querySelector('%s'); if(!c) return 'NOCOMP'; c.focus(); c.innerHTML=''; c.appendChild(document.createTextNode(%s)); c.dispatchEvent(new InputEvent('input',{bubbles:true})); c.dispatchEvent(new InputEvent('input',{bubbles:true})); return 'SET-'+c.innerText.length; })()" % (COMP, json.dumps(msg))
        r = C.js(SET)
        if not r or not str(r).startswith('SET-'):
            return 'fail', f'set text: {r}'
        time.sleep(1.2)
        ENT = "(() => { const c=document.querySelector('%s'); if(!c) return 'NOCOMP'; const kd=new KeyboardEvent('keydown',{key:'Enter',code:'Enter',which:13,keyCode:13,bubbles:true,cancelable:true}); const ku=new KeyboardEvent('keyup',{key:'Enter',code:'Enter',which:13,keyCode:13,bubbles:true,cancelable:true}); c.dispatchEvent(kd); c.dispatchEvent(ku); return (c.innerText||'').trim().length===0?'EMPTY':'HAS-'+c.innerText.length; })()" % COMP
        C.js(ENT)
        time.sleep(4)
        VER = "(() => { const comps=document.querySelectorAll('%s'); const empty=[...comps].every(e=>!(e.innerText||'').trim()); const hasCta=(document.body.innerText||'').includes('%s'); return JSON.stringify({compEmpty:empty,hasCta:hasCta}); })()" % (COMP, CTA)
        v = C.js(VER)
        try:
            vj = json.loads(v or '{}')
            if vj.get('compEmpty') and vj.get('hasCta'):
                return 'ok', 'verified in thread'
            return 'uncertain', f'verify: {v}'
        except Exception:
            return 'uncertain', f'verify parse: {v}'
    except Exception as e:
        return 'fail', str(e)[:120]

def main():
    dry = 0
    if '--dry' in sys.argv:
        try: dry = int(sys.argv[sys.argv.index('--dry')+1])
        except: dry = 1
    plan = load(PLAN)
    itemlog = load(ITEMLOG)
    # item-level dedup: already-sent (uid,advert) pairs
    sent_items = {(str(x.get('user_id')), str(x.get('advert_id'))) for x in itemlog}
    todo = [p for p in plan if (str(p.get('user_id')), str(p.get('advert_id'))) not in sent_items]
    print(f"PLAN: {len(plan)} rows, {len(todo)} to send (after item-level dedup)")
    if dry:
        for p in todo[:dry]:
            print(f"  [dry] {p['user_id']} :: {(p['item'] or '')[:45]}")
        return 0

    C.connect(substr='jiji.com.gh', exclude_substr=None)
    C.goto_url('https://jiji.com.gh/profile/my-clients')
    try: C.wait_for_load()
    except: pass
    time.sleep(3)

    ok=fail=0
    for i,p in enumerate(todo,1):
        rc, detail = send_one(p)
        print(f"[{i}/{len(todo)}] {rc}: uid={p.get('user_id')} :: {(p.get('item') or '')[:40]} | {detail[:50]}")
        if rc=='ok' or rc=='uncertain':
            # log item-level coverage regardless (confirmed delivered OR need manual check -> mark to avoid re-try spam)
            itemlog.append({"name": p.get('name'), "user_id": p.get('user_id'), "advert_id": p.get('advert_id'),
                            "item": p.get('item'), "chat_id": f"{p.get('user_id')}_{p.get('advert_id')}",
                            "state": rc, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            ok += 1
        else:
            fail += 1
        save(ITEMLOG, itemlog)
        if i < len(todo):
            time.sleep(25)
    print(f"\nDONE: {ok} ok/uncertain, {fail} failed. item log: {len(load(ITEMLOG))}")
    return 0 if fail==0 else 1

if __name__=='__main__':
    sys.exit(main())
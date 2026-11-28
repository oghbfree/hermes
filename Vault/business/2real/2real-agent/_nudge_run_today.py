#!/usr/bin/env python3
"""One-off daily batch nudge driver (27 Nov 26 run).
Reuses the proven send mechanic from nudge_send.py. Sends all 50 leads in
_batch50_today.json:
  - fresh leads / contact_view / unanswered_chat -> lead['message'] verbatim
  - repeat saved_ads (user already in sent log, distinct item) -> VARIANT
    catalogue-browsing message (29 Oct rule)
Logs each send to nudge_sent_log.json per-item (timeout-proof) and drops the
lead from nudge_queue.json. ~30s pace.
"""
import sys, os, time, json
from datetime import datetime
BASE = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent'
sys.path.insert(0, BASE)
os.environ['FB_CDP_URL'] = 'http://127.0.0.1:9222'
import cdp_harness as C

BATCH = os.path.join(BASE, '_batch50_today.json')
QUEUE = os.path.join(BASE, 'nudge_queue.json')
SENT  = os.path.join(BASE, 'nudge_sent_log.json')
CTA = '0204252252'
COMP = '.qa-messenger-send-message-textarea[contenteditable=true], .b-messenger-input[contenteditable=true]'

def load(p):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return []
def save(p, obj):
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, p)

def build_variant(lead):
    item = (lead.get('item') or '').strip()
    name = (lead.get('name') or '').strip()
    greet = f"Hi {name}!" if name else "Hi!"
    return (f"{greet} Thanks for checking out my catalogue — the {item} is also "
            f"available if you're still browsing. Pickup Oyarifa or Dome, delivery "
            f"via Yango/Uber arranged. WhatsApp {CTA} if you'd like details. No pressure!")

def send_one(lead, msg):
    chat_url = lead.get('chat_url') or ''
    uid = lead.get('user_id')
    if not chat_url or not uid:
        return 'skip', 'no chat_url/user_id'
    try:
        C.goto_url('https://jiji.com.gh' + chat_url)
        try: C.wait_for_load()
        except Exception: pass
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
        r2 = C.js(ENT)
        time.sleep(4)
        VER = "(() => { const comps=document.querySelectorAll('%s'); const empty=[...comps].every(e=>!(e.innerText||'').trim()); const hasCta=(document.body.innerText||'').includes('%s'); return JSON.stringify({compEmpty:empty,hasCta:hasCta,hasName:(document.body.innerText||'').includes(%s)}); })()" % (COMP, CTA, json.dumps('Hi '+lead.get('name','')))
        v = C.js(VER)
        try:
            vj = json.loads(v or '{}')
            if vj.get('compEmpty') and vj.get('hasCta') and vj.get('hasName'):
                return 'ok', 'verified in thread'
            return 'uncertain', 'verify: ' + (v or '')
        except Exception:
            return 'uncertain', 'verify parse: ' + (v or '')
    except Exception as e:
        return 'fail', str(e)[:120]

def main():
    batch = load(BATCH)
    sent = load(SENT)
    queue = load(QUEUE)
    sent_ids = {str(x.get('user_id')) for x in sent if x.get('user_id') is not None}
    if not batch:
        print("no batch"); return 0
    print(f"BATCH: {len(batch)} leads")
    ok = fail = uncer = skipc = 0
    C.connect(substr='jiji.com.gh', exclude_substr=None)
    C.goto_url('https://jiji.com.gh/profile/my-clients')
    try: C.wait_for_load()
    except Exception: pass
    time.sleep(3)
    for i, lead in enumerate(batch, 1):
        uid = lead.get('user_id')
        is_repeat = str(uid) in sent_ids and lead.get('source') == 'saved_ad'
        msg = build_variant(lead) if is_repeat else (lead.get('message') or '')
        if not msg:
            msg = f"Hi {lead.get('name','')}! The {lead.get('item','item')} is available — pickup Oyarifa or Dome, delivery arranged. WhatsApp {CTA}. Ready to assist!"
        rc, detail = send_one(lead, msg)
        print(f"[{i}/{len(batch)}] {rc}: {lead.get('name','')} (repeat={is_repeat}) | {detail[:55]}")
        if rc == 'ok':
            ok += 1
            status = 'sent'
        elif rc == 'uncertain':
            uncer += 1
            status = 'uncertain'  # plausible delivered; mark contacted to avoid double-nudge
        elif rc == 'skip':
            skipc += 1
            status = 'skip'
        else:
            fail += 1
            status = 'fail'
        if status in ('sent', 'uncertain'):
            # append per-item (timeout-proof)
            sent.append({
                "name": lead.get('name',''),
                "user_id": uid,
                "chat_id": f"{uid}_{lead.get('advert_id')}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "state": status,
                "msg": msg[:80],
                "variant": is_repeat,
            })
            save(SENT, sent)
            # drop this specific (user,advert) lead from queue
            queue = [x for x in queue
                     if not (str(x.get('user_id')) == str(uid) and str(x.get('advert_id')) == str(lead.get('advert_id')))]
            save(QUEUE, queue)
        if i < len(batch):
            time.sleep(28)
    print(f"\nDONE: {ok} ok, {uncer} uncertain, {skipc} skip, {fail} fail. queue now {len(load(QUEUE))}")
    return 0 if fail == 0 else 1

if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""nudge_send.py — send nudges from nudge_queue.json to Jiji leads, verified.

Uses the PROVEN send mechanic (verified 22/10/26 on chang wan):
  goto chat_url -> focus contenteditable composer -> insert message text ->
  single keydown+keyup Enter -> verify composer empty + message text in thread ->
  append to nudge_sent_log.json + remove from queue (timeout-proof per-item).

Cap: NATE default 50/day (system ceiling). Pace ~30s between sends (anti-velocity).

Usage: python nudge_send.py [--max 50] [--dry N]
"""
import sys, os, time, json, subprocess
from datetime import datetime

BASE = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent'
sys.path.insert(0, BASE)
os.environ['FB_CDP_URL'] = 'http://127.0.0.1:9222'
import cdp_harness as C

QUEUE = os.path.join(BASE, 'nudge_queue.json')
SENT = os.path.join(BASE, 'nudge_sent_log.json')
CTA = '0204252252'

COMP = '.qa-messenger-send-message-textarea[contenteditable=true], .b-messenger-input[contenteditable=true]'


def load(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return []


def save(p, obj):
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, p)


def send_one(lead):
    """Send one nudge. Returns ('ok'|'skip'|err, detail)."""
    chat_url = lead.get('chat_url') or ''
    uid = lead.get('user_id')
    if not chat_url or not uid:
        return 'skip', 'no chat_url/user_id'
    msg = lead.get('message') or ''
    if not msg:
        msg = f"Hi {lead.get('name','')}! The {lead.get('item','item')} is available — pickup Oyarifa or Dome, delivery arranged. WhatsApp {CTA}. Ready to assist!"
    try:
        C.goto_url('https://jiji.com.gh' + chat_url)
        try: C.wait_for_load()
        except Exception: pass
        time.sleep(5)
        # open thread if not auto (click the room row)
        if C.js(f"(() => !!document.querySelector('{COMP}'))()") is not True:
            # find a clickable element containing the lead name and click it
            C.js("""(() => {
              const el=[...document.querySelectorAll('div,li,a,span')].find(e=>(e.innerText||'').trim().startsWith(%s) && e.offsetParent!==null);
              if(!el) return; const rc=el.getBoundingClientRect(); const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window,clientX:rc.x+rc.width/2,clientY:rc.y+rc.height/2}); ['mousedown','mouseup','click'].forEach(t=>el.dispatchEvent(ME(t)));
            })()""" % json.dumps(lead.get('name','')))
            time.sleep(4)
        # set text
        SET = "(() => { const c=document.querySelector('%s'); if(!c) return 'NOCOMP'; c.focus(); c.innerHTML=''; c.appendChild(document.createTextNode(%s)); c.dispatchEvent(new InputEvent('input',{bubbles:true})); return c.innerText.length>0?'OK-BUT-PLACEHOLDER':'empty'; })()" % (COMP, json.dumps(msg))
        # fix placeholder: return len count properly
        SET = "(() => { const c=document.querySelector('%s'); if(!c) return 'NOCOMP'; c.focus(); c.innerHTML=''; c.appendChild(document.createTextNode(%s)); c.dispatchEvent(new InputEvent('input',{bubbles:true})); return 'SET-'+c.innerText.length; })()" % (COMP, json.dumps(msg))
        r = C.js(SET)
        if not r or not str(r).startswith('SET-'):
            return 'fail', f'set text: {r}'
        time.sleep(1.2)
        # single Enter
        ENT = "(() => { const c=document.querySelector('%s'); if(!c) return 'NOCOMP'; const kd=new KeyboardEvent('keydown',{key:'Enter',code:'Enter',which:13,keyCode:13,bubbles:true,cancelable:true}); const ku=new KeyboardEvent('keyup',{key:'Enter',code:'Enter',which:13,keyCode:13,bubbles:true,cancelable:true}); c.dispatchEvent(kd); c.dispatchEvent(ku); return (c.innerText||'').trim().length===0?'EMPTY':'HAS-'+c.innerText.length; })()" % COMP
        r2 = C.js(ENT)
        time.sleep(4)
        # verify
        VER = "(() => { const comps=document.querySelectorAll('%s'); const empty=[...comps].every(e=>!(e.innerText||'').trim()); const hasCta=(document.body.innerText||'').includes('%s'); const hasName=(document.body.innerText||'').includes('Hi %s'); return JSON.stringify({compEmpty:empty,hasCta:hasCta,hasName:hasName}); })()" % (COMP, CTA, lead.get('name',''))
        v = C.js(VER)
        try:
            vj = json.loads(v or '{}')
            if vj.get('compEmpty') and vj.get('hasCta') and vj.get('hasName'):
                return 'ok', 'verified in thread'
            return 'uncertain', f'verify: {v}'
        except Exception:
            return 'uncertain', f'verify parse: {v}'
    except Exception as e:
        return 'fail', str(e)[:120]


def main():
    cap = 50
    if '--max' in sys.argv:
        try: cap = int(sys.argv[sys.argv.index('--max')+1])
        except Exception: pass
    dry = 0
    if '--dry' in sys.argv:
        try: dry = int(sys.argv[sys.argv.index('--dry')+1])
        except Exception: dry = 1

    sent = load(SENT)
    sent_ids = {str(x.get('user_id')) for x in sent if x.get('user_id')} | {str(x.get('chat_id') or '').split('_')[0] for x in sent if x.get('chat_id')}
    queue = load(QUEUE)
    todo = [x for x in queue if x.get('chat_url') and str(x.get('user_id')) not in sent_ids]

    ok = skipped = failed = 0
    print(f"TODO: {len(todo)} nudgable leads (cap {cap})")

    C.connect(substr='jiji.com.gh', exclude_substr=None)
    # ensure on a jiji page first
    C.goto_url('https://jiji.com.gh/profile/my-clients')
    try: C.wait_for_load()
    except Exception: pass
    time.sleep(3)

    sent_this_run = []
    for i, lead in enumerate(todo[:cap]):
        if dry and len(sent_this_run) >= dry:
            print(f"[DRY stopping at {dry}] remaining would send {len(todo[:cap])-dry}")
            break
        rc, detail = send_one(lead)
        print(f"[{i+1}/{min(len(todo),cap)}] {rc}: {lead.get('name','')} | {detail[:60]}")
        if rc == 'ok':
            ok += 1
            sent_this_run.append(lead)
            sent.append({
                "name": lead.get('name',''), "user_id": lead.get('user_id'),
                "chat_id": str(lead.get('user_id')) + '_' + str(lead.get('advert_id') or ''),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "state": "sent", "msg": (lead.get('message') or '')[:80],
            })
            save(SENT, sent)
            # drop from queue
            queue = [x for x in queue if str(x.get('user_id')) != str(lead.get('user_id'))]
            save(QUEUE, queue)
        elif rc == 'skip':
            skipped += 1
        else:
            failed += 1
        if i < min(len(todo), cap) - 1 and rc == 'ok':
            time.sleep(28)  # anti-velocity

    print(f"\nDONE: {ok} sent, {skipped} skipped, {failed} failed. Queue now {len(load(QUEUE))}")
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
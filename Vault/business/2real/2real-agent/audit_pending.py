#!/usr/bin/env python3
"""audit_pending.py — full paginated fetch of contact_view(56)+saved_ad(67) lead
lists, dedupe against SENT LOG ONLY (authoritative), report all unsent leads by
source. Does NOT touch the queue (queue is cumulative & unreliable as dedup)."""
import sys, os, time, json
BASE = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent'
sys.path.insert(0, BASE)
os.environ['FB_CDP_URL'] = 'http://127.0.0.1:9222'
import cdp_harness as C

API = 'https://jiji.com.gh/api_web/v1/'
SENT = os.path.join(BASE, 'nudge_sent_log.json')

def load(p):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return []

def _api_get(path):
    return C.js_async(f"(async () => {{ const r = await fetch('{API}{path}', {{credentials:'include'}}); return await r.text(); }})()", timeout=45)

def fetch_all(typ, label):
    out=[]; page=1
    while True:
        path=f'potential-clients?type={typ}' + (f'&page={page}' if page>1 else '')
        body=_api_get(path)
        try: res=json.loads(body or '{}').get('result') or {}
        except Exception as e:
            print(label, page, 'err', e); break
        items=res.get('leads') or []
        for it in items:
            u=it.get('lead_user') or {}; a=it.get('advert') or {}
            name=((u.get('first_name') or '').strip()+' '+(u.get('last_name') or '').strip()).strip()
            chat=u.get('chat_url') or ''
            if not chat and u.get('user_id'):
                chat=f"/profile-messages/{u.get('user_id')}_{a.get('advert_id')}?utm_source=from_leads"
            out.append({"name":name,"user_id":u.get('user_id'),"item":a.get('title') or '',
                        "price":a.get('price'),"advert_id":a.get('advert_id'),"chat_url":chat,
                        "last_seen":u.get('last_seen') or '','source':label})
        nx=res.get('next_url')
        if not nx or not items: break
        page+=1; time.sleep(0.4)
    return out

def main():
    sent=load(SENT)
    sent_ids=set()
    for x in sent:
        if not isinstance(x, dict): continue
        uid=x.get('user_id')
        if uid is None:
            cid=x.get('chat_id')
            if cid and '_' in str(cid): uid=str(cid).split('_')[0]
        if uid is not None:
            try: sent_ids.add(int(str(uid).strip()))
            except: pass
    print(f"sent-log numeric ids: {len(sent_ids)}")
    C.connect(substr='jiji.com.gh', exclude_substr=None)
    C.goto_url('https://jiji.com.gh/profile/my-clients')
    try: C.wait_for_load()
    except Exception: pass
    time.sleep(3)
    all_leads = fetch_all(56,'contact_view') + fetch_all(67,'saved_ad')
    print(f"fetched {len(all_leads)} leads from 56+67")
    # dedupe by user_id across both
    seen=set(); uniq=[]
    for l in all_leads:
        uid=l.get('user_id')
        if not uid: continue
        if uid in seen: continue
        seen.add(uid)
        uniq.append(l)
    print(f"unique leads: {len(uniq)}")
    unsent=[l for l in uniq if l['user_id'] not in sent_ids]
    print(f"UNSENT (not in sent log): {len(unsent)}")
    for i,l in enumerate(unsent,1):
        print(f"{i}. [{l['source']}] uid={l['user_id']} {l['name']} :: {(l['item'] or '')[:38]} last={l['last_seen']}")
    # persist for the sender
    json.dump(unsent, open(os.path.join(BASE,'pending_unsent.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
    print("saved pending_unsent.json")

if __name__=='__main__':
    main()
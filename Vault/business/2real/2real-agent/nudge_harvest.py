#!/usr/bin/env python3
"""nudge_harvest.py — daily Jiji lead harvester for 2Real (feed for the nudger, 50/day).

Pulls ALL warm-lead buckets from the Jiji seller account via the logged-in :9222
browser's internal API (api_web/v1/potential-clients?type=<N>), dedupes against the
sent log + existing queue, writes nudge_queue.json (newest-first) in the format the
nudger already consumes.

Buckets (owner directive 22/10/26 — "the ore is on the my-clients page", API verified):
  type=56 CONTACT VIEWS  — people who saw H's phone number but never messaged (~77 new)
  type=67 SAVED ADS      — people who saved an ad but never followed up (~40 new)
  type=58 CALLBACKS      — people who requested a callback (has phone)
  UNANSWERED CHATS       — api chat/rooms.json where customer wrote last (~28 new)

Each lead has user_id + chat_url (+ phone for callbacks) from the API.

HARVEST ONLY — never sends. The nudge cron sends.
Usage: python nudge_harvest.py [--max 60]
"""
import sys, os, time, json

BASE = r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent'
sys.path.insert(0, BASE)
os.environ['FB_CDP_URL'] = 'http://127.0.0.1:9222'
import cdp_harness as C

QUEUE = os.path.join(BASE, 'nudge_queue.json')
SENT = os.path.join(BASE, 'nudge_sent_log.json')
SELLER_ID = 1249739
CTA = '0204252252'
API = 'https://jiji.com.gh/api_web/v1/'


def load(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return []


# Job-ad vs goods-ad classification (H 28/10/26): a reply to a JOB 2Real advertised
# must not get a "can I sell you this item" nudge (confusing + off-brand), and a
# goods reply must not get a recruitment nudge. Tag each lead with ad_type + give
# each type its own template. Jiji job/service categories + keyword signals.
JOB_CATEGORIES = {'jobs', 'services', 'job vacancies', 'job seekers', 'labor',
                  'domestic help', 'security services', 'freelance', 'recruitment'}
JOB_KEYWORDS = ('hiring', 'vacancy', 'position', 'welder', 'driver', 'cleaner', 'security',
                'nss', 'apply', 'cv', 'salary', 'job', 'recruit', 'labour', 'labor',
                'caregiver', 'mechanic wanted', 'assistant', 'contractor wanted', 'intern',
                'electrician', 'plumber', 'carpenter', 'mason', 'tiler', 'painter', 'apprentice',
                ' shop wiring', 'needed for', 'wanted for', 'required for', 'hiring a', 'lookin for a')


def ad_type_for(title, advert=None):
    """Return 'job' or 'goods' for an ad. Prefer the API advert's category if the
    API returns one (cased/plural-tolerant), else keyword-scan the title."""
    t = (title or '').strip()
    if advert:
        cat = str(advert.get('category') or advert.get('category_name') or '').strip().lower()
        if cat:
            for jc in JOB_CATEGORIES:
                if jc in cat or cat in jc:
                    return 'job'
    tl = t.lower()
    for kw in JOB_KEYWORDS:
        if kw in tl:
            return 'job'
    return 'goods'


def build_message(name, item, socially=False, ad_type='goods'):
    name = (name or '').strip()
    item = (item or '').strip()
    if ad_type == 'job':
        # A JOB ad response: acknowledge the enquiry/app; never pivot to selling goods.
        if socially:
            return (f"Hi {name}! Just checking in on the position you enquired about — "
                    f"happy to update you on the role if you're still interested. "
                    f"Message me on WhatsApp {CTA} when convenient. No pressure!")
        return (f"Hi {name}! Following up on the job/position you were interested in — "
                f"let me know if you'd still like details or if anything's changed. "
                f"Message me on WhatsApp {CTA}.")
    if socially:
        return (f"Hi {name}! Not sure if you're still looking, but the {item} is available "
                f"at a good price — pickup Oyarifa or Dome, delivery via Yango/Uber arranged. "
                f"WhatsApp {CTA} if you'd like details. No pressure!")
    return (f"Hi {name}! The {item} you were interested in is still available — "
            f"pickup Oyarifa or Dome, delivery via Yango/Uber arranged. "
            f"WhatsApp {CTA} to order or see photos of anything else. Ready to assist!")


def _api_get(path):
    return C.js_async(f"(async () => {{ const r = await fetch('{API}{path}', {{credentials:'include'}}); return await r.text(); }})()", timeout=45)


def leads_from_potential_clients(typ):  # 56 contact_view, 67 saved_ad, 58 callback
    # Paginate: follow result.next_url (-> type=T&page=N) until null, ~20/page.
    out = []
    page = 1
    while True:
        path = f'potential-clients?type={typ}' + (f'&page={page}' if page > 1 else '')
        body = _api_get(path)
        try:
            res = json.loads(body or '{}').get('result') or {}
        except Exception as e:
            print(f"type{typ} page{page} parse err:", e)
            break
        items = res.get('leads') or []
        for item in items:
            u = item.get('lead_user') or {}
            a = item.get('advert') or {}
            name = ((u.get('first_name') or '').strip() + ' ' + (u.get('last_name') or '').strip()).strip() or str(u.get('user_id') or '')
            chat = u.get('chat_url') or ''
            if not chat and u.get('user_id'):
                chat = f"/profile-messages/{u.get('user_id')}_{a.get('advert_id')}?utm_source=from_leads"
            ad_title = a.get('title') or ''
            out.append({
                "name": name, "user_id": u.get('user_id'),
                "item": ad_title, "price": a.get('price'),
                "advert_id": a.get('advert_id'), "chat_url": chat,
                "last_seen": u.get('last_seen') or '',
                "phone": u.get('phone') or '',
                "source": {56: 'contact_view', 67: 'saved_ad', 58: 'callback'}[typ],
                "ad_type": ad_type_for(ad_title, a),
            })
        nx = res.get('next_url')
        if not nx or not items:
            break
        page += 1
        time.sleep(0.4)
    return out


def unanswered_chats():
    body = _api_get('chat/rooms.json?sort=active')
    out = []
    try:
        for rm in (json.loads(body or '{}').get('results') or []):
            cust, adv, lmsg = rm.get('user') or {}, rm.get('advert') or {}, rm.get('last_msg') or {}
            if lmsg.get('from_user_id') == SELLER_ID:
                continue
            ad_title = adv.get('title') or ''
            out.append({
                "name": cust.get('user_name') or '', "user_id": cust.get('id'),
                "item": ad_title, "price": adv.get('price'),
                "advert_id": adv.get('id'),
                "chat_url": (f"/profile-messages/{cust.get('id')}_{adv.get('id')}?utm_source=from_leads" if adv.get('id') else ''),
                "last_seen": lmsg.get('date_created') or '', "phone": '',
                "source": "unanswered_chat",
                "ad_type": ad_type_for(ad_title, adv),
            })
    except Exception as e:
        print("chats err:", e)
    return out


def main():
    cap = 60
    if '--max' in sys.argv:
        try: cap = int(sys.argv[sys.argv.index('--max')+1])
        except Exception: cap = 60
    # Ensure the tab is on a Jiji origin BEFORE any API fetch (CORS: fetch to
    # jiji API only works from a jiji page). Navigate to my-clients first.
    C.connect(substr='jiji.com.gh', exclude_substr=None)
    C.goto_url('https://jiji.com.gh/profile/my-clients')
    try: C.wait_for_load()
    except Exception: pass
    time.sleep(4)
    sent = load(SENT)
    existing = load(QUEUE)
    sent_ids = {str(x.get('user_id')) for x in sent if x.get('user_id')} | {str(x.get('chat_id') or '').split('_')[0] for x in sent if x.get('chat_id')}
    # Multi-item saved-ads are logged separately at (user,advert) granularity (29 Oct 26)
    try:
        mlog = json.load(open(os.path.join(BASE, 'nudge_multi_sent_log.json'), encoding='utf-8')) or []
    except Exception:
        mlog = []
    mlog_items = {(str(x.get('user_id')), str(x.get('advert_id'))) for x in mlog if x.get('advert_id')}
    q_ids = {str(x.get('user_id')) for x in existing if x.get('user_id')}
    # Item-level sent coverage for saved_ads (rule 29 Oct 26: one nudge per DISTINCT
    # saved item, not per user). Items already sent carry user_id + advert_id/chat_id.
    sent_items = {(str(x.get('user_id')), str(x.get('advert_id'))) for x in sent if x.get('advert_id')} | \
                 {(str(x.get('chat_id') or '').split('_')[0], str(x.get('chat_id') or '').split('_')[1]) for x in sent if '_' in str(x.get('chat_id') or '')} | mlog_items
    q_items = {(str(x.get('user_id')), str(x.get('advert_id'))) for x in existing if x.get('advert_id')}
    seen = set(); new_leads = []

    def add(lead, social):
        uid = lead.get('user_id')
        if not uid: return False
        k = str(uid)
        if k in seen: return False
        seen.add(k)
        # saved_ads: allow one nudge per distinct (user, advert); skip only if that
        # exact item is already covered. Other buckets stay user-level (one/lead).
        if lead.get('source') == 'saved_ad':
            it = (str(uid), str(lead.get('advert_id')))
            if it in sent_items or it in q_items: return False
        else:
            if k in sent_ids or k in q_ids: return False
        lead.setdefault('ad_type', 'goods')
        lead['message'] = build_message(lead.get('name', ''), lead.get('item', ''), social,
                                        lead.get('ad_type', 'goods'))
        new_leads.append(lead); return True

    bundles = [
        ("chats", unanswered_chats(), False),
        ("contact_views", leads_from_potential_clients(56), True),
        ("saved_ads", leads_from_potential_clients(67), True),
        ("callbacks", leads_from_potential_clients(58), True),
    ]
    for label, leads, social in bundles:
        added = sum(1 for l in leads if add(l, social))
        print(f"BUCKET {label}: fetched {len(leads)}, added {added}")

    if new_leads:
        combined = new_leads + existing
        if len(combined) > 400: combined = combined[:400]
        tmp = QUEUE + '.tmp'
        json.dump(combined, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        os.replace(tmp, QUEUE)
        print(f"HARVESTED {len(new_leads)} leads -> queue (total {len(combined)})")
        for l in new_leads[:6]:
            print("   ", l['source'], '|', l.get('name'), '|', (l.get('item') or '')[:38])
    else:
        print(f"HARVESTED 0 new (all in queue/sent). queue {len(existing)}")
    return 0

if __name__ == '__main__':
    sys.exit(main())

# Jiji Ads Performance Harvester (2Real Enterprises)
# Run inside browser_exec (session must be logged into jiji.com.gh as Two Real Enterprises).
# Harvests ALL active ads via Jiji SPA API and saves per-listing performance to Vault.
import json, time, os

VAULT = r"C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent"
OUT = os.path.join(VAULT, "jiji_ads_performance.json")

# Ensure logged in: open profile page first
goto_url("https://jiji.com.gh/profile")
wait_for_load()
time.sleep(4)
txt = js("document.body.innerText.slice(0,300)")
if "Two Real Enterprises" not in txt:
    print("NOT LOGGED IN — stop and prompt H to log in once in the browser session.")
else:
    print("Login verified: Two Real Enterprises")
    all_ads, page = [], 1
    while page <= 50:
        res = js(f"""fetch('https://jiji.com.gh/api_web/v1/profile/my-ads.json?status=active&page={page}&size=100', {{credentials:'include'}}).then(r=>r.json()).then(d=>JSON.stringify(d)).catch(e=>'ERR:'+e)""")
        time.sleep(2.5)
        if not isinstance(res, str) or res.startswith('ERR'):
            print("page", page, "fetch error:", res); break
        d = json.loads(res)
        lst = d.get('adverts_list', [])
        if not lst: break
        for a in lst:
            all_ads.append({
                'id': a.get('id'), 'guid': a.get('guid'), 'title': a.get('title'),
                'price': a.get('price_title'), 'url': a.get('url'),
                'status': a.get('status'),
                'impressions': (a.get('impressions') or {}).get('total'),
                'visitors': (a.get('count_views') or {}).get('total'),
                'views_today': (a.get('count_views') or {}).get('today'),
                'chats_total': (a.get('chat_count') or {}).get('total'),
                'chats_today': (a.get('chat_count') or {}).get('today'),
                'count_contacts': a.get('count_contacts'),
                'images': a.get('images_count'), 'top': a.get('top'),
            })
        print(f"page {page}: total {len(all_ads)}")
        if not d.get('next_url'): break
        page += 1
    json.dump({'scraped': time.strftime('%Y-%m-%d %H:%M'), 'total': len(all_ads), 'ads': all_ads}, open(OUT, 'w'), indent=1)
    print(f"SAVED {len(all_ads)} ads -> {OUT}")

#!/usr/bin/env python3
# Mission Control collector — pulls REAL data from 5 sources and writes mission_control.json
# Sources: kanban.db (to-dos / waiting-on-me / activity), cron stores (routines),
#          jiji_listings_full.json + jiji_ads_performance.json (Jiji), credits API (OpenRouter),
#          daily-sales-log.md (sales), FB run logs (FB activity)
import json, os, re, sqlite3, datetime, urllib.request, glob

HERMES=r"C:\Users\User\AppData\Local\hermes"
VAULT=r"C:\Users\User\.hermes\workspace\Vault"
OUT=os.path.join(VAULT,"business","2real","MissionControl","mission_control.json")
now=datetime.datetime.now()
D={}
D["generated"]=now.strftime("%Y-%m-%d %H:%M")
D["day"]=now.strftime("%A %d %b %Y")

def s(seg): return os.path.join(HERMES,seg)

# ---------- 1. KANBAN (to-dos / waiting-on-me / activity) ----------
def kanban():
    db=os.path.join(HERMES,"kanban.db")
    con=sqlite3.connect(f"file:{db}?mode=ro",uri=True); cur=con.cursor()
    cur.execute("SELECT id,title,status,priority,assignee,created_at,completed_at FROM tasks")
    rows=[]
    for tid,title,status,prio,assignee,ca,co in cur.fetchall():
        rows.append({"id":tid,"title":title,"status":status,
                     "priority":prio or 0,"assignee":assignee or "unassigned",
                     "created":ca,"completed":co})
    # unique titles (board has duplicates) — keep first, count dupes
    seen={}
    for r in rows:
        t=r["title"]
        if t not in seen: seen[t]=r; seen[t]["dup"]=1
        else: seen[t]["dup"]+=1
    uniq=list(seen.values())
    by={}
    for r in uniq: by.setdefault(r["status"],[]).append(r)
    return {"total":len(rows),"unique":len(uniq),
            "by_status":{k:len(v) for k,v in by.items()},
            "ready":[r for r in uniq if r["status"]=="ready"],
            "blocked":[r for r in uniq if r["status"]=="blocked"],
            "review":[r for r in uniq if r["status"] in ("review",)],
            "duplicates":sum(1 for r in uniq if r["dup"]>1)}
try: D["kanban"]=kanban()
except Exception as e: D["kanban"]={"error":str(e)}

# ---------- 2. ROUTINES (upcoming) ----------
def crons():
    allj=[]
    for store in [HERMES, os.path.join(HERMES,"profiles","sat-nav"),
                  os.path.join(HERMES,"profiles","content-buddy")]:
        p=os.path.join(store,"cron","jobs.json")
        if not os.path.exists(p): continue
        try:
            d=json.load(open(p,encoding='utf-8')); jobs=d.get("jobs",d)
            if isinstance(jobs,list):
                for j in jobs:
                    if isinstance(j,dict) and j.get("enabled"):
                        expr=""
                        sch=j.get("schedule") or j.get("cron") or ""
                        if isinstance(sch,list) and sch: expr=sch[0].get("display",sch[0].get("expr",""))
                        elif isinstance(sch,dict): expr=sch.get("display",sch.get("expr",""))
                        elif isinstance(sch,str): expr=sch
                        owner="default"
                        if "profiles\\sat-nav" in store or "profiles/sat-nav" in store: owner="sat-nav"
                        elif "content-buddy" in store: owner="content-buddy"
                        allj.append({"id":j.get("id","")[:8],"name":j.get("name") or j.get("job_name") or "?",
                                     "schedule":expr,"owner":owner})
        except Exception: pass
    return allj
D["routines"]=crons()
D["routine_count"]=len(D["routines"])

# ---------- 3. JIJI ----------
def jiji():
    jl=os.path.join(VAULT,"business","2real","2real-agent","jiji_listings_full.json")
    d=json.load(open(jl,encoding='utf-8'))
    items=d.get("items",[])
    active=sum(1 for i in items if i.get("status","")=="active")
    # category histogram (top 8)
    from collections import Counter
    cats=Counter(i.get("category") or i.get("category_name") or "Uncategorised" for i in items)
    # older ads_performance if present: top chats
    jp=os.path.join(VAULT,"business","2real","2real-agent","jiji_ads_performance.json")
    top=[]; active_perf=0; total_chats=0; total_impressions=None
    if os.path.exists(jp):
        perf=json.load(open(jp,encoding='utf-8'))
        ads=perf.get("ads",[]) if isinstance(perf,dict) else perf
        # schema: flat keys — chats_total, impressions, visitors, count_contacts, contact_views
        rows=[]
        for a in ads:
            try:
                ch=(a.get("chats_total") or 0) or 0
                rows.append({"title":(a.get("title") or "?")[:45],"chats":ch,
                             "views":(a.get("visitors") or 0),
                             "impressions":(a.get("impressions") or 0),
                             "price":a.get("price"),
                             "status":a.get("status")})
            except: pass
        rows.sort(key=lambda x:-x["chats"])
        top=rows[:5]
        active_perf=sum(1 for r in rows if r["status"]=="active" and r["chats"]>0)
        total_chats=sum(r["chats"] for r in rows)
    return {"total":d.get("count"),"active":active,
            "top_categories":cats.most_common(8),"top_by_chats":top,
            "ads_with_chats":active_perf,"total_chats":total_chats,
            "total_impressions":perf.get("total") if isinstance(perf,dict) else None}
try: D["jiji"]=jiji()
except Exception as e: D["jiji"]={"error":str(e)}

# ---------- 4. CREDITS ----------
def credits():
    key=None
    for line in open(os.path.join(HERMES,"profiles","sat-nav",".env"),encoding='utf-8'):
        if line.strip().startswith('OPENROUTER'):
            key=line.split('=',1)[1].strip().strip('"').strip("'"); break
    req=urllib.request.Request("https://openrouter.ai/api/v1/credits",headers={"Authorization":"Bearer "+key})
    c=json.load(urllib.request.urlopen(req,timeout=15)); d=c.get("data",{})
    return {"rem":round((d.get("total_credits") or 0)-(d.get("total_usage") or 0),2),
            "total":d.get("total_credits")}
try: D["credits"]=credits()
except Exception as e: D["credits"]={"error":str(e),"rem":None}

# ---------- 5. SALES ----------
def sales():
    txt=open(os.path.join(VAULT,"business","2real","daily-sales-log.md"),encoding='utf-8').read()
    rows=[]
    for m in re.finditer(r"\|\s*(\d{1,2}/\d{2}/\d{2})(?:\s+[A-Za-z]+)?\s*\|\s*([\d,]+)\s*\|\s*([\d,]*)\s*\|\s*([\d,]*%?)",txt):
        date,act,cogs,margin=m.group(1),m.group(2),m.group(3),m.group(4)
        act=v=int(act.replace(",","")) if act else 0
        rows.append({"date":date,"actual":act,"cogs":int(cogs.replace(",","")) if cogs else None,"margin":margin})
    last=rows[-1] if rows else None
    wk=[r for r in rows[-7:]]
    week=sum(r["actual"] for r in wk)
    return {"last":last,"week_total":week,"rows":rows[-14:]}
try: D["sales"]=sales()
except Exception as e: D["sales"]={"error":str(e)}

# ---------- 6.5 FB MESSAGES MONITOR ----------
def fb_messages():
    fp=os.path.join(VAULT,"business","2real","MissionControl","fb_messages.json")
    if not os.path.exists(fp): return {"status":"not-run","thread_count":0,"note":"monitor not run yet"}
    d=json.load(open(fp,encoding='utf-8'))
    # freshness: show a stale tag if the snapshot is >26h old
    try:
        gen=datetime.datetime.strptime(d.get("generated",""),"%Y-%m-%d %H:%M")
        age=(datetime.datetime.now()-gen).total_seconds()
        if age>26*3600 and d.get("status")=="ok": d["note"]=(d.get("note") or "")+" (stale >26h)"
    except Exception: pass
    return d
try: D["fb_messages"]=fb_messages()
except Exception as e: D["fb_messages"]={"status":"error","note":str(e)}

# ---------- 6. FB ACTIVITY ----------
def fb():
    pats=os.path.join(VAULT,"business","2real","2real-agent","channel_upload_package","*.txt")
    pubs=0; lines=[]
    for p in glob.glob(pats):
        if "log" not in os.path.basename(p).lower(): continue
        txt=open(p,encoding='utf-8').read()
        pubs+=len(re.findall(r"published",txt,re.I))
        for ln in txt.splitlines():
            if ln.strip() and ("published" in ln.lower() or "LOGGED" in ln):
                lines.append(ln.strip()[:60])
    return {"published":pubs,"recent":lines[-6:]}
try: D["fb"]=fb()
except Exception as e: D["fb"]={"error":str(e)}

with open(OUT,"w",encoding='utf-8') as f: json.dump(D,f,ensure_ascii=False,indent=2)
print("Mission Control data written:", OUT)
print("day:",D["day"])
print("routines:",D["routine_count"],"| kanban:",D.get("kanban",{}).get("total"),"tasks (",D.get("kanban",{}).get("unique"),"unique )")
print("sales last:",D.get("sales",{}).get("last"))
print("credits:",D.get("credits",{}).get("rem"))
print("jiji:",D.get("jiji",{}).get("active"),"active")
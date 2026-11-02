#!/usr/bin/env python3
"""Render Mission Control HTML from mission_control.json (self-contained, dark)."""
import json, os, html, datetime

BASE=r"C:\Users\User\.hermes\workspace\Vault\business\2real\MissionControl"
D=json.load(open(os.path.join(BASE,"mission_control.json"),encoding='utf-8'))
E=html.escape

def status_color(s):
    return {"ready":"#fbbf24","blocked":"#f87171","review":"#60a5fa","todo":"#94a3b8",
            "running":"#34d399","done":"#34d399"}.get(s,"#64748b")

def prio_flag(p):
    p=int(p or 0)
    if p>=3: return "🔴"
    if p>=2: return "🟠"
    if p>=1: return "🟡"
    return ""

# ---- clocks to inject
gen=D.get("generated","")
day=D.get("day","")

# ---- stat cards
kanban=D.get("kanban",{})
cred=D.get("credits",{}) or {}
sales=D.get("sales",{}) or {}
jiji=D.get("jiji",{}) or {}
fb=D.get("fb",{}) or {}

def fmt_gh(v):
    try: return f"GH₵ {int(v):,}"
    except: return "—"

cards=[]
cards.append(("🛒 Jiji Live", f"{jiji.get('active','—'):,}","active listings on Jiji (source of truth)"))
cards.append(("💸 Last Sale", fmt_gh((sales.get('last') or {}).get('actual')), f"{(sales.get('last') or {}).get('date','')} · margin {(sales.get('last') or {}).get('margin','—')}"))
cards.append(("📈 7-day Sales", fmt_gh(sales.get('week_total')),"sum of last 7 recorded days"))
cards.append(("⚡ OpenRouter", str(cred.get('rem','—')) or "—","credits remaining of accounts"))
cards.append(("✅ Open To-dos", str(kanban.get('unique','—')),"kanban tasks (deduped)"))
cards.append(("🤖 Active Bots", str(D.get('routine_count','—')),"automated routines running"))

cards_html="".join(f"<div class='stat'><div class='stat-val'>{E(c[1])}</div><div class='stat-lab'>{E(c[0])}</div><div class='stat-sub'>{E(c[2])}</div></div>" for c in cards)

# ---- Waiting on me (left): ready + high-priority blocked + review, newest first by created
def time_ago(ts):
    if not ts: return ""
    try:
        dt=datetime.datetime.fromtimestamp(int(ts))
        d=(datetime.datetime.now()-dt).days
        return f"{d}d" if d>=1 else "today"
    except: return ""

disputed_markers=["Croydon","New Cross","Peckham","Owusu","Ford Ranger","Samsung S8","Costa","shed","Mum insurance","Kids","junior bank","EDF","Tide","Facebook","FB ","Future-proof","gov.uk","Consolidate to one phone"]
waiting=[]
for r in kanban.get("ready",[]):
    waiting.append(r)
# blocked items that are actively waiting on H input → surface them but note they may be external-waiting
for r in kanban.get("blocked",[])[:0]:  # keep left column = YOUR approvals/actions
    pass
waiting.sort(key=lambda r:(r.get("created") or 0),reverse=True)

def wait_card(r):
    mark=r.get("title","")
    note=""
    if prio_flag(r.get("priority")) in ("🔴",): note="<div class='tag hot'>high</div>"
    if r.get("dup",1)>1: note+=f"<div class='tag dup'>dup×{r['dup']}</div>"
    return (f"<div class='wait-item'><div class='wait-top'><span class='wait-title'>{E(mark)}</span>"
            f"<span class='wait-time'>{time_ago(r.get('created'))}</span></div>"
            f"<div class='wait-meta'>{note}<span class='tag prio'>{prio_flag(r.get('priority'))}</span>"
            f"<button class='open-btn' data-id='{E(r.get('id',''))}'>Open</button></div></div>")

# only show actionable (ready) + blocked that are H-dependent (no assignee worker) newest-first, cap 12
ready_sorted=sorted([r for r in kanban.get("ready",[])],key=lambda r:(r.get("created") or 0),reverse=True)
waiting_html="".join(wait_card(r) for r in ready_sorted[:12])
if not ready_sorted: waiting_html="<div class='empty'>Nothing waiting on you — shelf cleared.</div>"

# ---- Activity timeline (middle): recently completed + FB/kanban done
activity=[]
today_int=int(datetime.datetime.now().timestamp())
# completed kanban tasks with completed_at
for r in (kanban.get("ready",[])+kanban.get("blocked",[])+kanban.get("review",[])):
    pass
html_too=[]

# use FB recent + a note that full kanban history lives in board
act=[]
for ln in (fb.get("recent") or []):
    act.append({"t":"fb","txt":ln})
# recent routine completions are in cron output files; we surface FB + a health line
activity_html="".join(f"<div class='act-item'><span class='act-badge fb'>FB</span><span class='act-txt'>{E(a['txt'])}</span></div>" for a in act)
if not act: activity_html="<div class='empty'>No recent bot completions logged yet this cycle.</div>"

# ---- Upcoming routines (right): grouped, with owner bot
def next_label(expr):
    ex=str(expr)
    if "*/" in ex or "," in ex: return ex
    if "0 7" in ex: return "daily 07:00"
    if "0 9" in ex: return "daily 09:00"
    if "0 10" in ex: return "daily 10:00"
    return ex
routines=D.get("routines",[])
routines.sort(key=lambda r:(r.get("owner",""),r.get("schedule","")))
own_col={"default":"#34d399","sat-nav":"#60a5fa","content-buddy":"#fbbf24"}
def own_badge(o):
    c=own_col.get(o,'#64748b')
    return f"<span class='badge' style='background:{c}22;color:{c}'>{E(o)}</span>"
routine_html="".join(f"<div class='rt-item'>{own_badge(r.get('owner','default'))}<span class='rt-name'>{E(r.get('name',''))}</span><span class='rt-sched'>{E(next_label(r.get('schedule','')))}</span></div>" for r in routines[:0])  # placeholder, build grouped below
# group by owner
grouped={}
for r in routines:
    grouped.setdefault(r.get("owner","default"),[]).append(r)
group_html=""
for own in ["default","sat-nav","content-buddy"]:
    if own not in grouped: continue
    group_html+=f"<div class='rt-group'><div class='rt-group-h'>{own_badge(own)} <b>{own}</b></div>"
    for r in grouped[own][:18]:
        group_html+=f"<div class='rt-item'><span class='rt-name'>{E(r.get('name',''))}</span><span class='rt-sched'>{E(next_label(r.get('schedule','')))}</span></div>"
    group_html+="</div>"

# ---- FB messages monitor / trends strip
jcats="".join(f"<div class='cat'><span class='cat-name'>{E(c)}</span><span class='cat-n'>{n:,}</span></div>"
              for c,n in (jiji.get('top_categories') or [])[:6])
n_chat=jiji.get('ads_with_chats',0); tot_ch=jiji.get('total_chats',0); imp=jiji.get('total_impressions',0)
jitrend=(f"<div class='sub'>Jiji scale</div>"
         f"<div class='cat'><span class='cat-name'>Ads with chats</span><span class='cat-n'>{n_chat:,}</span></div>"
         f"<div class='cat'><span class='cat-name'>Total chats</span><span class='cat-n'>{tot_ch:,}</span></div>"
         f"<div class='cat'><span class='cat-name'>Impressions</span><span class='cat-n'>{imp:,}</span></div>" if (imp or tot_ch) else "")
topchats="".join(f"<div class='chats'><span class='chats-t'>{E(t.get('title',''))}</span><span class='chats-n'>{t.get('chats')} chats</span></div>"
                 for t in (jiji.get('top_by_chats') or [])[:6])
if not topchats: topchats="<div class='empty'>No per-listing chat data in the latest harvest.</div>"

html_out = """<!doctype html><html><head><meta charset="utf-8">
<style>
:root{--bg:#0b0f17;--card:#121826;--card2:#0f1522;--line:#1e293b;--txt:#e2e8f0;--muted:#7b8aa3;--acc:#34d399;--blue:#60a5fa;--amber:#fbbf24;--red:#f87171;}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--txt);font-family:ui-sans-serif,system-ui,'Segoe UI',sans-serif;padding:18px 20px;min-height:100vh}
.top{display:flex;align-items:baseline;gap:14px;margin-bottom:16px;flex-wrap:wrap}
h1{font-size:22px;font-weight:700;letter-spacing:.3px}
h1 span{color:var(--acc)}
.clock{font-size:15px;color:var(--muted);font-variant-numeric:tabular-nums;margin-left:auto}
.day{font-size:13px;color:var(--muted)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:16px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.stat-val{font-size:22px;font-weight:700;color:var(--txt);line-height:1.1}
.stat-lab{font-size:12px;color:var(--muted);margin-top:2px;text-transform:uppercase;letter-spacing:.4px}
.stat-sub{font-size:11px;color:var(--muted);opacity:.8;margin-top:4px}
.cols{display:grid;grid-template-columns:1.1fr 1fr 1.1fr;gap:12px;align-items:start}
.panel{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
.panel h2{font-size:13px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin-bottom:12px;display:flex;align-items:center;gap:7px}
.panel h2 .n{background:var(--acc);color:#052e22;border-radius:999px;font-size:10px;padding:1px 7px;font-weight:700}
.wait-item,.act-item,.rt-item{border-top:1px solid var(--line);padding:9px 0}
.wait-item:first-child,.act-item:first-child,.rt-item:first-child{border-top:none}
.wait-top{display:flex;justify-content:space-between;gap:8px}
.wait-title{font-size:13px;font-weight:600;line-height:1.35}
.wait-time{font-size:11px;color:var(--muted);white-space:nowrap}
.wait-meta{display:flex;align-items:center;gap:6px;margin-top:6px}
.tag{font-size:10px;border-radius:999px;padding:2px 8px;background:var(--card2);border:1px solid var(--line);color:var(--muted)}
.tag.hot{background:#f8717122;color:var(--red);border-color:#f8717155}
.tag.dup{background:#fbbf2422;color:var(--amber);border-color:#fbbf2455}
.open-btn{margin-left:auto;background:var(--card2);border:1px solid var(--line);color:var(--blue);border-radius:6px;font-size:11px;padding:3px 10px;cursor:pointer}
.open-btn:hover{background:var(--blue);color:#052e22;border-color:var(--blue)}
.act-badge{font-size:9px;font-weight:700;border-radius:4px;padding:2px 6px;margin-right:8px;vertical-align:1px}
.act-badge.fb{background:#1877f222;color:#4d9aff}
.act-txt{font-size:12.5px;color:#cbd5e1}
.empty{color:var(--muted);font-size:12.5px;padding:6px 0;font-style:italic}
.rt-group{margin-bottom:10px}
.rt-group-h{font-size:11px;color:var(--muted);margin-bottom:5px;display:flex;align-items:center;gap:6px}
.rt-item{display:flex;justify-content:space-between;gap:8px}
.rt-name{font-size:12.5px;color:#cbd5e1}
.rt-sched{font-size:11px;color:var(--muted);white-space:nowrap}
.badge{font-size:9px;border-radius:999px;padding:2px 8px;font-weight:600;letter-spacing:.3px}
.botstrip{background:var(--card2);border:1px solid var(--line);border-radius:12px;padding:14px;margin-top:12px}
.botstrip h2{font-size:13px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin-bottom:12px}
.fb-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.sub{font-size:11px;color:var(--muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:.4px}
.cat,.chats{display:flex;justify-content:space-between;padding:5px 0;border-top:1px solid var(--line);font-size:12.5px}
.cat-name,.chats-t{color:#cbd5e1}
.cat-n,.chats-n{color:var(--acc);font-weight:600;font-variant-numeric:tabular-nums}
@media(max-width:1100px){.cols{grid-template-columns:1fr}.fb-grid{grid-template-columns:1fr}}
</style></head><body>
<div class="top"><h1>🛰️ Mission <span>Control</span></h1>
<span class="day">{{DAY}}</span>
<span class="clock" id="clk">{{GEN}}</span></div>

<div class="stats">{{CARDS}}</div>

<div class="cols">
  <div class="panel"><h2>⏳ Waiting on me <span class="n">{{WAITN}}</span></h2>
    <div style="max-height:520px;overflow:auto">{{WAITING}}</div></div>
  <div class="panel"><h2>📡 Activity timeline</h2>
    <div style="max-height:520px;overflow:auto">{{ACTIVITY}}</div></div>
  <div class="panel"><h2>🗓 Upcoming routines <span class="n">{{RTN}}</span></h2>
    <div style="max-height:520px;overflow:auto">{{ROUTINES}}</div></div>
</div>

<div class="botstrip"><h2>🌐 Jiji & Facebook — market trends</h2>
  <div class="fb-grid">
    <div><div class="sub">Jiji top categories</div><div id="jcat">{{JCATS}}</div>{{JITREND}}</div>
    <div><div class="sub">Top listings by chats</div><div id="jchats">{{JCHATS}}</div></div>
  </div></div>

<script>
const clk=document.getElementById('clk');
function t(){clk.textContent=new Date().toLocaleString('en-GB',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit',second:'2-digit'});}
t();setInterval(t,1000);
document.querySelectorAll('.open-btn').forEach(b=>{b.onclick=()=>{
  if(window.hermes&&window.hermes.send){window.hermes.send('Show me kanban task '+b.dataset.id);}
};});
</script></body></html>
"""
html_out=(html_out.replace("{{DAY}}",E(day)).replace("{{GEN}}",E(gen))
          .replace("{{CARDS}}",cards_html)
          .replace("{{WAITN}}",str(len(ready_sorted)))
          .replace("{{WAITING}}",waiting_html)
          .replace("{{ACTIVITY}}",activity_html)
          .replace("{{RTN}}",str(len(D.get('routines',[]))))
          .replace("{{ROUTINES}}",group_html)
          .replace("{{JCATS}}",jcats).replace("{{JCHATS}}",topchats)
          .replace("{{JITREND}}",jitrend))
outp=os.path.join(BASE,"MissionControl.html")
open(outp,"w",encoding='utf-8').write(html_out)
print("Dashboard written:",outp,"|",len(html_out),"bytes")
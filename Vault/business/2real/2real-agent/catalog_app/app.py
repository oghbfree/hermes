"""2Real Master Catalog — local-first catalog app.

Serves the merged master_catalog.json (Jiji ads + Zobaze costs) as a
phone-friendly web UI. Owner mode: edit GBP cost / purchase date /
location / price, mark sold. Browse mode: photo + price only (send to
customers). Stdlib only — no dependencies.

Run:  python app.py   →  http://localhost:8765  (LAN IP shown for phone)
Data: ../master_catalog.json  (saved back on every edit)
"""
import json
import os
import re
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "..", "master_catalog.json")
PORT = 8765


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def save(items):
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=1, ensure_ascii=False)


MONTH_YEAR = re.compile(r"^\d{1,2}/\d{2,4}$")       # mm/yy or mm/yyyy
DAY_MONTH_YEAR = re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4}$")  # dd/mm/yy or dd/mm/yyyy


def parse_purchase_date(s):
    """Accepts dd/mm/yy(yy) or mm/yy(yy). Returns normalised string or ''."""
    s = (s or "").strip()
    if not s:
        return ""
    if DAY_MONTH_YEAR.match(s):
        d, m, y = s.split("/")
        if len(y) == 2:
            y = "20" + y
        return f"{int(d):02d}/{int(m):02d}/{y}"
    if MONTH_YEAR.match(s):
        m, y = s.split("/")
        if len(y) == 2:
            y = "20" + y
        return f"{int(m):02d}/{y}"
    return None  # invalid


def recalc(item):
    """cost_gbp + fx -> cost_ghs; profit = canonical_price - cost_ghs."""
    gbp = item.get("cost_gbp_incl_shipping")
    fx = item.get("fx_rate")
    if gbp and fx:
        item["cost_ghs_calc"] = round(float(gbp) * float(fx), 2)
    else:
        item["cost_ghs_calc"] = None
    if item.get("cost_ghs_calc") and item.get("canonical_price"):
        item["profit_ghs"] = round(item["canonical_price"] - item["cost_ghs_calc"], 2)
    else:
        item["profit_ghs"] = None


HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>2Real Catalog</title>
<style>
:root{--fg:#eee;--mut:#999;--card:#1c1c1e;--bg:#111;--acc:#4caf50;--warn:#ff9800}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
 font-family:system-ui,sans-serif;font-size:15px}
header{position:sticky;top:0;background:var(--bg);padding:8px 12px;z-index:5;
 border-bottom:1px solid #333;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
header input{flex:1;min-width:140px;padding:8px;border-radius:8px;border:1px solid #444;
 background:#222;color:var(--fg)}
button{padding:8px 12px;border-radius:8px;border:1px solid #444;background:#2a2a2c;
 color:var(--fg);cursor:pointer}
button.mode{font-weight:bold}
.mode.owner{background:#0a3; color:#000;border-color:#0a3}
.mode.browse{background:#06c;color:#fff;border-color:#06c}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;padding:10px}
.item{background:var(--card);border-radius:10px;overflow:hidden;cursor:pointer}
.item img{width:100%;aspect-ratio:1;object-fit:cover;background:#333;display:block}
.p{padding:8px}.t{font-size:13px;line-height:1.3;max-height:2.6em;overflow:hidden}
.pr{color:#ffd54f;font-weight:bold;margin-top:4px}
.meta{color:var(--mut);font-size:12px;margin-top:4px}
.sold{color:var(--warn);font-weight:bold}
.closewarn{color:#f66;font-size:12px}
dialog{background:var(--card);color:var(--fg);border:1px solid #444;border-radius:12px;
 max-width:420px;width:92%}
dialog img{width:100%;border-radius:8px}
label{display:block;margin:8px 0 2px;font-size:12px;color:var(--mut)}
input.f{width:100%;padding:8px;border-radius:6px;border:1px solid #444;background:#222;color:var(--fg)}
.row{display:flex;gap:8px;margin-top:12px}
.row button{flex:1}
.save{background:var(--acc);color:#000;border-color:var(--acc);font-weight:bold}
.stats{padding:4px 12px;color:var(--mut);font-size:13px}
</style></head><body>
<header>
 <button class="mode browse" id="modeBtn" onclick="toggleMode()">Browse</button>
 <input id="q" placeholder="Search title..." oninput="render()">
 <span class="stats" id="stats"></span>
</header>
<div class="grid" id="grid"></div>
<dialog id="dlg"><div id="dlgBody"></div></dialog>
<script>
let ITEMS=[],mode='browse';
const q=s=>document.querySelector(s);
function toggleMode(){mode=mode==='browse'?'owner':'browse';
 const b=q('#modeBtn');b.textContent=mode==='owner'?'Owner':'Browse';
 b.className='mode '+(mode==='owner'?'owner':'browse');render();}
async function load(){
 ITEMS=await (await fetch('/api/items')).json();render();}
function profitTag(it){
 if(it.profit_ghs!=null)return `<div class="meta">Profit: GHS ${it.profit_ghs}</div>`;
 if(it.cost_gbp_incl_shipping)return `<div class="meta closewarn">Set FX rate</div>`;
 return '';}
function render(){
 const query=q('#q').value.toLowerCase();
 const vis=ITEMS.filter(it=>(mode==='browse'?true:it._visible!==false)
   && it.title.toLowerCase().includes(query));
 q('#grid').innerHTML=vis.map((it)=>`
  <div class="item" onclick='openItem(${JSON.stringify(it.jiji_id)})'>
   <img loading="lazy" src="${it.image||''}" onerror="this.style.opacity=.15">
   <div class="p"><div class="t">${esc(it.title)}</div>
    <div class="pr">GHS ${it.canonical_price??'?'}</div>
    ${mode==='owner'?`
      <div class="meta">stock: ${it._qty ?? it.zobaze_stock ?? '?'}</div>
      ${it.cost_gbp_incl_shipping?`<div class="meta">£${it.cost_gbp_incl_shipping} · ${it.purchase_date||'no date'}</div>`:'<div class="meta">cost not set</div>'}
      ${profitTag(it)}
      ${it._close_ad?'<div class="closewarn">STOCK 0 — CLOSE JIJI AD</div>':''}
      ${it.sold?'<div class="sold">SOLD</div>':''}`:''}
   </div></div>`).join('');
 q('#stats').textContent=`${vis.length} items · ${mode} mode`;}
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/'/g,'&#39;')}
function openItem(id){
 const it=ITEMS.find(x=>x.jiji_id===id);if(!it)return;
 const b=q('#dlgBody');
 if(mode==='browse'){
  b.innerHTML=`<img src="${it.image||''}"><div class="p"><div class="t">${esc(it.title)}</div>
   <div class="pr">GHS ${it.canonical_price??'?'}</div>
   <div class="row"><a href="${it.url}" target="_blank" style="flex:1">
   <button style="width:100%">View on Jiji</button></a></div></div>`;
 }else{
  b.innerHTML=`<img src="${it.image||''}"><div class="p">
   <div class="t">${esc(it.title)}</div>
   <label>Cost GBP (incl. shipping)</label>
   <input class="f" id="f_gbp" type="number" step="0.01" value="${it.cost_gbp_incl_shipping??''}">
   <label>Purchase date (dd/mm/yy or mm/yy)</label>
   <input class="f" id="f_date" value="${it.purchase_date||''}">
   <label>FX rate (£→GHS) — blank = 15.75</label>
   <input class="f" id="f_fx" type="number" step="0.01" value="${it.fx_rate??''}">
   <label>Quantity in stock</label>
   <input class="f" id="f_qty" type="number" value="${it._qty ?? it.zobaze_stock ?? 0}">
   <label>Selling price GHS (canonical)</label>
   <input class="f" id="f_price" type="number" step="0.01" value="${it.canonical_price??''}">
   <label>Location (bag/box code)</label>
   <input class="f" id="f_loc" value="${it.location||''}" placeholder="BAG-01 / A2 ...">
   <div class="row"><button class="save" onclick="saveItem(${id})">Save</button>
   <button onclick="markSold(${id})">Mark sold −1</button></div>
   <div class="row"><a href="${it.url}" target="_blank" style="flex:1">
   <button style="width:100%">Open on Jiji</button></a>
   <button onclick="document.getElementById('dlg').close()">Close</button></div></div>`;
 }
 q('#dlg').showModal();}
async function saveItem(id){
 const it=ITEMS.find(x=>x.jiji_id===id);
 const body={jiji_id:id,
  cost_gbp_incl_shipping:q('#f_gbp').value||null,
  purchase_date:q('#f_date').value||null,
  fx_rate:q('#f_fx').value||null,
  qty:q('#f_qty').value,
  canonical_price:q('#f_price').value||null,
  location:q('#f_loc').value||null};
 const r=await (await fetch('/api/update',{method:'POST',
  headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})).json();
 if(r.error){alert(r.error);return;}
 Object.assign(it,r.item);document.getElementById('dlg').close();render();}
async function markSold(id){
 const r=await (await fetch('/api/sold',{method:'POST',
  headers:{'Content-Type':'application/json'},body:JSON.stringify({jiji_id:id})})).json();
 if(r.error){alert(r.error);return;}
 Object.assign(ITEMS.find(x=>x.jiji_id===id),r.item);
 document.getElementById('dlg').close();render();}
load();
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, HTML)
        elif self.path == "/api/items":
            items = load()
            # hide internal fields in browse mode is client-side; send all to owner device
            self._send(200, json.dumps(items), "application/json; charset=utf-8")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._send(400, '{"error":"bad json"}', "application/json")
        items = load()
        it = next((x for x in items if x.get("jiji_id") == body.get("jiji_id")), None)
        if not it:
            return self._send(404, '{"error":"item not found"}', "application/json")

        if self.path == "/api/update":
            if body.get("cost_gbp_incl_shipping") is not None:
                try:
                    it["cost_gbp_incl_shipping"] = float(body["cost_gbp_incl_shipping"])
                except ValueError:
                    pass
            if "purchase_date" in body:
                pd = parse_purchase_date(body.get("purchase_date"))
                if pd is None:
                    return self._send(400, '{"error":"bad date: use dd/mm/yy or mm/yy"}', "application/json")
                it["purchase_date"] = pd
            if body.get("fx_rate") is not None:
                it["fx_rate"] = float(body["fx_rate"])
            elif body.get("cost_gbp_incl_shipping") and not it.get("fx_rate"):
                it["fx_rate"] = 15.75  # H fallback rate
            if body.get("canonical_price") is not None:
                it["canonical_price"] = float(body["canonical_price"])
            if body.get("location") is not None:
                it["location"] = body["location"]
            if body.get("qty") is not None:
                it["_qty"] = int(body["qty"])
                it["_close_ad"] = it["_qty"] <= 0
            recalc(it)
            save(items)
            return self._send(200, json.dumps({"item": it}), "application/json")

        if self.path == "/api/sold":
            qty = int(it.get("_qty", it.get("zobaze_stock") or 0))
            qty = max(0, qty - 1)
            it["_qty"] = qty
            it["_close_ad"] = qty <= 0
            save(items)
            return self._send(200, json.dumps({"item": it}), "application/json")

        self._send(404, '{"error":"unknown"}', "application/json")


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    ip = lan_ip()
    print(f"2Real Catalog running:")
    print(f"  This PC:   http://localhost:{PORT}")
    print(f"  Phone:     http://{ip}:{PORT}   (same WiFi/hotspot)")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
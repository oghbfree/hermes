"""Append 'Pairs well with' bundle line to a FB listing description.
Usage: python fb_edit_bundle.py "<title substring>"
Run with FB_CDP_URL set. Drives cdp_harness (trusted clicks + JS dispatch).
"""
import sys, time, re
import cdp_harness as H

BUNDLE_LINE = "Pairs well with: Gorilla Glue + Super Glue Gel — grab the Adhesives Starter set, one pickup, one MoMo."


def dispatch_click(el):
    H.js("""(function(el){['mousedown','mouseup','click'].forEach(function(t){
      el.dispatchEvent(new MouseEvent(t,{bubbles:true,cancelable:true,view:window}));});})""", el)
    # cdp_harness.js(expr) evaluates a string; pass element via argument binding not supported,
    # so fall through to Runtime.callFunctionOn style below.


def js_call(fn_source, arg_ref=""):
    """Evaluate JS that returns a JSON string."""
    return H.js(fn_source)


def find_card(title_sub):
    expr = """(() => {
      const sub = %s;
      const els = [...document.querySelectorAll('div[role=button]')];
      for (const el of els) {
        const t = el.innerText || '';
        if (t.includes('Active') && t.includes(sub)) {
          const r = el.getBoundingClientRect();
          return JSON.stringify({found:true, x: Math.round(r.x+r.width/2), y: Math.round(r.y+r.height/2), text: t.slice(0,120)});
        }
      }
      return JSON.stringify({found:false});
    })()""" % __import__("json").dumps(title_sub)
    raw = H.js(expr)
    import json as J
    return J.loads(raw) if raw else {"found": False}


def click_at(x, y):
    H.click_at_xy(x, y)


def main(title_sub):
    time.sleep(2)
    card = find_card(title_sub)
    if not card.get("found"):
        # try the search-your-listings input first
        print("CARD NOT FOUND on page; searching your listings")
        H.js("""(() => { const inp=[...document.querySelectorAll('input[placeholder*=\"Search\"]')]
            .find(i=>i.closest('div').innerText.match(/your listings/i)) ||
            [...document.querySelectorAll('input')].find(i=>(i.placeholder||'').toLowerCase().includes('search your'));
            if(inp){ const st=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
            st.call(inp, %s); inp.dispatchEvent(new Event('input',{bubbles:true})); }})()""" % __import__("json").dumps(title_sub.split()[0]))
        time.sleep(4)
        card = find_card(title_sub)
        if not card.get("found"):
            print("STILL NOT FOUND:", title_sub)
            return
    click_at(card["x"], card["y"])
    time.sleep(5)
    # detail panel should now show Edit listing
    r = H.js("""(() => {
      const btn=[...document.querySelectorAll('div[role=button],a[role=link]')].find(b=>(b.innerText||'').trim()==='Edit listing' || (b.innerText||'').trim().startsWith('Edit listing'));
      if(!btn) return JSON.stringify({ok:false});
      const r=btn.getBoundingClientRect();
      return JSON.stringify({ok:true,x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)});
    })()""")
    import json as J
    d = J.loads(r) if r else {"ok": False}
    if not d.get("ok"):
        print("EDIT LISTING BUTTON NOT FOUND")
        return
    click_at(d["x"], d["y"])
    time.sleep(6)
    # edit form: find description textarea, check if bundle line already present
    expr = """(() => {
      const ta=[...document.querySelectorAll('textarea')];
      const out=ta.map((t,i)=>({i, name:t.getAttribute('name')||'', label:(t.labels&&t.labels[0]?t.labels[0].innerText:''), len:(t.value||'').length, val:(t.value||'').slice(-80)}));
      return JSON.stringify(out);
    })()"""
    import json as J
    tas = J.loads(H.js(expr) or "[]")
    print("textareas:", tas)
    desc = None
    for t in tas:
        blob = (t["label"] + t["name"]).lower()
        if "desc" in blob or "description" in blob or t["len"] > 60:
            desc = t["i"]
            break
    if desc is None:
        print("NO DESCRIPTION TEXTAREA FOUND")
        return
    cur = H.js("""(() => { const tas=[...document.querySelectorAll('textarea')];
      return tas[%d] ? tas[%d].value : ''; })()""" % (desc, desc))
    if BUNDLE_LINE in cur:
        print("ALREADY HAS BUNDLE LINE")
        return
    new = (cur.rstrip() + "\n\n" + BUNDLE_LINE).strip()
    ok = H.js("""(() => {
      const tas=[...document.querySelectorAll('textarea')]; const ta=tas[%d];
      if(!ta) return 'no_ta';
      const st=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;
      st.call(ta, %s); ta.dispatchEvent(new Event('input',{bubbles:true}));
      return 'set:' + ta.value.slice(-60);
    })()""" % (desc, __import__("json").dumps(new)))
    print("set:", ok)
    time.sleep(2)
    # Save
    r = H.js("""(() => {
      const btns=[...document.querySelectorAll('div[role=button],button')].filter(b=>(b.innerText||'').trim()==='Save');
      if(!btns.length) return JSON.stringify({ok:false});
      const b=btns[btns.length-1]; const r=b.getBoundingClientRect();
      return JSON.stringify({ok:true,x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)});
    })()""")
    d = J.loads(r) if r else {"ok": False}
    if not d.get("ok"):
        print("SAVE BUTTON NOT FOUND")
        return
    click_at(d["x"], d["y"])
    time.sleep(6)
    print("SAVED OK:", title_sub)


if __name__ == "__main__":
    main(sys.argv[1])

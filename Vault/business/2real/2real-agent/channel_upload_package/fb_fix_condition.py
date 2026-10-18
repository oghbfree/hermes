"""Fix FB listing Condition (New -> Used - good) + description condition line.
Usage: FB_CDP_URL=http://127.0.0.1:9222 python fb_fix_condition.py "<title substring>" "<wrong desc fragment>" "<correct condition line>"
Driven by cdp_harness (trusted clicks + JS dispatch). 17 Oct 26 condition-mislabel repair.
"""
import sys, time, json
import cdp_harness as H


def find_card(title_sub):
    expr = """(() => {
      const sub = %s;
      const els = [...document.querySelectorAll('div[role=button]')];
      for (const el of els) {
        const t = el.innerText || '';
        if (t.includes('Active') && t.includes(sub)) {
          const r = el.getBoundingClientRect();
          return JSON.stringify({found:true, x: Math.round(r.x+r.width/2), y: Math.round(r.y+r.height/2)});
        }
      }
      return JSON.stringify({found:false});
    })()""" % json.dumps(title_sub)
    raw = H.js(expr)
    return json.loads(raw) if raw else {"found": False}


def click(x, y):
    H.click_at_xy(x, y)


def js_set_combobox(label_prefix, want_norm):
    """Open a labelled combobox and pick option whose normalized text == want_norm."""
    H.js("""(() => {
      const c=[...document.querySelectorAll('[role=combobox]')].filter(e=>e.offsetParent!==null)
        .find(e=>{const l=e.closest('label'); return l && (l.textContent||'').trim().startsWith(%s);});
      if(!c) return;
      c.scrollIntoView({block:'center'});
      const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window});
      ['mousedown','mouseup','click'].forEach(t=>c.dispatchEvent(ME(t)));
    })()""" % json.dumps(label_prefix))
    time.sleep(2.5)
    r = H.js("""(() => {
      const norm=s=>s.toLowerCase().replace(/[^a-z0-9]/g,'');
      const want=%s;
      const lab=[...document.querySelectorAll('label')].filter(e=>e.offsetParent!==null)
        .find(e=>{const l=e.closest('label'); return l && (l.textContent||'').trim().startsWith(%s);});
      if(!lab) return 'nolab';
      const lb=document.getElementById(lab.getAttribute('aria-controls'));
      if(!lb) return 'nolb';
      const opt=[...lb.querySelectorAll('[role=option]')].find(o=>norm(o.textContent)===want);
      if(!opt) return JSON.stringify({err:'noopt', opts:[...lb.querySelectorAll('[role=option]')].map(o=>o.textContent).slice(0,8)});
      const ME=t=>new MouseEvent(t,{bubbles:true,cancelable:true,view:window});
      ['mousedown','mouseup','click'].forEach(t=>opt.dispatchEvent(ME(t)));
      return 'dispatched';
    })()""" % (json.dumps(want_norm), json.dumps(label_prefix)))
    time.sleep(2)
    return r


def main(title_sub, wrong_frag, correct_line):
    H.goto_url('https://www.facebook.com/marketplace/you/selling')
    time.sleep(8)
    card = find_card(title_sub)
    if not card.get('found'):
        print('CARD NOT FOUND', title_sub); return
    click(card['x'], card['y']); time.sleep(5)
    r = H.js("""(() => {
      const btn=[...document.querySelectorAll('div[role=button],a[role=link]')].find(b=>(b.innerText||'').trim().startsWith('Edit listing'));
      if(!btn) return JSON.stringify({ok:false});
      const r=btn.getBoundingClientRect();
      return JSON.stringify({ok:true,x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)});
    })()""")
    d = json.loads(r) if r else {'ok': False}
    if not d.get('ok'):
        print('EDIT BTN NOT FOUND'); return
    click(d['x'], d['y']); time.sleep(6)
    # read current condition + description
    info = H.js("""(() => {
      const norm=s=>s.toLowerCase().replace(/[^a-z0-9]/g,'');
      const cond=[...document.querySelectorAll('[role=combobox]')].filter(e=>e.offsetParent!==null)
        .find(e=>{const l=e.closest('label'); return l && (l.textContent||'').trim().startsWith('Condition');});
      const tas=[...document.querySelectorAll('textarea')].map((t,i)=>({i, len:(t.value||'').length}));
      return JSON.stringify({cond: cond? (cond.closest('label').textContent||'').slice(0,60):null, tas});
    })()""")
    print('before:', info)
    # 1. description fix
    desc_idx = json.loads(info)['tas'] and max(json.loads(info)['tas'], key=lambda t: t['len'])['i']
    cur = H.js("(() => { const tas=[...document.querySelectorAll('textarea')]; return tas[%d]?tas[%d].value:''; })()" % (desc_idx, desc_idx))
    if wrong_frag and wrong_frag in cur:
        new = cur.replace(wrong_frag, correct_line)
        H.js("""(() => {
          const tas=[...document.querySelectorAll('textarea')]; const ta=tas[%d];
          const st=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;
          st.call(ta, %%s); ta.dispatchEvent(new Event('input',{bubbles:true}));
        })()""" % desc_idx % json.dumps(new))
        time.sleep(1.5)
        print('desc fixed')
    # 2. condition fix
    r2 = js_set_combobox('Condition', 'usedgood')
    print('cond select:', r2)
    time.sleep(2)
    info2 = H.js("""(() => {
      const cond=[...document.querySelectorAll('[role=combobox]')].filter(e=>e.offsetParent!==null)
        .find(e=>{const l=e.closest('label'); return l && (l.textContent||'').trim().startsWith('Condition');});
      return cond ? (cond.closest('label').textContent||'').trim() : 'none';
    })()""")
    print('after cond:', info2)
    # 3. save
    r = H.js("""(() => {
      const btns=[...document.querySelectorAll('div[role=button],button')].filter(b=>(b.innerText||'').trim()==='Save' || (b.innerText||'').trim()==='Post');
      if(!btns.length) return JSON.stringify({ok:false});
      const b=btns[btns.length-1]; const r=b.getBoundingClientRect();
      return JSON.stringify({ok:true,x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2),t:(b.innerText||'').trim()});
    })()""")
    d = json.loads(r) if r else {'ok': False}
    if not d.get('ok'):
        print('SAVE BTN NOT FOUND'); return
    print('clicking', d['t'])
    click(d['x'], d['y']); time.sleep(6)
    print('SAVED:', title_sub)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '', sys.argv[3] if len(sys.argv) > 3 else 'UK Pre-Owned, Tested Working')

#!/usr/bin/env python3
"""gform_fill.py — add questions to a Google Form editor via :9222 (28/10/26).
Verified flow: click 'Add question' (Google auto-creates + focuses the new title
box) -> Input.insertText(question) -> read back to verify.
Usage:
  gform_fill.py <url-substr> click-add
  gform_fill.py <url-substr> type "<question text>"
  gform_fill.py <url-substr> read                # dump current form text
  gform_fill.py <url-substr> add "<question>" ["type"]   # click-add + type (+ set type)
"""
import sys, json, time, urllib.request, websocket

DEBUG = 'http://127.0.0.1:9222'


def tabs():
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return json.loads(op.open(DEBUG + '/json', timeout=10).read())


def ws_for(substr):
    for t in tabs():
        if substr in (t.get('url') or ''):
            return t['webSocketDebuggerUrl']
    return None


def send(wsurl, method, params, timeout=30):
    ws = websocket.create_connection(wsurl, timeout=timeout)
    mid = int(time.time() * 1000) % 1000000
    ws.send(json.dumps({'id': mid, 'method': method, 'params': params}))
    dead = time.time() + timeout
    while time.time() < dead:
        try:
            m = json.loads(ws.recv())
        except Exception:
            break
        if m.get('id') == mid:
            ws.close()
            return m.get('result', {})
    ws.close()
    return {'timeout': True}


def eval_js(wsurl, expr, timeout=25):
    r = send(wsurl, 'Runtime.evaluate',
             {'expression': expr, 'returnByValue': True, 'awaitPromise': True}, timeout)
    er = r.get('result', {})
    if er.get('exceptionDetails'):
        return 'EXC:' + str(er['exceptionDetails'])[:200]
    return er.get('value')


def click_add(wsurl):
    js = ("(()=>{const b=Array.from(document.querySelectorAll('*')).find("
          "e=>e.getAttribute('aria-label')==='Add question'&&e.getBoundingClientRect().x>0);"
          "if(b){b.click();return true;}return false;})()")
    return eval_js(wsurl, js)


def insert_text(wsurl, text):
    return send(wsurl, 'Input.insertText', {'text': text})


def read_questions(wsurl):
    t = eval_js(wsurl, "document.body?document.body.innerText:''")
    if not isinstance(t, str):
        return str(t)
    idx = t.find('This form is automatically')
    body = t[idx:idx + 2500] if idx != -1 else t[:2500]
    return body


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    sub, act = sys.argv[1], sys.argv[2]
    w = ws_for(sub)
    if not w:
        print("NO TAB for", sub); sys.exit(1)
    if act == 'click-add':
        print('clicked add:', click_add(w)); time.sleep(1.5)
        print('verify:', read_questions(w)[:700])
    elif act == 'type' and len(sys.argv) > 3:
        print('insert:', insert_text(w, sys.argv[3]))
        time.sleep(.5)
        print('verify:', read_questions(w)[:700])
    elif act == 'fill-idx' and len(sys.argv) > 4:
        idx = int(sys.argv[3]); q = sys.argv[4]
        # Focus the contenteditable via JS click (same mechanism that worked for 'add')
        js = ("(()=>{const ces=Array.from(document.querySelectorAll('[contenteditable=true]'));"
              "const e=ces[" + str(idx) + "];if(!e)return 'no-idx';"
              "e.querySelector ? 0 : 0; "
              "e.focus(); const r=e.getBoundingClientRect(); "
              "return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2,ok:true});})()")
        pos = eval_js(w, js)
        try:
            p = json.loads(pos) if isinstance(pos, str) else pos
        except Exception:
            p = {}
        if p and p.get('ok'):
            # real click via element JS select + Input dispatch on its coords (element is on-screen)
            send(w, 'Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': p['x'], 'y': p['y'], 'button': 'left', 'clickCount': 1})
            send(w, 'Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': p['x'], 'y': p['y'], 'button': 'left', 'clickCount': 1})
            time.sleep(.5)
            # use Input.imeSetComposition then insertText (Google rich-text needs it)
            send(w, 'Input.imeSetComposition', {'text': q, 'selectionStart': 0, 'selectionEnd': len(q)})
            time.sleep(.2)
            send(w, 'Input.insertText', {'text': q})
            time.sleep(.5)
            print('inserted via IME at', int(p['x']), int(p['y']))
        time.sleep(.5)
        print('--- readback (idx16-21) ---')
        print(eval_js(w, "(()=>{const ces=Array.from(document.querySelectorAll('[contenteditable=true]'));"
                         "return JSON.stringify(ces.slice(14).map((e,i)=>({i:14+i,txt:e.innerText.slice(0,45)})));})()"))
    elif act == 'read':
        print(read_questions(w)[:2500])
    elif act == 'add' and len(sys.argv) > 3:
        q = sys.argv[3]
        print('add click:', click_add(w)); time.sleep(1.5)
        print('type:', insert_text(w, q)); time.sleep(.5)
        if len(sys.argv) > 4:
            # infer type not yet robust; skip for now
            pass
        print('--- readback ---')
        print(read_questions(w)[:1000])
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""cdp_eval.py — robust CDP Runtime.evaluate against a :9222 tab (28/10/26)."""
import sys, json, time, urllib.request, websocket

DEBUG = 'http://127.0.0.1:9222'


def list_tabs():
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return json.loads(op.open(DEBUG + '/json', timeout=10).read())


def eval_js(ws_url, expression, timeout=30):
    ws = websocket.create_connection(ws_url, timeout=timeout)
    mid = 1
    ws.send(json.dumps({'id': mid, 'method': 'Runtime.evaluate',
                        'params': {'expression': expression, 'returnByValue': True,
                                   'awaitPromise': True}}))
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            m = json.loads(ws.recv())
        except Exception:
            return {'error': 'recv-timeout'}
        if m.get('id') == mid:
            ws.close()
            if 'result' in m:
                return {'value': m['result'].get('result', {}).get('value'),
                        'exception': m['result'].get('exceptionDetails')}
            return {'error': m.get('error', {})}
    ws.close()
    return {'error': 'no-response'}


def connect_tab(substr):
    for t in list_tabs():
        if substr in (t.get('url') or ''):
            return t.get('webSocketDebuggerUrl'), t.get('title', ''), t.get('url', '')
    return None, None, None


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: cdp_eval.py <url-substr> <js-expr>"); sys.exit(1)
    ws, title, url = connect_tab(sys.argv[1])
    if not ws:
        print("NO TAB for", sys.argv[1]); sys.exit(1)
    print(json.dumps({'title': title, 'url': url[:80]}))
    r = eval_js(ws, sys.argv[2])
    print(json.dumps(r, ensure_ascii=False)[:4000])
"""CDP DOM.setFileInputFiles photo upload for the FB create form."""
import sys, json, time
sys.path.insert(0, r'C:\Users\User\.hermes\workspace\Vault\business\2real\2real-agent\channel_upload_package')
import cdp_harness as H

def attach_create():
    # close any existing create tabs, then open a fresh one (resets dirty form)
    for t in H.list_tabs():
        if '/marketplace/create/item' in t['url']:
            try:
                H._send('Target.closeTarget', targetId=t['targetId'])
            except Exception:
                pass
    r = H._send('Target.createTarget', url='https://www.facebook.com/marketplace/create/item')
    time.sleep(8)
    tabs = [t for t in H.list_tabs() if '/marketplace/create/item' in t['url']]
    ws = tabs[0]['webSocketDebuggerUrl']
    import websocket
    if H._conn:
        try: H._conn.close()
        except Exception: pass
    H._conn = websocket.create_connection(ws, timeout=180, suppress_origin=True)
    return tabs[0]

def set_file(path):
    doc = H._send('DOM.getDocument')
    root = doc['root']['nodeId']
    q = H._send('DOM.querySelectorAll', nodeId=root, selector='input[type=file]')
    done = False
    for nid in q['nodeIds']:
        if done: continue
        attrs = H._send('DOM.getAttributes', nodeId=nid)
        a = attrs.get('attributes', [])
        acc = a[a.index('accept')+1] if 'accept' in a else ''
        if 'image' in acc:
            H._send('DOM.setFileInputFiles', files=[path], nodeId=nid)
            H._send('Runtime.evaluate', expression="""
              [...document.querySelectorAll('input[type=file]')].forEach(i=>{ if((i.accept||'').includes('image')) i.dispatchEvent(new Event('change',{bubbles:true})); });
            """, returnByValue=True)
            done = True
    # dispatch change on all of them via JS
    time.sleep(3)
    r = H.js("(function(){ const m=document.body.innerText.match(/(\\d+)\\s+photo[s]?\\s+attached/); return m?parseInt(m[1]):0; })()")
    return r

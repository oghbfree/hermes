#!/usr/bin/env python3
"""Tiny TCP forwarder: 127.0.0.1:9222 -> 127.0.0.1:<live CDP port from DevToolsActivePort>.
The harvest/send scripts hard-code FB_CDP_URL=127.0.0.1:9222, but the persistent browser
launches with --remote-debugging-port=0 (random), so 9222 is stale. Tunnel bridges them.
Usage: python cdp_tunnel_9222.py
"""
import socket, threading, time, os, sys

ACTIVE_PORT_FILE = r"C:\Users\User\AppData\Local\hermes\browser-profile\chrome\DevToolsActivePort"

def live_port():
    try:
        with open(ACTIVE_PORT_FILE) as f:
            p = f.read().split("\n")[0].strip()
        if p.isdigit():
            return int(p)
    except OSError:
        pass
    return None

def pipe(src, dst):
    try:
        while True:
            b = src.recv(65536)
            if not b:
                break
            dst.sendall(b)
    except Exception:
        pass
    finally:
        try: dst.shutdown(socket.SHUT_WR)
        except Exception: pass
        try: dst.close()
        except Exception: pass
        try: src.close()
        except Exception: pass

def handle(client):
    lp = live_port()
    if not lp:
        client.close()
        return
    try:
        upstream = socket.create_connection(("127.0.0.1", lp), timeout=5)
    except Exception:
        client.close()
        return
    threading.Thread(target=pipe, args=(client, upstream), daemon=True).start()
    threading.Thread(target=pipe, args=(upstream, client), daemon=True).start()

def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 9222))
    srv.listen(50)
    sys.stdout.write("tunnel up 9222 -> %s\n" % live_port())
    sys.stdout.flush()
    while True:
        c, _ = srv.accept()
        threading.Thread(target=handle, args=(c,), daemon=True).start()

if __name__ == "__main__":
    main()
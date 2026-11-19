#!/usr/bin/env python3
"""Relay 127.0.0.1:9222 -> 127.0.0.1:64365 (live CDP port). Blocking upstream.
Ad-hoc: the harvest/send scripts hard-code 9222 but DevToolsActivePort is stale (63676)."""
import socket, threading, time, sys

LP = 64365

def connect_up():
    for _ in range(100):
        try:
            s = socket.create_connection(("127.0.0.1", LP), timeout=5)
            s.settimeout(None)  # BLOCKING - must not misread idle as close
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            return s
        except Exception:
            time.sleep(0.3)
    return None

def relay(client):
    up = [connect_up()]
    if up[0] is None:
        try: client.close()
        except Exception: pass
        return
    running = [True]
    def reconnect_up():
        try: up[0].close()
        except Exception: pass
        up[0] = connect_up()
    def c2u():
        while running[0]:
            try: b = client.recv(65536)
            except Exception: b = b""
            if not b:
                running[0] = False; break
            u = up[0]
            if u is None:
                time.sleep(0.2); continue
            try: u.sendall(b)
            except Exception: reconnect_up()
        try: client.close()
        except Exception: pass
    def u2c():
        while running[0]:
            u = up[0]
            if u is None:
                time.sleep(0.2); continue
            try: b = u.recv(65536)
            except Exception: b = b""
            if not b:
                reconnect_up()  # TRUE EOF (blocking socket => not an idle false-positive)
                continue
            try: client.sendall(b)
            except Exception:
                running[0] = False; break
        try: client.close()
        except Exception: pass
    threading.Thread(target=c2u, daemon=True).start()
    threading.Thread(target=u2c, daemon=True).start()

def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 9222))
    srv.listen(200)
    sys.stdout.write("tunnel 9222 -> %d blocking ready\n" % LP)
    sys.stdout.flush()
    while True:
        c, _ = srv.accept()
        threading.Thread(target=relay, args=(c,), daemon=True).start()

if __name__ == "__main__":
    main()
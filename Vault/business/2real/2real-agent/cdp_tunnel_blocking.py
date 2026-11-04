#!/usr/bin/env python3
"""Pure pass-through TCP relay: 127.0.0.1:9222 -> live CDP port (DevToolsActivePort).
The harvest/send scripts hard-code FB_CDP_URL=127.0.0.1:9222, but the persistent
business browser launches with --remote-debugging-port=0 (a random port), so 9222
is stale. This relays bytes verbatim so the scripts' WS / JSON-over-HTTP calls reach
the real browser.

CRITICAL: the upstream socket must be BLOCKING (settimeout(None)). If it inherits a
recv timeout from create_connection, a long idle (e.g. the sender's ~28s anti-velocity
pause) makes the relay's recv raise socket.timeout, which was being misread as an
upstream close -> reconnect -> the client's persistent WebSocket silently dies and
every subsequent send "Connection timed out". A true EOF/close is the only reason to
reconnect.
"""
import socket, threading, time, sys

ACTIVE_PORT_FILE = r"C:\Users\User\AppData\Local\hermes\browser-profile\chrome\DevToolsActivePort"

def live_port():
    try:
        with open(ACTIVE_PORT_FILE) as f:
            p = f.read().split("\n")[0].strip()
        return int(p) if p.isdigit() else None
    except OSError:
        return None

def connect_up():
    for _ in range(50):
        lp = live_port()
        if lp:
            try:
                s = socket.create_connection(("127.0.0.1", lp), timeout=5)
                s.settimeout(None)          # BLOCKING — do not misread idle as close
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                return s
            except Exception:
                pass
        time.sleep(0.5)
    return None

def pipe(src, dst, running, on_upstream_dead):
    """src->dst. Return when src EOFs (client) or upstream dies.
    on_upstream_dead called if the death was the upstream socket (so caller can reconnect)."""
    while running[0]:
        try:
            b = src.recv(65536)
        except Exception:
            b = b""
        if not b:
            if src is dst:  # placeholder never used
                pass
            return "client" if not _is_up(src) else "upstream"
        try:
            dst.sendall(b)
        except Exception:
            on_upstream_dead()
            return "upstream"

def _is_up(sock):
    return True

class Relay:
    def __init__(self, client):
        self.client = client
        self.up = None
        self.running = [True]

    def run(self):
        self.up = connect_up()
        if self.up is None:
            try: self.client.close()
            except Exception: pass
            return
        def reconnect_up():
            try: self.up.close()
            except Exception: pass
            self.up = connect_up()
        def c2u():
            while self.running[0]:
                try: b = self.client.recv(65536)
                except Exception: b = b""
                if not b:
                    self.running[0]=False; break
                u = self.up
                if u is None:
                    time.sleep(0.2); continue
                try: u.sendall(b)
                except Exception: reconnect_up()
            try: self.client.close()
            except Exception: pass
        def u2c():
            while self.running[0]:
                u = self.up
                if u is None:
                    time.sleep(0.2); continue
                try: b = u.recv(65536)
                except Exception: b = b""
                if not b:
                    # TRUE upstream EOF (blocking socket, so not an idle false-positive)
                    reconnect_up()
                    continue
                try: self.client.sendall(b)
                except Exception:
                    self.running[0]=False
            try: self.client.close()
            except Exception: pass
        threading.Thread(target=c2u, daemon=True).start()
        threading.Thread(target=u2c, daemon=True).start()

def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 9222))
    srv.listen(200)
    sys.stdout.write("tunnel 9222 -> %s blocking ready\n" % live_port())
    sys.stdout.flush()
    while True:
        c, _ = srv.accept()
        threading.Thread(target=Relay(c).run, daemon=True).start()

if __name__ == "__main__":
    main()
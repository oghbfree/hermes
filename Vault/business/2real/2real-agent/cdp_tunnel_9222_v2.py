#!/usr/bin/env python3
"""Robust TCP relay: 127.0.0.1:9222 -> live CDP port (from DevToolsActivePort).
The harvest/send scripts hard-code FB_CDP_URL=127.0.0.1:9222, but the persistent
browser launches with --remote-debugging-port=0 (random), so 9222 is stale.

Survives transient browser-side resets: on upstream read failure it re-connects to
the live CDP port, so the client's long-lived WebSocket to :9222 stays open.
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
                return socket.create_connection(("127.0.0.1", lp), timeout=5)
            except Exception:
                pass
        time.sleep(0.5)
    return None

class Relay:
    def __init__(self, client):
        self.client = client
        self.up = None
        self.running = True

    def run(self):
        self.up = connect_up()
        if self.up is None:
            try: self.client.close()
            except Exception: pass
            return
        def safe_send(sock, b):
            try: sock.sendall(b); return True
            except Exception: return False
        def c2u():
            while self.running:
                try: b = self.client.recv(65536)
                except Exception: b = b""
                if not b:
                    self.running = False; break
                if not safe_send(self.up, b):
                    self.up = connect_up()
            try: self.client.close()
            except Exception: pass
        def u2c():
            while self.running:
                u = self.up
                if u is None:
                    time.sleep(0.2); continue
                try: b = u.recv(65536)
                except Exception: b = b""
                if not b:
                    try: u.close()
                    except Exception: pass
                    self.up = connect_up()
                    continue
                if not safe_send(self.client, b):
                    self.running = False
            try: self.client.close()
            except Exception: pass
        threading.Thread(target=c2u, daemon=True).start()
        threading.Thread(target=u2c, daemon=True).start()

def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 9222))
    srv.listen(50)
    sys.stdout.write("tunnel 9222 -> %s ready\n" % live_port())
    sys.stdout.flush()
    while True:
        c, _ = srv.accept()
        threading.Thread(target=Relay(c).run, daemon=True).start()

if __name__ == "__main__":
    main()
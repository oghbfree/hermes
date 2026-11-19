import socket, threading, sys
# bridge 127.0.0.1:9222 -> 127.0.0.1:64365 (confirmed live CDP port), blocking upstream
LP = 64365
def connect_up():
    for _ in range(50):
        try:
            s = socket.create_connection(("127.0.0.1", LP), timeout=5)
            s.settimeout(None)  # BLOCKING - critical
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            return s
        except Exception:
            pass
    return None
running=[True]
def relay(client):
    up = connect_up()
    if up is None:
        try: client.close()
        except: pass
        return
    def rec(): 
        while running[0]:
            try: b=client.recv(65536)
            except: b=b""
            if not b: running[0]=False; break
            try: up.sendall(b)
            except:
                try: up.close()
                except: pass
                u=connect_up()
                if u is None: pass
                else: 
                    global _up; _up=u
    def send():
        u=up
        while running[0]:
            try: b=u.recv(65536)
            except: b=b""
            if not b:
                # true EOF: reconnect upstream
                try: up.close()
                except: pass
                u=connect_up()
                if u is None: time.sleep(0.2)
                continue
            try: client.sendall(b)
            except: running[0]=False; break
        try: client.close()
        except: pass
    threading.Thread(target=rec,daemon=True).start()
    threading.Thread(target=send,daemon=True).start()
srv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
srv.bind(("127.0.0.1",9222)); srv.listen(200)
sys.stdout.write("tunnel 9222 -> 64365 blocking ready\n"); sys.stdout.flush()
while True:
    c,_=srv.accept()
    threading.Thread(target=relay,daemon=True).start()

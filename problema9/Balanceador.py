import socket
import socketserver
import threading
import time

nodes = []
current_node = 0
lock = threading.Lock()

class LoadBalancerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global current_node
        data = self.request.recv(1024).decode()

        if data.startswith("Registrar"):
            _, n_id, n_port = data.split(":")
            with lock:
                nodes.append({"id": n_id, "port": int(n_port)})
            print(f"Nodo registrado: {n_id}{n_port}")
            return

        with lock:
            if not nodes:
                self.request.sendall(b"No hay backends disponibles.")
                return
            
            target = nodes[current_node]
            current_node = (current_node + 1) % len(nodes)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("localhost", target["port"]))
                s.sendall(data.encode())
                res = s.recv(1024)
                self.request.sendall(res)
        except:
            print(f"Nodo {target['id']} falló.")
            with lock:
                nodes.remove(target)

def health_check():
    while True:
        time.sleep(10)
        with lock:
            for node in nodes[:]:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(2)
                        s.connect(("localhost", node["port"]))
                        s.sendall(b"salud")
                        if s.recv(1024) != b"OK": raise Exception()
                except:
                    print(f"salud Check falló para {node['id']}")
                    nodes.remove(node)

if __name__ == "main":
    threading.Thread(target=health_check, daemon=True).start()   
    with socketserver.ThreadingTCPServer(("localhost", 9000), LoadBalancerHandler) as lb:
        print("Balanceador de Carga iniciado")
        lb.serve_forever()
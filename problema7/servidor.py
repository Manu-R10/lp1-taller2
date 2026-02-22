import socket
import socketserver
import threading

HOST = "localhost"
PORT = 8088
BUFFER_SIZE = 8111

class ProxyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            data = self.request.recv(BUFFER_SIZE)
            if not data: return
            
            peticion = data.decode('utf-8', errors='ignore')
            primera_linea = peticion.split('\n')[0]
            print(f"Solicitud: {primera_linea}")

            partes = primera_linea.split(' ')
            if len(partes) < 2: return
            
            metodo = partes[0]
            url = partes[1]

            if metodo == "CONECTAR":
                
                host, puerto = url.split(':')
                self.handle_tunnel(host, int(puerto))
            else:
                host = url.replace("http://", "").split('/')[0]
                self.handle_http(host, 80, data)

        except Exception as e:
            print(f"Error en Proxy: {e}")

    def handle_http(self, host, puerto, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_sock:
            remote_sock.connect((host, puerto))
            remote_sock.sendall(data)

            while True:
                respuesta = remote_sock.recv(BUFFER_SIZE)
                if not respuesta: break
                self.request.sendall(respuesta)

    def handle_tunnel(self, host, puerto):
        """Túnel para HTTPS (Método CONECTAR)"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_sock:
            try:
                remote_sock.connect((host, puerto))
                self.request.sendall(b"HTTP/1.1 200 Conecta\r\n\r\n")
  
                self.bridge(self.request, remote_sock)
            except Exception as e:
                print(f"Error en: {e}")

    def bridge(self, client, remote):
   
        def forward(source, dest):
            try:
                while True:
                    data = source.recv(BUFFER_SIZE)
                    if not data: break
                    dest.sendall(data)
            except: pass

    
        t = threading.Thread(target=forward, args=(remote, client), daemon=True)
        t.start()
  
        forward(client, remote)

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((HOST, PORT), ProxyHandler) as server:
        print(f"Proxy activo en {HOST}:{PORT}")
        server.serve_forever()
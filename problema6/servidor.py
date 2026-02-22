import socketserver
import threading
import os

HOST = "localhost"
PORT = 9000


salas = {"General": []}
usuarios = {} 
user_room = {} 
lock = threading.Lock()

class ChatHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        usuario_conectado = False
        try:
            while True:
                
                data = self.request.recv(1024).decode().strip()
                if not data: break

                parts = data.split(":")
                comando = parts[0]

              
                if comando == "entrar a manu":
                    username = parts[1]
                    with lock:
                        usuarios[self.request] = username
                        user_room[self.request] = "General"
                        salas["General"].append(self.request)
                    usuario_conectado = True
                    self.broadcast("General", f"Servidor: {username} ha entrado")
                    self.request.sendall(b"Conectado")

                elif comando == "MSG" and usuario_conectado:
                    contenido = parts[1]
                    room = user_room[self.request]
                    user = usuarios[self.request]
                    self.broadcast(room, f"[{room}] {user}: {contenido}", self.request)

                elif comando == "unirse":
                    nueva_sala = parts[1]
                    self.cambiar_sala(nueva_sala)

                elif comando == "privado":
                    target = parts[1]
                    msj = parts[2]
                    self.enviar_privado(target, msj)

        except Exception as e:
            print(f"Error {e}")
        finally:
            self.limpiar_conexion()

    def broadcast(self, room_name, mensaje, exclude_sock=None):
        with lock:
            for client in salas.get(room_name, []):
                if client != exclude_sock:
                    try:
                        client.sendall(mensaje.encode())
                    except: pass

    def cambiar_sala(self, nueva_sala):
        user = usuarios[self.request]
        with lock:
         
            old_room = user_room[self.request]
            if self.request in salas[old_room]:
                salas[old_room].remove(self.request)
            if nueva_sala not in salas:
                salas[nueva_sala] = []
            salas[nueva_sala].append(self.request)
            user_room[self.request] = nueva_sala
        
        self.request.sendall(f"Te has movido a {nueva_sala}".encode())
        self.broadcast(nueva_sala, f"Servidor {user} se unido")

    def enviar_privado(self, target, mensaje):
        sender = usuarios[self.request]
        found = False
        with lock:
            for sock, name in usuarios.items():
                if name == target:
                    sock.sendall(f"PRIVADO de {sender}: {mensaje}".encode())
                    found = True
                    break
        if not found:
            self.request.sendall(b"Usuario no encontrado.")

    def limpiar_conexion(self):
        with lock:
            if self.request in usuarios:
                room = user_room[self.request]
                if self.request in salas[room]:
                    salas[room].remove(self.request)
                del usuarios[self.request]
                del user_room[self.request]
        self.request.close()

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((HOST, PORT), ChatHandler) as server:
        print(f"Servidor de Chat en {HOST}:{PORT}")
        server.serve_forever()
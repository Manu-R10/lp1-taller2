import socketserver
import threading
import json

HOST = "localhost"
PORT = 9000

class TicTacToe:
    def __init__(self):
        self.tablero = [" "] * 9
        self.turno = "X"
        self.ganador = None
        self.jugadores = [] 
        self.espectadores = []

    def mover(self, posicion, simbolo):
        if self.tablero[posicion] == " " and self.turno == simbolo:
            self.tablero[posicion] = simbolo
            self.turno = "O" if simbolo == "X" else "X"
            self.verificar_ganador()
            return True
        return False

    def verificar_ganador(self):
        vias = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in vias:
            if self.tablero[a] == self.tablero[b] == self.tablero[c] != " ":
                self.ganador = self.tablero[a]
        if " " not in self.tablero and not self.ganador:
            self.ganador = "Empate"

partida = TicTacToe()
lock = threading.Lock()

class GameHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global partida
        print(f"Nueva conexión: {self.client_address}")
        
        with lock:
            if len(partida.jugadores) < 2:
                rol = "X" if len(partida.jugadores) == 0 else "O"
                partida.jugadores.append(self.request)
                self.request.sendall(f"ROL:{rol}".encode())
            else:
                rol = "ESPECTADOR"
                partida.espectadores.append(self.request)
                self.request.sendall(b"ROL:E")
        
        self.notificar_estado()

        try:
            while not partida.ganador:
                data = self.request.recv(1024).decode()
                if not data: break
                
                if data.startswith("MOVE:") and rol in ["X", "O"]:
                    pos = int(data.split(":")[1])
                    with lock:
                        if partida.mover(pos, rol):
                            self.notificar_estado()
                        else:
                            self.request.sendall(b"Movimiento invalido")
            
            if partida.ganador:
                self.request.sendall(f"Ganador {partida.ganador}".encode())
        except:
            pass

    def notificar_estado(self):
        estado = {
            "tablero": partida.tablero,
            "turno": partida.turno,
            "ganador": partida.ganador
        }
        msg = "actualizar:" + json.dumps(estado)
        for s in partida.jugadores + partida.espectadores:
            try:
                s.sendall(msg.encode())
            except: pass

if __name__ == "main":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((HOST, PORT), GameHandler) as server:
        print("Servidor de manu iniciado")
        server.serve_forever()
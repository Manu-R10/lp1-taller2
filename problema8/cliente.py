import socket
import threading
import json

def mostrar_tablero(tablero):
    print("\n")
    print(f" {tablero[0]} | {tablero[1]} | {tablero[2]} ")
    print("-----------")
    print(f" {tablero[3]} | {tablero[4]} | {tablero[5]} ")
    print("-----------")
    print(f" {tablero[6]} | {tablero[7]} | {tablero[8]} ")

def escuchar_servidor(sock):
    while True:
        data = sock.recv(2048).decode()
        if not data: break
        
        if data.startswith("actualizar:"):
            estado = json.loads(data.split(":", 1)[1])
            mostrar_tablero(estado['tablero'])
            if estado['ganador']:
                print(f"FIN DEL Jogo: {estado['ganador']} !!!")
                break
            print(f"Es turno de: {estado['turno']}")
        elif data.startswith("ROL:"):
            print(f"Tu rol es: {data.split(':')[1]}")

def ejecutar_cliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 9000))
        threading.Thread(target=escuchar_servidor, args=(s,), daemon=True).start()
        
        print("Ingresa posición")
        while True:
            pos = input("Tu movimiento: ")
            s.sendall(f"MOVER:{pos}".encode())
if __name__ == "main":
    ejecutar_cliente()
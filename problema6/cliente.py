import socket
import threading
import sys

HOST = "localhost"
PORT = 9000

def escuchar_servidor(sock):
    while True:
        try:
            data = sock.recv(4096).decode()
            if data:
                print(f"\r{data}\n> ", end="")
            else:
                break
        except:
            break

def ejecutar_cliente():
    print("Cliente de Chat")
    nombre = input("Tu nombre de usuario es ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
       
            s.sendall(f"unirse {nombre}".encode())

            threading.Thread(target=escuchar_servidor, args=(s,), daemon=True).start()

            while True:
                opcion = input("> ")
                
                if opcion.startswith("/unirse "):
                    sala = opcion.split(" ")[1]
                    s.sendall(f"unirse {sala}".encode())
                
                elif opcion.startswith("/privado "):
                    parts = opcion.split(" ", 2)
                    s.sendall(f"privado:{parts[1]}:{parts[2]}".encode())
                
                elif opcion.lower() == "salirse":
                    break
                
                else:
                    s.sendall(f"MSG:{opcion}".encode())

        except ConnectionRefusedError:
            print("Servidor esta apagado.")

if __name__ == "__main__":
    ejecutar_cliente()
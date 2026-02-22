import socket

def peticion_cliente(msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 9000))
        s.sendall(msg.encode())
        print(f"El servidor nos dice: {s.recv(1024).decode()}")

if __name__ == "__main__":
    while True:
        m = input("Mensaje para el clúster: ")
        peticion_cliente(m)
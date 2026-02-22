import socket
import threading

def start_backend(node_id, port, lb_port=9000):
    host = "localhost"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, lb_port))
            s.sendall(f"registrarse:{node_id}:{port}".encode())
    except:
        print(f"Balanceador no encontrado {lb_port}")

    print(f"{node_id} activo en el puerto {port}")

    while True:
        conn, addr = server.accept()
        data = conn.recv(1024).decode()
        
        if data == "SALUD":
            conn.sendall(b"OK")
        else:
            print(f"{node_id} procesando: {data}")
            conn.sendall(f"Respuesta{node_id}: {data}".encode())
        conn.close()

if __name__ == "main":
    import sys
    start_backend(sys.argv[1], int(sys.argv[2]))
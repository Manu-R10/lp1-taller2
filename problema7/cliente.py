import socket

PROXY_HOST = "localhost"
PROXY_PORT = 8088

def ejecutar_cliente():
    print("Cliente de Prueba Proxy")
    print("1.Probar HTTP")
    print("2.Probar HTTPS CONECTAR")
    opcion = input("Seleccionar: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((PROXY_HOST, PROXY_PORT))

            if opcion == "1":
             
                peticion = (
                    "GET http://www.example.com/ HTTP/1.1\r\n"
                    "Host: www.example.com\r\n"
                    "Connection: close\r\n\r\n"
                )
                s.sendall(peticion.encode())
            
            elif opcion == "2":
        
                peticion = "CONECTAR google.com:443 HTTP/1.1\r\n\r\n"
                s.sendall(peticion.encode())

            respuesta = s.recv(4096)
            print("\nRESPUESTA RECIBIDA")
            print(respuesta.decode('utf-8', errors='ignore'))

        except Exception as e:
            print(f"Error de conexión: {e}")

if __name__ == "__main__":
    ejecutar_cliente()
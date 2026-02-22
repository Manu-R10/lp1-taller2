import socket
import os
import hashlib

HOST = "localhost"
PORT = 9000
BUFFER_SIZE = 4096

def calcular_hash(ruta):
    sha = hashlib.sha256()
    with open(ruta, "rb") as f:
        while chunk := f.read(BUFFER_SIZE):
            sha.update(chunk)
    return sha.hexdigest()

def ejecutar_cliente():
    print("Cliente de Transferencia")
    print("1 Subir Archivo (UPLOAD)")
    print("2 Listar Archivos (LIST)")
    opcion = input("Selecciona una opción de manu: ")

    # Crear el socket (como hacíamos con HTTPConnection)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))

            if opcion == "1":
                ruta = input("Ruta del archivo: ")
                if not os.path.exists(ruta): return print("No existe")
                
                nombre = os.path.basename(ruta)
                tamano = os.path.getsize(ruta)
                f_hash = calcular_hash(ruta)

                # Enviar encabezado
                header = f"UPLOAD:{nombre}:{tamano}:{f_hash}"
                s.sendall(header.encode())

                # Enviar datos por bloques (Control de flujo)
                with open(ruta, "rb") as f:
                    while chunk := f.read(BUFFER_SIZE):
                        s.sendall(chunk)
                
                print("Esperando validación del servidor de manu")

            elif opcion == "2":
                s.sendall(b"LIST:all")
            
            # Recibir respuesta final
            respuesta = s.recv(4096).decode()
            print(f"\nRespuesta del servidor:\n{respuesta}")

        except ConnectionRefusedError:
            print("El servidor de manu no está encendido.")

if __name__ == "__main__":
    ejecutar_cliente()
#!/usr/bin/env python3
"""
Problema 2: Comunicación bidireccional - Cliente
Objetivo: Crear un cliente TCP que envíe un mensaje al servidor y reciba la misma respuesta
"""

#!/usr/bin/env python3
import socket

#
HOST = '127.0.0.1' 
PORT = 65432

# 
message = input("Mensaje: ")

# 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # 
    client_socket.connect((HOST, PORT))
    
    # TODO 
    
    # 
    client_socket.sendall(message.encode()) 
    print(f"Mensaje '{message}' enviado.")
    
    # 
    data = client_socket.recv(1000)
    
    # 
    print("Mensaje recibido del servidor: ", data.decode())

# 
print("Conexión cerrada.")
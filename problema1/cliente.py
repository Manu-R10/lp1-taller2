#!/usr/bin/env python3
"""
Problema 1: Sockets básicos - Cliente
Objetivo: Crear un cliente TCP que se conecte a un servidor e intercambie mensajes básicos
"""

import socket

HOST = '127.0.0.1' 
PORT = 65432

# TODO: 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #TODO: 
    print(f"Conectandose a {HOST}:{PORT}...")
    s.connect((HOST, PORT))
    # TODO:
    mensaje = "Hola, servidor de manu."
    s.sendall(mensaje.encode('utf-8'))
    print("Mensaje enviado.")
    # TODO:
    data = s.recv(1024)
    # TODO: 
    print(f"Recibido del servidor de manu: {data.decode('utf-8')}")
    # TODO:
print("Conexión finalizada.")
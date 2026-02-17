#!/usr/bin/env python3
"""
Problema 1: Sockets básicos - Servidor
Objetivo: Crear un servidor TCP que acepte una conexión y intercambie mensajes básicos
"""

import socket

# TODO: 
HOST = '127.0.0.1' 
PORT = 65432

# TODO: 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) 
    s.listen(1)         
    print(f"Servidor de manu en esperaa.") 
    
    conn, addr = s.accept() 
    with conn:
        print(f"Conexión realizada por {addr}")
        
        # TODO: 
        data = conn.recv(1024)
        
        if not data:
            print("No se recibieron datos.")
        else:
            print(f"El cliente nos dice: {data.decode('utf-8')}")
            
            # TODO: 
            respuesta = "Mensaje recibido."
            conn.sendall(respuesta.encode('utf-8'))
            print("Respuesta enviada.")

# TODO: 
print("Servidor cerrado.")
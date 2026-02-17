#!/usr/bin/env python3
"""
Problema 2: Comunicación bidireccional - Servidor
Objetivo: Crear un servidor TCP que devuelva exactamente lo que recibe del cliente
"""

import socket


HOST = '127.0.0.1' 
PORT = 65432


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
   
    server_socket.bind((HOST, PORT))
    
    
    server_socket.listen(1)
    print(f"Servidor de manu en espera {HOST}:{PORT}...")

    while True:
      
        conn, addr = server_socket.accept()
        
        with conn:
            print(f"Conexión desde: {addr}")
            
            while True:
               
                data = conn.recv(1024)
                
               
                if not data:
                    print(f"Cliente {addr} desconectado.")
                    break
                
                print(f"Recibido: {data.decode()}")
                
                
                conn.sendall(data)
                print("Respuesta enviada.")
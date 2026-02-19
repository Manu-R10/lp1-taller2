#!/usr/bin/env python3
"""
Problema 3: Chat simple con múltiples clientes - Servidor
"""

import socket
import threading

# TODO: 
SERVER_HOST = '127.0.0.1' 
SERVER_PORT = 12345        

# 
clients = []

def broadcast(message, sender_socket):
    """
    Envía un mensaje a todos los clientes conectados excepto al remitente.
    """
    for client in clients:
        if client != sender_socket:
            try:
                # TODO:
                client.send(message.encode('utf-8'))
            except:
                # 
                if client in clients:
                    clients.remove(client)

def handle_client(client_socket, client_name):
    """
    Maneja la comunicación con un cliente específico en un hilo separado.
    """
    while True:
        try:
            # TODO: )
            data = client_socket.recv(1001)
            
            # 
            if not data:
                break
                
            # 
            message = f"{client_name}: {data.decode('utf-8')}"
            
            # 
            print(message)
            
            # TODO: 
            broadcast(message, client_socket)
            
        except (ConnectionResetError, ConnectionAbortedError):
            break
        except Exception as e:
            print(f"Error con {client_name}: {e}")
            break

    # 
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()
    broadcast(f" {client_name} ha salido del chat", None)
    print(f" Conexión cerrada con {client_name}")

# TODO: 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# TODO: 
server_socket.bind((SERVER_HOST, SERVER_PORT))

# TODO: 
server_socket.listen(5)

print(f" Servidor iniciado en {SERVER_HOST}:{SERVER_PORT}")
print("Esperando conexiones")

# 
while True:
    # TODO: 
    client, addr = server_socket.accept()
    
    try:
        # TODO:
        client_name = client.recv(1024).decode('utf-8')
        
        # TODO: 
        clients.append(client)
        
        print(f" Conexión realizada por {client_name} desde {addr}")
        
        # 
        client.send("Ya esta conectada ".encode('utf-8'))
        
        # 
        broadcast(f"--- {client_name} se ha unido. ---", client)
        
        # TODO: 
        client_handler = threading.Thread(target=handle_client, args=(client, client_name))
        client_handler.daemon = True
        client_handler.start()
        
    except Exception as e:
        print(f"Error de conexión: {e}")
        client.close()
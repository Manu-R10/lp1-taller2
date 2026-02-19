#!/usr/bin/env python3
import socket
import threading
import sys

# 
SERVER_HOST = '127.0.0.1' 
SERVER_PORT = 12345       

def receive_messages(sock):
    """
    Función para recibir mensajes sin bloquear el envío.
    """
    while True:
        try:
            # 
            message = sock.recv(1001).decode('utf-8')
            if message:
                # 
                print(f"\r{message}\nMensaje: ", end="", flush=True)
            else:
                print("\n Conexión cerrada.")
                break
        except:
            print("\n Error de conexión.")
            break
    sock.close()
    sys.exit()

#
client_name = input("Me puedes decir cual es tu nombre?  ")

# 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    
    # 
    client_socket.send(client_name.encode('utf-8'))

    # 
    # 
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    receive_thread.start()

    print(f" Hola {client_name}. Escribe 'chao' para terminar ")
    # 
    while True:

        msg_to_send = input("Mensaje: ")
        
        if msg_to_send.lower() == 'chao':
            break
        
        if msg_to_send:
            client_socket.send(msg_to_send.encode('utf-8'))

except ConnectionRefusedError:
    print("No se pudo conectar.")
except Exception as e:
    print(f"Hay un error: {e}")
finally:
    client_socket.close()
    print("Chat finalizado.")
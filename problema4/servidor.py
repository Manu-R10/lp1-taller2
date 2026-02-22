#!/usr/bin/env python3
"""
Problema 4: Servidor HTTP básico - Servidor
Objetivo: Implementar un servidor web simple que responda peticiones HTTP GET
y sirva archivos estáticos comprendiendo headers HTTP
"""

import http.server
import socket
import socketserver

# TODO: 
HOST = "localhost"  
PORT = 8000
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Manejador personalizado de peticiones HTTP.
    Hereda de SimpleHTTPRequestHandler que proporciona funcionalidad básica
    para servir archivos estáticos y manejar peticiones HTTP.
    
    SimpleHTTPRequestHandler incluye:
    - Servicio de archivos estáticos desde el directorio actual
    - Manejo de métodos HTTP GET y HEAD
    - Generación automática de listados de directorios
    - Headers HTTP básicos (Content-Type, Content-Length, etc.)
    """
    pass
    # Nota: Al no sobreescribir ningún método, se usa el comportamiento por defecto
    # que sirve archivos del directorio actual y genera listados de directorios
# TODO: 
with socketserver.TCPServer((HOST, PORT), MyRequestHandler) as httpd:
    print(f"{HOST}:{PORT}")  
    try:
        # TODO: 
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nservidor de manu esta detenido")
        httpd.shutdown()
#!/usr/bin/env python3
"""
Problema 4: Servidor HTTP básico - Cliente
Objetivo: Crear un cliente HTTP que realice una petición GET a un servidor web local
"""

import http.client

# TODO: 
HOST = 'localhost'
PUERTO = 8000

# TODO:
# HTTPConnection permite establecer conexiones HTTP con servidores
conexion = http.client.HTTPConnection(HOST, PUERTO)

# TODO: 
# request() envía la petición HTTP al servidor
# Primer parámetro: método HTTP (GET, POST, etc.)
# Segundo parámetro: path del recurso solicitado
conexion.request("GET", "/")
# TODO: 
# getresponse() devuelve un objeto HTTPResponse con los datos de la respuesta
respuesta = conexion.getresponse()
# TODO: 
# read() devuelve el cuerpo de la respuesta en bytes
datos_bytes = respuesta.read()
# TODO:
# decode() convierte los bytes a string usando UTF-8 por defecto
contenido = datos_bytes.decode('utf-8')
print("Contenido recibido")
print(contenido)
# TODO: 
conexion.close()
print("Conexión cerrada")

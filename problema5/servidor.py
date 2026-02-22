import socket
import socketserver
import os
import hashlib

HOST = "localhost"
PORT = 9000
BUFFER_SIZE = 4096
STORAGE_DIR = "server_storage"

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

class FileTransferHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        try:
        
            header_data = self.request.recv(1024).decode().split(':')
            if not header_data or len(header_data) < 2:
                return

            comando = header_data[0]

            if comando == "UPLOAD":
                filename = os.path.basename(header_data[1])
                filesize = int(header_data[2])
                client_hash = header_data[3]
                filepath = os.path.join(STORAGE_DIR, filename)

                print(f"Recibiendo {filename} ({filesize} bytes)")
                
                with open(filepath, "wb") as f:
                    received = 0
                    while received < filesize:
                        chunk = self.request.recv(min(BUFFER_SIZE, filesize - received))
                        if not chunk: break
                        f.write(chunk)
                        received += len(chunk)

               
                server_hash = self.get_checksum(filepath)
                if server_hash == client_hash:
                    self.request.sendall(b"Subida exitosa")
                    print(f"Archivo {filename} guardado correctamente.")
                else:
                    self.request.sendall(b"ERROR: Hash no coincide. Archivo descartado.")
                    os.remove(filepath)
            
            elif comando == "LIST":
                archivos = os.listdir(STORAGE_DIR)
                respuesta = "\n".join(archivos) if archivos else "(Carpeta vacía)"
                self.request.sendall(respuesta.encode())

        except Exception as e:
            print(f"Error {e}")

    def get_checksum(self, filepath):
        sha = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(BUFFER_SIZE):
                sha.update(chunk)
        return sha.hexdigest()

if __name__ == "__main__":
    
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), FileTransferHandler) as server:
        print(f"Servidor activo  {HOST}:{PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nApagando servidor dee manu")
            server.shutdown()
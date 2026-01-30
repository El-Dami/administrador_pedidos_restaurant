
import socket
import threading
import os
import sys




class Servidor:
        _instancia = None
        _lock = threading.Lock()

        def __new__(cls):
                with cls._lock:
                        if cls._instancia is None:
                                cls._instancia = super().__new__(cls)
                        return cls._instancia

        def __init__(self):
                        self._client_socket = None
                        self.server_socket = None
                        

        @classmethod
        def set_client_socket(cls, valor):
                #print('set de client_socket ============')
                #print("client socket antes de SET = ", cls._instancia._client_socket)
                cls._instancia._client_socket = valor
                #print("client socket despues de SET = ", cls._instancia._client_socket)

        @classmethod
        def get_client_socket(cls):
                return cls._instancia._client_socket

        client_socket = property(get_client_socket, set_client_socket)

        def inicializar_servidor(self):
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.host = socket.gethostname()
                self.server_ip = socket.gethostbyname(self.host)
                self.server_port = 12345
                
                
                
        
                try:
                        self.server_socket.bind((self.server_ip, self.server_port))
                        self.server_socket.listen(5)
                        print("Servidor escuchando en IP: %s Puerto: %s..." % (self.server_ip, self.server_port))
                        
                        while True:
                                client_socket, client_address = self.server_socket.accept()
                                print("Cliente conectado desde: ", client_address)
                                self.set_client_socket(client_socket)
                                threading.Thread(target=self.handle_client, args=(client_socket,)).start()

                except Exception as e:
                        print("Ocurrió un error: ", e)

                finally:
                        if self.server_socket:
                                self.server_socket.close()
        
        def handle_client(self, client_socket):
                try:
                        data = client_socket.recv(1024)
                        if data:
                                print("MENSAJE ENVIADO POR EL CLIENTE: ", data.decode())
                                message_to_send = "Conexión establecida con el servidor"
                                client_socket.send(message_to_send.encode("UTF-8"))
                                
                                data = client_socket.recv(1024).decode()
                                with open("cliente_log.txt", "a") as log_file:
                                        
                                        log_file.write(data + '\n')
                                        print("Datos registrados en cliente log.")
                                
                except Exception as e:
                        print("Ocurrió un error en el envio de mensajes: ", e)
        
        @classmethod
        def envio_a_cliente(cls, pedido, mesa):
                #print("en envio_a_cliente")
                client_socket = cls._instancia._client_socket
                #print("_client_socket en envio al cliente", client_socket)
                if client_socket is None:
                        print("El cliente no está conectado.")
                else:
                        mensaje = f"Comanda enviada por socket: {pedido} para mesa {mesa}"
                try:
                        client_socket.sendall(mensaje.encode())
                except Exception as e:
                        print("Ocurrió un error al enviar el mensaje:", e)
                        print("No recupera el Singleton inicializado por tread.")

        @classmethod
        def get_instancia(cls):
                if cls._instancia is None:
                        cls._instancia = cls()
                return cls._instancia
                

nuevo_servidor=None
if __name__ == "__main__":
        nuevo_servidor = Servidor.get_instancia()
        nuevo_servidor.inicializar_servidor()

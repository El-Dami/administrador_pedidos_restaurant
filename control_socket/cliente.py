import socket


def cliente():
        server_ip = '127.0.0.1'  
        server_port = 12345       

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
        try:
                                
                client_socket.connect((server_ip, server_port))
                print("Conexión establecida con el servidor.")
                                
                                
                client_socket.sendall(b'Conexion establecida con el cliente')
                
                                
                while True:
                                        
                        data = client_socket.recv(1024)  
                        if not data:
                                break  
                                                
                                        
                        print("MENSAJE ENVIADO POR EL SERVIDOR: ", data.decode())
                        
                        data = input("Información para el registro de log ======== ")
                        client_socket.sendall(data.encode())
                        print("Datos enviados al servidor.")
                                
        except Exception as e:
                        print("Error :" , e)
        except Exception as e:
                        print("Ocurrió un error:", e)
        finally:
                print("se cierra cliente")
                client_socket.close()
if __name__ == "__main__":
        cliente()

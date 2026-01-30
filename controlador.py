"""
controlador.py

        Módulo gestor de la ejecución del programa.


"""

from tkinter import Tk
import vista
import observador
from control_socket.conexion import ConexionAServidor



class Controlador:
        
        def __init__(self, root):
                self.root_controler = root
                self.objeto_servidor=ConexionAServidor()
                self.objeto_vista = vista.VistaPrincipal(self.root_controler, self.objeto_servidor)
                self.observador_del_comtrolador=observador.ConcreteObserverA(self.objeto_vista.base_consumos)


if __name__ == "__main__":
        raiz= Tk()
        app= Controlador(raiz)
        raiz.mainloop()
        




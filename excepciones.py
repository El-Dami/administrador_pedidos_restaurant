"""
excepciones.py

        Cuenta con las clases y métodos con los cuales se gestionan y registran los errores del programa.    

    """

import os
import datetime



class RegistroError(Exception):
    """
    La clase *RegistroError()* crea un archivo de registro de errores y registra en él las excepciones capturadas.
    """
    
    
    def __init__(self, error, archivo):
        self.error = error
        self.archivo = archivo
        self.fecha = datetime.datetime.now()
        self.BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
        self.ruta = os.path.join(self.BASE_DIR, "log.txt")

    def registrar_error(self):
        """
        Registra en el archivo *log.txt* información relevante de la excepción capturada.
        """
        log = open(self.ruta, "a")
        print("Se produjo un error:", self. error, "en el archivo ", self.archivo, "en fecha ", self.fecha, file=log)
    
    
class AplicaRegistro():
    """
    La clase *AplicaRegistro()* hace correr la excepción *RegistroError()* para poder realizar en registro de la 
    excepción capturada.
    """
    def __init__(self,motivo, nombre, error):
        t=error
        try:
            raise RegistroError(motivo, nombre) from t
        except RegistroError as log:
            log.registrar_error()
    
    

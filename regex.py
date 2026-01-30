"""
regex.py
    Proporciona los regex para validar campos de entrada.
    """

import re
from tkinter.messagebox import showerror

class Validar():
    """
    La clase *Validar()* cuenta con los métodos de validación de campos utilizados en el programa.
    """
    
    def __init__(self,)->None:
        pass
        
    def valida_producto(self, cadena):
        """
        Valida los ingresos del Entry *Producto* que debe tener exclusivamente caracteres alfabéticos.

        :param cadena: (_str_) cadena de caracteres a ser validada.

        :returns True: (_boolean_) 
        
        .. note::
            Si la validación genera un resultado False, el método retorna
            una ventana de error.
        """
        
        patron="^[A-Za-záéíóú]*$"  
        if(re.match(patron, cadena)):
            return True
        else:
            showerror(message="Ha ingresado un producto inexistente")
        
    def valida_mesa(self, cadena):
        """
        Valida los ingresos del Entry *Mesa* que debe tener exclusivamente caracteres numéricos.

        :param cadena: (_str_) cadena de caracteres a ser validada.

        :returns True: (_boolean_) 
        
        .. note::
            Si la validación genera un resultado False, el método retorna
            una ventana de error.
        """
        
        patron= re.compile('[\d^a-zA-Z]{1,2}?$')
        if(re.match(patron, cadena)):
            return True
        else:
            showerror(message="Ha ingresado un número de mesa incorrecto")
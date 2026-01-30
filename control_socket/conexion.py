    
import os
import sys
from pathlib import Path
import subprocess
import threading
#import time
#import datetime
import socket


class ConexionAServidor:
    
    def __init__(self):
        self.raiz = Path(__file__).resolve().parent
        self.ruta_server = os.path.join(self.raiz, 'servidor.py')
        
        self.theproc= ""
        #print("en __init__ ConexionAServidor =========")
        
    def try_connection(self, ): 
        #print("en try_conexion =====================")
        if self.theproc != "":
            self.theproc.kill()
            threading.Thread(target=self.lanzar_servidor, args=(True,), daemon=True).start()
        else:
            threading.Thread(target=self.lanzar_servidor, args=(True,), daemon=True).start()    
        
    
    def lanzar_servidor(self, var):

        the_path =  self.ruta_server
        if var==True:
            
            #print("en conexion, lanzar_servidor=========")
            self.theproc = subprocess.Popen([sys.executable, the_path])
            self.theproc.communicate()
        else:
            print("")

        
    def stop_server(self, ):

        if self.theproc !="":
            self.theproc.kill() 


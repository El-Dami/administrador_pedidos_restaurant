"""
modelo.py
    
        Cuenta con las clases y métodos que se ejecutan desde los *Botones* 
        de la interfaz gráfica.
        En el módulo *modelo.py* se ejecutan las clases y métodos de administración de la 
        Base de Datos (del módulo *admin_bases.py*), se realizan las validaciones 
        de campos (del módulo *regex.py*) y las capturas de excepciones (del módulo
        *excepciones.py*).
    
"""

from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno
from tkinter.filedialog import askopenfilename
from tkinter import TclError
import sys
import datetime
import vista
import regex

from control_socket.servidor import Servidor
import threading


import decoradores

from excepciones import AplicaRegistro
from admin_bases import BaseDeDatos
from admin_bases import BaseClientes
from admin_bases import BaseConsumos
from observador import Sujeto


class ClientesBD():
    """
        La Clase *ClientesBD()* cuenta con los métodos que vinculan la interfaz gráfica 
        con la tabla *clientes* de las base de datos *clientes_sql.db*.
    
    """
    
    def __init__(self):
        self.base_clientes=BaseClientes()
        self.crea_bases=BaseDeDatos()
        self.set_interfaz=vista.SetInterfaz()
        self.set_tree=vista.SetTree()
        self.validacion=regex.Validar()
    
    def alta_cliente(self, nro_mesa, cant_comensales, tree, root, tree2):
        """
        Da de alta un cliente nuevo en la tabla *clientes* a partir 
        del ingreso obligatorio de los valores *mesa* y *comensales* de los
        respectivos Entry's de la ventana principal.
        
        :param nro_mesa: (_int_) número entero que se ingresa en el Entry *Mesa* de la vista principal.
        :param cant_comensales: (_int_): número entero que se ingresa en el Entry *Comensales* de la vista principal.
        :param tree: (_Tree_) objeto Tree de Tkinter - tree *listado* de *VentanaPrincipal()* del módulo *vista.py*.
        :param root: (_root_) objeto root Tkinter de VistaPrincipal().
        """
        
        id_cliente= self.crea_bases.get_id()
        listado= tree
        listado_consumos=tree2
        principal= root
        
        try:
            mesa= nro_mesa.get()
            comensales= cant_comensales.get()
            
        except TclError as t:
            showerror(message="Ingrese valores numéricos en los campos correspondientes" )
            motivo=sys.exc_info()
            registrar= AplicaRegistro(motivo, __name__,t)
            self.crea_bases.borra_ultimo_id()
            
        else:   
            t=str(mesa)
            if self.validacion.valida_mesa(t) == True: ###REGEX LIMITE NUMERICO
                self.crea_bases.crea_tabla_clientes()
                total=0
                estado= "ABIERTO"
                hora_ingreso= datetime.datetime.now().strftime("%H:%M:%S--%d/%m/%y")
                hora_egreso= ""
                cliente_nuevo=(id_cliente, mesa, comensales, estado, total, hora_ingreso, hora_egreso)
                
                self.base_clientes.alta_sql(cliente_nuevo)
                
                self.set_tree.actualiza_tree_clientes( id_cliente, listado)
                self.set_tree.limpiar_tree(listado_consumos)
                self.set_interfaz.setear_entrys_consulta(principal, id_cliente)
                self.set_interfaz.limpiar_entrys_raiz(principal)
                
                
                #print("CLIENTE AGREGADO =================> ID  ", id_cliente)

            else:
                self.crea_bases.borra_ultimo_id()
            
    
    def cierra_mesa(self, tree, root): 
        """
        Modifica el atributo *estado* del cliente seleccionado en la tabla *clientes*.
        
        :param tree: (_Tree_) objeto Tree de Tkinter - tree *listado* de *VentanaPrincipal()* del módulo *vista.py*.
        :param root: (_root_) objeto root Tkinter de VistaPrincipal().
        
        .. note::
            Una vez cerrada la mesa ya no se podrá borrar de la base de datos ni modificar ningún valor.
        """
        listado= tree
        principal= root
        
        puntero= listado.focus()
        w= listado.item(puntero) 
        try:
            id_cierra= int(w["text"])
            
        except ValueError as t:
            showerror(message="Seleccione el cliente a cerrar" )
            motivo=sys.exc_info()
            registrar= AplicaRegistro(motivo, __name__,t)
        
        else:
            if self.base_clientes.estado_mesa_sql(id_cierra) == True:
                self.set_tree.borra_puntero(listado, puntero)
                self.base_clientes.cierra_sql(id_cierra)
                
                self.set_tree.actualiza_tree_clientes(id_cierra, listado)
                self.set_interfaz.setear_entrys_consulta(principal, id_cierra)
                self.set_interfaz.limpiar_entrys_raiz(principal)
                
                #print("___ SE CERRÓ LA MESA DEL CLIENTE  ",id_cierra, "___")
    
    def borra_cliente(self, tree, tree_consumos, root2): 
        """
        Borra al cliente seleccionado y sus consumos de las tablas *clientes* y *consumos*.
        
        :param tree: (_Tree_) objeto Tree de Tkinter _ tree *listado* de *VentanaPrincipal()* del módulo *vista.py*.
        :param tree_consumos: (_Tree_) objeto Tree de Tkinter _ tree *listado_consumos* de *VentanaPrincipal()* del módulo *vista.py*.
        """
        ventana= root2
        listado= tree
        listado_consumos= tree_consumos
        puntero= listado.focus()
        w= listado.item(puntero)
        
        id_borra= w["text"]
        
        try:
            id_borra= int(w["text"])
        except ValueError as t:
            showerror(message="Seleccione el cliente que desea borrar")
            motivo=sys.exc_info()
            registrar= AplicaRegistro(motivo, __name__,t)
        else:
            if self.base_clientes.estado_mesa_sql(id_borra) == True:
                self.base_clientes.borra_cliente_sql(id_borra)
                self.set_tree.borra_puntero(listado, puntero)
                self.set_tree.limpiar_tree(listado_consumos) 
                self.set_interfaz.limpiar_entrys_consulta(ventana)
                    
                #print("_______________ SE BORRÓ EL CLIENTE ", id_borra, "_________________")
    
    def consulta_cliente(self, tree, tree_consumos, root): 
        """
        Muestra los datos del cliente seleccionado en la ventana secundaria *Consultas*.
        
        :param tree: (_Tree_) objeto Tree de Tkinter _ tree *listado* de *VentanaPrincipal()* del módulo *vista.py*.
        :param tree_consumos: (_Tree_) objeto Tree de Tkinter _ tree *listado_consumos* de *VentanaPrincipal()* del módulo *vista.py*.
        :param root: (_root_) objeto root Tkinter de VistaPrincipal().
        """
        listado_consumos= tree_consumos                   
        listado= tree
        principal= root
        
        puntero= listado.focus() 
        listado.item(puntero)
        w= listado.item(puntero)
        
        try:
            id_cliente=int(w["text"])
            
        except ValueError as t:
            showerror(message="Seleccione el cliente que desea consular")
            motivo=sys.exc_info()
            registrar= AplicaRegistro(motivo, __name__,t)
        else:
            principal.var_total_pagar.set("")
            self.set_interfaz.setear_entrys_consulta(principal, id_cliente)
            self.set_tree.limpiar_tree(listado_consumos)
            self.set_tree.actualiza_tree_consumos(listado_consumos, id_cliente)
    
    
    def agrega_comensal(self,tree, root, tree2):
        """
        
        Modifica el atributo *cantidad de comensales* del cliente seleccionado en la tabla
        *clientes* y lo muestra en los entrys y trees de la interfaz gráfica.
        
        :param tree: (_Tree_) objeto Tree de Tkinter _ tree *listado* de *VentanaPrincipal()* del módulo *vista.py*.
        :param tree2: (_Tree_) objeto Tree de Tkinter _ tree *listado_consumos* de *VentanaPrincipal()* del módulo *vista.py*.
        :param root: (_root_) objeto root Tkinter de VistaPrincipal().
        """
        listado= tree
        principal= root
        listado_consumos=tree2
        
        puntero= listado.focus()
        w= listado.item(puntero)    
        operacion= "suma"
        
        try:
            id_cliente=int(w["text"])
        except ValueError as t:
            showerror(message="Seleccione el cliente que desea modificar")
            motivo=sys.exc_info()
            registrar= AplicaRegistro(motivo, __name__,t)
        else:
            if self.base_clientes.estado_mesa_sql(id_cliente) == True:
                self.set_tree.borra_puntero(listado, puntero)
                self.base_clientes.modifica_comensal_sql(id_cliente,operacion)
                
                self.set_tree.limpiar_tree(listado_consumos)
                self.set_tree.actualiza_tree_consumos(listado_consumos, id_cliente)
                
                self.set_tree.actualiza_tree_clientes(id_cliente, listado)
                self.set_interfaz.setear_entrys_consulta(principal, id_cliente)
    
    
    def quita_comensal(self,tree, root, tree2): 
        """
        Modifica el atributo *cantidad de comensales* del cliente seleccionado en la tabla *clientes*.
        
        :param tree: (_Tree_) objeto Tree de Tkinter _ tree *listado* de *VentanaPrincipal()* del módulo *vista.py*.
        :param tree2: (_Tree_) objeto Tree de Tkinter _ tree *listado_consumos* de *VentanaPrincipal()* del módulo *vista.py*.
        :param root: (_root_) objeto root Tkinter de VistaPrincipal()
        """
        
        listado= tree
        principal= root
        listado_consumos=tree2
        
        puntero= listado.focus()
        w= listado.item(puntero)    
        operacion= "resta"
        
        try:
            id_cliente=int(w["text"])
        except ValueError as t:
            showerror(message="Seleccione el cliente que desea modificar")
            motivo=sys.exc_info()
            registrar= AplicaRegistro(motivo, __name__,t)
        else:
            if self.base_clientes.estado_mesa_sql(id_cliente) == True:
                self.set_tree.borra_puntero(listado, puntero)
                self.base_clientes.modifica_comensal_sql(id_cliente,operacion)
                
                self.set_tree.limpiar_tree(listado_consumos)
                self.set_tree.actualiza_tree_consumos(listado_consumos, id_cliente)
                
                self.set_tree.actualiza_tree_clientes(id_cliente, listado)
                self.set_interfaz.setear_entrys_consulta(principal, id_cliente)
    
    
    def cambia_mesa(self, consul_mesa, tree, root, tree2): 
        """
        Modifica el atributo *cantidad de comensales* del cliente seleccionado en la tabla
        *clientes*.
        
        :param consul_mesa: (_IntVar_) variable int de Tkinter ingresada en el Entry *Comensales* de la ventana secundaria.
        :param tree: (_Tree_) objeto Tree de Tkinter _ tree *listado* de *VentanaPrincipal()* del módulo *vista.py*.
        :param tree2: (_Tree_) objeto Tree de Tkinter _ tree *listado_consumos* de *VentanaPrincipal()* del módulo *vista.py*.
        :param root: (_root_) objeto root Tkinter de VistaPrincipal().
        """
        
        listado= tree
        listado_consumos=tree2
        principal= root
        
        try:
            nueva_mesa= int(consul_mesa.get()) #TclError
            puntero= listado.focus()
            w= listado.item(puntero)    
            id_cliente=int(w["text"])   #ValueError
            
        except ValueError as t:
            motivo=sys.exc_info()
            showerror(message="Seleccione el cliente de la mesa que desea modificar" )
            registrar= AplicaRegistro(motivo, __name__,t)
                
            
        except TclError as t:
            showerror(message="Ingrese valores numéricos en los campos correspondientes" )
            motivo=sys.exc_info()
            registrar= AplicaRegistro(motivo, __name__,t)
        
        else:  
            if self.base_clientes.estado_mesa_sql(id_cliente) == True:
                self.base_clientes.modifica_mesa_sql(nueva_mesa, id_cliente)
                self.set_tree.borra_puntero(listado, puntero)
                self.set_tree.limpiar_tree(listado_consumos)
                self.set_tree.actualiza_tree_consumos(listado_consumos, id_cliente)
                self.set_tree.actualiza_tree_clientes(id_cliente, listado)
                self.set_interfaz.setear_entrys_consulta(principal, id_cliente)
        
class ConsumosBD(Sujeto):
    
    """
    La Clase *ConsumossBD()* cuenta con los métodos que vinculan la interfaz gráfica 
    con la tabla *consumos* de la base de datos *clientes_sql.db* a partir del ingreso obligatorio de 
    los valores *producto* y *precio* de los respectivos Entry's de la ventana principal
    
    """
    
    def __init__(self):
        self.base_consumos=BaseConsumos()
        self.base_clientes=BaseClientes()
        self.crea_bases=BaseDeDatos()
        self.set_interfaz=vista.SetInterfaz()
        self.set_tree=vista.SetTree()
        self.validacion=regex.Validar()
        
        
        
        
    
    def agrega_pedido(self,tree, tree_consumos, root): 
        """
        Agrega un pedido a la tabla *consumos* a partir de los datos ingresados en los Entry's
        *producto* y *precio* de la ventana secundaria "Consultas".

        :param tree: (_Tree_) objeto Tree de Tkinter _ tree *listado* de *VentanaPrincipal()* del módulo *vista.py*.
        :param tree_consumos: (_Tree_) objeto Tree de Tkinter _ tree *listado_consumos* de *VentanaPrincipal()* del módulo *vista.py*.
        :param root: (_root_) objeto root Tkinter de VistaPrincipal().
        """
        listado= tree
        listado_consumos= tree_consumos
        principal= root
        self.set_tree.limpiar_tree(listado_consumos)
        
        puntero= listado.focus()
        listado.item(puntero)
        w= listado.item(puntero)
        #print("W ==>", w)
        principal.var_total_pagar.set("")
        
        self.crea_bases.crea_tabla_consumos()
        
        try:
            id_cliente= int(w["text"])
        except ValueError as t: 
            showerror(message="Seleccione un cliente para agregar pedido")
            motivo=sys.exc_info()
            registrar= AplicaRegistro(motivo, __name__,t)
        else:
            try:
                producto= principal.var_producto.get()
                precio= principal.var_precio.get()
            except TclError as t:
                showerror(message="Ingrese valores es los campos correspondientes" )
                motivo=sys.exc_info()
                registrar= AplicaRegistro(motivo, __name__,t)
            else:
                if self.validacion.valida_producto(producto)== True:##REGEX PRODUCTO
                    if self.base_clientes.estado_mesa_sql(id_cliente) == True: 
                        self.base_consumos.alta_compra_sql(id_cliente, producto, precio, principal)
                        self.set_tree.actualiza_tree_consumos(listado_consumos, id_cliente)
                        self.set_interfaz.setear_entrys_consulta(principal, id_cliente)
                        self.set_interfaz.limpiar_compra(principal)
                        
                        ########### METODO PARA INFORMAR A OBSERVADOR ############
                        self.notificar(producto, w['values'][0])
                        ##########################################################
                        
                        
                        ###### METODO PARA INFORMAR A CLIENTE POR SOCKET #########
                        
                        #self.servidor=nuevo_servidor
                        #self.servidor.inicializar_servidor()
                        
                        self.servidor=Servidor.get_instancia()
                        threading.Thread(target=self.servidor.envio_a_cliente, args=(producto, w['values'][0]), daemon=True).start()
                        #self.servidor.envio_a_cliente(producto, w['values'][0])
                        #Servidor._instancia.envio_a_cliente(producto, w['values'][0])
                        #print("INSTANCIA DE SERVIDOR EN MODELO ========== ", Servidor._instancia)
                        #Servidor._instancia.envio_a_cliente(producto, w['values'][0])
                        
                        
                        

                        #############################################################"""
    
    
    def quita_pedido(self, tree_consumos, root): 
        """
        Borra el pedido seleccionado del tree *listado_consumos* de la tabla *consumos*.

        :param tree_consumos: (_Tree_) objeto Tree de Tkinter _ tree *listado_consumos* de *VentanaPrincipal()* del módulo *vista.py*.
        :param root: (_root_) objeto root Tkinter de VistaPrincipal().
        """
        listado_consumos= tree_consumos
        principal= root
        
        puntero= listado_consumos.focus()
        w= listado_consumos.item(puntero)
        try:
            id_cliente= int(w["text"]) 
            
        except ValueError as t:
            showerror(message="Seleccione el pedido que desea eliminar")
            motivo=sys.exc_info()
            registrar= AplicaRegistro(motivo, __name__,t)
        else:
            if self.base_clientes.estado_mesa_sql(id_cliente) == True:
                producto=w["values"][0]
                precio=w["values"][1]
                self.base_consumos.baja_compra_sql(id_cliente, producto, precio, principal)
                
                self.set_tree.borra_puntero(listado_consumos, puntero)
                self.set_interfaz.limpiar_compra(principal)
                self.set_interfaz.setear_entrys_consulta(principal, id_cliente)

class MuestraClientesBD():
    
    """
    La clase *MuestraClientes()* presenta en el tree *listado* los clientes que se encuentran registrados en 
    la tabla *clienstes*.
    """
    
    def __init__(self):
        self.set_interfaz=vista.SetInterfaz()
        self.set_tree=vista.SetTree()
        self.base_clientes=BaseClientes()
        self.crea_bases=BaseDeDatos()
    
    def muestra_clientes_activos(self, root, tree, tree2): 
        """
        Muestra en el Tree de la página principal todos los clientes de la tabla *clientes* cuyo atributo *estado* sea "ABIERTO".
        
        :param tree: (_Tree_) objeto Tree de Tkinter _ tree *listado* de *VentanaPrincipal()* del módulo *vista.py*.
        :param tree2: (_Tree_) objeto Tree de Tkinter _ tree *listado_consumos* de *VentanaPrincipal()* del módulo *vista.py*.
        :param root: (_root_) objeto root Tkinter de VistaPrincipal().
        """
        
        listado= tree
        listado_consumos=tree2
        principal=root
        
        self.set_tree.limpiar_tree(tree1=listado)
        self.set_tree.limpiar_tree(tree1=listado_consumos)
        self.set_interfaz.limpiar_entrys_consulta(principal)
        self.crea_bases.crea_tabla_clientes()
        estado= "ABIERTO"
        clientes= self.base_clientes.muestra_clientes_sql(estado)
        
        for cliente in clientes:
            id_cliente=cliente[0]
            self.set_tree.actualiza_tree_clientes( id_cliente, listado)
    
    def muestra_clientes_total(self, root,tree, tree2): 
        """
        Muestra todos clientes de la tabla *clientes* en el Tree de la página principal.
        
        :param tree: (_Tree_) objeto Tree de Tkinter _ tree *listado* de *VentanaPrincipal()* del módulo *vista.py*.
        :param tree2: (_Tree_) objeto Tree de Tkinter _ tree *listado_consumos* de *VentanaPrincipal()* del módulo *vista.py*.
        :param root: (_root_) objeto root Tkinter de VistaPrincipal().
        """
        listado= tree
        listado_consumos=tree2
        principal=root
        
        self.set_tree.limpiar_tree(listado)
        self.set_tree.limpiar_tree(tree1=listado_consumos)
        self.set_interfaz.limpiar_entrys_consulta(principal)
        self.crea_bases.crea_tabla_clientes()
        
        estado= "TOTAL"
        clientes= self.base_clientes.muestra_clientes_sql(estado)
        
        for cliente in clientes:
            id_cliente=cliente[0]
            self.set_tree.actualiza_tree_clientes( id_cliente, listado)
    
class ProgramaAdmin():
    """
    Clase en construcción.
    """
    
    def __init__(self)-> None:
        
        pass
    
    def salir_programa(self,root):
        """
        Salir del programa.

        :param root: (_root_) objeto root Tkinter de VistaPrincipal().
        """
        principal= root
        if askyesno("Usted está saliendo del programa","¿Desea salir?"):
            showinfo("Si", "¡Hasta la próxima!")
            principal.quit()
        else:
            showinfo("No", "Haga click para volver a la página principal")

    def guardar(self): 
        """
        Prueba de boton "Guardar"
        """
        ruta_guardar= askopenfilename()
    
    
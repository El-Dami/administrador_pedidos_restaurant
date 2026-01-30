"""
vista.py

        Ejecuta y administra la interfaz gráfica de la aplicación.
        
        
    """

from tkinter import IntVar
from tkinter import DoubleVar
from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Menu
from tkinter import Frame
from tkinter import ttk

from control_socket.conexion import ConexionAServidor
import modelo

from pathlib import Path
import subprocess
import threading
import os
import sys


class VistaPrincipal():
    """
    La clase *VistaPrincipal()* ejecuta y administra la interfaz gráfica, 
    los Botones, Entradas, Etiquetas y Cuadros (Trees) de la aplicación.
    
    """
    
    
    def __init__(self, root, conexion):
        self.theproc=""
        self.principal= root
        self.principal.title("Gestión de mesas")
        self.principal.geometry("1300x450")

        self.color_a= '#A7C4B6'
        self.principal.configure(background=self.color_a)
        self.color_b='#98A389'
        self.color_c='#B9C4A7'
        
        self.base_clientes= modelo.ClientesBD()
        self.base_consumos= modelo.ConsumosBD()
        self.base_mostrar= modelo.MuestraClientesBD()
        self.admin_programa= modelo.ProgramaAdmin()
        
        
        
        self.conexion_servidor=conexion
        
        
        
        
        self.ventana = Frame(self.principal, bg=self.color_c, height=122,borderwidth=2)
        self.ventana.grid(row=0, column=6, columnspan=6, rowspan=9, padx=1, pady=1)
        
        
        self.mesa_nro= IntVar()
        self.comensales_nro= IntVar()
        self.var_producto= StringVar()
        self.var_precio= DoubleVar()
        self.var_consul_mesa=IntVar()
        self.var_consul_comens= IntVar()
        self.var_total_pagar= DoubleVar()
        self.var_hora_ingreso= StringVar()
        self.var_hora_egreso= StringVar()


        self.mesa_nro.set("")
        self.comensales_nro.set("")
        self.var_producto.set("")
        self.var_precio.set("")
        self.var_consul_comens.set("")
        self.var_consul_mesa.set("")
        self.var_total_pagar.set("")
        
        
        self.alta_label=Label(self.principal, text= "ALTA MESA", bg='#A3A389',fg='black', height=1,width=60)
        self.alta_label.grid(row=0, column=0, columnspan=6, padx=1, pady=1, sticky="w"+"e")


        self.mesa_ing= Label(self.principal, text= "Mesa Nº", fg= 'black')
        self.mesa_ing.grid(row=1, column=2, sticky="w")
        self.mesa_ing.configure(background=self.color_a)
        self.ingresa_mesa= Entry(self.principal, fg= 'black')
        self.ingresa_mesa.grid(row=1, column=3)
        self.ingresa_mesa.config(textvariable= self.mesa_nro)
        self.ingresa_mesa.configure(background= self.color_b)


        self.comensales= Label(self.principal, text= "Nºcomensales", fg= 'black')
        self.comensales.grid(row=2, column=2, sticky="w")
        self.comensales.configure(background=self.color_a)
        self.ingresa_comensales= Entry(self.principal, fg= 'black')
        self.ingresa_comensales.grid(row=2, column=3)
        self.ingresa_comensales.config(textvariable=self.comensales_nro)
        self.ingresa_comensales.configure(background= self.color_b)


        self.muestra_consulta=Label(self.ventana, text= "CONSULTA", fg= 'black', bg='#A3A389', height=1,width=60)
        self.muestra_consulta.grid(row=0, column=6, columnspan=6, padx=1, pady=1, sticky="w"+"e")


        self.producto= Label(self.ventana, text="Ingrese producto",fg= 'black')
        self.producto.grid(row=1, column=6, sticky="w")
        self.producto.configure(background=self.color_c)
        self.ingresa_producto= Entry(self.ventana, fg= 'black')
        self.ingresa_producto.grid(row=1, column=7)
        self.ingresa_producto.config(textvariable=self.var_producto)
        self.ingresa_producto.configure(background= self.color_b)


        self.precio= Label(self.ventana, text="Ingrese precio", fg= 'black')
        self.precio.grid(row=2, column=6, sticky="w")
        self.precio.configure(background=self.color_c)
        self.ingresa_precio= Entry(self.ventana, fg= 'black')
        self.ingresa_precio.grid(row=2, column=7)
        self.ingresa_precio.config(textvariable=self.var_precio)
        self.ingresa_precio.configure(background= self.color_b)

        
        
        
        
        

        self.consul_mesa=Label(self.ventana, text= "Mesa",fg= 'black')
        self.consul_mesa.grid(row=1, column=8, sticky="w", padx=5, pady=5)
        self.consul_mesa.configure(background=self.color_c)
        self.consul_mesa_entry= Entry(self.ventana, fg= 'black')
        self.consul_mesa_entry.grid(row=1, column=9, padx=1, pady=20)
        self.consul_mesa_entry.config(textvariable=self.var_consul_mesa)
        self.consul_mesa_entry.configure(background= self.color_b)


        self.consul_comens=Label(self.ventana, text= "Comensales",fg= 'black')
        self.consul_comens.grid(row=2, column=8, sticky="w")
        self.consul_comens.configure(background=self.color_c)
        self.consul_comens_entry= Entry(self.ventana, fg= 'black')
        self.consul_comens_entry.grid(row=2, column=9)
        self.consul_comens_entry.config(textvariable=self.var_consul_comens)
        self.consul_comens_entry.configure(background=self.color_b)


        self.total_pagar=Label(self.ventana, text= "Total a Abonar",fg= 'black')
        self.total_pagar.grid(row=9, column=6, sticky="w")
        self.total_pagar.configure(background=self.color_c)
        self.total_pagar_entry= Entry(self.ventana,fg= 'black')
        self.total_pagar_entry.grid(row=9, column=7)
        self.total_pagar_entry.config(textvariable=self.var_total_pagar)
        self.total_pagar_entry.configure(background= self.color_b)

        self.hora_ingreso=Label(self.ventana, text= "Hora de Ingreso",fg= 'black')
        self.hora_ingreso.grid(row=9, column=8, sticky="w")
        self.hora_ingreso.configure(background=self.color_c)
        self.hora_ingreso_entry= Entry(self.ventana,fg= 'black')
        self.hora_ingreso_entry.grid(row=9, column=9)
        self.hora_ingreso_entry.config(textvariable=self.var_hora_ingreso)
        self.hora_ingreso_entry.configure(background= self.color_b)

        self.hora_egreso=Label(self.ventana, text= "Hora de Egreso",fg= 'black')
        self.hora_egreso.grid(row=10, column=8, sticky="w")
        self.hora_egreso.configure(background=self.color_c)
        self.hora_egreso_entry= Entry(self.ventana,fg= 'black')
        self.hora_egreso_entry.grid(row=10, column=9)
        self.hora_egreso_entry.config(textvariable=self.var_hora_egreso)
        self.hora_egreso_entry.configure(background= self.color_b)



        ###############################################################
        ##                       TREEVIEWS                           ##
        ###############################################################


        self.listado = ttk.Treeview(self.principal)
        #self.colores_filas = ("gray",  "white")
        self.listado.tag_configure(self.color_b, background=self.color_b)
        self.listado["columns"]=("col1", "col2", "col3")
        self.listado.column("#0", width=90, minwidth=50, anchor="w")
        self.listado.column("col1", width=90, minwidth=90)
        self.listado.column("col2", width=90, minwidth=90)
        self.listado.column("col3", width=120, minwidth=120)
        self.listado.heading("#0", text="Cliente")
        self.listado.heading("col1", text="Mesa Nº")
        self.listado.heading("col2", text="Comensales")
        self.listado.heading("col3", text="Estado")
        self.listado.grid(row=5, column=1, columnspan=4)


        self.listado_consumos=ttk.Treeview(self.ventana)
        self.listado_consumos["columns"]=("col1", "col2")
        self.listado_consumos.column("#0", width=20, minwidth=20)
        self.listado_consumos.column("col1",width=120, minwidth=120)
        self.listado_consumos.column("col2",width=120, minwidth=120)
        self.listado_consumos.heading("col1", text="producto")
        self.listado_consumos.heading("col2", text="precio")
        self.listado_consumos.grid(row=6, column=6, columnspan=3)





        ##########################################################
        ##                     BOTONES                          ##
        ##########################################################


        self.alta_mesa= Button(self.principal, text="Alta mesa", command= lambda: self.base_clientes.alta_cliente(self.mesa_nro,\
        self.comensales_nro, self.listado, self, self.listado_consumos))
        self.alta_mesa.grid(row=4, column=1)
        self.alta_mesa.configure(background=self.color_a)

        self.baja_mesa= Button(self.principal, text="Baja mesa", command= lambda: self.base_clientes.cierra_mesa(self.listado, self))
        self.baja_mesa.grid(row=4, column=3)
        

        self.agrega_producto= Button(self.ventana, text="Agregar Producto", command= lambda: self.base_consumos.agrega_pedido(self.listado, \
        self.listado_consumos, self))
        self.agrega_producto.grid(row=4, column=6)

        self.quitar_producto= Button(self.ventana, text="Quitar Producto", command= lambda: self.base_consumos.quita_pedido(self.listado_consumos,self))
        self.quitar_producto.grid(row=4, column=7)
        
        
        self.consulta= Button(self.principal, text="Consulta", command= lambda: self.base_clientes.consulta_cliente(self.listado, \
        self.listado_consumos, self))
        self.consulta.grid(row=6, column=3)
        
        self.borrar= Button(self.principal, text="Borrar", command= lambda: self.base_clientes.borra_cliente(self.listado, self.listado_consumos, self))
        self.borrar.grid(row=6, column=2)
        
        self.clientes_activos= Button(self.principal, text="Cl.Activos",\
        command= lambda: self.base_mostrar.muestra_clientes_activos(self, self.listado, tree2=self.listado_consumos))
        self.clientes_activos.grid(row=8, column=2)
        
        self.clientes_total= Button(self.principal, text="Cl.Total",\
        command= lambda: self.base_mostrar.muestra_clientes_total(self,self.listado, tree2= self.listado_consumos))
        self.clientes_total.grid(row=8, column=3)
        
        #self.guarda= Button(self.principal, text="Conectar", command= lambda: self.conexion_servidor.try_connection)
        self.guarda = Button(self.principal, text="Conectar", command=lambda: self.conexion_servidor.try_connection())
        #self.try_connection(self,))
        self.guarda.grid(row=9, column= 2)
        
        self.mas_comensales= Button(self.ventana,text="+",command= lambda: self.base_clientes.agrega_comensal(self.listado,\
        self, self.listado_consumos ))
        self.mas_comensales.grid(row=2, column=10)
        
        self.menos_comensales= Button(self.ventana,text="-",command= lambda: self.base_clientes.quita_comensal(self.listado,\
        self, self.listado_consumos))
        self.menos_comensales.grid(row=2, column=11)
        
        self.modif_mesa= Button(self.ventana,text="Modificar",command= lambda: self.base_clientes.cambia_mesa(self.var_consul_mesa,\
        self.listado, self, self.listado_consumos))
        self.modif_mesa.grid(row=1, column=10, columnspan= 2)


        self.salir= Button(self.principal, text="Salir", command= lambda: self.admin_programa.salir_programa(self.principal))
        self.salir.grid(row=9, column= 3)


        #########################################################
        ##                      MENU BAR                       ## 
        #########################################################

        self.menubar= Menu(self.principal)

        self.menu_archivo= Menu(self.menubar, tearoff=0)
        self.menu_archivo.add_command(label= "Abrir",command=lambda:self.base_consumos.agrega_pedido(self.listado, \
        self.listado_consumos, self))
        self.menu_archivo.add_command(label="Guardar", command= lambda: self.admin_programa.salir_programa(self.principal))
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command= lambda: self.admin_programa.salir_programa(self.principal))
        self.menubar.add_cascade(label="Archivo", menu= self.menu_archivo)
        
        self.menu_edicion= Menu(self.menubar, tearoff=0)
        self.menu_edicion.add_command(label= "Agregar",command=lambda: self.base_consumos.agrega_pedido(self.listado, \
        self.listado_consumos, self))
        self.menu_edicion.add_command(label="Quitar", command= lambda: self.base_consumos.quita_pedido(self.listado_consumos,self))
        self.menubar.add_cascade(label="Edición", menu= self.menu_edicion)
        
        self.principal.config(menu=self.menubar)
        
        

        
                ######### SE HABILITA UN SUBPROCESO QUE LANZA EL SERVIDOR ##############
        #self.objeto_servidor=control_socket.conexion.ConexionAServidor()


class SetInterfaz():
    
    """
    La clase *SetInterfaz()* permite modificar los datos 
    que se muestran en los Entry's de la interfaz gráfica.
    
    """
    
    
    def __init__(self):
        self.base_clientes= modelo.BaseClientes()
    
    
    def limpiar_entrys_raiz(self, root):
        """
        Limpia los Entry's de la ventana principal.
        
        :param root: (_root_) objeto root Tkinter de VistaPrincipal().
            
        """
        principal= root
        principal.mesa_nro.set("")
        principal.comensales_nro.set("")
    
    
    def setear_entrys_consulta(self, root, cliente):
        """
        Muestra los datos del cliente seleccionado en los Entry's de la ventana secundaria "CONSULTAS".

        :param root: (_root_) objeto Frame Tkinter de VistaPrincipal().
        :param cliente: (_int_) número del cliente de quien se van a mostrar datos.
            
        """
        principal= root
        id_ingreso= int(cliente)
        
        cliente_actualiza= self.base_clientes.selecc_para_entrys_sql(id_ingreso)
        for cliente in cliente_actualiza:
            mesa=cliente[0]
            comensales=cliente[1]
            total=cliente[2]
            hora_ingreso=cliente[3]
            hora_egreso=cliente[4]
            
            principal.var_consul_mesa.set(mesa)
            principal.var_consul_comens.set(comensales)
            principal.var_hora_ingreso.set(hora_ingreso)
            principal.var_hora_egreso.set(hora_egreso)
            principal.var_total_pagar.set(total)
    
    
    def limpiar_entrys_consulta(self, root):
        """
        Limpia los Entry's de la ventana secundaria.

        :param root: (_root_) objeto Frame Tkinter de VistaPrincipal().
        
        """
        principal= root
        principal.var_consul_mesa.set("")
        principal.var_consul_comens.set("")
        principal.var_hora_ingreso.set("")
        principal.var_hora_egreso.set("")
        principal.var_total_pagar.set("")
    
    
    def limpiar_compra(self, root):
        """
        Limpia los Entry's *Producto* y *Precio* de la ventana secundaria.
        
        :param root: (_root_) objeto Frame Tkinter de VistaPrincipal().
        
        """
        principal= root
        principal.var_producto.set(value="")
        principal.var_precio.set("")


class SetTree():
    """
    La clase *SetTree()* permite modificar los datos 
    que se muestran en los Trees's de la interfaz gráfica.
    
    """
    
    
    def __init__(self):
        self.base_clientes= modelo.BaseClientes()
        
        
    def limpiar_tree(self, tree1):
        """
        Borra toda la información del Tree seleccionado.
        
        :param tree1: (_Tree_) objeto Tree de Tkinter.
            
        """
        tree= tree1
        tree.delete(*tree.get_children()) 
    
    
    def actualiza_tree_clientes(self, cliente, tree): 
        """
        Muestra información del/los cliente/s seleccionado/s en el Tree Clientes.
        
        :param cliente: (_int_) id del cliente.
        :param tree: (_Tree_) objeto Tree de Tkinter.
            
        """
        
        id_cliente=int(cliente)
        listado_clientes=tree
        
        cliente_seleccionado=self.base_clientes.selecc_tree_clientes_sql(id_cliente)
        
        for cliente in cliente_seleccionado:
            mesa=cliente[0]
            comensales=cliente[1]
            estado=cliente[2]
            listado_clientes.insert(parent="", index="end", text=id_cliente,\
            values=(mesa, comensales,estado))
    
    
    def actualiza_tree_consumos(self,tree, id_cl):
        """
        Muestra información del/los cliente/s seleccionado/s
        en el Tree Consumos.
        
        :param tree: (_Tree_) objeto Tree de Tkinter.
        :para id_cl: (_int_) id del cliente.
            
        """
        
        listado_consumos= tree
        id_cliente=id_cl
        
        cliente_seleccionado=self.base_clientes.selecc_tree_consumos_sql(id_cliente)
        
        for cliente in cliente_seleccionado:
            producto=cliente[0]
            precio=cliente[1]
            
            listado_consumos.insert(parent="", index="end", text=id_cliente,\
            values=(producto, precio))


    def borra_puntero(self, tree, puntero):
        """
        Borra el objeto *puntero* de un Tree de Tkinter.
        
        :param tree: (_Tree_) objeto Tree de Tkinter.
        :param puntero: (_puntero_) puntero de Tree de Tkinter.
            
        """
        
        tree.delete(puntero)


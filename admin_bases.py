"""
    admin_bases.py
        
        Contiene todas las clases y métodos que crean y administran las bases de datos.

    """

from tkinter.messagebox import showerror
import sqlite3
import datetime
import decoradores



class Conexion():
    """
    La clase *Conexion()* crea y se conecta con la base de datos "clientes_sql.db".
    Todas las clases del módulo 'admin_bases.py' heredan de la clase *Conexion()*
    
    """
    
    def __init__(self)->None:
        pass
    
    def conexion_bd(self):
        """
        Genera la conexión sqlite3.
        
        :returns: objeto *connect()* de sqlite3.
        """
        con= sqlite3.connect("clientes_sql.db")
        return con    

class BaseDeDatos(Conexion):
    """
    La clase *BaseDeDatos()* crea las tablas sqlite3 con las que trabajará la aplicación.

    """
    
    def __init__(self)->None:
    
        pass
    
    def crea_tabla_id(self):
        """
        Crea la tabla "id_base" que proporcionará los números de ID para la tabla "clientes".
        
        """
        con = self.conexion_bd()
        cursor = con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS id_base
                (id INT NOT NULL)"""
        cursor.execute(sql)
        con.commit()
    
    def get_id(self):
        """
        Proporciona un número de ID autoincrementable, lo almacena en la tabla "id_base" y lo retorna para ser utilizado 
        como *PRIMARY KEY* en la tabla "clientes".

        :returns id: (_int_) integer para ID de la tabla "clientes".
            
        """
        con = self.conexion_bd()
        
        cursor = con.cursor()
        self.crea_tabla_id()
        sql= "SELECT MAX (id) FROM id_base;"
        cursor.execute(sql)
        mi_id= cursor.fetchall()
        con.commit()
        
        for tt in mi_id:
            if tt==(None,):
                uno=(1,)
                print("nueva base id_clientes")
                sql_id= "INSERT INTO ID_Base(id) VALUES( ?)"
                cursor.execute(sql_id, uno)
                con.commit()
                return 1
            else:    
                ultimo_id= tt[0]
                ultimo_id+=1
                data=(ultimo_id,)
                sql2= "INSERT INTO ID_Base(id) VALUES(?)"
                cursor.execute(sql2, data)
                con.commit()
                return ultimo_id
    
    def borra_ultimo_id(self):
        """
        Borra el último ingreso de la tabla "id_base".
        """
        con = self.conexion_bd()
        
        cursor = con.cursor()
        self.crea_tabla_id()
        sql= "SELECT MAX (id) FROM id_base;"
        cursor.execute(sql)
        mi_id= cursor.fetchall()
        con.commit()
        
        for tt in mi_id:
            ultimo_id= tt[0]
            data=(ultimo_id,)
            sql2= "DELETE from id_base WHERE id = ?;"
            cursor.execute(sql2, data)
            con.commit()
    
    def crea_tabla_clientes(self):
        """
        Crea la tabla "clientes".
        """
        con = self.conexion_bd()
        cursor = con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS clientes
                (id INTEGER PRIMARY KEY,
                n_mesa INT NOT NULL, 
                cant_comensales INTEGER NOT NULL, 
                estado TEXT,
                total REAL NULL, 
                hora_ingreso REAL, 
                hora_egreso REAL NULL
                )
        """
        cursor.execute(sql)
        con.commit()

    def crea_tabla_consumos(self,):
        """
        Crea la tabla "consumos".
        """
        
        con = self.conexion_bd()
        cursor = con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS consumos
                (compra int,
                producto TEXT,
                precio REAL, 
                cliente INT,
                FOREIGN KEY (cliente) REFERENCES clientes(id))
                
        """
        cursor.execute(sql)
        con.commit()

class BaseClientes(Conexion):
    """
    La clase *BaseClientes()* cuenta con los métodos que brindan con las directrices necesarias
    para administrar la información de la tabla "clientes".
    """
    
    def __init__(self)->None:
        pass
    
    @decoradores.registro_abm  ################### DECORADOR
    def alta_sql(self,cliente):
        """
        Agrega un nuevo cliente en la tabla "clientes".

        :param cliente: (_tuple_) datos proporcionados desde el módulo *modelo.py* para la alta del cliente.
        """
        
        data= cliente
        con= self.conexion_bd()
        cursor=con.cursor()
        sql="INSERT INTO clientes(id, n_mesa, cant_comensales, estado, total, hora_ingreso, hora_egreso) VALUES( ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        cliente=data[0]
        #print(cliente)
        return  cliente
    
    @decoradores.registro_abm   ################### DECORADOR
    def cierra_sql(self, id_cliente): 
        """
        Modifica el atributo *estado* del cliente seleccionado en la tabla "clientes" y agrega horario de cierre
        al atributo *hora_egreso* del cliente seleccionado.

        :param id_cliente: (_int_) id de cliente.
        """
        
        con=self.conexion_bd()
        cursor = con.cursor()
        mi_id = int(id_cliente)
        h_egreso=datetime.datetime.now().strftime("%H:%M:%S--%d/%m/%y")
        data = ("CERRADO", h_egreso, mi_id)
        sql = "UPDATE clientes SET estado=?, hora_egreso=? WHERE id=?;"
        cursor.execute(sql, data)
        con.commit()
        return mi_id
    
    def estado_mesa_sql(self, id_cliente):
        """
        Proporciona el atributo *estado* del cliente seleccionado.

        :param id_cliente: (_int_): id del cliente seleccionado

        :returns True: (_boolean_) si la mesa del cliente seleccionado está "ABIERTA"
        
        .. note::
            Si el estado de la mesa del cliente seleccionado es "CERRADA", el método retorna
            una ventana de error.
        """
        id_cliente=int(id_cliente)
        data=(id_cliente,)
        sql = "SELECT estado FROM clientes WHERE id =?;"
        
        con=self.conexion_bd()
        cursor = con.cursor()
        cursor.execute(sql, data)
        con.commit()
        estado= cursor.fetchall()
            
        for anterior in estado:
            estado_final=anterior[0]
            
            if estado_final=="ABIERTO":
                return True
            else:
                showerror(message="La mesa seleccionada está cerrada y no se puede modificar" )
    
    @decoradores.registro_abm  ################### DECORADOR
    def borra_cliente_sql(self, id_cliente):
        """
        Borra al cliente seleccionado de la tabla "clientes".

        :param id_cliente (_int_): id del cliente seleccionado.

        """
        mi_id = int(id_cliente)
        
        con=self.conexion_bd()
        cursor = con.cursor()
            
        data = (mi_id,)
        sql = "DELETE from clientes WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        self.borra_consumos_cliente_borrado_sql(mi_id)
        return mi_id
    
    def borra_consumos_cliente_borrado_sql(self, id_cliente):
        """
        Borra de la tabla "consumos" los datos correspondientes al cliente borrado con el método *borra_cliente_sql()*.

        :param id_cliente (_int_): id del cliente seleccionado.
        """
        con=self.conexion_bd()
        cursor = con.cursor()
            
        data = (id_cliente,)
        sql = "DELETE from consumos WHERE cliente = ?;"
        cursor.execute(sql, data)
        con.commit()
        
    @decoradores.registro_abm   ################### DECORADOR
    def modifica_mesa_sql(self, nueva_mesa, id_cliente):
        """
        Modifica el atributo *n_mesa* del cliente seleccionado en la tabla "clientes".

        :param nueva_mesa: (_int_): número de mesa proporcionado por el módulo *modelo.py*.
        :param id_cliente: (_int_): ID del cliente seleccionado.
        """
        
        con2=self.conexion_bd()
        cursor = con2.cursor()
        data2=(nueva_mesa, id_cliente)
        sql2 = "UPDATE Clientes SET n_mesa=? WHERE id=?;"
        cursor.execute(sql2, data2)
        con2.commit()
        return id_cliente
    
    @decoradores.registro_abm  ################### DECORADOR
    def modifica_comensal_sql(self, id_cliente, operacion):
        """
        Modifica el atributo *n_comensales* del cliente seleccionado en la tabla "clientes".
        
        :param id_cliente: (_int_) ID del cliente seleccionado
        :param operacion: (_str_) "suma" o "resta" según se vaya a agregar o quitar un comensal.
        """
        data=(id_cliente,)
        sql = "SELECT cant_comensales FROM clientes WHERE id =?;"
        con=self.conexion_bd()
        cursor = con.cursor()
        cursor.execute(sql, data)
        con.commit()
        comensales= cursor.fetchall()
            
        for comensal in comensales:
            total_comens=comensal[0]
            if operacion == "suma":
                total_comens+=1         
            elif operacion == "resta":
                total_comens-=1
                
            con2=self.conexion_bd()
            cursor = con2.cursor()
            data2=(total_comens,id_cliente)
            sql2 = "UPDATE clientes SET cant_comensales=? WHERE id=?;"
            cursor.execute(sql2, data2)
            con2.commit()
        return id_cliente

    def muestra_clientes_sql(self, estado1):
        """
        Obtiene de la tabla "clientes" un listado de clientes para ser mostrado en el Tree de la ventana principal. 
        
        :param estado1: (_str_): "ABIERTO" o "TOTAL" según se muestren los clientes activos o todos los clientes.
        
        :returns clientes_abiertos o clientes_total: (_list_) retorna el listado de clientes activos o la totalidad de los clientes dependiendo del parámetro brindado desde el módulo *modelo.py*.
        
        """
        con=self.conexion_bd()
        cursor = con.cursor()
        if estado1 == "ABIERTO":
        
            data = (estado1,)
            sql = "SELECT * FROM Clientes WHERE Estado =?;"
            cursor.execute(sql, data)
            clientes_abiertos = cursor.fetchall()
            #print("CLIENTES ABIERTOS === ", clientes_abiertos)
            return clientes_abiertos
            
        elif estado1 == "TOTAL":
            sql = "SELECT * FROM Clientes;"
            cursor.execute(sql)
            clientes_total = cursor.fetchall()
            #print("CLIENTES TOTALES === ", clientes_total)
            return clientes_total
    
    def selecc_para_entrys_sql(self, id_cliente):
        """
        Obtiene y retorna de la tabla "clientes" los datos de un cliente requeridos para 
        presentar en los Entrys de la ventana secundaria.
        
        :param id_cliente: (_int_) ID del cliente seleccionado.
        
        :returns clientes_actualiza: (_list_) Listado de atributos del cliente seleccionado para mostrar en los Entrys de la ventana secundaria.
        """
        con=self.conexion_bd()
        cursor = con.cursor()
        data=(id_cliente,)
        sql = "SELECT n_mesa, cant_comensales, total, hora_ingreso, hora_egreso FROM clientes WHERE id =?;"
        cursor.execute(sql, data)
        con.commit()
        cliente_actualiza = cursor.fetchall()
        return cliente_actualiza
    
    def selecc_tree_clientes_sql(self, id_cliente):
        """
        Obtiene y retorna de la tabla "clientes" los datos requeridos de un cliente para 
        presentar en el tree *listado* de la ventana principal.
        
        :param id_cliente: (_int_) ID del clientte seleccionado.
        
        :returns cliente_seleccionado: (_list_) listado de atributos del cliente seleccionado que serán presentados en el Tree de la ventana principal.
        
        """
        con=self.conexion_bd()
        cursor = con.cursor()
        data=(id_cliente,)
        sql = "SELECT n_mesa, cant_comensales, estado FROM clientes WHERE id =?;"
        cursor.execute(sql, data)
        con.commit()
        cliente_seleccionado = cursor.fetchall()
        return cliente_seleccionado
    
    def selecc_tree_consumos_sql(self, id_cliente):
        """
        Obtiene y retorna de la tabla "clientes" los datos requeridos de un cliente para 
        presentar en el tree *listado_consumos* de la ventana secundaria.
        
        :param id_cliente: (_int_) ID del clientte seleccionado.
        
        :returns cliente_seleccionado: (_list_) listado de atributos del cliente seleccionado que serán presentados en el Tree de la ventana principal.
        
        """
        con=self.conexion_bd()
        cursor = con.cursor()
        data=(id_cliente,)
        sql = "SELECT producto, precio FROM consumos WHERE cliente =?;"
        cursor.execute(sql, data)
        con.commit()
        cliente_seleccionado = cursor.fetchall()
        return cliente_seleccionado
    
class BaseConsumos(Conexion):
    """
    La clase *BaseConsumos()* cuenta con los métodos que brindan con las directrices necesarias 
    para administrar la información de la base de datos "consumos".

    """
    
    def __init__(self):
        self.est_mesa=BaseClientes()
        #self.validacion=regex.Validar()
    
    def suma_total_sql(self, id_client, nuevo_precio, root):
        """
        Actualiza en la tabla "clientes" el atributo *total* del cliente seleccionado al agregar un pedido.

        :param id_client: (_int_) ID del cliente seleccionado.
        :param nuevo_precio: (_float_) precio del pedido agregado.
        :param root: (_root_) objeto root de Tkinter.
        """
        principal=root
        id_cliente= id_client
        precio=nuevo_precio
        
        data=(id_cliente,)
        sql = "SELECT total FROM clientes WHERE id =?;"
        con=self.conexion_bd()
        cursor = con.cursor()
        cursor.execute(sql, data)
        con.commit()
        total= cursor.fetchall()
        for anterior in total:
            total_ul=anterior[0]
            total_ul+=precio
            principal.var_total_pagar.set(total_ul)
            
            data2=(total_ul, id_cliente)
            sql2="UPDATE clientes SET total=? WHERE id=?;"
            con=self.conexion_bd()
            cursor = con.cursor()
            cursor.execute(sql2, data2)
            con.commit()
    
    def resta_total_sql(self, id_client, nuevo_precio, root):
        """
        Actualiza en la tabla "clientes" el atributo *total* del cliente seleccionado al borrar un pedido.
        
        :param id_client: (_int_) ID del cliente seleccionado.
        :param nuevo_precio: (_float_) precio del pedido borrado.
        :param root: (_root_) objeto root de Tkinter.
        
        """
        principal=root
        id_cliente= id_client
        precio=nuevo_precio
        
        data=(id_cliente,)
        sql = "SELECT total FROM clientes WHERE id =?;"
        con=self.conexion_bd()
        cursor = con.cursor()
        cursor.execute(sql, data)
        con.commit()
        total= cursor.fetchall()
        for anterior in total:
            print("anterior o ", anterior[0])
            total_ul=float(anterior[0])
            total_ul-=precio
            principal.var_total_pagar.set(total_ul)
                
            data2=(total_ul, id_cliente)
            sql2="UPDATE clientes SET total=? WHERE id=?;"
            con=self.conexion_bd()
            cursor = con.cursor()
            cursor.execute(sql2, data2)
            con.commit()
    
    def alta_compra_sql(self, id_cliente, producto, precio, root):
        """
        Agrega un pedido a la tabla "consumos" y lo asocia al cliente seleccionado mediante su ID.
        
        :param id_cliente: (_int_) ID del cliente seleccionado.
        :param producto: (_str_) nombre del producto.
        :param precio: (_float_) precio del producto.
        :param root: (_root_)  objeto root de Tkinter.
        """
        principal=root
        cliente= id_cliente
        
        data=(producto, precio, cliente)
        sql="INSERT INTO consumos(producto, precio, cliente) VALUES( ?, ?, ?)"
        
        con=self.conexion_bd()
        cursor = con.cursor()
        cursor.execute(sql, data)
        con.commit()
        
        self.suma_total_sql(cliente, precio, principal)
    
    def baja_compra_sql(self, id_cliente, producto, precio, root):
        """
        Borra un pedido a la tabla "consumos".
        
        :param id_cliente: (_int_) ID del cliente seleccionado.
        :param producto: (_str_) nombre del producto.
        :param precio: (_float_) precio del producto.
        :param root: (_root_)  objeto root de Tkinter.
        """
        principal=root
        con=self.conexion_bd()
        cursor = con.cursor()
        mi_id = int(id_cliente)
        prod= str(producto)
        prec=float(precio)
        
        
        data = (mi_id, prod, prec)
        sql = "DELETE from consumos WHERE cliente = ? AND producto = ? AND precio = ?;"
        cursor.execute(sql, data)
        con.commit()
            
        self.resta_total_sql(mi_id, prec, principal)

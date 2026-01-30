





def registro_abm(funcion):
    def envoltura(*args, **kwargs):
            
        envoltura.numero_de_llamada+=1
        
        
        if funcion.__name__=="alta_sql":
            acto= "ALTA del cliente "
        elif funcion.__name__=="modifica_comensal_sql":
            acto= "MODIFICA COMENSAL el cliente "
        elif funcion.__name__=="cierra_sql":
            acto= "CIERRA MESA el cliente "
        elif funcion.__name__=="modifica_mesa_sql":
            acto= "MODIFICA MESA el cliente "
        elif funcion.__name__=="borra_cliente_sql":
            acto= "BORRADO el cliente "
        
        print("#"* 42)
        print("LLAMADA DESDE DECORADOR")
        
        print("Llamada número %s a la función %s" %(envoltura.numero_de_llamada, funcion.__name__, ))
        print(acto, funcion(*args, **kwargs))
        
        print("#"* 42)
        
        
    envoltura.numero_de_llamada=0
    
    return envoltura


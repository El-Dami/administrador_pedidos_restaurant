


class Sujeto:

    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def quitar(self, obj):
        
        for observad in self.observadores:
            if observad==obj:
                del observad
                

    def notificar(self, *args):
        for observador in self.observadores:
            observador.update(args)


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ConcreteObserverA(Observador):
    def __init__(self, obj):
        self.observado_a = obj
        self.observado_a.agregar(self)

    def update(self, *args):
        print("#"*40)
        print("NOTIFICACIÖN DESDE EL OBSERVADOR")
        print("Producto solicitado ==> %s" %(args[0][0]))  
        print("Mesa Nº==> %s" %(args[0][1]))
        print("#"*40)




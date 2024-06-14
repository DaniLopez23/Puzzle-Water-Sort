import hashlib

class Nodo:
    def __init__(self=None, id=None, costo=None, estado=None, profundidad=None, heuristica=None, valor=None, id_padre=None, accion=None):
        self.id = id
        self.costo = costo
        self.estado = estado
        self.id_padre = id_padre
        self.accion = accion
        self.profundidad = profundidad
        self.heuristica = heuristica
        self.valor = valor

    def __str__(self):
        """
        La función devuelve una representación de cadena de un objeto, incluidos varios atributos y sus valores.
        :return: El método `__str__` devuelve una representación de cadena formateada de un objeto. La cadena devuelta 
        incluye varios atributos del objeto formateados y concatenados  mediante interpolación de cadenas (`f-string`).
        """
        if(self.id_padre == None):
            return f"[{self.id}][{self.costo:.1f},{hashlib.md5(str(self.estado.exportar_Estado()).encode()).hexdigest()},None,None,{self.profundidad},{self.heuristica},{self.valor:.2f}]"

        return f"[{self.id}][{self.costo:.1f},{hashlib.md5(str(self.estado.exportar_Estado()).encode()).hexdigest()},{self.id_padre.id},{tuple(self.accion)},{self.profundidad},{self.heuristica},{self.valor:.2f}]"

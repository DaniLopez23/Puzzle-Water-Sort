class Visitados():
        
    def crear_vacio(self):
        """
        Inicializa un conjunto vacío llamado "visited_nodes".
        """
        self.nodos_visitados = set() 
    
    def insertar(self, nodo):
        """
        Añade un nodo a un conjunto llamado "nodos_visitados".
        
        :param nodo: Representa un nodo que desea insertar en la estructura de datos
        """
        self.nodos_visitados.add(nodo)
    
    def pertenece(self, nodo_actual):
        """
        Comprueba si un nodo determinado ya está en la lista de nodos visitados.
        
        :param nodo_actual: Representa el nodo actual que se está verificando para determinar si se encuentra en la lista de nodos visitados
        :return: un valor booleano. Devuelve True si el "nodo_actual" dado se encuentra en la lista "self.nodos_visitados", y False en caso contrario.
        """
        for nodo in self.nodos_visitados:
         if nodo.estado.exportar_Estado() == nodo_actual.estado.exportar_Estado():
            return True
        return False


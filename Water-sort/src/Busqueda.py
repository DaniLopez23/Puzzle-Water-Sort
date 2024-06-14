from Nodo import Nodo
from Visitados import Visitados
from sortedcontainers import SortedList
import hashlib

class Busqueda:
    LastID = 1  # Esta es una variable de clase o estática

    def Expand(self, node, problem, opcion):
        """
        La función Expand genera nodos sucesores para un nodo determinado en un problema de búsqueda,
        según la estrategia de búsqueda elegida.
        
        :param node: El nodo actual en el árbol de búsqueda
        :param problem: El parámetro "problema" es una instancia de una clase de problema que define el
        espacio de estados y determina las acciones que se pueden tomar en ese espacio de estados. Proporciona la
        información necesaria para generar sucesores de un nodo determinado
        :param opcion: El parámetro "opción" es una cadena que determina el tipo de estrategia de búsqueda a
        utilizar. Puede tomar uno de los siguientes valores: DEPTH, BREADTH o UNIFORM
        :return: una lista de nodos sucesores.
        """
        successors = []
        for accion, result, cost in problem.sucesores(node.estado):
            s = Nodo()
            s.id = Busqueda.LastID
            s.id_padre = node
            s.accion = accion
            s.estado = result
            s.costo = node.costo + cost
            s.profundidad = node.profundidad + 1
            
            if (opcion == "DEPTH"): #Si la estrategia es en profundidad
                s.valor = 1 / (s.profundidad + 1)
            elif (opcion == "BREADTH"): #Si la estrategia es en anchura
                 s.valor = s.profundidad
            elif (opcion == "UNIFORM"): #Si la estrategia es coste uniforme
                s.valor = s.costo

            successors.append(s) #Añadir el nodo a la lista de sucesores
            Busqueda.LastID += 1
        return successors


    def Graph_Search(self, problem, opcion):
        """
        La función Graph_Search realiza un algoritmo de búsqueda de gráficos utilizando diferentes
        estrategias para encontrar una solución a un problema determinado.
        
        :param problem: El parámetro "problema" es una instancia de una clase de problema que define el
        estado inicial y capacidad máxima de las botellas. Se utiliza 
        para determinar el estado objetivo y generar nodos sucesores durante el proceso de búsqueda
        :param opcion: El parámetro "opción" es una cadena que especifica la estrategia de búsqueda a
        utilizar. Puede tomar uno de los siguientes valores: DEPTH, BREADTH o UNIFORM
        :return: failure si la lista de nodos pendientes está vacía, o devuelve el nodo si se alcanza el estado objetivo.
        """
        visitados = Visitados() 
        visitados.crear_vacio() #Crear conjunto de nodos visitados vacio
        frontera = SortedList(key=lambda nodo: (nodo.valor, nodo.id))    # Insertar el nodo inicial en la lista de nodos pendientes ordenado según el valor y el ID

        if opcion == "DEPTH": # Si la estrategia es en profundidad
            nodo_inicial = Nodo(0, 0, problem.initState, 0, None, 1, None, None)
        else: # Si la estrategia es en anchura o coste uniforme
            nodo_inicial = Nodo(0, 0, problem.initState, 0, None, 0, None, None)

        frontera.add(nodo_inicial) # Añadir el nodo inicial a la lista de nodos pendientes

        while True:
            if len(frontera) == 0:   # Si la lista de nodos pendientes está vacía, devolver una falla
                return "failure"
            nodo = frontera.pop(0)   # Extraer el primer nodo de la lista
            if problem.objetivo(nodo.estado):   # Si este nodo es un objetivo, devolverlo
                return nodo
            if not visitados.pertenece(nodo):  # Si el estado de este nodo no ha sido visitado, añadirlo a la lista de visitados y expandir sus sucesores
                visitados.insertar(nodo)
                frontera.update(self.Expand(nodo, problem, opcion))

                
                
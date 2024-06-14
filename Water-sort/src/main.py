from Busqueda import Busqueda
from Problema import Problema
from Nodo import Nodo

def mostrar_menu():
    """
    Muestra un menú y solicita al usuario que seleccione un algoritmo de búsqueda.
    :return: la estrategia del algoritmo de búsqueda seleccionada como una cadena.
    """
    estrategias = {1: "DEPTH", 2: "BREADTH", 3: "UNIFORM"}
    opcion = None
    while opcion not in [1, 2, 3]:
        print("""Selecciona uno de los algoritmos de búsqueda (1-3):
    1.- Profundidad
    2.- Anchura
    3.- Coste uniforme""")
        entrada = input()

        if entrada.isdigit():
            opcion = int(entrada)
            if opcion not in [1, 2, 3]:
                print("Error. Introduce un número entre 1 y 3.")
            else:
                return estrategias[opcion]
        else:
            print("Error leyendo el dato introducido.")

def guardar_solucion(nodo_solucion, problema, opcion):
    """
    Guarda la solución de un problema escribiendo los nodos de la solución en un archivo de texto.
    
    :param nodo_solucion: Representa el nodo final de la solución en un algoritmo de búsqueda. 
    :param problema: Es un objeto que representa el problema para el cual se guarda la solución.
    :param opcion: Es una cadena que representa el tipo de algoritmo de búsqueda solicitado.
    Se utiliza para generar el nombre de archivo de la solución guardada junto con el id del problema.
    """
    lista_nodos_solucion = []

    while nodo_solucion.id_padre:
        lista_nodos_solucion.append(nodo_solucion)
        nodo_solucion = nodo_solucion.id_padre

    with open(f'{problema.id}_{opcion.capitalize()}.txt', 'w') as f:
        f.write(str(nodo_solucion) + '\n')

        for nodo in reversed(lista_nodos_solucion):
            f.write(str(nodo) + '\n')


def main():  
    """
    La función principal importa un problema desde un archivo JSON, muestra el estado inicial y la
    capacidad del problema, solicita al usuario una opción de búsqueda, realiza una búsqueda 
    utilizando la opción elegida y guarda la solución si la encuentra.
    """
    problema = Problema()
    problema.importar_problema("importar.json")
    print(f"Problema: {problema.id} Estado: {problema.initState.listaBotellas} Capacidad: {problema.bottleSize}\n")
    opcion=mostrar_menu()
  
    nodo_solucion = Busqueda.Graph_Search(Busqueda(),problema, opcion)
    if nodo_solucion == "failure":
        print("No se ha encontrado solución")
    else:
        guardar_solucion(nodo_solucion, problema, opcion)
    

if __name__ == "__main__":
    main()
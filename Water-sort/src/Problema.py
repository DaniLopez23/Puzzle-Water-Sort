import copy
import sys
import json
from Estado import Estado

class Problema:  
    def __init__(self, id=None, initState=None, bottleSize=None):
        self.id=id
        self.initState=initState
        self.bottleSize=bottleSize


    def objetivo(self, estado):
        """
        Comprueba si el estado dado de las botellas satisface determinadas condiciones. 
        Estas condiciones son que cada botella contenga un solo color y que los colores de las 
        botellas sean únicos.
        
        :param estado: El parámetro "estado" representa el estado de las botellas. Es un objeto de la clase Estado,
        que tiene una propiedad llamada "listaBotellas", que es una lista de botellas. Cada botella
        se representa como una lista de porciones, donde cada porción es una tupla que contiene el color y
        la cantidad de líquido
        :return: el valor de la variable "aux".
        """

        aux = True
        color_botella = set() # Creamos un nuevo conjunto para almacenar los colores de las botellas
        for botella in estado.listaBotellas: # Recorremos la lista de botellas
            color_liquido = set() # Creamos un nuevo conjunto para almacenar los colores de las porciones de la botella
            for porcion in botella: # Recorremos la lista de porciones de la botella
                color_liquido.add(porcion[0]) # Añadimos el color de la porción al nuevo conjunto
            if len(color_liquido) not in [0, 1]: # Comprobamos si la botella tiene más de un color
                aux = False
                break
            elif len(color_liquido) == 1: # Comprobamos si la botella tiene un solo color
                color_actual = color_liquido.pop()  # Guardamos el color actual
                if color_actual in color_botella:   # Comprobamos si el color actual ya está en el conjunto
                    aux = False
                    break
                else:
                    color_botella.add(color_actual)  # Añadimos el color de la botella al nuevo conjunto
        return aux
    
    

    def sucesores(self, estado):
        """
        Genera una lista de estados sucesores basados en el estado actual del sistema.
        
        :param estado: El parámetro "estado" representa el estado actual del sistema, el cual incluye la lista de botellas y sus respectivos niveles de líquido
        :return: una lista de sucesores. Cada sucesor se representa como una lista que contiene tres elementos: la acción realizada 
        (representada como una lista con el índice de la botella de origen, el índice de la botella de destino y la cantidad de líquido transferido), 
        el estado resultante después de la acción y un valor de costo de 1.
        """
        sucesores = []
        estadoActual = estado.listaBotellas #Obtener lista de botellas
        for i, botella_origen in enumerate(estadoActual): #Recorrer lista de botellas
            cantidad_liquido = botella_origen[0][1] if botella_origen else -1  #Obtener cantidad superior del liquido de la botella
            if cantidad_liquido != -1: #Si la botella no esta vacia
                for posicion in range(0, len(estadoActual)): #Recorrer lista de botellas
                    if posicion != i:  #Si la botella de origen no es igual a la de destino
                        valido =  estado.accion(i, posicion, cantidad_liquido) #Si se puede devuelve la lista
                        if valido != None: #Si la accion es valida, ya que devuelve None si no lo es
                            sucesor = [[i, posicion, cantidad_liquido], valido, 1] #Crea el sucesor
                            sucesores.append(sucesor)

                sucesores.sort(key=lambda x: (x[0][0], x[0][1], x[0][2]))  #Ordena los sucesores según lo especificado en el enunciado
        return sucesores
    
    
    def importar_problema(self, file_path):
        """
        La función importa un problema desde un archivo JSON, extrae datos relevantes y maneja varios casos
        de error.
        
        :param file_path: La ruta del archivo es la ubicación del archivo que desea importar. Debe ser una
        cadena que especifique el nombre y la extensión del archivo.
        """

        try:
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file) # Cargar el archivo JSON
                    self.id = data['id'] # Obtener el ID del problema
                    self.initState = Estado(data['initState'], data['bottleSize']) # Crear un nuevo estado inicial
                    self.bottleSize = data['bottleSize'] # Obtener el tamaño de la botella
                except json.JSONDecodeError as e:
                    print(f"Error al analizar el archivo: {file}") # Error al analizar el archivo
                    sys.exit()
        except FileNotFoundError as e:
            print(f"No se ha encontrado el archivo: {file_path}") # Error al abrir el archivo
            sys.exit()
        except Exception as e:
            print(f"Error {e} desconocido al analizar el archivo: {file}") # Error desconocido
            sys.exit()


    def exportar_problema(self):
        """
        La función exporta un problema a un archivo JSON. Con los datos almacenados en el objeto de la clase Problema. 
        Para el nombre del archivo, se utiliza el ID del problema.
        """

        data = {
                'id': self.id,
                'bottleSize': self.bottleSize,
                'initState': self.initState.listaBotellas,
            }
        file_path = f"{self.id}.json"  # Generar la ruta del archivo usando el ID del problema
        try:
                with open(file_path, 'w') as file:
                    try:
                        json.dump(data, file) # Convertir los datos a JSON y escribirlos en el archivo
                    except TypeError as e:
                        print(f"Error al convertir los datos a JSON: {e}") # Error al convertir los datos a JSON
                        sys.exit()

        except IOError as e:
                print(f"Error al abrir el archivo {file_path} para escritura: {e}")
                sys.exit()


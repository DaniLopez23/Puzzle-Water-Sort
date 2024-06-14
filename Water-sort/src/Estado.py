import copy
class Estado:
    def __init__(self, listaBotellas, capacidad_maxima):
        self.listaBotellas = listaBotellas
        self.capacidad_maxima = capacidad_maxima

    def accion(self,indice_origen, indice_destino, cantidad):
     """
       La función accion toma tres parámetros (indice_origen, indice_destino, cantidad) y devuelve un
       nuevo objeto estado con la acción especificada aplicada a la lista de botellas.
       
       :param indice_origen: Representa el índice de la botella fuente desde la cual se verterá el líquido
       :param indice_destino: Representa el índice de la botella de destino donde se recibirá el líquido
       :param cantidad: Representa la cantidad de líquido que se transferirá de una botella a otra
       :return: Una nueva instancia de la clase Estado con estados de botella actualizados, o None si la acción no es posible.
     """
     nuevoEstado = Estado(copy.deepcopy(self.listaBotellas), self.capacidad_maxima)
     try:
            if nuevoEstado.es_AccionPosible(nuevoEstado.listaBotellas[indice_origen], nuevoEstado.listaBotellas[indice_destino], cantidad):
                lista = nuevoEstado.desplazarPorcion(nuevoEstado.listaBotellas[indice_origen], nuevoEstado.listaBotellas[indice_destino], cantidad)
                nuevoEstado.listaBotellas[indice_origen] = lista[0]
                nuevoEstado.listaBotellas[indice_destino] = lista[1]
                return nuevoEstado
            else:
                return None
     except IndexError as e:
            print(f"Error al acceder a la botella: {e}")

    def desplazarPorcion(self, botella_origen, botella_destino, porcion):
        """
        Toma una porción de líquido de una botella y la añade a otra botella. Previamente se comprueba que la botella 
        origen no esté vacia.
        
        :param botella_origen: Representa la botella origen de la cual queremos mover una porción de líquido
        :param botella_destino: Representa la botella de destino donde se recibirá la porción de líquido
        :param porcion: Representa la cantidad de líquido que se trasladará desde la botella de origen a la botella de destino
        :return: una lista que contiene botella_origen y botella_destino actualizadas.
        """
        for i in range(0,porcion):
            color_origen = botella_origen[0][0] if botella_origen else -1 #Obtener el color del primer líquido de la botella de origen
            botella_origen=self.separarPorcion(botella_origen) #Sustraemos una porción de la botella de origen
            botella_destino=self.recibirPorcion(botella_destino, color_origen) #La añadimos a la botella de destino
        return [botella_origen, botella_destino]

    def separarPorcion(self, botella_origen):
        """
        Toma una lista de botellas como entrada, resta 1 de la cantidad de la
        primera botella y elimina la botella de la lista si la cantidad pasa a 0.
        
        :param botella_origen: Representa la botella desde la cual se vierte o transfiere el líquido.
        :return: la lista actualizada `botella_origen` después de restar 1 a la cantidad de la primera
        botella en la lista. Si la cantidad llega a 0, la primera botella se elimina de la lista.
        """
        cantidad_origen = botella_origen[0][1] if botella_origen else -1
        if (cantidad_origen!=-1): #Control de errores 
            botella_origen[0][1] -= 1       #Restar una unidad a la cantidad de la botella de origen ->
                                            # -> (Recordamos que esta función se encuentra en un bucle for)
            if (botella_origen[0][1]==0): #Eliminamos la botella de origen de la lista si la cantidad de llenado es 0
              botella_origen.pop(0)
        return botella_origen

    def recibirPorcion(self, botella_destino, color_origen):
        """
        La función recibe un color y una botella de destino, y agrega el color a la botella si el primer color de esta coincide con el color de origen.
        Si la botella de destino está vacía, se agrega el color de origen a la botella de destino.

        :param botella_destino: Representa la botella de destino, que es una lista que contiene el color y la cantidad de líquido en la botella. 
        :param color_origen: El color del líquido en la botella origen de la primera porción
        :return: la lista actualizada `botella_destino`.
        """
        color_destino = botella_destino[0][0] if botella_destino else -1
        if color_destino == -1: #Comprobar si la botella de destino está vacía
            botella_destino.append([color_origen, 1]) #Añadimos la cantidad del color indicado a la botella de destino
        elif color_destino == color_origen: #Si no está vacía, comprobar si el color del líquido de la botella de destino es igual al de la botella de origen
            botella_destino[0][1] += 1 #En caso afirmativo, sumar una unidad a la cantidad de la botella de destino con ese color->
                                       # -> (Recordamos que esta función se encuentra en un bucle for)
        else:
            botella_destino.insert(0,[color_origen, 1]) #Si no se dan los casos anteriores, añadimos el líquido de otro color a la botella de destino
        return botella_destino
    
    def es_AccionPosible(self, botella_origen, botella_destino, cantidad):
        """
        Comprueba si es posible transferir una determinada cantidad de líquido
        de una botella a otra, basándose en las condiciones de tener suficiente líquido en la botella de
        origen, suficiente espacio en la botella de destino y que las botellas tengan el mismo color.
        
        :param botella_origen: Representa la botella desde la cual se vierte o transfiere el líquido.
        :param botella_destino: Representa la botella de destino donde se verterá el líquido
        :param cantidad: Representa la cantidad de líquido que se transfiere desde la botella de origen a la botella de destino
        :return: un valor booleano.
        """
        return self.tiene_suficiente(botella_origen, cantidad) and self.cabe(botella_destino, cantidad) and self.mismo_color(botella_origen, botella_destino)
    

    def obtener_cantidad_llenada(self, botella):
        """
        Calcula la cantidad total llenada en una botella sumando la cantidad de cada porción de liquido de la botella.
        
        :param botella: Es una lista de listas. Cada lista interior representa una porción y contiene dos elementos (color y la cantidad).
        :return: la cantidad total llenada en la botella, que es la suma del segundo índice de cada lista en la lista de botellas dada.
        """
        total=0
        for i in botella:
            total += i[1]
        return total
    
    #Condición 1
    def tiene_suficiente(self, botella, cantidad):
        """
        Comprueba si la cantidad echada en una botella es suficiente, es decir, si la botella tiene más líquido o igual a una determinada cantidad de líquido.

        :param botella: Representa un objeto botella.
        :param cantidad: Representa la cantidad de líquido que se desea llenar en la botella.
        :return: un valor booleano que indica si la cantidad llenada en la botella es mayor o igual a la cantidad dada.
        """
        return self.obtener_cantidad_llenada(botella) >= cantidad

    #Condición 2
    def cabe(self, botella, llenado):
        """
        Comprueba si hay suficiente espacio en una botella para llenarla con una determinada cantidad de líquido.
        
        :param botella: Representa un objeto botella.
        :param llenado: Representa la cantidad de líquido que se está llenando en la botella.
        :return: un valor booleano. Indica si la diferencia entre la capacidad máxima y la
        cantidad ya llena en la botella es mayor o igual a la cantidad a llenar.
        """
        return self.capacidad_maxima - self.obtener_cantidad_llenada(botella) >= llenado

        #Condición 3
    def mismo_color(self, botella_origen, botella_destino):
        """
        La función "mismo_color" comprueba si el color de la botella de origen es el mismo que el color de la botella de destino o si la botella de destino no tiene color.
        :param botella_origen: Representa la botella de origen.
        :param botella_destino: Representa la botella de destino.
        :return: un valor booleano que indica si el color de la primera porción de la botella de origen es el mismo que el color de la porción superior
        de la botella de destino o si la botella de destino no tiene color.
        """
        igual = False
        if len(botella_origen)!=0: #Comprobar si la botella de origen tiene color 
            color_origen = botella_origen[0][0]
            color_destino = botella_destino[0][0] if botella_destino else -1
            # Comprobar si los colores son iguales o si la botella de destino no tiene el mismo color
            if color_origen == color_destino or color_destino == -1:
                igual = True
        return igual

    def exportar_Estado(self):
        """
        Devuelve una representación en cadena de una lista de objetos.
        :return: una representación de cadena de una lista de objetos. Los objetos se convierten en cadenas
        usando la función `str()` y luego se unen con comas usando el método `join()`. La cadena resultante
        está entre corchetes.
        """
        return '[' + ', '.join(map(str, self.listaBotellas)).replace(' ', '') + ']'
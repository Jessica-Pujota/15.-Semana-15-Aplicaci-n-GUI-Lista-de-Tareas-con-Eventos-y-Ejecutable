# modelos/tarea.py
# Clase que representa una tarea individual

class Tarea: # Modelo de una tarea.
    """ Atributos:
        id (int): identificador único.
        descripcion (str): texto de la tarea.
        completado (bool): estado de finalización.
    """
    _id_counter = 0

    def __init__(self, descripcion): # Inicializa una nueva tarea con una descripción y un ID único.
        Tarea._id_counter += 1
        self.id = Tarea._id_counter
        self.descripcion = descripcion
        self.completado = False

    def __str__(self): # Representación legible de la tarea.
        return f"[{self.id}] {self.descripcion} - {'Completada' if self.completado else 'Pendiente'}"

    def marcar_completada(self): #Cambia el estado a completado.
        self.completado = True
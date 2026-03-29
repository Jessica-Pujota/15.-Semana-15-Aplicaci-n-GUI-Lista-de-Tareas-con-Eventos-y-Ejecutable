# servicios/tarea_servicio.py
# Lógica de negocio: manejo de la colección de tareas

from modelos.tarea import Tarea

class TareaServicio: #Servicio que gestiona las operaciones sobre la lista de tareas

    def __init__(self):
        self.tareas = []  # lista de objetos Tarea

    def agregar_tarea(self, descripcion): #Crea y añade una nueva tarea si la descripción no está vacía.
        if not descripcion or descripcion.strip() == "":
            return False
        nueva_tarea = Tarea(descripcion.strip())
        self.tareas.append(nueva_tarea)
        return True

    def completar_tarea(self, tarea_id): #Marca una tarea como completada si existe
        for tarea in self.tareas:
            if tarea.id == tarea_id:
                tarea.marcar_completada()
                return True
        return False

    def eliminar_tarea(self, tarea_id): #Elimina una tarea por su id.
        for tarea in self.tareas:
            if tarea.id == tarea_id:
                self.tareas.remove(tarea)
                return True
        return False

    def obtener_todas(self): #Retorna la lista de todas las tareas (sin modificar)
        return self.tareas
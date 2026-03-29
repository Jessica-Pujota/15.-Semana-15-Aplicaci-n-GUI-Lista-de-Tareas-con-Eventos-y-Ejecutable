# ui/app_tkinter.py
# Interfaz gráfica con Tkinter y manejo de eventos

import tkinter as tk
from tkinter import ttk, messagebox
from servicios.servicio_tarea import TareaServicio

class TodoListApp: #Ventana principal de la aplicación To-Do List.

    def __init__(self):
        self.servicio = TareaServicio()
        self.ventana = tk.Tk()
        self.ventana.title("Lista de Tareas")
        self.ventana.geometry("500x400")
        self.ventana.resizable(False, False)

        self._crear_widgets()
        self._cargar_tareas()

    def _crear_widgets(self): #Crea y organiza los componentes gráficos.
        # Marco superior: entrada y botón añadir
        frame_superior = ttk.Frame(self.ventana)
        frame_superior.pack(pady=10, padx=10, fill=tk.X)

        self.entry_tarea = ttk.Entry(frame_superior, width=40)
        self.entry_tarea.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        self.entry_tarea.bind("<Return>", self._evento_enter)  # Evento teclado

        btn_anadir = ttk.Button(frame_superior, text="Añadir Tarea", command=self._anadir_tarea)
        btn_anadir.pack(side=tk.RIGHT)

        # Treeview para mostrar tareas
        columnas = ("ID", "Descripción", "Estado")
        self.tree = ttk.Treeview(self.ventana, columns=columnas, show="headings", height=12)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Estado", text="Estado")
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Descripción", width=300)
        self.tree.column("Estado", width=100, anchor=tk.CENTER)
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Evento de doble clic sobre una tarea
        self.tree.bind("<Double-1>", self._evento_doble_clic)

        # Marco inferior: botones de acción
        frame_inferior = ttk.Frame(self.ventana)
        frame_inferior.pack(pady=10, padx=10, fill=tk.X)

        btn_completar = ttk.Button(frame_inferior, text="Marcar Completada", command=self._marcar_completada)
        btn_completar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = ttk.Button(frame_inferior, text="Eliminar", command=self._eliminar_tarea)
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        btn_salir = ttk.Button(frame_inferior, text="Salir", command=self.ventana.quit)
        btn_salir.pack(side=tk.RIGHT, padx=5)

    def _cargar_tareas(self): #Actualiza el Treeview con las tareas actuales.
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar cada tarea
        for tarea in self.servicio.obtener_todas(): #Obtener todas las tareas del servicio
            estado = "Completada" if tarea.completado else "Pendiente"
            valores = (tarea.id, tarea.descripcion, estado)
            item_id = self.tree.insert("", tk.END, values=valores)

            # Cambiar el color del texto si está completada (feedback visual)
            if tarea.completado:
                self.tree.tag_configure("completado", foreground="gray")
                self.tree.item(item_id, tags=("completado",))

    def _anadir_tarea(self): #Añade una nueva tarea usando el contenido del campo de entrada.
        descripcion = self.entry_tarea.get()
        if self.servicio.agregar_tarea(descripcion):
            self.entry_tarea.delete(0, tk.END)
            self._cargar_tareas()
        else:
            messagebox.showwarning("Entrada inválida", "La descripción no puede estar vacía.")

    def _obtener_tarea_seleccionada(self): #Obtiene el ID de la tarea seleccionada en el Treeview.
        seleccion = self.tree.selection()
        if not seleccion:
            return None
        # El ID está en la primera columna
        item = self.tree.item(seleccion[0])
        tarea_id = item['values'][0]
        return tarea_id

    def _marcar_completada(self): #Marca como completada la tarea seleccionada.
        tarea_id = self._obtener_tarea_seleccionada()
        if tarea_id is None:
            messagebox.showinfo("Sin selección", "Selecciona una tarea para marcar como completada.")
            return
        if self.servicio.completar_tarea(tarea_id):
            self._cargar_tareas()
        else:
            messagebox.showerror("Error", "No se pudo completar la tarea.")

    def _eliminar_tarea(self): #Elimina la tarea seleccionada.
        tarea_id = self._obtener_tarea_seleccionada()
        if tarea_id is None:
            messagebox.showinfo("Sin selección", "Selecciona una tarea para eliminar.")
            return
        if self.servicio.eliminar_tarea(tarea_id):
            self._cargar_tareas()
        else:
            messagebox.showerror("Error", "No se pudo eliminar la tarea.")

    # ---------- Manejadores de eventos con bind ----------
    def _evento_enter(self, event): #Manejador de la tecla Enter: añade la tarea.
        self._anadir_tarea()

    def _evento_doble_clic(self, event): #Manejador de doble clic: marca como completada la tarea seleccionada
        self._marcar_completada()

    def run(self): #Inicia el bucle principal de la aplicación.
        self.ventana.mainloop()
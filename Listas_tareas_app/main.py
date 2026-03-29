# main.py
# Orquestador: importa la clase de la interfaz y lanza la aplicación

from ui.app_tkinter import TodoListApp

if __name__ == "__main__": # Punto de entrada de la aplicación
    
    app = TodoListApp()
    app.run()
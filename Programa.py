import tkinter as tk
from tkinter import messagebox

# Función para inicializar la GUI
def init_gui():
    window = tk.Tk()
    window.title("Gestión de Colección de Películas")

    # Etiquetas y campos de entrada
    tk.Label(window, text="Nombre de la película:").grid(row=0, column=0)
    name_entry = tk.Entry(window)
    name_entry.grid(row=0, column=1)

    tk.Label(window, text="Año:").grid(row=1, column=0)
    year_entry = tk.Entry(window)
    year_entry.grid(row=1, column=1)

    tk.Label(window, text="Formato:").grid(row=2, column=0)
    format_entry = tk.Entry(window)
    format_entry.grid(row=2, column=1)

    tk.Label(window, text="Tamaño:").grid(row=3, column=0)
    size_entry = tk.Entry(window)
    size_entry.grid(row=3, column=1)

    # Botones
    tk.Button(window, text="Buscar", command=lambda: buscar_pelicula(name_entry.get())).grid(row=4, column=0)
    tk.Button(window, text="Añadir", command=lambda: añadir_pelicula(name_entry.get(), year_entry.get(), format_entry.get(), size_entry.get())).grid(row=4, column=1)
    tk.Button(window, text="Modificar", command=lambda: modificar_pelicula(name_entry.get())).grid(row=5, column=0)
    tk.Button(window, text="Eliminar", command=lambda: eliminar_pelicula(name_entry.get())).grid(row=5, column=1)

    # Área de texto para resultados
    result_text = tk.Text(window, height=10, width=50)
    result_text.grid(row=6, column=0, columnspan=2)

    window.mainloop()

# Ejemplo de una función de búsqueda (placeholder, necesitará más desarrollo)
def buscar_pelicula(nombre):
    # Lógica de búsqueda aquí
    print("Buscar:", nombre)

# Placeholder para funciones de añadir, modificar, eliminar
def añadir_pelicula(nombre, año, formato, tamaño):
    print("Añadir:", nombre, año, formato, tamaño)

def modificar_pelicula(nombre):
    print("Modificar:", nombre)

def eliminar_pelicula(nombre):
    print("Eliminar:", nombre)

# Iniciar la GUI
init_gui()
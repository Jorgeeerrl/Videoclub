import tkinter as tk
from tkinter import messagebox
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def init_driver():
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service)

def cargar_datos():
    try:
        return pd.read_excel('Videoclub.xlsx')
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
        return pd.DataFrame()  # Retorna un DataFrame vacío para manejo de errores

def guardar_datos(datosPeli):
    try:
        datosPeli.to_excel('Videoclub.xlsx', index=False)
    except PermissionError as e:
        messagebox.showerror("Error de permiso", f"No se pudo guardar el archivo: {str(e)}")

def buscar_pelicula(nombre, mensaje, datosPeli):
    try:
        pelicula = datosPeli[datosPeli['NOMBRE'].str.contains(nombre, case=False, na=False)]
        if not pelicula.empty:
            mensaje.insert(tk.END, f"Datos de la película encontrada:\n{pelicula}\n")
        else:
            mensaje.insert(tk.END, "La película no se encuentra en la colección.\n")
    except Exception as e:
        mensaje.insert(tk.END, f"Error al buscar: {str(e)}\n")

def añadir_pelicula(nombre, formato, tamaño, mensaje, driver, datosPeli):
    try:
        if nombre in datosPeli['NOMBRE'].values:
            mensaje.insert(tk.END, "La película ya existe en la colección.\n")
            return

        driver.get("https://www.filmaffinity.com")
        driver.find_element(By.CSS_SELECTOR,".css-113jtbf:nth-child(2) > span").click()
        search_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "stext")))
        search_box.send_keys(nombre)
        search_box.submit()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='title-result']/div/div[2]/div[2]/div/div[2]/div[1]/a"))).click()
        año_elemento = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//dd[@itemprop='datePublished']")))
        año = año_elemento.text.strip()
        director_elemento = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//span[@itemprop='name'])[2]")))
        director = director_elemento.text.strip()

        nuevosDatos = pd.DataFrame({'NOMBRE': [nombre], 'AÑO': [año], 'FORMATO': [formato], 'TAMAÑO': [tamaño], 'DIRECTOR': [director]})
        datosPeli = pd.concat([datosPeli, nuevosDatos], ignore_index=True)
        guardar_datos(datosPeli)
        mensaje.insert(tk.END, f"Película '{nombre}' añadida con éxito. Año: {año}, Director: {director}\n")
    except Exception as e:
        mensaje.insert(tk.END, f"Error al añadir la película: {str(e)}\n")

def modificar_pelicula(nombre, nuevo_nombre, nuevo_formato, nuevo_tamaño, mensaje):
    try:
        datosPeli = pd.read_excel('Videoclub.xlsx')
        indices = datosPeli[datosPeli['NOMBRE'].str.contains(nombre, case=False, na=False)].index
        if not indices.empty:
            datosPeli.loc[indices, 'NOMBRE'] = nuevo_nombre
            datosPeli.loc[indices, 'FORMATO'] = nuevo_formato
            datosPeli.loc[indices, 'TAMAÑO'] = nuevo_tamaño
            datosPeli.to_excel('Videoclub.xlsx', index=False)
            mensaje.insert(tk.END, f"Película '{nombre}' modificada con éxito.\n")
        else:
            mensaje.insert(tk.END, "La película no se encuentra en la colección.\n")
    except Exception as e:
        mensaje.insert(tk.END, f"Error al modificar la película: {str(e)}\n")

def eliminar_pelicula(nombre, mensaje):
    try:
        datosPeli = pd.read_excel('Videoclub.xlsx')
        datosPeli = datosPeli[~datosPeli['NOMBRE'].str.contains(nombre, case=False, na=False)]
        datosPeli.to_excel('Videoclub.xlsx', index=False)
        mensaje.insert(tk.END, f"Película '{nombre}' eliminada con éxito.\n")
    except Exception as e:
        mensaje.insert(tk.END, f"Error al eliminar la película: {str(e)}\n")


def init_gui():
    window = tk.Tk()
    window.title("Gestión de Colección de Películas")
    datosPeli = cargar_datos()  # Cargar los datos al inicio

    # Define los widgets como antes
    tk.Label(window, text="Nombre de la película:").grid(row=0, column=0)
    entrada_nombre = tk.Entry(window)
    entrada_nombre.grid(row=0, column=1)
    tk.Label(window, text="Formato:").grid(row=1, column=0)
    entrada_formato = tk.Entry(window)
    entrada_formato.grid(row=1, column=1)
    tk.Label(window, text="Tamaño:").grid(row=2, column=0)
    entrada_tamaño = tk.Entry(window)
    entrada_tamaño.grid(row=2, column=1)
    mensaje = tk.Text(window, height=15, width=100)
    mensaje.grid(row=6, column=0, columnspan=2)

    # Modifica los comandos de los botones para incluir datosPeli
    tk.Button(window, text="Buscar", command=lambda: buscar_pelicula(entrada_nombre.get(), mensaje, datosPeli)).grid(row=4, column=0)
    tk.Button(window, text="Añadir", command=lambda: añadir_pelicula(entrada_nombre.get(), entrada_formato.get(), entrada_tamaño.get(), mensaje, init_driver(), datosPeli)).grid(row=4, column=1)
    tk.Button(window, text="Modificar", command=lambda: modificar_pelicula(entrada_nombre.get(), entrada_nombre.get(), entrada_formato.get(), entrada_tamaño.get(), mensaje)).grid(row=5, column=0)
    tk.Button(window, text="Eliminar", command=lambda: eliminar_pelicula(entrada_nombre.get(), mensaje)).grid(row=5, column=1)

    window.mainloop()


if __name__ == "__main__":
    init_gui()
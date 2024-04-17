import tkinter as tk
from tkinter import messagebox
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def buscar_pelicula(nombre, result_text):
    try:
        df = pd.read_excel('Videoclub.xlsx')
        pelicula = df[df['NOMBRE'].str.contains(nombre, case=False, na=False)]
        if not pelicula.empty:
            result_text.insert(tk.END, f"Datos de la película encontrada:\n{pelicula}\n")
        else:
            result_text.insert(tk.END, "La película no se encuentra en la colección.\n")
    except Exception as e:
        result_text.insert(tk.END, f"Error al buscar la película: {str(e)}\n")

def añadir_pelicula(nombre, formato, tamaño, result_text):
    try:
        df = pd.read_excel('Videoclub.xlsx')
        if nombre in df['NOMBRE'].values:
            result_text.insert(tk.END, "La película ya existe en la colección.\n")
            return

        driver.get("https://www.filmaffinity.com")
        driver.find_element(By.CSS_SELECTOR,".css-113jtbf:nth-child(2) > span").click()
        search_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "stext")))
        search_box.send_keys(nombre)
        search_box.submit()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='title-result']/div/div[2]/div[2]/div/div[2]/div[1]/a"))).click()
        año_elemento = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//dd[@itemprop='datePublished']")))
        año = año_elemento.text.strip()

        new_data = pd.DataFrame({'NOMBRE': [nombre], 'AÑO': [año], 'FORMATO': [formato], 'TAMAÑO': [tamaño]})
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel('Videoclub.xlsx', index=False)
        result_text.insert(tk.END, f"Película '{nombre}' añadida con éxito. Año: {año}\n")
    except Exception as e:
        result_text.insert(tk.END, f"Error al añadir la película: {str(e)}\n")
    try:
        df.to_excel('Videoclub.xlsx', index=False)
    except PermissionError as e:
        result_text.insert(tk.END, f"Error de permiso al intentar escribir el archivo: {str(e)}\n")
    print(f"Asegúrate de que el archivo no esté abierto en otro programa y que tengas permisos adecuados.")

def modificar_pelicula(nombre, nuevo_nombre, nuevo_formato, nuevo_tamaño, result_text):
    try:
        df = pd.read_excel('Videoclub.xlsx')
        indices = df[df['NOMBRE'].str.contains(nombre, case=False, na=False)].index
        if not indices.empty:
            df.loc[indices, 'NOMBRE'] = nuevo_nombre
            df.loc[indices, 'FORMATO'] = nuevo_formato
            df.loc[indices, 'TAMAÑO'] = nuevo_tamaño
            df.to_excel('Videoclub.xlsx', index=False)
            result_text.insert(tk.END, f"Película '{nombre}' modificada con éxito.\n")
        else:
            result_text.insert(tk.END, "La película no se encuentra en la colección.\n")
    except Exception as e:
        result_text.insert(tk.END, f"Error al modificar la película: {str(e)}\n")

def eliminar_pelicula(nombre, result_text):
    try:
        df = pd.read_excel('Videoclub.xlsx')
        df = df[~df['NOMBRE'].str.contains(nombre, case=False, na=False)]
        df.to_excel('Videoclub.xlsx', index=False)
        result_text.insert(tk.END, f"Película '{nombre}' eliminada con éxito.\n")
    except Exception as e:
        result_text.insert(tk.END, f"Error al eliminar la película: {str(e)}\n")

def init_gui():
    window = tk.Tk()
    window.title("Gestión de Colección de Películas")
    tk.Label(window, text="Nombre de la película:").grid(row=0, column=0)
    name_entry = tk.Entry(window)
    name_entry.grid(row=0, column=1)
    tk.Label(window, text="Formato:").grid(row=1, column=0)
    format_entry = tk.Entry(window)
    format_entry.grid(row=1, column=1)
    tk.Label(window, text="Tamaño:").grid(row=2, column=0)
    size_entry = tk.Entry(window)
    size_entry.grid(row=2, column=1)
    result_text = tk.Text(window, height=15, width=50)
    result_text.grid(row=6, column=0, columnspan=2)
    tk.Button(window, text="Buscar", command=lambda: buscar_pelicula(name_entry.get(), result_text)).grid(row=3, column=0)
    tk.Button(window, text="Añadir", command=lambda: añadir_pelicula(name_entry.get(), format_entry.get(), size_entry.get(), result_text)).grid(row=3, column=1)
    tk.Button(window, text="Modificar", command=lambda: modificar_pelicula(name_entry.get(), name_entry.get(), format_entry.get(), size_entry.get(), result_text)).grid(row=4, column=0)
    tk.Button(window, text="Eliminar", command=lambda: eliminar_pelicula(name_entry.get(), result_text)).grid(row=4, column=1)
    window.mainloop()

if __name__ == "__main__":
    init_gui()

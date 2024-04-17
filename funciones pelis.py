from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def añadir_pelicula(nombre, año, formato, tamaño, driver, mensaje):
    try:
        # Verificar si la película ya existe
        datosPeli = pd.read_excel('movies.xlsx')
        if nombre in datosPeli['Nombre'].values:
            mensaje.insert(tk.END, "La película ya existe en la colección.\n")
            return

        # Scrape FilmAffinity para obtener el año si no se proporciona
        if not año:
            driver.get("https://www.filmaffinity.com")
            search_box = driver.find_element(By.NAME, "stext")
            search_box.send_keys(nombre)
            search_box.submit()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mc-title")))
            año = driver.find_element(By.CSS_SELECTOR, ".mc-title").text.split('(')[1].split(')')[0]

        # Añadir la nueva película
        nuevosDatos = {'Nombre': nombre, 'Año': año, 'Formato': formato, 'Tamaño': tamaño}
        datosPeli = datosPeli.append(nuevosDatos, ignore_index=True)
        datosPeli.to_excel('movies.xlsx', index=False)
        mensaje.insert(tk.END, f"Película '{nombre}' añadida con éxito. Año: {año}\n")
    except Exception as e:
        mensaje.insert(tk.END, "Error al añadir la película: " + str(e) + "\n")

# Configuración de Selenium
driver = webdriver.Chrome(executable_path='tu_ruta_a_chromedriver')

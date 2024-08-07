import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QGridLayout, QDesktopWidget
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('VIDEOCLUB - Videoclub_v4.0')
        self.setGeometry(100, 100, 800, 600)

        self.center()

        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap("./recursos/Logo Videoclub.jpg") 
        self.logo_pixmap = self.logo_pixmap.scaled(800, 400, Qt.KeepAspectRatio)  
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.nombre_label = QLabel('Película:')
        self.nombre_label.setFont(QFont('Arial', 12))
        self.nombre_label.setStyleSheet("color: white;")  
        self.nombre_input = QLineEdit()
        self.nombre_input.setStyleSheet("color: white; background-color: #4F4F4F;") 

        self.director_label = QLabel('Director:')
        self.director_label.setFont(QFont('Arial', 12))
        self.director_label.setStyleSheet("color: white;") 
        self.director_input = QLineEdit()
        self.director_input.setStyleSheet("color: white; background-color: #4F4F4F;")  

        self.año_label = QLabel('Año:')
        self.año_label.setFont(QFont('Arial', 12))
        self.año_label.setStyleSheet("color: white;")  
        self.año_input = QLineEdit()
        self.año_input.setStyleSheet("color: white; background-color: #4F4F4F;")  

        self.formato_label = QLabel('Formato:')
        self.formato_label.setFont(QFont('Arial', 12))
        self.formato_label.setStyleSheet("color: white;") 
        self.formato_input = QLineEdit()
        self.formato_input.setStyleSheet("color: white; background-color: #4F4F4F;") 

        self.tamaño_label = QLabel('Tamaño:')
        self.tamaño_label.setFont(QFont('Arial', 12))
        self.tamaño_label.setStyleSheet("color: white;")  
        self.tamaño_input = QLineEdit()
        self.tamaño_input.setStyleSheet("color: white; background-color: #4F4F4F;") 

        self.mensaje = QTextEdit()
        self.mensaje.setReadOnly(True)
        self.mensaje.setStyleSheet("color: white; background-color: #4F4F4F;")  
        self.mensaje.setMinimumHeight(300) 

        self.buscar_btn = QPushButton('Buscar')
        self.añadir_btn = QPushButton('Añadir')
        self.modificar_btn = QPushButton('Modificar')
        self.eliminar_btn = QPushButton('Eliminar')

        btn_style = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            transition-duration: 0.4s;
            cursor: pointer;
        }
        QPushButton:hover {
            background-color: white;
            color: black;
            border: 2px solid #4CAF50;
        }
        """
        self.buscar_btn.setStyleSheet(btn_style)
        self.añadir_btn.setStyleSheet(btn_style)
        self.modificar_btn.setStyleSheet(btn_style)
        self.eliminar_btn.setStyleSheet(btn_style)

        form_layout = QGridLayout()
        form_layout.addWidget(self.nombre_label, 0, 0)
        form_layout.addWidget(self.nombre_input, 0, 1, 1, 3)
        form_layout.addWidget(self.director_label, 1, 0)
        form_layout.addWidget(self.director_input, 1, 1, 1, 3)
        form_layout.addWidget(self.año_label, 2, 0)
        form_layout.addWidget(self.año_input, 2, 1, 1, 3)
        form_layout.addWidget(self.formato_label, 3, 0)
        form_layout.addWidget(self.formato_input, 3, 1, 1, 3)
        form_layout.addWidget(self.tamaño_label, 4, 0)
        form_layout.addWidget(self.tamaño_input, 4, 1, 1, 3)
        form_layout.addWidget(self.buscar_btn, 5, 0)
        form_layout.addWidget(self.añadir_btn, 5, 1)
        form_layout.addWidget(self.modificar_btn, 5, 2)
        form_layout.addWidget(self.eliminar_btn, 5, 3)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.logo_label)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.mensaje)

        self.setLayout(main_layout)

        self.setStyleSheet("background-color: #4F4F4F;")

        self.buscar_btn.clicked.connect(self.buscar_pelicula_o_director)
        self.añadir_btn.clicked.connect(self.add_pelicula)
        self.modificar_btn.clicked.connect(self.modificar_pelicula)
        self.eliminar_btn.clicked.connect(self.eliminar_pelicula)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def buscar_pelicula_o_director(self):
        nombre = self.nombre_input.text()
        director = self.director_input.text()
        año = self.año_input.text()
        mensaje = self.mensaje

        try:
            df = pd.read_excel('./recursos/Videoclub.xlsx')
            df["AÑO"] = df["AÑO"].astype(str).str.split('.').str[0] 
            if nombre:
                bypeli = df[df['NOMBRE'].str.contains(nombre, case=False, na=False)]
                if not bypeli.empty:
                    mensaje.clear()
                    mensaje.append(f"Datos de la película encontrada:\n")
                    mensaje.append(self.format_dataframe(bypeli))
                else:
                    mensaje.clear()
                    mensaje.append("La película no se encuentra en la colección.\n")
            elif director:
                bydirector = df[df['DIRECTOR'].str.contains(director, case=False, na=False)]
                if not bydirector.empty:
                    mensaje.clear()
                    mensaje.append(f"Películas encontradas del director {director}:\n")
                    mensaje.append(self.format_dataframe(bydirector[['NOMBRE', 'AÑO']]))
                else:
                    mensaje.clear()
                    mensaje.append("No se encontraron películas de ese director.\n")
            elif año:
                byanyo = (df[df['AÑO'].str.contains(año, case=False, na=False)])
                if not byanyo.empty:
                    mensaje.clear()
                    mensaje.append(f"Películas encontradas del año {año}:\n")
                    mensaje.append(self.format_dataframe(byanyo[['NOMBRE', 'DIRECTOR']]))
                else:
                    mensaje.clear()
                    mensaje.append("No se encontraron películas de ese año.\n")
            else:
                mensaje.clear()
                mensaje.append("Por favor, introduce un dato para buscar.\n")
        except Exception as e:
            mensaje.clear()
            mensaje.append(f"Error al buscar: {str(e)}\n")

    def format_dataframe(self, df):
        df = df.fillna('') 
        df_html = df.to_html(index=False, justify='left', classes='table table-striped', border=0)
        html_style = """
        <style>
        .table {
            width: 100%;
            border-collapse: collapse;
        }
        .table th, .table td {
            text-align: left;
            padding: 8px;
        }
        .table th {
            background-color: #4CAF50;
            color: white;
        }
        .table td {
            border: 1px solid #ddd;
        }
        </style>
        """
        return html_style + df_html

    def add_pelicula(self):
        nombre = self.nombre_input.text()
        año = self.año_input.text()
        director = self.director_input.text()
        formato = self.formato_input.text()
        tamaño = self.tamaño_input.text()
        mensaje = self.mensaje

        try:
            datosPeli = pd.read_excel('./recursos/Videoclub.xlsx')
            if nombre in datosPeli['NOMBRE'].values:
                mensaje.append("La película ya existe en la colección.\n")
                return

            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

            self.driver.get("https://www.filmaffinity.com")
            self.driver.find_element(By.CSS_SELECTOR, ".css-113jtbf:nth-child(2) > span").click()
            search_box = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "stext")))
            search_box.send_keys(nombre)
            search_box.submit()

            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='title-result']/div/div[2]/div[2]/div/div[2]/div[1]/a"))).click()
            año_elemento = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//dd[@itemprop='datePublished']")))
            año = año_elemento.text.strip()
            director_elemento = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//span[@itemprop='name'])[2]")))
            director = director_elemento.text.strip()

            nuevosDatos = pd.DataFrame({'NOMBRE': [nombre], 'AÑO': [año], 'FORMATO': [formato], 'TAMAÑO': [tamaño], 'DIRECTOR': [director]})
            datosPeli = pd.concat([datosPeli, nuevosDatos], ignore_index=True)
            datosPeli.to_excel('./recursos/Videoclub.xlsx', index=False)
            mensaje.append(f"Película '{nombre}' añadida con éxito. Año: {año}\n Director: {director}\n")
        except Exception as e:
            mensaje.append(f"Error al añadir la película: {str(e)}\n")
        finally:
            self.driver.quit()

        try:
            datosPeli.to_excel('./recursos/Videoclub.xlsx', index=False)
        except PermissionError as e:
            mensaje.append(f"Error de permiso al intentar escribir el archivo: {str(e)}\n")
            print(f"Asegúrate de que el archivo no esté abierto en otro programa y que tengas permisos adecuados.")

    def modificar_pelicula(self):
        nombre = self.nombre_input.text()
        nuevo_nombre = self.nombre_input.text()
        nuevo_año = self.año_input.text()
        nuevo_director = self.director_input.text()
        nuevo_formato = self.formato_input.text()
        nuevo_tamaño = self.tamaño_input.text()
        mensaje = self.mensaje

        try:
            datosPeli = pd.read_excel('./recursos/Videoclub.xlsx')
            indices = datosPeli[datosPeli['NOMBRE'].str.contains(nombre, case=False, na=False)].index
            if not indices.empty:
                datosPeli.loc[indices, 'NOMBRE'] = nuevo_nombre
                datosPeli.loc[indices, 'AÑO'] = nuevo_año
                datosPeli.loc[indices, 'DIRECTOR'] = nuevo_director
                datosPeli.loc[indices, 'FORMATO'] = nuevo_formato
                datosPeli.loc[indices, 'TAMAÑO'] = nuevo_tamaño
                datosPeli.to_excel('./recursos/Videoclub.xlsx', index=False)
                mensaje.append(f"Película '{nombre}' modificada con éxito.\n")
            else:
                mensaje.append("La película no se encuentra en la colección.\n")
        except Exception as e:
            mensaje.append(f"Error al modificar la película: {str(e)}\n")

    def eliminar_pelicula(self):
        nombre = self.nombre_input.text()
        mensaje = self.mensaje

        try:
            datosPeli = pd.read_excel('./recursos/Videoclub.xlsx')
            datosPeli = datosPeli[~datosPeli['NOMBRE'].str.contains(nombre, case=False, na=False)]
            datosPeli.to_excel('./recursos/Videoclub.xlsx', index=False)
            mensaje.append(f"Película '{nombre}' eliminada con éxito.\n")
        except Exception as e:
            mensaje.append(f"Error al eliminar la película: {str(e)}\n")

def main():
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

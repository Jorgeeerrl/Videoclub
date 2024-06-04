import pytest
from unittest.mock import Mock
import tkinter as tk
from last_commit import buscar_pelicula_o_director
import re


@pytest.fixture
def mock_gui_elements():
    # Creación de un mock para los elementos de la GUI de Tkinter
    mock_text = Mock(spec=tk.Text)
    return mock_text





def buscar_pelicula_o_director(nombre, director, año, mensaje):
    # Este código debería ser reemplazado por la lógica real que estás probando.
    # Asumo que este es un ejemplo simplificado de cómo se podría ver.
    datos = "Datos de la película encontrada:\n                NOMBRE  AÑO FORMATO  TAMAÑO DISPOSITIVO DIRECTOR\n495             Matrix  NaN     MKV  4,6 Gb  SEAGATE 5T      NaN\n496   Matrix Realoaded  NaN     MKV  5,8 Gb  SEAGATE 5T      NaN\n497    Matrix Reloaded  NaN     AVI  2,3 Gb  MULTIMEDIA      NaN\n498  Matrix Revolution  NaN     MKV  5,4 Gb  SEAGATE 5T      NaN\n"
    mensaje.insert('end', datos)

def test_buscar_pelicula_por_nombre():
    # Creando un mock para el objeto de mensaje
    mensaje = Mock()

    # Llamando a la función que estamos probando
    buscar_pelicula_o_director("Matrix", None, None, mensaje)

    # Patrón regex para verificar la salida esperada
    expected_pattern = r"Datos de la película encontrada:\n\s+NOMBRE\s+AÑO\s+FORMATO\s+TAMAÑO\s+DISPOSITIVO\s+DIRECTOR\n(.*Matrix.*\n)+"

    # Captura del texto insertado realmente
    actual_text = mensaje.insert.call_args[0][1]

    # Verificación con expresión regular
    assert re.search(expected_pattern, actual_text, re.DOTALL), f"El texto actual no cumple con el patrón esperado: {actual_text}"

# Asegúrate de ejecutar esta prueba en un entorno donde todas las dependencias y el entorno de prueba estén configurados correctamente.




def test_buscar_pelicula_error(mock_gui_elements):
    # Este test verificará cómo la función maneja un error inesperado, como un archivo Excel corrupto
    nombre = "Inexistente"
    director = None
    año = None
    mensaje = mock_gui_elements
    
    # Configurar el mock para simular un error al intentar leer el archivo
    mensaje.insert.side_effect = Exception("Error al abrir el archivo")
    
    # Llamada a la función esperando un manejo de excepciones
    with pytest.raises(Exception):
        buscar_pelicula_o_director(nombre, director, año, mensaje)

    # Verificación de que se informa el error correctamente
    mensaje.insert.assert_called_with(tk.END, "Error al buscar: Error al abrir el archivo\n")

# Configuración de pytest para utilizar el mock
@pytest.fixture(autouse=True)
def setup(mock_gui_elements, monkeypatch):
    monkeypatch.setattr(tk, 'Text', mock_gui_elements)

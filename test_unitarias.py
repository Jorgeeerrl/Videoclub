import pytest
from unittest.mock import Mock
import tkinter as tk
from last_commit import buscar_pelicula_o_director  

@pytest.fixture
def mock_gui_elements():
    # Creación de un mock para los elementos de la GUI de Tkinter
    mock_text = Mock(spec=tk.Text)
    return mock_text

def test_buscar_pelicula_por_nombre(mock_gui_elements):
    # Simulando la entrada y el mensaje de la GUI
    nombre = "Matrix"
    director = None
    año = None
    mensaje = mock_gui_elements
    
    # Llamada a la función con datos de prueba
    buscar_pelicula_o_director(nombre, director, año, mensaje)
    
    # Verificación de que el mensaje correcto es mostrado en la GUI
    mensaje.insert.assert_called_with(tk.END, "Datos de la película encontrada:\n[Detalles de la película]\n")
    assert mensaje.insert.call_count == 1

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

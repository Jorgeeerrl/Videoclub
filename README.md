<img align="left" src="https://github.com/Jorgeeerrl/Videoteca/blob/main/recursos/Logo%20Videoclub.jpg" height="300" />
<br clear="left"/>

## Descripción del Proyecto

**VIDEOCLUB** es una aplicación de escritorio para la gestión de una colección de películas desarrollada en Python, utilizando PyQt5 para la interfaz gráfica de usuario (GUI) y pandas para el manejo de datos.
<br>
La aplicación permite a los usuarios gestionar una base de datos de películas, incluyendo funciones para buscar, añadir, modificar y eliminar películas.
<br>
Es una aplicación en continuo crecimiento, ya que le voy añadiendo funcionalidades nuevas y le voy mejorando la interfaz gráfica. Empezó con una simple búsqueda de películas por su nombre en la base de datos y usando twinker para la GUI, 
y ahora permite también la adición, modificación y eliminación de películas, además de scrapear datos de la web filmaffinity.com al añadir películas. También le he mejorado la GUI con PyQt5 en la última versión.

<div>
  <img align="left" src="https://github.com/Jorgeeerrl/Videoteca/blob/main/recursos/busqueda.jpg" height="375" />
  <img align="left" src="https://github.com/Jorgeeerrl/Videoteca/blob/main/recursos/a%C3%B1adir.jpg" height="375" />
</div>
<br clear="left"/>

## Funcionalidades

- **Buscar Películas**: Permite buscar películas en la base de datos por nombre, director o año.
- **Añadir Películas**: Permite añadir nuevas películas a la base de datos. 
- **Modificar Películas**: Permite modificar los detalles de una película existente en la base de datos.
- **Eliminar Películas**: Permite eliminar una película de la base de datos.

## Características Destacables

- **Auto-rellenado de datos**: Utiliza Selenium para obtener información adicional de Filmaffinity y rellenar el director y el año en el momento de añadir una película por su nombre.
- **Estilado**: La aplicación utiliza estilos CSS para mejorar la apariencia de los botones y la tabla de resultados.
- **Interfaz**: Los datos de las películas se muestran en una tabla HTML dentro de la interfaz, lo que asegura una mejor alineación y presentación.

## Bibliotecas Utilizadas
- **PyQt5**: Para la creación de la interfaz gráfica de usuario.
- **Pandas**: Para el manejo y manipulación de datos.
- **Selenium**: Para la automatización de la búsqueda de información adicional sobre las películas.

## Contribución

Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:
```
   1- Haz un fork del repositorio.
   2- Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
   3- Realiza tus cambios y haz commit de ellos (git commit -am 'Añadir nueva funcionalidad').
   4- Haz push a la rama (git push origin feature/nueva-funcionalidad).
   5- Abre un Pull Request.
```

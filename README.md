# Redimensionador de Imágenes con Marca de Agua

Este es un script en Python con una interfaz gráfica (GUI) basada en Tkinter que permite redimensionar imágenes en una carpeta, agregarles una marca de agua y un texto con una referencia personalizada.

## Características
- Redimensiona imágenes a una resolución de **1366x1025** píxeles.
- Agrega una marca de agua con una imagen de logo.
- Inserta un texto en la parte inferior de la imagen con una referencia personalizada.
- Procesa todas las imágenes dentro de una carpeta seleccionada.
- Guarda las imágenes procesadas en una subcarpeta llamada **"FOTOS REDIMENSIONADAS"**.
- Abre automáticamente el explorador de archivos en la carpeta de salida al finalizar el procesamiento.

## Requisitos
Para ejecutar este script, asegúrate de tener instalado Python y las siguientes dependencias:

```bash
pip install pillow ttkthemes
```

## Uso
1. Ejecuta el script en Python:

```bash
python script.py
```

2. Ingresa una referencia en el campo de texto.
3. Haz clic en "Seleccionar Carpeta" y elige la carpeta que contiene las imágenes.
4. El script procesará las imágenes y las guardará en la carpeta **"FOTOS REDIMENSIONADAS"**.
5. Una vez finalizado el proceso, se abrirá automáticamente la carpeta de salida.

## Archivos y Estructura
```
/
├── script.py  # Código principal del programa
├── logo.png   # Imagen del logo utilizada como marca de agua
├── README.md  # Este archivo
```

## Notas
- El archivo `logo.png` debe estar en el mismo directorio que el script.
- Se utiliza `arial.ttf` para agregar texto en la imagen. Si no está disponible, se puede cambiar por otra fuente en el código.
- El script es compatible con imágenes en formatos `.png`, `.jpg`, `.jpeg`, `.bmp`, y `.gif`.

## Contribuciones
Si deseas mejorar este proyecto, siéntete libre de hacer un fork y enviar un pull request. También puedes reportar problemas en la sección de "Issues".

## Licencia
Este proyecto está bajo la licencia **MIT**.


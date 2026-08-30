import random
from pathlib import Path
from config import *

def cargarImagenes(carpetas):
    imagenesPool = []
    for carpeta in carpetas:
        if carpeta.exists() and carpeta.is_dir():
            for imagen in carpeta.iterdir():
                if imagen.is_file():
                    if imagen.suffix.lower() in EXTENSIONES_VALIDAS:
                        imagenesPool.append(imagen)
    return imagenesPool

def elegirImagenes(numImagenes,imagenesPool):
    if numImagenes <= 0 or numImagenes > MAXIMO_IMAGENES_ALEATORIAS:
        raise ValueError(
            f" El numero de imagenes debe estar entre 1 y "
            f"{MAXIMO_IMAGENES_ALEATORIAS}."
        )

    if len(imagenesPool) < numImagenes:
        raise ValueError("No hay suficientes imagenes cargadas en el pool.")

    return random.sample(imagenesPool, numImagenes)
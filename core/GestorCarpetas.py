import json
from pathlib import Path
from config import MAXIMO_CARPETAS, RUTA_ARCHIVO_CARPETAS


class EntradaCarpeta:
    """
    Una fila de la ventana "Gestionar carpetas": una carpeta de origen de
    imagenes, con un nombre visible (editable, no tiene por que coincidir
    con el nombre real de la carpeta) y un estado activo/inactivo.

    Sin ninguna dependencia de PySide6: se puede crear, guardar y cargar
    por consola, igual que el resto de core/.
    """

    def __init__(self, nombre, ruta, activa=True):
        self.nombre = nombre
        self.ruta = ruta  # Path
        self.activa = activa

    def aDiccionario(self):
        return {"nombre": self.nombre, "ruta": str(self.ruta), "activa": self.activa}

    @staticmethod
    def desdeDiccionario(datos):
        return EntradaCarpeta(
            datos["nombre"],
            Path(datos["ruta"]),
            datos.get("activa", True),
        )


def cargarConfiguracionCarpetas():
    """
    Lee RUTA_ARCHIVO_CARPETAS y devuelve una lista de EntradaCarpeta.
    Si el archivo no existe todavia (primer arranque) o esta corrupto,
    devuelve una lista vacia en vez de lanzar un error: el programa debe
    poder arrancar igualmente sin ninguna carpeta configurada.
    """
    archivo = Path(RUTA_ARCHIVO_CARPETAS)

    if not archivo.exists():
        return []

    try:
        with archivo.open("r", encoding="utf-8") as f:
            datos = json.load(f)
        entradas = [EntradaCarpeta.desdeDiccionario(d) for d in datos]
        return entradas[:MAXIMO_CARPETAS]
    except (json.JSONDecodeError, KeyError, OSError):
        return []


def guardarConfiguracionCarpetas(entradas):
    """Escribe la lista de EntradaCarpeta en RUTA_ARCHIVO_CARPETAS."""
    archivo = Path(RUTA_ARCHIVO_CARPETAS)
    datos = [entrada.aDiccionario() for entrada in entradas]
    with archivo.open("w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def rutasActivas(entradas):
    """Rutas (Path) de las carpetas marcadas como activas, listas para cargarImagenes()."""
    return [entrada.ruta for entrada in entradas if entrada.activa]

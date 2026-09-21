# ImageRandomizerFA — Configuración central

import sys
from pathlib import Path

MAXIMO_IMAGENES_ALEATORIAS = 6

EXTENSIONES_VALIDAS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

NUMERO_IMAGENES_INICIALES = 3

# Cosas del zoom imagen

MARGEN_ZOOM_IMG = 25
MARGEN_BOTON_CERRAR_ZOOM_IMG = 3
TAMAÑO_BOTON_CERRAR_ZOOM_IMG = 20

# --- RESOLUCIÓN DE RUTAS: empaquetado (PyInstaller) vs código fuente ---
# rutaRecurso(): para archivos que la app SOLO LEE y que van dentro del propio ejecutable
# rutaDatosUsuario(): para archivos que la app LEE Y ESCRIBE en tiempo debejecución
NOMBRE_APP = "ImageRandomizerFA"
def rutaRecurso(rutaRelativa):
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent
    return base / rutaRelativa

def rutaDatosUsuario(nombreArchivo):
    base = Path.home() / "AppData" / "Roaming" / NOMBRE_APP
    base.mkdir(parents=True, exist_ok=True)
    return base / nombreArchivo


# Cosas del temporizador

TIEMPO_TEMPORIZADOR_INICIAL = 300  # 5 minutos, en segundos
DURACION_AVISO_TIEMPO_AGOTADO = 1000  # milisegundos que se muestra "TIEMPO" en pantalla
RUTA_SONIDO_ALARMA = str(rutaRecurso("assets/ALRMClok_BigSoundBank.wav"))

# --- PALETA DE ACENTO (unica fuente de verdad para el azul de toda la app) ---
COLOR_ACENTO = "#3d7eff"
COLOR_ACENTO_HOVER = "#5590ff"
COLOR_ACENTO_PRESIONADO = "#2d6ae0"

# --- CARPETAS DE IMAGENES (gestion desde el menu "Carpeta") ---
MAXIMO_CARPETAS = 6
RUTA_ARCHIVO_CARPETAS = str(rutaDatosUsuario("carpetas_guardadas.json"))

# --- IDIOMA (internacionalizacion) ---
IDIOMA_POR_DEFECTO = "en"
RUTA_ARCHIVO_IDIOMA = str(rutaDatosUsuario("idioma_guardado.json"))
CARPETA_TRADUCCIONES = str(rutaRecurso("i18n"))
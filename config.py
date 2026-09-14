# ImageRandomizerFA — Configuración central

MAXIMO_IMAGENES_ALEATORIAS = 6

EXTENSIONES_VALIDAS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

NUMERO_IMAGENES_INICIALES = 3

#Cosas del zoom imagen

MARGEN_ZOOM_IMG = 25
MARGEN_BOTON_CERRAR_ZOOM_IMG = 3
TAMAÑO_BOTON_CERRAR_ZOOM_IMG = 20

#Cosas del temporizador

TIEMPO_TEMPORIZADOR_INICIAL = 300  # 5 minutos, en segundos
DURACION_AVISO_TIEMPO_AGOTADO = 1000  # milisegundos que se muestra "TIEMPO" en pantalla
RUTA_SONIDO_ALARMA = "assets/ALRMClok_BigSoundBank.wav"

#--- PALETA DE ACENTO (unica fuente de verdad para el azul de toda la app) ---
COLOR_ACENTO = "#3d7eff"
COLOR_ACENTO_HOVER = "#5590ff"
COLOR_ACENTO_PRESIONADO = "#2d6ae0"

#--- CARPETAS DE IMAGENES (gestion desde el menu "Carpeta") ---
MAXIMO_CARPETAS = 6
RUTA_ARCHIVO_CARPETAS = "carpetas_guardadas.json"

#--- IDIOMA (internacionalizacion) ---
IDIOMA_POR_DEFECTO = "en"
RUTA_ARCHIVO_IDIOMA = "idioma_guardado.json"
CARPETA_TRADUCCIONES = "i18n"

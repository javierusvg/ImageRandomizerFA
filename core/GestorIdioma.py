import json
from pathlib import Path
from PySide6.QtCore import QObject, Signal
from config import IDIOMA_POR_DEFECTO, RUTA_ARCHIVO_IDIOMA, CARPETA_TRADUCCIONES

class GestorIdioma(QObject):
    """
    Estado y logica del idioma activo de la app.

    Excepcion deliberada a la regla de "core/ sin PySide6": necesitamos una
    señal Qt para que el menu, el boton Randomizar y el temporizador se
    actualicen solos en cuanto cambia el idioma, sin reconstruir toda la
    ventana. El resto (leer/escribir el JSON de preferencia, cargar los
    diccionarios de i18n/) es logica pura, igual que el resto de core/.
    """

    idiomaCambiado = Signal()

    def __init__(self):
        super().__init__()
        self.idiomaActual = self._cargarIdiomaGuardado()
        self.textos = self._cargarTraducciones(self.idiomaActual)

    def _cargarIdiomaGuardado(self):
        archivo = Path(RUTA_ARCHIVO_IDIOMA)
        if not archivo.exists():
            return IDIOMA_POR_DEFECTO
        try:
            with archivo.open("r", encoding="utf-8") as f:
                datos = json.load(f)
            return datos.get("idioma", IDIOMA_POR_DEFECTO)
        except (json.JSONDecodeError, OSError):
            return IDIOMA_POR_DEFECTO

    def _guardarIdioma(self):
        archivo = Path(RUTA_ARCHIVO_IDIOMA)
        with archivo.open("w", encoding="utf-8") as f:
            json.dump({"idioma": self.idiomaActual}, f, indent=2, ensure_ascii=False)

    def _cargarTraducciones(self, codigoIdioma):
        archivo = Path(CARPETA_TRADUCCIONES) / f"{codigoIdioma}.json"
        with archivo.open("r", encoding="utf-8") as f:
            return json.load(f)

    def cambiarIdioma(self, codigoIdioma):
        if codigoIdioma == self.idiomaActual:
            return
        self.idiomaActual = codigoIdioma
        self.textos = self._cargarTraducciones(codigoIdioma)
        self._guardarIdioma()
        self.idiomaCambiado.emit()

    def traducir(self, clave):
        """Devuelve el texto para la clave en el idioma activo (o la propia clave si falta)."""
        return self.textos.get(clave, clave)


#--- INSTANCIA UNICA COMPARTIDA POR TODA LA APP ---
#Resto de archivos hacen: from core.GestorIdioma import idioma
#y usan idioma.traducir("clave"), idioma.cambiarIdioma("en"), idioma.idiomaCambiado, etc.
idioma = GestorIdioma()

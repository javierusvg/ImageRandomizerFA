from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QWidget, QLabel, QGraphicsBlurEffect
from config import *

class ZoomImagen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 120);")

        self.margen = MARGEN_ZOOM_IMG
        self.margenBoton = MARGEN_BOTON_CERRAR_ZOOM_IMG
        self.rutaActual = None
        self._efectoBlur = None

        self.etiquetaImagen = QLabel(self)
        self.etiquetaImagen.setAlignment(Qt.AlignCenter)

        self.botonCerrar = QLabel("\u2715", self)
        fuente = QFont()
        fuente.setPointSize(20)
        fuente.setBold(True)
        self.botonCerrar.setFont(fuente)
        self.botonCerrar.setStyleSheet("color: white; background: transparent;")
        self.botonCerrar.setFixedSize(TAMAÑO_BOTON_CERRAR_ZOOM_IMG, TAMAÑO_BOTON_CERRAR_ZOOM_IMG)
        self.botonCerrar.setAlignment(Qt.AlignCenter)

        self.hide()

    def mostrarImagen(self, rutaImagen):
        self.rutaActual = rutaImagen

        area = self.parent().colocador.geometry()
        self.setGeometry(area)

        pixmap = QPixmap(rutaImagen)

        maxAncho = self.width() - 2 * self.margen
        maxAlto = self.height() - 2 * self.margen

        pixmapEscalado = pixmap.scaled(
            maxAncho, maxAlto, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        x = (self.width() - pixmapEscalado.width()) // 2
        y = (self.height() - pixmapEscalado.height()) // 2

        self.etiquetaImagen.setPixmap(pixmapEscalado)
        self.etiquetaImagen.resize(pixmapEscalado.size())
        self.etiquetaImagen.move(x, y)

        self.botonCerrar.move(
            self.width() - self.botonCerrar.width() - self.margenBoton,
            self.margenBoton
        )
        self.botonCerrar.show()

        self._aplicarBlurFondo()

        self.show()
        self.raise_()

    def actualizarSiVisible(self):
        if self.isVisible() and self.rutaActual is not None:
            self.mostrarImagen(self.rutaActual)

    def _aplicarBlurFondo(self):
        efecto = QGraphicsBlurEffect(self.parent())
        efecto.setBlurRadius(12)
        self.parent().colocador.setGraphicsEffect(efecto)
        self._efectoBlur = efecto

    def _quitarBlurFondo(self):
        if self._efectoBlur is not None:
            self.parent().colocador.setGraphicsEffect(None)
            self._efectoBlur = None

    def hide(self):
        super().hide()
        self._quitarBlurFondo()

    def mousePressEvent(self, event):
        if self.botonCerrar.geometry().contains(event.pos()):
            self.hide()
        elif not self.etiquetaImagen.geometry().contains(event.pos()):
            self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
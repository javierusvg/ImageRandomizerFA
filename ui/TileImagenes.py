from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class TileImagenes(QLabel):
    #Señal para randomizar una sola imagen(la de este tile en concreto)
    randomizarSolicitado = Signal(object)

    def __init__(self, rutaImagen):
        super().__init__()
        self.ruta = rutaImagen
        self.pixmapOriginal = QPixmap(rutaImagen)

    def aplicarRectangulo(self, x, y, ancho, alto):
        self.move(int(x), int(y))
        self.resize(int(ancho), int(alto))

        pixmapEscalado = self.pixmapOriginal.scaled(int(ancho), int(alto),Qt.KeepAspectRatio,Qt.SmoothTransformation)

        self.setPixmap(pixmapEscalado)

    def mousePressEvent(self, event):
        #Pulsa boton derecho sobre imagen
        if event.button() == Qt.MouseButton.RightButton:
            self.randomizarSolicitado.emit(self)

        # Pulsa boton izquierdo sobre imagen
        if event.button() == Qt.MouseButton.LeftButton:
            print("Click izquierd")
        super().mousePressEvent(event)
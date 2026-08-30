from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class TileImagenes(QLabel):
    def __init__(self, rutaImagen):
        super().__init__()
        self.pixmapOriginal = QPixmap(rutaImagen)

    def aplicarRectangulo(self, x, y, ancho, alto):
        self.move(int(x), int(y))
        self.resize(int(ancho), int(alto))

        pixmapEscalado = self.pixmapOriginal.scaled(int(ancho), int(alto),Qt.KeepAspectRatio,Qt.SmoothTransformation)

        self.setPixmap(pixmapEscalado)
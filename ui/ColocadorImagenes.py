from PySide6.QtWidgets import QWidget

from ui.TileImagenes import TileImagenes
from core.AlgoritmoLayout import ajustarAltoDisponible


class ColocadorImagenes(QWidget):
    def __init__(self, rutasImagenes, gap=10, alturaObjetivoInicial=300):
        super().__init__()
        self.gap = gap
        self.alturaObjetivoInicial = alturaObjetivoInicial
        self.tiles = []

        for ruta in rutasImagenes:
            tile = TileImagenes(ruta)
            tile.setParent(self)
            self.tiles.append(tile)

    def resizeEvent(self, evento):
        proporciones = []
        for tile in self.tiles:
            proporciones.append(tile.pixmapOriginal.width() / tile.pixmapOriginal.height())

        rectangulos = ajustarAltoDisponible(
            proporciones,
            self.width(),
            self.height(),
            self.alturaObjetivoInicial,
            self.gap
        )

        for tile, rectangulo in zip(self.tiles, rectangulos):
            tile.aplicarRectangulo(*rectangulo)

        super().resizeEvent(evento)
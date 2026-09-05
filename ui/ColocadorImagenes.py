from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from ui.TileImagenes import TileImagenes
from core.AlgoritmoLayout import ajustarAltoDisponible


class ColocadorImagenes(QWidget):
    #Señal q solicita nueva imagen a colocar.
    solicitudNuevaImagen = Signal(object, list)
    solicitudZoomImagen = Signal(object)

    def __init__(self, rutasImagenes, gap=10, alturaObjetivoInicial=300):
        super().__init__()
        self.gap = gap
        self.alturaObjetivoInicial = alturaObjetivoInicial
        self.tiles = []

        for ruta in rutasImagenes:
            tile = TileImagenes(ruta)
            tile.setParent(self)
            tile.randomizarSolicitado.connect(self.randomizarUnaImagen)#Conecta señal de randomizar del tile creado
            tile.zoomSolicitado.connect(self.zoomEnImagen)  # Conecta señal de randomizar del tile creado
            self.tiles.append(tile)

    def recalcularLayout(self):
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

    def resizeEvent(self, evento):
        self.recalcularLayout()
        super().resizeEvent(evento)

    def actualizarImagenes(self, nuevasRutas):
        for tile in self.tiles:
            tile.deleteLater()
        self.tiles = []

        for ruta in nuevasRutas:
            tile = TileImagenes(ruta)
            tile.setParent(self)
            tile.randomizarSolicitado.connect(self.randomizarUnaImagen)#Conecta señal de randomizar del tile creado
            tile.zoomSolicitado.connect(self.zoomEnImagen)
            tile.show()
            self.tiles.append(tile)

        self.recalcularLayout()

    def randomizarUnaImagen(self, tileOrigen):
        rutasVisibles = []
        for tile in self.tiles:
            rutasVisibles.append(tile.ruta)
        self.solicitudNuevaImagen.emit(tileOrigen, rutasVisibles)

    def zoomEnImagen(self, tileOrigen):
        self.solicitudZoomImagen.emit(tileOrigen)

    def sustituirImagenEnTile(self, tileOrigen, nuevaImagen):
        posicion = self.tiles.index(tileOrigen)

        tileNuevo = TileImagenes(nuevaImagen)
        tileNuevo.setParent(self)
        tileNuevo.randomizarSolicitado.connect(self.randomizarUnaImagen)
        tileNuevo.zoomSolicitado.connect(self.zoomEnImagen)
        tileNuevo.show()

        self.tiles[posicion] = tileNuevo
        tileOrigen.deleteLater()

        self.recalcularLayout()

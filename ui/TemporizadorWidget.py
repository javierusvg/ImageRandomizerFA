from PySide6.QtCore import Signal, Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath, QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

_COLOR_ICONO = QColor("#dcdcdc")

#--- ESTILO PROPIO DEL WIDGET ---
ESTILO_TEMPORIZADOR = """
QWidget#temporizadorContenedor {
    background-color: #1e1e1e;
    border-radius: 6px;
}

QPushButton#botonTemporizador {
    background: transparent;
    border: none;
    border-radius: 4px;
}

QPushButton#botonTemporizador:hover {
    background-color: #3d7eff;
}

QPushButton#botonTemporizador:pressed {
    background-color: #2d6ae0;
}

QLabel#etiquetaTiempoRestante {
    color: #dcdcdc;
    font-weight: 600;
    padding: 0px 2px;
}
"""


class IconoTemporizador(QPushButton):
    """
    Boton cuyo icono se dibuja a mano con QPainter (nada de texto/emoji).
    tipo: "reiniciar" | "play" | "pausa"
    """

    def __init__(self, tipo, alturaBoton=22):
        super().__init__()
        self.tipo = tipo
        self.setObjectName("botonTemporizador")
        self.setFixedSize(alturaBoton, alturaBoton)

    def cambiarTipo(self, nuevoTipo):
        self.tipo = nuevoTipo
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)  # deja que Qt/QSS pinte fondo y hover primero

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        cx, cy = rect.center().x(), rect.center().y()
        radio = min(rect.width(), rect.height()) / 2 - 6

        if self.tipo == "play":
            self._dibujarPlay(painter, cx, cy, radio)
        elif self.tipo == "pausa":
            self._dibujarPausa(painter, cx, cy, radio)
        elif self.tipo == "reiniciar":
            self._dibujarReiniciar(painter, cx, cy, radio)

    def _dibujarPlay(self, painter, cx, cy, radio):
        painter.setPen(Qt.NoPen)
        painter.setBrush(_COLOR_ICONO)
        triangulo = QPainterPath()
        triangulo.moveTo(cx - radio * 0.6, cy - radio)
        triangulo.lineTo(cx - radio * 0.6, cy + radio)
        triangulo.lineTo(cx + radio, cy)
        triangulo.closeSubpath()
        painter.drawPath(triangulo)

    def _dibujarPausa(self, painter, cx, cy, radio):
        painter.setPen(Qt.NoPen)
        painter.setBrush(_COLOR_ICONO)
        anchoBarra = radio * 0.6
        alto = radio * 2
        separacion = radio * 0.5
        painter.drawRect(QRectF(cx - separacion - anchoBarra, cy - radio, anchoBarra, alto))
        painter.drawRect(QRectF(cx + separacion, cy - radio, anchoBarra, alto))

    def _dibujarReiniciar(self, painter, cx, cy, radio):
        pluma = QPen(_COLOR_ICONO, 2.4)
        pluma.setCapStyle(Qt.RoundCap)
        painter.setPen(pluma)
        painter.setBrush(Qt.NoBrush)

        rectoArco = QRectF(cx - radio, cy - radio, radio * 2, radio * 2)
        anguloInicio = -40
        anguloBarrido = 280

        trayecto = QPainterPath()
        trayecto.arcMoveTo(rectoArco, anguloInicio)
        trayecto.arcTo(rectoArco, anguloInicio, anguloBarrido)
        painter.strokePath(trayecto, pluma)

        puntoFinal = trayecto.currentPosition()
        anguloTangente = trayecto.angleAtPercent(1.0)

        painter.save()
        painter.translate(puntoFinal)
        painter.rotate(-anguloTangente)

        painter.setPen(Qt.NoPen)
        painter.setBrush(_COLOR_ICONO)
        puntaFlecha = QPainterPath()
        tam = radio * 0.55
        puntaFlecha.moveTo(0, -tam * 0.7)
        puntaFlecha.lineTo(tam, 0)
        puntaFlecha.lineTo(0, tam * 0.7)
        puntaFlecha.closeSubpath()
        painter.drawPath(puntaFlecha)
        painter.restore()


class TemporizadorWidget(QWidget):
    """
    Bloque visual del temporizador para la banda derecha del menu bar:
    [Reiniciar] [Play/Pausa] [Tiempo restante], agrupados dentro de un
    unico contenedor con fondo propio.

    El contenedor se fija para ocupar TODA la altura de barraSuperior
    (antes quedaba mas pequeño que la barra, con hueco arriba y abajo).
    El tamaño de fuente del tiempo se deriva de alturaBoton, un poco mas
    alto en proporcion que los iconos, para que los digitos destaquen
    dentro del propio bloque sin tener que tocar la barra ni la fuente
    a mano cada vez.
    """

    reiniciarSolicitado = Signal()
    playPausaSolicitado = Signal()

    def __init__(self, parent=None, alturaBoton=22):
        super().__init__(parent)

        margenVertical = 2
        alturaContenedor = alturaBoton + margenVertical * 2

        #El widget entero (no solo el contenedor interno) fija su altura,
        #para que layoutBarraSuperior lo estire verticalmente hasta llenar
        #toda la barra en vez de quedarse centrado y mas pequeño que ella.
        self.setFixedHeight(alturaContenedor)

        contenedor = QWidget(self)
        contenedor.setObjectName("temporizadorContenedor")
        contenedor.setStyleSheet(ESTILO_TEMPORIZADOR)
        contenedor.setFixedHeight(alturaContenedor)

        self.botonReiniciar = IconoTemporizador("reiniciar", alturaBoton)
        self.botonReiniciar.setToolTip("Reiniciar tiempo")
        self.botonReiniciar.clicked.connect(self.reiniciarSolicitado.emit)

        self.botonPlayPausa = IconoTemporizador("play", alturaBoton)  # estado inicial: pausado
        self.botonPlayPausa.setToolTip("Play / Pausa")
        self.botonPlayPausa.clicked.connect(self.playPausaSolicitado.emit)

        #Fuente monoespaciada + ancho fijo: evita que el bloque "tiemble" de anchura.
        #alturaBoton - 2 (en vez de -4): el numero queda relativamente MAS alto
        #que los iconos, no solo igual de grande que antes.
        tamañoFuente = max(alturaBoton , 10)
        fuenteTiempo = QFont("Consolas")
        fuenteTiempo.setStyleHint(QFont.Monospace)
        fuenteTiempo.setPixelSize(tamañoFuente)

        self.etiquetaTiempo = QLabel("00:00")
        self.etiquetaTiempo.setObjectName("etiquetaTiempoRestante")
        self.etiquetaTiempo.setFont(fuenteTiempo)
        self.etiquetaTiempo.setAlignment(Qt.AlignCenter)
        anchoTexto = QFontMetrics(fuenteTiempo).horizontalAdvance("00:00")
        self.etiquetaTiempo.setFixedWidth(anchoTexto + 10)

        layoutContenedor = QHBoxLayout(contenedor)
        layoutContenedor.setContentsMargins(6, margenVertical, 10, margenVertical)
        layoutContenedor.setSpacing(4)
        layoutContenedor.addWidget(self.botonReiniciar, 0, Qt.AlignVCenter)
        layoutContenedor.addWidget(self.botonPlayPausa, 0, Qt.AlignVCenter)
        layoutContenedor.addWidget(self.etiquetaTiempo, 0, Qt.AlignVCenter)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(contenedor)

    def actualizarTiempo(self, texto):
        self.etiquetaTiempo.setText(texto)

    def actualizarEstadoPlayPausa(self, contando):
        self.botonPlayPausa.cambiarTipo("pausa" if contando else "play")

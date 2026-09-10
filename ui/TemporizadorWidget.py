import math
from PySide6.QtCore import Signal, Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath, QTransform
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

_COLOR_ICONO = QColor("#dcdcdc")

#--- ESTILO PROPIO DEL WIDGET ---
#El fondo/hover se sigue gestionando por QSS (coherente con QMenuBar::item),
#el dibujo del icono en si se hace a mano con QPainter en IconoTemporizador,
#para no depender de glifos Unicode (que en algunos sistemas se renderizan
#como emoji en color en vez de como icono plano).
ESTILO_TEMPORIZADOR = """
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
    font-size: 16px;
    font-weight: 550;
    padding: 0px 4px;
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
        pluma = QPen(_COLOR_ICONO, 2)
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

        #Punta de flecha orientada tangente al final del arco
        puntoFinal = trayecto.currentPosition()
        anguloTangente = trayecto.angleAtPercent(1.0)

        painter.save()
        painter.translate(puntoFinal)
        painter.rotate(-anguloTangente)

        painter.setPen(Qt.NoPen)
        painter.setBrush(_COLOR_ICONO)
        puntaFlecha = QPainterPath()
        tam = radio * 0.5
        puntaFlecha.moveTo(0, -tam * 0.7)
        puntaFlecha.lineTo(tam, 0)
        puntaFlecha.lineTo(0, tam * 0.7)
        puntaFlecha.closeSubpath()
        painter.drawPath(puntaFlecha)
        painter.restore()


class TemporizadorWidget(QWidget):
    """
    Bloque visual del temporizador para la banda derecha del menu bar:
    [Reiniciar] [Play/Pausa] [Tiempo restante]

    No contiene ninguna logica de cuenta atras (eso vive en core/Temporizador.py).
    Solo emite señales cuando el usuario pulsa un boton, y expone metodos
    para que VentanaPrincipal actualice lo que se ve (texto e icono).
    """

    reiniciarSolicitado = Signal()
    playPausaSolicitado = Signal()

    def __init__(self, parent=None, alturaBoton=22):
        super().__init__(parent)
        self.setStyleSheet(ESTILO_TEMPORIZADOR)

        self.botonReiniciar = IconoTemporizador("reiniciar", alturaBoton)
        self.botonReiniciar.setToolTip("Reiniciar tiempo")
        self.botonReiniciar.clicked.connect(self.reiniciarSolicitado.emit)

        self.botonPlayPausa = IconoTemporizador("play", alturaBoton)  # estado inicial: pausado
        self.botonPlayPausa.setToolTip("Play / Pausa")
        self.botonPlayPausa.clicked.connect(self.playPausaSolicitado.emit)

        self.etiquetaTiempo = QLabel("00:00")
        self.etiquetaTiempo.setObjectName("etiquetaTiempoRestante")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(self.botonReiniciar)
        layout.addWidget(self.botonPlayPausa)
        layout.addWidget(self.etiquetaTiempo)

    def actualizarTiempo(self, texto):
        self.etiquetaTiempo.setText(texto)

    def actualizarEstadoPlayPausa(self, contando):
        self.botonPlayPausa.cambiarTipo("pausa" if contando else "play")
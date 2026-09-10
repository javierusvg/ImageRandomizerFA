from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QSize
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QAbstractButton

#Colores del switch (mismo azul de acento que el resto de la app)
_COLOR_APAGADO = QColor("#4a4a4a")
_COLOR_ENCENDIDO = QColor("#3d7eff")
_COLOR_BOLA = QColor("#ffffff")


class Interruptor(QAbstractButton):
    """
    Switch On/Off dibujado a mano (QPainter), con la bolita deslizante
    animada de izquierda (Off) a derecha (On). Sustituye al boton de
    texto ON/OFF: mismo comportamiento (checkable), distinta presentacion.
    """

    def __init__(self, activadoInicial=False, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self._posicion = 1.0 if activadoInicial else 0.0
        self.setChecked(activadoInicial)

        self.setFixedSize(44, 24)
        self.setCursor(Qt.PointingHandCursor)

        self._animacion = QPropertyAnimation(self, b"posicion", self)
        self._animacion.setDuration(150)
        self._animacion.setEasingCurve(QEasingCurve.InOutCubic)
        self.toggled.connect(self._animarHaciaEstado)

    def _animarHaciaEstado(self, activado):
        self._animacion.stop()
        self._animacion.setStartValue(self._posicion)
        self._animacion.setEndValue(1.0 if activado else 0.0)
        self._animacion.start()

    #--- PROPIEDAD ANIMABLE: posicion de la bolita, de 0.0 (izquierda) a 1.0 (derecha) ---
    def _obtenerPosicion(self):
        return self._posicion

    def _fijarPosicion(self, valor):
        self._posicion = valor
        self.update()

    posicion = Property(float, _obtenerPosicion, _fijarPosicion)

    def sizeHint(self):
        return QSize(44, 24)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        #Interpola el color de fondo entre apagado y encendido segun la posicion actual,
        #para que el propio fondo cambie de color a la vez que se desliza la bolita.
        t = self._posicion
        colorFondo = QColor(
            int(_COLOR_APAGADO.red() + (_COLOR_ENCENDIDO.red() - _COLOR_APAGADO.red()) * t),
            int(_COLOR_APAGADO.green() + (_COLOR_ENCENDIDO.green() - _COLOR_APAGADO.green()) * t),
            int(_COLOR_APAGADO.blue() + (_COLOR_ENCENDIDO.blue() - _COLOR_APAGADO.blue()) * t),
        )

        rect = self.rect()
        painter.setBrush(colorFondo)
        painter.drawRoundedRect(rect, rect.height() / 2, rect.height() / 2)

        margen = 3
        diametroBola = rect.height() - margen * 2
        xMinimo = margen
        xMaximo = rect.width() - margen - diametroBola
        xBola = xMinimo + (xMaximo - xMinimo) * t

        painter.setBrush(_COLOR_BOLA)
        painter.drawEllipse(int(xBola), margen, diametroBola, diametroBola)

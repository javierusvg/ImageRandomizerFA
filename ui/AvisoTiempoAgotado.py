from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from core.GestorIdioma import idioma

ESTILO_AVISO = """
QLabel#tarjetaAvisoTiempo {
    color: white;
    background: transparent;
    font-size: 120px;
    font-weight: 700;
}
"""


class AvisoTiempoAgotado(QWidget):
    """
    Overlay que se muestra centrado sobre el collage cuando el temporizador
    llega a 0. Es persistente (se crea una sola vez en VentanaPrincipal),
    asi que necesita su propio metodo retraducir() para actualizarse si el
    idioma cambia mientras la app esta abierta.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 140);")

        self.tarjeta = QLabel(idioma.traducir("aviso_tiempo.texto"), self)
        self.tarjeta.setObjectName("tarjetaAvisoTiempo")
        self.tarjeta.setStyleSheet(ESTILO_AVISO)
        self.tarjeta.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tarjeta, 0, Qt.AlignCenter)

        self._efectoOpacidad = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._efectoOpacidad)
        self._animacionEntrada = QPropertyAnimation(self._efectoOpacidad, b"opacity", self)
        self._animacionEntrada.setDuration(200)
        self._animacionEntrada.setStartValue(0.0)
        self._animacionEntrada.setEndValue(1.0)
        self._animacionEntrada.setEasingCurve(QEasingCurve.OutCubic)

        self.hide()

    def mostrar(self):
        self.setGeometry(self.parent().colocador.geometry())
        self._efectoOpacidad.setOpacity(0.0)
        self.show()
        self.raise_()
        self._animacionEntrada.start()

    def ocultar(self):
        self.hide()

    def actualizarSiVisible(self):
        if self.isVisible():
            self.setGeometry(self.parent().colocador.geometry())

    def retraducir(self):
        self.tarjeta.setText(idioma.traducir("aviso_tiempo.texto"))

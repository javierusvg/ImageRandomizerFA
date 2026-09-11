from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect

#--- ESTILO DEL AVISO ---
#Solo texto, sin tarjeta/fondo propio detras (se quito a peticion expresa).
#La legibilidad sobre imagenes claras la sigue dando la cortina semitransparente
#de fondo (self.setStyleSheet mas abajo, igual recurso que usa ZoomImagen),
#que oscurece TODO el collage antes de pintar el texto encima.
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
    llega a 0. Se posiciona igual que ZoomImagen (sobre self.parent().colocador).
    La cortina oscura semitransparente (heredada del mismo patron que ZoomImagen)
    es la que garantiza que el texto se lea sin importar el color de las
    imagenes visibles detras; el texto en si no lleva ningun fondo propio.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 140);")

        self.tarjeta = QLabel("TIEMPO", self)
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
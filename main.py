import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from ui.VentanaPrincipal import VentanaPrincipal
from config import COLOR_ACENTO

app = QApplication(sys.argv)
app.setStyle("Fusion")

paleta = app.palette()
paleta.setColor(QPalette.ButtonText, QColor("#dcdcdc"))

#Sin esto, controles nativos de Qt que no pasan por nuestro QSS (el segmento
#seleccionado dentro de un QTimeEdit, el "relleno" de progreso de un QSlider
#sin regla ::sub-page explicita, etc.) usan el azul de resaltado por defecto
#del sistema operativo, que no coincide con nuestro azul de acento. Fijando
#aqui el Highlight de la paleta, TODO lo que Qt resalte de forma nativa usa
#el mismo azul que el resto de la app.
paleta.setColor(QPalette.Highlight, QColor(COLOR_ACENTO))
paleta.setColor(QPalette.HighlightedText, QColor("white"))
app.setPalette(paleta)

ventana = VentanaPrincipal()
ventana.resize(1000, 700)
ventana.show()

sys.exit(app.exec())
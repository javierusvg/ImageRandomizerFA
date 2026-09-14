import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from ui.VentanaPrincipal import VentanaPrincipal
from config import COLOR_ACENTO

app = QApplication(sys.argv)
app.setStyle("Fusion")

paleta = app.palette()
paleta.setColor(QPalette.ButtonText, QColor("#dcdcdc"))
paleta.setColor(QPalette.Highlight, QColor(COLOR_ACENTO))
paleta.setColor(QPalette.HighlightedText, QColor("white"))
app.setPalette(paleta)

ventana = VentanaPrincipal()
ventana.resize(1000, 700)
ventana.show()

sys.exit(app.exec())

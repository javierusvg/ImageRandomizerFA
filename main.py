import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from ui.VentanaPrincipal import VentanaPrincipal

app = QApplication(sys.argv)
app.setStyle("Fusion")

paleta = app.palette()
paleta.setColor(QPalette.ButtonText, QColor("#dcdcdc"))
app.setPalette(paleta)

ventana = VentanaPrincipal()
ventana.resize(1000, 700)
ventana.show()

sys.exit(app.exec())
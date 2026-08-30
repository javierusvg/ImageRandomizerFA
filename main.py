import sys
from PySide6.QtWidgets import QApplication
from ui.VentanaPrincipal import VentanaPrincipal

app = QApplication(sys.argv)

ventana = VentanaPrincipal()
ventana.resize(1000, 700)
ventana.show()

sys.exit(app.exec())
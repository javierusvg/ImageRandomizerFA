import sys

from PySide6.QtWidgets import QApplication, QMainWindow


app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Image Randomizer")
window.resize(1000, 700)
window.show()

sys.exit(app.exec())
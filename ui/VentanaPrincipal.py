from PySide6.QtWidgets import QWidget, QSpinBox, QPushButton, QHBoxLayout, QVBoxLayout
from pathlib import Path
from config import MAXIMO_IMAGENES_ALEATORIAS, NUMERO_IMAGENES_INICIALES
from core.ListaImagenes import *
from ui.ColocadorImagenes import ColocadorImagenes

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.numeroImagenesSeleccionado = NUMERO_IMAGENES_INICIALES
        self.carpetas = [Path(r"C:\Wac\Estudio\RandomImageSelector_V3.2\Example_Reference_Library")]
        self.imagenesPool = cargarImagenes(self.carpetas)
        self.imagenesElegidas = elegirImagenes(self.numeroImagenesSeleccionado, self.imagenesPool)

        self.colocador = ColocadorImagenes(self.imagenesElegidas)
        self.colocador.solicitudNuevaImagen.connect(self.gestionarSolicitudNuevaImagen)#Conecta señal para randomizar una imagen

        #BOTOM SELECTOR NUMERO DE IMAGENES
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, MAXIMO_IMAGENES_ALEATORIAS)
        self.spinbox.setValue(self.numeroImagenesSeleccionado)
        self.spinbox.valueChanged.connect(self.actualizarNumeroSeleccionado)

        #BOTON PARA RANDOMIZAR
        self.botonRandomizar = QPushButton("Randomizar")
        self.botonRandomizar.clicked.connect(self.randomizarTodo)


        layoutControles = QHBoxLayout()
        layoutControles.addWidget(self.spinbox)
        layoutControles.addWidget(self.botonRandomizar)

        layoutPrincipal = QVBoxLayout()
        layoutPrincipal.addLayout(layoutControles)
        layoutPrincipal.addWidget(self.colocador)

        self.setLayout(layoutPrincipal)

    def actualizarNumeroSeleccionado(self, valor):
        self.numeroImagenesSeleccionado = valor

    def randomizarTodo(self):
        nuevasImagenesElegidas = elegirImagenes(self.numeroImagenesSeleccionado, self.imagenesPool, self.imagenesElegidas)
        self.imagenesElegidas = nuevasImagenesElegidas
        self.colocador.actualizarImagenes(self.imagenesElegidas)

    def gestionarSolicitudNuevaImagen(self, tileOrigen, rutasVisibles):
        resultado=elegirImagenes(1, self.imagenesPool, rutasVisibles)
        nuevaImagen = resultado[0]
        self.colocador.sustituirImagenEnTile(tileOrigen, nuevaImagen)
from PySide6.QtCore import Qt, QTime, Signal
from PySide6.QtWidgets import (
    QDialog, QLabel, QPushButton, QSlider, QTimeEdit, QAbstractSpinBox,
    QGridLayout, QVBoxLayout, QHBoxLayout, QFrame
)
from config import COLOR_ACENTO, COLOR_ACENTO_HOVER
from ui.Interruptor import Interruptor

#--- ESTILO PROPIO DEL DIALOGO ---
ESTILO_AJUSTES = f"""
QDialog {{
    background-color: #2b2b2b;
    color: #dcdcdc;
}}

QLabel {{
    color: #dcdcdc;
    font-size: 13px;
}}

QLabel:disabled {{
    color: #6e6e6e;
}}

QFrame#separadorAjustes {{
    background-color: #1a1a1a;
    max-height: 1px;
    border: none;
}}

QTimeEdit {{
    background-color: #1e1e1e;
    color: #dcdcdc;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 13px;
}}

QSlider::groove:horizontal {{
    height: 3px;
    background: #1e1e1e;
    border-radius: 1px;
}}

QSlider::sub-page:horizontal {{
    background: {COLOR_ACENTO};
    border-radius: 1px;
}}

QSlider::sub-page:horizontal:disabled {{
    background: #3a3a3a;
}}

QSlider::handle:horizontal {{
    width: 12px;
    height: 12px;
    margin: -5px 0;
    background: {COLOR_ACENTO};
    border-radius: 6px;
}}

QSlider::handle:horizontal:disabled {{
    background: #4a4a4a;
}}

QPushButton#botonCerrarAjustes {{
    background-color: {COLOR_ACENTO};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 20px;
    font-weight: 500;
}}

QPushButton#botonCerrarAjustes:hover {{
    background-color: {COLOR_ACENTO_HOVER};
}}
"""


class AjustesTemporizador(QDialog):
    """
    Panel de ajustes del temporizador: Tiempo, Parar al acabar, Alarma,
    Volumen alarma y Randomizar al acabar.
    """

    configuracionModificada = Signal()

    def __init__(self, temporizador, parent=None):
        super().__init__(parent)
        self.temporizador = temporizador

        self.setWindowTitle("Ajustes del temporizador")
        self.setStyleSheet(ESTILO_AJUSTES)
        #Ancho subido de 400 a 480: el slider de volumen ahora es mas largo (170px)
        #y necesitaba mas hueco para no obligar a recortar las etiquetas largas.
        self.setFixedWidth(480)

        #--- FILA: TIEMPO ---
        etiquetaTiempo = QLabel("Tiempo")
        self.selectorTiempo = QTimeEdit()
        self.selectorTiempo.setDisplayFormat("mm:ss")
        self.selectorTiempo.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.selectorTiempo.setFixedHeight(26)
        self.selectorTiempo.setFixedWidth(70)
        self.selectorTiempo.setAlignment(Qt.AlignCenter)
        minutos, segundos = divmod(self.temporizador.tiempoTotal, 60)
        self.selectorTiempo.setTime(QTime(0, minutos, segundos))
        self.selectorTiempo.timeChanged.connect(self.cambiarTiempo)

        #--- FILA: PARAR AL ACABAR ---
        etiquetaParar = QLabel("Parar el temporizador al acabar")
        self.interruptorParar = Interruptor(self.temporizador.pararTemporizadorAlAcabar)
        self.interruptorParar.toggled.connect(self.cambiarPararAlAcabar)

        #--- FILA: ALARMA ---
        etiquetaAlarma = QLabel("Alarma")
        self.interruptorAlarma = Interruptor(self.temporizador.alarma)
        self.interruptorAlarma.toggled.connect(self.cambiarAlarma)

        #--- FILA: VOLUMEN ALARMA (depende de Alarma) ---
        self.etiquetaVolumen = QLabel("Volumen alarma")
        self.sliderVolumen = QSlider(Qt.Horizontal)
        #Ancho subido de 110 a 170: se veia demasiado corto respecto al resto de controles.
        self.sliderVolumen.setFixedWidth(170)
        self.sliderVolumen.setRange(0, 100)
        self.sliderVolumen.setValue(self.temporizador.volumenAlarma)
        self.sliderVolumen.valueChanged.connect(self.cambiarVolumen)

        self.etiquetaVolumen.setEnabled(self.temporizador.alarma)
        self.sliderVolumen.setEnabled(self.temporizador.alarma)

        #--- FILA: RANDOMIZAR AL ACABAR ---
        etiquetaRandomizar = QLabel("Randomizar imágenes al acabar")
        self.interruptorRandomizar = Interruptor(self.temporizador.randomizarImagenesAlAcabar)
        self.interruptorRandomizar.toggled.connect(self.cambiarRandomizar)

        #--- MONTAJE: rejilla etiqueta (izquierda) + control (alineado a la derecha) ---
        filas = QGridLayout()
        filas.setContentsMargins(0, 0, 0, 0)
        filas.setHorizontalSpacing(20)
        filas.setVerticalSpacing(16)
        filas.setColumnStretch(0, 1)

        filas.addWidget(etiquetaTiempo, 0, 0)
        filas.addWidget(self.selectorTiempo, 0, 1, Qt.AlignRight)

        filas.addWidget(etiquetaParar, 1, 0)
        filas.addWidget(self.interruptorParar, 1, 1, Qt.AlignRight)

        filas.addWidget(etiquetaAlarma, 2, 0)
        filas.addWidget(self.interruptorAlarma, 2, 1, Qt.AlignRight)

        filas.addWidget(self.etiquetaVolumen, 3, 0)
        filas.addWidget(self.sliderVolumen, 3, 1, Qt.AlignRight)

        filas.addWidget(etiquetaRandomizar, 4, 0)
        filas.addWidget(self.interruptorRandomizar, 4, 1, Qt.AlignRight)

        separador = QFrame()
        separador.setObjectName("separadorAjustes")
        separador.setFrameShape(QFrame.HLine)

        botonCerrar = QPushButton("Cerrar")
        botonCerrar.setObjectName("botonCerrarAjustes")
        botonCerrar.clicked.connect(self.accept)

        filaBoton = QHBoxLayout()
        filaBoton.addStretch()
        filaBoton.addWidget(botonCerrar)

        layoutPrincipal = QVBoxLayout(self)
        layoutPrincipal.setContentsMargins(24, 22, 24, 20)
        layoutPrincipal.setSpacing(18)
        layoutPrincipal.addLayout(filas)
        layoutPrincipal.addWidget(separador)
        layoutPrincipal.addLayout(filaBoton)

    #--- GESTORES: escriben en el Temporizador real y avisan a VentanaPrincipal ---
    def cambiarTiempo(self, nuevoQTime):
        nuevoTotal = nuevoQTime.minute() * 60 + nuevoQTime.second()
        self.temporizador.tiempoTotal = nuevoTotal
        if not self.temporizador.contando:
            self.temporizador.tiempoRestante = nuevoTotal
        self.configuracionModificada.emit()

    def cambiarPararAlAcabar(self, activado):
        self.temporizador.pararTemporizadorAlAcabar = activado

    def cambiarAlarma(self, activado):
        self.temporizador.alarma = activado
        self.etiquetaVolumen.setEnabled(activado)
        self.sliderVolumen.setEnabled(activado)

    def cambiarVolumen(self, valor):
        self.temporizador.volumenAlarma = valor

    def cambiarRandomizar(self, activado):
        self.temporizador.randomizarImagenesAlAcabar = activado

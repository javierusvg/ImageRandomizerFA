from PySide6.QtCore import Qt, QTime, Signal
from PySide6.QtWidgets import (
    QDialog, QLabel, QPushButton, QSlider, QTimeEdit,
    QGridLayout, QVBoxLayout, QHBoxLayout
)
from ui.Interruptor import Interruptor

#--- ESTILO PROPIO DEL DIALOGO ---
#Reutiliza la paleta oscura y el azul de acento (#3d7eff) del resto de la app.
ESTILO_AJUSTES = """
QDialog {
    background-color: #2b2b2b;
    color: #dcdcdc;
}

QLabel {
    color: #dcdcdc;
    font-size: 13px;
}

QLabel:disabled {
    color: #6e6e6e;
}

QTimeEdit {
    background-color: #1e1e1e;
    color: #dcdcdc;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 2px 6px;
}

QSlider::groove:horizontal {
    height: 4px;
    background: #1e1e1e;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    width: 14px;
    margin: -5px 0;
    background: #3d7eff;
    border-radius: 7px;
}

QSlider::handle:horizontal:disabled {
    background: #4a4a4a;
}

QSlider::sub-page:horizontal:disabled {
    background: #3a3a3a;
}

QPushButton#botonCerrarAjustes {
    background-color: #3d7eff;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 4px 16px;
    font-weight: 500;
}

QPushButton#botonCerrarAjustes:hover {
    background-color: #5590ff;
}
"""
class AjustesTemporizador(QDialog):
    """
    Panel de ajustes del temporizador: Tiempo, Parar al acabar, Alarma,
    Volumen alarma y Randomizar al acabar.

    Los cambios se aplican en vivo directamente sobre la instancia de
    core.Temporizador recibida (sin botones Aceptar/Cancelar), porque
    es un panel de configuracion simple, no un formulario que se confirma.
    Al modificar cualquier valor emite configuracionModificada para que
    VentanaPrincipal pueda refrescar el bloque visible del temporizador
    (por ejemplo si se cambia el tiempo mientras esta en pausa).
    """

    configuracionModificada = Signal()

    def __init__(self, temporizador, parent=None):
        super().__init__(parent)
        self.temporizador = temporizador

        self.setWindowTitle("Ajustes del temporizador")
        self.setStyleSheet(ESTILO_AJUSTES)
        self.setFixedWidth(320)

        #--- FILA: TIEMPO ---
        etiquetaTiempo = QLabel("Tiempo")
        self.selectorTiempo = QTimeEdit()
        self.selectorTiempo.setDisplayFormat("mm:ss")
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
        self.sliderVolumen.setRange(0, 100)
        self.sliderVolumen.setValue(self.temporizador.volumenAlarma)
        self.sliderVolumen.valueChanged.connect(self.cambiarVolumen)

        self.etiquetaVolumen.setEnabled(self.temporizador.alarma)
        self.sliderVolumen.setEnabled(self.temporizador.alarma)

        #--- FILA: RANDOMIZAR AL ACABAR ---
        etiquetaRandomizar = QLabel("Randomizar imágenes al acabar")
        self.interruptorRandomizar = Interruptor(self.temporizador.randomizarImagenesAlAcabar)
        self.interruptorRandomizar.toggled.connect(self.cambiarRandomizar)

        #--- MONTAJE: rejilla etiqueta (izquierda) + control (derecha) ---
        filas = QGridLayout()
        filas.setContentsMargins(0, 0, 0, 0)
        filas.setHorizontalSpacing(16)
        filas.setVerticalSpacing(14)
        filas.setColumnStretch(0, 1)

        filas.addWidget(etiquetaTiempo, 0, 0)
        filas.addWidget(self.selectorTiempo, 0, 1)

        filas.addWidget(etiquetaParar, 1, 0)
        filas.addWidget(self.interruptorParar, 1, 1)

        filas.addWidget(etiquetaAlarma, 2, 0)
        filas.addWidget(self.interruptorAlarma, 2, 1)

        filas.addWidget(self.etiquetaVolumen, 3, 0)
        filas.addWidget(self.sliderVolumen, 3, 1)

        filas.addWidget(etiquetaRandomizar, 4, 0)
        filas.addWidget(self.interruptorRandomizar, 4, 1)

        botonCerrar = QPushButton("Cerrar")
        botonCerrar.setObjectName("botonCerrarAjustes")
        botonCerrar.clicked.connect(self.accept)

        filaBoton = QHBoxLayout()
        filaBoton.addStretch()
        filaBoton.addWidget(botonCerrar)

        layoutPrincipal = QVBoxLayout(self)
        layoutPrincipal.setContentsMargins(20, 20, 20, 16)
        layoutPrincipal.setSpacing(20)
        layoutPrincipal.addLayout(filas)
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

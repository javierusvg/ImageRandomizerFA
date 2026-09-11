from PySide6.QtWidgets import QWidget, QSpinBox, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QMenuBar, QMenu, QGraphicsBlurEffect
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtMultimedia import QSoundEffect
from pathlib import Path
from config import *
from core.ListaImagenes import *
from core.Temporizador import Temporizador
from ui.ColocadorImagenes import ColocadorImagenes
from ui.ZoomImagen import ZoomImagen
from ui.TemporizadorWidget import TemporizadorWidget
from ui.AjustesTemporizador import AjustesTemporizador
from ui.AvisoTiempoAgotado import AvisoTiempoAgotado

#--- ESTILO GLOBAL DE LA APP (QSS) ---
ESTILO_APP = f"""
QWidget {{
    background-color: #2b2b2b;
    color: #dcdcdc;
    font-size: 13px;
}}

#barraSuperior, #panelInferior {{
    background-color: #232323;
    border: none;
}}

#panelInferior {{
    border-top: 1px solid #1a1a1a;
}}

#barraSuperior {{
    border-bottom: 1px solid #1a1a1a;
}}

QPushButton {{
    background-color: {COLOR_ACENTO};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 4px 16px;
    font-weight: 500;
}}

QPushButton:hover {{
    background-color: {COLOR_ACENTO_HOVER};
}}

QPushButton:pressed {{
    background-color: {COLOR_ACENTO_PRESIONADO};
}}

QSpinBox {{
    background-color: #1e1e1e;
    color: #dcdcdc;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 2px 6px;
}}

QSpinBox::up-button, QSpinBox::down-button {{
    background-color: #2b2b2b;
    border: none;
    width: 16px;
}}

QMenuBar {{
    background-color: transparent;
    color: #dcdcdc;
    border: none;
    spacing: 2px;
}}

QMenuBar::item {{
    background: transparent;
    padding: 4px 10px;
    border-radius: 4px;
}}

QMenuBar::item:selected, QMenuBar::item:pressed {{
    background-color: {COLOR_ACENTO};
}}

QMenu {{
    background-color: #2b2b2b;
    color: #dcdcdc;
    border: 1px solid #3a3a3a;
}}

QMenu::item {{
    padding: 4px 20px;
}}

QMenu::item:selected, QMenu::item:pressed {{
    background-color: {COLOR_ACENTO};
}}
"""


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        #Vuelta a 27 (sin cambios de altura de barra, tal como pediste).
        alturaBarraSuperior = 27
        alturaBarraInferior = 34

        #--- CONFIGURACION VISUAL BASE ---
        self.setStyleSheet(ESTILO_APP)

        #--- ESTADO DE DATOS: POOL DE IMAGENES ---
        self.numeroImagenesSeleccionado = NUMERO_IMAGENES_INICIALES
        self.carpetas = [Path(r"C:\Wac\Estudio\RandomImageSelector_V3.2\Example_Reference_Library")]

        self.imagenesPool = cargarImagenes(self.carpetas)
        self.imagenesElegidas = elegirImagenes(self.numeroImagenesSeleccionado, self.imagenesPool)

        #--- WIDGETS FUNCIONALES ---
        self.colocador = ColocadorImagenes(self.imagenesElegidas)
        self.colocador.solicitudNuevaImagen.connect(self.gestionarSolicitudNuevaImagen)
        self.colocador.solicitudZoomImagen.connect(self.gestionarZoomImagen)

        self._efectoBlur = None

        self.zoom = ZoomImagen(self)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, MAXIMO_IMAGENES_ALEATORIAS)
        self.spinbox.setValue(self.numeroImagenesSeleccionado)
        self.spinbox.valueChanged.connect(self.actualizarNumeroSeleccionado)

        self.botonRandomizar = QPushButton("Randomizar")
        self.botonRandomizar.clicked.connect(self.randomizarTodo)

        #--- TEMPORIZADOR: ESTADO, SONIDO Y AVISO EN PANTALLA ---
        self.temporizador = Temporizador(TIEMPO_TEMPORIZADOR_INICIAL)

        self._sonidoAlarma = QSoundEffect(self)
        self._sonidoAlarma.setSource(QUrl.fromLocalFile(RUTA_SONIDO_ALARMA))

        #alturaBoton = alturaBarraSuperior - 4: TemporizadorWidget suma 2px de
        #margen arriba y 2px abajo por dentro, asi que el bloque resultante
        #(27 = 23 + 2 + 2) ocupa EXACTAMENTE toda la altura de la barra,
        #sin quedar mas pequeño que ella como pasaba antes.
        self.temporizadorWidget = TemporizadorWidget(alturaBoton=alturaBarraSuperior - 4)
        self.temporizadorWidget.actualizarTiempo(self.temporizador.tiempoFormateado())
        self.temporizadorWidget.actualizarEstadoPlayPausa(self.temporizador.contando)
        self.temporizadorWidget.reiniciarSolicitado.connect(self.gestionarReinicioTemporizador)
        self.temporizadorWidget.playPausaSolicitado.connect(self.gestionarPlayPausaTemporizador)

        self.avisoTiempo = AvisoTiempoAgotado(self)

        self.relojInterno = QTimer(self)
        self.relojInterno.setInterval(1000)
        self.relojInterno.timeout.connect(self.tickTemporizador)
        self.relojInterno.start()

        #--- CONSTRUCCION DE LA ESTRUCTURA VISUAL (3 BANDAS) ---
        barraSuperior = QWidget()
        barraSuperior.setObjectName("barraSuperior")
        barraSuperior.setFixedHeight(alturaBarraSuperior)

        self.menuSuperior = self.crearMenuSuperior()
        self.menuSuperior.setFixedHeight(alturaBarraSuperior)

        layoutBarraSuperior = QHBoxLayout(barraSuperior)
        layoutBarraSuperior.setContentsMargins(4, 0, 10, 0)
        layoutBarraSuperior.addWidget(self.menuSuperior)
        layoutBarraSuperior.addStretch()
        layoutBarraSuperior.addWidget(self.temporizadorWidget)

        panelInferior = QWidget()
        panelInferior.setObjectName("panelInferior")
        panelInferior.setFixedHeight(alturaBarraInferior)

        self.spinbox.setFixedHeight(alturaBarraInferior - 4)
        self.spinbox.setFixedWidth(50)
        self.botonRandomizar.setFixedHeight(alturaBarraInferior - 4)

        layoutControles = QHBoxLayout(panelInferior)
        layoutControles.setContentsMargins(10, 0, 10, 0)
        layoutControles.setSpacing(8)
        layoutControles.addStretch()
        layoutControles.addWidget(self.botonRandomizar)
        layoutControles.addWidget(self.spinbox)
        layoutControles.addStretch()

        layoutPrincipal = QVBoxLayout()
        layoutPrincipal.setContentsMargins(0, 0, 0, 0)
        layoutPrincipal.setSpacing(0)
        layoutPrincipal.addWidget(barraSuperior)
        layoutPrincipal.addWidget(self.colocador)
        layoutPrincipal.addWidget(panelInferior)

        self.setLayout(layoutPrincipal)

    def crearMenuSuperior(self):
        menuCarpeta = QMenu("Carpeta", self)

        menuAjustes = QMenu("Ajustes", self)
        menuAjustes.addMenu(QMenu("Idioma", self))
        accionTemporizador = menuAjustes.addAction("Temporizador")
        accionTemporizador.triggered.connect(self.abrirAjustesTemporizador)

        menuBar = QMenuBar(self)
        menuBar.addMenu(menuCarpeta)
        menuBar.addMenu(menuAjustes)

        return menuBar

    def actualizarNumeroSeleccionado(self, valor):
        self.numeroImagenesSeleccionado = valor

    def randomizarTodo(self):
        nuevasImagenesElegidas = elegirImagenes(self.numeroImagenesSeleccionado, self.imagenesPool, self.imagenesElegidas)
        self.imagenesElegidas = nuevasImagenesElegidas
        self.colocador.actualizarImagenes(self.imagenesElegidas)
        self.zoom.hide()

    def gestionarSolicitudNuevaImagen(self, tileOrigen, rutasVisibles):
        resultado = elegirImagenes(1, self.imagenesPool, rutasVisibles)
        nuevaImagen = resultado[0]
        self.colocador.sustituirImagenEnTile(tileOrigen, nuevaImagen)

    def gestionarZoomImagen(self, tileOrigen):
        self.zoom.mostrarImagen(tileOrigen.ruta)

    def gestionarReinicioTemporizador(self):
        self.temporizador.reiniciar(respetarSwitchPausa=False)
        self.temporizadorWidget.actualizarTiempo(self.temporizador.tiempoFormateado())
        self.temporizadorWidget.actualizarEstadoPlayPausa(self.temporizador.contando)

    def gestionarPlayPausaTemporizador(self):
        if self.temporizador.contando:
            self.temporizador.pausa()
        else:
            self.temporizador.play()
        self.temporizadorWidget.actualizarEstadoPlayPausa(self.temporizador.contando)

    def abrirAjustesTemporizador(self):
        dialogo = AjustesTemporizador(self.temporizador, self)
        dialogo.configuracionModificada.connect(self.refrescarTemporizadorWidget)
        dialogo.exec()

    def refrescarTemporizadorWidget(self):
        self.temporizadorWidget.actualizarTiempo(self.temporizador.tiempoFormateado())
        self.temporizadorWidget.actualizarEstadoPlayPausa(self.temporizador.contando)

    def aplicarBlurFondo(self):
        efecto = QGraphicsBlurEffect(self)
        efecto.setBlurRadius(12)
        self.colocador.setGraphicsEffect(efecto)
        self._efectoBlur = efecto

    def quitarBlurFondo(self):
        if self._efectoBlur is not None:
            self.colocador.setGraphicsEffect(None)
            self._efectoBlur = None

    def tickTemporizador(self):
        agotado = self.temporizador.avanzarUnSegundo()
        self.temporizadorWidget.actualizarTiempo(self.temporizador.tiempoFormateado())
        if agotado:
            self.gestionarTiempoAgotado()

    def gestionarTiempoAgotado(self):
        self.aplicarBlurFondo()
        self.avisoTiempo.mostrar()

        if self.temporizador.alarma:
            self._sonidoAlarma.setVolume(self.temporizador.volumenAlarma / 100)
            self._sonidoAlarma.play()

        QTimer.singleShot(DURACION_AVISO_TIEMPO_AGOTADO, self.finalizarAvisoTiempoAgotado)

    def finalizarAvisoTiempoAgotado(self):
        self.avisoTiempo.ocultar()
        self.quitarBlurFondo()
        self.temporizador.reiniciar(respetarSwitchPausa=True)
        self.temporizadorWidget.actualizarTiempo(self.temporizador.tiempoFormateado())
        self.temporizadorWidget.actualizarEstadoPlayPausa(self.temporizador.contando)

        if self.temporizador.randomizarImagenesAlAcabar:
            self.randomizarTodo()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.zoom.actualizarSiVisible()
        self.avisoTiempo.actualizarSiVisible()

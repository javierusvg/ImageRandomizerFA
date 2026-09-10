from PySide6.QtWidgets import QWidget, QSpinBox, QPushButton, QHBoxLayout, QVBoxLayout, QFrame,QMenuBar, QMenu, QLabel, QGraphicsBlurEffect
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QFont
from PySide6.QtMultimedia import QSoundEffect
from pathlib import Path
from config import *
from core.ListaImagenes import *
from core.Temporizador import Temporizador
from ui.ColocadorImagenes import ColocadorImagenes
from ui.ZoomImagen import ZoomImagen
from ui.TemporizadorWidget import TemporizadorWidget
from ui.AjustesTemporizador import AjustesTemporizador


#--- ESTILO GLOBAL DE LA APP (QSS) ---
#Se aplica una sola vez sobre toda la ventana en vez de estilos sueltos por widget
ESTILO_APP = """
QWidget {
    background-color: #2b2b2b;
    color: #dcdcdc;
    font-size: 13px;
}

#barraSuperior, #panelInferior {
    background-color: #232323;
    border: none;
}

#panelInferior {
    border-top: 1px solid #1a1a1a;
}

#barraSuperior {
    border-bottom: 1px solid #1a1a1a;
}

QPushButton {
    background-color: #3d7eff;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 4px 16px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #5590ff;
}

QPushButton:pressed {
    background-color: #2d6ae0;
}

QSpinBox {
    background-color: #1e1e1e;
    color: #dcdcdc;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 2px 6px;
}

QSpinBox::up-button, QSpinBox::down-button {
    background-color: #2b2b2b;
    border: none;
    width: 16px;
}

QMenuBar {
    background-color: transparent;
    color: #dcdcdc;
    border: none;
    spacing: 2px;
}

QMenuBar::item {
    background: transparent;
    padding: 4px 10px;
    border-radius: 4px;
}

QMenuBar::item:selected {
    background-color: #3d7eff;
}

QMenu {
    background-color: #2b2b2b;
    color: #dcdcdc;
    border: 1px solid #3a3a3a;
}

QMenu::item {
    padding: 4px 20px;
}

QMenu::item:selected {
    background-color: #3d7eff;
}

QLabel#etiquetaAvisoTiempo {
    color: white;
    background: transparent;
    font-size: 64px;
    font-weight: 700;
}
"""


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        alturaBarraSuperior = 27
        alturaBarraInferior = 34

        #--- CONFIGURACION VISUAL BASE ---
        self.setStyleSheet(ESTILO_APP)

        #--- ESTADO DE DATOS: POOL DE IMAGENES ---
        #CARPETA ORIGEN
        self.numeroImagenesSeleccionado = NUMERO_IMAGENES_INICIALES
        self.carpetas = [Path(r"C:\Wac\Estudio\RandomImageSelector_V3.2\Example_Reference_Library")]

        #POOL COMPLETO (todas las imagenes validas de esas carpetas) y la seleccion actual visible
        self.imagenesPool = cargarImagenes(self.carpetas)
        self.imagenesElegidas = elegirImagenes(self.numeroImagenesSeleccionado, self.imagenesPool)

        #--- WIDGETS FUNCIONALES ---
        #COLLAGE IMAGENES (area central) + conexion de sus señales al gestor de esta ventana
        self.colocador = ColocadorImagenes(self.imagenesElegidas)
        self.colocador.solicitudNuevaImagen.connect(self.gestionarSolicitudNuevaImagen)
        self.colocador.solicitudZoomImagen.connect(self.gestionarZoomImagen)

        #BLUR DE FONDO
        self._efectoBlur = None

        #OVERLAY DE ZOOM
        self.zoom = ZoomImagen(self)

        #CONTROLES PANEL INFERIOR: cuantas imagenes randomizar y boton de randomizar
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

        self.temporizadorWidget = TemporizadorWidget(alturaBoton=alturaBarraSuperior - 6)
        self.temporizadorWidget.actualizarTiempo(self.temporizador.tiempoFormateado())
        self.temporizadorWidget.actualizarEstadoPlayPausa(self.temporizador.contando)
        self.temporizadorWidget.reiniciarSolicitado.connect(self.gestionarReinicioTemporizador)
        self.temporizadorWidget.playPausaSolicitado.connect(self.gestionarPlayPausaTemporizador)

        #Etiqueta "TIEMPO" que aparece centrada sobre el collage al agotarse el temporizador
        self.etiquetaAvisoTiempo = QLabel("TIEMPO", self)
        self.etiquetaAvisoTiempo.setObjectName("etiquetaAvisoTiempo")
        self.etiquetaAvisoTiempo.setAlignment(Qt.AlignCenter)
        self.etiquetaAvisoTiempo.hide()

        #Reloj real: cada 1000ms descuenta un segundo del temporizador (si esta en play)
        self.relojInterno = QTimer(self)
        self.relojInterno.setInterval(1000)
        self.relojInterno.timeout.connect(self.tickTemporizador)
        self.relojInterno.start()

        #--- CONSTRUCCION DE LA ESTRUCTURA VISUAL (3 BANDAS) ---
        #BANDA SUPERIOR (menu bar a la izquierda; el cronometro visible ira a la derecha en la siguiente version)
        barraSuperior = QWidget()
        barraSuperior.setObjectName("barraSuperior")
        barraSuperior.setFixedHeight(alturaBarraSuperior)

        #Menu bar propiamente dicho (Carpeta / Ajustes), sin funcionalidad todavia
        self.menuSuperior = self.crearMenuSuperior()
        self.menuSuperior.setFixedHeight(alturaBarraSuperior)

        layoutBarraSuperior = QHBoxLayout(barraSuperior)
        layoutBarraSuperior.setContentsMargins(4, 0, 10, 0)
        layoutBarraSuperior.addWidget(self.menuSuperior)
        layoutBarraSuperior.addStretch()
        layoutBarraSuperior.addWidget(self.temporizadorWidget)

        #BANDA INFERIOR (controles de randomizado)
        panelInferior = QWidget()
        panelInferior.setObjectName("panelInferior")
        panelInferior.setFixedHeight(alturaBarraInferior)

        #Tamaños de los controles ajustados a la altura compacta de la banda
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

        #--- ENSAMBLADO FINAL: BARRA SUPERIOR + COLLAGE + PANEL INFERIOR ---
        layoutPrincipal = QVBoxLayout()
        layoutPrincipal.setContentsMargins(0, 0, 0, 0)
        layoutPrincipal.setSpacing(0)
        layoutPrincipal.addWidget(barraSuperior)
        layoutPrincipal.addWidget(self.colocador)
        layoutPrincipal.addWidget(panelInferior)

        self.setLayout(layoutPrincipal)

    #--- CONSTRUCCION DEL MENU SUPERIOR (Carpeta / Ajustes) ---
    def crearMenuSuperior(self):
        #Carpeta: por ahora sin acciones (se añadira mas adelante el dialogo para elegir carpetas)
        menuCarpeta = QMenu("Carpeta", self)

        #Ajustes: contiene los submenus Idioma y Temporizador, ambos vacios por ahora
        menuAjustes = QMenu("Ajustes", self)
        menuAjustes.addMenu(QMenu("Idioma", self))
        accionTemporizador = menuAjustes.addAction("Temporizador")
        accionTemporizador.triggered.connect(self.abrirAjustesTemporizador)

        menuBar = QMenuBar(self)
        menuBar.addMenu(menuCarpeta)
        menuBar.addMenu(menuAjustes)

        return menuBar

    #--- GESTORES DE ESTADO ---
    def actualizarNumeroSeleccionado(self, valor):
        self.numeroImagenesSeleccionado = valor

    def randomizarTodo(self):
        nuevasImagenesElegidas = elegirImagenes(self.numeroImagenesSeleccionado, self.imagenesPool, self.imagenesElegidas)
        self.imagenesElegidas = nuevasImagenesElegidas
        self.colocador.actualizarImagenes(self.imagenesElegidas)
        self.zoom.hide()

    #--- GESTORES DE SEÑALES DEL COLOCADOR ---
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

    #--- BLUR DE FONDO (compartido entre ZoomImagen y el aviso del temporizador) ---
    def aplicarBlurFondo(self):
        efecto = QGraphicsBlurEffect(self)
        efecto.setBlurRadius(12)
        self.colocador.setGraphicsEffect(efecto)
        self._efectoBlur = efecto

    def quitarBlurFondo(self):
        if self._efectoBlur is not None:
            self.colocador.setGraphicsEffect(None)
            self._efectoBlur = None

    #--- TEMPORIZADOR: TICK Y SECUENCIA FINAL ---
    def tickTemporizador(self):
        agotado = self.temporizador.avanzarUnSegundo()
        self.temporizadorWidget.actualizarTiempo(self.temporizador.tiempoFormateado())
        if agotado:
            self.gestionarTiempoAgotado()

    def gestionarTiempoAgotado(self):
        self.aplicarBlurFondo()
        self.etiquetaAvisoTiempo.setGeometry(self.colocador.geometry())
        self.etiquetaAvisoTiempo.show()
        self.etiquetaAvisoTiempo.raise_()

        if self.temporizador.alarma:
            self._sonidoAlarma.setVolume(self.temporizador.volumenAlarma / 100)
            self._sonidoAlarma.play()

        QTimer.singleShot(DURACION_AVISO_TIEMPO_AGOTADO, self.finalizarAvisoTiempoAgotado)

    def finalizarAvisoTiempoAgotado(self):
        self.etiquetaAvisoTiempo.hide()
        self.quitarBlurFondo()
        self.temporizador.reiniciar(respetarSwitchPausa=True)
        self.temporizadorWidget.actualizarTiempo(self.temporizador.tiempoFormateado())
        self.temporizadorWidget.actualizarEstadoPlayPausa(self.temporizador.contando)

        if self.temporizador.randomizarImagenesAlAcabar:
            self.randomizarTodo()

    #--- EVENTOS DE QT ---
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.zoom.actualizarSiVisible()
        if self.etiquetaAvisoTiempo.isVisible():
            self.etiquetaAvisoTiempo.setGeometry(self.colocador.geometry())
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,
    QVBoxLayout, QHBoxLayout
)
from config import COLOR_ACENTO, COLOR_ACENTO_HOVER, MAXIMO_CARPETAS
from core.GestorCarpetas import EntradaCarpeta
from core.GestorIdioma import idioma
from ui.RecuadroCarpeta import RecuadroCarpeta

#--- ESTILO COMPARTIDO POR LOS DOS DIALOGOS DE ESTE ARCHIVO ---
ESTILO_DIALOGO = f"""
QDialog {{
    background-color: #2b2b2b;
    color: #dcdcdc;
}}

QLabel {{
    color: #dcdcdc;
    font-size: 13px;
}}

QLineEdit {{
    background-color: #1e1e1e;
    color: #dcdcdc;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 5px 8px;
}}

QPushButton#botonCancelarCarpetas {{
    background-color: #3a3a3a;
    color: #dcdcdc;
    border: none;
    border-radius: 4px;
    padding: 6px 20px;
}}

QPushButton#botonCancelarCarpetas:hover {{
    background-color: #4a4a4a;
}}

QPushButton#botonAceptarCarpetas {{
    background-color: {COLOR_ACENTO};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 20px;
    font-weight: 500;
}}

QPushButton#botonAceptarCarpetas:hover {{
    background-color: {COLOR_ACENTO_HOVER};
}}

QPushButton#botonCambiarCarpeta {{
    background-color: #2b2b2b;
    color: #dcdcdc;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 6px 14px;
}}

QPushButton#botonCambiarCarpeta:hover {{
    background-color: #333333;
}}
"""


class EditarCarpetaDialog(QDialog):
    """
    Mini-formulario del boton "Editar": nombre editable en un campo de texto
    + boton "Cambiar carpeta" que reabre el explorador de archivos.
    """

    def __init__(self, nombreActual, rutaActual, parent=None):
        super().__init__(parent)
        self.setWindowTitle(idioma.traducir("carpetas.titulo_editar"))
        self.setStyleSheet(ESTILO_DIALOGO)
        self.setFixedWidth(380)

        self.rutaSeleccionada = rutaActual

        etiquetaNombre = QLabel(idioma.traducir("carpetas.nombre"))
        self.campoNombre = QLineEdit(nombreActual)

        etiquetaRuta = QLabel(idioma.traducir("carpetas.carpeta"))
        self.etiquetaRutaActual = QLabel(str(rutaActual))
        self.etiquetaRutaActual.setWordWrap(True)
        self.etiquetaRutaActual.setStyleSheet("color: #9a9a9a; font-size: 12px;")

        botonCambiarCarpeta = QPushButton(idioma.traducir("carpetas.cambiar_carpeta"))
        botonCambiarCarpeta.setObjectName("botonCambiarCarpeta")
        botonCambiarCarpeta.clicked.connect(self.elegirCarpeta)

        botonCancelar = QPushButton(idioma.traducir("comun.cancelar"))
        botonCancelar.setObjectName("botonCancelarCarpetas")
        botonCancelar.clicked.connect(self.reject)

        botonAceptar = QPushButton(idioma.traducir("comun.aceptar"))
        botonAceptar.setObjectName("botonAceptarCarpetas")
        botonAceptar.clicked.connect(self.accept)

        layoutBotones = QHBoxLayout()
        layoutBotones.addWidget(botonCancelar)
        layoutBotones.addWidget(botonAceptar)
        layoutBotones.addStretch()

        layoutPrincipal = QVBoxLayout(self)
        layoutPrincipal.setContentsMargins(20, 20, 20, 16)
        layoutPrincipal.setSpacing(10)
        layoutPrincipal.addWidget(etiquetaNombre)
        layoutPrincipal.addWidget(self.campoNombre)
        layoutPrincipal.addSpacing(6)
        layoutPrincipal.addWidget(etiquetaRuta)
        layoutPrincipal.addWidget(self.etiquetaRutaActual)
        layoutPrincipal.addWidget(botonCambiarCarpeta)
        layoutPrincipal.addSpacing(8)
        layoutPrincipal.addLayout(layoutBotones)

    def elegirCarpeta(self):
        rutaTexto = QFileDialog.getExistingDirectory(self, idioma.traducir("carpetas.selecciona_carpeta"))
        if rutaTexto:
            self.rutaSeleccionada = Path(rutaTexto)
            self.etiquetaRutaActual.setText(str(self.rutaSeleccionada))

    def obtenerResultado(self):
        return self.campoNombre.text().strip(), self.rutaSeleccionada


class GestorCarpetasDialog(QDialog):
    """
    Ventana "Gestionar carpetas": 6 recuadros fijos (MAXIMO_CARPETAS).
    Trabaja siempre sobre una COPIA de las entradas recibidas; nada se
    aplica de verdad (ni se guarda en disco) hasta que se pulsa Aceptar.
    """

    def __init__(self, entradasActuales, parent=None):
        super().__init__(parent)
        self.setWindowTitle(idioma.traducir("carpetas.titulo_gestor"))
        self.setStyleSheet(ESTILO_DIALOGO)
        self.setFixedWidth(460)

        self.entradas = [
            entradasActuales[i] if i < len(entradasActuales) else None
            for i in range(MAXIMO_CARPETAS)
        ]

        self.recuadros = []
        layoutRecuadros = QVBoxLayout()
        layoutRecuadros.setSpacing(8)

        for indice in range(MAXIMO_CARPETAS):
            recuadro = RecuadroCarpeta(indice)
            recuadro.solicitudAñadir.connect(self.añadirCarpeta)
            recuadro.solicitudEditar.connect(self.editarCarpeta)
            recuadro.solicitudToggle.connect(self.alternarActiva)
            recuadro.solicitudEliminar.connect(self.eliminarCarpeta)
            self.recuadros.append(recuadro)
            layoutRecuadros.addWidget(recuadro)

        botonCancelar = QPushButton(idioma.traducir("comun.cancelar"))
        botonCancelar.setObjectName("botonCancelarCarpetas")
        botonCancelar.clicked.connect(self.reject)

        botonAceptar = QPushButton(idioma.traducir("comun.aceptar"))
        botonAceptar.setObjectName("botonAceptarCarpetas")
        botonAceptar.clicked.connect(self.accept)

        layoutBotones = QHBoxLayout()
        layoutBotones.addWidget(botonCancelar)
        layoutBotones.addWidget(botonAceptar)
        layoutBotones.addStretch()

        layoutPrincipal = QVBoxLayout(self)
        layoutPrincipal.setContentsMargins(20, 20, 20, 16)
        layoutPrincipal.setSpacing(16)
        layoutPrincipal.addLayout(layoutRecuadros)
        layoutPrincipal.addLayout(layoutBotones)

        self.refrescarTodos()

    def refrescarTodos(self):
        for indice, recuadro in enumerate(self.recuadros):
            entrada = self.entradas[indice]
            if entrada is None:
                recuadro.mostrarVacio()
            else:
                recuadro.mostrarConCarpeta(entrada.nombre, entrada.activa)

    def _rutaYaExiste(self, ruta, ignorarIndice=None):
        for indice, entrada in enumerate(self.entradas):
            if entrada is not None and indice != ignorarIndice and entrada.ruta == ruta:
                return True
        return False

    def añadirCarpeta(self, indice):
        rutaTexto = QFileDialog.getExistingDirectory(self, idioma.traducir("carpetas.selecciona_carpeta"))
        if not rutaTexto:
            return

        ruta = Path(rutaTexto)

        if self._rutaYaExiste(ruta):
            QMessageBox.warning(
                self,
                idioma.traducir("carpetas.duplicada_titulo"),
                idioma.traducir("carpetas.duplicada_mensaje"),
            )
            return

        self.entradas[indice] = EntradaCarpeta(ruta.name, ruta, activa=True)
        self.refrescarTodos()

    def editarCarpeta(self, indice):
        entrada = self.entradas[indice]

        dialogoEdicion = EditarCarpetaDialog(entrada.nombre, entrada.ruta, self)
        if dialogoEdicion.exec() != QDialog.Accepted:
            return

        nuevoNombre, nuevaRuta = dialogoEdicion.obtenerResultado()

        if self._rutaYaExiste(nuevaRuta, ignorarIndice=indice):
            QMessageBox.warning(
                self,
                idioma.traducir("carpetas.duplicada_titulo"),
                idioma.traducir("carpetas.duplicada_mensaje"),
            )
            return

        entrada.nombre = nuevoNombre if nuevoNombre else nuevaRuta.name
        entrada.ruta = nuevaRuta
        self.refrescarTodos()

    def alternarActiva(self, indice):
        entrada = self.entradas[indice]
        entrada.activa = not entrada.activa
        self.refrescarTodos()

    def eliminarCarpeta(self, indice):
        self.entradas[indice] = None
        self.refrescarTodos()

    def obtenerEntradasFinales(self):
        return [entrada for entrada in self.entradas if entrada is not None]

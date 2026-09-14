from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QHBoxLayout, QWidget
from config import COLOR_ACENTO, COLOR_ACENTO_HOVER
from core.GestorIdioma import idioma

#--- ESTILOS: uno por estado del recuadro (vacio / activo / inactivo) ---
ESTILO_VACIO = """
QFrame#recuadroCarpeta {
    background-color: #1e1e1e;
    border: 1px dashed #3a3a3a;
    border-radius: 6px;
}
QWidget#contenidoRecuadro {
    background: transparent;
}
"""

ESTILO_ACTIVO = """
QFrame#recuadroCarpeta {
    background-color: #1e1e1e;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
}
QWidget#contenidoRecuadro {
    background: transparent;
}
"""

ESTILO_INACTIVO = """
QFrame#recuadroCarpeta {
    background-color: #232323;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
}
QWidget#contenidoRecuadro {
    background: transparent;
}
"""

ESTILO_BOTON_AÑADIR = f"""
QPushButton#botonAñadirCarpeta {{
    background-color: {COLOR_ACENTO};
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 30px;
    font-weight: 700;
    padding: 0px;
}}
QPushButton#botonAñadirCarpeta:hover {{
    background-color: {COLOR_ACENTO_HOVER};
}}
"""

ESTILO_BOTON_ACCION = """
QPushButton#botonAccionCarpeta {
    background-color: #2b2b2b;
    color: #dcdcdc;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 3px 10px;
    font-weight: 400;
    font-size: 12px;
}
QPushButton#botonAccionCarpeta:hover {
    background-color: #333333;
}
"""

ESTILO_BOTON_ELIMINAR = """
QPushButton#botonEliminarCarpeta {
    background-color: #2b2b2b;
    color: #dcdcdc;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 12px;
}
QPushButton#botonEliminarCarpeta:hover {
    background-color: #b23b3b;
    border-color: #b23b3b;
    color: white;
}
"""


class RecuadroCarpeta(QFrame):
    """
    Una fila de la ventana "Gestionar carpetas". Tiene dos estados visuales:
    - Vacio: un boton cuadrado "+" pegado a la izquierda.
    - Con carpeta: nombre + botones Editar / Deshabilitar-Habilitar / Eliminar.

    No conoce nada de carpetas.json ni del pool de imagenes: solo emite
    señales con su propio indice, y quien las escuche (GestorCarpetasDialog)
    decide que hacer. Los textos de sus botones salen de idioma.traducir():
    como este widget se crea de nuevo cada vez que se abre el dialogo de
    carpetas, siempre nace ya en el idioma activo en ese momento.
    """

    solicitudAñadir = Signal(int)
    solicitudEditar = Signal(int)
    solicitudToggle = Signal(int)
    solicitudEliminar = Signal(int)

    ALTURA = 44

    def __init__(self, indice):
        super().__init__()
        self.indice = indice
        self.setObjectName("recuadroCarpeta")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(self.ALTURA)

        #--- ESTADO VACIO: boton cuadrado "+" a la izquierda ---
        self.botonAñadir = QPushButton("+")
        self.botonAñadir.setObjectName("botonAñadirCarpeta")
        self.botonAñadir.setStyleSheet(ESTILO_BOTON_AÑADIR)
        self.botonAñadir.setFixedSize(40, 32)
        self.botonAñadir.setCursor(Qt.PointingHandCursor)
        self.botonAñadir.clicked.connect(lambda: self.solicitudAñadir.emit(self.indice))

        self.contenedorVacio = QWidget()
        self.contenedorVacio.setObjectName("contenidoRecuadro")
        layoutVacio = QHBoxLayout(self.contenedorVacio)
        layoutVacio.setContentsMargins(0, 0, 0, 0)
        layoutVacio.addWidget(self.botonAñadir, 0, Qt.AlignVCenter)
        layoutVacio.addStretch()

        #--- ESTADO CON CARPETA ---
        self.etiquetaNombre = QLabel()

        self.botonEditar = QPushButton(idioma.traducir("carpetas.editar"))
        self.botonEditar.setObjectName("botonAccionCarpeta")
        self.botonEditar.setStyleSheet(ESTILO_BOTON_ACCION)
        self.botonEditar.clicked.connect(lambda: self.solicitudEditar.emit(self.indice))

        self.botonToggle = QPushButton(idioma.traducir("carpetas.deshabilitar"))
        self.botonToggle.setObjectName("botonAccionCarpeta")
        self.botonToggle.setStyleSheet(ESTILO_BOTON_ACCION)
        self.botonToggle.clicked.connect(lambda: self.solicitudToggle.emit(self.indice))

        self.botonEliminar = QPushButton(idioma.traducir("carpetas.eliminar"))
        self.botonEliminar.setObjectName("botonEliminarCarpeta")
        self.botonEliminar.setStyleSheet(ESTILO_BOTON_ELIMINAR)
        self.botonEliminar.clicked.connect(lambda: self.solicitudEliminar.emit(self.indice))

        self.contenedorLleno = QWidget()
        self.contenedorLleno.setObjectName("contenidoRecuadro")
        layoutLleno = QHBoxLayout(self.contenedorLleno)
        layoutLleno.setContentsMargins(0, 0, 0, 0)
        layoutLleno.setSpacing(8)
        layoutLleno.addWidget(self.etiquetaNombre, 1)
        layoutLleno.addWidget(self.botonEditar)
        layoutLleno.addWidget(self.botonToggle)
        layoutLleno.addWidget(self.botonEliminar)

        layoutPrincipal = QHBoxLayout(self)
        layoutPrincipal.setContentsMargins(12, 0, 12, 0)
        layoutPrincipal.addWidget(self.contenedorVacio)
        layoutPrincipal.addWidget(self.contenedorLleno)

        self.mostrarVacio()

    def _repintar(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def mostrarVacio(self):
        self.contenedorVacio.show()
        self.contenedorLleno.hide()
        self.setStyleSheet(ESTILO_VACIO)
        self._repintar()

    def mostrarConCarpeta(self, nombre, activa):
        self.contenedorVacio.hide()
        self.contenedorLleno.show()

        self.etiquetaNombre.setText(nombre)
        self.botonToggle.setText(
            idioma.traducir("carpetas.habilitar") if not activa else idioma.traducir("carpetas.deshabilitar")
        )

        if activa:
            self.setStyleSheet(ESTILO_ACTIVO)
            self.etiquetaNombre.setStyleSheet("color: #dcdcdc; font-weight: 500; background: transparent;")
        else:
            self.setStyleSheet(ESTILO_INACTIVO)
            self.etiquetaNombre.setStyleSheet("color: #6e6e6e; font-weight: 500; background: transparent;")

        self._repintar()

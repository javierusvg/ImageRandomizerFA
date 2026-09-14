#ENTRADA:
# proporciones: Lista de las proporciones(ancho/alto) de las imagenes
# anchoDisponible: Ancho disponible en ventana
# altoObjetivoFila: Altura objetivo de la fila(altura maxima de la ventana)
# gap: separacion entre imagenes.
#SALIDA:
# Lista de rectangulos(uno por imagen), con sus posiciones -> [(x, y, ancho, alto), ...]
def calcularLayout(proporciones,anchoDisponible, altoObjetivoFila, gap):
    filas = agruparEnFilas(proporciones, anchoDisponible, altoObjetivoFila, gap)
    rectangulos = calcularRectangulos(filas, anchoDisponible, gap,altoObjetivoFila)
    return rectangulos

#Decide q imagenes van juntas en cada columna
def agruparEnFilas(proporciones, anchoDisponible, alturaObjetivo, gap):
    filas = []
    filaActual = []

    for proporcion in proporciones:
        n_imagenes = len(filaActual) + 1
        suma_proporciones = sum(filaActual) + proporcion
        anchoFilas = suma_proporciones * alturaObjetivo + gap * (n_imagenes - 1)

        if anchoFilas > anchoDisponible and len(filaActual) > 0:
            filas.append(filaActual)
            filaActual = [proporcion]
        else:
            filaActual.append(proporcion)

    if len(filaActual) > 0:
        filas.append(filaActual)

    return filas

def calcularRectangulos(filas, anchoDisponible, gap, alturaObjetivo):
    factorAlturaMaxima = 1.5
    factorAlturaMinima = 0.8
    rectangulos = []
    yActual = 0
    altura_maxima = alturaObjetivo * factorAlturaMaxima
    altura_minima = alturaObjetivo * factorAlturaMinima

    for fila in filas:
        n = len(fila)
        sumaProporciones = sum(fila)

        alturaReal = (anchoDisponible - gap * (n - 1)) / sumaProporciones
        alturaReal = max(min(alturaReal, altura_maxima), altura_minima)

        anchoOcupado = sumaProporciones * alturaReal + gap * (n - 1)
        margenLateral = (anchoDisponible - anchoOcupado) / 2

        xActual = margenLateral

        for proporcion in fila:
            anchoImagen = proporcion * alturaReal
            rectangulos.append((xActual, yActual, anchoImagen, alturaReal))
            xActual += anchoImagen + gap

        yActual += alturaReal + gap

    return rectangulos

def ajustarAltoDisponible(proporciones, anchoDisponible, altoDisponible, alturaObjetivoInicial, gap):
    #Sin imagenes que colocar (pool vacio o todas las carpetas deshabilitadas):
    #no hay nada que calcular. Sin esta guarda, el max() de mas abajo revienta
    #con "ValueError: max() iterable argument is empty" en cuanto la ventana
    #se muestra o redimensiona con el collage vacio.
    if not proporciones:
        return []

    bajo = 50
    alto = altoDisponible * 2
    mejorResultado = None

    for _ in range(30):
        medio = (bajo + alto) / 2
        rectangulos = calcularLayout(proporciones, anchoDisponible, medio, gap)
        altoTotal = max(y + altoImagen for (x, y, ancho, altoImagen) in rectangulos)

        if altoTotal <= altoDisponible:
            mejorResultado = rectangulos
            bajo = medio
        else:
            alto = medio

    altoTotalFinal = max(y + altoImagen for (x, y, ancho, altoImagen) in mejorResultado)
    offsetY = (altoDisponible - altoTotalFinal) / 2

    return [(x, y + offsetY, ancho, altoImagen) for (x, y, ancho, altoImagen) in mejorResultado]

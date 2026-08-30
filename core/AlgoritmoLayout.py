
#ENTRADA:
#   proporciones: Lista de las proporciones(ancho/alto) de las imagenes
#   anchoDisponible: Ancho disponible en ventana
#   altoObjetivoFila: Altura objetivo de la fila(altura maxima de la ventana)
#   gap: separacion entre imagenes.
#SALIDA:
#   Lista de rectangulos(uno por imagen), con sus posiciones -> [(x, y, ancho, alto), ...]
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
    rectangulos = []
    yActual = 0
    altura_maxima = alturaObjetivo * factorAlturaMaxima

    for fila in filas:
        n = len(fila)
        sumaProporciones = sum(fila)

        alturaReal = (anchoDisponible - gap * (n - 1)) / sumaProporciones
        alturaReal = min(alturaReal, altura_maxima)

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
    alturaObjetivo = alturaObjetivoInicial

    while alturaObjetivo > 50:
        rectangulos = calcularLayout(proporciones, anchoDisponible, alturaObjetivo, gap)
        altoTotal = max(y + alto for (x, y, ancho, alto) in rectangulos)

        if altoTotal > altoDisponible:
            alturaObjetivo *= 0.9
        else:
            return rectangulos

    return rectangulos
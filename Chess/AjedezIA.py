import random

puntuacionPieza = {"R": 0, "Q": 10, "T": 5, "A": 3, "C": 3, "P": 1}

puntuacionCaballo = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                     [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                     [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                     [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                     [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                     [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                     [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                     [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

puntuacionAlfil = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                   [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                   [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                   [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                   [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                   [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                   [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                   [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

puntuacionTorres = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                    [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

puntuacionReina = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                   [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                   [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                   [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                   [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                   [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                   [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                   [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

puntuacionPeon = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
                  [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                  [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                  [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                  [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                  [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                  [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                  [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

puntuacionesPosicionPiezas = {"bC": puntuacionCaballo,
                              "nC": puntuacionCaballo[::-1],
                              "bA": puntuacionAlfil,
                              "nA": puntuacionAlfil[::-1],
                              "bQ": puntuacionReina,
                              "nQ": puntuacionReina[::-1],
                              "bT": puntuacionTorres,
                              "nT": puntuacionTorres[::-1],
                              "bP": puntuacionPeon,
                              "nP": puntuacionPeon[::-1]}

JAQUEMATE = 1000
TABLAS = 0
PROF = 2


def encontrarMovimientoRandom(movimientosValidos):
    return random.choice(movimientosValidos)


def encontrarMejorMovnoRecurcion(estadoJuego, movValidos):
    multiplicarTurno = 1 if estadoJuego.movimientoBlanca else -1
    puntuacionMax = -JAQUEMATE
    mejorMov = None
    for movimientoJugador in movValidos:
        estadoJuego.hacerMovimiento(movimientoJugador)
        if estadoJuego.jaqueMate:
            puntaje = JAQUEMATE
        elif estadoJuego.tablas:
            puntaje = TABLAS
        else:
            puntaje = multiplicarTurno * puntuacionMaterial(estadoJuego.tablero)
        if puntaje > puntuacionMax:
            puntaje = puntuacionMax
            mejorMov = movimientoJugador
        estadoJuego.deshacerMovimiento()
    return mejorMov


def encontrarMejorMovimiento(estadoJuego, movValidos, return_queue):
    global movimientoSiguiente
    movimientoSiguiente = None
    random.shuffle(movValidos)
    # encontrarMovimientoRandom(movValidos)
    # encontrarMovimimientoMinMax(estadoJuego,movValidos,PROF , estadoJuego.movimientoBlanca)
    # encontrarMovMegaMax(estadoJuego, movValidos, PROF, 1 if estadoJuego.movimientoBlanca else -1)
    encontrarMovMaxAlfaBeta(estadoJuego, movValidos, PROF, -JAQUEMATE, JAQUEMATE,
                            1 if estadoJuego.movimientoBlanca else -1)
    return_queue.put(movimientoSiguiente)


def encontrarMovimimientoMinMax(estadoJuego, movValidos, profundidad, movimientoJugador):
    global movimientoSiguiente
    if profundidad == 0:
        return puntuacionMaterial(estadoJuego.tablero)
    if movimientoJugador:
        puntuacionMax = -JAQUEMATE
        for mov in movValidos:
            estadoJuego.hacerMovimiento(mov)
            movimientosSiguientes = estadoJuego.traerMovimietosValidos()
            puntuacion = encontrarMovimimientoMinMax(estadoJuego, movimientosSiguientes, profundidad - 1, False)
            if puntuacion > puntuacionMax:
                puntuacionMax = puntuacion
                if profundidad == PROF:
                    movimientoSiguiente = mov
            estadoJuego.movAnterior()
        return puntuacionMax

    else:
        puntuacionMin = JAQUEMATE
        for mov in movValidos:
            estadoJuego.hacerMovimiento(mov)
            movimientosSiguientes = estadoJuego.traerMovimietosValidos()
            puntuacion = encontrarMovimimientoMinMax(estadoJuego, movimientosSiguientes, profundidad - 1, True)
            if puntuacion < puntuacionMin:
                puntuacionMax = puntuacion
                if profundidad == PROF:
                    movimientoSiguiente = mov
            estadoJuego.movAnterior()
        return puntuacionMin


def encontrarMovMegaMax(estadoJuego, movValidos, profundidad, multiplicadorTUrno):
    global movimientoSiguiente
    if profundidad == 0:
        return multiplicadorTUrno * puntuarTablero(estadoJuego)
    puntuacionMax = -JAQUEMATE
    for mov in movValidos:
        estadoJuego.hacerMovimiento(mov)
        movimientoSiguiente = estadoJuego.traerMovimientosValidos()
        puntuacion = -encontrarMovMegaMax(estadoJuego, movimientoSiguiente, profundidad - 1, -multiplicadorTUrno)
        if puntuacion > puntuacionMax:
            puntuacionMax = puntuacion
            if profundidad == PROF:
                movimientoSiguiente = mov

        estadoJuego.deshacerMovimiento()
    return puntuacionMax


def encontrarMovMaxAlfaBeta(estadoJuego, movValidos, profundidad, alfa, beta, multiplicadorTurno):
    global movSiguiente
    if profundidad == 0:
        return multiplicadorTurno * puntuarTablero(estadoJuego)

    max_score = -JAQUEMATE
    for move in movValidos:
        estadoJuego.hacerMovimiento(move)
        next_moves = estadoJuego.traerMovimientosValidos()
        score = -encontrarMovMaxAlfaBeta(estadoJuego, next_moves, profundidad - 1, -beta, -alfa, -multiplicadorTurno)
        if score > max_score:
            max_score = score
            if profundidad == PROF:
                movSiguiente = move
        estadoJuego.deshacerMovimiento()
        if max_score > alfa:
            alfa = max_score
        if alfa >= beta:
            break
    return max_score


'''
UN puntaje Positivo es bueno para las blancas y uno negativo, bueno para las negras
'''


def puntuarTablero(estadoJuego):
    if estadoJuego.jaqueMate:
        if estadoJuego.movimientoBlanca:
            return -JAQUEMATE
        else:
            return JAQUEMATE
    elif estadoJuego.tablas:
        return TABLAS
    puntuacion = 0
    for f in range(len(estadoJuego.tablero)):
        for c in range(len(estadoJuego.tablero[f])):
            pieza = estadoJuego.tablero[f][c]
            if pieza != "--":
                puntuacionPosicionPieza = 0
                if pieza[1] != "R":
                    puntuacionPosicionPieza = puntuacionesPosicionPiezas[pieza][f][c]
                if pieza[0] == 'b':
                    puntuacion += puntuacionPieza[pieza[1]] + puntuacionPosicionPieza
                if pieza[0] == 'n':
                    puntuacion -= puntuacionPieza[pieza[1]] + puntuacionPosicionPieza

    return puntuacion


'''
Puntuar el tablero basado en el material
'''


def puntuacionMaterial(tablero):
    puntuacion = 0
    for f in tablero:
        for cuadrado in f:
            if cuadrado[0] == 'b':
                puntuacion += puntuacionPieza[cuadrado[1]]
            elif cuadrado[0] == 'n':
                puntuacion -= puntuacionPieza[cuadrado[1]]

    return puntuacion
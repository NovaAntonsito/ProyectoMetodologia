import random

puntuacionPieza = {"R": 0, "Q": 9, "T": 5, "A": 3, "C": 3, "P": 1}

puntosCaballo = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

puntosAlfil = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
               [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
               [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
               [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
               [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
               [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
               [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
               [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

puntosTorre = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

puntosReina = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
               [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
               [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
               [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
               [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
               [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
               [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
               [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

puntosPeon = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
              [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
              [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
              [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
              [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
              [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
              [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
              [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

puntuacionPorPieza = {"bC": puntosCaballo,
                         "nC": puntosCaballo[::-1],
                         "bA": puntosAlfil,
                         "nA": puntosAlfil[::-1],
                         "bQ": puntosReina,
                         "nQ": puntosReina[::-1],
                         "bT": puntosTorre,
                         "nT": puntosTorre[::-1],
                         "bP": puntosPeon,
                         "nP": puntosPeon[::-1]}

JAQUEMATE = 1000
TABLAS = 0
PROF = 3


def encontrarMejorMovimiento(estadoJuego, movValidos, pila):
    global movSiguiente
    movSiguiente = None
    random.shuffle(movValidos)
    mejorMovimientoInteleginete(estadoJuego, movValidos, PROF, -JAQUEMATE, JAQUEMATE,
                             1 if estadoJuego.movimientoBlanca else -1)
    pila.put(movSiguiente)


def mejorMovimientoInteleginete(estadoJuego, movValidos, profundidad, alpha, beta, posibilidad):
    global movSiguiente
    if profundidad == 0:
        return posibilidad * puntuacionTablero(estadoJuego)
    puntuacionMax = -JAQUEMATE
    for movimiento in movValidos:
        estadoJuego.hacerMovimiento(movimiento)
        movSiguientes = estadoJuego.traerMovimientosValidos()
        puntuacion = -mejorMovimientoInteleginete(estadoJuego, movSiguientes, profundidad - 1, -beta, -alpha, -posibilidad)
        if puntuacion > puntuacionMax:
            puntuacionMax = puntuacion
            if profundidad == PROF:
                movSiguiente = movimiento
        estadoJuego.deshacerMovimiento()
        if puntuacionMax > alpha:
            alpha = puntuacionMax
        if alpha >= beta:
            break
    return puntuacionMax


def puntuacionTablero(estadoJuego):
    if estadoJuego.jaqueMate:
        if estadoJuego.movimientoBlanca:
            return -JAQUEMATE
        else:
            return JAQUEMATE 
    elif estadoJuego.tablas:
        return TABLAS
    puntuacion = 0
    for fila in range(len(estadoJuego.tablero)):
        for col in range(len(estadoJuego.tablero[fila])):
            pieza = estadoJuego.tablero[fila][col]
            if pieza != "--":
                puntuacionPiezaEnPosicion = 0
                if pieza[1] != "R":
                    puntuacionPiezaEnPosicion = puntuacionPorPieza[pieza][fila][col]
                if pieza[0] == "b":
                    puntuacion += puntuacionPieza[pieza[1]] + puntuacionPiezaEnPosicion
                if pieza[0] == "n":
                    puntuacion -= puntuacionPieza[pieza[1]] + puntuacionPiezaEnPosicion

    return puntuacion


def encontrarMovRandom(movValidos):
    return random.choice(movValidos)

import random

rangoPieza = {"R": 0, "Q": 10, "T": 5, "A": 3, "C": 3, "P": 1}
jaqueMate = 1000
tablas = 0


def encontrarMovimientoRandom(movimientosValidos):
    return movimientosValidos[random.randint(0, len(movimientosValidos) - 1)]


def encontrarMejorMov(estadoJuego, movValidos):
    multiplicarTurno = 1 if estadoJuego.movimientoBlanca else -1
    puntuacionMax = -jaqueMate
    mejorMov = None
    for movimientoJugador in movValidos:
        estadoJuego.hacerMovimiento(movimientoJugador)
        if estadoJuego.enJaque():
            puntaje = jaqueMate
        elif estadoJuego.tablas():
            puntaje = tablas
        else:
            puntaje = multiplicarTurno * puntuacionMaterial(estadoJuego.tablero)
        if puntaje > puntuacionMax:
            puntaje = puntuacionMax
            mejorMov = movimientoJugador
    return mejorMov

'''
Puntuar el tablero basado en el material
'''


def puntuacionMaterial(tablero):
    puntuacion = 0
    for f in tablero:
        for cuadrado in f:
            if cuadrado[0] == 'b':
                puntuacion += rangoPieza[cuadrado[1]]
            elif cuadrado[0] == 'n':
                puntuacion -= rangoPieza[cuadrado[1]]

    return puntuacion

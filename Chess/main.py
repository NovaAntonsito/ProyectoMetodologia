import pygame as p
from Chess import Engine

# Settings iniciales para PYGAME
p.init()
ANCHO = ALTO = 512
DIMENSION = 8
SQ_SIZE = ANCHO // DIMENSION
MAX_FPS = 15
IMAGENES = {}


def cargarImagenes():
    # Transformar las imagenes a una escala para el tablero
    IMAGENES["nA"] = p.transform.scale(
        p.image.load("imagenes/nA.png"), (SQ_SIZE, SQ_SIZE))
    IMAGENES["nC"] = p.transform.scale(
        p.image.load("imagenes/nC.png"), (SQ_SIZE, SQ_SIZE))
    IMAGENES["nT"] = p.transform.scale(
        p.image.load("imagenes/nT.png"), (SQ_SIZE, SQ_SIZE))
    IMAGENES["nQ"] = p.transform.scale(
        p.image.load("imagenes/nQ.png"), (SQ_SIZE, SQ_SIZE))
    IMAGENES["nR"] = p.transform.scale(
        p.image.load("imagenes/nR.png"), (SQ_SIZE, SQ_SIZE))
    IMAGENES["nP"] = p.transform.scale(
        p.image.load("imagenes/nP.png"), (SQ_SIZE, SQ_SIZE))
    IMAGENES["bA"] = p.transform.scale(
        p.image.load("imagenes/bA.png"), (SQ_SIZE, SQ_SIZE))
    IMAGENES["bC"] = p.transform.scale(
        p.image.load("imagenes/bC.png"), (SQ_SIZE, SQ_SIZE))
    IMAGENES["bT"] = p.transform.scale(
        p.image.load("imagenes/bT.png"), (SQ_SIZE, SQ_SIZE))
    IMAGENES["bQ"] = p.transform.scale(
        p.image.load("imagenes/bQ.png"), (SQ_SIZE, SQ_SIZE))
    IMAGENES["bR"] = p.transform.scale(
        p.image.load("imagenes/bR.png"), (SQ_SIZE, SQ_SIZE))
    IMAGENES["bP"] = p.transform.scale(
        p.image.load("imagenes/bP.png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    pantalla = p.display.set_mode((ANCHO, ALTO))
    reloj = p.time.Clock()
    pantalla.fill(p.Color(255, 255, 255))
    estadoJuego = Engine.EstadoJuego()
    movimientosValidos = estadoJuego.traerMovimietosValidos()
    movRealizado = False
    p.display.set_caption("Ajedrez Grupo H")
    logo = p.image.load("imagenes/logo.png")
    p.display.set_icon(logo)
    cargarImagenes()
    ejecutando = True
    posicionAnterior = ()
    clicksJugador = []
    while ejecutando:
        for e in p.event.get():
            if e.type == p.QUIT:
                ejecutando = False
            elif e.type == p.MOUSEBUTTONDOWN:
                posicion = p.mouse.get_pos()  # posicion (x,y)
                col = posicion[0] // SQ_SIZE
                fil = posicion[1] // SQ_SIZE
                if posicionAnterior == (fil, col):
                    posicionAnterior = ()
                    clicksJugador = []
                else:
                    posicionAnterior = (fil, col)
                    clicksJugador.append(posicionAnterior)
                if len(clicksJugador) == 2:
                    mover = Engine.Mover(
                        clicksJugador[0], clicksJugador[1], estadoJuego.tablero)
                    print(mover.getNotacionAjedrez())
                    if mover in movimientosValidos:
                        estadoJuego.hacerMovimiento(mover)
                        movRealizado = True
                        posicionAnterior=()
                        clicksJugador=[]
                    else:
                        clicksJugador=[posicionAnterior]
                    posicionAnterior = ()
                    clicksJugador = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # z esta presionada
                    estadoJuego.movAnterior()
                    movRealizado = True

        if movRealizado:
            movimientosValidos = estadoJuego.traerMovimietosValidos()
            movRealizado = False

        dibujarEstado(pantalla, estadoJuego)
        reloj.tick(MAX_FPS)
        p.display.flip()


'''
Dibuja las casillas del tablero
'''


def dibujarTablero(pantalla):
    color1 = p.Color("#C5742A")
    color2 = p.Color("#EBCCAA")

    for f in range(DIMENSION):
        for c in range(DIMENSION):
            if (f + c) % 2 == 0:
                color = color2
            else:
                color = color1
            p.draw.rect(pantalla, color, p.Rect(
                c * SQ_SIZE, f * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Dibuja las piezas en el tablero utilizando el estado actual => Estado de juego
'''


def dibujarPiezas(pantalla, tablero):
    for f in range(DIMENSION):
        for c in range(DIMENSION):
            pieza = tablero[f][c]
            if pieza != "--":
                pantalla.blit(IMAGENES[pieza], p.Rect(
                    c * SQ_SIZE, f * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Responsable de todos los graficos que estan dentro del estado de juego actual
'''


def dibujarEstado(pantalla, estadoJuego):
    # Dibuja el tablero
    dibujarTablero(pantalla)
    # Previsualización posibles direcciones(Luego)

    dibujarPiezas(pantalla, estadoJuego.tablero)

    # Dibujando piezas en los casilleros de los extremos


if __name__ == "__main__":
    main()

import pygame as p
from Chess import Engine


# Settings iniciales para PYGAME
p.init()
ANCHO = ALTO = 512
DIMENSION = 8
SQ_SIZE = ANCHO // DIMENSION
MAX_FPS = 15
IMAGENES = {}
p.mixer.init()
p.mixer.music.load("Sonidos y Musica/Musica de fondo.wav")
p.mixer.music.play(-1)



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

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # z esta presionada
                    estadoJuego.movAnterior()
                    movRealizado = True

        if movRealizado:
            animacionPiezas(estadoJuego.registroMov[-1],pantalla,estadoJuego.tablero, reloj)
            movimientosValidos = estadoJuego.traerMovimietosValidos()
            movRealizado = False

        dibujarEstado(pantalla, estadoJuego, movimientosValidos, posicionAnterior)
        reloj.tick(MAX_FPS)
        p.display.flip()



'''
Dibuja las casillas del tablero
'''

#pantalla, array[]
#d1,d2
def dibujarTablero(pantalla):
      global colores
      colores = [p.Color("grey"), p.Color("white")]

      for f in range(DIMENSION):
        for c in range(DIMENSION):
            color = colores[(f + c) % 2]
            p.draw.rect(pantalla, color, p.Rect(
                c * SQ_SIZE, f * SQ_SIZE, SQ_SIZE, SQ_SIZE), 0)



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


def dibujarEstado(pantalla, estadoJuego, movimientosValidos, posicionAnterior):
    # Dibuja el tablero
    dibujarTablero(pantalla)
    LACONCHADETUMADREPYTHON(pantalla, estadoJuego, movimientosValidos, posicionAnterior)
    # Previsualización posibles direcciones(Luego)

    dibujarPiezas(pantalla, estadoJuego.tablero)
    if (estadoJuego.movimientoBlanca):
        p.display.set_caption("Ajedrez Grupo H ---- Turno Blanca")
        p.display.update()
    else:
        p.display.update()
        p.display.set_caption("Ajedrez Grupo H ---- Turno Negra")

    # Dibujando piezas en los casilleros de los extremos

'''Resaltar el movimientos de las piezas'''
def LACONCHADETUMADREPYTHON(pantalla, estadoJuego, movimientosValidos, posicionAnterior):
    if posicionAnterior != ():
        f, c = posicionAnterior
        if estadoJuego.tablero[f][c][0] == ('b' if estadoJuego.movimientoBlanca else 'n'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(128)
            s.fill(p.Color("Blue"))
            pantalla.blit(s, (c * SQ_SIZE, f * SQ_SIZE))
            s.fill(p.Color('Yellow'))
            for mover in movimientosValidos:
                if mover.filaInicial == f and mover.columnaInicial == c:
                    pantalla.blit(s, (mover.columnaFinal * SQ_SIZE, mover.filaFinal * SQ_SIZE))


def animacionPiezas(mover, pantalla, tablero, reloj):
     global colores
     dF = mover.filaFinal - mover.filaInicial
     dC = mover.columnaFinal - mover.columnaInicial
     FramesPorCuadrado = 10
     CuentaFrames = (abs(dF) + abs(dC)) * FramesPorCuadrado
     for Frames in range(CuentaFrames + 1):
         r , c =((mover.filaInicial + dF * Frames / CuentaFrames, mover.columnaInicial + dC * Frames / CuentaFrames))
         dibujarTablero(pantalla)
         dibujarPiezas(pantalla, tablero)
         color = colores [(mover.filaFinal + mover.columnaFinal) % 2]
         cuadradoFinal = p.Rect(mover.columnaFinal* SQ_SIZE, mover.filaFinal * SQ_SIZE, SQ_SIZE, SQ_SIZE)
         p.draw.rect(pantalla, color, cuadradoFinal)
         if mover.piezaCapturada != "--":
             pantalla.blit(IMAGENES[mover.piezaCapturada], cuadradoFinal)
         pantalla.blit(IMAGENES[mover.piezaMovida], p.Rect(c* SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
         p.display.flip()
         reloj.tick(60)




if __name__ == "__main__":
    main()

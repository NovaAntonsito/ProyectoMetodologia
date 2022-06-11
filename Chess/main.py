# import pygame_gui
import sys

import pygame as p
import Botones,RenderImagen
from Chess import Engine, AjedezIA
from multiprocessing import Process, Queue
import time

# Settings iniciales para PYGAME
p.init()
jugar_img = p.image.load("imagenes/JugarBotton.png")
salir_img = p.image.load("imagenes/SalirBotton.png")
regresar_img = p.image.load("imagenes/RegresarBotton.png")
jvsj_img = p.image.load("imagenes/JvsJBotton.png")
jvsIA_img = p.image.load("imagenes/JvsIABotton.png")
titulo_img = p.image.load("imagenes/TituloAjedrez.png")
reynaB_img = p.image.load("imagenes/bQ.png.")
reyB_img = p.image.load("imagenes/bR.png")
reynaN_img = p.image.load("imagenes/nQ.png.")
reyN_img = p.image.load("imagenes/nR.png")

ANCHO = ALTO = 500
MOVELOGPANELANCHO = 250
MOVELOGPANELALTO = ALTO
DIMENSION = 8
SQ_SIZE = ANCHO // DIMENSION
MAX_FPS = 15
IMAGENES = {}
p.mixer.init()
p.mixer.music.load("Sonidos/Musica de fondo.wav")
p.mixer.music.play(-1)
p.mixer.music.set_volume(0.050)
PANTALLA_MENU = (ANCHO , ALTO)
PANTALLA_AJEDREZ = (ANCHO + MOVELOGPANELANCHO, ALTO)
PANTALLA = p.display.set_mode(PANTALLA_AJEDREZ)





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
    juegoCorriendo = True
    menu = True
    # Variables para el ajedrez
    jugador1 = True
    jugador2 = False

    while juegoCorriendo:
        if not menu:
            PANTALLA = p.display.set_mode(PANTALLA_AJEDREZ)

            BG = p.transform.scale(p.image.load("imagenes/fondo.png"), (SQ_SIZE, SQ_SIZE))
            reloj = p.time.Clock()
            PANTALLA.fill(p.Color(255, 255, 255))
            estadoJuego = Engine.EstadoJuego()
            movimientosValidos = estadoJuego.traerMovimientosValidos()
            movRealizado = False
            animar = False
            pausar = p.mixer.music.get_busy()
            juegoTerminado = False
            moveLogFuentes = p.font.SysFont("Console", 15, False, False)
            moveLogTimer = p.font.SysFont("Console", 20, True, False)
            modoB = False

            pensamientoIa = False
            movimientoRehecho = False
            encontrarmov = None
            logo = p.image.load("imagenes/logo.png")
            p.display.set_icon(logo)
            cargarImagenes()
            ejecutando = True
            posicionAnterior = ()
            clicksJugador = []
            p.time.set_timer(p.USEREVENT, 1000)

            while ejecutando:
                if not juegoTerminado:
                    turnoHumano = (estadoJuego.movimientoBlanca and jugador1) or (not estadoJuego.movimientoBlanca and jugador2)

                for e in p.event.get():
                    if not juegoTerminado:
                        if e.type == p.USEREVENT:
                            if estadoJuego.movimientoBlanca:
                                estadoJuego.contadorBlanca -= 1
                                m, s = divmod(estadoJuego.contadorBlanca, 60)
                                print("Timer Blanca: "+'{:02d}:{:02d}'.format(m, s))
                            else:
                                estadoJuego.contadorNegra -= 1
                                m, s = divmod(estadoJuego.contadorNegra, 60)
                                print("Timer Negra: "+'{:02d}:{:02d}'.format(m, s))

                    if e.type == p.QUIT:
                        p.quit()
                        sys.exit()
                    elif e.type == p.MOUSEBUTTONDOWN:
                        if not juegoTerminado:
                            '''if e.type == p.QUIT:
                                ejecutando = False
                                juegoCorriendo = False
                               '''
                            if not juegoTerminado and turnoHumano:
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
                                    for i in range(len(movimientosValidos)):
                                        if mover == movimientosValidos[i]:
                                            estadoJuego.hacerMovimiento(movimientosValidos[i])
                                            movRealizado = True
                                            animar = True
                                            posicionAnterior = ()
                                            clicksJugador = []
                                    if not movRealizado:
                                        clicksJugador = [posicionAnterior]
                    elif e.type == p.KEYDOWN:
                        if e.key == p.K_z:  # z esta presionada
                            estadoJuego.deshacerMovimiento()
                            movRealizado = True
                            animar = False
                            juegoTerminado = False
                            if pensamientoIa:
                                encontrarmov.terminate()
                                pensamientoIa = False
                            movimientoRehecho = True
                        if e.key == p.K_r:
                            estadoJuego = Engine.EstadoJuego()
                            estadoJuego.contadorBlanca = estadoJuego.contadorInicial
                            estadoJuego.contadorBlanca = estadoJuego.contadorInicial
                            movimientosValidos = estadoJuego.traerMovimientosValidos()
                            posicionAnterior = ()
                            clicksJugador = []
                            movRealizado = False
                            animar = False
                            juegoTerminado = False
                            if pensamientoIa:
                                encontrarmov.terminate()
                                pensamientoIa = False
                            movimientoRehecho = True
                        if e.key == p.K_b:
                            p.mixer.quit()
                            p.mixer.init()
                            p.mixer.music.load("Sonidos/easteregg.wav")
                            p.mixer.music.play(-1)
                            modoB = True
                        if e.key == p.K_m:
                            p.mixer.music.set_volume(p.mixer.music.get_volume() + 0.05)
                        if e.key == p.K_n:
                            p.mixer.music.set_volume(p.mixer.music.get_volume() - 0.05)
                        if e.key == p.K_t:
                            if pausar:
                                p.mixer.music.pause()
                            else:
                                p.mixer.music.unpause()
                        pausar = not pausar

                # logica ia
                if not juegoTerminado and not turnoHumano and not movimientoRehecho:
                    if not pensamientoIa:
                        pensamientoIa = True
                        return_queue = Queue()
                        encontrarmov = Process(target=AjedezIA.encontrarMejorMovimiento,
                                               args=(estadoJuego, movimientosValidos, return_queue))
                        encontrarmov.start()

                    if not encontrarmov.is_alive():
                        movimientoIA = return_queue.get()
                        if movimientoIA is None:
                            movimientoIA = AjedezIA.encontrarMovimientoRandom(movimientosValidos)
                        estadoJuego.hacerMovimiento(movimientoIA)
                        movRealizado = True
                        animar = True
                        pensamientoIa = False

                if movRealizado:

                    if animar:
                        animacionPiezas(estadoJuego.registroMov[-1], PANTALLA, estadoJuego.tablero, reloj, modoB)
                    movimientosValidos = estadoJuego.traerMovimientosValidos()
                    movRealizado = False
                    animar = False
                    movimientoRehecho = False

                dibujarEstado(PANTALLA, estadoJuego, movimientosValidos, posicionAnterior, moveLogFuentes,moveLogTimer, modoB)

                if estadoJuego.jaqueMate or estadoJuego.tablas or estadoJuego.contadorBlanca == 0 or estadoJuego.contadorNegra == 0:
                    juegoTerminado = True
                    if estadoJuego.tablas:
                        mensaje = "empate"
                        dibujarTextos(PANTALLA, mensaje)
                    elif estadoJuego.jaqueMate:
                        if estadoJuego.movimientoBlanca:
                            mensaje = "Negro gana por jaque"
                            dibujarTextos(PANTALLA, mensaje)
                        else:
                            mensaje = "Blanca gana por jaque"
                            dibujarTextos(PANTALLA, mensaje)
                    else:
                        if estadoJuego.movimientoBlanca:
                            mensaje = "Negro gana por tiempo"
                            dibujarTextos(PANTALLA, mensaje)
                        else:
                            mensaje = "Blanca gana por tiempo"
                            dibujarTextos(PANTALLA, mensaje)
                reloj.tick(MAX_FPS)
                p.display.flip()

                p.display.update()
        else:
            print("Menu")
            PANTALLA = p.display.set_mode(PANTALLA_MENU)
            print(PANTALLA.get_width())
            PANTALLA.fill(p.Color("Orange"))
            ejecutandoMenu = True
            tituloComponente = RenderImagen.imagen((PANTALLA.get_width()/2)-(titulo_img.get_width()*4)/2, 20, titulo_img, 4)
            reyB_Componente = RenderImagen.imagen(0,PANTALLA.get_height()-reyB_img.get_height(),reyB_img,1)
            reynaB_Componente = RenderImagen.imagen(PANTALLA.get_width()-reynaB_img.get_width(),0,reynaB_img,1)
            reyN_Componente = RenderImagen.imagen(PANTALLA.get_width()-reyN_img.get_width(),PANTALLA.get_height()-reyN_img.get_height(),reyN_img,1)
            reynaN_Componente = RenderImagen.imagen(0,0,reynaN_img,1)


            boton_salir = Botones.boton((PANTALLA.get_width()/2)-(salir_img.get_width()), 250, salir_img, 2)

            boton_JvsIA = Botones.boton(20, 150, jvsIA_img, 2)
            boton_JvsJ = Botones.boton(PANTALLA.get_width()-(jvsj_img.get_width()*2)-20, 150, jvsj_img, 2)
            while ejecutandoMenu:
                tituloComponente.draw(PANTALLA)
                reyB_Componente.draw(PANTALLA)
                reyB_Componente.draw(PANTALLA)
                reynaB_Componente.draw(PANTALLA)
                reyN_Componente.draw(PANTALLA)
                reynaN_Componente.draw(PANTALLA)
                if boton_JvsJ.draw(PANTALLA):
                    jugador2 = True
                    ejecutandoMenu = False
                    menu = False
                if boton_JvsIA.draw(PANTALLA):
                    jugador2 = False
                    ejecutandoMenu = False
                    menu = False
                if boton_salir.draw(PANTALLA):
                    ejecutandoMenu = False
                    juegoCorriendo = False
                for e in p.event.get():
                    if e.type == p.QUIT:
                        ejecutandoMenu = False
                        juegoCorriendo = False
                p.display.update()


'''
Dibuja las casillas del tablero
'''


def dibujarMoveLog(pantalla, estadoJuego, moveLogFuentes,moveLogTimer, modoB):
    moveLogPantalla = p.Rect(ANCHO, 0, MOVELOGPANELANCHO, MOVELOGPANELALTO)
    p.draw.rect(pantalla, p.Color("black"), moveLogPantalla)
    moveLog = estadoJuego.registroMov
    texto1 = "ee"
    moveTexto = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2 + 1) + ", " + moveLog[i].getNotacionAjedrez() + " "
        if i + 1 < len(moveLog):
            moveString += moveLog[i + 1].getNotacionAjedrez()
        moveTexto.append(moveString)
    relleno = 5
    espacioEntre = 2
    textoY = relleno
    mB, sB = divmod(estadoJuego.contadorBlanca, 60)
    mN, sN = divmod(estadoJuego.contadorNegra, 60)
    textoNegra = "Timer Negra:" + '{:02d}:{:02d}'.format(mN, sN)
    mensajePantalla = moveLogTimer.render(textoNegra, True, p.Color("White"))
    ubicacionTexto = moveLogPantalla.move(relleno, textoY)
    textoY += mensajePantalla.get_height() + espacioEntre
    pantalla.blit(mensajePantalla, ubicacionTexto)

    textoBlanca = "Timer Blanca:" + '{:02d}:{:02d}'.format(mB, sB)
    mensajePantalla = moveLogTimer.render(textoBlanca, True, p.Color("White"))
    ubicacionTexto = moveLogPantalla.move(relleno, textoY)
    textoY += mensajePantalla.get_height() + espacioEntre
    pantalla.blit(mensajePantalla, ubicacionTexto)

    if (estadoJuego.movimientoBlanca):
        texto1 = "Turno Blanca"
        mensajePantalla = moveLogFuentes.render(texto1, True, p.Color("White"))
        ubicacionTexto = moveLogPantalla.move(MOVELOGPANELANCHO/2-50, textoY)
        textoY += mensajePantalla.get_height() + espacioEntre
        pantalla.blit(mensajePantalla, ubicacionTexto)

    else:
        texto1 = "Turno Negra"
        mensajePantalla = moveLogFuentes.render(texto1, True, p.Color("White"))
        ubicacionTexto = moveLogPantalla.move(MOVELOGPANELANCHO/2-50, textoY)
        textoY += mensajePantalla.get_height() + espacioEntre
        pantalla.blit(mensajePantalla, ubicacionTexto)
    if modoB:
        MODOBOCA = "VAMO BOQUITA"
        mensajePantalla = moveLogFuentes.render(MODOBOCA, True, p.Color("White"))
        ubicacionTexto = moveLogPantalla.move(relleno, textoY)
        textoY += mensajePantalla.get_height() + espacioEntre
        pantalla.blit(mensajePantalla, ubicacionTexto)
    for i in range(len(moveTexto)):
        text = moveTexto[i]
        mensajePantalla = moveLogFuentes.render(text, True, p.Color("White"))
        ubicacionTexto = moveLogPantalla.move(relleno, textoY)
        pantalla.blit(mensajePantalla, ubicacionTexto)
        textoY += mensajePantalla.get_height() + espacioEntre

    espacioEntre = 20




def dibujarTablero(pantalla, modoB=False):
    global colores
    if (modoB):
        colores = [p.Color("#F3A717"), p.Color("#0E457F")]
        for f in range(DIMENSION):
            for c in range(DIMENSION):
                color = colores[(f + c) % 2]
                p.draw.rect(pantalla, color, p.Rect(
                    c * SQ_SIZE, f * SQ_SIZE, SQ_SIZE, SQ_SIZE), 0)
    else:
        colores = [p.Color("#C5742A"), p.Color("#EBCCAA")]
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


def dibujarEstado(pantalla, estadoJuego, movimientosValidos, posicionAnterior, moveLogFuentes,moveLogTimer, modoB=False):
    # Dibuja el tablero
    dibujarTablero(pantalla, modoB)
    resaltarMovimientos(pantalla, estadoJuego, movimientosValidos, posicionAnterior)
    dibujarMoveLog(pantalla, estadoJuego, moveLogFuentes,moveLogTimer, modoB)
    dibujarPiezas(pantalla, estadoJuego.tablero)

    # Dibujando piezas en los casilleros de los extremos


'''Resaltar el movimientos de las piezas'''


def resaltarMovimientos(pantalla, estadoJuego, movimientosValidos, posicionAnterior):
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


def animacionPiezas(mover, pantalla, tablero, reloj, modoB=False):
    dF = mover.filaFinal - mover.filaInicial
    dC = mover.columnaFinal - mover.columnaInicial
    FramesPorCuadrado = 10
    CuentaFrames = (abs(dF) + abs(dC)) * FramesPorCuadrado
    for Frames in range(CuentaFrames + 1):
        r, c = ((mover.filaInicial + dF * Frames / CuentaFrames, mover.columnaInicial + dC * Frames / CuentaFrames))
        dibujarTablero(pantalla, modoB)
        dibujarPiezas(pantalla, tablero)
        color = colores[(mover.filaFinal + mover.columnaFinal) % 2]
        cuadradoFinal = p.Rect(mover.columnaFinal * SQ_SIZE, mover.filaFinal * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(pantalla, color, cuadradoFinal)
        if mover.piezaCapturada != "--":
            if mover.movimientoCapturaAlPaso:
                capturaAlPasoFila = (mover.filaFinal + 1) if mover.piezaCapturada[0] == 'n' else (mover.filaFinal - 1)
                cuadradoFinal = p.Rect(mover.columnaFinal * SQ_SIZE, capturaAlPasoFila * SQ_SIZE, SQ_SIZE, SQ_SIZE)

            pantalla.blit(IMAGENES[mover.piezaCapturada], cuadradoFinal)
        if mover.piezaMovida != '--':
            pantalla.blit(IMAGENES[mover.piezaMovida], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        reloj.tick(60)


def dibujarTextos(pantalla, mensaje):
    fuente = p.font.SysFont("Helvitca", 32, True, False)
    mensajePantalla = fuente.render(mensaje, 0, p.Color("Gray"))
    ubicacionTexto = p.Rect(0, 0, ANCHO, ALTO).move(ANCHO / 2 - mensajePantalla.get_width() / 2,
                                                    ALTO / 2 - mensajePantalla.get_height() / 2)
    pantalla.blit(mensajePantalla, ubicacionTexto)


def countdown(num_of_secs):
    cantidadSecs = int(num_of_secs)
    while cantidadSecs:
        m, s = divmod(cantidadSecs, 60)
        min_sec_format = '{:02d}:{:02d}'.format(m, s)
        print(min_sec_format + '\r')
        time.sleep(1)
        cantidadSecs -= 1

    print('Countdown finished.')


if __name__ == "__main__":
    main()

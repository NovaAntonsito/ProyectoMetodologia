class EstadoJuego:
    def __init__(self):
        # el talblero es un array de 8x8, donde cada elemento tiene dos caracteres.
        # el primero refiere al color n(negro) y b(blanco)
        # el segundo refiere a la pieza que representa en el ajerez.
        self.tablero = [
            ["nT", "nC", "nA", "nQ", "nR", "nA", "nC", "nT"],
            ["nP", "nP", "nP", "nP", "nP", "nP", "nP", "nP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["bT", "bC", "bA", "bQ", "bR", "bA", "bC", "bT"]]
        self.movimientoBlanca = True
        self.registroMov = []
        # Lectura de jaques mate
        self.ubicacionReyBlanco = (0, 4)
        self.ubicacionReyNegro = (7, 4)
        self.enJaque = False
        self.clavada = []
        self.posiblesJaques = []

    '''
    Toma un movimiento como parametro y lo ejecuta
    '''

    def hacerMovimiento(self, mover):
        self.tablero[mover.filaInicial][mover.columnaInicial] = "--"
        self.tablero[mover.filaFinal][mover.columnaFinal] = mover.piezaMovida
        self.registroMov.append(mover)  # registramos el movimiento
        self.movimientoBlanca = not self.movimientoBlanca  # cambio de turno
        # Cambiar la pos del rey
        if mover.piezaMovida == "bR":
            self.ubicacionReyBlanco = (mover.filaFinal, mover.columnaFinal)
        elif mover.piezaMovida == "nR":
            self.ubicacionReyNegro = (mover.filaFinal, mover.columnaFinal)

    '''
    Rehacer el ultimo movimiento
    '''

    def movAnterior(self):
        if len(self.registroMov) != 0:
            movimiento = self.registroMov.pop()
            self.tablero[movimiento.filaInicial][movimiento.columnaInicial] = movimiento.piezaMovida
            self.tablero[movimiento.filaFinal][movimiento.columnaFinal] = movimiento.piezaCapturada
            self.movimientoBlanca = not self.movimientoBlanca
            if movimiento.piezaMovida == "bR":
                self.ubicacionReyBlanco = (movimiento.filaInicial, movimiento.columnaInicial)
            elif movimiento.piezaMovida == "nR":
                self.ubicacionReyNegro = (movimiento.filaInicial, movimiento.columnaInicial)

    def traerMovimietosValidos(self):
        movimientos = []
        self.enJaque, self.clavada, self.posiblesJaques = self.validarClavadayJaques()
        if self.movimientoBlanca:
            filaRey = self.ubicacionReyBlanco[0]
            colRey = self.ubicacionReyBlanco[1]
        else:
            filaRey = self.ubicacionReyNegro[0]
            colRey = self.ubicacionReyNegro[1]
        if self.enJaque:
            if len(self.posiblesJaques) == 1:  # Solo 1 Jaque, jaque bloqueado o movimiento de rey
                movimientos = self.traerTodosMovimientosPosibles()
                # Para bloquear un jaque debes de mover una pieza en una entre medio de los cuadrados de la pieza del enemigo y el rey
                jaque = self.posiblesJaques[0]  # informacion del Jaque
                filaValida = jaque[0]
                colValida = jaque[1]
                piezaValida = self.tablero[filaValida][colValida]  # Pieza enemiga causando el Jaque
                cuadradosValidos = []  # Cuadrados que la pieza pueda mover

                if piezaValida[1] == 'C':
                    cuadradosValidos = [(filaValida, colValida)]
                else:
                    for i in range(1, 8):
                        cuadradoValido = (
                            filaRey + jaque[2] * i,
                            colRey + jaque[3] * i)  # Jaque[2] y Jaque[3] son las direcciones del Jaque
                        cuadradosValidos.append(cuadradoValido)
                        if cuadradoValido[0] == filaValida and cuadradoValido[1] == colValida:
                            break

                for i in range(len(movimientos) - 1, -1, -1):
                    if movimientos[i].piezaMovida[1] != 'R':
                        if not (movimientos[i].TerminarFila, movimientos[i].TerminarCol) in cuadradosValidos:
                            movimientos.remove(movimientos[i])
            else:
                self.getMovimientoRey(filaRey, colRey, movimientos)
        else:
            self.traerMovimietosValidos()

        return movimientos

    # Determinar si el jugador esta en jaque
    def enJaque(self):
        if self.movimientoBlanca:
            return self.cuadradoBajoAtaque(self.ubicacionReyBlanco[0], self.ubicacionReyBlanco[1])
        else:
            return self.cuadradoBajoAtaque(self.ubicacionReyNegro[0], self.ubicacionReyNegro[1])

    def cuadradoBajoAtaque(self, f, c):
        self.movimientoBlanca = not self.movimientoBlanca
        movEnemigo = self.traerTodosMovimientosPosibles()
        self.movimientoBlanca = not self.movimientoBlanca
        for mov in movEnemigo:
            if mov.filaFinal == f and mov.columnaFinal == c:
                self.movimientoBlanca = not self.movimientoBlanca
                return True
        return False

    '''
    MOVIMIENTOS
    '''

    def traerTodosMovimientosPosibles(self):
        movimientos = []
        for f in range(len(self.tablero)):
            for c in range(len(self.tablero[f])):
                turno = self.tablero[f][c][0]
                if (turno == 'b' and self.movimientoBlanca) or (
                        turno == "n" and not self.movimientoBlanca):

                    pieza = self.tablero[f][c][1]
                    if pieza == 'P':
                        self.getMovimientoPeon(f, c, movimientos)
                    elif pieza == 'T':
                        self.getMovimientoTorre(f, c, movimientos)
                    elif pieza == 'A':
                        self.getMovimientosAlfil(f, c, movimientos)
                    elif pieza == 'C':
                        self.getMovimientoCaballo(f, c, movimientos)
                    elif pieza == 'Q':
                        self.getMovimientoQueen(f, c, movimientos)
                    elif pieza == 'R':
                        self.getMovimientoRey(f, c, movimientos)

        return movimientos

    '''
    obtener todos los movimentos por el peon selecionado
    '''

    def getMovimientoPeon(self, f, c, movimientos):
        if self.movimientoBlanca:
            if self.tablero[f - 1][c] == "--":
                movimientos.append(Mover((f, c), (f - 1, c), self.tablero))
                if f == 6 and self.tablero[f - 2][c] == "--":
                    movimientos.append(Mover((f, c), (f - 2, c), self.tablero))
            if c - 1 >= 0:
                if self.tablero[f - 1][c - 1][0] == 'n':
                    movimientos.append(Mover((f, c), (f - 1, c - 1), self.tablero))
            if c + 1 <= 7:
                if self.tablero[f - 1][c + 1][0] == 'n':
                    movimientos.append(Mover((f, c), (f - 1, c + 1), self.tablero))
        else:
            if self.tablero[f + 1][c] == "--":
                movimientos.append(Mover((f, c), (f + 1, c), self.tablero))
                if f == 1 and self.tablero[f + 2][c] == "--":
                    movimientos.append(Mover((f, c), (f + 2, c), self.tablero))
                if c - 1 >= 0:
                    if self.tablero[f + 1][c - 1][0] == 'b':
                        movimientos.append(Mover((f, c), (f + 1, c - 1), self.tablero))
                if c + 1 <= 7:
                    if self.tablero[f + 1][c + 1][0] == 'b':
                        movimientos.append(Mover((f, c), (f + 1, c + 1), self.tablero))

    ''' 
    obtener todos los movimentos por la torre selecionada
    '''

    def getMovimientoTorre(self, f, c, moves):
        dirreciones = ((-1, 0), (0, -1), (1, 0), (0, 1))
        colorEnemigo = 'n' if self.movimientoBlanca else 'b'

        for d in dirreciones:
            for i in range(1, 8):
                finalFil = f + d[0] * i
                finalCol = c + d[1] * i

                if 0 <= finalFil < 8 and 0 <= finalCol < 8:
                    finalPieza = self.tablero[finalFil][finalCol]
                    if finalPieza == "--":
                        moves.append(Mover((f, c), (finalFil, finalCol), self.tablero))
                    elif finalPieza[0] == colorEnemigo:
                        moves.append(Mover((f, c), (finalFil, finalCol), self.tablero))
                        break
                    else:
                        break
                else:
                    break

    def getMovimientosAlfil(self, f, c, moves):
        dirreciones = ((-1, -1), (1, 1), (-1, 1), (-1, 1))
        colorEnemigo = 'n' if self.movimientoBlanca else 'b'

        for d in dirreciones:
            for i in range(1, 8):
                finalFil = f + d[0] * i
                finalCol = c + d[1] * i
                if 0 <= finalFil < 8 and 0 <= finalCol < 8:
                    finalPieza = self.tablero[finalFil][finalCol]
                    if finalPieza == "--":
                        moves.append(Mover((f, c), (finalFil, finalCol), self.tablero))
                    elif finalPieza[0] == colorEnemigo:
                        moves.append(Mover((f, c), (finalFil, finalCol), self.tablero))
                        break
                    else:
                        break
                else:
                    break

    def getMovimientoCaballo(self, f, c, moves):
        dirreciones = ((-2, 1), (-2, -1), (2, 1), (2, -1), (1, -2), (1, 2), (-1, -2), (-1, 2))
        colorAliado = 'b' if self.movimientoBlanca else 'n'

        for d in dirreciones:
            finalFil = f + d[0]
            finalCol = c + d[1]
            if 0 <= finalFil < 8 and 0 <= finalCol < 8:
                finalPieza = self.tablero[finalFil][finalCol]
                if finalPieza[0] != colorAliado:
                    moves.append(Mover((f, c), (finalFil, finalCol), self.tablero))

        def getMovimientoQueen(self, f, c, moves):
            dirreciones = ((-1, -1), (1, 1), (-1, 1), (-1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
            colorEnemigo = 'n' if self.movimientoBlanca else 'b'
            for d in dirreciones:
                for i in range(1, 8):
                    finalFil = f + d[0] * i
                    finalCol = c + d[1] * i

                    if 0 <= finalFil < 8 and 0 <= finalCol < 8:
                        finalPieza = self.tablero[finalFil][finalCol]
                        if finalPieza == "--":
                            moves.append(Mover((f, c), (finalFil, finalCol), self.tablero))
                        elif finalPieza[0] == colorEnemigo:
                            moves.append(Mover((f, c), (finalFil, finalCol), self.tablero))
                            break
                        else:
                            break
                    else:
                        break

        def getMovimientoRey(self, f, c, moves):
            dirreciones = ((-1, -1), (1, 1), (-1, 1), (-1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
            colorAliado = 'b' if self.movimientoBlanca else 'n'
            for d in dirreciones:
                finalFil = f + d[0]
                finalCol = c + d[1]
                if 0 <= finalFil < 8 and 0 <= finalCol < 8:
                    finalPieza = self.tablero[finalFil][finalCol]
                    if finalPieza[0] != colorAliado:
                        moves.append(Mover((f, c), (finalFil, finalCol), self.tablero))

    def validarClavadayJaques(self):

        posiblesJaques = []
        clavada = []
        enJaque = False

        if self.movimientoBlanca:
            colorEnemigo = "n"
            colorAliado = "b"
            comienzoFila = self.ubicacionReyBlanco[0]
            comienzoCol = self.ubicacionReyBlanco[1]
        else:
            colorEnemigo = "b"
            colorAliado = "n"
            comienzoFila = self.ubicacionReyBlanco[0]
            comienzoCol = self.ubicacionReyBlanco[1]
        direcciones = ((-1, 0), (0, 1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(direcciones)):
            d = direcciones[j]
            posibleClavada = ()
            for i in range(1, 8):
                finalFila = comienzoFila + d[0] * i
                finalCol = comienzoCol + d[1] * i
                if 0 <= finalFila < 8 and 0 <= finalCol < 8:
                    piezaFinal = self.tablero[finalFila][finalCol]
                    if piezaFinal[0] == colorAliado:
                        if posibleClavada == ():
                            posibleClavada = (finalFila, finalCol, d[0], d[1])
                        else:
                            break
                    elif piezaFinal[0] == colorEnemigo:
                        tipo = piezaFinal[0]
                        # verificar vertical horizontal por si son torres
                        # verificar diagonales por si son alfiles
                        # 1 cuadrado en diagonal para los peones
                        # cualquier direccion para la reina
                        # cualquier direccion pero solo a un bloque de distancia para los reyes
                        if (0 <= j <= 3 and tipo == 'T') or \
                                (4 <= j <= 7 and tipo == 'A') or \
                                (i == 1 and tipo == 'P' and ((colorEnemigo == 'b' and 6 <= j <= 7) or (
                                        colorEnemigo == 'n' and 4 <= j <= 5))) or \
                                (tipo == 'Q') or (i == 1 and tipo == 'R'):
                            if posibleClavada == ():
                                enJaque = True
                                posiblesJaques.append((finalFila, finalCol, d[0], d[1]))
                                break
                            else:
                                clavada.append(posibleClavada)
                                break
                        else:
                            break
        movimientosCaballo = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in movimientosCaballo:
            finalFila = comienzoFila + m[0]
            finalCol = comienzoCol + m[1]
            if 0 <= finalFila < 8 and 0 <= finalCol < 8:
                finalPieza = self.tablero[finalFila][finalCol]
                if finalPieza[0] == colorEnemigo and finalPieza[1] == 'C':
                    enJaque = True
                    posiblesJaques.append((finalFila, finalCol, m[0], m[1]))
        return enJaque, clavada, posiblesJaques


# Lista de movimientos separados
class Mover:
    rangosFilas = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    filasRangos = {v: k for k, v in rangosFilas.items()}
    filasColumnas = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}

    columnasFilas = {v: k for k, v in filasColumnas.items()}

    def __init__(self, casInicial, casFinal, tablero):
        self.filaInicial = casInicial[0]
        self.columnaInicial = casInicial[1]
        self.filaFinal = casFinal[0]
        self.columnaFinal = casFinal[1]
        self.piezaMovida = tablero[self.filaInicial][self.columnaInicial]
        self.piezaCapturada = tablero[self.filaFinal][self.columnaFinal]
        self.movimientoID = self.filaInicial * 1000 + self.filaFinal * 100 + self.filaFinal * 10 + self.columnaFinal

    def __eq__(self, otro):
        if isinstance(otro, Mover):
            return self.movimientoID == otro.movimientoID
        return False

    def getNotacionAjedrez(self):
        return self.getRangoFila(self.filaInicial, self.columnaInicial) + self.getRangoFila(self.filaFinal,
                                                                                            self.columnaFinal)

    def getRangoFila(self, f, c):
        return self.columnasFilas[c] + self.filasRangos[f]

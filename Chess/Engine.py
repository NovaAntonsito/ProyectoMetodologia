class EstadoJuego:

    def __init__(self):
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
        self.contadorInicial = 20
        self.contadorNegra = self.contadorInicial
        self.contadorBlanca = self.contadorInicial
        self.registroMov = []
        self.ubicacionReyBlanco = (7, 4)
        self.ubicacionReyNegro = (0, 4)
        self.jaqueMate = False
        self.tablas = False
        self.enJaque = False
        self.clavadas = []
        self.posiblesJaques = []
        self.capturaAlPasoPosible = ()
        self.registroCapturas = [self.capturaAlPasoPosible]
        self.enroque = Enroque(True, True, True, True)
        self.registroEnroques = [Enroque(self.enroque.ReyBlanco, self.enroque.ReyNegro,
                                         self.enroque.ReinaBlanca, self.enroque.ReinaNegra)]
    def definirTiempoInicial(self,tiempo):
        self.contadorInicial = tiempo
        self.contadorNegra = self.contadorInicial
        self.contadorBlanca = self.contadorInicial
    def hacerMovimiento(self, movimiento):
        self.tablero[movimiento.filaInicial][movimiento.columnaInicial] = "--"
        self.tablero[movimiento.filaFinal][movimiento.columnaFinal] = movimiento.piezaMovida
        self.registroMov.append(movimiento)
        self.movimientoBlanca = not self.movimientoBlanca
        if movimiento.piezaMovida == "bR":
            self.ubicacionReyBlanco = (movimiento.filaFinal, movimiento.columnaFinal)
        elif movimiento.piezaMovida == "nR":
            self.ubicacionReyNegro = (movimiento.filaFinal, movimiento.columnaFinal)
        if movimiento.coronacionPeon:
            self.tablero[movimiento.filaFinal][movimiento.columnaFinal] = movimiento.piezaMovida[0] + "Q"
        if movimiento.movimientoCapturaAlPaso:
            self.tablero[movimiento.filaInicial][movimiento.columnaFinal] = "--"
        if movimiento.piezaMovida[1] == "P" and abs(
                movimiento.filaInicial - movimiento.filaFinal) == 2:
            self.capturaAlPasoPosible = (
                (movimiento.filaInicial + movimiento.filaFinal) // 2, movimiento.columnaInicial)
        else:
            self.capturaAlPasoPosible = ()

        if movimiento.movimientoEnroque:
            if movimiento.columnaFinal - movimiento.columnaInicial == 2:
                self.tablero[movimiento.filaFinal][movimiento.columnaFinal - 1] = self.tablero[movimiento.filaFinal][
                    movimiento.columnaFinal + 1]
                self.tablero[movimiento.filaFinal][movimiento.columnaFinal + 1] = '--'
            else:
                self.tablero[movimiento.filaFinal][movimiento.columnaFinal + 1] = self.tablero[movimiento.filaFinal][
                    movimiento.columnaFinal - 2]
                self.tablero[movimiento.filaFinal][movimiento.columnaFinal - 2] = '--'

        self.registroCapturas.append(self.capturaAlPasoPosible)

        self.actualizarEnroque(movimiento)
        self.registroEnroques.append(Enroque(self.enroque.ReyBlanco, self.enroque.ReyNegro,
                                             self.enroque.ReinaBlanca, self.enroque.ReinaNegra))

    def deshacerMovimiento(self):
        if len(self.registroMov) != 0:
            movimiento = self.registroMov.pop()
            self.tablero[movimiento.filaInicial][movimiento.columnaInicial] = movimiento.piezaMovida
            self.tablero[movimiento.filaFinal][movimiento.columnaFinal] = movimiento.piezaCapturada
            self.movimientoBlanca = not self.movimientoBlanca

            if movimiento.piezaMovida == "bR":
                self.ubicacionReyBlanco = (movimiento.filaInicial, movimiento.columnaInicial)
            elif movimiento.piezaMovida == "nR":
                self.ubicacionReyNegro = (movimiento.filaInicial, movimiento.columnaInicial)

            if movimiento.movimientoCapturaAlPaso:
                self.tablero[movimiento.filaFinal][movimiento.columnaFinal] = "--"
                self.tablero[movimiento.filaInicial][movimiento.columnaFinal] = movimiento.piezaCapturada

            self.registroCapturas.pop()
            self.capturaAlPasoPosible = self.registroCapturas[-1]

            self.registroEnroques.pop()
            self.enroque = self.registroEnroques[-1]

            if movimiento.movimientoEnroque:
                if movimiento.columnaFinal - movimiento.columnaInicial == 2:
                    self.tablero[movimiento.filaFinal][movimiento.columnaFinal + 1] = \
                        self.tablero[movimiento.filaFinal][movimiento.columnaFinal - 1]
                    self.tablero[movimiento.filaFinal][movimiento.columnaFinal - 1] = '--'
                else:
                    self.tablero[movimiento.filaFinal][movimiento.columnaFinal - 2] = \
                        self.tablero[movimiento.filaFinal][movimiento.columnaFinal + 1]
                    self.tablero[movimiento.filaFinal][movimiento.columnaFinal + 1] = '--'
            self.jaqueMate = False
            self.tablas = False

    def actualizarEnroque(self, movimiento):
        if movimiento.piezaCapturada == "bT":
            if movimiento.columnaFinal == 0:
                self.enroque.ReinaBlanca = False
            elif movimiento.columnaFinal == 7:
                self.enroque.ReyBlanco = False
        elif movimiento.piezaCapturada == "nT":
            if movimiento.columnaFinal == 0:
                self.enroque.ReinaNegra = False
            elif movimiento.columnaFinal == 7:
                self.enroque.ReyNegro = False

        if movimiento.piezaMovida == 'bR':
            self.enroque.ReinaBlanca = False
            self.enroque.ReyBlanco = False
        elif movimiento.piezaMovida == 'nR':
            self.enroque.ReinaNegra = False
            self.enroque.ReyNegro = False
        elif movimiento.piezaMovida == 'bT':
            if movimiento.filaInicial == 7:
                if movimiento.columnaInicial == 0:  # left rook
                    self.enroque.ReinaBlanca = False
                elif movimiento.columnaInicial == 7:  # right rook
                    self.enroque.ReyBlanco = False
        elif movimiento.piezaMovida == 'nT':
            if movimiento.filaInicial == 0:
                if movimiento.columnaInicial == 0:  # left rook
                    self.enroque.ReinaNegra = False
                elif movimiento.columnaInicial == 7:  # right rook
                    self.enroque.ReyNegro = False

    def traerMovimientosValidos(self):
        enroqueTemp = Enroque(self.enroque.ReyBlanco, self.enroque.ReyNegro,
                              self.enroque.ReinaBlanca, self.enroque.ReinaNegra)

        movimientos = []
        self.enJaque, self.clavadas, self.posiblesJaques = self.validarClavadasyJaques()

        if self.movimientoBlanca:
            filaRey = self.ubicacionReyBlanco[0]
            colRey = self.ubicacionReyBlanco[1]
        else:
            filaRey = self.ubicacionReyNegro[0]
            colRey = self.ubicacionReyNegro[1]
        if self.enJaque:
            if len(self.posiblesJaques) == 1:
                movimientos = self.traerMovimientosPosibles()

                jaque = self.posiblesJaques[0]
                filaJaque = jaque[0]
                colJaque = jaque[1]
                piezaEnJaque = self.tablero[filaJaque][colJaque]
                cuadradosValidos = []

                if piezaEnJaque[1] == "C":
                    cuadradosValidos = [(filaJaque, colJaque)]
                else:
                    for i in range(1, 8):
                        cuadradoValido = (filaRey + jaque[2] * i,
                                          colRey + jaque[3] * i)
                        cuadradosValidos.append(cuadradoValido)
                        if cuadradoValido[0] == filaJaque and cuadradoValido[
                            1] == colJaque:
                            break

                for i in range(len(movimientos) - 1, -1,
                               -1):
                    if movimientos[i].piezaMovida[
                        1] != "R":
                        if not (movimientos[i].filaFinal,
                                movimientos[
                                    i].columnaFinal) in cuadradosValidos:
                            movimientos.remove(movimientos[i])
            else:
                self.movimientosRey(filaRey, colRey, movimientos)
        else:
            movimientos = self.traerMovimientosPosibles()
            if self.movimientoBlanca:
                self.movimientosEnroque(self.ubicacionReyBlanco[0], self.ubicacionReyBlanco[1], movimientos)
            else:
                self.movimientosEnroque(self.ubicacionReyNegro[0], self.ubicacionReyNegro[1], movimientos)

        if len(movimientos) == 0:
            if self.estaEnJaque():
                self.jaqueMate = True
            else:

                self.tablas = True
        else:
            self.jaqueMate = False
            self.tablas = False

        self.enroque = enroqueTemp
        return movimientos

    def estaEnJaque(self):
        if self.movimientoBlanca:
            return self.cuadradoBajoAtaque(self.ubicacionReyBlanco[0], self.ubicacionReyBlanco[1])
        else:
            return self.cuadradoBajoAtaque(self.ubicacionReyNegro[0], self.ubicacionReyNegro[1])

    def cuadradoBajoAtaque(self, f, c):
        self.movimientoBlanca = not self.movimientoBlanca
        movEnemigo = self.traerMovimientosPosibles()
        self.movimientoBlanca = not self.movimientoBlanca
        for movimiento in movEnemigo:
            if movimiento.filaFinal == f and movimiento.columnaFinal == c:
                return True
        return False

    def traerMovimientosPosibles(self):
        movimientos = []
        for f in range(len(self.tablero)):
            for c in range(len(self.tablero[f])):
                turno = self.tablero[f][c][0]
                if (turno == 'b' and self.movimientoBlanca) or (turno == "n" and not self.movimientoBlanca):
                    pieza = self.tablero[f][c][1]
                    if pieza == 'P':
                        self.movimientosPeon(f, c, movimientos)
                    elif pieza == 'T':
                        self.movimientosTorre(f, c, movimientos)
                    elif pieza == 'A':
                        self.movimientosAlfil(f, c, movimientos)
                    elif pieza == 'C':
                        self.movimientosCaballo(f, c, movimientos)
                    elif pieza == 'Q':
                        self.movimientosReina(f, c, movimientos)
                    elif pieza == 'R':
                        self.movimientosRey(f, c, movimientos)
        return movimientos

    def validarClavadasyJaques(self):
        clavadas = []
        posiblesJaques = []
        enJaque = False
        if self.movimientoBlanca:
            colorEnemigo = "n"
            colorAliade = "b"
            filaInicial = self.ubicacionReyBlanco[0]
            columnaInicial = self.ubicacionReyBlanco[1]
        else:
            colorEnemigo = "b"
            colorAliade = "n"
            filaInicial = self.ubicacionReyNegro[0]
            columnaInicial = self.ubicacionReyNegro[1]

        direcciones = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(direcciones)):
            d = direcciones[j]
            posibleClavada = ()
            for i in range(1, 8):
                filaFinal = filaInicial + d[0] * i
                columnaFinal = columnaInicial + d[1] * i
                if 0 <= filaFinal <= 7 and 0 <= columnaFinal <= 7:
                    piezaFinal = self.tablero[filaFinal][columnaFinal]
                    if piezaFinal[0] == colorAliade and piezaFinal[1] != "R":
                        if posibleClavada == ():
                            posibleClavada = (filaFinal, columnaFinal, d[0], d[1])
                        else:
                            break
                    elif piezaFinal[0] == colorEnemigo:
                        tipo = piezaFinal[1]

                        if (0 <= j <= 3 and tipo == "T") or (4 <= j <= 7 and tipo == "A") or (
                                i == 1 and tipo == "P" and (
                                (colorEnemigo == "b" and 6 <= j <= 7) or (colorEnemigo == "n" and 4 <= j <= 5))) or (
                                tipo == "Q") or (i == 1 and tipo == "R"):
                            if posibleClavada == ():
                                enJaque = True
                                posiblesJaques.append((filaFinal, columnaFinal, d[0], d[1]))
                                break
                            else:
                                clavadas.append(posibleClavada)
                                break
                        else:
                            break
                else:
                    break

        movimientosCaballo = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for movimiento in movimientosCaballo:
            filaFinal = filaInicial + movimiento[0]
            columnaFinal = columnaInicial + movimiento[1]
            if 0 <= filaFinal <= 7 and 0 <= columnaFinal <= 7:
                piezaFinal = self.tablero[filaFinal][columnaFinal]
                if piezaFinal[0] == colorEnemigo and piezaFinal[1] == "C":
                    enJaque = True
                    posiblesJaques.append((filaFinal, columnaFinal, movimiento[0], movimiento[1]))
        return enJaque, clavadas, posiblesJaques

    def movimientosPeon(self, f, c, movimientos):
        piezaClavada = False
        direccionClavada = ()
        for i in range(len(self.clavadas) - 1, -1, -1):
            if self.clavadas[i][0] == f and self.clavadas[i][1] == c:
                piezaClavada = True
                direccionClavada = (self.clavadas[i][2], self.clavadas[i][3])
                self.clavadas.remove(self.clavadas[i])
                break

        if self.movimientoBlanca:
            cantidadMov = -1
            filaInicial = 6
            colorEnemigo = "n"
            filaRey, colRey = self.ubicacionReyBlanco
        else:
            cantidadMov = 1
            filaInicial = 1
            colorEnemigo = "b"
            filaRey, colRey = self.ubicacionReyNegro

        if self.tablero[f + cantidadMov][c] == "--":
            if not piezaClavada or direccionClavada == (cantidadMov, 0):
                movimientos.append(Mover((f, c), (f + cantidadMov, c), self.tablero))
                if f == filaInicial and self.tablero[f + 2 * cantidadMov][c] == "--":
                    movimientos.append(Mover((f, c), (f + 2 * cantidadMov, c), self.tablero))
        if c - 1 >= 0:
            if not piezaClavada or direccionClavada == (cantidadMov, -1):
                if self.tablero[f + cantidadMov][c - 1][0] == colorEnemigo:
                    movimientos.append(Mover((f, c), (f + cantidadMov, c - 1), self.tablero))
                if (f + cantidadMov, c - 1) == self.capturaAlPasoPosible:
                    piezaEnAtaque = piezaEnBloqueo = False
                    if filaRey == f:
                        if colRey < c:

                            dentroDeRango = range(colRey + 1, c - 1)
                            fueraDeRango = range(c + 1, 8)
                        else:
                            dentroDeRango = range(colRey - 1, c, -1)
                            fueraDeRango = range(c - 2, -1, -1)
                        for i in dentroDeRango:
                            if self.tablero[f][i] != "--":
                                piezaEnBloqueo = True
                        for i in fueraDeRango:
                            casilla = self.tablero[f][i]
                            if casilla[0] == colorEnemigo and (casilla[1] == "T" or casilla[1] == "Q"):
                                piezaEnAtaque = True
                            elif casilla != "--":
                                piezaEnBloqueo = True
                    if not piezaEnAtaque or piezaEnBloqueo:
                        movimientos.append(
                            Mover((f, c), (f + cantidadMov, c - 1), self.tablero, movimientoCapturaAlPaso=True))
        if c + 1 <= 7:
            if not piezaClavada or direccionClavada == (cantidadMov, +1):
                if self.tablero[f + cantidadMov][c + 1][0] == colorEnemigo:
                    movimientos.append(Mover((f, c), (f + cantidadMov, c + 1), self.tablero))
                if (f + cantidadMov, c + 1) == self.capturaAlPasoPosible:
                    piezaEnAtaque = piezaEnBloqueo = False
                    if filaRey == f:
                        if colRey < c:

                            dentroDeRango = range(colRey + 1, c)
                            fueraDeRango = range(c + 2, 8)
                        else:
                            dentroDeRango = range(colRey - 1, c + 1, -1)
                            fueraDeRango = range(c - 1, -1, -1)
                        for i in dentroDeRango:
                            if self.tablero[f][i] != "--":
                                piezaEnBloqueo = True
                        for i in fueraDeRango:
                            casilla = self.tablero[f][i]
                            if casilla[0] == colorEnemigo and (casilla[1] == "T" or casilla[1] == "Q"):
                                piezaEnAtaque = True
                            elif casilla != "--":
                                piezaEnBloqueo = True
                    if not piezaEnAtaque or piezaEnBloqueo:
                        movimientos.append(
                            Mover((f, c), (f + cantidadMov, c + 1), self.tablero, movimientoCapturaAlPaso=True))

    def movimientosTorre(self, f, c, movimientos):
        piezaClavada = False
        direccionClavada = ()
        for i in range(len(self.clavadas) - 1, -1, -1):
            if self.clavadas[i][0] == f and self.clavadas[i][1] == c:
                piezaClavada = True
                direccionClavada = (self.clavadas[i][2], self.clavadas[i][3])
                if self.tablero[f][c][
                    1] != "Q":
                    self.clavadas.remove(self.clavadas[i])
                break

        direcciones = ((-1, 0), (0, -1), (1, 0), (0, 1))
        colorEnemigo = "n" if self.movimientoBlanca else "b"
        for d in direcciones:
            for i in range(1, 8):
                filaFinal = f + d[0] * i
                columnaFinal = c + d[1] * i
                if 0 <= filaFinal <= 7 and 0 <= columnaFinal <= 7:
                    if not piezaClavada or direccionClavada == d or direccionClavada == (
                            -d[0], -d[1]):
                        piezaFinal = self.tablero[filaFinal][columnaFinal]
                        if piezaFinal == "--":
                            movimientos.append(Mover((f, c), (filaFinal, columnaFinal), self.tablero))
                        elif piezaFinal[0] == colorEnemigo:
                            movimientos.append(Mover((f, c), (filaFinal, columnaFinal), self.tablero))
                            break
                        else:
                            break
                else:
                    break

    def movimientosCaballo(self, f, c, movimientos):
        piezaClavada = False
        for i in range(len(self.clavadas) - 1, -1, -1):
            if self.clavadas[i][0] == f and self.clavadas[i][1] == c:
                piezaClavada = True
                self.clavadas.remove(self.clavadas[i])
                break

        movimientosCaballo = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2),
                              (1, -2))
        colorAliade = "b" if self.movimientoBlanca else "n"
        for movimiento in movimientosCaballo:
            filaFinal = f + movimiento[0]
            columnaFinal = c + movimiento[1]
            if 0 <= filaFinal <= 7 and 0 <= columnaFinal <= 7:
                if not piezaClavada:
                    piezaFinal = self.tablero[filaFinal][columnaFinal]
                    if piezaFinal[0] != colorAliade:
                        movimientos.append(Mover((f, c), (filaFinal, columnaFinal), self.tablero))

    def movimientosAlfil(self, f, c, movimientos):
        piezaClavada = False
        direccionClavada = ()
        for i in range(len(self.clavadas) - 1, -1, -1):
            if self.clavadas[i][0] == f and self.clavadas[i][1] == c:
                piezaClavada = True
                direccionClavada = (self.clavadas[i][2], self.clavadas[i][3])
                self.clavadas.remove(self.clavadas[i])
                break

        direcciones = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        colorEnemigo = "n" if self.movimientoBlanca else "b"
        for d in direcciones:
            for i in range(1, 8):
                filaFinal = f + d[0] * i
                columnaFinal = c + d[1] * i
                if 0 <= filaFinal <= 7 and 0 <= columnaFinal <= 7:
                    if not piezaClavada or direccionClavada == d or direccionClavada == (
                            -d[0], -d[1]):
                        piezaFinal = self.tablero[filaFinal][columnaFinal]
                        if piezaFinal == "--":
                            movimientos.append(Mover((f, c), (filaFinal, columnaFinal), self.tablero))
                        elif piezaFinal[0] == colorEnemigo:
                            movimientos.append(Mover((f, c), (filaFinal, columnaFinal), self.tablero))
                            break
                        else:
                            break
                else:
                    break

    def movimientosReina(self, f, c, movimientos):
        self.movimientosAlfil(f, c, movimientos)
        self.movimientosTorre(f, c, movimientos)

    def movimientosRey(self, f, c, movimientos):
        movimientosFila = (-1, -1, -1, 0, 0, 1, 1, 1)
        movimientosColumna = (-1, 0, 1, -1, 1, -1, 0, 1)
        colorAliade = "b" if self.movimientoBlanca else "n"
        for i in range(8):
            filaFinal = f + movimientosFila[i]
            columnaFinal = c + movimientosColumna[i]
            if 0 <= filaFinal <= 7 and 0 <= columnaFinal <= 7:
                piezaFinal = self.tablero[filaFinal][columnaFinal]
                if piezaFinal[0] != colorAliade:

                    if colorAliade == "b":
                        self.ubicacionReyBlanco = (filaFinal, columnaFinal)
                    else:
                        self.ubicacionReyNegro = (filaFinal, columnaFinal)
                    enJaque, clavadas, posiblesJaques = self.validarClavadasyJaques()
                    if not enJaque:
                        movimientos.append(Mover((f, c), (filaFinal, columnaFinal), self.tablero))

                    if colorAliade == "b":
                        self.ubicacionReyBlanco = (f, c)
                    else:
                        self.ubicacionReyNegro = (f, c)

    def movimientosEnroque(self, f, c, movimientos):
        if self.cuadradoBajoAtaque(f, c):
            return
        if (self.movimientoBlanca and self.enroque.ReyBlanco) or (
                not self.movimientoBlanca and self.enroque.ReyNegro):
            self.traerMovimientosReyAdyacenteTorre(f, c, movimientos)
        if (self.movimientoBlanca and self.enroque.ReinaBlanca) or (
                not self.movimientoBlanca and self.enroque.ReinaNegra):
            self.traerMovimientosReinaAdyacenteTorre(f, c, movimientos)

    def traerMovimientosReyAdyacenteTorre(self, f, c, movimientos):
        if self.tablero[f][c + 1] == '--' and self.tablero[f][c + 2] == '--':
            if not self.cuadradoBajoAtaque(f, c + 1) and not self.cuadradoBajoAtaque(f, c + 2):
                movimientos.append(Mover((f, c), (f, c + 2), self.tablero, movimientoEnroque=True))

    def traerMovimientosReinaAdyacenteTorre(self, f, c, movimientos):
        if self.tablero[f][c - 1] == '--' and self.tablero[f][c - 2] == '--' and self.tablero[f][c - 3] == '--':
            if not self.cuadradoBajoAtaque(f, c - 1) and not self.cuadradoBajoAtaque(f, c - 2):
                movimientos.append(Mover((f, c), (f, c - 2), self.tablero, movimientoEnroque=True))


class Enroque:
    def __init__(self, ReyBlanco, ReyNegro, ReinaBlanca, ReinaNegra):
        self.ReyBlanco = ReyBlanco
        self.ReyNegro = ReyNegro
        self.ReinaBlanca = ReinaBlanca
        self.ReinaNegra = ReinaNegra


class Mover:
    rangosFilas = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    filasRangos = {v: k for k, v in rangosFilas.items()}
    filasColumnas = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    columnasFilas = {v: k for k, v in filasColumnas.items()}

    def __init__(self, casInicial, casFinal, tablero, movimientoCapturaAlPaso=False, movimientoEnroque=False):
        self.filaInicial = casInicial[0]
        self.columnaInicial = casInicial[1]
        self.filaFinal = casFinal[0]
        self.columnaFinal = casFinal[1]
        self.piezaMovida = tablero[self.filaInicial][self.columnaInicial]
        self.piezaCapturada = tablero[self.filaFinal][self.columnaFinal]
        self.coronacionPeon = (self.piezaMovida == "bP" and self.filaFinal == 0) or (
                self.piezaMovida == "nP" and self.filaFinal == 7)
        self.movimientoCapturaAlPaso = movimientoCapturaAlPaso
        if self.movimientoCapturaAlPaso:
            self.piezaCapturada = "bP" if self.piezaMovida == "nP" else "nP"

        self.movimientoEnroque = movimientoEnroque

        self.estaCapturada = self.piezaCapturada != "--"
        self.movimientoID = self.filaInicial * 1000 + self.columnaInicial * 100 + self.filaFinal * 10 + self.columnaFinal

    def __eq__(self, other):

        if isinstance(other, Mover):
            return self.movimientoID == other.movimientoID
        return False

    def getNotacionAjedrez(self):
        if self.coronacionPeon:
            return self.getRangoFila(self.filaFinal, self.columnaFinal) + "Q"
        if self.movimientoEnroque:
            if self.columnaFinal == 1:
                return "0-0-0"
            else:
                return "0-0"
        if self.movimientoCapturaAlPaso:
            return self.getRangoFila(self.filaInicial, self.columnaInicial)[0] + "x" + self.getRangoFila(
                self.filaFinal,
                self.columnaFinal) + " e.P."
        if self.piezaCapturada != "--":
            if self.piezaMovida[1] == "P":
                return self.getRangoFila(self.filaInicial, self.columnaInicial)[0] + "x" + self.getRangoFila(
                    self.filaFinal,
                    self.columnaFinal)
            else:
                return self.piezaMovida[1] + "x" + self.getRangoFila(self.filaFinal, self.columnaFinal)
        else:
            if self.piezaMovida[1] == "P":
                return self.getRangoFila(self.filaFinal, self.columnaFinal)
            else:
                return self.piezaMovida[1] + self.getRangoFila(self.filaFinal, self.columnaFinal)

    def getRangoFila(self, f, c):
        return self.columnasFilas[c] + self.filasRangos[f]

    def __str__(self):
        if self.movimientoEnroque:
            return "0-0" if self.columnaFinal == 6 else "0-0-0"

        casFinal = self.getRangoFila(self.filaFinal, self.columnaFinal)

        if self.piezaMovida[1] == "P":
            if self.estaCapturada:
                return self.columnasFilas[self.columnaInicial] + "x" + casFinal
            else:
                return casFinal + "Q" if self.coronacionPeon else casFinal
        movimientosReg = self.piezaMovida[1]
        if self.estaCapturada:
            movimientosReg += "x"
        return movimientosReg + casFinal

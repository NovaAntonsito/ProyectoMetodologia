import random


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

    '''
    Toma un movimiento como parametro y lo ejecuta
    '''

    def hacerMovimiento(self, mover):
        self.tablero[mover.filaInicial][mover.columnaInicial] = "--"
        self.tablero[mover.filaFinal][mover.columnaFinal] = mover.piezaMovida
        self.registroMov.append(mover)  # registramos el movimiento
        self.movimientoBlanca = not self.movimientoBlanca  # cambio de turno

    '''
    Rehacer el ultimo movimiento
    '''

    def movAnterior(self):
        if len(self.registroMov) != 0:
            movimiento = self.registroMov.pop()
            self.tablero[movimiento.filaInicial][movimiento.columnaInicial] = movimiento.piezaMovida
            self.tablero[movimiento.filaFinal][movimiento.columnaFinal] = movimiento.piezaCapturada
            self.movimientoBlanca = not self.movimientoBlanca

    def traerMovimietosValidos(self):
        return self.traerTodosMovimientosPosibles()

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
                    print(self.movimientoBlanca)
                    pieza = self.tablero[f][c][1]
                    if pieza == 'P':
                        self.getMovimientoPeon(f, c, movimientos)
                    elif pieza == 'T':
                        self.getMovimientoTorre(f, c, movimientos)
        return movimientos

    '''
    obtener todos los movimentos por el peon selecionado
    '''

    def getMovimientoPeon(self, f, c, movimientos):
        print("getMovimientoPeon", self.movimientoBlanca)
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
            print("Entre aca=>", f, c)
            if self.tablero[f + 1][c] == "--":
                movimientos.append(Mover((f, c), (f + 1, c), self.tablero))
                if f == 1 and self.tablero[f + 2][c] == "--":
                    movimientos.append(Mover((f, c), (f + 2, c), self.tablero))

    ''' 
    obtener todos los movimentos por la torre selecionada
    '''

    def getMovimientoTorre(self, f, c, moves):
        pass


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

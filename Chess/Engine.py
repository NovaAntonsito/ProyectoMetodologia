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

    def hacerMovimiento(self, mover):
        self.tablero[mover.filaInical][mover.columnaInicial] = "--"
        self.tablero[mover.filaFinal][mover.columnaFinal] = mover.piezaMovida
        self.registroMov.append(mover)  # registramos el movimiento
        self.movimientoBlanca = not self.movimientoBlanca  # cambio de turno


# Lista de movimientos separados
class Mover:
    rangosFilas = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    filasRangos = {v: k for k, v in rangosFilas.items()}
    filasColumnas = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}

    columnasFilas = {v: k for k, v in filasColumnas.items()}

    def __init__(self, casInical, casFinal, tablero):
        self.filaInical = casInical[0]
        self.columnaInicial = casInical[1]
        self.filaFinal = casFinal[0]
        self.columnaFinal = casFinal[1]
        self.piezaMovida = tablero[self.filaInical][self.columnaInicial]
        self.piezaCapturada = tablero[self.filaFinal][self.columnaFinal]

    def getNotacionAjedrez(self):
        return self.getRangoFila(self.filaInical, self.columnaInicial) + self.getRangoFila(self.filaFinal,
                                                                                           self.columnaFinal)

    def getRangoFila(self, f, c):
        return self.columnasFilas[c] + self.filasRangos[f]

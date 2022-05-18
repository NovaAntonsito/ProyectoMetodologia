class EstadoJuego():
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
        self.MovimientoBlanca = True
        self.registroMov = True
# Lista de movimientos separados

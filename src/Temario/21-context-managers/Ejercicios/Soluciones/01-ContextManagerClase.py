# =============================================================================
# SOLUCIÓN
# =============================================================================


class Indentador:
    def __init__(self) -> None:
        self.nivel = 0

    def __enter__(self):
        self.nivel += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.nivel -= 1
        return False

    def escribir(self, texto: str) -> None:
        print("    " * self.nivel + texto)


# Pruebas
ind = Indentador()
ind.escribir("Inicio")
with ind:
    ind.escribir("Nivel 1")
    with ind:
        ind.escribir("Nivel 2")
        ind.escribir("Todavía nivel 2")
    ind.escribir("De vuelta al nivel 1")
ind.escribir("Fin")

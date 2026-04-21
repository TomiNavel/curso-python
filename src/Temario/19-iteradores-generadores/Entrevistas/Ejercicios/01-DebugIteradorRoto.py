# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Iterador personalizado roto
# =============================================================================
# El siguiente código intenta definir un iterador que produzca los números
# pares menores que "limite". Tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# [0, 2, 4, 6, 8]
# [0, 2, 4]
# =============================================================================


class Pares:
    def __init__(self, limite):
        self.limite = limite
        self.actual = 0

    def __next__(self):
        if self.actual >= self.limite:
            return
        valor = self.actual
        self.actual += 1
        return valor


print(list(Pares(10)))
print(list(Pares(6)))

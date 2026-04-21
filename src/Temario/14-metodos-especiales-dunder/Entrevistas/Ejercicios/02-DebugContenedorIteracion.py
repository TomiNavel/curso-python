# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Contenedor e iteración
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Longitud: 3
# Elemento 0: rojo
# rojo verde azul
# verde está: True
# =============================================================================

class Paleta:
    def __init__(self, *colores):
        self.colores = list(colores)

    def __len__(self):
        return self.colores

    def __getitem__(self, indice):
        return self.colores[indice]

    def __iter__(self):
        return self.colores

    def __contains__(self, color):
        return color in self.colores

    def __repr__(self):
        return f"Paleta({self.colores})"


p = Paleta("rojo", "verde", "azul")
print(f"Longitud: {len(p)}")
print(f"Elemento 0: {p[0]}")
print(" ".join(c for c in p))
print(f"verde está: {'verde' in p}")

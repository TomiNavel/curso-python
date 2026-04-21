# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Composición vs herencia
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Biblioteca Municipal: 2 estantes
# Estante Ficción: ['Cien años de soledad', 'Don Quijote']
# Estante Ciencia: ['Cosmos']
# Total libros: 3
# =============================================================================

class Estante:
    LIBROS_DEFAULT = []

    def __init__(self, nombre):
        self.nombre = nombre
        self.libros = self.LIBROS_DEFAULT

    def agregar(self, titulo):
        self.libros.append(titulo)

    def cantidad(self):
        return len(self.libros)

    def __str__(self):
        return f"Estante {self.nombre}: {self.libros}"


class Biblioteca(Estante):
    def __init__(self, nombre):
        self.nombre = nombre
        self.estantes = []

    def agregar_estante(self, estante):
        self.estantes.append(estante)

    def total_libros(self):
        return sum(e.cantidad for e in self.estantes)

    def __str__(self):
        return f"{self.nombre}: {len(self.estantes)} estantes"


ficcion = Estante("Ficción")
ficcion.agregar("Cien años de soledad")
ficcion.agregar("Don Quijote")

ciencia = Estante("Ciencia")
ciencia.agregar("Cosmos")

bib = Biblioteca("Biblioteca Municipal")
bib.agregar_estante(ficcion)
bib.agregar_estante(ciencia)

print(bib)
print(ficcion)
print(ciencia)
print(f"Total libros: {bib.total_libros()}")

# =====================
# SOLUCIÓN
# =====================
# Error 1: Estante usa una lista mutable como atributo de clase (LIBROS_DEFAULT)
#   y la asigna directamente: self.libros = self.LIBROS_DEFAULT. Todos los
#   estantes comparten la misma lista. Agregar a uno afecta a todos.
#   Solución: self.libros = [] en __init__ (lista nueva por instancia)
#
# Error 2: Biblioteca hereda de Estante, pero una Biblioteca no ES un Estante.
#   Una biblioteca TIENE estantes → debe usar composición, no herencia.
#   Solución: class Biblioteca: (sin heredar de Estante)
#
# Error 3: total_libros() llama a e.cantidad sin paréntesis. cantidad es un
#   método, no una propiedad. Sin () devuelve el objeto método en lugar del
#   entero, y sum() falla.
#   Solución: e.cantidad() con paréntesis
#
# ERRORES CORREGIDOS:
# 1. self.libros = self.LIBROS_DEFAULT -> self.libros = []
# 2. class Biblioteca(Estante) -> class Biblioteca
# 3. e.cantidad -> e.cantidad()


class Estante:
    def __init__(self, nombre):
        self.nombre = nombre
        self.libros = []

    def agregar(self, titulo):
        self.libros.append(titulo)

    def cantidad(self):
        return len(self.libros)

    def __str__(self):
        return f"Estante {self.nombre}: {self.libros}"


class Biblioteca:
    def __init__(self, nombre):
        self.nombre = nombre
        self.estantes = []

    def agregar_estante(self, estante):
        self.estantes.append(estante)

    def total_libros(self):
        return sum(e.cantidad() for e in self.estantes)

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

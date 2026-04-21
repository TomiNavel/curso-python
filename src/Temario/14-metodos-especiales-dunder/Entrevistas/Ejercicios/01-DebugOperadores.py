# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Operadores aritméticos y comparación
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Vector(4, 6)
# Vector(2, 2)
# True
# False
# =============================================================================

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            raise NotImplementedError
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


a = Vector(3, 4)
b = Vector(1, 2)
print(a + b)
print(a - b)
print(Vector(1, 1) == Vector(1, 1))
print(Vector(1, 1) == Vector(2, 2))

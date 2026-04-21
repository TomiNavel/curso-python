# =====================
# SOLUCIÓN
# =====================
# Error 1: __add__ modifica self en lugar de crear un nuevo objeto.
#   self.x += other.x modifica el vector original. Después de a + b,
#   a queda modificado y a - b da un resultado incorrecto.
#   Solución: return Vector(self.x + other.x, self.y + other.y)
#
# Error 2: __eq__ lanza NotImplementedError (excepción) cuando debería
#   devolver NotImplemented (valor). Al comparar con un tipo distinto,
#   lanzaría una excepción en lugar de devolver False.
#   Solución: return NotImplemented
#
# Error 3: (Consecuencia del Error 1) a - b produce un resultado incorrecto
#   porque a ya fue modificado por a + b. Se resuelve al corregir Error 1.
#
# ERRORES CORREGIDOS:
# 1. __add__ modifica self → crear nuevo Vector
# 2. raise NotImplementedError → return NotImplemented


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


a = Vector(3, 4)
b = Vector(1, 2)
print(a + b)
print(a - b)
print(Vector(1, 1) == Vector(1, 1))
print(Vector(1, 1) == Vector(2, 2))

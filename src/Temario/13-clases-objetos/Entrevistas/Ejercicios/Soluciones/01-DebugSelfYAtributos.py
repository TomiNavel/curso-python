# =====================
# SOLUCIÓN
# =====================
# Error 1: En __init__, las asignaciones "ancho = ancho" y "alto = alto" crean
#   variables locales en lugar de atributos de instancia. Faltan los "self.".
#   Solución: self.ancho = ancho, self.alto = alto
#
# Error 2: El método area() no tiene self como primer parámetro.
#   Python pasa la instancia automáticamente, pero el método no lo acepta.
#   Solución: def area(self):
#
# Error 3: (Consecuencia del Error 1) __str__ y perimetro intentan acceder a
#   self.ancho y self.alto que nunca se crearon. Se resuelve al corregir Error 1.
#
# ERRORES CORREGIDOS:
# 1. ancho = ancho → self.ancho = ancho (y lo mismo con alto)
# 2. def area(): → def area(self):


class Rectangulo:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

    def area(self):
        return self.ancho * self.alto

    def perimetro(self):
        return 2 * (self.ancho + self.alto)

    def __str__(self):
        return f"Rectángulo: {self.ancho} x {self.alto}"


r = Rectangulo(10, 5)
print(r)
print(f"Área: {r.area()}")
print(f"Perímetro: {r.perimetro()}")

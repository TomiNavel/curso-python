# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — self y atributos
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Rectángulo: 10 x 5
# Área: 50
# Perímetro: 30
# =============================================================================

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

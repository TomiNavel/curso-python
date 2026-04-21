# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Clase abstracta mal declarada
# =============================================================================
# El siguiente código intenta crear una jerarquía de formas geométricas con
# una clase abstracta Forma. Tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Cuadrado: área = 25, perímetro = 20
# Triangulo: área = 6.0, perímetro = 12
# Error al instanciar Forma
# Error al instanciar Incompleta
# =============================================================================

from abc import abstractmethod


class Forma:
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimetro(self):
        pass

    def describir(self):
        return f"{type(self).__name__}: área = {self.area()}, perímetro = {self.perimetro()}"


class Cuadrado(Forma):
    def __init__(self, lado):
        self.lado = lado

    def area(self):
        return self.lado ** 2

    def perimetro(self):
        return 4 * self.lado


class Triangulo(Forma):
    def __init__(self, base, altura, lado_a, lado_b, lado_c):
        self.base = base
        self.altura = altura
        self.lado_a = lado_a
        self.lado_b = lado_b
        self.lado_c = lado_c

    def area(self):
        return self.base * self.altura / 2
    # falta perimetro()


class Incompleta(Forma):
    def area(self):
        return 0


print(Cuadrado(5).describir())
print(Triangulo(4, 3, 3, 4, 5).describir())

try:
    f = Forma()
except TypeError:
    print("Error al instanciar Forma")

try:
    i = Incompleta()
except TypeError:
    print("Error al instanciar Incompleta")

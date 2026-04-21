# =====================
# SOLUCIÓN
# =====================
# Error 1: La clase Forma no hereda de ABC. Sin esa herencia, @abstractmethod
#   no tiene ningún efecto: Python no impide instanciar Forma ni detecta
#   subclases incompletas. Hay que importar ABC y hacer "class Forma(ABC)".
#
# Error 2: Falta importar ABC. El import actual es "from abc import abstractmethod"
#   y necesitamos añadir ABC.
#
# Error 3: Triangulo no implementa perimetro(), que es abstracto. Debe
#   añadirse el método sumando los tres lados.
#
# ERRORES CORREGIDOS:
# 1. from abc import abstractmethod -> from abc import ABC, abstractmethod
# 2. class Forma: -> class Forma(ABC):
# 3. Añadir perimetro() a Triangulo


from abc import ABC, abstractmethod


class Forma(ABC):
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

    def perimetro(self):
        return self.lado_a + self.lado_b + self.lado_c


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

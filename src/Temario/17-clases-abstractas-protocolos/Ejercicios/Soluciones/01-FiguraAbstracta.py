import math
from abc import ABC, abstractmethod


class Figura(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimetro(self):
        pass

    def descripcion(self):
        return f"Figura con área {self.area()} y perímetro {self.perimetro()}"


class Cuadrado(Figura):
    def __init__(self, lado):
        self.lado = lado

    def area(self):
        return self.lado ** 2

    def perimetro(self):
        return 4 * self.lado


class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return round(math.pi * self.radio ** 2, 2)

    def perimetro(self):
        return round(2 * math.pi * self.radio, 2)


c = Cuadrado(5)
print(c.descripcion())

circ = Circulo(5)
print(circ.descripcion())

try:
    f = Figura()
except TypeError as e:
    print(f"Error: {e}")


class Incompleta(Figura):
    def area(self):
        return 0
    # falta perimetro()


try:
    i = Incompleta()
except TypeError as e:
    print(f"Error: {e}")

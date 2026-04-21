import math


class Figura:
    def __init__(self, nombre):
        self.nombre = nombre

    def area(self):
        raise NotImplementedError("Las subclases deben implementar area()")

    def perimetro(self):
        raise NotImplementedError("Las subclases deben implementar perimetro()")

    def __str__(self):
        return f"{self.nombre}: área={self.area():.2f}, perímetro={self.perimetro():.2f}"


class Rectangulo(Figura):
    def __init__(self, base, altura):
        super().__init__("Rectángulo")
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura

    def perimetro(self):
        return 2 * (self.base + self.altura)


class Circulo(Figura):
    def __init__(self, radio):
        super().__init__("Círculo")
        self.radio = radio

    def area(self):
        return round(math.pi * self.radio ** 2, 2)

    def perimetro(self):
        return round(2 * math.pi * self.radio, 2)


class Triangulo(Figura):
    def __init__(self, base, altura, lado_a, lado_b, lado_c):
        super().__init__("Triángulo")
        self.base = base
        self.altura = altura
        self.lado_a = lado_a
        self.lado_b = lado_b
        self.lado_c = lado_c

    def area(self):
        return self.base * self.altura / 2

    def perimetro(self):
        return self.lado_a + self.lado_b + self.lado_c


def mostrar_figuras(figuras):
    for fig in figuras:
        print(fig)


figuras = [
    Rectangulo(5, 3),
    Circulo(5),
    Triangulo(4, 3, 3, 4, 5),
]
mostrar_figuras(figuras)

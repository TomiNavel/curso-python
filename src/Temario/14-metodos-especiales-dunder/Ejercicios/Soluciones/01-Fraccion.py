import math


class Fraccion:
    def __init__(self, numerador, denominador):
        if denominador == 0:
            raise ValueError("El denominador no puede ser cero")
        # Mover signo al numerador si el denominador es negativo
        if denominador < 0:
            numerador = -numerador
            denominador = -denominador
        # Simplificar
        mcd = math.gcd(abs(numerador), denominador)
        self.numerador = numerador // mcd
        self.denominador = denominador // mcd

    def __add__(self, other):
        num = self.numerador * other.denominador + other.numerador * self.denominador
        den = self.denominador * other.denominador
        return Fraccion(num, den)

    def __sub__(self, other):
        num = self.numerador * other.denominador - other.numerador * self.denominador
        den = self.denominador * other.denominador
        return Fraccion(num, den)

    def __mul__(self, other):
        return Fraccion(self.numerador * other.numerador,
                        self.denominador * other.denominador)

    def __truediv__(self, other):
        if other.numerador == 0:
            raise ZeroDivisionError("No se puede dividir entre una fracción con numerador 0")
        return Fraccion(self.numerador * other.denominador,
                        self.denominador * other.numerador)

    def __eq__(self, other):
        if not isinstance(other, Fraccion):
            return NotImplemented
        return self.numerador == other.numerador and self.denominador == other.denominador

    def __repr__(self):
        return f"Fraccion({self.numerador}, {self.denominador})"

    def __str__(self):
        return f"{self.numerador}/{self.denominador}"


a = Fraccion(1, 2)
b = Fraccion(1, 3)
print(f"{a} + {b} = {a + b}")
print(f"{Fraccion(3, 4)} - {Fraccion(1, 4)} = {Fraccion(3, 4) - Fraccion(1, 4)}")
print(f"{Fraccion(2, 3)} * {Fraccion(3, 5)} = {Fraccion(2, 3) * Fraccion(3, 5)}")
print(f"{Fraccion(1, 2)} / {Fraccion(1, 4)} = {Fraccion(1, 2) / Fraccion(1, 4)}")
print(f"Fraccion(2, 3) == Fraccion(4, 6): {Fraccion(2, 3) == Fraccion(4, 6)}")
print(repr(a))

# =====================
# SOLUCIÓN
# =====================
# Error 1: a_fahrenheit está decorado con @classmethod pero se usa como método
#   de instancia (accede a self.valor y self.escala). Un @classmethod recibe
#   cls (la clase), no self (la instancia). Debería ser un método de instancia.
#   Solución: eliminar @classmethod
#
# Error 2: es_valida es un @staticmethod pero declara self como primer parámetro.
#   Un @staticmethod no recibe ni self ni cls. Al llamar
#   Temperatura.es_valida(25, 'C'), Python asigna 25 a self y 'C' a valor,
#   dejando escala sin valor → TypeError.
#   Solución: eliminar self de los parámetros
#
# Error 3: __repr__ no usa !r para el string escala. El resultado esperado
#   muestra Temperatura(25, 'C') con comillas alrededor de 'C'.
#   Sin !r, mostraría Temperatura(25, C) — sin comillas, no es válido como
#   expresión Python.
#   Solución: usar {self.escala!r} en __repr__
#
# ERRORES CORREGIDOS:
# 1. @classmethod → eliminado (a_fahrenheit es método de instancia)
# 2. def es_valida(self, valor, escala) → def es_valida(valor, escala)
# 3. {self.escala} → {self.escala!r} en __repr__


class Temperatura:
    def __init__(self, valor, escala="C"):
        self.valor = valor
        self.escala = escala

    def a_fahrenheit(self):
        if self.escala == "C":
            nuevo_valor = self.valor * 9 / 5 + 32
            return Temperatura(nuevo_valor, "F")
        return Temperatura(self.valor, self.escala)

    @staticmethod
    def es_valida(valor, escala):
        if escala == "C":
            return valor >= -273.15
        elif escala == "F":
            return valor >= -459.67
        return False

    def __repr__(self):
        return f"Temperatura({self.valor}, {self.escala!r})"

    def __str__(self):
        return f"{self.valor}°{self.escala}"


temp = Temperatura(25, "C")
print(f"Celsius: {repr(temp)}")
convertida = temp.a_fahrenheit()
print(f"Convertido a F: {repr(convertida)}")
print(f"Es válida: {Temperatura.es_valida(25, 'C')}")
print(f"Mostrar: {temp}")

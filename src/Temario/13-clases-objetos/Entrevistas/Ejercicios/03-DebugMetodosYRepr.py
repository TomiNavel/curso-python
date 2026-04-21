# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Métodos y representación
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Celsius: Temperatura(25, 'C')
# Convertido a F: Temperatura(77.0, 'F')
# Es válida: True
# Mostrar: 25°C
# =============================================================================

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
        return f"Temperatura({self.valor}, {self.escala})"

    def __str__(self):
        return f"{self.valor}°{self.escala}"


temp = Temperatura(25, "C")
print(f"Celsius: {repr(temp)}")
convertida = temp.a_fahrenheit()
print(f"Convertido a F: {repr(convertida)}")
print(f"Es válida: {Temperatura.es_valida(25, 'C')}")
print(f"Mostrar: {temp}")

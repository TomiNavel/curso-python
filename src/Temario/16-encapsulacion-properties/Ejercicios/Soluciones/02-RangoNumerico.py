class RangoNumerico:
    def __init__(self, valor, minimo, maximo):
        self._minimo = minimo
        self._maximo = maximo
        self.valor = valor  # pasa por el setter (clampea)

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, nuevo):
        if nuevo < self._minimo:
            self._valor = self._minimo
        elif nuevo > self._maximo:
            self._valor = self._maximo
        else:
            self._valor = nuevo

    @property
    def minimo(self):
        return self._minimo

    @property
    def maximo(self):
        return self._maximo

    @property
    def porcentaje(self):
        return round((self._valor - self._minimo) / (self._maximo - self._minimo) * 100, 1)

    def __str__(self):
        return f"{self._valor} [{self._minimo} - {self._maximo}] ({self.porcentaje}%)"

    def __repr__(self):
        return f"RangoNumerico({self._valor}, {self._minimo}, {self._maximo})"


r = RangoNumerico(50, 0, 100)
print(r)
r.valor = 75
print(r)
r.valor = 150  # clampea a 100
print(r)
r.valor = -10  # clampea a 0
print(r)

r2 = RangoNumerico(36.5, -20, 80)
print(r2)

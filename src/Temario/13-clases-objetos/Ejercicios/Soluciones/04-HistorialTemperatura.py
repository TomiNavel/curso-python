class HistorialTemperatura:
    def __init__(self, ciudad):
        self.ciudad = ciudad
        self.mediciones = []

    def registrar(self, temperatura):
        if not isinstance(temperatura, (int, float)):
            raise TypeError(f"Se esperaba int o float, se recibió {type(temperatura).__name__}")
        self.mediciones.append(temperatura)

    def media(self):
        if not self.mediciones:
            raise ValueError("No hay mediciones registradas")
        return round(sum(self.mediciones) / len(self.mediciones), 1)

    def maxima(self):
        return max(self.mediciones)

    def minima(self):
        return min(self.mediciones)

    def rango(self):
        return self.maxima() - self.minima()

    def por_encima_de(self, umbral):
        return [t for t in self.mediciones if t > umbral]

    @classmethod
    def desde_lista(cls, ciudad, temperaturas):
        historial = cls(ciudad)
        for t in temperaturas:
            historial.registrar(t)
        return historial

    def __repr__(self):
        return f"HistorialTemperatura({self.ciudad!r}, {len(self.mediciones)} mediciones)"

    def __str__(self):
        return f"{self.ciudad}: {len(self.mediciones)} mediciones, media {self.media()}°C"


h = HistorialTemperatura("Madrid")
for t in [22.5, 18.0, 28.0, 19.0, 30.5]:
    h.registrar(t)
print(h)
print(f"Máxima: {h.maxima()}, Mínima: {h.minima()}, Rango: {h.rango()}")
print(f"Por encima de 25: {h.por_encima_de(25)}")
print(repr(h))
print()
h2 = HistorialTemperatura.desde_lista("Barcelona", [20.0, 22.5, 19.0, 24.5])
print(h2)

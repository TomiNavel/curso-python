class Historial:
    def __init__(self, valor_inicial):
        self._valor = valor_inicial
        self._cambios = []

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, nuevo):
        if nuevo == self._valor:
            return
        self._cambios.append((self._valor, nuevo))
        self._valor = nuevo

    @property
    def total_cambios(self):
        return len(self._cambios)

    @property
    def ultimo_cambio(self):
        if not self._cambios:
            return None
        return self._cambios[-1]

    def historial_completo(self):
        return [f"{anterior} -> {nuevo}" for anterior, nuevo in self._cambios]

    def revertir(self):
        if not self._cambios:
            raise ValueError("No hay cambios que revertir")
        anterior, _ = self._cambios.pop()
        self._valor = anterior

    def __str__(self):
        return f"Historial: valor={self._valor}, cambios={self.total_cambios}"


h = Historial(10)
print(h)
h.valor = 20
print(h)
h.valor = 50
print(h)
h.valor = 50  # mismo valor, no registra cambio
print(h)
print(f"Último cambio: {h.ultimo_cambio}")
print("Historial completo:")
for linea in h.historial_completo():
    print(f"  {linea}")
h.revertir()
print("Después de revertir:")
print(h)

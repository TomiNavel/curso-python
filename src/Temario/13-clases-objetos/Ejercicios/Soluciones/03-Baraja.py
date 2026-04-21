import random


class Carta:
    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo

    def __repr__(self):
        return f"Carta({self.valor!r}, {self.palo!r})"

    def __str__(self):
        return f"{self.valor} de {self.palo}"


class Baraja:
    PALOS = ["Corazones", "Diamantes", "Tréboles", "Picas"]
    VALORES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "As"]

    def __init__(self, valores=None):
        if valores is None:
            valores = self.VALORES
        self.cartas = [
            Carta(valor, palo)
            for palo in self.PALOS
            for valor in valores
        ]

    def mezclar(self):
        random.shuffle(self.cartas)

    def repartir(self, n=1):
        if n > len(self.cartas):
            raise ValueError("No hay suficientes cartas")
        mano = self.cartas[-n:]
        self.cartas = self.cartas[:-n]
        return mano

    def cartas_restantes(self):
        return len(self.cartas)

    @classmethod
    def crear_baraja_reducida(cls):
        valores_reducidos = ["7", "8", "9", "10", "J", "Q", "K", "As"]
        return cls(valores=valores_reducidos)

    def __repr__(self):
        return f"Baraja({len(self.cartas)} cartas)"


random.seed(42)
b = Baraja()
print(repr(b))
b.mezclar()
mano = b.repartir(5)
print(f"Mano: {mano}")
print(f"Quedan: {b.cartas_restantes()}")
reducida = Baraja.crear_baraja_reducida()
print(f"Baraja reducida: {repr(reducida)}")

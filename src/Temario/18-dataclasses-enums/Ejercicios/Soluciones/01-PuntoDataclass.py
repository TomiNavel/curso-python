import math
from dataclasses import dataclass


@dataclass
class Punto:
    x: float = 0.0
    y: float = 0.0

    def distancia_al_origen(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)


# Pruebas
p1 = Punto(3.0, 4.0)
print(p1)
print(p1.distancia_al_origen())

p2 = Punto()
print(p2)
print(p2.distancia_al_origen())

print(Punto(1.0, 2.0) == Punto(1.0, 2.0))

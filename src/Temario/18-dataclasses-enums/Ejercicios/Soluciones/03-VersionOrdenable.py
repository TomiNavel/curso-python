from dataclasses import dataclass


@dataclass(order=True)
class Version:
    mayor: int
    menor: int
    parche: int


# Pruebas
versiones = [
    Version(1, 2, 5),
    Version(2, 0, 0),
    Version(1, 0, 0),
    Version(1, 2, 3),
]
print(sorted(versiones))
print(Version(1, 2, 3) < Version(1, 2, 5))
print(Version(2, 0, 0) < Version(1, 9, 9))

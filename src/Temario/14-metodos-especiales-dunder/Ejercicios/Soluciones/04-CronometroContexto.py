import time


class Cronometro:
    mediciones = []

    def __init__(self, nombre):
        self.nombre = nombre
        self.inicio = 0
        self.duracion = 0

    def __enter__(self):
        self.inicio = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duracion = time.perf_counter() - self.inicio
        Cronometro.mediciones.append((self.nombre, self.duracion))
        return False

    def __repr__(self):
        return f"Cronometro({self.nombre!r}, {self.duracion:.4f})"

    def __str__(self):
        return f"{self.nombre}: {self.duracion:.4f}s"

    def __bool__(self):
        return self.duracion > 0.01

    @classmethod
    def resumen(cls):
        lineas = ["=== Mediciones ==="]
        total = 0
        for nombre, duracion in cls.mediciones:
            lineas.append(f"{nombre}: {duracion:.4f}s")
            total += duracion
        lineas.append(f"Total: {total:.4f}s")
        return "\n".join(lineas)


with Cronometro("ordenar") as c1:
    sorted(range(100000, 0, -1))

print(c1)

with Cronometro("buscar") as c2:
    99999 in range(100000)

print(c2)
print(f"¿Ordenar fue lento?: {bool(c1)}")
print(Cronometro.resumen())

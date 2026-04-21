# =============================================================================
# SOLUCIÓN
# =============================================================================

from contextlib import contextmanager
import time


@contextmanager
def temporizador():
    inicio = time.perf_counter()
    try:
        yield
    finally:
        duracion = time.perf_counter() - inicio
        print(f"Bloque ejecutado en {duracion:.4f}s")


# Pruebas
with temporizador():
    resultado = sum(range(1_000_000))
    print(f"Resultado: {resultado}")

with temporizador():
    resultado = sum(range(10_000_000))
    print(f"Resultado: {resultado}")

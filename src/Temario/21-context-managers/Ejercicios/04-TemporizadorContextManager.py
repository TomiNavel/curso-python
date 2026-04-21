# =============================================================================
# EJERCICIO 4: Temporizador con @contextmanager
# =============================================================================
# Implementa un context manager "temporizador" usando @contextmanager que
# mida el tiempo transcurrido dentro del bloque with.
# Debe imprimir el tiempo en segundos con 4 decimales al salir del bloque.
#
# Para simular trabajo que tome tiempo medible, usa un bucle que sume
# números. No uses time.sleep().
#
# RESULTADO ESPERADO (el tiempo variará):
# Resultado: 499999500000
# Bloque ejecutado en X.XXXXs
# Resultado: 49999995000000
# Bloque ejecutado en X.XXXXs
# =============================================================================

from contextlib import contextmanager
import time

# Tu código aquí


# Pruebas
with temporizador():
    resultado = sum(range(1_000_000))
    print(f"Resultado: {resultado}")

with temporizador():
    resultado = sum(range(10_000_000))
    print(f"Resultado: {resultado}")

# =============================================================================
# EJERCICIO 4: Cronómetro como Context Manager
# =============================================================================
# Crea una clase `Cronometro` que funcione como context manager para medir
# el tiempo de ejecución de bloques de código.
#
# Atributos:
# - nombre (str, identificador del bloque medido)
# - inicio (float, se asigna en __enter__)
# - duracion (float, se calcula en __exit__)
# - mediciones (atributo de clase, lista que acumula todas las mediciones
#   como tuplas (nombre, duracion))
#
# Métodos especiales:
# - __enter__: registra el tiempo de inicio (time.perf_counter), devuelve self
# - __exit__: calcula duración, la guarda en self.duracion,
#   añade (nombre, duracion) a mediciones de clase. No suprime excepciones.
# - __repr__: Cronometro('ordenar', 0.0023)  (duración con 4 decimales)
# - __str__: "ordenar: 0.0023s"
# - __bool__: True si la duración supera 0.01 segundos (operación "lenta")
#
# Método de clase:
# - @classmethod resumen(cls): devuelve un string con todas las mediciones:
#   "=== Mediciones ===\nordenar: 0.0023s\nbuscar: 0.0001s\nTotal: 0.0024s"
#
# RESULTADO ESPERADO (los tiempos varían):
# ordenar: X.XXXXs
# buscar: X.XXXXs
# ¿Ordenar fue lento?: True/False
# === Mediciones ===
# ordenar: X.XXXXs
# buscar: X.XXXXs
# Total: X.XXXXs
# =============================================================================

# Tu código aquí

# import time
# with Cronometro("ordenar") as c1:
#     sorted(range(100000, 0, -1))
#
# print(c1)
#
# with Cronometro("buscar") as c2:
#     99999 in range(100000)
#
# print(c2)
# print(f"¿Ordenar fue lento?: {bool(c1)}")
# print(Cronometro.resumen())

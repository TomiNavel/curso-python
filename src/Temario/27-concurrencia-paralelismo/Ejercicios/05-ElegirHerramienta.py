# =============================================================================
# EJERCICIO 5: Clasificar el tipo de carga de trabajo
# =============================================================================
# Escribe una función "recomendar_herramienta(descripcion)" que clasifique
# el tipo de tarea y recomiende qué herramienta usar. La descripción será
# un diccionario con dos claves:
#   - "cpu_intensivo": bool — True si la tarea hace cálculos en Python puro.
#   - "espera_io": bool — True si la tarea espera red/disco/base de datos.
#
# Devuelve uno de estos strings:
#   - "multiprocessing" si cpu_intensivo es True y espera_io es False.
#   - "threading" si cpu_intensivo es False y espera_io es True.
#   - "asyncio" si tanto cpu_intensivo como espera_io son False
#     (caso raro, pero por convención asumimos I/O masivo asíncrono).
#   - "mixto: considerar analizar más" si ambos son True.
#
# RESULTADO ESPERADO:
# multiprocessing
# threading
# mixto: considerar analizar más
# asyncio
# =============================================================================


def recomendar_herramienta(descripcion):
    # Tu código aquí
    pass


# Pruebas
print(recomendar_herramienta({"cpu_intensivo": True, "espera_io": False}))
print(recomendar_herramienta({"cpu_intensivo": False, "espera_io": True}))
print(recomendar_herramienta({"cpu_intensivo": True, "espera_io": True}))
print(recomendar_herramienta({"cpu_intensivo": False, "espera_io": False}))

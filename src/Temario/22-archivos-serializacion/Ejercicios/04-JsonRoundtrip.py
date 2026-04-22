# =============================================================================
# EJERCICIO 4: Serializar y recuperar datos con JSON
# =============================================================================
# Dada la lista "empleados" con diccionarios, escribe dos funciones:
#   - guardar(ruta, datos): escribe los datos en "ruta" como JSON, con
#     indentación de 2 espacios y permitiendo caracteres no ASCII tal cual.
#   - cargar(ruta): lee el archivo JSON y devuelve la estructura Python.
#
# Usa encoding="utf-8" y context managers.
#
# RESULTADO ESPERADO:
# True
# [{'nombre': 'Ana García', 'salario': 42000}, {'nombre': 'Luis Núñez', 'salario': 38500}]
# =============================================================================

empleados = [
    {"nombre": "Ana García", "salario": 42000},
    {"nombre": "Luis Núñez", "salario": 38500},
]


# Tu código aquí


# Pruebas
guardar("empleados.json", empleados)
recuperado = cargar("empleados.json")
print(recuperado == empleados)
print(recuperado)

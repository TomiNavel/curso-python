# =============================================================================
# EJERCICIO 5: Log Mixin
# =============================================================================
# Crea un mixin que añada funcionalidad de logging a cualquier clase,
# y úsalo con dos clases de ejemplo.
#
# Clase LogMixin:
# - Atributo: _log (lista vacía, inicializada en __init__ del mixin o
#   creada dinámicamente si no existe)
# - registrar(mensaje): añade una tupla (timestamp, mensaje) al _log.
#   Para el timestamp, usa un contador estático que se incrementa en cada
#   registro (no usar datetime, para que los tests sean deterministas).
# - Atributo de clase: _contador_log = 0
# - ver_log(): devuelve una lista de strings "[1] mensaje"
#
# Clase Calculadora(LogMixin):
# - Atributo: resultado (float, inicializado a 0)
# - sumar(n): suma n al resultado, registra "sumar {n}"
# - restar(n): resta n del resultado, registra "restar {n}"
# - __str__: "Resultado: 15.0"
#
# Clase Inventario(LogMixin):
# - Atributo: items (dict vacío)
# - agregar(nombre, cantidad): añade al inventario, registra "agregar {nombre}: {cantidad}"
# - retirar(nombre, cantidad): resta del inventario (si hay suficiente),
#   registra "retirar {nombre}: {cantidad}". Si no hay suficiente → ValueError.
# - __str__: "Inventario: 3 productos"
#
# RESULTADO ESPERADO:
# Resultado: 15.0
# Log calculadora:
# [1] sumar 10
# [2] sumar 5
#
# Inventario: 2 productos
# Log inventario:
# [3] agregar Laptop: 5
# [4] agregar Mouse: 10
# [5] retirar Mouse: 3
# =============================================================================

# Tu código aquí

# calc = Calculadora()
# calc.sumar(10)
# calc.sumar(5)
# print(calc)
# print("Log calculadora:")
# for linea in calc.ver_log():
#     print(linea)
# print()
#
# inv = Inventario()
# inv.agregar("Laptop", 5)
# inv.agregar("Mouse", 10)
# inv.retirar("Mouse", 3)
# print(inv)
# print("Log inventario:")
# for linea in inv.ver_log():
#     print(linea)

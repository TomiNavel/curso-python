# =============================================================================
# EJERCICIO 5: Transformador Callable
# =============================================================================
# Crea una clase `Transformador` que sea un objeto callable que aplica una
# cadena de transformaciones a un valor, manteniendo un historial.
#
# Atributos:
# - transformaciones (lista de funciones, recibidas en __init__ como *args)
# - historial (lista de tuplas (entrada, salida), inicializada vacía)
#
# Métodos especiales:
# - __call__(valor): aplica todas las transformaciones en orden al valor,
#   guarda (entrada, salida) en historial, y devuelve el resultado final.
# - __len__: cantidad de transformaciones registradas
# - __getitem__(indice): acceso al historial por índice
# - __iter__: itera sobre el historial
# - __bool__: True si hay historial, False si está vacío
# - __repr__: Transformador(2 funciones, 3 llamadas)
#
# RESULTADO ESPERADO:
# Resultado 1: 30
# Resultado 2: -15
# Resultado 3: 15
# Repr: Transformador(2 funciones, 3 llamadas)
# Historial [0]: (5, 30)
# Historial [1]: (-10, -15)
# Tiene historial: True
# Recorrido:
#   5 -> 30
#   -10 -> -15
#   0 -> 15
# =============================================================================

# Tu código aquí

# t = Transformador(lambda x: x + 5, lambda x: x * 3)
# print(f"Resultado 1: {t(5)}")      # 5+5=10, 10*3=30
# print(f"Resultado 2: {t(-10)}")    # -10+5=-5, -5*3=-15
# print(f"Resultado 3: {t(0)}")      # 0+5=5, 5*3=15
# print(f"Repr: {repr(t)}")
# print(f"Historial [0]: {t[0]}")
# print(f"Historial [1]: {t[1]}")
# print(f"Tiene historial: {bool(t)}")
# print("Recorrido:")
# for entrada, salida in t:
#     print(f"  {entrada} -> {salida}")

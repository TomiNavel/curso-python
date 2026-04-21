# =============================================================================
# EJERCICIO 2: Contador con Closure
# =============================================================================
# Crea una función crear_contador(inicio) que devuelva una función.
# Cada vez que se llame a la función devuelta, debe incrementar el valor
# en 1 y devolver el nuevo valor.
#
# RESULTADO ESPERADO:
# 1
# 2
# 3
# 10
# 11
# =============================================================================

# Tu código aquí

# Pruebas
contador = crear_contador(0)
print(contador())  # 1
print(contador())  # 2
print(contador())  # 3

otro = crear_contador(9)
print(otro())  # 10
print(otro())  # 11

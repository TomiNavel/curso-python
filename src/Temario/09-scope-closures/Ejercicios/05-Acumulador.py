# =============================================================================
# EJERCICIO 5: Acumulador con Dos Funciones
# =============================================================================
# Crea una función crear_acumulador() que devuelva DOS funciones:
# - agregar(valor): suma el valor al total acumulado y lo devuelve
# - obtener_total(): devuelve el total actual sin modificarlo
#
# Usa nonlocal para mantener el estado compartido entre ambas funciones.
#
# =============================================================================

# Tu código aquí

# Pruebas
agregar, obtener_total = crear_acumulador()

print(agregar(10))        # 10
print(agregar(15))        # 25
print(obtener_total())    # 25
print(agregar(5))         # 30
print(obtener_total())    # 30

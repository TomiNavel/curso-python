# =============================================================================
# EJERCICIO 3: Fábrica de Operaciones
# =============================================================================
# Crea una función crear_operacion(operador, valor) que devuelva una función.
# La función devuelta recibe un número y le aplica la operación con el valor
# configurado.
#
# Operadores soportados: "+", "-", "*", "/"
# Si el operador no es válido, la función devuelta debe devolver None.
#
# RESULTADO ESPERADO:
# 15
# 3
# 50
# 2.0
# None
# =============================================================================

# Tu código aquí


# Pruebas
sumar5 = crear_operacion("+", 5)
restar7 = crear_operacion("-", 7)
por10 = crear_operacion("*", 10)
entre5 = crear_operacion("/", 5)
invalida = crear_operacion("%", 3)

print(sumar5(10))     # 15
print(restar7(10))    # 3
print(por10(5))       # 50
print(entre5(10))     # 2.0
print(invalida(10))   # None

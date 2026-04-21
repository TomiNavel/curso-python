# =============================================================================
# EJERCICIO 3: Función genérica con TypeVar
# =============================================================================
# Implementa una función genérica "ultimo" que reciba una lista de cualquier
# tipo y devuelva su último elemento. Usa TypeVar para que mypy pueda inferir
# el tipo de retorno a partir del tipo de la lista.
#
# Implementa también una función "invertir_par" que reciba una tupla de dos
# elementos (de tipos posiblemente distintos) y devuelva la tupla invertida.
# Usa dos TypeVar distintos.
#
# RESULTADO ESPERADO:
# 3
# hola
# True
# (2, 'a')
# (False, 42)
# =============================================================================

# Tu código aquí


# Pruebas
print(ultimo([1, 2, 3]))
print(ultimo(["hola"]))
print(ultimo([False, True]))

print(invertir_par(("a", 2)))
print(invertir_par((42, False)))

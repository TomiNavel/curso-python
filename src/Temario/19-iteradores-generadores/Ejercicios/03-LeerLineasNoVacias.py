# =============================================================================
# EJERCICIO 3: Filtrar líneas no vacías con un generador
# =============================================================================
# Escribe una función generadora "lineas_no_vacias" que reciba un iterable de
# líneas (por ejemplo, una lista de strings) y produzca solo las líneas que no
# estén vacías ni contengan solo espacios en blanco. Las líneas producidas
# deben devolverse sin espacios iniciales ni finales.
#
# Requisitos:
# - Debe ser un generador (usar yield)
# - No puedes construir una lista intermedia
# - Usa el método strip() para limpiar cada línea
#
# RESULTADO ESPERADO:
# ['hola', 'mundo', 'python']
# ['linea uno', 'linea dos']
# =============================================================================


# Tu código aquí


# Tests
entrada1 = ["hola", "", "mundo", "   ", "python", ""]
print(list(lineas_no_vacias(entrada1)))

entrada2 = ["  linea uno  ", "\n", "linea dos", "   "]
print(list(lineas_no_vacias(entrada2)))

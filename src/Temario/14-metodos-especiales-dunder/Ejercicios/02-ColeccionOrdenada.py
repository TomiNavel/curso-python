# =============================================================================
# EJERCICIO 2: Colección Ordenada
# =============================================================================
# Crea una clase `ColeccionOrdenada` que actúe como una lista que mantiene
# sus elementos siempre ordenados.
#
# Métodos:
# - agregar(elemento): inserta el elemento en la posición correcta para
#   mantener el orden. Usa bisect.insort para inserción eficiente.
#
# Métodos especiales:
# - __len__: cantidad de elementos
# - __getitem__(indice): acceso por índice (también habilita slicing)
# - __contains__(elemento): búsqueda eficiente con bisect.bisect_left
# - __iter__: iteración sobre los elementos
# - __bool__: True si hay elementos, False si está vacía
# - __repr__: ColeccionOrdenada([1, 3, 5, 7])
#
# RESULTADO ESPERADO:
# ColeccionOrdenada([1, 3, 5, 7, 9])
# Longitud: 5
# Elemento [0]: 1
# Elemento [-1]: 9
# Slice [1:4]: [3, 5, 7]
# 5 está: True
# 6 está: False
# Bool vacía: False
# Bool con datos: True
# Iteración: 1 3 5 7 9
# =============================================================================

# Tu código aquí

# import bisect
# col = ColeccionOrdenada()
# for n in [5, 1, 9, 3, 7]:
#     col.agregar(n)
# print(repr(col))
# print(f"Longitud: {len(col)}")
# print(f"Elemento [0]: {col[0]}")
# print(f"Elemento [-1]: {col[-1]}")
# print(f"Slice [1:4]: {col[1:4]}")
# print(f"5 está: {5 in col}")
# print(f"6 está: {6 in col}")
# vacia = ColeccionOrdenada()
# print(f"Bool vacía: {bool(vacia)}")
# print(f"Bool con datos: {bool(col)}")
# print("Iteración:", " ".join(str(x) for x in col))

# =============================================================================
# EJERCICIO 3: Dataclass ordenable (order=True)
# =============================================================================
# Crea una dataclass "Version" con tres campos enteros: mayor, menor, parche.
# Usa order=True para permitir comparar y ordenar versiones.
#
# Una versión es menor que otra si su "mayor" es menor, o si empata en mayor
# y su "menor" es menor, etc. (orden lexicográfico por los tres campos).
#
# RESULTADO ESPERADO:
# [Version(mayor=1, menor=0, parche=0), Version(mayor=1, menor=2, parche=3), Version(mayor=1, menor=2, parche=5), Version(mayor=2, menor=0, parche=0)]
# True
# False
# =============================================================================

# Tu código aquí


# Pruebas
versiones = [
    Version(1, 2, 5),
    Version(2, 0, 0),
    Version(1, 0, 0),
    Version(1, 2, 3),
]
print(sorted(versiones))
print(Version(1, 2, 3) < Version(1, 2, 5))
print(Version(2, 0, 0) < Version(1, 9, 9))

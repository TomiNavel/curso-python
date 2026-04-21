# =============================================================================
# EJERCICIO 2: Dataclass con default_factory
# =============================================================================
# Crea una dataclass "Carrito" con dos campos:
#   - cliente: str
#   - productos: list (por defecto, lista vacía — usa default_factory)
# Añade un método "agregar(producto)" que añada un producto a la lista y
# un método "total_items()" que devuelva la cantidad de productos.
#
# Verifica que dos carritos distintos NO comparten la misma lista.
#
# RESULTADO ESPERADO:
# Carrito(cliente='Ana', productos=['Libro', 'Café'])
# 2
# Carrito(cliente='Luis', productos=[])
# 0
# =============================================================================

# Tu código aquí


# Pruebas
c1 = Carrito("Ana")
c1.agregar("Libro")
c1.agregar("Café")
print(c1)
print(c1.total_items())

c2 = Carrito("Luis")
print(c2)
print(c2.total_items())

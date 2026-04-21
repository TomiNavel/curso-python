# =============================================================================
# EJERCICIO 2: Sistema de Inventario
# =============================================================================
# Crea dos clases: `Producto` e `Inventario`.
#
# Clase Producto:
# - Atributos: nombre (str), precio (float), stock (int)
# - __repr__: Producto('Laptop', 999.99, 10)
# - __str__: "Laptop - $999.99 (10 uds)"
#
# Clase Inventario:
# - Atributos: nombre_tienda (str), productos (lista, inicializada vacía)
# - agregar(producto): añade un Producto a la lista
# - buscar(nombre): devuelve el Producto con ese nombre, o None si no existe
# - valor_total(): devuelve la suma de precio * stock de todos los productos
# - productos_bajo_stock(minimo=5): devuelve lista de productos con stock < minimo
# - resumen(): devuelve string con el formato mostrado abajo
#
# RESULTADO ESPERADO:
# === Inventario de TechStore ===
# - Laptop - $999.99 (10 uds)
# - Mouse - $25.00 (3 uds)
# - Teclado - $75.50 (50 uds)
# Valor total: $10,849.40
#
# Bajo stock: ['Mouse - $25.00 (3 uds)']
# Buscar 'Mouse': Mouse - $25.00 (3 uds)
# Buscar 'Tablet': None
# =============================================================================

# Tu código aquí

# inv = Inventario("TechStore")
# inv.agregar(Producto("Laptop", 999.99, 10))
# inv.agregar(Producto("Mouse", 25.00, 3))
# inv.agregar(Producto("Teclado", 75.50, 50))
# print(inv.resumen())
# print()
# print(f"Bajo stock: {inv.productos_bajo_stock()}")
# print(f"Buscar 'Mouse': {inv.buscar('Mouse')}")
# print(f"Buscar 'Tablet': {inv.buscar('Tablet')}")

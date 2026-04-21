# =====================
# SOLUCIÓN
# =====================
# Error 1: NO hay error en este bloque. Es una trampa: sorted() con key
#   devuelve los elementos originales ordenados por el criterio de key,
#   NO los resultados de key. Este bloque funciona correctamente.
#   El candidato debe saber que key solo determina el criterio de
#   comparación, no transforma los elementos.
#
# Error 2: .sort() modifica la lista in-place y devuelve None.
#   Después de .sort(), productos_original ya está ordenada, no intacta.
#   Además, "ordenados" es None.
#   Corrección: usar sorted() que crea una lista nueva.
#
# Error 3: min() se aplica sobre los precios extraídos (p[1]), así que
#   devuelve solo el precio (25), no la tupla completa.
#   Corrección: usar min() con key sobre la lista de productos.
#
# ERRORES CORREGIDOS:
# 1. (Sin error — trampa para verificar comprensión de key)
# 2. productos_original.sort(...) → sorted(productos_original, ...)
# 3. min(p[1] for p in productos) → min(productos, key=lambda p: p[1])


productos = [("laptop", 999), ("teclado", 75), ("mouse", 25)]

por_precio = sorted(productos, key=lambda p: p[1])
print(f"Por precio: {por_precio}")

productos_original = [("laptop", 999), ("teclado", 75), ("mouse", 25)]
ordenados = sorted(productos_original, key=lambda p: p[1])
print(f"Original intacta: {productos_original}")

mas_barato = min(productos, key=lambda p: p[1])
print(f"Más barato: {mas_barato}")

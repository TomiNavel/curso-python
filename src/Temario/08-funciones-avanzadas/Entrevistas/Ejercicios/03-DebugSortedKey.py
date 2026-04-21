# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — sorted() y key
# =============================================================================
# El siguiente código tiene 3 errores relacionados con sorted() y sort().
# Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Por precio: [('mouse', 25), ('teclado', 75), ('laptop', 999)]
# Original intacta: [('laptop', 999), ('teclado', 75), ('mouse', 25)]
# Más barato: ('mouse', 25)
# =============================================================================

productos = [("laptop", 999), ("teclado", 75), ("mouse", 25)]

# Error 1: el programador espera obtener las tuplas ordenadas,
# pero obtiene otra cosa
por_precio = sorted(productos, key=lambda p: p[1])
print(f"Por precio: {por_precio}")

# Error 2: el programador quiere ordenar sin modificar la lista original,
# pero la original cambia
productos_original = [("laptop", 999), ("teclado", 75), ("mouse", 25)]
ordenados = productos_original.sort(key=lambda p: p[1])
print(f"Original intacta: {productos_original}")

# Error 3: el programador quiere el producto más barato pero obtiene
# solo el precio
mas_barato = min(p[1] for p in productos)
print(f"Más barato: {mas_barato}")

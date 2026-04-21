"""
Solución: Gestionar inventario
"""

productos = ["portátil", "ratón", "tablet", "portátil", "webcam"]

productos.append("teclado")
productos.append("monitor")
print(f"Después de añadir: {productos}")

productos.insert(2, "auriculares")
print(f"Después de insertar: {productos}")

productos.remove("ratón")
print(f"Después de eliminar ratón: {productos}")

extraido = productos.pop()
print(f"Elemento extraído: {extraido}")
print(f"Después de pop: {productos}")

print(f"Veces que aparece portátil: {productos.count('portátil')}")

print(f"Posición de tablet: {productos.index('tablet')}")

productos.sort()
print(f"Ordenada: {productos}")

productos.reverse()
print(f"Invertida: {productos}")

print(f"Total de productos: {len(productos)}")

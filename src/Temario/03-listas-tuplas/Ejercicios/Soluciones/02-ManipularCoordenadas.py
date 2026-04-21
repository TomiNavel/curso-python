"""
Solución: Manipular coordenadas
"""

punto_a = (1, 2, 3)
punto_b = (4, 5, 6)

x, y, z = punto_a
print(f"x={x}, y={y}, z={z}")

print(f"Tercera coordenada de punto_b: {punto_b[-1]}")

ruta = punto_a + punto_b
print(f"Ruta completa: {ruta}")

print(f"Primeras 3: {ruta[:3]}")

print(f"Últimas 3: {ruta[3:]}")

temp = list(punto_a)
temp[0] = 99
punto_modificado = tuple(temp)
print(f"Punto modificado: {punto_modificado}")

print(f"¿5 está en punto_b? {5 in punto_b}")

print(f"Longitud de ruta: {len(ruta)}")

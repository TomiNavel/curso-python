# =============================================================================
# EJERCICIO 1: Dataclass Punto
# =============================================================================
# Crea una dataclass "Punto" con dos campos: x e y (float, por defecto 0.0).
# Añade un método "distancia_al_origen" que devuelva la distancia euclídea
# al punto (0, 0), usando math.sqrt.
#
# RESULTADO ESPERADO:
# Punto(x=3.0, y=4.0)
# 5.0
# Punto(x=0.0, y=0.0)
# 0.0
# True
# =============================================================================

# Tu código aquí


# Pruebas
p1 = Punto(3.0, 4.0)
print(p1)
print(p1.distancia_al_origen())

p2 = Punto()
print(p2)
print(p2.distancia_al_origen())

print(Punto(1.0, 2.0) == Punto(1.0, 2.0))

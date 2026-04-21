# =============================================================================
# EJERCICIO 1: Figura Abstracta
# =============================================================================
# Crea una clase abstracta `Figura` que sirva como base para figuras geométricas.
#
# Clase abstracta Figura (hereda de ABC):
# - Método abstracto area()
# - Método abstracto perimetro()
# - Método concreto descripcion() que devuelve:
#   "Figura con área {area} y perímetro {perimetro}"
#
# Subclases a implementar:
# - Cuadrado(lado): area = lado**2, perimetro = 4*lado
# - Circulo(radio): area = pi*radio**2, perimetro = 2*pi*radio (usa math.pi)
#
# Verifica que:
# - Figura() no puede instanciarse (TypeError)
# - Una subclase incompleta no puede instanciarse
#
# RESULTADO ESPERADO:
# Figura con área 25 y perímetro 20
# Figura con área 78.54 y perímetro 31.42
# Error: Can't instantiate abstract class Figura...
# Error: Can't instantiate abstract class Incompleta...
# =============================================================================

# Tu código aquí

# c = Cuadrado(5)
# print(c.descripcion())
#
# circ = Circulo(5)
# print(circ.descripcion())
#
# try:
#     f = Figura()
# except TypeError as e:
#     print(f"Error: {e}")
#
# class Incompleta(Figura):
#     def area(self):
#         return 0
#     # falta perimetro()
#
# try:
#     i = Incompleta()
# except TypeError as e:
#     print(f"Error: {e}")

# =============================================================================
# EJERCICIO 1: Figuras Geométricas
# =============================================================================
# Crea una jerarquía de clases para figuras geométricas.
#
# Clase base Figura:
# - Atributo: nombre (str)
# - Método area(): lanza NotImplementedError
# - Método perimetro(): lanza NotImplementedError
# - __str__: "Rectángulo: área=15.00, perímetro=16.00"
#
# Subclase Rectangulo(Figura):
# - Atributos: base, altura
# - area(): base * altura
# - perimetro(): 2 * (base + altura)
#
# Subclase Circulo(Figura):
# - Atributo: radio
# - area(): pi * radio^2 (redondear a 2 decimales)
# - perimetro(): 2 * pi * radio (redondear a 2 decimales)
#
# Subclase Triangulo(Figura):
# - Atributos: base, altura, lado_a, lado_b, lado_c
# - area(): base * altura / 2
# - perimetro(): lado_a + lado_b + lado_c
#
# Función libre mostrar_figuras(figuras): recibe una lista de figuras
# e imprime cada una usando polimorfismo (sin isinstance).
#
# RESULTADO ESPERADO:
# Rectángulo: área=15.00, perímetro=16.00
# Círculo: área=78.54, perímetro=31.42
# Triángulo: área=6.00, perímetro=12.00
# =============================================================================

# Tu código aquí

# import math
# figuras = [
#     Rectangulo(5, 3),
#     Circulo(5),
#     Triangulo(4, 3, 3, 4, 5),
# ]
# mostrar_figuras(figuras)

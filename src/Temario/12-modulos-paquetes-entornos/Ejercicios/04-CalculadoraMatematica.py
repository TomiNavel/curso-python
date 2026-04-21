# =============================================================================
# EJERCICIO 4: Calculadora Matemática
# =============================================================================
# Crea un módulo simulado (dentro de este mismo archivo) con funciones
# matemáticas que usen el módulo `math`.
#
# Funciones a crear:
#
# 1. `distancia_puntos(x1, y1, x2, y2)`: distancia euclidiana entre dos puntos.
#    Fórmula: sqrt((x2-x1)² + (y2-y1)²)
#
# 2. `area_triangulo(a, b, c)`: área de un triángulo dados sus tres lados
#    usando la fórmula de Herón.
#    - s = (a + b + c) / 2
#    - area = sqrt(s * (s-a) * (s-b) * (s-c))
#    - Si los lados no forman un triángulo válido, lanzar ValueError
#
# 3. `convertir_temperatura(valor, de, a)`: convierte entre escalas.
#    - Escalas: "C" (Celsius), "F" (Fahrenheit), "K" (Kelvin)
#    - Si la escala no es válida, lanzar ValueError
#    - Redondear a 2 decimales
#
# 4. `estadisticas(numeros)`: recibe una lista de números y devuelve un
#    diccionario con: "media", "minimo", "maximo", "rango", "suma".
#    - Si la lista está vacía, lanzar ValueError
#
# RESULTADO ESPERADO:
# distancia_puntos(0, 0, 3, 4): 5.0
# area_triangulo(3, 4, 5): 6.0
# convertir_temperatura(100, "C", "F"): 212.0
# convertir_temperatura(32, "F", "C"): 0.0
# convertir_temperatura(0, "C", "K"): 273.15
# estadisticas([10, 20, 30, 40, 50]): {'media': 30.0, 'minimo': 10, 'maximo': 50, 'rango': 40, 'suma': 150}
# =============================================================================

# Tu código aquí

# print(distancia_puntos(0, 0, 3, 4))
# print(area_triangulo(3, 4, 5))
# print(convertir_temperatura(100, "C", "F"))
# print(convertir_temperatura(32, "F", "C"))
# print(convertir_temperatura(0, "C", "K"))
# print(estadisticas([10, 20, 30, 40, 50]))

import math


def distancia_puntos(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def area_triangulo(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError(f"Los lados {a}, {b}, {c} no forman un triángulo válido")
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def convertir_temperatura(valor, de, a):
    escalas_validas = {"C", "F", "K"}
    if de not in escalas_validas or a not in escalas_validas:
        raise ValueError(f"Escalas válidas: C, F, K. Recibido: de='{de}', a='{a}'")

    if de == a:
        return round(valor, 2)

    # Convertir a Celsius primero
    if de == "F":
        celsius = (valor - 32) * 5 / 9
    elif de == "K":
        celsius = valor - 273.15
    else:
        celsius = valor

    # Convertir de Celsius a la escala destino
    if a == "F":
        resultado = celsius * 9 / 5 + 32
    elif a == "K":
        resultado = celsius + 273.15
    else:
        resultado = celsius

    return round(resultado, 2)


def estadisticas(numeros):
    if not numeros:
        raise ValueError("La lista no puede estar vacía")

    return {
        "media": sum(numeros) / len(numeros),
        "minimo": min(numeros),
        "maximo": max(numeros),
        "rango": max(numeros) - min(numeros),
        "suma": sum(numeros),
    }


print(distancia_puntos(0, 0, 3, 4))
print(area_triangulo(3, 4, 5))
print(convertir_temperatura(100, "C", "F"))
print(convertir_temperatura(32, "F", "C"))
print(convertir_temperatura(0, "C", "K"))
print(estadisticas([10, 20, 30, 40, 50]))

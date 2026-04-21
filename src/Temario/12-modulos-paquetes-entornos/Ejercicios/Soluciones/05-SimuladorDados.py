import random
from collections import Counter


def lanzar_dados(n_dados, caras=6):
    return [random.randint(1, caras) for _ in range(n_dados)]


def frecuencia_resultados(lanzamientos):
    return dict(sorted(Counter(lanzamientos).items()))


def simulacion_completa(n_lanzamientos, n_dados, caras=6, semilla=None):
    if semilla is not None:
        random.seed(semilla)

    sumas = []
    for _ in range(n_lanzamientos):
        resultado = lanzar_dados(n_dados, caras)
        sumas.append(sum(resultado))

    return {
        "sumas": sumas,
        "media": round(sum(sumas) / len(sumas), 2),
        "minimo": min(sumas),
        "maximo": max(sumas),
        "frecuencia_sumas": frecuencia_resultados(sumas),
    }


resultado = simulacion_completa(1000, 2, semilla=42)
print(f"Media: {resultado['media']}")
print(f"Mínimo: {resultado['minimo']}")
print(f"Máximo: {resultado['maximo']}")
print(f"Frecuencia de sumas: {resultado['frecuencia_sumas']}")

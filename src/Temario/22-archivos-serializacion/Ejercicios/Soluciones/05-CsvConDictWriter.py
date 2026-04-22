# =============================================================================
# SOLUCIÓN
# =============================================================================

import csv

productos = [
    {"codigo": "A1", "nombre": "Teclado", "precio": 45},
    {"codigo": "A2", "nombre": "Ratón", "precio": 25},
    {"codigo": "B1", "nombre": "Portátil", "precio": 950},
    {"codigo": "B2", "nombre": "Monitor", "precio": 220},
]


def exportar_csv(ruta: str, filas: list[dict]) -> None:
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["codigo", "nombre", "precio"])
        writer.writeheader()
        writer.writerows(filas)


def cargar_caros(ruta: str, umbral: float) -> list[str]:
    resultado = []
    with open(ruta, "r", encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            if float(fila["precio"]) > umbral:
                resultado.append(fila["nombre"])
    return resultado


# Pruebas
exportar_csv("productos.csv", productos)
print(cargar_caros("productos.csv", 100))

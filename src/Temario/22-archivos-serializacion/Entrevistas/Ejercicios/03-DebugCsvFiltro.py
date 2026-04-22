# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — CSV y filtrado numérico
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# El objetivo es escribir un CSV con una cabecera y dos filas, y luego
# filtrar los productos con precio estrictamente mayor que 50.
#
# RESULTADO ESPERADO:
# ['Teclado', 'Portátil']
# =============================================================================

import csv
from pathlib import Path

productos = [
    {"nombre": "Ratón", "precio": 20},
    {"nombre": "Teclado", "precio": 90},
    {"nombre": "Portátil", "precio": 950},
]


def exportar(ruta: str, filas: list[dict]) -> None:
    with open(ruta, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nombre", "precio"])
        writer.writerows(filas)


def filtrar_caros(ruta: str, umbral: float) -> list[str]:
    resultado = []
    with open(ruta, "r", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            if fila["precio"] > umbral:
                resultado.append(fila["nombre"])
    return resultado


# Pruebas
exportar("productos.csv", productos)
print(filtrar_caros("productos.csv", 50))

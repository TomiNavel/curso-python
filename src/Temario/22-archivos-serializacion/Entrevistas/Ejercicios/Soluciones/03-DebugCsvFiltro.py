# =====================
# SOLUCIÓN
# =====================
# Error 1: exportar() no llama a writer.writeheader(). Sin la cabecera,
#   el DictReader que usa filtrar_caros toma la primera fila de datos
#   como nombres de columna, con lo que falta una fila y las claves
#   no coinciden.
#   Solución: añadir writer.writeheader() antes de writerows.
#
# Error 2: los open() de ambas funciones no pasan newline="". En Windows
#   esto añade líneas en blanco entre cada registro al escribir y
#   genera filas vacías al leer. Es obligatorio al trabajar con csv.
#   Solución: añadir newline="" en los dos open.
#
# Error 3: filtrar_caros() compara fila["precio"] con un número. csv
#   siempre devuelve strings, así que la comparación "20" > 50 lanza
#   TypeError en Python 3 al mezclar tipos incompatibles.
#   Solución: convertir con float() antes de comparar.
#
# ERRORES CORREGIDOS:
# 1. falta writer.writeheader() → añadir
# 2. falta newline="" en ambos open → añadir
# 3. comparar string con número → float(fila["precio"])

import csv
from pathlib import Path

productos = [
    {"nombre": "Ratón", "precio": 20},
    {"nombre": "Teclado", "precio": 90},
    {"nombre": "Portátil", "precio": 950},
]


def exportar(ruta: str, filas: list[dict]) -> None:
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["nombre", "precio"])
        writer.writeheader()
        writer.writerows(filas)


def filtrar_caros(ruta: str, umbral: float) -> list[str]:
    resultado = []
    with open(ruta, "r", encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            if float(fila["precio"]) > umbral:
                resultado.append(fila["nombre"])
    return resultado


# Pruebas
exportar("productos.csv", productos)
print(filtrar_caros("productos.csv", 50))

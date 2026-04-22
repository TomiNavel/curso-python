# =============================================================================
# SOLUCIÓN
# =============================================================================

import json

empleados = [
    {"nombre": "Ana García", "salario": 42000},
    {"nombre": "Luis Núñez", "salario": 38500},
]


def guardar(ruta: str, datos) -> None:
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def cargar(ruta: str):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


# Pruebas
guardar("empleados.json", empleados)
recuperado = cargar("empleados.json")
print(recuperado == empleados)
print(recuperado)

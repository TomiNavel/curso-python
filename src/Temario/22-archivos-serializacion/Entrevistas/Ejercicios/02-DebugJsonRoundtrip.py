# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Roundtrip JSON
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# El objetivo es guardar un pedido con fecha y una lista de productos a JSON,
# y recuperarlo sin perder información legible.
#
# RESULTADO ESPERADO:
# Guardado correctamente
# {'cliente': 'María Ñoño', 'fecha': '2026-04-22', 'productos': ['Café', 'Té']}
# =============================================================================

import json
from datetime import date

pedido = {
    "cliente": "María Ñoño",
    "fecha": date(2026, 4, 22),
    "productos": ["Café", "Té"],
}


def guardar(ruta: str, datos: dict) -> None:
    with open(ruta, "w") as f:
        json.dumps(datos, f, indent=2)
    print("Guardado correctamente")


def cargar(ruta: str) -> dict:
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


# Pruebas
guardar("pedido.json", pedido)
print(cargar("pedido.json"))

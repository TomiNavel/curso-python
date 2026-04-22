# =====================
# SOLUCIÓN
# =====================
# Error 1: guardar() llama a json.dumps (con s) pasándole un archivo como
#   segundo argumento. dumps devuelve un string y no acepta un file-like;
#   la función adecuada para escribir a archivo es json.dump (sin s).
#   Solución: usar json.dump.
#
# Error 2: El diccionario contiene un objeto date, que json no sabe
#   serializar — lanza TypeError: Object of type date is not JSON
#   serializable. Hay que convertir la fecha a string antes de serializar,
#   por ejemplo con isoformat().
#   Solución: pasar default=str a json.dump (o convertir manualmente) para
#   que json sepa representar la fecha como "2026-04-22".
#
# Error 3: El open de guardar() no especifica encoding y omite
#   ensure_ascii=False. Sin encoding, escribe con el del sistema; sin
#   ensure_ascii=False, los caracteres no ASCII se escapan como \uXXXX
#   y el archivo queda ilegible para humanos (aunque sea válido).
#   Solución: encoding="utf-8" y ensure_ascii=False.
#
# ERRORES CORREGIDOS:
# 1. json.dumps(datos, f, ...) → json.dump(datos, f, ...)
# 2. date no serializable → default=str
# 3. sin encoding ni ensure_ascii=False → añadir ambos

import json
from datetime import date

pedido = {
    "cliente": "María Ñoño",
    "fecha": date(2026, 4, 22),
    "productos": ["Café", "Té"],
}


def guardar(ruta: str, datos: dict) -> None:
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False, default=str)
    print("Guardado correctamente")


def cargar(ruta: str) -> dict:
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


# Pruebas
guardar("pedido.json", pedido)
print(cargar("pedido.json"))

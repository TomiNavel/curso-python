# =============================================================================
# SOLUCIÓN
# =============================================================================

from contextlib import suppress


def obtener_valor(datos: dict, claves: list[str]):
    for clave in claves:
        with suppress(KeyError):
            return datos[clave]
    return None


# Pruebas
datos = {"nombre": "Ana", "edad": 30}

print(obtener_valor(datos, ["nombre", "edad"]))
print(obtener_valor(datos, ["altura", "peso", "edad"]))
print(obtener_valor(datos, ["altura", "peso"]))

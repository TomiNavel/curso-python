from typing import TypedDict


class RespuestaAPI(TypedDict):
    status: int
    mensaje: str
    datos: list[dict[str, str]]


def crear_respuesta(codigo: int, usuarios: list[dict[str, str]]) -> RespuestaAPI:
    return {
        "status": codigo,
        "mensaje": "OK" if codigo == 200 else "Error",
        "datos": usuarios
    }


# Pruebas
usuarios = [{"nombre": "Ana"}, {"nombre": "Luis"}]
print(crear_respuesta(200, usuarios))
print(crear_respuesta(404, []))

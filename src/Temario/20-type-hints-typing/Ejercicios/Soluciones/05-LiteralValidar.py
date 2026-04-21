from typing import Literal

NivelLog = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


def registrar(mensaje: str, nivel: NivelLog) -> str:
    return f"[{nivel}] {mensaje}"


def es_critico(nivel: NivelLog) -> bool:
    return nivel == "ERROR"


# Pruebas
print(registrar("Servidor iniciado", "INFO"))
print(registrar("Conexión perdida", "ERROR"))
print(registrar("Variable x = 42", "DEBUG"))
print(es_critico("WARNING"))
print(es_critico("ERROR"))

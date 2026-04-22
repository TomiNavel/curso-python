# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Encoding y modo de apertura
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# El objetivo es guardar un saludo con caracteres españoles y recuperarlo.
# La función "guardar" debe dejar el archivo listo para que "cargar" devuelva
# el mismo string sin corromper los acentos ni la ñ.
#
# RESULTADO ESPERADO:
# ¡Hola señor García!
# =============================================================================

from pathlib import Path


def guardar(ruta: str, texto: str) -> None:
    f = open(ruta, "wb")
    f.write(texto)


def cargar(ruta: str) -> str:
    with open(ruta) as f:
        return f.read()


# Pruebas
guardar("saludo.txt", "¡Hola señor García!")
print(cargar("saludo.txt"))

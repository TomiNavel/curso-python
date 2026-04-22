# =====================
# SOLUCIÓN
# =====================
# Error 1: guardar() abre en modo "wb" (binario) pero intenta escribir un
#   str. En binario, write() solo acepta bytes y lanza TypeError. Además,
#   el archivo no se cierra: no usa "with" y no hay close(), lo que deja
#   el descriptor abierto y los datos posiblemente sin flush.
#   Solución: usar "w" en modo texto, y envolver en "with" para asegurar
#   el cierre.
#
# Error 2: guardar() no especifica encoding. Aunque el texto tiene caracteres
#   no ASCII, depende del locale del sistema. En Windows con cp1252 funciona
#   por casualidad con acentos y ñ, pero un emoji o carácter fuera de cp1252
#   haría fallar la escritura. Es importante ser explícito con utf-8.
#   Solución: pasar encoding="utf-8" en el open.
#
# Error 3: cargar() tampoco especifica encoding. Al leer en un sistema con
#   un locale distinto del usado al escribir (por ejemplo, cp1252 vs utf-8),
#   los bytes se interpretan mal y los acentos se corrompen o lanzan
#   UnicodeDecodeError.
#   Solución: pasar encoding="utf-8" al abrir para leer.
#
# ERRORES CORREGIDOS:
# 1. guardar() usa "wb" sin with → usar "w" y with
# 2. guardar() sin encoding → añadir encoding="utf-8"
# 3. cargar() sin encoding → añadir encoding="utf-8"

from pathlib import Path


def guardar(ruta: str, texto: str) -> None:
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)


def cargar(ruta: str) -> str:
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


# Pruebas
guardar("saludo.txt", "¡Hola señor García!")
print(cargar("saludo.txt"))

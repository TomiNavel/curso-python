# =====================
# SOLUCIÓN
# =====================
# Error 1: Los recursos no se registran en el ExitStack. El código llama
#   a recurso(nombre) pero no usa pila.enter_context(). Sin esto, el
#   context manager nunca ejecuta __enter__, los recursos no se adquieren,
#   y r es un objeto generador en lugar del string producido por yield.
#   Solución: usar r = pila.enter_context(recurso(nombre)).
#
# Error 2: pila.callback(limpieza_extra()) llama a la función
#   inmediatamente (por los paréntesis) y registra su valor de retorno
#   (None) como callback. La función se ejecuta durante la construcción
#   del bloque, no al salir del ExitStack.
#   Solución: pasar la función sin invocarla: pila.callback(limpieza_extra).
#
# Error 3: suppress(KeyError) no captura FileNotFoundError. La función
#   os.remove lanza FileNotFoundError cuando el archivo no existe, no
#   KeyError. Al suprimir el tipo incorrecto, la excepción se propaga
#   y el programa termina con un traceback.
#   Solución: cambiar a suppress(FileNotFoundError).
#
# ERRORES CORREGIDOS:
# 1. recurso(nombre) → pila.enter_context(recurso(nombre))
# 2. pila.callback(limpieza_extra()) → pila.callback(limpieza_extra)
# 3. suppress(KeyError) → suppress(FileNotFoundError)

from contextlib import ExitStack, suppress, contextmanager


@contextmanager
def recurso(nombre: str):
    print(f"Recurso {nombre} adquirido")
    try:
        yield nombre
    finally:
        print(f"Recurso {nombre} liberado")


def limpieza_extra():
    print("Limpieza extra ejecutada")


def borrar_temporal() -> None:
    import os
    os.remove("archivo_inexistente.txt")


# Pruebas
nombres_recursos = ["A", "B", "C"]

with ExitStack() as pila:
    recursos = []
    for nombre in nombres_recursos:
        r = pila.enter_context(recurso(nombre))
        recursos.append(r)

    pila.callback(limpieza_extra)
    print(f"Usando recursos: {', '.join(recursos)}")

with suppress(FileNotFoundError):
    borrar_temporal()

print("No se pudo borrar: archivo no encontrado")
print("Listo")

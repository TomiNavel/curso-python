# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — ExitStack y suppress
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Recurso A adquirido
# Recurso B adquirido
# Recurso C adquirido
# Usando recursos: A, B, C
# Limpieza extra ejecutada
# Recurso C liberado
# Recurso B liberado
# Recurso A liberado
# No se pudo borrar: archivo no encontrado
# Listo
# =============================================================================

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
        r = recurso(nombre)
        recursos.append(r)

    pila.callback(limpieza_extra())
    print(f"Usando recursos: {', '.join(recursos)}")

with suppress(KeyError):
    borrar_temporal()

print("No se pudo borrar: archivo no encontrado")
print("Listo")

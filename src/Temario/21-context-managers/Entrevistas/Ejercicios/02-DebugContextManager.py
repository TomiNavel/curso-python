# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — @contextmanager
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# [LOG] Iniciando seccion: carga de datos
# Procesando datos...
# [LOG] Finalizando seccion: carga de datos
# [LOG] Iniciando seccion: exportacion
# Exportando...
# [LOG] Error en seccion exportacion: disco lleno
# [LOG] Finalizando seccion: exportacion
# =============================================================================

from contextlib import contextmanager


@contextmanager
def seccion_log(nombre: str):
    print(f"[LOG] Iniciando seccion: {nombre}")
    yield nombre
    print(f"[LOG] Finalizando seccion: {nombre}")


def procesar(nombre_seccion: str) -> None:
    print("Procesando datos...")


def exportar(nombre_seccion: str) -> None:
    print("Exportando...")
    raise IOError("disco lleno")


# Pruebas
with seccion_log("carga de datos") as nombre:
    procesar(nombre)

with seccion_log("exportacion") as nombre:
    exportar(nombre)

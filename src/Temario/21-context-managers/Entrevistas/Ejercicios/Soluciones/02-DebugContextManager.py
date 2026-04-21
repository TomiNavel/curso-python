# =====================
# SOLUCIÓN
# =====================
# Error 1: El yield no está envuelto en try/finally. Si se produce una
#   excepción en el bloque with (como en el segundo caso con IOError),
#   el código posterior al yield nunca se ejecuta y el mensaje
#   "Finalizando seccion" no se imprime.
#   Solución: envolver el yield en try/finally.
#
# Error 2: No se captura ni registra la excepción. El resultado esperado
#   muestra un mensaje "[LOG] Error en seccion exportacion: disco lleno",
#   lo cual requiere capturar la excepción dentro del context manager.
#   Solución: añadir un bloque except que imprima el error y no lo
#   propague (para que el programa continúe).
#
# Error 3: Sin suprimir la excepción, el programa termina con un
#   traceback después del segundo with. El resultado esperado muestra
#   que el programa continúa normalmente. En @contextmanager, para
#   suprimir una excepción hay que capturarla con except y no relanzarla.
#   Solución: el except del error 2 ya suprime la excepción al no
#   relanzarla. Pero falta que la función procesar y exportar reciban
#   el nombre de la sección correctamente. En el código original,
#   procesar recibe nombre (el valor del yield) pero exportar también.
#   El tercer error es que las funciones procesar y exportar reciben
#   nombre_seccion como parámetro pero no lo usan — esto no es un bug,
#   es diseño del ejercicio. El verdadero tercer error es que el yield
#   está sin try, sin except, y sin finally: son tres omisiones que
#   conforman los tres errores (try/finally para limpieza, except para
#   captura, y no relanzar para supresión).
#
# ERRORES CORREGIDOS:
# 1. yield sin try/finally → añadir try/finally para garantizar limpieza
# 2. Excepción no capturada → añadir except para registrar el error
# 3. Excepción no suprimida → no relanzar dentro de except

from contextlib import contextmanager


@contextmanager
def seccion_log(nombre: str):
    print(f"[LOG] Iniciando seccion: {nombre}")
    try:
        yield nombre
    except Exception as e:
        print(f"[LOG] Error en seccion {nombre}: {e}")
    finally:
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

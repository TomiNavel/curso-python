# =============================================================================
# SOLUCIÓN
# =============================================================================

from contextlib import ExitStack
import tempfile
import os


def leer_multiples_archivos(rutas: list[str]) -> dict[str, str]:
    resultado = {}
    with ExitStack() as pila:
        for ruta in rutas:
            try:
                f = pila.enter_context(open(ruta, "r"))
                resultado[ruta] = f.read()
            except FileNotFoundError:
                resultado[ruta] = "ARCHIVO NO ENCONTRADO"
    return resultado


# Pruebas: crear archivos temporales para probar
directorio = tempfile.mkdtemp()
ruta1 = os.path.join(directorio, "archivo1.txt")
ruta2 = os.path.join(directorio, "archivo2.txt")
ruta3 = os.path.join(directorio, "noexiste.txt")

with open(ruta1, "w") as f:
    f.write("Contenido del archivo 1")
with open(ruta2, "w") as f:
    f.write("Contenido del archivo 2")

resultado = leer_multiples_archivos([ruta1, ruta2, ruta3])
for nombre, contenido in resultado.items():
    print(f"{os.path.basename(nombre)}: {contenido}")

# Limpiar archivos temporales
import shutil
shutil.rmtree(directorio)

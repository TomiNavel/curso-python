# =============================================================================
# EJERCICIO 5: ExitStack con número dinámico de recursos
# =============================================================================
# Implementa una función "leer_multiples_archivos" que reciba una lista
# de rutas de archivo y devuelva un diccionario con el nombre del archivo
# como clave y su contenido como valor.
#
# Usa ExitStack para abrir todos los archivos de forma segura.
# Si algún archivo no existe, debe capturarse FileNotFoundError e incluir
# el mensaje "ARCHIVO NO ENCONTRADO" como valor en el diccionario.
#
# RESULTADO ESPERADO (creará archivos temporales para la prueba):
# archivo1.txt: Contenido del archivo 1
# archivo2.txt: Contenido del archivo 2
# noexiste.txt: ARCHIVO NO ENCONTRADO
# =============================================================================

from contextlib import ExitStack
import tempfile
import os

# Tu código aquí


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

# =====================
# SOLUCIÓN
# =====================
# Error 1: ruta.extension no existe. El atributo correcto es ruta.suffix.
#   Solución: ruta.extension → ruta.suffix
#
# Error 2: ruta.name devuelve el nombre completo con extensión ("mi_script.py").
#   Para obtener el nombre sin extensión se usa ruta.stem.
#   Solución: ruta.name → ruta.stem
#
# Error 3: ruta.absolute es un método, no una propiedad. Sin los paréntesis,
#   se obtiene una referencia al método en lugar de la ruta resuelta.
#   Solución: ruta.absolute → ruta.absolute() (o mejor, ruta.resolve())
#
# ERRORES CORREGIDOS:
# 1. ruta.extension → ruta.suffix
# 2. ruta.name → ruta.stem (para nombre sin extensión)
# 3. ruta.absolute → ruta.resolve() (con paréntesis, y resolve es más robusto)


from pathlib import Path

ruta = Path("proyecto") / "src" / "mi_script.py"

extension = ruta.suffix
print(f"Extensión: {extension}")

nombre = ruta.stem
print(f"Nombre sin extensión: {nombre}")

ruta_completa = ruta.resolve()
print(f"Ruta completa: {ruta_completa}")

import os
directorio = os.getcwd()
print(f"Directorio actual: {directorio}")

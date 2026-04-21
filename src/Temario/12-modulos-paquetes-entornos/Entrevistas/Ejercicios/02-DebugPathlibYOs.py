# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — pathlib y os
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Extensión: .py
# Nombre sin extensión: mi_script
# Ruta completa: <ruta_absoluta>/proyecto/src/mi_script.py
# Directorio actual: <directorio_actual>
# =============================================================================

from pathlib import Path

ruta = Path("proyecto") / "src" / "mi_script.py"

extension = ruta.extension
print(f"Extensión: {extension}")

nombre = ruta.name
print(f"Nombre sin extensión: {nombre}")

ruta_completa = ruta.absolute
print(f"Ruta completa: {ruta_completa}")

import os
directorio = os.getcwd()
print(f"Directorio actual: {directorio}")

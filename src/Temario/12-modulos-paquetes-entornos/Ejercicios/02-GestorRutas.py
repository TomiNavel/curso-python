# =============================================================================
# EJERCICIO 2: Gestor de Rutas con pathlib
# =============================================================================
# Crea una función `analizar_ruta` que reciba una ruta (string) y devuelva un
# diccionario con información sobre ella.
#
# La función debe devolver:
# - "ruta_completa": la ruta absoluta (string)
# - "nombre": nombre del archivo o directorio
# - "extension": extensión del archivo (sin punto), o "" si no tiene
# - "nombre_sin_extension": nombre sin extensión (stem)
# - "padre": directorio padre (string)
# - "existe": True/False
# - "tipo": "archivo", "directorio" o "no existe"
#
# Crea también una función `buscar_por_extension` que reciba una ruta de
# directorio y una extensión, y devuelva una lista de nombres de archivos
# que tengan esa extensión (búsqueda NO recursiva).
#
# RESULTADO ESPERADO (las rutas varían según el sistema):
# analizar_ruta("12-modulos-paquetes-entornos.md"):
#   nombre: 12-modulos-paquetes-entornos.md
#   extension: md
#   nombre_sin_extension: 12-modulos-paquetes-entornos
#   existe: True (si se ejecuta desde el directorio correcto)
#   tipo: archivo
#
# buscar_por_extension(".", "py"):
#   ['01-ExplorarModulo.py', '02-GestorRutas.py', ...] (archivos .py del directorio)
# =============================================================================

# Tu código aquí

# from pathlib import Path
# info = analizar_ruta("12-modulos-paquetes-entornos.md")
# for clave, valor in info.items():
#     print(f"  {clave}: {valor}")
# print()
# archivos_py = buscar_por_extension(".", "py")
# print(f"Archivos .py: {archivos_py}")

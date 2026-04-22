# =============================================================================
# EJERCICIO 3: Explorar un directorio con pathlib
# =============================================================================
# Escribe una función "archivos_python(raiz)" que devuelva una lista ordenada
# con todos los archivos .py dentro del directorio "raiz", incluyendo los que
# estén en subdirectorios. Devuelve cada ruta como string (no como Path).
#
# Usa pathlib. No uses os.walk.
#
# RESULTADO ESPERADO:
# ['proyecto/main.py', 'proyecto/utils/helpers.py', 'proyecto/utils/io.py']
# =============================================================================

from pathlib import Path

# Preparación: crea la estructura de prueba
base = Path("proyecto")
base.mkdir(exist_ok=True)
(base / "utils").mkdir(exist_ok=True)
(base / "main.py").write_text("", encoding="utf-8")
(base / "README.md").write_text("", encoding="utf-8")
(base / "utils" / "helpers.py").write_text("", encoding="utf-8")
(base / "utils" / "io.py").write_text("", encoding="utf-8")
(base / "utils" / "datos.txt").write_text("", encoding="utf-8")


# Tu código aquí


# Pruebas
rutas = archivos_python("proyecto")
print([r.replace("\\", "/") for r in rutas])

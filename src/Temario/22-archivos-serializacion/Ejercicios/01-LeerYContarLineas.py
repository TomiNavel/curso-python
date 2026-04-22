# =============================================================================
# EJERCICIO 1: Leer y contar líneas
# =============================================================================
# Dado el archivo "poema.txt", escribe una función "contar_lineas_no_vacias"
# que devuelva el número de líneas que no estén vacías (ignorando espacios
# en blanco al principio o al final).
# Itera sobre el archivo línea a línea, no uses read() ni readlines().
# Especifica encoding="utf-8" al abrir.
#
# RESULTADO ESPERADO:
# 4
# =============================================================================

from pathlib import Path

# Preparación: crea el archivo de prueba
Path("poema.txt").write_text(
    "La luna sale tarde\n"
    "\n"
    "   \n"
    "sobre los tejados rojos\n"
    "y el silencio se hace\n"
    "\n"
    "eterno en las calles\n",
    encoding="utf-8",
)


# Tu código aquí


# Pruebas
print(contar_lineas_no_vacias("poema.txt"))

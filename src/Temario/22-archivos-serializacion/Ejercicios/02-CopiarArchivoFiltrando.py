# =============================================================================
# EJERCICIO 2: Copiar archivo filtrando
# =============================================================================
# Escribe una función "copiar_sin_comentarios(origen, destino)" que lea el
# archivo "origen" y escriba en "destino" solo las líneas que NO empiecen
# por el carácter "#" (ignorando espacios iniciales). Usa encoding="utf-8"
# en ambos archivos y conserva los saltos de línea originales.
#
# RESULTADO ESPERADO:
# from pathlib import Path
# print("hola")
# valor = 42
# =============================================================================

from pathlib import Path

# Preparación: crea el archivo de origen
Path("script.py").write_text(
    "# Este es un comentario inicial\n"
    "from pathlib import Path\n"
    "   # comentario indentado\n"
    "print(\"hola\")\n"
    "# otro comentario\n"
    "valor = 42\n",
    encoding="utf-8",
)


# Tu código aquí


# Pruebas
copiar_sin_comentarios("script.py", "limpio.py")
print(Path("limpio.py").read_text(encoding="utf-8"), end="")

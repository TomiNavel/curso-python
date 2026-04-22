# =============================================================================
# SOLUCIÓN
# =============================================================================

from pathlib import Path

Path("script.py").write_text(
    "# Este es un comentario inicial\n"
    "from pathlib import Path\n"
    "   # comentario indentado\n"
    "print(\"hola\")\n"
    "# otro comentario\n"
    "valor = 42\n",
    encoding="utf-8",
)


def copiar_sin_comentarios(origen: str, destino: str) -> None:
    with open(origen, "r", encoding="utf-8") as entrada, \
         open(destino, "w", encoding="utf-8") as salida:
        for linea in entrada:
            if not linea.lstrip().startswith("#"):
                salida.write(linea)


# Pruebas
copiar_sin_comentarios("script.py", "limpio.py")
print(Path("limpio.py").read_text(encoding="utf-8"), end="")

# =============================================================================
# SOLUCIÓN
# =============================================================================

from pathlib import Path

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


def contar_lineas_no_vacias(ruta: str) -> int:
    total = 0
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            if linea.strip():
                total += 1
    return total


# Pruebas
print(contar_lineas_no_vacias("poema.txt"))

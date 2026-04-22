# =============================================================================
# SOLUCIÓN
# =============================================================================

from pathlib import Path

base = Path("proyecto")
base.mkdir(exist_ok=True)
(base / "utils").mkdir(exist_ok=True)
(base / "main.py").write_text("", encoding="utf-8")
(base / "README.md").write_text("", encoding="utf-8")
(base / "utils" / "helpers.py").write_text("", encoding="utf-8")
(base / "utils" / "io.py").write_text("", encoding="utf-8")
(base / "utils" / "datos.txt").write_text("", encoding="utf-8")


def archivos_python(raiz: str) -> list[str]:
    return sorted(str(p) for p in Path(raiz).rglob("*.py"))


# Pruebas
rutas = archivos_python("proyecto")
print([r.replace("\\", "/") for r in rutas])

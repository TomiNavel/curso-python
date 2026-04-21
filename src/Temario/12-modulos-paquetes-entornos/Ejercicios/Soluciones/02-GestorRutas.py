from pathlib import Path


def analizar_ruta(ruta_str):
    ruta = Path(ruta_str)

    if ruta.is_file():
        tipo = "archivo"
    elif ruta.is_dir():
        tipo = "directorio"
    else:
        tipo = "no existe"

    return {
        "ruta_completa": str(ruta.resolve()),
        "nombre": ruta.name,
        "extension": ruta.suffix.lstrip("."),
        "nombre_sin_extension": ruta.stem,
        "padre": str(ruta.parent),
        "existe": ruta.exists(),
        "tipo": tipo,
    }


def buscar_por_extension(directorio, extension):
    ruta = Path(directorio)
    return sorted(f.name for f in ruta.glob(f"*.{extension}") if f.is_file())


info = analizar_ruta("12-modulos-paquetes-entornos.md")
for clave, valor in info.items():
    print(f"  {clave}: {valor}")
print()

archivos_py = buscar_por_extension(".", "py")
print(f"Archivos .py: {archivos_py}")

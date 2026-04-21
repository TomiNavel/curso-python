# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — TypedDict y Literal
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# {'titulo': 'Informe Q1', 'estado': 'borrador', 'paginas': 0}
# {'titulo': 'Informe Q1', 'estado': 'publicado', 'paginas': 15}
# borrador: Informe Q1
# publicado: Informe Q1 (15 páginas)
# =============================================================================

from typing import TypedDict, Literal

EstadoDoc = Literal["borrador", "revision", "publicado"]


class Documento(TypedDict):
    titulo: str
    estado: str
    paginas: int


def crear_documento(titulo: str) -> Documento:
    return {"titulo": titulo, "estado": "borrador"}


def publicar(doc: Documento, paginas: int) -> Documento:
    doc["estado"] = "publicado"
    doc["paginas"] = paginas
    return doc


def resumen(doc: Documento) -> str:
    if doc["estado"] == "borrador":
        return f"borrador: {doc['titulo']}"
    return f"{doc['estado']}: {doc['titulo']} ({doc['paginas']} páginas)"


# Pruebas
doc = crear_documento("Informe Q1")
print(doc)
doc = publicar(doc, 15)
print(doc)

print(resumen(crear_documento("Informe Q1")))
print(resumen(publicar(crear_documento("Informe Q1"), 15)))

# =====================
# SOLUCIÓN
# =====================
# Error 1: En la clase Documento, el campo "estado" está anotado como "str"
#   en lugar de usar el tipo Literal definido arriba (EstadoDoc). El propósito
#   de definir EstadoDoc era restringir los valores posibles, pero no se usa.
#   Solución: cambiar "estado: str" por "estado: EstadoDoc".
#
# Error 2: La función crear_documento devuelve un diccionario sin la clave
#   "paginas". Pero Documento exige tres claves (titulo, estado, paginas).
#   mypy señalaría que falta la clave "paginas".
#   Solución: añadir "paginas": 0 al diccionario retornado.
#
# Error 3: La función publicar muta el diccionario original en lugar de crear
#   uno nuevo. Aunque esto funciona en ejecución, es un problema conceptual:
#   al mutar el original, la variable doc antes de publicar ya no tiene el
#   estado "borrador" — la primera línea de pruebas imprime el estado correcto
#   solo porque se reasigna doc inmediatamente. Pero el problema real es que
#   el diccionario doc creado en las pruebas finales se muta dentro de
#   publicar, así que crear_documento("Informe Q1") dentro de resumen
#   devuelve un documento que ya fue mutado. Solución: crear un nuevo
#   diccionario con spread (**doc) en lugar de mutar.
#
# ERRORES CORREGIDOS:
# 1. estado: str → estado: EstadoDoc
# 2. Añadir "paginas": 0 en crear_documento
# 3. Crear nuevo diccionario en publicar en lugar de mutar

from typing import TypedDict, Literal

EstadoDoc = Literal["borrador", "revision", "publicado"]


class Documento(TypedDict):
    titulo: str
    estado: EstadoDoc
    paginas: int


def crear_documento(titulo: str) -> Documento:
    return {"titulo": titulo, "estado": "borrador", "paginas": 0}


def publicar(doc: Documento, paginas: int) -> Documento:
    return {**doc, "estado": "publicado", "paginas": paginas}


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

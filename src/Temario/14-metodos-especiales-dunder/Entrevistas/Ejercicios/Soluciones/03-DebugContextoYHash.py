# =====================
# SOLUCIÓN
# =====================
# Error 1: __enter__ de Archivo no devuelve self. La variable "f" en
#   "with Archivo(...) as f" recibe None, no el objeto Archivo.
#   Solución: añadir return self
#
# Error 2: __exit__ de Archivo devuelve True, lo que suprime cualquier
#   excepción que ocurra dentro del bloque with. Debería devolver False
#   para no ocultar errores.
#   Solución: return False
#
# Error 3: Etiqueta define __eq__ pero no __hash__. Al definir __eq__,
#   Python establece __hash__ = None, haciendo los objetos no hashables.
#   Crear un set de Etiquetas lanza TypeError.
#   Solución: definir __hash__ basado en los mismos atributos que __eq__
#
# ERRORES CORREGIDOS:
# 1. __enter__ no devuelve self → añadir return self
# 2. __exit__ return True → return False
# 3. Falta __hash__ → añadir __hash__ con hash((self.nombre, self.categoria))


class Archivo:
    def __init__(self, nombre):
        self.nombre = nombre

    def __enter__(self):
        print(f"Abriendo archivo {self.nombre}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Cerrando archivo {self.nombre}")
        return False


class Etiqueta:
    def __init__(self, nombre, categoria):
        self.nombre = nombre
        self.categoria = categoria

    def __eq__(self, other):
        if not isinstance(other, Etiqueta):
            return NotImplemented
        return self.nombre == other.nombre and self.categoria == other.categoria

    def __hash__(self):
        return hash((self.nombre, self.categoria))

    def __repr__(self):
        return f"Etiqueta({self.nombre!r}, {self.categoria!r})"


with Archivo("datos.txt") as f:
    pass

e1 = Etiqueta("python", "tech")
e2 = Etiqueta("python", "tech")
e3 = Etiqueta("java", "tech")

print(f"{repr(e1)} == {repr(e2)}: {e1 == e2}")
unicos = {e1, e2, e3}
print(f"Únicos: {len(unicos)}")

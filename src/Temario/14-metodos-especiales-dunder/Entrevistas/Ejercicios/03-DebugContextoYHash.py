# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Context manager y hashing
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Abriendo archivo datos.txt
# Cerrando archivo datos.txt
# Etiqueta('python', 'tech') == Etiqueta('python', 'tech'): True
# Únicos: 2
# =============================================================================

class Archivo:
    def __init__(self, nombre):
        self.nombre = nombre

    def __enter__(self):
        print(f"Abriendo archivo {self.nombre}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Cerrando archivo {self.nombre}")
        return True


class Etiqueta:
    def __init__(self, nombre, categoria):
        self.nombre = nombre
        self.categoria = categoria

    def __eq__(self, other):
        if not isinstance(other, Etiqueta):
            return NotImplemented
        return self.nombre == other.nombre and self.categoria == other.categoria

    def __repr__(self):
        return f"Etiqueta({self.nombre!r}, {self.categoria!r})"


with Archivo("datos.txt") as f:
    pass  # simula operación con archivo

e1 = Etiqueta("python", "tech")
e2 = Etiqueta("python", "tech")
e3 = Etiqueta("java", "tech")

print(f"{repr(e1)} == {repr(e2)}: {e1 == e2}")
unicos = {e1, e2, e3}
print(f"Únicos: {len(unicos)}")

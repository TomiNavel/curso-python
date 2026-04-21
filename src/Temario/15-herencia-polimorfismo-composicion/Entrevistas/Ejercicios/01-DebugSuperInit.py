# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — super() e __init__
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Producto: Laptop, $999.00, Electrónica
# Producto: Python 101, $29.99, Libros (digital)
# =============================================================================

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"Producto: {self.nombre}, ${self.precio:.2f}"


class ProductoCategoria(Producto):
    def __init__(self, nombre, precio, categoria):
        self.categoria = categoria

    def __str__(self):
        return f"{super().__str__()}, {self.categoria}"


class ProductoDigital(ProductoCategoria):
    def __init__(self, nombre, precio, categoria):
        Producto.__init__(self, nombre, precio)
        self.categoria = categoria

    def __str__(self):
        return f"{ProductoCategoria.__str__(self)} (digital)"


laptop = ProductoCategoria("Laptop", 999, "Electrónica")
print(laptop)

libro = ProductoDigital("Python 101", 29.99, "Libros")
print(libro)

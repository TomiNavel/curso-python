# =====================
# SOLUCIÓN
# =====================
# Error 1: ProductoCategoria.__init__ no llama a super().__init__().
#   Los atributos nombre y precio nunca se inicializan.
#   Solución: añadir super().__init__(nombre, precio)
#
# Error 2: ProductoDigital.__init__ llama a Producto.__init__() directamente
#   en lugar de super().__init__(). Esto salta ProductoCategoria en el MRO y
#   es frágil. Debe usar super() para seguir la cadena correctamente.
#   Solución: super().__init__(nombre, precio, categoria)
#
# Error 3: ProductoDigital.__str__ llama a ProductoCategoria.__str__(self)
#   directamente en lugar de usar super().__str__().
#   Solución: super().__str__()
#
# ERRORES CORREGIDOS:
# 1. ProductoCategoria: añadir super().__init__(nombre, precio)
# 2. ProductoDigital: Producto.__init__ -> super().__init__(nombre, precio, categoria)
# 3. ProductoDigital: ProductoCategoria.__str__(self) -> super().__str__()


class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"Producto: {self.nombre}, ${self.precio:.2f}"


class ProductoCategoria(Producto):
    def __init__(self, nombre, precio, categoria):
        super().__init__(nombre, precio)
        self.categoria = categoria

    def __str__(self):
        return f"{super().__str__()}, {self.categoria}"


class ProductoDigital(ProductoCategoria):
    def __init__(self, nombre, precio, categoria):
        super().__init__(nombre, precio, categoria)
        self.categoria = categoria

    def __str__(self):
        return f"{super().__str__()} (digital)"


laptop = ProductoCategoria("Laptop", 999, "Electrónica")
print(laptop)

libro = ProductoDigital("Python 101", 29.99, "Libros")
print(libro)

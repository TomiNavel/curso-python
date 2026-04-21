class Producto:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def __repr__(self):
        return f"Producto({self.nombre!r}, {self.precio}, {self.stock})"

    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f} ({self.stock} uds)"


class Inventario:
    def __init__(self, nombre_tienda):
        self.nombre_tienda = nombre_tienda
        self.productos = []

    def agregar(self, producto):
        self.productos.append(producto)

    def buscar(self, nombre):
        for producto in self.productos:
            if producto.nombre == nombre:
                return producto
        return None

    def valor_total(self):
        return sum(p.precio * p.stock for p in self.productos)

    def productos_bajo_stock(self, minimo=5):
        return [p for p in self.productos if p.stock < minimo]

    def resumen(self):
        lineas = [f"=== Inventario de {self.nombre_tienda} ==="]
        for producto in self.productos:
            lineas.append(f"- {producto}")
        lineas.append(f"Valor total: ${self.valor_total():,.2f}")
        return "\n".join(lineas)


inv = Inventario("TechStore")
inv.agregar(Producto("Laptop", 999.99, 10))
inv.agregar(Producto("Mouse", 25.00, 3))
inv.agregar(Producto("Teclado", 75.50, 50))
print(inv.resumen())
print()
print(f"Bajo stock: {inv.productos_bajo_stock()}")
print(f"Buscar 'Mouse': {inv.buscar('Mouse')}")
print(f"Buscar 'Tablet': {inv.buscar('Tablet')}")

from dataclasses import dataclass, field


@dataclass
class Carrito:
    cliente: str
    productos: list = field(default_factory=list)

    def agregar(self, producto: str) -> None:
        self.productos.append(producto)

    def total_items(self) -> int:
        return len(self.productos)


# Pruebas
c1 = Carrito("Ana")
c1.agregar("Libro")
c1.agregar("Café")
print(c1)
print(c1.total_items())

c2 = Carrito("Luis")
print(c2)
print(c2.total_items())

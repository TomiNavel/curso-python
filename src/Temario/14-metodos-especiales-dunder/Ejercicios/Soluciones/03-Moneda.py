from functools import total_ordering


@total_ordering
class Moneda:
    def __init__(self, cantidad, divisa="EUR"):
        self.cantidad = round(cantidad, 2)
        self.divisa = divisa

    def __eq__(self, other):
        if not isinstance(other, Moneda):
            return NotImplemented
        return self.cantidad == other.cantidad and self.divisa == other.divisa

    def __lt__(self, other):
        if not isinstance(other, Moneda):
            return NotImplemented
        if self.divisa != other.divisa:
            raise ValueError(f"No se pueden comparar {self.divisa} y {other.divisa}")
        return self.cantidad < other.cantidad

    def __hash__(self):
        return hash((self.cantidad, self.divisa))

    def __bool__(self):
        return self.cantidad != 0

    def __repr__(self):
        return f"Moneda({self.cantidad}, {self.divisa!r})"

    def __str__(self):
        return f"{self.cantidad} {self.divisa}"


a = Moneda(29.99, "EUR")
b = Moneda(29.99, "EUR")
c = Moneda(50.00, "EUR")
d = Moneda(100, "USD")

print(a)
print(repr(a))
print(f"Iguales: {a == b}")
print(f"Menor: {a < c}")
print(f"Mayor o igual: {c >= a}")
print(f"Bool 0: {bool(Moneda(0))}")
print(f"Bool 100: {bool(Moneda(100))}")

monedas = {Moneda(10, "EUR"), Moneda(10, "EUR"), Moneda(20, "EUR"), Moneda(10, "USD")}
print(f"Únicos en set: {len(monedas)}")

precios = {Moneda(29.99, "EUR"): "Camiseta"}
print(f"Lookup dict: {list(precios.keys())[0]}")

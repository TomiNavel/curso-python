# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Property y recursión
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Producto: Laptop ($999.00)
# Producto: Laptop ($1099.00)
# Error: El precio no puede ser negativo
# =============================================================================

class Producto:
    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio  # no pasa por el setter

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self.precio  # recursión infinita

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        self.precio = valor  # recursión infinita

    def __str__(self):
        return f"Producto: {self._nombre} (${self._precio:.2f})"


p = Producto("Laptop", 999)
print(p)
p.precio = 1099
print(p)

try:
    p.precio = -50
except ValueError as e:
    print(f"Error: {e}")

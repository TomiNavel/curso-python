# =====================
# SOLUCIÓN
# =====================
# Error 1: En __init__, self._precio = precio asigna directamente al atributo
#   interno, saltándose la validación del setter. Con Producto("Laptop", -50)
#   se crearía un producto con precio negativo.
#   Solución: self.precio = precio (sin guion bajo, para pasar por el setter)
#
# Error 2: El getter de precio devuelve self.precio en lugar de self._precio.
#   Esto crea una recursión infinita: acceder a self.precio invoca el getter,
#   que accede a self.precio, que invoca el getter...
#   Solución: return self._precio
#
# Error 3: El setter de precio asigna self.precio = valor en lugar de
#   self._precio = valor. Misma recursión infinita que el getter.
#   Solución: self._precio = valor
#
# ERRORES CORREGIDOS:
# 1. self._precio = precio -> self.precio = precio en __init__
# 2. return self.precio -> return self._precio en getter
# 3. self.precio = valor -> self._precio = valor en setter


class Producto:
    def __init__(self, nombre, precio):
        self._nombre = nombre
        self.precio = precio  # pasa por el setter

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = valor

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

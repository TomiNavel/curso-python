# =====================
# SOLUCIÓN
# =====================
# Error 1: En __init__, self._email = email asigna directamente al atributo
#   interno, saltándose la validación del setter. Con Usuario("Ana", "sinArroba", 25)
#   se crearía un usuario con email inválido.
#   Solución: self.email = email (sin guion bajo, para pasar por el setter)
#
# Error 2: En __init__, self._edad = edad asigna directamente al atributo
#   interno, saltándose la validación del setter. Con Usuario("Ana", "a@b.com", -5)
#   se crearía un usuario con edad negativa.
#   Solución: self.edad = edad (sin guion bajo, para pasar por el setter)
#
# ERRORES CORREGIDOS:
# 1. self._email = email -> self.email = email en __init__
# 2. self._edad = edad -> self.edad = edad en __init__


class Usuario:
    def __init__(self, nombre, email, edad):
        self.nombre = nombre
        self.email = email  # pasa por el setter
        self.edad = edad  # pasa por el setter

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ValueError("Email inválido")
        self._email = valor

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, valor):
        if valor < 0 or valor > 150:
            raise ValueError("La edad debe estar entre 0 y 150")
        self._edad = valor

    def __str__(self):
        return f"Usuario: {self.nombre} ({self._email}), edad: {self._edad}"


u = Usuario("Ana", "ana@mail.com", 25)
print(u)

try:
    u.edad = -5
except ValueError as e:
    print(f"Error edad: {e}")

try:
    u.email = "sinArroba"
except ValueError as e:
    print(f"Error email: {e}")

u.edad = 30
print(f"Edad actualizada: {u.edad}")

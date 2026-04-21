# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Validación en __init__ y properties
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Usuario: Ana (ana@mail.com), edad: 25
# Error edad: La edad debe estar entre 0 y 150
# Error email: Email inválido
# Edad actualizada: 30
# =============================================================================

class Usuario:
    def __init__(self, nombre, email, edad):
        self.nombre = nombre
        self._email = email
        self._edad = edad

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

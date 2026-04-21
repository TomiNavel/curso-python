class Contacto:
    def __init__(self, nombre, email, telefono):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError("Email inválido")
        self._email = valor.lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        limpio = valor.replace(" ", "")
        if len(limpio) != 9 or not limpio.isdigit():
            raise ValueError("El teléfono debe tener 9 dígitos")
        self._telefono = limpio

    @property
    def dominio(self):
        return self._email.split("@")[1]

    def __str__(self):
        return f"{self._nombre} <{self._email}> ({self._telefono})"

    def __repr__(self):
        return f"Contacto({self._nombre!r}, {self._email!r}, {self._telefono!r})"


c = Contacto("Ana García", "ana@mail.com", "600111222")
print(c)
print(f"Dominio: {c.dominio}")
print(repr(c))

try:
    c.nombre = "   "
except ValueError as e:
    print(f"Error nombre: {e}")

try:
    c.email = "invalido"
except ValueError as e:
    print(f"Error email: {e}")

try:
    c.telefono = "12345"
except ValueError as e:
    print(f"Error teléfono: {e}")

c.email = "PEDRO@Empresa.ES"
print(f"Email normalizado: {c.email}")

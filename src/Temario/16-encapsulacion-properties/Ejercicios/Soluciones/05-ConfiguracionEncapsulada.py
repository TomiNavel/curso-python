class Configuracion:
    _ENTORNOS_VALIDOS = ("dev", "staging", "prod")

    def __init__(self, nombre, entorno, secreto):
        self.nombre = nombre
        self.entorno = entorno  # pasa por el setter
        self.__secreto = secreto

    @property
    def entorno(self):
        return self._entorno

    @entorno.setter
    def entorno(self, valor):
        if valor not in self._ENTORNOS_VALIDOS:
            raise ValueError(f"Entorno inválido: {valor}")
        self._entorno = valor

    @property
    def es_produccion(self):
        return self._entorno == "prod"

    def obtener_secreto(self, clave):
        if clave == "admin":
            return self.__secreto
        return "Acceso denegado"

    def cambiar_secreto(self, clave, nuevo_secreto):
        if clave != "admin":
            raise PermissionError("Clave incorrecta")
        self.__secreto = nuevo_secreto

    def __str__(self):
        return f"Config {self.nombre!r} [{self._entorno}] (producción: {self.es_produccion})"

    def __repr__(self):
        return f"Configuracion({self.nombre!r}, {self._entorno!r})"


c = Configuracion("API", "prod", "s3cr3t_k3y")
print(c)
c.entorno = "dev"
print(c)

try:
    c.entorno = "test"
except ValueError as e:
    print(f"Error entorno: {e}")

print(f"Secreto con clave correcta: {c.obtener_secreto('admin')}")
print(f"Secreto con clave incorrecta: {c.obtener_secreto('user')}")

c.cambiar_secreto("admin", "nueva_clave_123")
print(f"Secreto cambiado: {c.obtener_secreto('admin')}")

# Demostrar name mangling
print(f"Name mangling: s3cr3t_k3y existe como _Configuracion__secreto")

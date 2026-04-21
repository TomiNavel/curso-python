# =====================
# SOLUCIÓN
# =====================
# Error 1: __enter__ no devuelve self. Sin return, la variable "conn"
#   del bloque with es None, y conn.ejecutar() lanza AttributeError
#   porque NoneType no tiene el método ejecutar.
#   Solución: añadir "return self" en __enter__.
#
# Error 2: __exit__ devuelve False incondicionalmente. Cuando se produce
#   la excepción RuntimeError en el segundo bloque, __exit__ la registra
#   correctamente con el print, pero al devolver False la excepción se
#   propaga y el programa termina con un traceback. El resultado esperado
#   muestra que el programa debe continuar normalmente tras capturar el
#   error.
#   Solución: devolver True cuando hay excepción para suprimirla.
#
# Error 3: El atributo consultas no se reinicia al entrar en un nuevo
#   bloque with. Si se reutiliza el mismo objeto Conexion, el historial
#   acumula consultas de sesiones anteriores. __enter__ debe reiniciar
#   el estado de la conexión.
#   Solución: añadir self.consultas = [] en __enter__.
#
# ERRORES CORREGIDOS:
# 1. __enter__ sin return → return self
# 2. __exit__ devuelve False → devolver True cuando hay excepción
# 3. consultas no se reinicia en __enter__ → self.consultas = []


class Conexion:
    def __init__(self, servidor: str) -> None:
        self.servidor = servidor
        self.consultas: list[str] = []

    def __enter__(self):
        print(f"Conectando a {self.servidor}")
        self.consultas = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Error capturado: {exc_val}")
        print(f"Desconectando de {self.servidor}")
        return exc_type is not None

    def ejecutar(self, consulta: str) -> None:
        self.consultas.append(consulta)
        print(f"Ejecutando consulta: {consulta}")

    def historial(self) -> list[str]:
        return list(self.consultas)


# Pruebas
with Conexion("produccion") as conn:
    conn.ejecutar("SELECT * FROM users")

with Conexion("produccion") as conn:
    conn.ejecutar("INSERT INTO logs VALUES (1)")
    raise RuntimeError("fallo simulado")

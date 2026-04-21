# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Context manager con clase
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Conectando a produccion
# Ejecutando consulta: SELECT * FROM users
# Desconectando de produccion
# Conectando a produccion
# Ejecutando consulta: INSERT INTO logs VALUES (1)
# Error capturado: fallo simulado
# Desconectando de produccion
# =============================================================================


class Conexion:
    def __init__(self, servidor: str) -> None:
        self.servidor = servidor
        self.consultas: list[str] = []

    def __enter__(self):
        print(f"Conectando a {self.servidor}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Error capturado: {exc_val}")
        print(f"Desconectando de {self.servidor}")
        return False

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

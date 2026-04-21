# =====================
# SOLUCIÓN
# =====================
# Error 1: Usuario hereda explícitamente de Serializable. Los protocolos no
#   requieren herencia: basta con tener los métodos con la firma correcta.
#   Heredar de un protocolo elimina su principal ventaja (aceptar clases de
#   terceros sin modificarlas). Solución: "class Usuario:" sin herencia.
#
# Error 2: Producto define el método como `to_json` en lugar de `a_json`.
#   El protocolo exige un método llamado exactamente `a_json`. Aunque mypy
#   detectaría este error en tiempo de análisis estático, en tiempo de
#   ejecución serializar(Producto(...)) fallaría con AttributeError.
#   Solución: renombrar to_json a a_json.
#
# Error 3: Pedido no implementa a_json. Este caso es intencional para mostrar
#   que los protocolos NO verifican en tiempo de ejecución: la llamada
#   serializar(Pedido(42)) se compila sin problemas y solo falla al intentar
#   invocar el método ausente. El try/except ya captura el error. No es un
#   error a corregir, sino a entender: los protocolos son verificación
#   estática, no garantía de ejecución.
#
# ERRORES CORREGIDOS:
# 1. "class Usuario(Serializable):" -> "class Usuario:"
# 2. En Producto, "to_json" -> "a_json"


from typing import Protocol


class Serializable(Protocol):
    def a_json(self) -> str:
        ...


class Usuario:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def a_json(self) -> str:
        return f'{{"tipo": "usuario", "nombre": "{self.nombre}", "edad": {self.edad}}}'


class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def a_json(self) -> str:
        return f'{{"tipo": "producto", "nombre": "{self.nombre}", "precio": {self.precio}}}'


class Pedido:
    def __init__(self, id):
        self.id = id


def serializar(obj: Serializable) -> str:
    return obj.a_json()


print(serializar(Usuario("Ana", 28)))
print(serializar(Producto("Laptop", 999)))

try:
    print(serializar(Pedido(42)))
except AttributeError as e:
    print(f"Error: {e}")

# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Protocolo mal aplicado
# =============================================================================
# El siguiente código intenta usar un protocolo `Serializable` para procesar
# distintos tipos de objetos que pueden convertirse a JSON. Tiene 3 errores.
# Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# {"tipo": "usuario", "nombre": "Ana", "edad": 28}
# {"tipo": "producto", "nombre": "Laptop", "precio": 999}
# Error: 'Pedido' object has no attribute 'a_json'
# =============================================================================

from typing import Protocol


class Serializable(Protocol):
    def a_json(self) -> str:
        pass


class Usuario(Serializable):
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def a_json(self) -> str:
        return f'{{"tipo": "usuario", "nombre": "{self.nombre}", "edad": {self.edad}}}'


class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def to_json(self) -> str:
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

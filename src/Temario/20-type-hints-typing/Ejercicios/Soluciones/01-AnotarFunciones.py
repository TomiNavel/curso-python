def area_rectangulo(base: float, altura: float) -> float:
    return base * altura


def saludar(nombre: str | None = None) -> str:
    if nombre is None:
        return "Hola, invitado"
    return f"Hola, {nombre}"


def filtrar_pares(numeros: list[int]) -> list[int]:
    return [n for n in numeros if n % 2 == 0]


# Pruebas
print(area_rectangulo(3, 5))
print(saludar("Ana"))
print(saludar())
print(filtrar_pares([1, 2, 3, 4, 5, 6]))

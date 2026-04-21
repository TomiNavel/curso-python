from typing import Protocol


class Dibujable(Protocol):
    def dibujar(self) -> None:
        ...

    def ocultar(self) -> None:
        ...


class Boton:
    def __init__(self, texto):
        self.texto = texto

    def dibujar(self) -> None:
        print(f"Mostrando botón: {self.texto}")

    def ocultar(self) -> None:
        print(f"Ocultando botón: {self.texto}")


class Imagen:
    def __init__(self, ruta):
        self.ruta = ruta

    def dibujar(self) -> None:
        print(f"Renderizando imagen desde {self.ruta}")

    def ocultar(self) -> None:
        print(f"Ocultando imagen desde {self.ruta}")


class Etiqueta:
    def __init__(self, contenido):
        self.contenido = contenido

    def dibujar(self) -> None:
        print(f"Texto: {self.contenido}")

    def ocultar(self) -> None:
        print("Texto oculto")


def renderizar_todos(elementos: list[Dibujable]) -> None:
    for e in elementos:
        e.dibujar()


elementos = [
    Boton("Aceptar"),
    Imagen("/img/logo.png"),
    Etiqueta("Bienvenido"),
]

renderizar_todos(elementos)
elementos[0].ocultar()

# =============================================================================
# EJERCICIO 5: Protocolo Dibujable
# =============================================================================
# Crea un protocolo `Dibujable` que defina la forma requerida para renderizar
# cualquier elemento gráfico, sin obligar a heredar de ninguna clase.
#
# Protocolo Dibujable (hereda de typing.Protocol):
# - Método dibujar() -> None
# - Método ocultar() -> None
#
# Clases que deben satisfacer el protocolo (SIN heredar de Dibujable):
# - Boton(texto):
#     dibujar imprime "Mostrando botón: {texto}"
#     ocultar imprime "Ocultando botón: {texto}"
# - Imagen(ruta):
#     dibujar imprime "Renderizando imagen desde {ruta}"
#     ocultar imprime "Ocultando imagen desde {ruta}"
# - Etiqueta(contenido):
#     dibujar imprime "Texto: {contenido}"
#     ocultar imprime "Texto oculto"
#
# Función:
# - renderizar_todos(elementos: list[Dibujable]) -> None
#   Recorre la lista y llama a dibujar() en cada uno.
#
# Ninguna de las tres clases hereda de Dibujable. Satisfacen el protocolo
# simplemente por tener los métodos con la firma correcta.
#
# RESULTADO ESPERADO:
# Mostrando botón: Aceptar
# Renderizando imagen desde /img/logo.png
# Texto: Bienvenido
# Ocultando botón: Aceptar
# =============================================================================

# Tu código aquí

# elementos = [
#     Boton("Aceptar"),
#     Imagen("/img/logo.png"),
#     Etiqueta("Bienvenido"),
# ]
#
# renderizar_todos(elementos)
# elementos[0].ocultar()

# El bug: todas las lambdas capturan una REFERENCIA a la misma variable i.
# Cuando el bucle termina, i vale 4, y todas devuelven 4 ** 2 = 16.
# Resultado sin corregir: [16, 16, 16, 16, 16]

# Solución: capturar el valor actual con un argumento por defecto.
# Los argumentos por defecto se evalúan en el momento de la definición,
# no en el momento de la llamada.
funciones = []
for i in range(5):
    funciones.append(lambda i=i: i ** 2)

print([f() for f in funciones])  # [0, 1, 4, 9, 16]

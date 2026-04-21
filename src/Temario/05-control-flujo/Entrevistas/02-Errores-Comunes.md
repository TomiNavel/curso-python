# Errores comunes: Control de Flujo

## Error 1: Usar `=` en lugar de `==` en condiciones

`=` es asignación, `==` es comparación. En Python esto no compila (a diferencia de C, donde sí compila y causa bugs silenciosos), pero sigue siendo un error frecuente en principiantes.

```python
x = 10

# MAL — SyntaxError: asignación dentro de un if no es válida
if x = 10:
    print("es diez")

# BIEN — comparación
if x == 10:
    print("es diez")
```

## Error 2: Comparar con `==` en lugar de `is` para `None`

`==` compara valores, `is` compara identidad (si es el mismo objeto en memoria). `None` es un singleton — solo existe una instancia. Comparar con `==` puede dar resultados inesperados si un objeto redefine `__eq__`.

```python
valor = None

# MAL — funciona, pero no es idiomático y puede fallar con __eq__ personalizado
if valor == None:
    print("sin valor")

# BIEN — is compara identidad, que es lo correcto para None
if valor is None:
    print("sin valor")
```

## Error 3: Confundir `elif` con múltiples `if`

Usar varios `if` cuando se necesita `elif` hace que se evalúen todas las condiciones de forma independiente, ejecutando potencialmente varios bloques cuando solo se quería uno.

```python
nota = 85

# MAL — imprime "Aprobado" Y "Suficiente" porque ambos if son independientes
if nota >= 70:
    print("Aprobado")
if nota >= 50:
    print("Suficiente")

# BIEN — solo imprime "Aprobado"
if nota >= 70:
    print("Aprobado")
elif nota >= 50:
    print("Suficiente")
```

## Error 4: Olvidar los dos puntos `:` al final de `if`, `for`, `while`

Python usa `:` para indicar el inicio de un bloque. Olvidarlo produce `SyntaxError`. Es un error trivial pero muy frecuente al empezar.

```python
# MAL — SyntaxError
if x > 5
    print("mayor")

for i in range(3)
    print(i)

# BIEN
if x > 5:
    print("mayor")

for i in range(3):
    print(i)
```

## Error 5: Modificar una lista mientras se itera sobre ella

Eliminar o añadir elementos durante una iteración `for` desplaza los índices internos. El bucle puede saltarse elementos o procesarlos dos veces.

```python
numeros = [1, 2, 3, 4, 5, 6]

# MAL — se salta el 4 porque al eliminar el 2, los índices se desplazan
for n in numeros:
    if n % 2 == 0:
        numeros.remove(n)
print(numeros)  # [1, 3, 5]? Resultado real: [1, 3, 5] aquí, pero falla con otras listas

# BIEN — iterar sobre una copia con [:]
for n in numeros[:]:
    if n % 2 == 0:
        numeros.remove(n)
```

## Error 6: Usar `range(len(...))` en lugar de `enumerate()`

Iterar con `range(len(lista))` y luego acceder por índice es redundante cuando ya se tiene el elemento disponible. No es un error funcional, pero es un antipatrón que produce código menos legible.

```python
frutas = ["manzana", "pera", "uva"]

# MAL — redundante, accede por índice cuando el elemento está disponible
for i in range(len(frutas)):
    print(f"{i}: {frutas[i]}")

# BIEN — enumerate da índice y valor directamente
for i, fruta in enumerate(frutas):
    print(f"{i}: {fruta}")
```

## Error 7: Asumir que `else` en un bucle se ejecuta cuando la condición es falsa

El `else` de un bucle no funciona como el `else` de un `if`. Se ejecuta cuando el bucle **termina sin `break`**, no cuando la condición del `while` es falsa (aunque en `while` coincide si no hay `break`). La confusión lleva a resultados inesperados.

```python
numeros = [1, 3, 5, 7]

# El else se ejecuta porque el bucle terminó sin break (no encontró par)
for n in numeros:
    if n % 2 == 0:
        print(f"Par encontrado: {n}")
        break
else:
    print("No hay pares")  # se ejecuta

# Si se añade un 4 a la lista, el break se ejecuta y el else NO se ejecuta
```

## Error 8: Crear un bucle infinito por no actualizar la condición

Si la variable que controla la condición del `while` no se modifica dentro del bucle, la condición nunca cambia y el bucle no termina.

```python
# MAL — bucle infinito: i nunca cambia
i = 0
while i < 5:
    print(i)
    # falta: i += 1

# BIEN
i = 0
while i < 5:
    print(i)
    i += 1
```

## Error 9: Confundir `break` con `continue`

`break` termina el bucle entero. `continue` salta a la siguiente iteración. Usar uno cuando se necesita el otro cambia completamente el comportamiento.

```python
# Se quiere saltar los negativos y procesar el resto
numeros = [-1, 2, -3, 4, 5]

# MAL — break termina el bucle al primer negativo, no procesa nada más
for n in numeros:
    if n < 0:
        break
    print(n)  # solo imprime... nada, porque el primero es -1

# BIEN — continue salta los negativos y sigue con el resto
for n in numeros:
    if n < 0:
        continue
    print(n)  # imprime 2, 4, 5
```

## Error 10: Olvidar que `range()` excluye el último valor

`range(5)` genera `0, 1, 2, 3, 4` — el 5 no está incluido. Es consistente con el slicing de Python, pero causa errores de "off-by-one" si se espera que el final esté incluido.

```python
# MAL — si se quiere imprimir del 1 al 5, esto solo llega al 4
for i in range(1, 5):
    print(i)  # 1, 2, 3, 4

# BIEN — incluir 6 como fin para que 5 entre
for i in range(1, 6):
    print(i)  # 1, 2, 3, 4, 5
```

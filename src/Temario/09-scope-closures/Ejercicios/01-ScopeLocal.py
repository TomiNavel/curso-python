# =============================================================================
# EJERCICIO 1: Scope Local
# =============================================================================
# Para cada bloque de código, escribe qué imprime o si lanza un error.
# NO ejecutes el código — el objetivo es entender las reglas de scope.
#
# Después de escribir tu predicción, descomenta la llamada para verificar.
#
# =============================================================================

# BLOQUE 1: ¿Qué imprime?
x = 10

def bloque1():
    print(x)

# Tu predicción: ___
# bloque1()


# BLOQUE 2: ¿Qué imprime o qué error lanza?
y = 10

def bloque2():
    print(y)
    y = 20

# Tu predicción: ___
# bloque2()


# BLOQUE 3: ¿Qué imprime?
z = 1

def bloque3():
    z = 99
    def interna():
        print(z)
    z = 1
    interna()

# Tu predicción: ___
# bloque3()


# BLOQUE 4: ¿Qué imprime?
a = "global"

def bloque4():
    a = "local"
    print(a)

# Tu predicción: ___
# bloque4()


# BLOQUE 5: ¿Qué imprime?
def bloque5():
    x = 5
    def interna():
        print(x)
    interna()

# Tu predicción: ___
# bloque5()
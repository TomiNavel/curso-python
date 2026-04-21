# BLOQUE 1: imprime 10
# No hay asignación a x dentro de bloque1(), así que Python busca en el scope
# global y encuentra x = 10.
x = 10

def bloque1():
    print(x)

bloque1()  # 10


# BLOQUE 2: UnboundLocalError
# Hay una asignación y = 20 dentro de la función, así que Python marca y como
# local en TODA la función. Cuando print(y) se ejecuta antes de la asignación,
# la variable local existe pero no tiene valor.
y = 10

def bloque2():
    try:
        print(y)
        y = 20
    except UnboundLocalError as e:
        print(f"UnboundLocalError: {e}")

bloque2()


# BLOQUE 3: imprime 1
# La función interna() captura una REFERENCIA a z, no su valor.
# z se reasigna a 1 ANTES de llamar a interna(), así que interna() ve z = 1.
z = 1

def bloque3():
    z = 99
    def interna():
        print(z)
    z = 1
    interna()

bloque3()  # 1


# BLOQUE 4: imprime "local"
# La asignación a = "local" crea una variable local que oculta la global.
# print(a) lee la variable local.
a = "global"

def bloque4():
    a = "local"
    print(a)

bloque4()  # local


# BLOQUE 5: imprime 5
# interna() no tiene x local, así que busca en el scope Enclosing (bloque5)
# y encuentra x = 5.
def bloque5():
    x = 5
    def interna():
        print(x)
    interna()

bloque5()  # 5

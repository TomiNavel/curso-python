# =====================
# SOLUCIÓN
# =====================
# Error 1: precio = precio * 0.8 hace que Python marque precio como local.
#   Al intentar leer precio para multiplicar, la variable local no tiene valor.
#   Corrección: añadir "global precio" al inicio de la función.
#
# Error 2: intentos -= 1 es una asignación (intentos = intentos - 1), lo que
#   marca intentos como local en usar_intento(). Necesita nonlocal.
#   Corrección: añadir "nonlocal intentos" al inicio de usar_intento().
#
# Error 3: las asignaciones en aplicar_tema() crean variables locales nuevas
#   que no afectan a las de configurar(). Necesitan nonlocal.
#   Corrección: añadir "nonlocal modo, idioma" al inicio de aplicar_tema().
#
# ERRORES CORREGIDOS:
# 1. Añadir "global precio" en aplicar_descuento()
# 2. Añadir "nonlocal intentos" en usar_intento()
# 3. Añadir "nonlocal modo, idioma" en aplicar_tema()


precio = 100

def aplicar_descuento():
    global precio
    precio = precio * 0.8
    print(f"Descuento aplicado: {precio}")

aplicar_descuento()


def gestionar_intentos():
    intentos = 3

    def usar_intento():
        nonlocal intentos
        intentos -= 1
        return intentos

    restantes = usar_intento()
    print(f"Intentos restantes: {restantes}")

gestionar_intentos()


def configurar():
    modo = "claro"
    idioma = "en"

    def aplicar_tema():
        nonlocal modo, idioma
        modo = "oscuro"
        idioma = "es"

    aplicar_tema()
    print(f"Configuración: modo={modo}, idioma={idioma}")

configurar()

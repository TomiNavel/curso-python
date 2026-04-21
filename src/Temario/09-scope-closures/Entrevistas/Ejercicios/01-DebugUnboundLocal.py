# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — UnboundLocalError
# =============================================================================
# El siguiente código tiene 3 errores relacionados con scope.
# Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Descuento aplicado: 80.0
# Intentos restantes: 2
# Configuración: modo=oscuro, idioma=es
# =============================================================================

# Error 1: la función debería aplicar un 20% de descuento al precio global
precio = 100

def aplicar_descuento():
    precio = precio * 0.8
    print(f"Descuento aplicado: {precio}")

aplicar_descuento()


# Error 2: la función interna debería decrementar los intentos de la externa
def gestionar_intentos():
    intentos = 3

    def usar_intento():
        intentos -= 1
        return intentos

    restantes = usar_intento()
    print(f"Intentos restantes: {restantes}")

gestionar_intentos()


# Error 3: la función interna debería modificar las variables de la externa
def configurar():
    modo = "claro"
    idioma = "en"

    def aplicar_tema():
        modo = "oscuro"
        idioma = "es"

    aplicar_tema()
    print(f"Configuración: modo={modo}, idioma={idioma}")

configurar()

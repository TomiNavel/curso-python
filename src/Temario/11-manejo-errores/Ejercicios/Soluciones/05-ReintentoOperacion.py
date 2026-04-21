def reintentar(funcion, max_intentos=3):
    ultima_excepcion = None

    for intento in range(1, max_intentos + 1):
        try:
            return funcion()
        except Exception as e:
            ultima_excepcion = e
            print(f"Intento {intento}/{max_intentos}: {e}")

    raise ultima_excepcion


# --- Código de prueba ---

contador = 0

def operacion_inestable():
    global contador
    contador += 1
    if contador < 3:
        raise RuntimeError("fallo simulado")
    print(f"Éxito en intento {contador}")
    return "ok"

def operacion_imposible():
    raise RuntimeError("siempre fallo")

resultado = reintentar(operacion_inestable, max_intentos=3)
print(f"Resultado: {resultado}")

print("---")

try:
    reintentar(operacion_imposible, max_intentos=2)
except RuntimeError as e:
    print(f"Error final: {e}")

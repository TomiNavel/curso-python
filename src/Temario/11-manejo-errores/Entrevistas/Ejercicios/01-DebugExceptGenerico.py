# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Except Genérico
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Resultado: 5.0
# Error: division by zero
# Error: No se pudo convertir 'abc' a número
# =============================================================================

def dividir_seguro(a, b):
    try:
        resultado = a / b
        return resultado
    except:
        print("Algo salió mal")
        return None

def convertir_y_dividir(texto, divisor):
    try:
        numero = int(texto)
        resultado = dividir_seguro(numero, divisor)
        print(f"Resultado: {resultado}")
    except Exception as e:
        print(f"Error: {e}")


convertir_y_dividir("10", 2)
convertir_y_dividir("10", 0)
convertir_y_dividir("abc", 1)

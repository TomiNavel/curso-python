# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Generador que malgasta memoria
# =============================================================================
# El siguiente código intenta procesar un rango muy grande sumando los
# cuadrados de los números múltiplos de 5. El autor quería usar generadores
# para mantener el consumo de memoria constante, pero lo hizo mal. Tiene
# 3 errores relacionados con el uso incorrecto de generadores. Encuéntralos
# y corrígelos.
#
# RESULTADO ESPERADO:
# 66661666750000
# =============================================================================


def multiplos_de_cinco(limite):
    return [n for n in range(limite) if n % 5 == 0]


def cuadrados(numeros):
    resultado = []
    for n in numeros:
        resultado.append(n * n)
    return resultado


limite = 100_000
pipeline = cuadrados(multiplos_de_cinco(limite))
print(sum([x for x in pipeline]))

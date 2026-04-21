import random
import string


def generar_password(longitud=12, mayusculas=True, digitos=True, especiales=False):
    if longitud < 4:
        raise ValueError("La longitud mínima es 4")

    caracteres = string.ascii_lowercase
    obligatorios = [random.choice(string.ascii_lowercase)]

    if mayusculas:
        caracteres += string.ascii_uppercase
        obligatorios.append(random.choice(string.ascii_uppercase))
    if digitos:
        caracteres += string.digits
        obligatorios.append(random.choice(string.digits))
    if especiales:
        caracteres += string.punctuation
        obligatorios.append(random.choice(string.punctuation))

    restantes = [random.choice(caracteres) for _ in range(longitud - len(obligatorios))]

    password = obligatorios + restantes
    random.shuffle(password)

    return "".join(password)


def evaluar_fortaleza(password):
    tipos = 0
    if any(c in string.ascii_lowercase for c in password):
        tipos += 1
    if any(c in string.ascii_uppercase for c in password):
        tipos += 1
    if any(c in string.digits for c in password):
        tipos += 1
    if any(c in string.punctuation for c in password):
        tipos += 1

    if tipos <= 1:
        return "débil"
    elif tipos <= 3:
        return "media"
    else:
        return "fuerte"


random.seed(42)
print(generar_password())
print(generar_password(8, especiales=True))
print(generar_password(6, mayusculas=False, digitos=False))
print()
print(evaluar_fortaleza("abcdef"))
print(evaluar_fortaleza("aBc123"))
print(evaluar_fortaleza("aB3!xY9@"))

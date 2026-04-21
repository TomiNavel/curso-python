# PASO 1
texto = "Python"
total = 0
for caracter in texto:
    if caracter.lower() in "aeiou":
        total += 1
print(f"Total vocales: {total}")

# PASO 2
texto = "Murcielago"
cont_a = 0
cont_e = 0
cont_i = 0
cont_o = 0
cont_u = 0

for caracter in texto:
    letra = caracter.lower()
    if letra == "a":
        cont_a += 1
    elif letra == "e":
        cont_e += 1
    elif letra == "i":
        cont_i += 1
    elif letra == "o":
        cont_o += 1
    elif letra == "u":
        cont_u += 1

total = cont_a + cont_e + cont_i + cont_o + cont_u
print(f"Total vocales: {total}")
print(f"a: {cont_a}, e: {cont_e}, i: {cont_i}, o: {cont_o}, u: {cont_u}")

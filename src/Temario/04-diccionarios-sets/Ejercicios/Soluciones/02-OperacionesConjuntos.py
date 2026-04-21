# PASO 1
lenguajes = {"Python", "Java", "JavaScript", "Go"}
print(lenguajes)

# PASO 2
lenguajes.discard("Go")
lenguajes.discard("C++")
print(lenguajes)

# PASO 3
lenguajes.update({"TypeScript", "Rust"})
print(lenguajes)

# PASO 4
frontend = {"JavaScript", "TypeScript", "Python"}
print(lenguajes & frontend)

# PASO 5
print(frontend - lenguajes)

# PASO 6
print(lenguajes ^ frontend)

# PASO 7
print(frontend.issubset(lenguajes))
print(lenguajes.isdisjoint(frontend))

# PASO 8
permisos = frozenset({"lectura", "escritura"})
print(permisos)
roles = {permisos: "editor"}
print(roles[permisos])

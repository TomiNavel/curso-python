# =============================================================================
# EJERCICIO 3: Contacto con Validación
# =============================================================================
# Crea una clase `Contacto` con properties que validen nombre, email y teléfono.
#
# Properties con getter y setter:
# - nombre: no puede ser vacío ni solo espacios (ValueError). Se almacena
#   con strip() aplicado.
# - email: debe contener "@" y "." después del "@" (ValueError).
#   Se almacena en minúsculas.
# - telefono: debe tener exactamente 9 dígitos (ValueError).
#   Se almacena como string sin espacios.
#
# Property calculada:
# - dominio: devuelve la parte después del "@" del email.
#
# __str__: "Ana García <ana@mail.com> (600111222)"
# __repr__: Contacto('Ana García', 'ana@mail.com', '600111222')
#
# RESULTADO ESPERADO:
# Ana García <ana@mail.com> (600111222)
# Dominio: mail.com
# Contacto('Ana García', 'ana@mail.com', '600111222')
# Error nombre: El nombre no puede estar vacío
# Error email: Email inválido
# Error teléfono: El teléfono debe tener 9 dígitos
# Email normalizado: pedro@empresa.es
# =============================================================================

# Tu código aquí

# c = Contacto("Ana García", "ana@mail.com", "600111222")
# print(c)
# print(f"Dominio: {c.dominio}")
# print(repr(c))
#
# try:
#     c.nombre = "   "
# except ValueError as e:
#     print(f"Error nombre: {e}")
#
# try:
#     c.email = "invalido"
# except ValueError as e:
#     print(f"Error email: {e}")
#
# try:
#     c.telefono = "12345"
# except ValueError as e:
#     print(f"Error teléfono: {e}")
#
# c.email = "PEDRO@Empresa.ES"
# print(f"Email normalizado: {c.email}")

import bisect


class ColeccionOrdenada:
    def __init__(self):
        self._datos = []

    def agregar(self, elemento):
        bisect.insort(self._datos, elemento)

    def __len__(self):
        return len(self._datos)

    def __getitem__(self, indice):
        return self._datos[indice]

    def __contains__(self, elemento):
        i = bisect.bisect_left(self._datos, elemento)
        return i < len(self._datos) and self._datos[i] == elemento

    def __iter__(self):
        return iter(self._datos)

    def __bool__(self):
        return len(self._datos) > 0

    def __repr__(self):
        return f"ColeccionOrdenada({self._datos})"


col = ColeccionOrdenada()
for n in [5, 1, 9, 3, 7]:
    col.agregar(n)
print(repr(col))
print(f"Longitud: {len(col)}")
print(f"Elemento [0]: {col[0]}")
print(f"Elemento [-1]: {col[-1]}")
print(f"Slice [1:4]: {col[1:4]}")
print(f"5 está: {5 in col}")
print(f"6 está: {6 in col}")
vacia = ColeccionOrdenada()
print(f"Bool vacía: {bool(vacia)}")
print(f"Bool con datos: {bool(col)}")
print("Iteración:", " ".join(str(x) for x in col))

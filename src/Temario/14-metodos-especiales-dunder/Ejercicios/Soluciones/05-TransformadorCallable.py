class Transformador:
    def __init__(self, *funciones):
        self.transformaciones = list(funciones)
        self.historial = []

    def __call__(self, valor):
        entrada = valor
        resultado = valor
        for fn in self.transformaciones:
            resultado = fn(resultado)
        self.historial.append((entrada, resultado))
        return resultado

    def __len__(self):
        return len(self.transformaciones)

    def __getitem__(self, indice):
        return self.historial[indice]

    def __iter__(self):
        return iter(self.historial)

    def __bool__(self):
        return len(self.historial) > 0

    def __repr__(self):
        return f"Transformador({len(self.transformaciones)} funciones, {len(self.historial)} llamadas)"


t = Transformador(lambda x: x + 5, lambda x: x * 3)
print(f"Resultado 1: {t(5)}")      # 5+5=10, 10*3=30
print(f"Resultado 2: {t(-10)}")    # -10+5=-5, -5*3=-15
print(f"Resultado 3: {t(0)}")      # 0+5=5, 5*3=15
print(f"Repr: {repr(t)}")
print(f"Historial [0]: {t[0]}")
print(f"Historial [1]: {t[1]}")
print(f"Tiene historial: {bool(t)}")
print("Recorrido:")
for entrada, salida in t:
    print(f"  {entrada} -> {salida}")

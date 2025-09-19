from typing import Union, List

TASAS_PORCENTAJE = {
    "exento": 0.00,
    "iva19":  0.19,
    "iva5":   0.05,
    "inc8":   0.08,
    "licor25": 0.25,
}

IMPUESTO_BOLSA_FIJO_COP = 50


class CalculadoraImpuestos:
    def __init__(self, precio_base: Union[int, float], tipo_impuesto: Union[str, List[str]]):
        self.precio_base = precio_base
        self.tipo_impuesto = tipo_impuesto

    def _validar_entradas(self) -> None:
        if not isinstance(self.precio_base, (int, float)):
            raise TypeError("El precio base debe ser numérico (int o float).")
        if self.precio_base < 0:
            raise ValueError("El precio base no puede ser negativo.")

        if isinstance(self.tipo_impuesto, str):
            if self.tipo_impuesto.strip() == "":
                raise ValueError("El tipo de impuesto no puede ser vacío.")
        elif isinstance(self.tipo_impuesto, list):
            if not self.tipo_impuesto:
                raise ValueError("La lista de impuestos no puede estar vacía.")
            for t in self.tipo_impuesto:
                if not isinstance(t, str) or not t.strip():
                    raise ValueError("Todos los impuestos deben ser cadenas no vacías.")
        else:
            raise TypeError("El tipo de impuesto debe ser str o list[str].")

    def _sumar_impuesto_al_total(self, total_actual: float, tipo: str) -> float:
        tipo = tipo.strip().lower()

        if tipo == "bolsa":
            return total_actual + IMPUESTO_BOLSA_FIJO_COP

        if tipo in TASAS_PORCENTAJE:
            return total_actual + (self.precio_base * TASAS_PORCENTAJE[tipo])

        raise ValueError(f"Tipo de impuesto desconocido: {tipo}")

    def calcular(self) -> int:
        self._validar_entradas()
        total = float(self.precio_base)

        if isinstance(self.tipo_impuesto, str):
            total = self._sumar_impuesto_al_total(total, self.tipo_impuesto)
            return round(total)

        for t in self.tipo_impuesto:
            total = self._sumar_impuesto_al_total(total, t)

        return round(total)



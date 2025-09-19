from src.model.impuestos_model import CalculadoraImpuestos

def parsear_tipos(cadena: str):
    if "," in cadena:
        return [t.strip() for t in cadena.split(",") if t.strip()]
    return cadena.strip()

def calcular_total(precio, tipos):
    return CalculadoraImpuestos(precio, tipos).calcular()

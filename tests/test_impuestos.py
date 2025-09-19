import unittest
from src.model.impuestos_model import CalculadoraImpuestos

class TestImpuestos(unittest.TestCase):
    # ---------- Casos NORMALES (4) ----------
    def test_normal_1(self):
        # Exento
        precio = 5000
        tipo = "exento"
        esperado = 5000
        resultado = CalculadoraImpuestos(precio, tipo).calcular()
        self.assertEqual(resultado, esperado)

    def test_normal_2(self):
        # IVA 19%
        precio = 10000
        tipo = "iva19"
        esperado = 11900
        resultado = CalculadoraImpuestos(precio, tipo).calcular()
        self.assertEqual(resultado, esperado)

    def test_normal_3(self):
        # INC 8%
        precio = 8000
        tipo = "inc8"
        esperado = 8640
        resultado = CalculadoraImpuestos(precio, tipo).calcular()
        self.assertEqual(resultado, esperado)

    def test_normal_4(self):
        # Bolsa plástica (fijo 50)
        precio = 0
        tipo = "bolsa"
        esperado = 50
        resultado = CalculadoraImpuestos(precio, tipo).calcular()
        self.assertEqual(resultado, esperado)

    # ---------- Casos EXTRAORDINARIOS (3) ----------
    def test_extraordinario_1(self):
        # Licor 25% sobre 10,000
        precio = 10000
        tipo = "licor25"
        esperado = 12500
        resultado = CalculadoraImpuestos(precio, tipo).calcular()
        self.assertEqual(resultado, esperado)

    def test_extraordinario_2(self):
        # IVA 5% sobre 10,000
        precio = 10000
        tipo = "iva5"
        esperado = 10500
        resultado = CalculadoraImpuestos(precio, tipo).calcular()
        self.assertEqual(resultado, esperado)

    def test_extraordinario_3(self):
        # Combo: INC 8% + bolsa (50) sobre 10,000 => 10,000 + 800 + 50 = 10,850
        precio = 10000
        tipos = ["inc8", "bolsa"]
        esperado = 10850
        resultado = CalculadoraImpuestos(precio, tipos).calcular()
        self.assertEqual(resultado, esperado)

    # ---------- Casos de ERROR (4) ----------
    def test_error_1_precio_negativo(self):
        with self.assertRaises(ValueError):
            CalculadoraImpuestos(-5000, "iva19").calcular()

    def test_error_2_impuesto_desconocido(self):
        with self.assertRaises(ValueError):
            CalculadoraImpuestos(10000, "impuesto_raro").calcular()

    def test_error_3_impuesto_vacio(self):
        with self.assertRaises(ValueError):
            CalculadoraImpuestos(10000, "").calcular()

    def test_error_4_precio_no_numerico(self):
        with self.assertRaises(TypeError):
            CalculadoraImpuestos("cinco mil", "iva5").calcular()

if __name__ == "__main__":
    unittest.main()



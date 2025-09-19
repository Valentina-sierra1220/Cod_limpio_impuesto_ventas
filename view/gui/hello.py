# --- bootstrap para ejecutar este archivo directamente desde view/gui/ ---
import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))  # sube 2 niveles hasta la raíz
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# ------------------------------------------------------------------------

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from src.controller.impuestos_controller import parsear_tipos, calcular_total

KV = """
#:import dp kivy.metrics.dp

<Chip@ToggleButton>:
    size_hint_y: None
    height: dp(36)
    background_normal: ""
    background_down: ""
    background_color: (0.92, 0.94, 0.98, 1) if self.state == "normal" else (0.40, 0.60, 0.98, 1)
    color: (0.15, 0.20, 0.30, 1) if self.state == "normal" else (1, 1, 1, 1)
    font_size: dp(13)

<VistaCalculadora>:
    orientation: "vertical"
    padding: dp(16)
    spacing: dp(12)

    Label:
        text: "Calculadora de impuestos"
        font_size: dp(20)
        size_hint_y: None
        height: dp(40)

    BoxLayout:
        size_hint_y: None
        height: dp(44)
        spacing: dp(8)
        Label:
            text: "Precio base"
            size_hint_x: 0.35
        TextInput:
            id: inp_precio
            hint_text: "Ej: 10000"
            input_filter: "float"
            multiline: False

    BoxLayout:
        size_hint_y: None
        height: dp(44)
        spacing: dp(8)
        Label:
            text: "Impuestos"
            size_hint_x: 0.35
        TextInput:
            id: inp_impuestos
            hint_text: "Ej: iva19, bolsa"
            multiline: False
            on_text: root.sincronizar_desde_texto(self.text)

    GridLayout:
        cols: 3
        size_hint_y: None
        height: dp(90)
        spacing: dp(8)
        Chip:
            id: chip_exento
            text: "exento"
            on_state: root.alternar_chip(self.text, self.state)
        Chip:
            id: chip_iva19
            text: "iva19"
            on_state: root.alternar_chip(self.text, self.state)
        Chip:
            id: chip_iva5
            text: "iva5"
            on_state: root.alternar_chip(self.text, self.state)
        Chip:
            id: chip_inc8
            text: "inc8"
            on_state: root.alternar_chip(self.text, self.state)
        Chip:
            id: chip_licor25
            text: "licor25"
            on_state: root.alternar_chip(self.text, self.state)
        Chip:
            id: chip_bolsa
            text: "bolsa"
            on_state: root.alternar_chip(self.text, self.state)

    BoxLayout:
        size_hint_y: None
        height: dp(44)
        spacing: dp(10)
        Button:
            text: "Calcular"
            on_release: root.calcular(inp_precio.text, inp_impuestos.text)
        Button:
            text: "Limpiar"
            on_release: root.limpiar_formulario(inp_precio, inp_impuestos)

    Label:
        id: lbl_resultado
        text: "Ingresa un precio y selecciona impuestos."
        halign: "left"
        valign: "top"
        text_size: self.size
"""

IMPUESTOS_VALIDOS = ("exento", "iva19", "iva5", "inc8", "licor25", "bolsa")


class VistaCalculadora(BoxLayout):
    def on_kv_post(self, _):
        self.chips = {
            "exento": self.ids.chip_exento,
            "iva19": self.ids.chip_iva19,
            "iva5": self.ids.chip_iva5,
            "inc8": self.ids.chip_inc8,
            "licor25": self.ids.chip_licor25,
            "bolsa": self.ids.chip_bolsa,
        }

    def alternar_chip(self, nombre: str, estado: str) -> None:
        if estado == "down":
            if nombre == "exento":
                for k, c in self.chips.items():
                    c.state = "down" if k == "exento" else "normal"
            else:
                self.chips["exento"].state = "normal"

        activos = [k for k, c in self.chips.items() if c.state == "down"]
        if "exento" in activos and len(activos) > 1:
            for c in self.chips.values():
                c.state = "normal"
            self.chips["exento"].state = "down"
            activos = ["exento"]

        self.ids.inp_impuestos.text = ", ".join(activos)

    def sincronizar_desde_texto(self, texto: str) -> None:
        lista = [p.strip().lower() for p in texto.replace(";", ",").replace("|", ",").split(",") if p.strip()]
        lista = [p for p in lista if p in IMPUESTOS_VALIDOS]
        if "exento" in lista:
            lista = ["exento"]
        for k, c in self.chips.items():
            c.state = "down" if k in lista else "normal"

    def limpiar_formulario(self, campo_precio, campo_impuestos) -> None:
        campo_precio.text = ""
        campo_impuestos.text = ""
        for c in self.chips.values():
            c.state = "normal"
        self.ids.lbl_resultado.text = "Formulario limpio."

    def calcular(self, precio_txt: str, impuestos_txt: str) -> None:
        precio_txt = (precio_txt or "").strip()
        if not precio_txt:
            self.ids.lbl_resultado.text = "⚠ Ingresa un precio base."
            return
        try:
            precio = float(precio_txt)
            if precio < 0:
                self.ids.lbl_resultado.text = "⚠ El precio debe ser ≥ 0."
                return
        except ValueError:
            self.ids.lbl_resultado.text = "❌ El precio debe ser numérico."
            return

        impuestos_txt = (impuestos_txt or self.ids.inp_impuestos.text or "").strip()
        try:
            tipos = parsear_tipos(impuestos_txt)
            total = calcular_total(precio, tipos)
            self.ids.lbl_resultado.text = (
                "✅ Total calculado:\n"
                f"• Precio base: {precio}\n"
                f"• Impuesto(s): {tipos}\n"
                f"• Total a pagar: {total}"
            )
        except (ValueError, TypeError) as e:
            self.ids.lbl_resultado.text = f"❌ Error: {e}"


class AppCalculadoraImpuestos(App):
    title = "Calculadora de impuestos"
    def build(self):
        Builder.load_string(KV)
        return VistaCalculadora()


if __name__ == "__main__":
    AppCalculadoraImpuestos().run()

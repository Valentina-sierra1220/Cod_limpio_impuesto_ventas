# --- bootstrap para ejecutar este archivo directamente desde view/gui/ ---
import os
import sys
from typing import Dict

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

# --- bootstrap para rutas ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))  # sube 2 niveles hasta raíz
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
# -----------------------------

from src.controller.impuestos_controller import parsear_tipos, calcular_total

# ================================
# Definición de la interfaz en KV
# ================================
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

    Label:
        text: "Historial de cálculos"
        font_size: dp(16)
        size_hint_y: None
        height: dp(30)

    ScrollView:
        size_hint_y: 0.4
        do_scroll_x: False
        do_scroll_y: True
        Label:
            id: lbl_historial
            text: ""
            halign: "left"
            valign: "top"
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]
"""

IMPUESTOS_VALIDOS = ("exento", "iva19", "iva5", "inc8", "licor25", "bolsa")


# ================================
# Funciones auxiliares
# ================================
def mostrar_popup(mensaje: str, titulo: str = "⚠ Error"):
    """
    Muestra una ventana emergente con el mensaje de error.
    """
    from kivy.uix.boxlayout import BoxLayout

    box = BoxLayout(orientation="vertical", spacing=10, padding=10)
    lbl = Label(text=mensaje)
    btn = Button(text="Cerrar", size_hint_y=None, height=40)

    box.add_widget(lbl)
    box.add_widget(btn)

    popup = Popup(
        title=titulo,
        content=box,
        size_hint=(0.6, 0.4),
        auto_dismiss=False,
    )
    btn.bind(on_release=popup.dismiss)
    popup.open()


# ================================
# Clase principal de la vista
# ================================
class VistaCalculadora(BoxLayout):
    """
    Vista principal de la calculadora de impuestos.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chips: Dict[str, object] = {}
        self.historial = []

    def on_kv_post(self, _):
        """
        Inicializa los chips después de cargar la interfaz.
        """
        self.chips = {
            "exento": self.ids.chip_exento,
            "iva19": self.ids.chip_iva19,
            "iva5": self.ids.chip_iva5,
            "inc8": self.ids.chip_inc8,
            "licor25": self.ids.chip_licor25,
            "bolsa": self.ids.chip_bolsa,
        }

    # ----------------------------
    # Manejo de chips
    # ----------------------------
    def alternar_chip(self, nombre: str, estado: str) -> None:
        """
        Sincroniza los chips con el campo de impuestos.
        """
        impuestos_actuales = [
            p.strip() for p in self.ids.inp_impuestos.text.split(",") if p.strip()
        ]
        if estado == "down":
            if nombre not in impuestos_actuales:
                impuestos_actuales.append(nombre)
            if nombre == "exento":
                impuestos_actuales = ["exento"]
                for k, c in self.chips.items():
                    c.state = "down" if k == "exento" else "normal"
        else:
            if nombre in impuestos_actuales:
                impuestos_actuales.remove(nombre)

        self.ids.inp_impuestos.text = ", ".join(impuestos_actuales)

    def sincronizar_desde_texto(self, texto: str) -> None:
        """
        Sincroniza el texto del input con el estado de los chips.
        """
        lista = [
            p.strip().lower()
            for p in texto.replace(";", ",").replace("|", ",").split(",")
            if p.strip()
        ]
        lista = [p for p in lista if p in IMPUESTOS_VALIDOS]

        if "exento" in lista:
            lista = ["exento"]

        for k, c in self.chips.items():
            c.state = "down" if k in lista else "normal"

    # ----------------------------
    # Lógica de formulario
    # ----------------------------
    def limpiar_formulario(self, campo_precio, campo_impuestos) -> None:
        """
        Limpia los campos del formulario y el historial.
        """
        campo_precio.text = ""
        campo_impuestos.text = ""
        for c in self.chips.values():
            c.state = "normal"

        self.ids.lbl_resultado.text = "Formulario limpio."
        self.ids.lbl_historial.text = ""
        self.historial = []

    def calcular(self, precio_txt: str, impuestos_txt: str) -> None:
        """
        Realiza el cálculo de impuestos y actualiza el historial.
        """
        # Validar precio
        precio_txt = (precio_txt or "").strip()
        if not precio_txt:
            mostrar_popup("Debes ingresar un precio base.")
            return

        try:
            precio = float(precio_txt)
            if precio <= 0:
                mostrar_popup("El precio debe ser mayor que 0.")
                return
        except ValueError:
            mostrar_popup("El precio debe ser numérico.")
            return

        # Procesar impuestos
        impuestos_txt = (impuestos_txt or self.ids.inp_impuestos.text or "").strip()
        try:
            tipos = parsear_tipos(impuestos_txt)
            total = calcular_total(precio, tipos)

            resultado = f"• Precio base: {precio} | Impuestos: {tipos} | Total: {total}"
            self.ids.lbl_resultado.text = "✅ Último cálculo:\n" + resultado

            # Guardar en historial
            self.historial.insert(0, resultado)
            self.ids.lbl_historial.text = "\n".join(self.historial[:10])

        except (ValueError, TypeError) as e:
            mostrar_popup(str(e))
        except Exception as e:
            mostrar_popup(f"Error inesperado: {e}")


# ================================
# Aplicación principal
# ================================
class AppCalculadoraImpuestos(App):
    title = "Calculadora de impuestos"

    def build(self):
        Builder.load_string(KV)
        return VistaCalculadora()


if __name__ == "__main__":
    AppCalculadoraImpuestos().run()

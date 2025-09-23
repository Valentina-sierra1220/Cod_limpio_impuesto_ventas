# Calculadora de Impuestos de Venta (Clean Code + TDD)

# Integrantes
- Edwin Sanabria salaxar
- Valentina Sierra Ospina


## 📂 Estructura del proyecto

<img width="225" height="238" alt="image" src="https://github.com/user-attachments/assets/40c1a81e-8504-4ddc-9dec-370d6be4d7b0" />


## 🏗️ Arquitectura MVC

Modelo (impuestos_model.py) → Contiene la lógica de negocio (cálculo de impuestos, validaciones).

Controlador (impuestos_controller.py) → Recibe datos de la vista, los interpreta y comunica con el modelo.

Vista consola (view/impuestos_view.py) → Interfaz de texto (CLI).

Vista gráfica (view/gui/hello.py) → Interfaz con botones usando Kivy (GUI).


## ⚙️ Requisitos

**Python:** versión recomendada 3.10 – 3.12
Verificar instalación:

python --version
# o en Windows:
py --version


**pip** actualizado:

python -m pip install --upgrade pip


**Dependencias:**

Kivy
 (para la interfaz gráfica).

unittest ya viene con Python (para pruebas).



## 📦 Instalación de dependencias

Se recomienda usar un entorno virtual.

## 1. Crear y activar entorno virtual

**Windows (PowerShell):**

py -m venv .venv
.venv\Scripts\Activate.ps1


**macOS / Linux (bash/zsh):**

python3 -m venv .venv
source .venv/bin/activate


## 2. Instalar Kivy
pip install "kivy[base]"


Verificar instalación:

python -c "import kivy; print(kivy.__version__)"


## ▶️ Cómo ejecutar la aplicación
**Opción A — Consola (CLI)**

Ejecutar desde la raíz del proyecto:

py view/consola/impuestos_view.py



Ejemplo de uso:

💲 Precio base (o 'q' para salir): 10000
🧾 Ingrese impuesto(s): iva19
✅ Total calculado:
   • Precio base: 10000
   • Impuesto(s): iva19
   • Total a pagar: 11900

**Opción B — Interfaz gráfica (GUI con Kivy)**

Ejecutar desde la raíz del proyecto:

**Windows:**

**Activa tu entorno virtual**
py -m venv .venv

Actívalo (en PowerShell):
.\.venv\Scripts\activate
luego:
pip install kivy[base] kivy_examples
y por ultimo:

python view/gui/interfaz.py


**macOS / Linux:**

python3 view/gui/interfaz.py


Se abrirá una ventana gráfica donde podrás:

Ingresar un precio base

Seleccionar impuestos con chips (botones)

Calcular el total o limpiar el formulario


## 🧪 Cómo ejecutar las pruebas unitarias

Ejecutar en la terminal:

py -m unittest tests/test_impuestos.py -v



Las pruebas cubren:

**4 casos normales** (uso frecuente).

**3 casos extraordinarios** (combinaciones de impuestos).

**4 casos de error** (precio negativo, impuesto desconocido, entrada no numérica, vacío).


## 📜 Reglas de negocio

**Impuestos porcentuales sobre el precio base:**

iva19 → 19%

iva5 → 5%

inc8 → 8%

licor25 → 25%

exento → 0%

**Impuesto fijo:**

bolsa → +50 COP al total

exento **no puede combinarse** con otros impuestos.


## ✅ Decisiones de diseño

Constantes descriptivas (IMPUESTO_POR_BOLSA_PLASTICA_COP, TAX_RATES).

Eliminación de números mágicos en el código y en los tests.

Helper en pruebas (assertCalculoImpuesto) para evitar duplicación de lógica.

Métodos con nombres explícitos (_validar_entradas, _aplicar_un_impuesto).

Arquitectura MVC simplificada (modelo, vista, controlador en archivos separados).

Código validado con pylint / flake8 para cumplir PEP8.


## 🔄 Revisiones y calidad

✔️ Primera revisión: mensajes más claros y eliminación de números mágicos.

✔️ Segunda revisión: separación en MVC y ampliación del README.

✔️ Issue de dependencias corregido: ahora README incluye instrucciones de instalación.

✔️ Issue de nomenclatura corregido: nombres más descriptivos para constantes y métodos.

✔️ Issue de duplicación corregido: uso de helper en tests.

# Calculadora de Impuestos de Venta (Clean Code + TDD)

# Integrantes
- Edwin Sanabria salaxar
- Valentina Sierra Ospina


## 📂 Estructura del proyecto

```
Cod_limpio_impuesto_ventas/
├─ impuestos_model.py        # Modelo (lógica de negocio)
├─ impuestos_controller.py   # Controlador (orquesta la lógica)
├─ impuestos_view.py         # Vista (interfaz de usuario por consola)
├─ test_impuestos.py         # Pruebas unitarias (11 casos)
└─ README.md                 # Documentación
```

### Arquitectura MVC
- **Modelo** (`impuestos_model.py`) → Contiene la clase `CalculadoraImpuestos` con la lógica de negocio y validaciones.  
- **Controlador** (`impuestos_controller.py`) → Recibe datos de la vista, los interpreta y comunica con el modelo.  
- **Vista** (`impuestos_view.py`) → Interfaz por consola para el usuario.  

---
## ▶️ Cómo ejecutar la interfaz gráfica con Kivy
⚙️ Requisitos

Python: versión recomendada 3.10 – 3.12
Verifica con:

python --version


Kivy: versión 2.3.0 o superior
Instalación:

pip install "kivy[base]"
(se recomienda usar un entorno virtual venv para aislar dependencias)

1.Abre una terminal en la carpeta raíz del proyecto (donde está README.md).

2.Activa tu entorno virtual si lo creaste (.venv).

3.Ejecuta el archivo de la GUI



Para Windows (PowerShell o CMD):
py view/gui/hello.py


Para macOS / Linux (bash/zsh):
python3 view/gui/hello.py

## ▶️ Cómo ejecutar la aplicación 

1. Abrir la terminal en la carpeta del proyecto.  
2. Ejecutar:

```bash
python view/impuestos_view.py
```

Ejemplo de uso:

```
💲 Precio base (o 'q' para salir): 10000
🧾 Ingrese impuesto(s): iva19
✅ Total calculado:
   • Precio base: 10000
   • Impuesto(s): iva19
   • Total a pagar: 11900
```

---

## 🧪 Cómo ejecutar las pruebas unitarias

Las pruebas unitarias están en `test_impuestos.py`.  

Ejecutar en terminal:

```bash
python -m unittest test_impuestos.py -v
```

Las pruebas cubren:
- **4 casos normales** (uso frecuente).  
- **3 casos extraordinarios** (tasas menos comunes, combinación de impuestos).  
- **4 casos de error** (entradas inválidas: precio negativo, impuesto vacío, desconocido, precio no numérico).  

---

## 📜 Reglas de negocio

- Impuestos porcentuales calculados sobre el **precio base**:  
  - `iva19` → 19%  
  - `iva5` → 5%  
  - `inc8` → 8%  
  - `licor25` → 25%  
  - `exento` → 0%  
- `bolsa` suma un valor fijo de **50 COP** al total.  
- Se permite calcular con **un impuesto o varios impuestos combinados**.  

---

## ✅ Decisiones de diseño 

- **Constantes descriptivas**: `IMPUESTO_BOLSA_FIJO_COP`, `TASAS_PORCENTAJE`.  
- **Sin números mágicos** en las pruebas: se usan constantes y cálculos claros.  
- **Helper en pruebas** (`setUp`) para evitar repetir lógica.  
- **Métodos con nombres explícitos**: `_validar_entradas`, `_sumar_impuesto_al_total`.  
- **Arquitectura MVC simplificada**: modelo, vista y controlador separados en archivos.  

---

## 🔄 Revisiones y Calidad

- **Primera revisión atendida**:  
  - Mensajes de salida en consola más claros.  
  - Constantes renombradas con significado.  
  - Eliminación de números mágicos en pruebas.  

- **Segunda revisión atendida**:  
  - Separación en Modelo, Vista y Controlador (MVC simplificado).  
  - README ampliado con instrucciones de ejecución de pruebas y aplicación.  

- **Revisión con herramienta automatizada**:  
  - El código fue validado con `pylint` / `flake8` para cumplir convenciones de estilo PEP8.  
  - Ejemplo de comando usado:  
    ```bash
    pylint impuestos_model.py
    ```  

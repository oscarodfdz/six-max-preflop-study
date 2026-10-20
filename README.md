# ♠️ Six-Max Poker Tournament (No-Ante) — Estudio Pre-Flop Interactivo (GTO)

Aplicación web interactiva y guía en PDF con el estudio completo de rangos pre-flop para torneos **Six-Max (6 jugadores) sin ante**, basada en aproximaciones **GTO (Chip-EV)** y equilibrio de **Nash**.

---

## 🚀 Vista Rápida del Proyecto

* **`index.html`** — Aplicación web interactiva estilo *Solver* (lista para abrir en cualquier navegador o publicar gratuitamente en **GitHub Pages**).
* **`docs/Six-Max_Torneo_Estudio_PreFlop.pdf`** — Documento vectorial de 4 páginas en alta resolución (A4 horizontal) listo para imprimir o consultar en segunda pantalla.
* **`src/`** — Scripts en Python puro (sin dependencias externas) que construyen tanto el aplicativo HTML como el PDF vectorial a partir de los rangos definidos en `src/ranges_data.py`.

---

## 📊 Módulos Incluidos

1. **Rangos de Apertura (RFI ~100 bb):**
   * Matrices 13×13 para **UTG (LJ)**, **HJ**, **CO**, **BTN** y **SB vs BB**.
   * Diferenciación entre aperturas puras (`100%`), manos mixtas (`~50%`) y frecuencias de *limp* en SB.
   * Modo comparativo para visualizar las 5 posiciones simultáneamente e inspector de combos por mano.
2. **Defensa de Big Blind (vs Open Raise de 2.5 bb / 3.0 bb):**
   * Rangos de **3-Bet por Valor**, **3-Bet Bluff / Polarizado**, **Call** y **Fold** frente a UTG, HJ, CO, BTN y SB.
   * Calibrados para las *Pot Odds* reales de un torneo sin ante ($27.3\%$ de equity necesaria ante $2.5\text{ bb}$).
3. **3-Bet (IP y SB) y Defensa frente a 3-Bet:**
   * Rangos en posición (`BTN vs CO`, `CO vs UTG/HJ`).
   * Estrategia lineal *3-Bet o Fold* desde la Ciega Pequeña (`SB vs BTN`, `SB vs UTG/HJ`).
   * Defensa del abridor ante un 3-bet (**4-Bet Valor**, **4-Bet Bluff** y **Call**).
4. **Simulador Push / Fold Nash (`< 20 bb` Sin Ante):**
   * Cada celda muestra el **stack máximo en BB** con el que esa mano es *All-In* directo rentable (más tabla de *Call* en BB contra *Push* de SB).
   * Incluye un **deslizador interactivo (4 bb – 20 bb)** que ilumina en tiempo real el rango exacto para tu pila de fichas.
5. **Guía Estratégica, Matemáticas e ICM:**
   * Comparativa matemática *Sin Ante vs Con Ante*, ajustes por profundidad de stack y *Bubble Factor* (ICM).

---

## 🛠️ Estructura del Repositorio

```text
six-max-preflop-study/
├── index.html                                # Web App interactiva (GitHub Pages entry point)
├── docs/
│   └── Six-Max_Torneo_Estudio_PreFlop.pdf    # Guía completa en PDF vectorial (4 páginas)
├── src/
│   ├── ranges_data.py                        # Definición de todos los rangos y matrices Nash
│   ├── build_html.py                         # Generador de index.html
│   └── build_pdf.py                          # Motor generador del PDF vectorial (Python puro)
├── .env.example                              # Plantilla de variables de entorno (sin claves reales)
├── .gitignore                                # Protección de archivos .env y claves API
└── README.md
```

---

## ⚙️ Cómo Reconstruir los Archivos (`Build`)

No necesitas instalar librerías externas; el proyecto utiliza únicamente la librería estándar de **Python 3**:

```bash
# 1. Regenerar la aplicación interactiva (index.html)
python3 src/build_html.py

# 2. Regenerar el documento PDF vectorial (docs/Six-Max_Torneo_Estudio_PreFlop.pdf)
python3 src/build_pdf.py
```

a `main` y carpeta `/ (root)` y pulsa **Save**.
3. Tu aplicación interactiva quedará publicada en `https://TU_USUARIO.github.io/six-max-preflop-study/`.

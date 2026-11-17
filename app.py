"""Detector de EPP (casco) para obras.

App web hecha con Gradio: el encargado de Seguridad e Higiene sube una foto
y recibe la foto marcada (verde: con casco, rojo: sin casco) y un resumen
con el porcentaje de cumplimiento.

Ejecución:
    python app.py
"""

import os

# Avast agrega esta variable y rompe las conexiones seguras de Python (PLAN.md, problema 2)
os.environ.pop("SSLKEYLOGFILE", None)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import gradio as gr
from huggingface_hub import hf_hub_download
from PIL import Image, ImageDraw, ImageFont, ImageOps
from ultralytics import YOLO


# ---------------------------------------------------------------------------
# 1. Configuración
# ---------------------------------------------------------------------------

REPO_MODELO = "keremberke/yolov8n-hard-hat-detection"

# Traducimos las clases del modelo (definidas por quienes etiquetaron el dataset)
NOMBRES = {"Hardhat": "Con casco", "NO-Hardhat": "Sin casco"}
COLORES = {"Hardhat": (0, 170, 0), "NO-Hardhat": (220, 0, 0)}  # verde y rojo (RGB)

CONF_INICIAL = 0.25    # umbral de confianza (ver playground, Paso 4)
IMGSZ_INICIAL = 1280   # tamaño de análisis (ver playground, Paso 6)
ANCHO_MAXIMO = 1600    # achicamos la foto marcada para que cargue rápido en el navegador


# ---------------------------------------------------------------------------
# 2. Cargar el modelo (una sola vez, al iniciar la app)
# ---------------------------------------------------------------------------

modelo = YOLO(hf_hub_download(repo_id=REPO_MODELO, filename="best.pt"))


# ---------------------------------------------------------------------------
# 3. Lógica propia: de la salida del modelo a información útil
# ---------------------------------------------------------------------------

def leer_detecciones(resultado):
    """Pasa la respuesta de YOLO a una lista simple de diccionarios."""
    detecciones = []
    for caja in resultado.boxes:
        detecciones.append({
            "clase": modelo.names[int(caja.cls)],         # "Hardhat" o "NO-Hardhat"
            "confianza": float(caja.conf),                 # entre 0 y 1
            "caja": caja.xyxy[0].int().tolist(),           # [x1, y1, x2, y2] en píxeles
        })
    return detecciones


def contar(detecciones):
    """Cuenta cabezas con y sin casco y calcula el % de cumplimiento."""
    con_casco = sum(1 for d in detecciones if d["clase"] == "Hardhat")
    sin_casco = sum(1 for d in detecciones if d["clase"] == "NO-Hardhat")
    cabezas = con_casco + sin_casco

    # Si no hay cabezas, el porcentaje no tiene sentido: lo dejamos en None
    cumplimiento = con_casco / cabezas * 100 if cabezas > 0 else None

    return {
        "cabezas": cabezas,
        "con_casco": con_casco,
        "sin_casco": sin_casco,
        "cumplimiento": cumplimiento,
    }


# ---------------------------------------------------------------------------
# 4. Presentación: dibujar las cajas y escribir el resumen
# ---------------------------------------------------------------------------

def dibujar(foto, detecciones):
    """Dibuja una caja de color por cada cabeza detectada."""
    marcada = foto.copy()
    lapiz = ImageDraw.Draw(marcada)

    # El grosor y la letra dependen del tamaño de la foto, para que se vean en cualquier foto
    grosor = max(3, marcada.width // 300)
    letra = ImageFont.load_default(size=max(16, marcada.width // 60))

    for d in detecciones:
        color = COLORES[d["clase"]]
        x1, y1, x2, y2 = d["caja"]
        texto = f'{NOMBRES[d["clase"]]} {d["confianza"]:.0%}'

        lapiz.rectangle([x1, y1, x2, y2], outline=color, width=grosor)
        # Etiqueta con fondo de color, arriba de la caja
        izq, arriba, der, abajo = lapiz.textbbox((x1, y1), texto, font=letra, anchor="lb")
        lapiz.rectangle([izq, arriba - grosor, der + grosor * 2, abajo], fill=color)
        lapiz.text((x1 + grosor, y1), texto, fill="white", font=letra, anchor="lb")

    marcada.thumbnail((ANCHO_MAXIMO, ANCHO_MAXIMO))
    return marcada


def escribir_resumen(conteo):
    """Arma el resumen en Markdown para mostrarlo en la app."""
    if conteo["cabezas"] == 0:
        return "### No se detectaron cabezas\n\nProbá bajar el umbral de confianza o subir otra foto."

    resumen = (
        f"### Cumplimiento: {conteo['cumplimiento']:.0f} %\n\n"
        f"| Cabezas detectadas | Con casco | Sin casco |\n"
        f"|:---:|:---:|:---:|\n"
        f"| {conteo['cabezas']} | {conteo['con_casco']} | {conteo['sin_casco']} |\n\n"
    )
    if conteo["sin_casco"] > 0:
        resumen += f"⚠️ **Hay {conteo['sin_casco']} persona(s) sin casco.** Están marcadas en rojo.\n\n"

    resumen += (
        "> El modelo cuenta **cabezas**, no personas, y puede equivocarse: "
        "confunde pañuelos o cabezas descubiertas con cascos y no ve cabezas tapadas o lejanas. "
        "Revisá la foto antes de tomar decisiones."
    )
    return resumen


# ---------------------------------------------------------------------------
# 5. Función principal: la que llama Gradio cada vez que se analiza una foto
# ---------------------------------------------------------------------------

def analizar(foto, conf, imgsz):
    if foto is None:
        return None, "Subí una foto para empezar."

    # Las fotos de celular guardan la rotación aparte (EXIF): la aplicamos
    foto = ImageOps.exif_transpose(foto).convert("RGB")

    resultado = modelo.predict(foto, conf=conf, imgsz=int(imgsz), verbose=False)[0]
    detecciones = leer_detecciones(resultado)

    return dibujar(foto, detecciones), escribir_resumen(contar(detecciones))


# ---------------------------------------------------------------------------
# 6. Interfaz
# ---------------------------------------------------------------------------

with gr.Blocks(title="Detector de EPP") as app:
    gr.Markdown(
        "# Detector de EPP · Casco\n"
        "Subí una foto de la obra y la app marca las cabezas **con casco (verde)** "
        "y **sin casco (rojo)**, y calcula el porcentaje de cumplimiento."
    )

    with gr.Row():
        with gr.Column():
            entrada = gr.Image(type="pil", label="Foto de la obra")
            conf = gr.Slider(0.05, 0.95, value=CONF_INICIAL, step=0.05,
                             label="Umbral de confianza",
                             info="Más bajo: encuentra más cabezas, pero con más errores.")
            imgsz = gr.Radio([640, 1280], value=IMGSZ_INICIAL,
                             label="Tamaño de análisis (píxeles)",
                             info="1280 ayuda con personas lejanas, pero es más lento.")
            boton = gr.Button("Analizar", variant="primary")

        with gr.Column():
            salida_foto = gr.Image(type="pil", label="Resultado")
            salida_resumen = gr.Markdown()

    gr.Examples(
        examples=[["pruebas/foto1.jpg"], ["pruebas/foto2.jpg"]],
        inputs=[entrada],
        label="Fotos de ejemplo",
    )

    boton.click(analizar, inputs=[entrada, conf, imgsz], outputs=[salida_foto, salida_resumen])


if __name__ == "__main__":
    app.launch()

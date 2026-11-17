"""Convierte el modelo YOLO (best.pt) a ONNX para ejecutarlo en el navegador.

El archivo resultante (web/modelo.onnx) lo usa la versión web de la app (web/index.html).

Ejecución:
    python exportar_onnx.py
"""

import os
import shutil

os.environ.pop("SSLKEYLOGFILE", None)  # PLAN.md, problema 2

from huggingface_hub import hf_hub_download
from ultralytics import YOLO

modelo = YOLO(hf_hub_download("keremberke/yolov8n-hard-hat-detection", "best.pt"))

# dynamic=True: el modelo acepta distintos tamaños de entrada (640 o 1280)
ruta = modelo.export(format="onnx", dynamic=True, simplify=True, opset=17)

shutil.copy(ruta, "web/modelo.onnx")
print("Clases:", modelo.names)
print("Modelo guardado en web/modelo.onnx")

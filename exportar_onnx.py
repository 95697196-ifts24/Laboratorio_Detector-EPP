"""Convierte los dos modelos YOLO a ONNX para ejecutarlos en el navegador (web/index.html).

- Rápido  (YOLOv8n, 6 MB)  -> web/modelo.onnx          (13 MB)
- Preciso (YOLO11x, 114 MB) -> web/modelo_preciso.onnx  (58 MB, comprimido a int8)

El modelo Preciso en ONNX pesa 228 MB, demasiado para una página web. La cuantización
int8 guarda cada peso en 1 byte en lugar de 4: el archivo queda 4 veces más chico y
pierde un poco de precisión (error total 15 en lugar de 11 en las 17 fotos de prueba).

Ejecución:
    python exportar_onnx.py
"""

import os
import shutil

os.environ.pop("SSLKEYLOGFILE", None)  # PLAN.md, problema 2

from huggingface_hub import hf_hub_download
from onnxruntime.quantization import QuantType, quantize_dynamic
from ultralytics import YOLO


def exportar(repo, archivo):
    """Descarga el modelo y lo exporta a ONNX. Devuelve la ruta del .onnx."""
    modelo = YOLO(hf_hub_download(repo, archivo))
    print("Clases:", modelo.names)
    # dynamic=True: el modelo acepta distintos tamaños de entrada (640 o 1280)
    return modelo.export(format="onnx", dynamic=True, simplify=True, opset=17)


# Modelo Rápido: se copia tal cual
shutil.copy(exportar("keremberke/yolov8n-hard-hat-detection", "best.pt"), "web/modelo.onnx")

# Modelo Preciso: se comprime a int8
ruta = exportar("luisarizmendi/hardhat-or-hat", "v1/model/pytorch/best.pt")
quantize_dynamic(ruta, "web/modelo_preciso.onnx", weight_type=QuantType.QUInt8)

for f in ("web/modelo.onnx", "web/modelo_preciso.onnx"):
    print(f, round(os.path.getsize(f) / 1e6), "MB")

---
title: Detector de EPP (casco)
emoji: 👷
colorFrom: yellow
colorTo: green
sdk: static
app_file: index.html
pinned: false
license: agpl-3.0
short_description: Detecta cascos en fotos de obras y calcula el cumplimiento
---

# Detector de EPP · Casco

Subí una foto de una obra en construcción y la app marca las cabezas **con casco (verde)** y **sin casco (rojo)** y calcula el porcentaje de cumplimiento.

El modelo se ejecuta **en tu navegador** con [ONNX Runtime Web](https://onnxruntime.ai/): la foto no se envía a ningún servidor.

**Autor:** José J. Navas A. · Laboratorio Práctico Obligatorio · Técnicas de Procesamiento Digital de Imágenes · IFTS N.º 24 · 2026

- **Modelo Preciso** (por defecto): [luisarizmendi/hardhat-or-hat](https://huggingface.co/luisarizmendi/hardhat-or-hat) (YOLO11x), convertido a ONNX y comprimido a int8 (58 MB)
- **Modelo Rápido:** [keremberke/yolov8n-hard-hat-detection](https://huggingface.co/keremberke/yolov8n-hard-hat-detection) (YOLOv8 nano), convertido a ONNX (13 MB)
- **Código, pruebas y documentación:** [github.com/95697196-ifts24/Laboratorio_Detector-EPP](https://github.com/95697196-ifts24/Laboratorio_Detector-EPP)

> **Atención:** el modelo puede equivocarse, sobre todo con cascos tapados en multitudes o personas agachadas. Revisá la foto marcada: si una caja está mal, tocala para corregirla y el cumplimiento se recalcula.

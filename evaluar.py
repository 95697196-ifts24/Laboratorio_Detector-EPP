"""Analiza todas las fotos de la carpeta pruebas/ de una sola vez (fase 6).

Para cada foto guarda la imagen marcada en pruebas/resultados/ e imprime una
tabla en Markdown, lista para pegar en pruebas/fuentes.md.

Ejecución:
    python evaluar.py                         (modo combinado)
    python evaluar.py --modo 640 --conf 0.25
"""

import argparse
from pathlib import Path

from PIL import Image, ImageOps

# Reutilizamos la lógica de la app (importar app.py no abre la interfaz)
from app import CONF_INICIAL, MODO_INICIAL, MODOS, contar, detectar, dibujar

CARPETA = Path("pruebas")
SALIDA = CARPETA / "resultados"
EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp"}


def main():
    parser = argparse.ArgumentParser(description="Analiza las fotos de prueba")
    parser.add_argument("--conf", type=float, default=CONF_INICIAL)
    parser.add_argument("--modo", choices=MODOS, default=MODO_INICIAL)
    args = parser.parse_args()

    SALIDA.mkdir(exist_ok=True)
    sufijo = f"imgsz{args.modo}" if args.modo.isdigit() else "combinado"
    fotos = sorted(f for f in CARPETA.iterdir() if f.suffix.lower() in EXTENSIONES)

    print(f"conf={args.conf} · modo={args.modo} · {len(fotos)} fotos\n")
    print("| Archivo | Cabezas | Con casco | Sin casco | Cumplimiento | Confianzas |")
    print("|---|:---:|:---:|:---:|:---:|---|")

    for ruta in fotos:
        foto = ImageOps.exif_transpose(Image.open(ruta)).convert("RGB")
        detecciones = detectar(foto, args.conf, args.modo)
        conteo = contar(detecciones)

        dibujar(foto, detecciones).save(SALIDA / f"{ruta.stem}_{sufijo}.jpg")

        cumplimiento = "—" if conteo["cumplimiento"] is None else f"{conteo['cumplimiento']:.0f} %"
        confianzas = ", ".join(f"{d['confianza']:.0%}" for d in detecciones)
        print(f"| {ruta.name} | {conteo['cabezas']} | {conteo['con_casco']} | "
              f"{conteo['sin_casco']} | {cumplimiento} | {confianzas} |")

    print(f"\nImágenes marcadas en: {SALIDA}/")


if __name__ == "__main__":
    main()

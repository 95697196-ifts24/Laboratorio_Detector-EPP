r"""Publica la versión web de la app en Hugging Face Spaces (Space estático, gratuito).

Hugging Face cobra los Spaces con Gradio (PRO), pero los estáticos son gratis.
Por eso se publica web/index.html, que ejecuta el modelo en el navegador.

Pasos previos:
    python exportar_onnx.py              # genera web/modelo.onnx
    .venv\Scripts\hf auth login          # una sola vez, con un token de escritura

Ejecución:
    python publicar_space.py
"""

import os

os.environ.pop("SSLKEYLOGFILE", None)  # PLAN.md, problema 2

from huggingface_hub import HfApi, whoami

NOMBRE_SPACE = "detector-epp"


def main():
    usuario = whoami()["name"]
    repo_id = f"{usuario}/{NOMBRE_SPACE}"
    api = HfApi()

    api.create_repo(repo_id, repo_type="space", space_sdk="static", exist_ok=True)

    # La página, el modelo y las fotos de ejemplo (todo lo que hay en web/)
    api.upload_folder(folder_path="web", repo_id=repo_id, repo_type="space",
                      commit_message="Publicar la app web")
    # La ficha del Space (incluye la configuración en el encabezado)
    api.upload_file(path_or_fileobj="hf_space/README.md", path_in_repo="README.md",
                    repo_id=repo_id, repo_type="space", commit_message="Ficha del Space")

    print(f"\nListo: https://huggingface.co/spaces/{repo_id}")


if __name__ == "__main__":
    main()

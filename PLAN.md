# Plan del proyecto: Detector de EPP para obras

Laboratorio Práctico Obligatorio · Procesamiento Digital de Imágenes · IFTS N.º 24
Autor: José J. Navas A.
Fecha de planificación: 17/11/2026

> Este plan se definió con un agente que actuó como mentor de desarrollo de productos digitales. El agente hizo una pregunta por vez y no escribió código durante la planificación.

---

## 1. Qué queremos lograr

| Aspecto | Decisión |
|---|---|
| **Usuario** | El encargado de Seguridad e Higiene de una constructora |
| **Problema** | Tiene que verificar que el personal use casco en varias obras. Hoy lo hace mirando en persona o revisando fotos a ojo: es lento, depende de que esté presente y no deja un registro ordenado |
| **Entrada** | Fotos que el encargado saca con el celular durante la recorrida y después sube a la app |
| **Salida** | 1. La foto con recuadros de colores (verde: con casco, rojo: sin casco). 2. Un resumen: **cabezas** detectadas, con casco, sin casco y % de cumplimiento (ver hallazgo 1 de la sección 3 bis) |

## 2. Qué necesito aprender

| Tema | Estado inicial | Qué voy a aprender |
|---|---|---|
| VS Code + Python | Listo | Verificar la extensión Jupyter |
| uv | No instalado | Instalarlo y crear un entorno virtual |
| Hugging Face / GitHub | Cuentas creadas | Leer una Model Card y publicar el proyecto |
| Lectura de código | Nivel 2 de 5 | Trabajar en bloques chicos (5 a 15 líneas), comprendiendo cada uno antes de ejecutarlo |

## 3. Qué tecnología usar y por qué

**Elegida:** un modelo **YOLO** especializado en cascos (librería Ultralytics, modelo publicado en Hugging Face), con interfaz en **Gradio** y entorno **uv** con **Python 3.12**.

| Alternativa | Por qué no se eligió para el MVP |
|---|---|
| Detección zero-shot (OWL-ViT / OWLv2) | Más flexible, pero más lenta y menos precisa por ser genérica. Queda como experimento comparativo |
| MediaPipe Object Detector | No tiene la clase "casco": habría que reentrenarlo |

**Criterio de elección:** priorizar confiabilidad, velocidad en CPU y simpleza, que es lo que necesita el usuario.

**Tarea del modelo:** **detección de objetos**. Para cada objeto encontrado, el modelo devuelve dónde está (una caja), qué es (una clase) y con qué confianza.

## 3 bis. Fase 1 · Auditoría de modelos (17/11/2026)

| | Modelo 1 (principal) | Modelo 2 (comparación) |
|---|---|---|
| Repositorio | [keremberke/yolov8n-hard-hat-detection](https://huggingface.co/keremberke/yolov8n-hard-hat-detection) | [luisarizmendi/hardhat-or-hat](https://huggingface.co/luisarizmendi/hardhat-or-hat) |
| Clases | `Hardhat`, `NO-Hardhat` | `helmet`, `no_helmet`, `hat` |
| Arquitectura | YOLOv8n | YOLO11 (la ficha es inconsistente: "m" o "x") |
| Peso | 6,2 MB | 114 MB |
| Precisión declarada | mAP50 = 0,836 (autodeclarado, validación) | mAP50 = 0,567 (dudoso: igual al mAP50-95) |
| Dataset | `keremberke/hard-hat-detection` (Hugging Face) | Roboflow Universe "hardhat-or-hat" |
| Licencia | No declarada | No declarada |
| Actualización | Hace más de 3 años | Hace 1 mes |
| Riesgo | Hecho con Ultralytics 8.0.23: puede no cargar con la versión actual | Ficha desprolija |

**Hallazgos:**
1. **Ningún modelo detecta "personas": detectan cabezas.** El resumen cuenta cabezas, no personas. Quienes etiquetaron el dataset definieron esa categoría.
2. **El modelo 2 incluye la clase "gorra" (`hat`).** Sugiere que los detectores de cascos confunden gorras con cascos. Se usará para comparar en las pruebas.
3. **Licencias:** ninguna ficha declara licencia y YOLO usa AGPL-3.0. Para ofrecerlo como servicio comercial hay que publicar el código o adquirir una licencia de Ultralytics.

## 3 ter. Hallazgos de las primeras pruebas (17/11/2026)

4. **El tamaño de análisis importa.** YOLO achica la foto a 640 px (el tamaño de entrenamiento). En fotos grandes, los cascos lejanos o tapados quedan en unos 25 px y el modelo no los ve. Con `imgsz=1280` se detectan, pero bajan las confianzas de los cascos grandes. Detalle en `playground.ipynb`, Paso 6.
5. **El modelo casi nunca dice "sin casco".** En la foto 2 marca como "con casco" una cabeza descubierta y un pañuelo blanco, y no asigna `NO-Hardhat` ni con un umbral de 2 %. Consecuencia: **el % de cumplimiento tiende a salir más alto que el real**. Es el límite más importante para el usuario.

## 3 quater. Resultados de la fase 6 (17/11/2026)

Se probaron 17 fotos de Pexels. El detalle está en `pruebas/fuentes.md`.

6. **Conteo exacto en 8 de 17 fotos**, tanto con 640 como con 1280, aunque las fallas son distintas en cada caso.
7. **Gorras confundidas con cascos:** se confirma la sospecha del hallazgo 2. En una multitud, el modelo informa 88 % de cumplimiento cuando el real es menor a 50 %.
8. **Casco en la mano contado como "con casco":** el modelo detecta el objeto, no si la persona lo tiene puesto.
9. **1280 detecta más cabezas sin casco** (4 contra 2). Esto respalda la decisión 9.

## 4. Cómo construir la primera versión mínima (MVP)

| Fase | Qué hacemos | Qué aprendo |
|---|---|---|
| 1. Auditoría previa | Elegir el modelo en Hugging Face y leer su Model Card: clases, datos de entrenamiento, métricas | Quién definió las categorías y con qué datos |
| 2. Entorno | Instalar uv, crear el entorno con Python 3.12 e instalar las librerías | Qué es un entorno virtual |
| 3. Playground | Cuaderno `.ipynb`: cargar el modelo y probarlo con una foto | Qué devuelve un detector |
| 4. Lógica propia | Contar personas con y sin casco y calcular el % de cumplimiento | Transformar la salida del modelo en información útil |
| 5. Interfaz | App en Gradio: subir foto, ver la imagen marcada y el resumen | Conectar un modelo con una interfaz |
| 6. Pruebas y sesgos | Probar con 15 a 20 fotos y registrar aciertos y errores | Límites y sesgos reales |
| 7. Cierre | `app.py`, `README.md` y subida a GitHub (opcional: Hugging Face Spaces) | Reproducibilidad |

## 5. Plan de pruebas

Entre 15 y 20 fotos de **Pexels o Unsplash** (licencia libre), registrando la fuente de cada una en `pruebas/fuentes.md`.

| Caso | Qué queremos descubrir |
|---|---|
| Buena luz, de frente | Caso ideal |
| Contraluz o interior oscuro | Efecto de la iluminación |
| Personas de espaldas o lejos | Objetos chicos o parciales |
| Gorra, capucha o pelo recogido | ¿Confunde una gorra con un casco? |
| Cascos de colores poco comunes | ¿Depende del color? |
| Foto sin personas | Falsos positivos |

**Límite asumido:** no se probó con fotos reales de obras argentinas. Queda como trabajo futuro.

## 6. Para seguir explorando (fuera del MVP)

- Detección de chalecos reflectivos.
- Webcam en vivo y video grabado.
- Registro descargable (CSV) con fecha, obra y resultado, para informes. Es la funcionalidad clave para ofrecerlo como servicio.
- Comparación con la detección zero-shot (OWLv2).
- Fotos propias de obras locales.

## 7. Registro de decisiones

| # | Decisión | Motivo |
|---|---|---|
| 1 | Usuario: encargado de Seguridad e Higiene | Problema concreto y cliente identificable (servicio B2B) |
| 2 | Entrada: fotos subidas | Simple, funciona en cualquier PC, encaja con la recorrida |
| 3 | Salida: imagen marcada + resumen | Muestra dónde está el problema y cuánto incumplimiento hay |
| 4 | Pruebas con fotos de internet | Rapidez para la entrega. Documentado como límite |
| 5 | Tecnología: YOLO especializado | Rápido, preciso y estándar en la industria |
| 6 | Modelo 1 (keremberke, YOLOv8n) como principal | Liviano, mejor precisión declarada, muy usado |
| 7 | Modelo 2 (luisarizmendi, YOLO11) solo para comparar | Su clase "gorra" permite estudiar la confusión gorra/casco |
| 8 | Contar "cabezas" en lugar de "personas" | Es lo que realmente detectan los modelos |
| 9 | La app analiza con `imgsz=1280` por defecto y deja elegir 640 | Detecta personas lejanas (foto 1). El usuario puede volver a 640 si hay muchos falsos positivos |
| 10 | Umbral de confianza ajustable en la app (inicial 0,25) | No hay un valor que funcione bien en todas las fotos |
| 11 | La app muestra un aviso de que el resultado puede fallar | El modelo da falsos "con casco" (hallazgo 5): el encargado debe revisar la foto |
| 12 | Script `evaluar.py` para la fase 6 | Analiza todas las fotos de prueba de una vez y arma la tabla de resultados |
| 13 | Publicar una versión web estática (ONNX en el navegador) en lugar de la app de Gradio | Hugging Face exige PRO para Spaces con Gradio. El Space estático es gratis y, además, las fotos no salen de la computadora del usuario |

## 8. Registro de problemas y soluciones

| # | Problema | Causa | Solución |
|---|---|---|---|
| 1 | Pegar un link en la terminal da `CommandNotFoundException` | Se pegó la URL de la documentación en lugar del comando | Copiar solo el comando. uv ya estaba instalado (0.11.2) |
| 2 | `import gradio` cierra Python con `OPENSSL_Uplink ... no OPENSSL_Applink` | El antivirus Avast inyecta la variable `SSLKEYLOGFILE` para inspeccionar el tráfico HTTPS, y el módulo `ssl` de Python falla al usarla | Borrar la variable antes de importar: `$env:SSLKEYLOGFILE = $null` en la terminal, u `os.environ.pop("SSLKEYLOGFILE", None)` al inicio del código |
| 3 | La foto 1 tiene 4 cascos y el modelo detecta 3 | La foto mide 5754 px y YOLO la achica a 640: el casco del fondo, tapado a medias, queda en unos 24 × 31 px y sale con confianza 8 % | Analizar con `imgsz=1280` (confianza 54 %). Bajar el umbral no sirve: aparecen cajas repetidas |
| 4 | Las celdas agregadas al cuaderno desaparecieron | VS Code tenía el cuaderno abierto y, al guardar, escribió encima su versión vieja | Antes de guardar, recargar el archivo con "File: Revert File" si se modificó desde afuera |
| 5 | Publicar el Space con Gradio da `402 Payment Required` | Hugging Face ahora exige la suscripción PRO para Spaces con Gradio o Docker | Versión web estática: modelo en ONNX ejecutado en el navegador (decisión 13) |
| 6 | `uv pip install` falla con `invalid peer certificate: UnknownIssuer` | Avast intercepta el HTTPS con su propio certificado | Agregar `--system-certs` al comando de uv |
| 7 | La versión web daba cajas de más | Se usó IoU 0,7 para eliminar cajas repetidas (NMS), pero Ultralytics usa 0,5 | Usar `IOU_NMS = 0.5`, verificado comparando contra Ultralytics |

**Entorno verificado:** Python 3.12.13 · ultralytics 8.4.215 · torch 2.15.0+cpu · gradio 6.32.0 · huggingface_hub 2.4.0 · opencv 5.1.0.

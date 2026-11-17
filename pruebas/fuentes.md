# Fuentes de las fotos de prueba

Todas las fotos provienen de bancos con licencia libre (Pexels o Unsplash).

**Cómo completar esta tabla:**
1. Guardá la foto en `pruebas/` y anotá el link de origen.
2. Contá a ojo cuántos cascos y cuántas cabezas sin casco hay (columna "Realidad").
3. Ejecutá `python evaluar.py` (y también `python evaluar.py --imgsz 640` para comparar).
4. Copiá lo que detectó el modelo y mirá las imágenes marcadas en `pruebas/resultados/`.

Configuración: `conf=0.25`. "C" = con casco, "S" = sin casco.

| Archivo | Link de origen | Caso que prueba | Realidad | Modelo (`imgsz=640`) | Modelo (`imgsz=1280`) | Resultado observado |
|---|---|---|---|---|---|---|
| foto1.jpg | https://images.pexels.com/photos/35340756/pexels-photo-35340756.jpeg | Buena luz, de frente (caso ideal) | 4 C · 0 S | 3 C · 0 S | 4 C · 0 S | Con 640 se pierde el casco del obrero del fondo, que está tapado a medias (confianza 8 %). Con 1280 aparece (54 %), pero bajan las confianzas de los demás |
| foto2.jpg | https://www.pexels.com/es-es/foto/grupo-de-trabajadores-de-la-construccion-con-uniformes-azules-33150526/ | Grupo, cascos blancos, cabezas descubiertas y pañuelo | 5 C · 2 S | 7 C · 0 S | 7 C · 0 S | **2 falsos positivos:** una cabeza descubierta (con anteojos oscuros) y un pañuelo blanco se marcan como "con casco". El modelo nunca usa la clase "sin casco": el cumplimiento da 100 % cuando el real es 71 % |

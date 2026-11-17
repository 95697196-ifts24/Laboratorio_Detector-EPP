# Fuentes y resultados de las fotos de prueba

Todas las fotos provienen de [Pexels](https://www.pexels.com/), con licencia libre. Las imágenes marcadas por el modelo están en `pruebas/resultados/`.

**Cómo agregar una foto:**
1. Guardá la foto en `pruebas/` y anotá el link de origen.
2. Contá a ojo cuántas cabezas tienen casco y cuántas no (columna "Realidad").
3. Ejecutá `python evaluar.py --imgsz 640` y `python evaluar.py --imgsz 1280`.
4. Anotá lo que detectó el modelo y revisá las imágenes marcadas.

Configuración: `conf=0.25`. **C** = con casco, **S** = sin casco. ✅ = conteo exacto.

## Resultados por foto

| # | Archivo | Link de origen | Caso que prueba | Realidad | Modelo 640 | Modelo 1280 | Resultado observado |
|---|---|---|---|---|---|---|---|
| 1 | foto1.jpg | [35340756](https://www.pexels.com/photo/35340756/) | Grupo de frente, buena luz | 4 C | 3 C | 4 C ✅ | Con 640 se pierde el casco del fondo, tapado a medias |
| 2 | foto2.jpg | [33150526](https://www.pexels.com/photo/33150526/) | Grupo, cabeza descubierta y pañuelo blanco | 5 C · 2 S | 7 C | 7 C | La cabeza descubierta y el pañuelo se marcan como "con casco" |
| 3 | pexels-akoonie-32751451.jpg | [32751451](https://www.pexels.com/photo/32751451/) | Una persona agachada, casco naranja | 1 C | 1 C ✅ | 0 | Con 1280 no lo detecta: el casco ocupa gran parte de la foto |
| 4 | pexels-cmrcn-29988954.jpg | [29988954](https://www.pexels.com/photo/29988954/) | De espaldas, interior a contraluz | 1 C | 1 C ✅ | 1 C ✅ | Correcto aun de espaldas |
| 5 | pexels-cristian-rojas-8853472.jpg | [8853472](https://www.pexels.com/photo/8853472/) | Una persona de perfil, casco amarillo | 1 C | 1 C ✅ | 1 C ✅ | Correcto (55 % con 640 y 87 % con 1280) |
| 6 | pexels-dongfang-xiaowu-112541598-33982049.jpg | [33982049](https://www.pexels.com/photo/33982049/) | Una persona con casco y otra con el casco **en la mano** | 1 C · 1 S | 3 C | 2 C · 1 S | Con 640 cuenta el casco en la mano como dos "con casco" y no ve la cabeza descubierta. Con 1280 detecta bien la cabeza descubierta, pero marca un cartel de comida como casco |
| 7 | pexels-doruk-aksel-anil-477355556-15823388.jpg | [15823388](https://www.pexels.com/photo/15823388/) | Cascos rojos de rescate, uno tapado y otro lejos | 4 C | 2 C | 3 C | Con 1280 detecta el casco lejano. Ninguno ve el casco tapado |
| 8 | pexels-erik-debarre-2151386688-31884247.jpg | [31884247](https://www.pexels.com/photo/31884247/) | Visto desde arriba, cabeza inclinada | 1 C | 0 | 0 | No lo detecta: ángulo poco común |
| 9 | pexels-hanna-alves-1907982668-28812390.jpg | [28812390](https://www.pexels.com/photo/28812390/) | Casco con protectores auditivos, interior | 1 C | 1 C ✅ | 2 C | Con 1280 dibuja dos cajas sobre el mismo casco |
| 10 | pexels-imamuddin-mohammad-1225850-16687899.jpg | [16687899](https://www.pexels.com/photo/16687899/) | Multitud, cascos superpuestos | ≈ 8 C | 5 C | 4 C | Pierde cascos tapados. Con 1280 no ve el casco amarillo de primer plano |
| 11 | pexels-jerome031-5298215.jpg | [5298215](https://www.pexels.com/photo/5298215/) | Cuatro personas, una agachada y otra tapada | 4 C | 3 C | 2 C | Pierde el casco tapado; con 1280 también el de la persona agachada |
| 12 | pexels-kalz-michael-1277172-38284505.jpg | [38284505](https://www.pexels.com/photo/38284505/) | Obrero y un peatón sin casco al fondo | 1 C · 1 S | 1 C | 1 C · 1 S ✅ | Con 1280 detecta al peatón lejano sin casco |
| 13 | pexels-karanwang-11790051.jpg | [11790051](https://www.pexels.com/photo/11790051/) | Tres personas a contraluz, cascos rojo y amarillos | 3 C | 3 C ✅ | 3 C ✅ | Correcto: el contraluz y el color no afectan |
| 14 | pexels-madknoxxdeluxe-36096170.jpg | [36096170](https://www.pexels.com/photo/36096170/) | Persona lejana en una ventana | 1 C | 1 C ✅ | 1 C ✅ | Correcto (50 % con 640 y 83 % con 1280) |
| 15 | pexels-ozkanoztas-38043248.jpg | [38043248](https://www.pexels.com/photo/38043248/) | Multitud con cascos, **gorras** y cabezas descubiertas | ≈ 9 C · 10 o más S | 14 C · 2 S | 12 C · 2 S | Marca gorras y cabezas descubiertas como "con casco". Cumplimiento: 88 % según el modelo y menos de 50 % en la realidad |
| 16 | pexels-safari-consoler-3290243-11293619.jpg | [11293619](https://www.pexels.com/photo/11293619/) | Blanco y negro, persona agachada | 1 C | 1 C ✅ | 1 C ✅ | Correcto sin color |
| 17 | pexels-wal_-172619-2156618639-37636256.jpg | [37636256](https://www.pexels.com/photo/37636256/) | Cuatro personas en altura, cascos azules | 4 C | 4 C ✅ | 4 C ✅ | Correcto |

Los conteos marcados con "≈" son aproximados: en las multitudes hay cabezas tapadas que no se pueden contar con seguridad.

## Resumen

| | `imgsz=640` | `imgsz=1280` |
|---|:---:|:---:|
| Fotos con conteo exacto | 8 de 17 | 8 de 17 |
| Cabezas sin casco detectadas correctamente | 2 (las dos en la foto 15) | 4 (fotos 6, 12 y 15) |
| Fotos donde se pierde algún casco (sin contar la 15) | 5 | 5 |
| Fotos con algún falso "con casco" | 3 | 4 |

## Conclusiones

1. **Funciona bien en el caso simple:** pocas personas, cascos visibles y sin nada que los tape. Anda bien de frente, de perfil, de espaldas, a contraluz, en blanco y negro y con cascos de distintos colores.
2. **El cumplimiento sale más alto que el real.** El modelo confunde **gorras**, pañuelos y cabezas descubiertas con cascos, y casi nunca usa la clase "sin casco". En la foto 15 informa 88 % cuando el real es menor a 50 %.
3. **Pierde cascos tapados, cascos vistos desde arriba y personas agachadas.**
4. **Ningún tamaño de análisis es mejor en todo.** Con 1280 se ven mejor las personas lejanas y las cabezas sin casco, pero falla con cascos muy grandes y agrega cajas de más. Con 640 pasa lo contrario.
5. **Un casco en la mano cuenta como "con casco"** (foto 6, con 640). El modelo detecta el objeto casco, no si la persona lo tiene puesto.

# Observaciones de la directora: revisión 1 de la tesis v04

- Archivo revisado: `Loom - Tesis v04 rev 1 MOG.docx` (la v04 del commit `d51901c`, la que se envió el 2026-10-03).
- Fecha de los comentarios: 8 de octubre de 2026.
- Contenido: 20 comentarios, una nota escrita dentro del texto (en 3.1.1) y 9 fragmentos resaltados en amarillo sin
  comentario. No usó control de cambios, no marcó ningún comentario como resuelto y no hay respuestas encadenadas.
- Fuera de eso, el texto de la tesis no cambió: la comparación párrafo por párrafo contra la v04 enviada solo encuentra la nota.

## 1. Qué está pidiendo, en resumen

Las observaciones se agrupan en seis temas.

**A. Definir los términos la primera vez que aparecen.** Entre paréntesis y en el texto, no solo en la tabla de siglas:
*diff*, HU, *backlog*, Jira, Markdown, *framework* y la métrica pass@k. Resaltó además, sin comentario, SWE-bench,
*issues* e ISTQB, que parecen ir en el mismo sentido.

**B. No hablar de Loom antes de tiempo.** El primer párrafo de la justificación (1.4) debe redactarse sin la herramienta, y el
marco teórico (capítulo 2) no debe mencionar Loom: «No abordar Loom todavía, hasta resultados». Resaltó tres menciones más en
el capítulo 2.

**C. Quitar las frases que remiten a otros capítulos.** Pidió quitar «El capítulo 4 describe cada etapa.» (1.1) y la frase final
de 3.2 («Que la combinación produzca mejores resultados es lo que el capítulo 5 debe medir.»). Resaltó también «y así deben
leerse los resultados del capítulo 5.» (2.5).

**D. Organizar el trabajo por preguntas de investigación y no por hipótesis.** Es el cambio de fondo:
- quitar la nota de 1.6 «de acuerdo a lo que comentamos»;
- quitar las variables de 1.7 «ya que forman parte de la hipótesis»;
- en 4.1.6 dejar solo las preguntas de investigación;
- en 4.1.8 organizar el análisis por pregunta de investigación y no por H1;
- quitar el apartado 6.1.2 «Estado de las hipótesis».

**E. Reestructurar el marco teórico y el estado del arte.**
- El desarrollo dirigido por especificaciones (SDD) debe ser un tema aparte en el capítulo 2, no un párrafo dentro de 2.4.
- El estado del arte (3.1) se reorganiza por subtema y, dentro de cada subtema, un subtítulo por artículo (por ejemplo, 3.1.2
  «Resolución de tareas en repositorios reales» y 3.1.2.1 para el primer artículo citado, [3]). Cada artículo se redacta
  diciendo de qué trata y cuáles son sus resultados o características.

**F. Ajustes puntuales.**
- Revisar si «plausible» es el término adecuado en desarrollo de software (1.1).
- Citar en formato IEEE: la observación está sobre «Chen *et al.*», en 2.3.
- Explicar la métrica pass@k (2.3).
- Cambiar la forma de nombrar a quien operó Loom en 5.1.2 a «desarrollador freelance».
- Revisar el «;» del párrafo de la figura 1.2 y la última parte del objetivo general («ya sea que el proyecto arranque desde
  cero o ya tenga avance previo»), que resaltó sin comentario.

## 2. Comentarios, uno por uno

El número es el identificador del comentario en el .docx. «Texto marcado» es el fragmento al que está anclado.

| # | Apartado | Texto marcado | Observación | Qué implica |
|---|---|---|---|---|
| 11 | 1.1 | *diff* (en «el modelo que revisa ve el *diff*») | Definir concepto entre paréntesis | Definir *diff* en su primera aparición, por ejemplo «el *diff* (las líneas que un cambio agrega, modifica o elimina)». |
| 12 | 1.1 | plausible («Un modelo de lenguaje produce código plausible…») | Verificar que el término plausible esté adecuado al desarrollo de software | Revisar el término. Opciones: «código de apariencia correcta», «código que parece correcto», o conservarlo con una cita que lo use en ese sentido. |
| 14 | 1.1 | HU (párrafo de la figura 1.2) | Definir HU entre paréntesis | Escribir «historia de usuario (HU)» en la primera aparición del cuerpo, y revisar que la sigla no aparezca antes sin definir. |
| 15 | 1.1 | «El capítulo 4 describe cada etapa.» | Quitar | Borrar la frase (tema C). |
| 22 | 1.4 | Loom («Loom se dirige a equipos pequeños…») | Redefinir el párrafo, sin abordar la herramienta Loom | Reescribir el primer párrafo de la justificación hablando del problema y de a quién afecta, sin nombrar Loom (tema B). |
| 23 | 1.4 | *backlog* | definir | Definir *backlog* (la lista priorizada de trabajo pendiente de un producto). |
| 25 | 1.5 | Jira | Definir JIRA, markdown | Definir Jira (herramienta de seguimiento de proyectos e incidencias) y Markdown (formato de texto plano con marcas ligeras). |
| 26 | 1.5 | particular («un lenguaje o *framework* particular») | definir | Por la posición, lo que hay que definir parece ser *framework* (marco de trabajo para construir aplicaciones). Confirmar. |
| 28 | 1.6 | «…y están sujetas a validación con el director de la tesis.» | Quitar de acuerdo a lo que comentamos | Quitar la nota. Depende de lo que se habló con ella: puede ser solo la frase o todo el apartado de hipótesis (tema D, ver dudas). |
| 30 | 1.7 | «…miden la calidad del resultado y su costo.» | Quitar las variables, ya que forman parte de la hipótesis | Quitar el contenido de 1.7 (párrafo y tabla 1.1). El encabezado de la plantilla dice «Si es pertinente». |
| 34 | 2.1 | «…pesan en el diseño de un sistema como Loom.» | No abordar Loom todavía, hasta resultados | Quitar las menciones a Loom del capítulo 2 y redactar los conceptos en general (tema B). |
| 37 | 2.3 | *et al* («Chen *et al.* publicaron HumanEval…») | Referencias con IEEE | En IEEE la cita numérica va junto al autor que se nombra: «Chen *et al.* [16] publicaron…». Hoy el número va al final de la oración. Aplica a las nueve menciones de autor con *et al.* de los capítulos 2 y 3, y conviene revisar también «Runeson y Höst», «Arcuri y Briand», «Wohlin *et al.*», etc. |
| 38 | 2.3 | *k* (en pass@k) | Explicar la métrica | Explicar pass@k con más detalle: qué es *k*, cómo se estima y un ejemplo (pass@1 es la proporción de problemas resueltos al primer intento). |
| 40 | 2.4 | «(*Spec-Driven Development*, SDD)» | Abordar como tema aparte en Marco Teórico | Crear un apartado propio para SDD en el capítulo 2 (tema E). |
| 49 | 3.1.1 | Nota que la directora escribió en el texto (ver abajo) | Reorganizar | Reorganizar 3.1 por subtema y por artículo (tema E). |
| 57 | 3.2 | medir («…es lo que el capítulo 5 debe medir.») | Quitar | Borrar la frase final de 3.2 (tema C). |
| 70 | 4.1.6 | PI1 (tabla 4.3) | Dejar sólo preguntas de investigación | Quitar de la tabla 4.3 las hipótesis (H1, H2, H3) y dejar las filas de PI1 a PI5; ajustar el título del apartado. |
| 74 | 4.1.8 | H1 («Para H1, la calificación produce…») | Por pregunta de investigación | Reescribir el análisis de datos organizado por pregunta (PI1 a PI5), no por hipótesis. |
| 108 | 5.1.2 | operó («La persona investigadora operó Loom…») | Cambiar a desarrollador freelance | Nombrar a quien operó Loom como desarrollador *freelance*. Confirmar si aplica solo aquí o en toda la tesis (hoy se usa «la persona investigadora»). |
| 151 | 6.1.2 | «6.1.2 Estado de las hipótesis» | Quitar | Quitar el apartado 6.1.2 y llevar a 6.1.1 lo que haga falta de ese contenido (tema D). |

### Nota escrita en el texto (3.1.1)

> NOTA: Reorganizar estado del arte de la siguiente manera: por subtema (ejemplo 3.1.2 resolución de tareas en repositorios
> reales, incluir como subtítulo 3.1.2.1 el primer artículo citado [3] y redactar haciendo mención de qué trata el artículo o
> publicación y mencionar resultados o características.

## 3. Resaltados sin comentario

La directora resaltó en amarillo estos fragmentos sin escribir comentario. La interpretación es tentativa y se apoya en los
comentarios cercanos.

| Apartado | Texto resaltado | Interpretación probable |
|---|---|---|
| 1.1 (figura 1.2) | el «;» antes de «y las pruebas de humo… cierran el ciclo» | Puntuación: el punto y coma antes de «y» sobra; usar coma o partir la oración. |
| 1.3.1 Objetivo general | «, ya sea que el proyecto arranque desde cero o ya tenga avance previo.» | El modo con avance previo no se validó (1.5 lo declara como limitación); probablemente pide quitarlo del objetivo o matizarlo. |
| Capítulo 2, introducción | «Loom,» («los agentes con los que está hecho Loom») | Tema B: no mencionar Loom en el marco teórico. |
| 2.1 | «Loom» («Loom no usa recuperación…») | Tema B. |
| 2.3 | «SWE-bench» e «*issues*» | Tema A: definir qué es SWE-bench y qué es un *issue*. |
| 2.5 | «ISTQB» | Tema A: definir la sigla (International Software Testing Qualifications Board). |
| 2.5 | «y así deben leerse los resultados del capítulo 5.» | Tema C: remisión a otro capítulo. |
| 2.6 | «En Loom,» («En Loom, cada observación de la revisión lleva una severidad…») | Tema B. |
| 3.2 | «Que la combinación produzca mejores resultados es lo que el capítulo 5 debe medir.» | Tema C; coincide con el comentario 57. |

## 4. Dudas: lo que resolvió la conversación del 8 de octubre

1. **Hipótesis.** La decidió el autor el 2026-10-11: se quitan (ADR-0093). La directora dijo que se pueden dejar solo las preguntas de investigación
   «para no tener que comprobar hipótesis», y que, si hay una manera alcanzable de comprobarlas, se pueden dejar. Sus comentarios
   en el documento (30, 70, 74 y 151) van en la primera dirección. Si se quitan, cambian también el resumen, el *abstract*, la
   introducción, 4.1.7, 5.2.14 y 6.1.1, que hablan de H1.
2. **«Desarrollador freelance».** Resuelta: «la persona investigadora» de 5.1.2 es el autor, que operó Loom en las corridas, y
   debe mencionarse como un desarrollador *freelance*. Es la única aparición de esa expresión en la tesis.
3. **Comentario 26.** Sin respuesta directa; se aplica la regla general (ver 6): definir *framework* en su primera aparición.
4. **Objetivo general.** El autor decidió el 2026-10-11 quitar «ya sea que el proyecto arranque desde cero o ya tenga avance
   previo», que no se validó.
5. **Las diez decisiones del documento de pendientes.** Respondidas casi todas en la conversación (sección 6).

## 5. Dónde se hace cada cambio

Los cambios se hacen en `borrador/v04/` y se regenera `Loom - Tesis v04.docx`; el archivo de la directora no se edita.

| Tema | Archivos |
|---|---|
| A, definiciones | `a-preliminares-y-capitulo-1.md`, `b-capitulo-2-marco-teorico.md`, y la tabla de siglas en `a-…` |
| B, Loom fuera de 1.4 y del capítulo 2 | `a-…` (1.4), `b-…` |
| C, remisiones | `a-…` (1.1), `b-…` (2.5), `c-capitulos-3-y-4.md` (3.2) |
| D, preguntas en lugar de hipótesis | `a-…` (resumen, *abstract*, introducción, 1.6, 1.7), `c-…` (4.1.6 a 4.1.9), `f-capitulo-5-resultados.md` (5.2.14, 5.2.16), `g-capitulo-6-conclusiones.md` (6.1.1, 6.1.2) |
| E, SDD y estado del arte | `b-…` (nuevo apartado de SDD), `c-…` (3.1 completo) |
| F, ajustes puntuales | `a-…`, `b-…`, `f-…` (5.1.2) |

## 6. Acuerdos de la conversación por WhatsApp (8 de octubre de 2026)

La directora y el autor revisaron las decisiones del documento de pendientes por mensaje. Lo acordado:

| Tema | Acuerdo | Decisión del documento de pendientes |
|---|---|---|
| Loom en la justificación | No mencionar Loom en la justificación: es el objetivo de la tesis, se maneja como parte del desarrollo y se muestra en los resultados. | Confirma el comentario 22 (tema B) |
| Alcance de la validación | Cerrar con los dos pilotos y el experimento de control. | 1: opción a) |
| Hipótesis | Se pueden dejar solo las preguntas de investigación para no tener que comprobar hipótesis; si hay una manera alcanzable de comprobarlas, se pueden dejar. | 4 (ver duda 1) |
| Uso de IA en la redacción | Esperar al análisis de similitud: si el porcentaje es bajo, no hay problema. | 5: por ahora no se agrega la declaración |
| Rúbricas no aplicadas | Quedan como trabajo futuro. | 8 |
| Código de Loom | El repositorio del código queda privado. Las *skills* se quedan en la tesis. | 9: no se publica el código |
| «Persona investigadora» (5.1.2) | Se refiere al autor; mencionarlo como un desarrollador *freelance*. | Comentario 108 |
| Términos técnicos y abreviaturas | Definir al menos en su primera mención: HU, *skills*, Jira, Markdown y los demás términos técnicos, aunque estén en la tabla de símbolos y abreviaturas. La tesis debe entenderla alguien que no domina los conceptos. | Tema A |
| Voz | Sigue impersonal, como está redactada («se hizo», «se elaboró»); no se cambia a primera persona. | 6: mantenerla |
| Páginas de la guía institucional | Ya se pueden quitar. | 7: quitarlas |

Sin respuesta explícita quedaron la decisión 2 (calificación de H1 por una persona), la 3 (análisis estadístico de H1) y la 10
(cómputo de cuartillas). Las dos primeras dependen de lo que se decida con las hipótesis; la tercera se cumple con cualquier
criterio.

Otros puntos de la conversación:
- La directora sigue con la revisión y después pasará la tesis al codirector y al revisor.
- Mientras tanto, el autor ya puede redactar y enviar el oficio de la prórroga y, al entregarlo en la División de Estudios de
  Posgrado e Investigación, pedir que revisen su expediente.
- La directora comentó que la redacción mejoró mucho respecto de la versión anterior que recibió.

## 7. Cómo se atendió en la v05 (2026-10-11)

Los cambios están en `borrador/v05/` y en `Loom - Tesis v05.docx`. La v04 queda como la versión que revisó la directora.

| Observación | Cambio en la v05 |
|---|---|
| 11, 14, 23, 25, 26, 38 y resaltados de SWE-bench, *issues* e ISTQB (definir términos) | Definidos en su primera mención, en la introducción: *diff*, historia de usuario y criterios de aceptación, *skill*, Pull Request, pruebas de humo, Jira, Markdown. Se repite una definición breve donde la directora la pidió: *diff* y HU en 1.1, *backlog* en 1.4, Jira, Markdown, Playwright y *framework* en 1.5. En el capítulo 2: *prompt*, API, CLI, SWE-bench (*benchmark*), *issue*, GitHub Copilot, ISTQB, *pipeline*, GitHub Actions y *token*. En el capítulo 4: monorepo, *worktree*, *checks* y Cloud Run. Se agregó «PI» a la tabla de siglas. |
| 12 («plausible») | «código de apariencia correcta, pero sin garantía de que compile…» (1.1 y 2.1). |
| 15, 57 y resaltado de 2.6 (remisiones a otros capítulos) | Quitadas: «El capítulo 4 describe cada etapa», «Que la combinación… es lo que el capítulo 5 debe medir» y «así deben leerse los resultados del capítulo 5». |
| Resaltado del «;» (figura 1.2) | El párrafo se partió en oraciones. |
| Resaltado del objetivo general | Se quitó «ya sea que el proyecto arranque desde cero o ya tenga avance previo». |
| 22 (justificación sin Loom) | El primer párrafo de 1.4 habla de a quién se dirige el trabajo; 1.4 ya no menciona Loom. |
| 34 y resaltados del capítulo 2 (Loom) | El capítulo 2 no menciona Loom. Lo que decía sobre Loom pasó al capítulo 4: registros de decisión (4.2.1), sin recuperación (4.2.2), desarrollo dirigido por especificaciones (4.2.3), TDD (4.2.5), supuestos de la HU, integración continua como juez externo (4.2.6), federación de identidad (4.2.8) y alcance de las pruebas de humo (4.2.9). |
| 28, 30, 70, 74 y 151 (hipótesis y variables) | Sin hipótesis ni variables (ADR-0093): fuera 1.6 y 1.7; 1.2 reescrito; tabla 4.3 solo con preguntas; 4.1.8 organizado por pregunta; 5.1.1 y 5.2.16 por pregunta; 6.1.2 «Estado de las hipótesis» fuera y su contenido llevado a 6.1.1; resumen, *abstract* e introducción sin hipótesis. |
| 37 (IEEE) | El número de cita va junto al autor que se nombra («Chen *et al.* [n] publicaron…») en los capítulos 2, 3 y 4, y en la tabla 3.1. |
| 38 (pass@k) | Explicación de la métrica, con un ejemplo (pass@1 y pass@10) y el estimador de Chen *et al.* |
| 40 (SDD aparte) | Nuevo apartado 2.5 «Desarrollo dirigido por especificaciones»; los apartados siguientes del capítulo 2 se renumeraron (2.6 a 2.10) y las referencias cruzadas se ajustaron. |
| 49 y la nota (estado del arte) | 3.1 reorganizado por subtema, con un subtítulo de cuarto nivel por artículo (3.1.2.1 SWE-bench, 3.1.2.2 SWE-agent, …, 3.1.5.4); cada uno dice de qué trata el trabajo y sus resultados. `llenar_tesis.py` admite ahora `#### ` para ese nivel. |
| 108 («desarrollador freelance») | 5.1.2: «Loom lo operó un desarrollador *freelance*, el autor de esta tesis, …». |
| Alcance (WhatsApp) | ADR-0092; 4.1.2, 5.1.1 y la tabla 4.3 lo declaran; la matriz E1 a E4 y PI4 pasan a 6.3. |
| Rúbricas (WhatsApp) | Trabajo futuro en 6.3 y en el Anexo E. |
| Páginas de la guía (WhatsApp) | Quitadas por `quitar_instrucciones.py` (tramo en `secciones_quitadas.json`), junto con la instrucción de agradecimientos. Quedan en amarillo solo los datos de portada y la guía de agradecimientos. |
| Código de Loom (WhatsApp) | Sin cambios: el Anexo I ya lo declara privado y el Anexo F conserva los *prompts* de las *skills*. |


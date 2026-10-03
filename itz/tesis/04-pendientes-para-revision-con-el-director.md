# Tesis «Loom»: estado y decisiones pendientes para revisión con el director

Maestría en Sistemas Computacionales, Instituto Tecnológico de Zacatecas. Documento que acompaña a `Loom - Tesis v04.docx`.
Corte: 3 de octubre de 2026.

## 1. Estado del documento

- Están escritos todos los apartados de la guía institucional: introducción, capítulos 1 a 6, resumen, *abstract*, referencias y
  nueve anexos (A a I).
- Extensión: unas 81 cuartillas sin anexos ni referencias y unas 162 con ellos. La guía pide 80 como mínimo.
- Referencias: 61, en formato IEEE, verificadas una por una contra su fuente.
- Cifras: 87 de los capítulos 4 a 6 se recalculan desde la evidencia versionada y todas coinciden (`trazabilidad-de-cifras.md`).
- Evidencia: datos de las corridas, experimentos y guiones en el repositorio público de la tesis
  (https://github.com/CarlosSotoGarcia/jcsoto-tech-lead, carpeta `itz/tesis/evidencia/`).

## 2. Resultados principales

- El flujo completó el ciclo de punta a punta en dos proyectos de dominios y tecnologías distintos (inventarios con Java y Angular;
  agenda de un taller con Node y React): 29 paquetes de código fusionados, las dos aplicaciones desplegadas en Google Cloud y 145
  casos de prueba ejecutados (104 aprobados, 11 fallidos, 30 bloqueados).
- PI1: los 110 criterios de aceptación de las seis HUs quedaron cubiertos por al menos un caso de prueba. El 70 % de esos criterios
  los infirió el propio sistema, y falta valorar si los casos son suficientes.
- H1 (el contexto mejora la revisión): sin apoyo. En el experimento de control, con calificación automática, la proporción de
  observaciones relevantes fue de 32.9 % con contexto y de 30.4 % solo con el *diff*, sin diferencia significativa. El contexto sí
  cambió el tipo de hallazgo, y cerca de dos de cada tres observaciones fueron ruido o falsas en las dos condiciones.
- H2 (generalización): evidencia parcial. El segundo proyecto completó el ciclo sin cambiar las *skills*, pero exigió corregir
  supuestos de la plataforma.
- H3 (comparación de proveedores): no se ejecutó.
- PI5: defectos que la revisión y la compilación no señalaron aparecieron en la integración continua y en las pruebas sobre la
  aplicación desplegada.

## 3. Cómo leer el documento

Lo resaltado en amarillo no es texto de la tesis: son las instrucciones de la plantilla institucional (85 párrafos), la guía de
la sección de agradecimientos, los datos de portada y oficio por completar, y una nota de trabajo en el apartado 1.6.

## 4. Decisiones que se necesitan del director

| # | Decisión | Opciones | Recomendación |
|---|---|---|---|
| 1 | Alcance de la validación. El diseño prevé cuatro escenarios con API (dos proyectos por dos proveedores, E1 a E4); no se ejecutaron por falta de saldo en la API de Anthropic (unos 100 USD) y por la facturación bloqueada de Gemini. | a) Cerrar con los dos pilotos y el experimento de control, registrar la reducción de alcance y ajustar el capítulo 4. b) Ejecutar E1 a E4. | a). H3 quedaría como trabajo futuro. |
| 2 | Evaluación de H1. La relevancia de las 177 observaciones la calificó un modelo (distinto del revisor, a ciegas), no una persona como pedía el diseño. | a) Presentar el resultado como evaluación automática preliminar, como está hoy. b) Que una persona califique la hoja ya preparada (7 a 8 horas, en seis sesiones); conviene que la haga el director u otra persona, porque el autor ya conoce el resultado automático. | b) si hay tiempo, porque es el instrumento que decide la hipótesis central. |
| 3 | Análisis estadístico de H1: nivel de significancia de 0.05 con prueba bilateral y correlación rango-biserial como tamaño del efecto, fijados antes de conocer los resultados. | Confirmar o ajustar. | Confirmar. |
| 4 | Preguntas de investigación e hipótesis (apartados 1.2 y 1.6). El 1.6 todavía dice que están sujetas a su validación. | Validarlas para quitar esa nota, o pedir cambios. | Validar. |
| 5 | Declaración del uso de IA en la redacción de la tesis. | Nota metodológica en 4.1, apartado en la introducción o anexo. | Una nota breve en 4.1. |
| 6 | Voz de la tesis. Hoy usa sobre todo construcciones impersonales y «la persona investigadora». | Mantenerla, o pasar a primera persona del plural. | Mantenerla. |
| 7 | Instrucciones de la plantilla institucional (en amarillo). | Quitarlas en la versión de entrega o conservarlas. | Quitarlas. |
| 8 | Rúbricas definidas y no aplicadas (suficiencia de los casos de prueba, calidad de un paquete, calidad de la arquitectura; Anexo E). | Aplicarlas antes de entregar, o dejarlas como trabajo futuro. | Dejarlas como trabajo futuro, salvo la de suficiencia si se quiere cerrar PI1. |
| 9 | Acceso al código de Loom. El repositorio de la plataforma es privado y los anexos lo citan. | Hacerlo público o dar acceso a quienes revisen la tesis. | Dar acceso a quienes revisen. |
| 10 | Cómputo de cuartillas: si el mínimo de 80 incluye anexos y referencias. | — | Se cumple en los dos casos; basta confirmarlo. |

## 5. Datos que debe completar el autor

- Título definitivo de la tesis, nombre completo, nombre del director o directores y fecha (portada y oficio).
- Agradecimientos.

## 6. Trabajo opcional

Si el director lo considera necesario:

- Ampliar el capítulo 2 (hoy unas 3,100 palabras; el plan preveía unas 5,000).
- Repetir el experimento de control sobre una muestra para medir la variabilidad del modelo, y sumar una segunda persona evaluadora.
- Medir cuántas observaciones de la ejecución descartada del experimento repetían las del piloto.
- Que la plataforma valide en código que cada criterio de aceptación tenga al menos un caso de prueba.

El detalle de cada punto, con su origen, está en `itz/tesis/03-pendientes-de-la-tesis.md`.

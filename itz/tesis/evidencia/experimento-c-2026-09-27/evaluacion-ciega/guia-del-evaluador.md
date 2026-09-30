# Guía para calificar las observaciones de revisión (experimento C)

Vas a calificar observaciones que hizo un revisor automático sobre 29 Pull Requests de dos proyectos generados con Loom. Cada PR
se revisó más de una vez y en la hoja están mezcladas todas sus observaciones, en orden aleatorio y con un identificador que no dice
de qué revisión salió. No hace falta saberlo: se califica cada observación por sí misma.

## Qué tienes

- `hoja-de-evaluacion.xlsx`, pestaña «Calificación»: una fila por observación, agrupadas por PR (`P01` … `P29`).
- `contexto/Pnn.md`: para cada PR, el enlace al cambio revisado, el paquete de trabajo que debía implementar y, si pertenece a una
  historia de usuario, su especificación y sus casos de prueba.
- La pestaña «Rúbrica» de la hoja, con las cuatro calificaciones.
- `contexto/arquitectura-E1c.md` y `contexto/arquitectura-E3c.md`: el documento de arquitectura aprobado de cada proyecto, para juzgar
  las observaciones que hablan de la arquitectura.
- `plan-de-sesiones.md`: el orden sugerido para calificar en seis sesiones, con los enlaces de cada PR y una bitácora.

## Cómo calificar

1. Toma un PR a la vez. Lee su `contexto/Pnn.md` y abre el enlace «Cambio revisado» (es el primer commit del PR, antes de las
   correcciones: el código que vio el revisor, no el que se fusionó).
2. Para cada observación de ese PR, elige en la columna «calificación»:

   | Calificación | Cuándo |
   |---|---|
   | relevante y correcta | Señala un problema real del cambio, y lo que dice es correcto y accionable. |
   | relevante pero mal sustentada | El problema es real, pero la explicación, la ubicación o la sugerencia son imprecisas o incompletas. |
   | ruido | Es cierto pero no aporta: preferencia de estilo sin impacto, obviedad o algo que no vale la pena corregir. |
   | falsa | Es incorrecta: el problema no existe o contradice el código, la HU o la arquitectura. |

3. Si dos observaciones del mismo PR dicen en esencia lo mismo, califica las dos y en «misma que (id)» de una de ellas escribe el id
   de la otra.
4. «comentario» es opcional; úsalo para dudas o para explicar una calificación difícil.

## Reglas

- Juzga contra el código del cambio y contra lo que pide el paquete o la HU, no contra lo que tú habrías hecho.
- Algunas observaciones mencionan la HU, sus criterios o la arquitectura y otras no: no lo tomes en cuenta para calificar, solo si lo
  que dicen es cierto y útil.
- No abras la carpeta `clave/`, el archivo `datos/experimento_c-c1.json` ni la colección `experimento_c` de Mongo hasta terminar:
  ahí está a qué revisión pertenece cada observación. Tampoco abras `segunda-opinion/`: es la calificación que hizo un modelo con
  esta misma rúbrica, y verla antes influiría en la tuya.
- Si no puedes decidir una observación sin correr el código, elige la calificación más probable y anótalo en «comentario».

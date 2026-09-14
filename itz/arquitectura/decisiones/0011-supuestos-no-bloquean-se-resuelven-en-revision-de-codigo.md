# ADR-0011: Los supuestos no bloquean el pipeline — se resuelven visiblemente en la revisión de código

## Estado

Aceptada

## Contexto

La skill de descubrimiento y especificación ([skills/01](../skills/01-descubrimiento-y-especificacion-hu.md))
puede marcar una HU con `tiene_supuestos: true` cuando encuentra ambigüedad real que no puede inferir
con confianza. Quedaba pendiente (también en [skills/02](../skills/02-generacion-de-tcs.md)) decidir qué
hace el resto del pipeline con esa marca: detenerse a esperar confirmación humana, avanzar sin más, o
clasificar por gravedad.

## Decisión

El pipeline **no se detiene** por una HU con `tiene_supuestos: true`. El sistema avanza usando su
propia interpretación (ya documentada explícitamente en `spec.md`, ADR-0008), y esa interpretación
queda con **visibilidad obligatoria en el checkpoint humano que ya existe en el flujo: la revisión de
código** (S5, ADR-0004) — no se crea un mecanismo de pausa/aprobación nuevo antes de generar código.

Concretamente:

- Todo PR generado (S4) a partir de una subtarea que desciende de una HU con `tiene_supuestos: true`
  incluye, en la descripción del PR, los supuestos concretos que se hicieron y qué parte del código
  afectan.
- La skill de revisión de código (S5) trata esos supuestos como observaciones de alta prioridad por
  defecto: un PR que arrastra un supuesto sin confirmar no se aprueba "en automático" — requiere al
  menos una pasada donde el supuesto quede explícitamente aceptado, corregido, o escalado.

Esto es consistente con un principio ya establecido en `00-vision-general.md` (alcance, fuera de
alcance): "el sistema asiste, una persona sigue pudiendo intervenir en cualquier fase" — se reutiliza
ese punto de intervención existente en vez de inventar uno nuevo.

## Consecuencias

- El pipeline se mantiene fluido end-to-end sin fricción por cada ambigüedad menor: la mayoría de HUs
  no tendrán supuestos, y las que sí, no detienen el resto del trabajo.
- El costo de resolver la ambigüedad se traslada a la revisión de código, no al arranque del flujo.
- Riesgo aceptado explícitamente: si un supuesto crítico pasa desapercibido en la revisión, el código
  puede llegar a `develop` y solo se detecta en smoke testing (ADR-0006) o después — mismo riesgo que
  ya existe con cualquier PR normal, no es un riesgo nuevo introducido por esta decisión.
- Pendiente al detallar S4 (generación de código): cómo se propaga la referencia a los supuestos de
  `spec.md` hacia la descripción del PR.
- Pendiente al detallar S5 (revisión de código): la regla explícita de "no aprobar si hay supuestos sin
  resolver" y qué significa exactamente "resolver" uno (¿un comentario del revisor basta, o se exige un
  cambio de código?).

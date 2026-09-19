# ADR-0049: Skill 07 — revisión de código del PR y correcciones sobre la misma rama

## Estado

Aceptada. Implementa `skills/07-revision-de-codigo.md` sobre los PRs que abre la skill 06
([ADR-0046](0046-skill-06-generacion-de-codigo-agente-con-tdd.md)).

## Contexto

La skill 06 abre un PR por paquete, pero nadie lo revisa contra lo que se pidió: la ficha de la skill 07 pide
comparar el código con la spec, la arquitectura y las buenas prácticas, publicar observaciones y respetar la
regla de supuestos (ADR-0011).

## Decisión

1. **Qué revisa.** Un análisis (Claude o Gemini, el proveedor del Proyecto, ADR-0047) recibe el paquete, la
   spec y los TCs de la HU, la arquitectura del repositorio, la descripción del PR y su diff (recortado a 140 KB),
   y devuelve observaciones con fuente (`criterio_aceptacion`, `arquitectura`, `buenas_practicas`, `pruebas`,
   `seguridad`), severidad (`bloqueante`, `mayor`, `menor`), archivo/línea y sugerencia. El código no se ejecuta.
2. **Veredicto.** `aprobado` si no hay observaciones bloqueantes ni mayores (las menores son sugerencias);
   si no, `con_observaciones`. Una HU con supuestos (`tiene_supuestos`) añade siempre una observación
   bloqueante: no se aprueba en automático con supuestos sin confirmar (ADR-0011).
3. **Publicación.** La revisión se publica en GitHub como una revisión de solo comentarios con el resumen
   agrupado por fuente y, cuando la línea existe en el diff, comentarios en línea (si GitHub los rechaza se
   publica solo el resumen). No se aprueba ni se pide cambios en GitHub: la cuenta que abre el PR es la misma
   que revisa.
4. **Estados del paquete.** `pendiente` → `en_revision` (PR abierto) → `con_observaciones` | `aprobado` →
   `fusionado`. Se guardan `observaciones`, `rondas_revision` y `revisado_en`, y `paquetes/PT-0N.md` las
   refleja. «Sincronizar PRs» vigila los tres estados con PR abierto.
5. **Correcciones.** «Corregir» reutiliza el agente de la skill 06 sobre la rama del PR (no sobre la base): recibe
   las observaciones, lee los archivos, corrige lo señalado, hace commit y push a la misma rama y deja el paquete
   `en_revision` para revisarse de nuevo. Es una decisión de la persona; no hay rondas automáticas.
6. **Interfaz.** Botón «Revisar PRs» (todos los `en_revision`) y por paquete: revisar, ver observaciones y
   corregir; el «siguiente paso recomendado» guía revisar → corregir → fusionar y sincronizar.
   Endpoints: `POST .../hus/revisar-codigo?grupo=&pt=` y `POST .../hus/corregir-codigo?grupo=&pt=`.

## Consecuencias

- Cada revisión cuesta un análisis por PR; un diff enorme se recorta y puede perder observaciones.
- La aprobación es informativa: la fusión la hace una persona en GitHub (ADR-0015 sigue pendiente como gate).
- Las HUs con supuestos nunca quedan `aprobado` hasta que exista una forma de confirmarlos.

## Pendiente

- Confirmar supuestos desde la plataforma y aprobar manualmente.
- Usar el resultado de la CI del PR como evidencia de la revisión.
- Rondas automáticas revisar → corregir con tope, y el gate de revisión manual (ADR-0015).

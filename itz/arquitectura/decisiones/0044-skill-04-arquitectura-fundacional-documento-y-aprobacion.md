# ADR-0044: Skill 04 en modo fundacional — documento de arquitectura por repositorio y aprobación

## Estado

Aceptada. Implementa `skills/04-diseno-de-arquitectura.md` en modo fundacional
([ADR-0014](0014-modo-de-arranque-de-proyecto-y-ejecucion-selectiva-por-fase.md)) y cierra el
pendiente de esa ficha sobre el formato del artefacto de arquitectura fundacional.

## Contexto

Con el stack decidido ([ADR-0038](0038-stack-microservicios-y-autenticacion-declarados-en-fase-2.md),
[ADR-0039](0039-catalogo-de-stack-y-propuesta-del-arquitecto.md)) y las HUs especificadas y con TCs,
faltaba la arquitectura en sí (capas, módulos, modelo de datos, estructura de carpetas...) que
alimenta la descomposición en paquetes de trabajo (skill 05) y la generación del esqueleto (skill
06). Estaba pendiente el formato del artefacto y quién lo da por bueno.

## Decisión

1. **Un documento Markdown por repositorio** en el repositorio de control:
   `arquitectura/<repositorio>.md`, con front-matter (proyecto, repositorio, tipo, modo
   `fundacional`, fase `arquitectura_definida`, fecha, HUs analizadas) y secciones fijas: resumen,
   **Backend** (capas, módulos, estructura de carpetas, persistencia, seguridad, convenciones),
   **Modelo de datos** (entidades, atributos, relaciones), **Frontend** (estructura, módulos y
   pantallas, estado y datos, convenciones), **Despliegue**, **Decisiones** (decisión, por qué,
   alternativas descartadas) y **Supuestos y preguntas abiertas**. Las secciones de Backend y
   Frontend aparecen según lo que contiene el repositorio.
2. **Qué es "un repositorio"**: en un **monorepo** hay un solo documento que cubre backend y
   frontend (aunque el repositorio esté etiquetado como backend o fullstack); en **multirepo**, uno
   por repositorio. Sin elegir estructura, varios repositorios se tratan como multirepo.
3. **Trazabilidad**: cada módulo, entidad y pantalla cita las HUs (por id) que lo motivan. El diseño
   se hace para esas HUs, no para un sistema genérico.
4. **El stack es una restricción**: se toma de la configuración de Diseño (o, si falta, de la
   propuesta del arquitecto de ADR-0039); si no hay ninguno, la skill se detiene y lo dice.
5. **Ambigüedades no se resuelven en silencio** (ADR-0011): quedan como "supuestos y preguntas
   abiertas", cada una con el supuesto que se tomó.
6. **Aprobación humana**: la arquitectura queda "generada · pendiente de aprobar". La persona la
   revisa y la aprueba desde la pestaña Diseño (`POST /proyectos/{id}/arquitectura/aprobar`).
   Regenerarla borra la aprobación. La skill 05 solo debe descomponer una arquitectura aprobada.
7. **Ejecución**: la Fase 2 pasa a tener dos skills implementadas que corren en orden — casos de
   prueba y arquitectura (`POST .../hus/generar-tcs` y `.../hus/arquitectura`, con el mismo progreso
   en vivo). Se pueden correr juntas ("Ejecutar Fase 2", "Ejecutar todas") o la arquitectura sola. Que
   no haya TCs pendientes ya no es un error, para no frenar el paso siguiente.
8. **Alcance actual**: solo modo fundacional (Proyecto `nuevo`). `con_arquitectura` no invoca la
   skill (ADR-0014) y el modo extensión (`avanzado`) responde que todavía no está implementado.

## Consecuencias

- El documento vive en el repositorio de control (git local, ADR-0035), así que cada generación y
  regeneración queda en la bitácora (ADR-0037).
- Es un análisis de un solo intento por repositorio (~1 minuto): su calidad depende de la de las HUs
  y del stack elegido; por eso el paso de aprobación es obligatorio antes de generar código.
- El documento es la entrada de la skill 05, que en el primer paquete de trabajo producirá el
  esqueleto del aplicativo.

## Pendiente

- Skill 05 (paquetes de trabajo, con el esqueleto como primero) y su exigencia de arquitectura
  aprobada.
- Modo extensión (Proyecto con código previo), que parte del diagnóstico (skill 03).
- Iterar sobre el documento con comentarios de la persona en vez de solo regenerar.

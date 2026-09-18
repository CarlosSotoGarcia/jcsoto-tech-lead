# ADR-0035: Carpeta local estática como implementación provisional del repositorio de control

## Estado

Aceptada. Sustituye, para la implementación actual, la parte de ADR-0012 y ADR-0017 que definía el
repositorio de control como una URL de Git declarada explícitamente por la persona al dar de alta el
Proyecto.

## Contexto

ADR-0012 decidió que la documentación SDD por HU (ADR-0008: `spec.md`, `test-cases.md`, `plan.md`,
`tasks.md`, `subtareas/`, `evidencia/`) vive en **un repositorio de control por Proyecto**, separado de
los repos de código. ADR-0017 lo hizo explícito y obligatorio: la persona declara la URL de ese repo al
dar de alta el Proyecto, y la plataforma no crea uno por default.

En la implementación real (ADR-0033), esa pieza nunca se construyó: el resultado del análisis de skill
01 se guarda directo en MongoDB, sin escribir ningún archivo ni tocar ningún repositorio — la
"simplificación documentada" que ADR-0033 dejó como deuda técnica. Pedirle a la persona una URL de Git
para un repositorio de control que la plataforma todavía no sabe escribir es, además, prematuro: exige
una decisión (dónde vive ese repo, con qué permisos) antes de que el mecanismo de escritura exista.

## Decisión

Para la implementación actual, el repositorio de control deja de ser una URL declarada por la persona y
pasa a ser una **carpeta local, estática y no configurable**, agrupada por Proyecto:

```
loom/loom_target/<proyecto_id>/<HU-ID o AC-ID>/spec.md
                                                test-cases.md
                                                plan.md
                                                ...
```

- **Estática**: la ruta base (`loom/loom_target/`) es fija en el código, no un campo de configuración
  del Proyecto. El campo `repositorio_control_url` se **elimina** del esquema de Proyecto (ADR-0017) y
  del formulario de alta/edición — no se deja como campo sin uso.
- **Git local por Proyecto**: cada `loom_target/<proyecto_id>/` es un repositorio Git que Loom
  inicializa y commitea él mismo, sin remoto configurado. Esto conserva la propiedad de ADR-0008 de que
  el `git log` sobre estos archivos es la auditoría de las transiciones de fase — no se pierde ese
  mecanismo, solo se pospone a dónde vive el remoto.
- **Sin remoto todavía**: no hay push a GitHub/GitLab ni sync a un bucket en esta etapa. Es el siguiente
  paso natural (mencionado explícitamente por la persona) una vez que se defina el mecanismo — subir el
  repo local a un remoto Git, o sincronizar/exportar su contenido a un bucket para descarga — pero es
  una decisión de implementación futura, no parte de este ADR.
- `loom_target/` se ignora en el repositorio del propio Loom (es estado generado en tiempo de ejecución,
  no código fuente), igual que `loom/` ya se ignora en el repositorio raíz de este proyecto de tesis.

## Consecuencias

- Cierra parcialmente la deuda técnica que dejó ADR-0033: los artefactos SDD por HU ahora sí se escriben
  como archivos Markdown versionados, no solo como documentos de MongoDB. Mongo puede seguir sirviendo
  como caché de lectura rápida para las pantallas de la plataforma (ADR-0012 ya permite eso a futuro,
  "no se asume una base de datos separada por ahora; sería una optimización a evaluar"), pero la carpeta
  local es ahora la fuente de verdad.
- El esquema de Proyecto (ADR-0017) pierde el campo `repo_control.url`. Cuando se defina el mecanismo de
  sync a un remoto o bucket, ese mecanismo probablemente reintroduce un campo de configuración — pero
  sería el **destino del sync**, no "dónde vive la documentación mientras se genera", que es lo que este
  ADR fija.
- Da por resuelto, para esta etapa, el pendiente que ADR-0012 dejó abierto ("¿se declara explícito al
  dar de alta el Proyecto, o la plataforma crea uno por default?") — ninguna de las dos: la plataforma
  usa una ubicación fija, sin que la persona la declare.
- Sigue sin resolverse (ADR-0012, "Pendiente"): el mecanismo de sincronización remoto/bucket, y si la
  plataforma de visualización lee del filesystem local, de Mongo, o de ambos.

## Pendiente

- Mecanismo concreto de sync del repo local a un remoto Git o a un bucket (tecnología, credenciales,
  cuándo se dispara).
- Si/cuándo Mongo deja de usarse como caché de lectura y las pantallas leen directo de
  `loom_target/<proyecto_id>/` (más fiel a ADR-0012, que ya asumía leer del repositorio de control).

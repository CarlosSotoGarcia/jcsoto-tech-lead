# ADR-0058: Fuente de HUs «Markdown» con archivos subidos a una carpeta del servidor

## Estado

Aceptada. Implementa la fuente Markdown de [ADR-0009](0009-proyecto-como-entidad-de-configuracion-y-fuente-de-hus-pluggable.md) para la skill 01, que hasta ahora solo
soportaba Jira. Sustituye la idea original de una carpeta `hus/` dentro del repositorio de control.

## Decisión

1. **Se suben desde la plataforma.** En la pestaña Requerimientos de un Proyecto con fuente Markdown hay un cargador de archivos (varios `.md` a la vez, arrastrando
   o eligiendo). `POST /proyectos/{id}/fuente-hus/archivos` (multipart) los guarda en `loom/loom_fuentes/<proyecto_id>/` en el servidor (carpeta fuera de git);
   `GET` los lista y `DELETE .../archivos/{nombre}` quita uno. Como el proyecto debe existir para subir, el alta solo elige Markdown y los archivos se suben justo después de crearlo.
2. **Un archivo = una HU o actividad.** El título es el primer encabezado `# ...` (o el nombre del archivo) y el resto es la descripción, con la historia y sus
   criterios; un bloque YAML inicial (`--- ... ---`) se ignora. La clave del elemento (`fuente_ref`) es el nombre sin extensión. La skill 01 los analiza igual que las
   tareas de Jira: clasificación HU/Actividad, criterios explícitos e inferidos, supuestos, `spec.md`.
3. **Orden = prioridad de negocio.** Los archivos se analizan en **orden natural de nombre** (`HU-2` antes de `HU-10`); esa posición es `orden_fuente` (ADR-0048).
4. **Cambios.** Subir un archivo con el mismo nombre lo reemplaza; la revisión de cambios (ADR-0040, sin IA) compara la huella de título y descripción y marca nuevas,
   modificadas y retiradas, y permite actualizar solo lo que cambió.
5. **Seguridad de la subida.** Solo el nombre base (sin rutas: `../../x.md` queda `x.md`), extensión `.md`, UTF-8, máximo 1 MB por archivo y 200 por proyecto, y solo el
   rol administrador puede subir o borrar; los archivos rechazados se informan con su motivo.
6. **Configuración.** Con Markdown ya no hay «referencia» (esa era la URL de Jira): la Fase 1 cuenta como configurada cuando hay al menos un archivo subido
   (`fuente_md_archivos` en el Proyecto).

## Consecuencias

- Los archivos viven en el servidor, no en Git: para la tesis conviene respaldarlos junto con los datos del Proyecto (el `spec.md` derivado sí queda en el repositorio de control).
- Una sola HU por archivo: un documento con varias HUs debe partirse antes de subirlo.
- Si se elimina el Proyecto, la carpeta no se borra automáticamente.
- Se probó con un Proyecto de prueba: subida de varios archivos (con nombre malicioso, archivo vacío y no `.md`), orden natural, análisis con «Claude (cuenta normal)»,
  clasificación de una actividad y detección de un archivo modificado; y la interfaz en el navegador.

## Pendiente

- Varias HUs en un mismo archivo; subir una carpeta o un `.zip`.
- Editar un archivo desde la plataforma y reordenar sin cambiar nombres.
- Fuente GitHub (Issues), ADR-0010.

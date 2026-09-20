# ADR-0075: Rediseño de la interfaz como consola de desarrollo

## Estado

Aceptada. Cambia solo la capa visual y de interacción del frontend; no toca rutas, servicios ni contratos de la API.

## Contexto

La interfaz de Loom era un panel administrativo claro con tarjetas de sombra suave y el índigo por omisión de PrimeNG. La persona que la usa es una sola (el tech lead que lleva un Proyecto), en sesiones de horas, vigilando procesos largos (generación, revisión, release, smoke). Pidió un estilo de plataforma de desarrollo moderno, sin estética «Matrix», con la paleta de Novex Dynamics como referencia.

## Decisión

1. **Un solo tema oscuro** basado en Novex: navy (`#050d1a`, `#071222`, `#0a1a30`, `#0d2240`), azul `#3b82f6` como acción, cian `#22d3ee` solo para lo activo o en vivo. Inter para el texto y JetBrains Mono para IDs, rutas y cifras. Justificación de uso: monitor de escritorio, sesiones largas, logs y progreso en vivo como contenido principal.
2. **Los tokens viven en `styles.scss`** (variables `--color-*`, tipografía, radios, sombras) y el preset de PrimeNG (Aura, en oscuro) se alimenta de la misma paleta, de modo que los componentes existentes heredan el tema sin reescribirse. Los colores fijos que quedaban en componentes se pasaron a tokens.
3. **Estados con icono, texto y color**, no solo color (fase, estado del proyecto, resultados de smoke).
4. **Tablas densas** (`tabla-densa`): encabezado sobrio, filas compactas, IDs en mono; los datos secundarios pasan a subtítulos o etiquetas cortas para que quepan sin desplazamiento horizontal.
5. **Estructura de página**: barra lateral de 232 px con marca y navegación por iconos; en pantallas estrechas se convierte en barra superior. Enlace para saltar al contenido, foco visible en cian y respeto de `prefers-reduced-motion`.
6. **Alcance de esta tanda:** sistema de diseño más las pantallas clave (estructura, lista de proyectos, proyecto, HUs y detalle, progreso en vivo). El resto de las pantallas hereda el tema y se pule después.

## Consecuencias

- Requiere las fuentes de Google (Inter, JetBrains Mono); sin red cae a la fuente del sistema.
- Quedan pendientes del revisor: panel derecho con el siguiente punto de control, costo y último resultado; ícono y confirmación visible en las acciones que cuestan; revisión del resto de las pantallas.
- El documento del sistema de diseño (`DESIGN.md`) se genera del resultado final con la skill de diseño.

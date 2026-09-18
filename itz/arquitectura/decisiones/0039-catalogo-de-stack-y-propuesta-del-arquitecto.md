# ADR-0039: Catálogo de stack y propuesta del arquitecto al terminar la Fase 1

## Estado

Aceptada. Extiende [ADR-0038](0038-stack-microservicios-y-autenticacion-declarados-en-fase-2.md):
la tecnología deja de ser texto libre y pasa a ser una elección estructurada, y para Proyectos
nuevos el sistema propone el stack a partir de las HUs leídas.

## Contexto

ADR-0038 dejaba `tecnologia_backend` como texto libre y `tecnologia_frontend` como un enum de tres
valores, sin poder expresar el detalle real de un stack ("Java con Spring Boot, Hibernate y JPA";
"Angular con PrimeNG y NgRx"). Además, la persona de un Proyecto **nuevo** normalmente todavía no
sabe qué stack le conviene: eso es justo lo que un arquitecto decide *después* de leer los
requerimientos.

## Decisión

1. **Catálogo único de tecnologías** (`backend/src/loom_backend/catalogo_stack.py`, expuesto por
   `GET /catalogo/stack`): por capa (backend/frontend), una tecnología principal (backend: Java,
   Python, Node.js, .NET; frontend: Angular, Vue, React) y, dependiendo de ella, la lista de
   frameworks/herramientas seleccionables (Spring Boot, Hibernate, Spring Data JPA... para Java;
   FastAPI, SQLAlchemy... para Python; PrimeNG, NgRx... para Angular; etc.). El formulario y el
   prompt del arquitecto consumen el mismo catálogo, así que nunca se propone algo que la pantalla
   no pueda mostrar.
2. **Config del Proyecto**: `tecnologia_backend` pasa a ser la clave del catálogo (`java`,
   `python`...), y se agregan `herramientas_backend` y `herramientas_frontend` (listas). El
   formulario ofrece primero la tecnología principal y luego un multiselect con sus herramientas;
   al cambiar la principal se descartan las herramientas que ya no le aplican.
3. **Propuesta del arquitecto**: al terminar la Fase 1 de un Proyecto con `modo_arranque: nuevo`,
   un paso adicional del propio stream de descubrimiento (ADR-0033) manda las HUs y actividades ya
   especificadas a un análisis con prompt de arquitecto senior: evalúa el tipo de sistema y qué lo
   hace exigente (transaccionalidad, seguridad, volumen, reportes...), decide monolito vs.
   microservicios (por defecto monolito salvo razón concreta), elige tecnología y herramientas del
   catálogo, autenticación y estructura de repositorios, y **justifica cada elección citando las
   HUs concretas que la motivan y las alternativas descartadas**. El despliegue (GCP) no se
   propone: ya está decidido.
4. **Persistencia y precarga**: la propuesta se guarda en el Proyecto (`propuesta_stack`, estado
   operativo como `fases_ultima_ejecucion`, ADR-0037). La pestaña Diseño la muestra en un banner
   ("Según las N HUs leídas en Fase 1...") con la justificación completa, y **precarga solo los
   campos que la persona aún no ha configurado**; nada se guarda hasta que ella confirme con
   Guardar cambios. Un botón permite aplicar la propuesta completa sobreescribiendo.
5. Si el análisis falla, la Fase 1 no se invalida: el descubrimiento de HUs ya quedó guardado y el
   stream informa que no hubo propuesta.

## Consecuencias

- Cierra en la práctica el pendiente de skill 04 (modo fundacional): el stack llega decidido y
  justificado antes de que la skill corra; la persona lo revisa en vez de partir de cero.
- La propuesta se regenera en cada corrida de Fase 1 de un Proyecto nuevo; la configuración ya
  guardada por la persona nunca se pisa automáticamente.
- El catálogo es deliberadamente corto; ampliarlo es agregar entradas a `catalogo_stack.py`.

## Pendiente

- Con muchas HUs (más de ~60) el prompt del arquitecto resume solo una muestra.
- Datos que un arquitecto también decidiría y que aún no se capturan: base de datos, cola de
  mensajes, estrategia de despliegue concreta en GCP.

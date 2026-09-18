# ADR-0038: Stack, despliegue, microservicios y autenticación declarados como config de Fase 2

## Estado

Aceptada. Resuelve un pendiente que dejaba abierto `skills/04-diseno-de-arquitectura.md`: "Cómo se
decide el stack/framework en modo fundacional cuando el tipo de Proyecto (ADR-0009, solo 'web' por
ahora) no basta para elegirlo por sí solo."

## Contexto

`skills/04-diseno-de-arquitectura.md` opera en **modo fundacional** cuando `modo_arranque: nuevo`
(ADR-0014): define la arquitectura inicial desde cero, incluyendo la elección de stack/framework.
Hasta ahora esa elección quedaba completamente a criterio del LLM en el momento de correr la skill
— sin que la persona pudiera fijar de antemano qué tecnología quiere usar, cuántos microservicios
tiene pensados, o qué tipo de autenticación va a manejar el sistema.

Esto es información que la persona típicamente ya sabe al dar de alta el Proyecto (viene de una
decisión de negocio/equipo, no algo que Loom deba inventar), y dejarla fuera empuja a la skill 04 a
adivinar o a preguntar en cada corrida.

## Decisión

Se agregan campos **opcionales** a la configuración de Proyecto, capturados en la Fase 2
(Diseño) del formulario — no son obligatorios para que Fase 2 cuente como configurada (ADR-0034):
solo son contexto adicional para cuando skill 04 exista.

- `proveedor_nube`: `gcp` | `aws` — dónde se va a desplegar. Por ahora la plataforma solo habilita
  GCP en el formulario (AWS aparece deshabilitado); el valor `aws` existe en el modelo para no
  romper datos cuando se habilite.
- `estructura_repositorios`: `monorepo` | `multirepo`. Monorepo = backend y frontend en el mismo
  repositorio (un solo repo de tipo `fullstack` en la lista de repositorios objetivo, ADR-0005);
  multirepo = un repositorio por frontend, por backend y por cada microservicio.
- `tecnologia_backend: str | null` — lenguaje/plataforma del backend. Nació como texto libre; ADR-0039
  lo cambia a una clave de catálogo (`java`, `python`...) con herramientas seleccionables.
- `numero_microservicios: int | null` — cuántos microservicios de backend tiene pensados el
  Proyecto; vacío o 0 se interpreta como monolito/no aplica.
- `tecnologia_frontend`: `angular` | `vue` | `react` — enum cerrado, a diferencia del backend: el
  conjunto de frameworks de frontend soportados es corto y skill 04 necesita interpretarlo sin
  parsear texto.
- `herramientas_backend` / `herramientas_frontend` — listas de frameworks y librerías elegidos
  dentro de la tecnología principal (ADR-0039).
- `plantilla_frontend: str | null` — plantilla/UI kit gratuito que se quiere usar sobre el
  framework (p. ej. "PrimeNG Sakai", "Vuetify", "MUI"), texto libre.
- `tipo_autenticacion` — enum cerrado (mismo criterio: patrones bien conocidos que skill 04 debe
  poder interpretar): `jwt` | `oauth2_oidc` | `sesion_cookie` | `api_key` | `ninguna`.

**Granularidad**: estos campos son **por Proyecto, no por repositorio objetivo** — un solo stack de
backend, uno de frontend, un número de microservicios y un tipo de autenticación, aunque el
Proyecto tenga varios repos configurados (ADR-0005). Si en el futuro se necesita que cada
microservicio declare su propia tecnología o autenticación (arquitectura realmente heterogénea por
servicio), eso es una extensión posterior, no parte de esta decisión.

## Consecuencias

- `skills/04-diseno-de-arquitectura.md` (modo fundacional): cuando estos campos vienen llenos, la
  skill los usa como restricción explícita en vez de elegir stack/framework por su cuenta — cierra
  el pendiente citado arriba. Cuando vienen vacíos, el comportamiento no cambia: la skill sigue
  decidiendo como hasta ahora.
- No afecta `fases_configuradas` (ADR-0034/ADR-0036): activar Fase 2 sigue exigiendo solo repos
  objetivo, estos campos son captura progresiva y opcional.
- `numero_microservicios` es informativo por ahora — no genera automáticamente N entradas en la
  lista de repositorios objetivo ni valida consistencia entre ambos; es la persona quien mantiene
  coherencia entre "cuántos microservicios dije" y "cuántos repos configuré".

## Pendiente

- Si `tipo_autenticacion` necesita variar por microservicio en Proyectos con arquitectura realmente
  heterogénea — no cubierto aquí (ver "Granularidad" arriba).
- Cómo exactamente skill 04 traduce `tipo_autenticacion` en decisiones concretas de arquitectura
  (qué librería, qué flujo) — eso es implementación de la skill, no de este ADR.

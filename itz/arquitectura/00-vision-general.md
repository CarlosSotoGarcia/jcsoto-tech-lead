# Telar — visión general de la solución

> **Telar** es el nombre del sistema que este documento diseña: el orquestador y el conjunto de skills
> que, a partir de una HU, generan TCs, diagnostican avance, diseñan arquitectura, generan código,
> revisan, y validan con smoke tests (ver `skills/`). Se distingue explícitamente del **Proyecto**: la
> aplicación objetivo que Telar construye o evalúa a partir de las fuentes de HUs configuradas
> (ADR-0009) — Telar es la herramienta: el Proyecto es lo que Telar construye o revisa.
>
> Punto de entrada rápido al diseño. El detalle completo del planteamiento y la justificación original
> está en la propuesta aprobada por los asesores:
> [`../documentación/propuesta-tesis-idea-elegida.pdf`](../documentación/propuesta-tesis-idea-elegida.pdf).
> El objetivo, los objetivos específicos y el alcance de **esta página son los vigentes** y ya
> incorporan los ajustes de diseño posteriores a la aprobación (ver Estado).

## Estado

**Aprobada por los asesores**, con el diseño refinado en varios ADRs desde entonces:

- [ADR-0002](decisiones/0002-alcance-de-infraestructura-diseno-no-despliegue.md) — la infraestructura
  de indexación se documenta a nivel de diseño, no se despliega ni se opera como servicio persistente.
- ~~ADR-0003~~ — código como eje y HUs como contexto secundario. **Reemplazado por ADR-0004.**
- [ADR-0004](decisiones/0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md) — la HU es
  la entrada primaria: el skill genera código a partir de ella, abre PRs, se autorrevisa y valida con
  smoke tests. Este es el diseño vigente.
- [ADR-0005](decisiones/0005-solucion-configurable-repositorios-y-ambiente-dev.md) — la solución es
  configurable por N repositorios (backend/frontend) y una URL de ambiente de desarrollo.
- [ADR-0006](decisiones/0006-smoke-tests-con-playwright-y-bitacora-de-hus.md) — smoke tests con
  Playwright (Python); bitácora de HUs preferentemente en GitHub (parte propuesta, no cerrada).
- [ADR-0007](decisiones/0007-soporte-proyectos-con-avance-previo.md) — el sistema soporta proyectos con
  avance previo (brownfield), no solo proyectos nuevos: diagnostica qué criterios de aceptación ya
  están cubiertos antes de diseñar y descomponer.
- [ADR-0008](decisiones/0008-adopcion-de-sdd-y-nombres-de-artefactos.md) — se adopta Spec-Driven
  Development; cada HU tiene su carpeta de trabajo (`spec.md`, `test-cases.md`, `plan.md`, `tasks.md`,
  `paquetes/`, `evidencia/`) en Markdown con front-matter, sin JSON.
- [ADR-0009](decisiones/0009-proyecto-como-entidad-de-configuracion-y-fuente-de-hus-pluggable.md) — se
  introduce "Proyecto" como entidad de configuración raíz: tipo de proyecto (solo web por ahora) +
  repos/ambiente (ADR-0005) + fuente de historias de usuario pluggable, decidida por proyecto.
- [ADR-0010](decisiones/0010-agregar-github-como-fuente-de-hus.md) — se agrega GitHub (Issues) como
  tercera fuente de HUs soportada, junto a Jira y Markdown.
- [ADR-0011](decisiones/0011-supuestos-no-bloquean-se-resuelven-en-revision-de-codigo.md) — un supuesto
  sin resolver no detiene el pipeline; se hace visible y se resuelve en la revisión de código (S5).
- [ADR-0012](decisiones/0012-plataforma-de-visualizacion-y-reportes.md) — la plataforma visualiza el
  avance por HU (log/timeline) y genera reportes agregados, de solo lectura sobre lo que las skills ya
  escriben. Resuelve un pendiente de ADR-0008/0009: la documentación por HU vive en **un repositorio de
  control por Proyecto**, no dispersa en los repos objetivo.
- [ADR-0013](decisiones/0013-cuenta-de-desarrollo-dedicada-para-acceso-a-repositorios.md) — el sistema
  opera sobre los repos objetivo con una cuenta de desarrollo dedicada (no personal), acotada por
  Proyecto — todo commit/PR generado queda identificable como del sistema, no de una persona.
- [ADR-0014](decisiones/0014-modo-de-arranque-de-proyecto-y-ejecucion-selectiva-por-fase.md) — un
  Proyecto declara su modo de arranque (`nuevo` / `con_arquitectura` / `avanzado`), y el orquestador
  soporta ejecutar una sola fase bajo demanda, no solo el flujo secuencial completo.
- [ADR-0015](decisiones/0015-revision-manual-opcional-antes-de-merge.md) — la cuenta de desarrollo
  (ADR-0013) se declara explícita por Proyecto; el merge puede requerir además una aprobación humana de
  una lista configurada de usuarios autorizados, según el Proyecto.
- [ADR-0016](decisiones/0016-cuentas-de-prueba-por-rol-para-ejecucion-de-tcs.md) — la configuración de
  Proyecto incluye una cuenta de prueba por rol de la aplicación; cada TC declara qué rol necesita.
- [ADR-0017](decisiones/0017-esquema-de-configuracion-de-proyecto.md) — esquema consolidado de toda la
  configuración de Proyecto (repos/ambiente, fuente de HUs, repo de control, cuenta de desarrollo, modo
  de arranque, revisión manual, cuentas de prueba, arquitectura base).
- [ADR-0018](decisiones/0018-framework-de-agentes-e-indexacion-de-codigo.md) — el orquestador y las
  skills se implementan sobre Claude Code Skills; el análisis de código es bajo demanda (grep/glob),
  sin índice persistente (ni AST ni embeddings).
- [ADR-0019](decisiones/0019-contrato-comun-de-adaptadores-de-fuente-de-hus.md) — contrato común que
  todo adaptador de fuente de HUs (Jira, Markdown, GitHub, y futuras) debe cumplir.
- [ADR-0020](decisiones/0020-smoke-testing-corre-todos-los-tcs-como-regresion.md) — cada corrida de
  smoke testing ejecuta todos los TCs de la HU (no solo los del paquete de trabajo), y cada corrida versionada
  sirve como historial de regresión.
- [ADR-0021](decisiones/0021-convencion-de-nombre-de-rama-basada-en-id-fuente.md) — la rama de cada
  paquete de trabajo se nombra `hu/{id_fuente}/{paquete_id}`, reutilizando el `id_fuente` del contrato
  de adaptadores (ADR-0019).
- [ADR-0022](decisiones/0022-repos-fuera-de-configuracion-o-de-alcance.md) — un repo fuera de la
  configuración del Proyecto se marca como pendiente de definir (recuperable); un tipo de sistema fuera
  del alcance de Telar se marca como fuera de alcance y la plataforma ofrece continuar o no.
- [ADR-0023](decisiones/0023-smoke-testing-espera-a-toda-la-hu-no-por-subtarea.md) — smoke testing no
  se dispara por cada paquete de trabajo fusionado; espera a que toda la ronda (descomposición original
  o tanda de fixes) esté fusionada. Separa "reportar avance" (continuo, vía la plataforma) de "validar
  comportamiento" (una vez por ronda).
- [ADR-0024](decisiones/0024-creacion-de-subtareas-en-la-fuente-via-mcp.md) — cuando la fuente de HUs
  es Jira o GitHub, la skill de descomposición también crea los paquetes de trabajo ahí vía MCP; el control
  interno en el repo de control (ADR-0012) siempre existe, sin importar la fuente. Con Markdown como
  fuente, el control interno es la única representación posible — no hay plataforma externa a la que
  escribir. Si esa creación falla, solo se advierte (reporte en la plataforma con opción de reintentar),
  no bloquea.
- [ADR-0025](decisiones/0025-verificacion-de-despliegue-antes-de-smoke-testing.md) — antes de correr
  smoke tests, el orquestador verifica que el ambiente de desarrollo ya refleja el código recién
  fusionado (fusionar no es lo mismo que desplegar).
- [ADR-0026](decisiones/0026-vocabulario-unificado-hu-actividad-paquete-de-trabajo.md) — vocabulario
  unificado: **HU** (con criterios de aceptación, pipeline completo) vs. **Actividad** (sin criterios,
  trabajo de arquitectura/preparación, pipeline reducido sin TCs ni smoke testing); **elemento del
  backlog** como término genérico antes de clasificar; **paquete de trabajo** en vez de "subtarea
  técnica" para lo que genera la skill de descomposición. Resuelve la colisión de vocabulario que
  arrastraba `00-vision-general.md` desde ADR-0009.
- [ADR-0027](decisiones/0027-prototipo-como-input-complementario.md) — el prototipo, cuando se
  entrega junto con la HU, informa la generación de TCs y la descomposición para cubrir back y front
  sin huecos, resolviendo la ambigüedad del diagnóstico inicial.
- [ADR-0028](decisiones/0028-ciclo-automatizado-de-calidad-como-mecanismo-suficiente.md) — sin
  revisión manual, el ciclo código→revisión→corrección sigue siendo el mecanismo de calidad, con
  evidencia documentada (rondas de revisión, comentarios del PR); un supuesto sin resolver no fuerza
  revisión manual por sí solo.
- [ADR-0029](decisiones/0029-orden-secuencial-de-paquetes-de-trabajo-dependientes.md) — paquetes de
  trabajo dependientes entre repos se generan en secuencia estricta (p. ej. backend antes que
  frontend), nunca en paralelo.
- [ADR-0030](decisiones/0030-paralelismo-entre-hus-con-dependencias.md) — el orquestador puede procesar
  varias HUs en paralelo dentro de un Proyecto, salvo que una dependa explícitamente de otra
  (`depende_de` a nivel HU).
- [ADR-0031](decisiones/0031-stack-tecnologico-de-la-plataforma-loom.md) — la plataforma Loom (ver
  [especificación de la plataforma](especificacion-plataforma-telar.md) y su
  [perfil de pantallas](pantallas-plataforma-telar.md)) se construye como monorepo: backend en
  Python + Pydantic, MongoDB con driver compatible con Firestore de GCP, frontend en Angular; login
  obligatorio para todo actor humano.
- [ADR-0032](decisiones/0032-mecanismo-de-credencial-de-la-cuenta-de-desarrollo.md) — mecanismo
  concreto de la credencial de la cuenta de desarrollo (ADR-0013) para repositorios en GitHub: PAT de
  grano fino desde una cuenta de servicio como mecanismo por defecto, GitHub App como evolución cuando
  Loom opera muchos Proyectos a la vez.
- [ADR-0033](decisiones/0033-primera-implementacion-skill-01-descubrimiento.md) — primera skill del
  pipeline (no solo de la plataforma) implementada en código real: descubrimiento y análisis de HU
  para fuente Jira, con Claude vía tool-use estructurado; `spec.md` persistido en Mongo, con la
  escritura al repositorio de control resuelta después en ADR-0035.
- [ADR-0034](decisiones/0034-fases-de-desarrollo-y-configuracion-minima-por-fase.md) — las 9 skills se
  agrupan en 4 fases de desarrollo (Requerimientos, Diseño, Desarrollo, Implementación — esta última
  incluye Test/Smoke Test), cada una con su propia configuración mínima; activar un Proyecto en la
  plataforma ya no exige toda la configuración, solo la de la Fase 1.
- [ADR-0035](decisiones/0035-carpeta-local-estatica-como-repositorio-de-control.md) — para la
  implementación actual, el repositorio de control deja de ser una URL de Git declarada por la
  persona (ADR-0017) y pasa a ser una carpeta local estática y no configurable
  (`loom/loom_target/<proyecto_id>/`), con su propio repo Git local por Proyecto que Loom inicializa
  y commitea — sin remoto todavía.
- [ADR-0036](decisiones/0036-ambiente-de-desarrollo-solo-hasta-fase-4.md) — el ambiente de
  desarrollo que ADR-0034 exigía tanto en Fase 2 como en Fase 4 se queda solo como requisito de
  Fase 4 (Implementación, donde realmente se usa para smoke testing) — Fase 2 deja de pedirlo, para
  cualquier modo de arranque.
- [ADR-0037](decisiones/0037-bitacora-y-resumen-de-ejecucion-por-fase-en-plataforma.md) — la
  plataforma expone el `git log` del repositorio de control como bitácora (sin duplicarlo aparte),
  y el Proyecto gana un campo operativo de última ejecución por fase; la pantalla de Proyecto pasa
  de wizard a tabs, con los datos generales fijos arriba y cada tab mostrando su resumen, su botón
  de play y su configuración juntos.
- [ADR-0038](decisiones/0038-stack-microservicios-y-autenticacion-declarados-en-fase-2.md) — el
  Proyecto gana campos opcionales en Fase 2 (nube de despliegue —solo GCP habilitado—, monorepo o
  multirepo, tecnología de backend, framework y plantilla de frontend, número de microservicios,
  tipo de autenticación) para que skill 04, en modo fundacional, no tenga que adivinar el stack
  cuando la persona ya lo sabe.
- [ADR-0039](decisiones/0039-catalogo-de-stack-y-propuesta-del-arquitecto.md) — la tecnología del
  Proyecto pasa a un catálogo con herramientas dependientes (Java → Spring Boot, Hibernate, JPA...),
  y al terminar la Fase 1 de un Proyecto nuevo un análisis de arquitecto propone el stack con su
  justificación (citando las HUs) y lo precarga en la pestaña Diseño.
- [ADR-0040](decisiones/0040-deteccion-de-cambios-en-la-fuente-y-regeneracion-selectiva.md) — cada
  HU guarda la huella de su fuente en Jira; la plataforma revisa sin LLM qué HUs son nuevas o
  cambiaron y permite regenerar solo esas (o una puntual), dejando el historial en la bitácora.
- [ADR-0041](decisiones/0041-configuracion-de-despliegue-gcp-para-release-sh.md) — la pestaña
  Implementación captura lo necesario para armar el release.sh de GCP (proyecto, región, servicios,
  Artifact Registry, disparador, autenticación —Workload Identity Federation recomendada— y solo
  *nombres* de secretos), con una guía de lo que hay que preparar en GCP.
- [ADR-0042](decisiones/0042-skill-de-release-generacion-de-release-sh.md) — skill 10 (Fase 4): genera
  `release.sh`, el workflow de GitHub Actions o `cloudbuild.yaml` y un LEEME con los pasos únicos de
  GCP, de forma determinista y sin credenciales; quedan en el repositorio de control, pendiente
  publicarlos en el repositorio del código.
- [ADR-0043](decisiones/0043-copias-locales-cuenta-de-desarrollo-y-publicacion-por-pr.md) — la cuenta
  de desarrollo (usuario + token de GitHub) se captura por Proyecto en la pestaña Desarrollo, con
  botón para probar conexión y permisos; los repositorios se clonan en `loom/loom_repos/` y se trabaja
  en ramas dentro de worktrees; primer uso: publicar el release.sh por Pull Request.
- [ADR-0044](decisiones/0044-skill-04-arquitectura-fundacional-documento-y-aprobacion.md) — skill 04 en
  modo fundacional: un documento de arquitectura por repositorio (capas, módulos, modelo de datos,
  frontend, despliegue, decisiones y preguntas abiertas, citando las HUs) que la persona aprueba antes
  de descomponer; la Fase 2 corre casos de prueba y arquitectura.
- [ADR-0045](decisiones/0045-skill-05-descomposicion-desde-arquitectura-fundacional.md) — skill 05 desde la
  arquitectura aprobada: planea el esqueleto (grupo BASE) y el orden de las HUs, y parte cada HU en
  paquetes de una sola capa y un solo repositorio que cubren todos sus TCs; `tasks.md` y `PT-0N.md` en
  el repositorio de control y la lista en la pestaña Desarrollo.
- [ADR-0046](decisiones/0046-skill-06-generacion-de-codigo-agente-con-tdd.md) — skill 06: un agente con
  herramientas acotadas escribe el código de un paquete en su rama, con TDD (pruebas unitarias primero,
  compuerta que las exige), abre el PR con la cuenta de desarrollo y sincroniza el estado de los PRs.
- [ADR-0047](decisiones/0047-proveedor-de-ia-por-proyecto-claude-o-gemini.md) — la IA es un atributo del
  Proyecto (Claude o Gemini) para las skills de análisis y el agente de código; keys por Proyecto o del
  servidor.
- [ADR-0048](decisiones/0048-orden-de-implementacion-de-hus-y-avance-por-hu.md) — orden de implementación de
  las HUs (prioridad de la fuente ajustada por dependencias) y avance por HU en Desarrollo: la skill 06
  elige por ese orden o con la HU que se indique.
- [ADR-0049](decisiones/0049-skill-07-revision-de-codigo-y-correcciones.md) — skill 07: revisión del PR contra
  spec, arquitectura y buenas prácticas, observaciones publicadas en GitHub y correcciones sobre la misma rama.
- [ADR-0050](decisiones/0050-entorno-de-desarrollo-dockerizado-y-readme-en-el-esqueleto.md) — el primer paquete
  del esqueleto deja el entorno de desarrollo dockerizado y su README, y se exige al agente.
- [ADR-0051](decisiones/0051-aceptar-y-fusionar-el-pr-desde-la-plataforma.md) — la persona acepta (fusiona) el PR de un
  paquete desde la lista de paquetes, con la cuenta de desarrollo; libera a los dependientes.
- [ADR-0052](decisiones/0052-backend-documentado-con-swagger-openapi.md) — el backend se genera documentado con Swagger/OpenAPI:
  la arquitectura define la API y el contrato de endpoints, y el agente y la revisión lo exigen.
- [ADR-0053](decisiones/0053-proveedor-claude-cuenta-normal-para-desarrollo.md) — proveedor «Claude (cuenta normal)»: usa el
  CLI de Claude Code de la máquina (sesión, sin API de pago) para desarrollo local; agente confinado al repositorio.
- [ADR-0054](decisiones/0054-release-py-en-lugar-de-release-sh.md) — el release se genera como `release.py` (Python, multiplataforma)
  en lugar de `release.sh`; el nombre del secreto se valida.
- [ADR-0055](decisiones/0055-ejecutar-el-release-desde-la-plataforma.md) — botón para ejecutar el release desde la plataforma
  (con el gcloud de la máquina y confirmación) y detección de cambios de infraestructura que dejan el despliegue desactualizado.
- [ADR-0056](decisiones/0056-un-readme-por-servicio.md) — un README por servicio (backend, frontend, microservicios) además
  del de la raíz; el esqueleto lo crea, el agente lo mantiene y la revisión lo verifica.
- [ADR-0057](decisiones/0057-instrumentacion-de-metricas-de-uso-de-ia.md) — métricas de uso de IA por llamada, skill, reintento y
  compuerta (proveedor, modelo, tokens, tiempo, costo), con resumen en pantalla y exportación CSV para la tesis.
- [ADR-0058](decisiones/0058-fuente-de-hus-markdown-con-archivos-subidos.md) — fuente de HUs Markdown: se suben varios `.md` desde
  la plataforma a una carpeta del servidor (un archivo por HU o actividad, orden natural de nombre) y de ahí arranca el análisis.
- [ADR-0059](decisiones/0059-smoke-testing-por-hu-con-script-generado-desde-el-codigo.md) — skill 08: smoke testing por HU; la IA lee el
  código, escribe un script de Playwright (validado y ejecutado aparte con cuentas de prueba por rol), un agente de navegador verifica los
  fallos y cada corrida queda como regresión repetible sin IA.
- [ADR-0060](decisiones/0060-diagnostico-de-avance-con-agente-de-navegador.md) — skill 03: diagnóstico de avance; el agente de navegador prueba los
  TCs contra el ambiente existente, marca cada uno cubierto/pendiente/sin evaluar y la skill 05 solo descompone lo pendiente.
- [ADR-0061](decisiones/0061-generacion-de-fixes-desde-smoke-testing.md) — skill 09: los TCs fallidos del smoke testing se diagnostican y se convierten en
  paquetes de fix (nueva ronda, máximo 3) que siguen el ciclo normal de código y revisión; después se vuelve a probar la HU.
- [ADR-0062](decisiones/0062-descomposicion-no-acepta-resultados-vacios.md) — skill 05: una HU sin paquetes no se da por buena; se reintenta hasta 3 veces y
  luego falla con un error claro (defecto hallado en el piloto de la tesis).
- [ADR-0063](decisiones/0063-el-esqueleto-deja-el-aplicativo-desplegable-antes-de-las-hus.md) — la arquitectura declara el despliegue, el esqueleto deja el
  aplicativo desplegable (Dockerfile de producción y CI) y las HUs dependen de él; el release avisa si falta el Dockerfile.
- [ADR-0064](decisiones/0064-responder-y-resolver-las-observaciones-al-corregir-un-pr.md) — skill 07: al corregir un PR se responde cada observación con lo que
  se cambió (según el diff) y se resuelven las conversaciones de las corregidas.
- [ADR-0065](decisiones/0065-agregar-hus-por-etapas-con-historial-de-versiones.md) — HUs por etapas: estado por HU visible, aviso de arquitectura desactualizada,
  esqueleto con avance protegido al re-descomponer e historial de versiones de spec y casos de prueba en Mongo.
- [ADR-0066](decisiones/0066-propagar-los-cambios-de-hu-a-casos-de-prueba-codigo-y-smoke.md) — un cambio de especificación o de casos de prueba se propaga como aviso
  a casos, código y smoke testing (versión funcional de los casos por paquete y corrida); la regresión se niega con casos cambiados.
- [ADR-0067](decisiones/0067-paquetes-de-cambio-cuando-cambian-los-casos-de-prueba.md) — paquetes de cambio: llevan el código y sus pruebas a los casos que cambiaron
  (mismo ciclo que un fix) y la arquitectura avisa cuando cambia la especificación de una HU.
- [ADR-0068](decisiones/0068-registro-de-rondas-de-revision-y-correccion-como-evidencia.md) — cada ronda de revisión y de corrección se guarda (observaciones, respuestas,
  commit, valoración humana) y se exporta a CSV como evidencia de la tesis.
- [ADR-0069](decisiones/0069-segunda-opinion-de-la-ia-sobre-las-observaciones-de-la-revision.md) — segunda opinión de la IA (idealmente independiente de quien revisó) sobre
  cada observación, contra el diff de esa revisión; historial de revisión rediseñado.
- [ADR-0070](decisiones/0070-compuerta-de-compilacion-antes-de-abrir-o-corregir-un-pr.md) — compuerta de compilación en un contenedor antes de subir código o su corrección; si
  falla se devuelve el error al agente y, si no se logra, el PR lleva la advertencia y la revisión la marca como bloqueante.
- [ADR-0071](decisiones/0071-el-release-crea-cloud-sql-secretos-y-variables-y-registra-los-fallos-de-arranque.md) — el release crea Cloud SQL, secretos y variables, resuelve
  las URL antes de desplegar y deja registrados los fallos de arranque del código generado.
- [ADR-0072](decisiones/0072-release-automatico-al-aceptar-un-pr.md) — opción por proyecto: aceptar un PR desde Loom lanza el release en segundo plano (una corrida a la vez).
- [ADR-0073](decisiones/0073-resultados-de-smoke-e-incidencias-visibles-en-las-hus.md) — el informe de smoke con iconos y porcentajes; «Ver HUs» y el detalle muestran resultados de smoke e incidencias (fixes).
- [ADR-0074](decisiones/0074-avanzar-con-una-hu-de-punta-a-punta.md) — «Avanzar con esta HU»: confirmación con rondas de corrección y avance por paquete (generar, revisar, corregir, fusionar) hasta completar la HU; al final se lanza el release.
- [ADR-0075](decisiones/0075-rediseno-de-la-interfaz-como-consola-de-desarrollo.md) — la interfaz pasa a una consola de desarrollo oscura con la paleta Novex, tokens compartidos con PrimeNG y estados con icono.
- [ADR-0076](decisiones/0076-no-fusionar-ni-avanzar-con-la-integracion-continua-en-rojo.md) — no se fusiona ni se avanza al siguiente paquete con los checks de GitHub en rojo o sin terminar.
- [ADR-0077](decisiones/0077-decisiones-sobre-los-supuestos-de-una-hu.md) — la persona confirma los supuestos de una HU en «Decisiones pendientes»; la revisión deja de bloquear y el agente recibe la decisión como requisito.
- [ADR-0078](decisiones/0078-corregir-con-el-log-de-la-integracion-continua.md) — si el CI falla al avanzar, se devuelve el log del check al agente como una ronda de corrección (hasta 2 por paquete).
- [ADR-0079](decisiones/0079-lint-y-pruebas-antes-de-subir-el-codigo.md) — la compuerta de compilación corre también lint y pruebas unitarias antes de subir el código.
- [ADR-0080](decisiones/0080-actividad-en-curso-visible-desde-cualquier-sesion.md) — el panel de actividad muestra lo que corre en el servidor aunque lo haya lanzado otra sesión.
- [ADR-0081](decisiones/0081-despliegue-automatico-con-github-actions-y-workload-identity-federation.md) — el despliegue se dispara con GitHub Actions + Workload Identity Federation que `release.py` configura solo; alcance por proveedor (GitLab a futuro).
- [ADR-0082](decisiones/0082-release-lanzado-desde-loom-en-github-actions.md) — Loom lanza el workflow de release en GitHub Actions cuando una HU queda completa; los PR de despliegue se aceptan desde Loom.
- [ADR-0083](decisiones/0083-procesos-concurrentes-con-reglas-de-exclusion.md) — propuesta: varios procesos a la vez con reglas de exclusión y el release exclusivo.
- [ADR-0084](decisiones/0084-historial-de-procesos-y-cancelacion.md) — los procesos se guardan en Mongo (cuándo empezó, cuándo terminó, cómo) y se pueden cancelar, deteniendo también sus procesos externos.
- [ADR-0085](decisiones/0085-proveedor-wif-compartido-entre-proyectos.md) — el proveedor de Workload Identity es uno por proyecto de GCP y acumula los repositorios de todos los Proyectos que despliegan ahí.

## Problema

Los enfoques actuales de asistencia por IA en el ciclo de desarrollo suelen automatizar una sola etapa
aislada (solo revisión, o solo generación de pruebas), asumen implícitamente un proyecto nuevo, y operan
sobre código ya escrito sin partir de la intención de negocio ni cerrar el ciclo hasta la validación
funcional real. Falta un flujo que, a partir de una historia de usuario, cubra de punta a punta:
generación de casos de prueba, diagnóstico de qué ya está hecho, diseño, desarrollo, revisión de código,
integración y validación funcional contra un ambiente real — de forma agnóstica al sistema sobre el que
se aplique, y sin asumir que se arranca de cero.

## Objetivo general

Diseñar e implementar un sistema de skills de IA que, a partir de una historia de usuario, orqueste todo
el ciclo de desarrollo de una funcionalidad — generación de casos de prueba, diagnóstico de avance
existente, diseño de arquitectura, descomposición en paquetes de trabajo, generación de código, revisión de
código, integración y validación funcional mediante smoke tests — de forma generalizable a distintos
repositorios y sistemas, ya sea que el proyecto arranque desde cero o ya tenga avance previo.

## Objetivos específicos

1. Diseñar el modelo de configuración de **Proyecto** (tipo de proyecto — solo web por ahora —, repos y
   ambiente de desarrollo) y el mecanismo de lectura de elementos del backlog desde una fuente pluggable
   (Jira, Markdown o GitHub), clasificando cada uno como HU o Actividad. *(ADR-0009, ADR-0026)*
2. Diseñar el mecanismo de análisis de una HU y sus criterios de aceptación para generar casos de
   prueba (TCs) derivados de ellos, documentado como `spec.md`/`test-cases.md` (SDD). *(ADR-0004,
   ADR-0008)*
3. Diseñar el mecanismo de diagnóstico de avance existente: ejecutar los TCs generados contra el estado
   actual del código/ambiente antes de diseñar, para distinguir qué ya está cubierto de lo que falta.
   *(ADR-0007)*
4. Diseñar el mecanismo de diseño de arquitectura y descomposición en paquetes de trabajo a partir de los TCs que
   el diagnóstico marcó como pendientes — respetando y extendiendo lo que ya existe, documentado como
   `plan.md`/`tasks.md` (SDD). *(ADR-0004, ADR-0007, ADR-0008)*
5. Implementar el skill de generación de código por paquete de trabajo y de apertura de Pull Requests. *(ADR-0004)*
6. Implementar el skill de revisión de código y el ciclo de aplicación de observaciones hasta que un PR
   queda sin pendientes. *(ADR-0004)*
7. Implementar el skill de ejecución de TCs (Playwright, Python) contra un ambiente de desarrollo
   configurado, reutilizado tanto para el diagnóstico inicial como para el smoke testing final, con
   evidencia como salida. *(ADR-0005, ADR-0006, ADR-0007)*
8. Diseñar el mecanismo de fallo → paquete de trabajo de fix, que reintroduce el ciclo de generación y revisión
   de código hasta que los TCs correspondientes pasan. *(ADR-0004)*
9. Diseñar (sin necesidad de desplegar ni operar como servicio persistente) el mecanismo de indexación
   multi-repositorio que da contexto de código a los skills anteriores. *(ADR-0002)*
10. Validar el sistema completo ejecutándolo sobre al menos 2-3 proyectos tipo web de dominios
    distintos — incluyendo al menos un caso greenfield y uno con avance previo, y variando la fuente de
    HUs (Jira, Markdown y GitHub) — cada uno con su propia configuración. *(ADR-0002, ADR-0005, ADR-0007,
    ADR-0009)*
11. Medir, por HU procesada: tasa de TCs generados que efectivamente cubren los criterios de aceptación,
    proporción de criterios ya cubiertos detectada correctamente en el diagnóstico inicial, número de
    rondas de revisión de código hasta aprobación, tasa de éxito de smoke tests por iteración, y grado
    de generalización del sistema entre proyectos y fuentes de HU distintas.

## Alcance vigente

**Dentro de alcance:**
- Alta de un **Proyecto** tipo web, con su fuente de HUs configurada (Jira, Markdown o GitHub), su
  configuración de repos/ambiente, y su **modo de arranque** (`nuevo` / `con_arquitectura` / `avanzado`).
  *(ADR-0009, ADR-0010, ADR-0014)*
- Ejecución selectiva por fase bajo demanda (p. ej. solo revisión de código, o solo smoke testing, sobre
  HUs/paquetes de trabajo ya existentes), no solo el flujo secuencial completo. *(ADR-0014)*
- Cuenta de desarrollo declarada explícitamente por Proyecto, y gate opcional de revisión manual antes
  de merge con lista de usuarios autorizados a aprobar. *(ADR-0013, ADR-0015)*
- Recorrido de la fuente configurada para descubrir elementos del backlog, clasificados como HU o
  Actividad (ADR-0026); las Actividades siguen un pipeline reducido, sin TCs ni smoke testing.
- Lectura de una HU con criterios de aceptación y generación de TCs a partir de ellos, documentado como
  `spec.md`/`test-cases.md`. *(ADR-0008)*
- Prototipo opcional entregado junto con la HU, usado para generar TCs completos y una descomposición
  sin huecos entre back y front. *(ADR-0027)*
- Diagnóstico de avance existente: correr los TCs contra el código/ambiente actual antes de diseñar,
  para soportar tanto proyectos nuevos (greenfield) como proyectos con avance previo (brownfield).
- Diseño de arquitectura y descomposición en paquetes de trabajo para esa HU, a partir de lo que el diagnóstico
  marca como pendiente, documentado como `plan.md`/`tasks.md`.
- Creación de paquetes de trabajo en la plataforma de origen vía MCP cuando la fuente lo soporta (Jira, GitHub);
  control interno siempre presente en el repo de control, con o sin esa sincronización. *(ADR-0024)*
- Generación de código por paquete de trabajo y apertura de PRs.
- Revisión de código automatizada, con ciclo de aplicación de observaciones hasta PR limpio.
- Smoke testing con Playwright (Python) contra un ambiente de desarrollo ya desplegado (externo al
  proyecto), a partir de los TCs generados, con evidencia como salida.
- Generación de paquetes de trabajo de fix ante TCs fallidos, reentrando al ciclo de código/revisión.
- Documentación del proceso en Markdown con front-matter, por HU, versionada en git. *(ADR-0008)*
- Plataforma de visualización (log/timeline de avance por HU) y reportes agregados, de solo lectura
  sobre la documentación que las skills ya escriben. *(ADR-0012)*
- Documentación por HU centralizada en un repositorio de control por Proyecto. *(ADR-0012)*
- Diseño (no despliegue) de un mecanismo de indexación multi-repositorio como soporte de contexto.
- Validación en 2-3 proyectos de dominios distintos (candidatos: proyectos propios ya públicos en
  GitHub; opcionalmente uno de un empleador, sujeto a autorización).

**Fuera de alcance:**
- Reemplazar por completo la revisión humana — el sistema asiste; una persona sigue pudiendo intervenir
  en cualquier fase.
- Optimizar para un lenguaje, framework o stack único; el objetivo es generalizar el enfoque.
- Desplegar y operar infraestructura de indexación multi-repositorio como servicio persistente/productivo
  del propio proyecto de tesis *(ADR-0002)*.
- Desplegar o administrar el ambiente de desarrollo usado para smoke testing — se asume ya existente y
  configurado por quien use el sistema *(ADR-0005)*.
- Tipos de proyecto distintos a **web** (API, mobile, otros) — el campo se diseña extensible, pero no
  se implementa ni valida en esta tesis. *(ADR-0009)*
- Fuentes de HUs distintas a Jira, Markdown y GitHub — el mecanismo se diseña pluggable, pero solo se
  implementan estas tres. *(ADR-0009, ADR-0010)*

## Qué falta decidir

Esta sección se vacía a medida que las decisiones se documentan como ADRs en
[`decisiones/`](decisiones/). Pendientes:

- ~~Qué framework de agentes implementa el orquestador y las skills~~ — resuelto en
  [ADR-0018](decisiones/0018-framework-de-agentes-e-indexacion-de-codigo.md): Claude Code Skills,
  invocado de forma headless.
- ~~Cómo se representa e indexa el código de un repositorio~~ — resuelto en ADR-0018: sin índice
  persistente, análisis bajo demanda con grep/glob y lectura directa.
- ~~Esquema/formato exacto de la configuración de Proyecto~~ — resuelto en
  [ADR-0017](decisiones/0017-esquema-de-configuracion-de-proyecto.md): esquema consolidado con todos
  los campos (repos/ambiente, fuente de HUs, repo de control, cuenta de desarrollo, modo de arranque,
  revisión manual, cuentas de prueba, arquitectura base).
- ~~Cómo se declara/valida el modo de arranque~~ — resuelto en ADR-0017: se declara explícito, sin
  validar contra el estado real del repo (el diagnóstico de ADR-0007 ya tolera la discrepancia).
- ~~Si el repositorio de control se declara explícito o se crea por default~~ — resuelto en ADR-0017:
  explícito y obligatorio, igual que los repos objetivo; para la implementación actual, ADR-0035
  reemplaza esto por una carpeta local estática, ninguna de las dos.
- ~~Formato de la arquitectura ya definida en modo `con_arquitectura`~~ — resuelto en ADR-0017: el
  mismo formato SDD (`plan.md`) que produce la skill 04 en modo fundacional, no un formato nuevo.
- Mecanismo de reconstrucción de `spec.md`/`plan.md`/`tasks.md` para HUs/código preexistentes en modo
  `avanzado` — sigue pendiente, ADR-0017 no lo resuelve (es un mecanismo, no parte del esquema).
- ~~Orden/paralelismo de paquetes de trabajo con `depende_de`~~ — resuelto en
  [ADR-0029](decisiones/0029-orden-secuencial-de-paquetes-de-trabajo-dependientes.md): secuencial
  estricto entre repos dependientes.
- ~~Si el orquestador procesa una HU a la vez o puede paralelizar~~ — resuelto en
  [ADR-0030](decisiones/0030-paralelismo-entre-hus-con-dependencias.md): paralelo entre HUs salvo
  dependencia declarada.
- ~~Si un supuesto sin resolver fuerza revisión manual automáticamente~~ — resuelto en
  [ADR-0028](decisiones/0028-ciclo-automatizado-de-calidad-como-mecanismo-suficiente.md): no se fuerza;
  el ciclo automatizado de revisión ya documenta y controla el supuesto (ADR-0011).
- ~~Dónde se administra la lista de aprobadores~~ — resuelto: desde la plataforma de Telar (ADR-0012,
  ADR-0015). Sigue abierto si aplica a nivel Proyecto completo o se puede afinar por repositorio/tipo
  de paquete de trabajo.
- ~~Diseño concreto del adaptador de lectura Jira / Markdown~~ — el contrato común que deben cumplir
  quedó resuelto en [ADR-0019](decisiones/0019-contrato-comun-de-adaptadores-de-fuente-de-hus.md); la
  implementación de cada adaptador (mapeo exacto de campos) sigue pendiente como trabajo de código.
- ~~Vocabulario para distinguir elementos de la fuente de lo que el sistema genera~~ — resuelto en
  [ADR-0026](decisiones/0026-vocabulario-unificado-hu-actividad-paquete-de-trabajo.md): "elemento del
  backlog" (fuente) vs. "paquete de trabajo" (generado por la skill de descomposición) — ya no
  comparten palabra.
- ~~Qué subconjunto de TCs se vuelve a correr tras un fix~~ — resuelto en
  [ADR-0020](decisiones/0020-smoke-testing-corre-todos-los-tcs-como-regresion.md): todos los TCs de la
  HU, versionando cada corrida como historial de regresión.
- ~~Qué hacer con TCs del diagnóstico inicial que no se pueden evaluar de forma aislada~~ — resuelto en
  [ADR-0027](decisiones/0027-prototipo-como-input-complementario.md): el diagnóstico no necesita
  distinguir la causa; la descomposición (informada por el prototipo, si existe) cubre ambas capas por
  construcción.
- ~~Regla exacta de "no aprobar un PR con supuestos sin resolver"~~ — resuelto en
  `skills/07-revision-de-codigo.md`: el supuesto genera una observación bloqueante explícita, separada
  de sugerencias menores.
- ~~Convención de nombre de rama~~ — resuelto en
  [ADR-0021](decisiones/0021-convencion-de-nombre-de-rama-basada-en-id-fuente.md):
  `hu/{id_fuente}/{paquete_id}`. Sigue abierto cómo se coordinan en la práctica paquetes de trabajo
  relacionados que tocan repos distintos con dependencia entre sí. *(pendiente de la skill de
  generación de código)*
- ~~Qué pasa si el enfoque de diseño de `plan.md` requiere un repositorio fuera de configuración~~ —
  resuelto en [ADR-0022](decisiones/0022-repos-fuera-de-configuracion-o-de-alcance.md).
- Qué tan grande puede ser un paquete de trabajo antes de que deba partirse más (criterio de "tamaño de
  PR razonable").

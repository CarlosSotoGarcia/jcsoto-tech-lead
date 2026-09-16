# ADR-0031: Stack tecnológico de la plataforma Loom

## Estado

Aceptada.

## Contexto

La [especificación de la plataforma](../especificacion-plataforma-telar.md) (ADR-0012, ADR-0015,
ADR-0017, ADR-0022) define **qué** debe soportar la plataforma, pero no con qué tecnología se
construye. Antes de empezar a armarla hace falta fijar el stack, igual que ya se hizo para el
framework de agentes de las skills (ADR-0018).

## Decisión

La plataforma Loom se construye como un **monorepo** con una parte backend y una parte frontend:

- **Backend**: Python, con **Pydantic** para modelado y validación de datos (esquemas de
  configuración de Proyecto, entidades de estado, contratos de API).
- **Base de datos**: **MongoDB**, accedida mediante un driver **compatible con Firestore de GCP** —
  la capa de acceso a datos se escribe contra una interfaz que ambos backends pueden satisfacer, para
  no atar la plataforma a un motor específico.
- **Frontend**: **Angular**.

## Consecuencias

- El repositorio de la plataforma es independiente del repositorio de control de cada Proyecto
  (ADR-0012) y de los repositorios objetivo (ADR-0005) — es el propio código fuente de Loom, no
  documentación SDD ni código generado.
- Los modelos Pydantic del backend son el punto natural para expresar el esquema de configuración
  consolidado de Proyecto (ADR-0017).
- Al mantener la capa de datos compatible con Firestore desde el inicio, cambiar de MongoDB a
  Firestore (o viceversa) más adelante no debería requerir rediseñar el resto del backend — solo la
  implementación concreta del driver.
- Queda pendiente (detalle de implementación, no bloquea el diseño): estructura exacta de carpetas del
  monorepo, framework de API (p. ej. FastAPI, dado que ya se usa Pydantic), y librería de componentes
  Angular si aplica.

## Aclaración — Autenticación

La plataforma requiere **login** para los actores que la usan (Administrador de Proyecto, Aprobador
autorizado, Observador — ver especificación de la plataforma, sección 2). Es especialmente
indispensable cuando `requiere_revision_manual` está activo (ADR-0015): el sistema necesita saber
**quién** está aprobando un PR, no solo que "alguien" lo aprobó, para poder verificar que la persona
pertenece a `usuarios_autorizados_a_aprobar`. Mecanismo concreto de autenticación (proveedor propio,
OAuth con GitHub/Google, SSO corporativo) queda como pendiente de implementación.

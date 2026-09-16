# Especificación técnica — Plataforma Telar

> Este documento especifica **la plataforma** (la aplicación que da de alta Proyectos, muestra avance y
> administra configuración) — no la lógica interna de las 9 skills ni el orquestador, que ya están
> especificados en detalle en [`skills/`](skills/). Aquí se consolida, en un solo lugar y en forma de
> requisitos trazables, todo lo que las decisiones de arquitectura (ADRs) ya establecieron que la
> plataforma debe hacer, para poder construirla.

## 1. Resumen

**Telar** es un orquestador y un conjunto de skills que, a partir de una historia de usuario (HU),
automatizan la generación de pruebas, el diseño, la generación de código, la revisión y la validación
funcional (ver [`00-vision-general.md`](00-vision-general.md)). **La plataforma** es la pieza con la
que una persona interactúa: da de alta los Proyectos sobre los que Telar va a operar, configura cómo
opera cada uno, y muestra qué está pasando y qué requiere su atención — sin ejecutar ella misma ninguna
fase del pipeline (eso es trabajo del orquestador y las skills).

## 1.1 Stack tecnológico (ADR-0031)

Loom se construye como **monorepo** con backend y frontend separados:

| Capa | Tecnología |
|---|---|
| Backend | Python + Pydantic |
| Base de datos | MongoDB, con driver compatible con Firestore de GCP |
| Frontend | Angular |

## 2. Actores

| Actor | Qué hace en la plataforma |
|---|---|
| **Administrador de Proyecto** | Da de alta un Proyecto y su configuración completa; la actualiza cuando cambian las necesidades (p. ej. activar/desactivar revisión manual, ADR-0015). |
| **Aprobador autorizado** | Da el visto bueno final a un PR cuando el Proyecto exige revisión manual (ADR-0015). |
| **Observador** | Consulta el avance de HUs y los reportes agregados, sin permisos de configuración. |
| **Orquestador (actor automatizado)** | Lee y escribe el estado de HUs/paquetes de trabajo en el repositorio de control; es quien realmente "usa" la configuración que la plataforma expone — no es un usuario humano, pero es el consumidor principal de lo que la plataforma gestiona. |

## 3. Requisitos funcionales

### 3.0 Autenticación (ADR-0015, ADR-0031)

- **RF-00**: Todo actor humano (Administrador de Proyecto, Aprobador autorizado, Observador) debe
  iniciar sesión para usar la plataforma — no hay acceso anónimo.
- **RF-00b**: El login es **obligatorio** para aprobar un PR cuando `requiere_revision_manual` está
  activo (ADR-0015): la plataforma debe poder verificar que la persona autenticada pertenece a
  `usuarios_autorizados_a_aprobar` antes de registrar la aprobación. Sin esta verificación de
  identidad, la aprobación no queda válida.
- **RF-00c**: Consultar avance/reportes (rol Observador) también requiere sesión iniciada, aunque no
  tenga permisos de configuración — la plataforma no expone estado de Proyectos sin autenticación.

### 3.1 Gestión de Proyectos (ADR-0009, ADR-0014, ADR-0017)

- **RF-01**: Dar de alta un Proyecto capturando: nombre, tipo (`web`, único soportado — ADR-0009), y
  modo de arranque (`nuevo` / `con_arquitectura` / `avanzado` — ADR-0014).
- **RF-02**: Registrar los repositorios objetivo del Proyecto (N backend/frontend), cada uno con tipo,
  URL y rama base (ADR-0005).
- **RF-03**: Registrar la URL del ambiente de desarrollo del Proyecto (ADR-0005).
- **RF-04**: Registrar el repositorio de control del Proyecto — explícito, obligatorio, no se crea por
  default (ADR-0012, ADR-0017).
- **RF-05**: Registrar la credencial de la cuenta de desarrollo dedicada, como referencia a un secreto
  gestionado aparte — nunca en texto plano (ADR-0013, ADR-0017).
- **RF-06**: Si el modo de arranque es `con_arquitectura`, permitir aportar la referencia a un `plan.md`
  ya escrito que sirva como arquitectura base (ADR-0014, ADR-0017).
- **RF-07**: Editar la configuración de un Proyecto existente después de darlo de alta (p. ej. alternar
  `requiere_revision_manual` sin tener que recrear el Proyecto — ADR-0015).

### 3.2 Fuente de historias de usuario (ADR-0009, ADR-0010, ADR-0019)

- **RF-08**: Configurar la fuente de HUs del Proyecto: `jira`, `markdown` o `github`, con los parámetros
  de conexión propios de cada tipo (proyecto de Jira; ubicación de archivos Markdown; repositorio de
  GitHub).
- **RF-09**: Para fuente `github`, indicar si la jerarquía de trabajo se resuelve por sub-issues nativos
  o por convención de labels/milestones (ADR-0010).

### 3.3 Cuentas de prueba y revisión manual (ADR-0015, ADR-0016)

- **RF-10**: Registrar una cuenta de prueba por cada rol relevante de la aplicación bajo evaluación
  (p. ej. `admin`, `usuario_final`, `invitado`), como referencia a secretos gestionados aparte.
- **RF-11**: Activar o desactivar `requiere_revision_manual` para el Proyecto, en cualquier momento —
  no es una decisión fija al dar de alta el Proyecto.
- **RF-12**: Administrar la lista de usuarios autorizados a aprobar PRs cuando `requiere_revision_manual`
  está activo — agregar, quitar personas.
- **RF-13**: Notificar (o al menos mostrar de forma visible) a los usuarios autorizados cuando un PR
  está esperando su aprobación.

### 3.4 Visualización de avance (ADR-0012)

- **RF-14**: Mostrar, por HU, un log/timeline de las transiciones de fase — leído del front-matter de
  los archivos SDD y de su historial en `git log` sobre el repositorio de control (ADR-0008, ADR-0012).
  La plataforma es de **solo lectura** respecto a este estado: nunca dispara una fase directamente.
- **RF-15**: Mostrar el estado de cada paquete de trabajo dentro de una HU: `pendiente`, `en_revision`,
  `fusionado` o `completo`, con su PR vinculado si existe (ADR-0008, ADR-0023).
- **RF-16**: Mostrar el historial de corridas de smoke testing de una HU (evidencia versionada,
  ADR-0020) — qué TCs pasaron o fallaron en cada corrida, para que sirva de historial de regresión.

### 3.5 Reportes agregados (ADR-0012)

- **RF-17**: Generar reportes por Proyecto con las métricas del objetivo 11 de
  [`00-vision-general.md`](00-vision-general.md): tasa de TCs generados que cubren los criterios de
  aceptación, proporción de criterios ya cubiertos detectada en el diagnóstico inicial, número de
  rondas de revisión de código hasta aprobación, tasa de éxito de smoke tests por iteración, y grado de
  generalización entre Proyectos y fuentes de HU.
- **RF-18**: Distinguir, en los reportes, trabajo generado por el sistema (autoría de la cuenta de
  desarrollo, ADR-0013) de cualquier otro cambio en el mismo repositorio.

### 3.6 Resolución de decisiones pendientes (ADR-0022)

- **RF-19**: Mostrar, de forma visible, cuando una HU queda con un paquete de trabajo marcado
  "pendiente de definir" por requerir un repositorio fuera de la configuración del Proyecto — sin
  bloquear el resto del avance de esa HU.
- **RF-20**: Cuando una HU queda marcada "fuera de alcance" (por requerir un tipo de sistema que Telar
  no soporta), presentar al usuario la decisión explícita: **continuar** (Telar sigue con lo que sí
  puede hacer) o **no continuar** (pausar el procesamiento de esa HU).

### 3.7 Sincronización con la fuente (ADR-0024)

- **RF-21**: Cuando la creación de un paquete de trabajo en la plataforma de origen (Jira/GitHub, vía
  MCP) falla, mostrar un reporte de la falla con la opción explícita de **reintentar** la creación desde
  la plataforma — sin que esto bloquee el control interno del paquete.

## 4. Requisitos no funcionales

- **RNF-01**: La plataforma no ejecuta fases del pipeline ni sustituye al orquestador (ADR-0012) — su
  responsabilidad es configuración, visualización y presentación de decisiones pendientes.
- **RNF-02**: Ninguna credencial (cuenta de desarrollo, cuentas de prueba) se almacena en texto plano en
  la configuración — siempre como referencia a un secreto gestionado aparte (ADR-0017).
- **RNF-03**: La plataforma no requiere infraestructura de indexación de código propia — el análisis de
  código lo hacen las skills bajo demanda (ADR-0002, ADR-0018), la plataforma no lo replica.
- **RNF-04**: Todo lo que la plataforma muestra debe poder reconstruirse leyendo el repositorio de
  control (ADR-0012) — no debe existir un estado que solo viva en la plataforma y en ningún otro lado.

## 5. Fuera de alcance de la plataforma

- Ejecutar o disparar directamente cualquiera de las 9 skills o el orquestador (RNF-01).
- Dar soporte a tipos de proyecto distintos a `web`, o fuentes de HU distintas a Jira/Markdown/GitHub
  (ADR-0009, ADR-0010) — el diseño es extensible, pero no se implementa en esta tesis.
- Reemplazar la revisión humana — solo la hace opcional u obligatoria según configuración (ADR-0015).

## 6. Trazabilidad

| Requisito | ADR(s) |
|---|---|
| RF-00, RF-00b, RF-00c | ADR-0015, ADR-0031 |
| RF-01 a RF-07 | ADR-0009, ADR-0013, ADR-0014, ADR-0017 |
| RF-08, RF-09 | ADR-0009, ADR-0010, ADR-0019 |
| RF-10 a RF-13 | ADR-0015, ADR-0016 |
| RF-14 a RF-16 | ADR-0008, ADR-0012, ADR-0020, ADR-0023 |
| RF-17, RF-18 | ADR-0012, ADR-0013 |
| RF-19, RF-20 | ADR-0022 |
| RF-21 | ADR-0024 |

## 7. Pendiente

Esta especificación cubre lo que ya está decidido. Lo que sigue pendiente en `00-vision-general.md`
(formato de serialización de la configuración, mecanismo de notificación a aprobadores, mecanismo
concreto de autenticación — proveedor propio, OAuth, SSO — ADR-0031, etc.) es trabajo de diseño de
detalle/implementación, no de esta especificación funcional.

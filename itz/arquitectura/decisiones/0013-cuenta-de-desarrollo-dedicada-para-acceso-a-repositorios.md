# ADR-0013: Acceso a repositorios mediante una cuenta de desarrollo dedicada, no personal

## Estado

Aceptada

## Contexto

La skill de generación de código necesita crear ramas, hacer commits, hacer push y abrir Pull Requests
en los repositorios objetivo configurados por Proyecto (ADR-0005). Hace falta decidir con qué identidad
git/plataforma realiza esas operaciones.

## Decisión

El sistema opera sobre los repositorios objetivo con una **cuenta de desarrollo dedicada** (una cuenta
de servicio/bot), configurada por Proyecto, con permisos de escritura acotados a los repos que ese
Proyecto declara (ADR-0005) — **no** se usan las credenciales personales del usuario que da de alta el
Proyecto ni las de quien lo opera.

Todo commit y todo PR que el sistema genera queda registrado bajo esa identidad, de forma que sea
identificable de inmediato como generado por el sistema y no por una persona.

## Consecuencias

- La configuración de Proyecto (ADR-0009) gana otro campo: la credencial de la cuenta de desarrollo
  (token/llave, sin comprometer aquí un mecanismo concreto — sigue siendo diseño, no implementación).
- Principio de mínimo privilegio: esa credencial solo debe poder escribir en los repositorios
  configurados de ese Proyecto, no en cualquier repositorio accesible por la cuenta.
- Los PRs y commits generados por el sistema quedan distinguibles de trabajo humano por autoría — esto
  es lo que permite que la plataforma de reportes (ADR-0012) separe métricas de "código generado por el
  sistema" de cualquier otro cambio en el mismo repositorio.
- Refuerza ADR-0011: como el autor del commit/PR es la cuenta de desarrollo, un supuesto sin resolver
  documentado en la descripción del PR es inequívocamente responsabilidad del sistema, no de una
  persona que "debió haber preguntado".
- Pendiente: mecanismo concreto de la credencial (token de acceso personal de una cuenta de bot, GitHub
  App, llave SSH dedicada, etc.) y cómo se rota/revoca — decisión de implementación, no de esta tesis
  en su fase de documentación.
- Pendiente: qué pasa si la cuenta de desarrollo no tiene permisos suficientes sobre un repositorio
  configurado (detección temprana al dar de alta el Proyecto, o falla en el primer intento de push).

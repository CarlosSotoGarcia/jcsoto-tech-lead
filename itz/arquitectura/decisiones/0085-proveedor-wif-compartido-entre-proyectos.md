# ADR-0085: Proveedor de Workload Identity compartido entre Proyectos del mismo proyecto de GCP

## Estado

Aceptada. Corrige el alcance del despliegue automático con GitHub Actions ([ADR-0081](0081-despliegue-automatico-con-github-actions-y-workload-identity-federation.md), [ADR-0082](0082-release-lanzado-desde-loom-en-github-actions.md)).

## Contexto

`release.py` crea un pool (`loom-github`) y un proveedor OIDC (`github`) con nombres fijos, y restringe el proveedor con `assertion.repository=='<dueño>/<repo>'`. Si el proveedor ya existía, el script no lo tocaba. Al configurar un segundo Proyecto en el mismo proyecto de GCP (el piloto E3c de ITZ Agenda Taller, repositorio `loom-piloto-e3c-claude-cli`), su workflow de GitHub Actions habría sido rechazado al autenticarse: la condición solo aceptaba el repositorio del primer Proyecto (E1c). El error solo aparecería en la Fase 4, después de toda la generación de código.

## Decisión

1. **Un solo pool y un solo proveedor por proyecto de GCP**, compartidos por todos los Proyectos de Loom que despliegan ahí. No se crea un proveedor por repositorio.
2. **La condición del proveedor acumula repositorios.** Al preparar la identidad federada, `release.py` lee la condición actual; si el repositorio del Proyecto no aparece, la reemplaza por `<condición actual> || assertion.repository=='<dueño>/<repo>'` con `update-oidc`. Nunca quita repositorios.
3. **El permiso sigue siendo por repositorio.** Cada repositorio recibe su propio `roles/iam.workloadIdentityUser` sobre la cuenta desplegadora mediante `principalSet://…/attribute.repository/<dueño>/<repo>`, como antes.
4. Como el resto de la preparación de identidad, esto solo corre fuera de GitHub Actions (con la sesión de `gcloud` de quien ejecuta el release), porque modificar el proveedor requiere permisos de administración que la cuenta desplegadora no tiene.

## Consecuencias

- Aplicado el 2026-09-26 al configurar E3c: la condición pasó de `assertion.repository=='CarlosSotoGarcia/loom-piloto-e1c-claude-cli'` a esa misma regla `|| assertion.repository=='CarlosSotoGarcia/loom-piloto-e3c-claude-cli'`; el repositorio nuevo recibió su permiso y las variables `GCP_WORKLOAD_IDENTITY_PROVIDER` y `GCP_SERVICE_ACCOUNT`. Una segunda ejecución no cambia nada (la regla ya está).
- La condición crece con cada repositorio. Un Proyecto borrado deja su regla; quitarla es un paso manual.
- Todos los repositorios aceptados comparten la misma cuenta desplegadora y, por lo tanto, los mismos permisos sobre el proyecto de GCP. Es aceptable para los pilotos de la tesis; en un uso real convendría una cuenta desplegadora por Proyecto.

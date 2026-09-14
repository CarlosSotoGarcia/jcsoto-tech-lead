# ADR-0017: Esquema de configuración de Proyecto

## Estado

Aceptada. Consolida en un solo lugar los campos de configuración ya decididos por separado en
ADR-0005, ADR-0009, ADR-0010, ADR-0012, ADR-0013, ADR-0014, ADR-0015 y ADR-0016, y resuelve tres
pendientes que quedaban sueltos.

## Contexto

La configuración de "Proyecto" fue creciendo un campo a la vez a lo largo de varios ADRs, sin un lugar
único que mostrara la forma completa. Además quedaban tres preguntas sin resolver: cómo se declara/
valida el modo de arranque, si el repositorio de control se declara explícito o se crea por default, y
en qué formato se aporta una arquitectura ya definida (modo `con_arquitectura`).

## Decisión

**Esquema consolidado** (ilustrativo — el formato de serialización exacto, YAML/JSON/UI, es detalle de
implementación):

```yaml
proyecto:
  id: proy-001
  nombre: "Plataforma de gestión residencial"
  tipo: web                       # ADR-0009 — único valor soportado por ahora
  modo_arranque: nuevo            # nuevo | con_arquitectura | avanzado — ADR-0014

  repos:                          # ADR-0005 — N backends/frontends
    - nombre: backend-principal
      tipo: backend
      url: https://github.com/org/backend-principal
      rama_base: develop
    - nombre: frontend-admin
      tipo: frontend
      url: https://github.com/org/frontend-admin
      rama_base: develop

  ambiente_dev:
    url: https://dev.miapp.example.com   # ADR-0005

  fuente_hus:                      # ADR-0009 / ADR-0010
    tipo: github                   # jira | markdown | github
    conexion:
      repo: org/backend-principal
      jerarquia: sub_issues        # sub_issues | labels_milestones (solo github, ADR-0010)

  repo_control:                    # ADR-0012 — explícito y obligatorio, ver Decisión
    url: https://github.com/org/proy-001-control

  cuenta_desarrollo:                # ADR-0013 — explícita y obligatoria
    credencial_ref: secreto://proy-001/dev-account

  revision_manual:                  # ADR-0015 — mutable en el tiempo
    requiere_revision_manual: true
    usuarios_autorizados_a_aprobar:
      - persona.a@ejemplo.com
      - persona.b@ejemplo.com

  cuentas_prueba:                   # ADR-0016 — una por rol relevante, no una genérica
    admin:
      credencial_ref: secreto://proy-001/test-admin
    usuario_final:
      credencial_ref: secreto://proy-001/test-user
    invitado: null                  # sin login

  arquitectura_base:                 # solo si modo_arranque = con_arquitectura
    plan_ref: ./arquitectura-base/plan.md   # mismo formato SDD que produce skill 04 en modo fundacional
```

**Resoluciones puntuales:**

1. **Modo de arranque**: es un campo declarado explícitamente por la persona al dar de alta el
   Proyecto — **no se valida contra el estado real del repositorio**. Si se declara `nuevo` pero el
   repo ya tiene código, el diagnóstico de avance (ADR-0007) simplemente encuentra TCs que ya pasan; el
   mecanismo ya es tolerante a esa discrepancia sin necesitar una validación adicional.
2. **Repositorio de control**: se declara **explícito y obligatorio** al dar de alta el Proyecto — la
   plataforma no crea uno por default. Es consistente con que los repos objetivo (ADR-0005) también se
   declaran explícitos, y evita que el sistema cree repositorios por su cuenta sin que quede claro bajo
   qué organización o con qué permisos.
3. **Arquitectura ya definida** (`arquitectura_base`, modo `con_arquitectura`): se aporta en el
   **mismo formato SDD** que la skill de diseño de arquitectura genera en su modo fundacional (un
   `plan.md`) — no se define un tercer formato. Para el resto del pipeline (a partir de la
   descomposición en subtareas), un `plan.md` es un `plan.md` sin importar si lo escribió una persona o
   el sistema.

## Consecuencias

- Toda referencia a credenciales en la configuración (`credencial_ref`) es una **indirección a un
  secreto gestionado aparte**, nunca el secreto en texto plano dentro de esta configuración — principio
  de seguridad a mantener cuando esto se implemente, aunque el mecanismo concreto de secretos sigue
  siendo detalle de implementación.
- `skills/04-diseno-de-arquitectura.md` (modo fundacional) y `arquitectura_base` quedan como las dos
  únicas fuentes posibles de un `plan.md` a nivel de repositorio — no hay una tercera vía.
- Da un lugar único (este ADR) al que apuntar cuando se agregue un campo de configuración nuevo en el
  futuro, en vez de seguir dispersándolo entre ADRs de temas distintos.

## Pendiente

- Formato de serialización real (YAML/JSON/formulario de UI) — el ejemplo de arriba es ilustrativo, no
  una decisión de formato de archivo.

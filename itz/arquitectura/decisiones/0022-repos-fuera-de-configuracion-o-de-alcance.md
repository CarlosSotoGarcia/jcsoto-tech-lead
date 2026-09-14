# ADR-0022: Repositorios fuera de configuración o fuera de alcance se marcan y se escalan vía la plataforma

## Estado

Aceptada. Cierra un pendiente de `skills/04-diseno-de-arquitectura.md`.

## Contexto

Al diseñar `plan.md` (`skills/04-...md`) para una HU, puede descubrirse que hace falta tocar un
repositorio que no está en la configuración del Proyecto (ADR-0005), o algo más severo: un tipo de
sistema fuera del alcance que Telar soporta (por ahora, solo proyectos `web`, ADR-0009 — p. ej. un
componente tipo API queda fuera de alcance de esta tesis). Sin un tratamiento explícito, el sistema
podría ignorar esa parte del trabajo sin que nadie se entere, o inventar una ubicación arbitraria.

## Decisión

Se distinguen dos casos:

1. **Repo fuera de configuración (recuperable)** — el repo hace falta pero es del mismo tipo de
   sistema, simplemente no está dado de alta en el Proyecto. Se marca explícitamente en `plan.md` como
   pendiente de definir (necesita ampliar la configuración del Proyecto para incluir ese repo). La
   plataforma (Telar, ADR-0012) muestra esto como una señal de "hay algo que resolver" en el
   log/timeline de esa HU — **no bloquea** el resto del trabajo que sí es viable con los repos ya
   configurados.
2. **Fuera de alcance por tipo de sistema (no recuperable solo con configuración)** — lo que se
   necesita no es un repo no listado, es un tipo de sistema que Telar no soporta (ADR-0009). Se marca
   explícitamente como **fuera de alcance**, y la plataforma presenta la decisión a un humano:
   **continuar** (Telar sigue con lo que sí puede hacer, dejando esa parte fuera) o **no continuar**
   (pausar el procesamiento de esa HU).

## Consecuencias

- Ningún caso se resuelve en silencio — ambos generan una señal visible en la plataforma, consistente
  con el principio ya establecido de que una persona puede intervenir en cualquier fase.
- El caso 1 se resuelve ampliando la configuración del Proyecto, sin tocar el alcance de Telar; el caso
  2 es un límite real del sistema (ADR-0009) y requiere una decisión de negocio, no de configuración.
- La plataforma (ADR-0012) gana un tercer rol, además de visualización/reportes y administración de
  configuración (aclarado en ADR-0012/0015 esta misma sesión): **presentar decisiones pendientes** al
  humano cuando el orquestador no puede seguir sin ellas — distinto de aprobar un PR (ADR-0015), que es
  una decisión de calidad de código, no de alcance.

## Pendiente

- Formato exacto del flag en `plan.md` para distinguir un caso del otro (p. ej.
  `bloqueo: repo_no_configurado` vs. `bloqueo: fuera_de_alcance`) y cómo se refleja cada uno en el
  log/timeline de la plataforma.

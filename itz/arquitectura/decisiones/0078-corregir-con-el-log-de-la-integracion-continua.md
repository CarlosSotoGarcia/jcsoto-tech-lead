# ADR-0078: Corregir con el log de la integración continua

## Estado

Aceptada. Amplía el avance por HU ([ADR-0074](0074-avanzar-con-una-hu-de-punta-a-punta.md)) y la regla de no fusionar en rojo ([ADR-0076](0076-no-fusionar-ni-avanzar-con-la-integracion-continua-en-rojo.md)).

## Contexto

Con el ADR-0076, un PR con el CI en rojo detenía el avance de la HU y esperaba a una persona, aunque la causa (una prueba, el lint) estuviera en el log del propio check. En HU-003 el paquete PT-02 se quedó así con dos pruebas de Jest fallidas.

## Decisión

1. **Si el CI falla durante «Avanzar con esta HU», Loom lee el log de los checks fallidos** de GitHub Actions y extrae lo relevante: las líneas que preceden a la marca `##[error]`, donde están la prueba, el compilador o el lint que fallaron.
2. **Ese extracto se registra como observación bloqueante** del paquete (fuente `pruebas`), con la orden de corregir la causa sin debilitar las pruebas, y el agente hace una ronda de corrección con él.
3. **Hasta 2 correcciones por CI por paquete**, aparte de las rondas de la revisión; después se vuelve a esperar el CI. Con 0 rondas, o agotadas las 2, se detiene y deja el PR abierto.

## Consecuencias

- Primer caso real: HU-003/PT-02 pasó de rojo a verde con una corrección basada en el log.
- El primer extractor tomaba la primera línea que parecía un fallo y entregó al agente el registro del `checkout` en lugar del error de PT-03; se cambió a las marcas `##[error]` de Actions. El fallo real era un lint trivial.
- El agente sigue sin ejecutar lint ni pruebas: cada intento gasta una espera de CI (de 2 a 4 minutos). Ejecutarlos en un contenedor antes del push (como ya se hace con la compilación, ADR-0070) evitaría el viaje.

## Pendiente

- Ejecutar lint y pruebas unitarias en contenedor antes del push.
- Leer también los logs de otros proveedores de CI (hoy solo GitHub Actions).

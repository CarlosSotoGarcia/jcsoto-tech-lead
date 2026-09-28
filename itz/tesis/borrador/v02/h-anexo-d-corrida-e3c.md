@@ tesis_anexos+
CAPITULO: D
### Anexo D. Pantallas principales de la corrida piloto E3c

Este anexo reúne las pantallas principales de la corrida E3c (Proyecto de agenda de un taller mecánico, con Claude por CLI), hecha el 26 y 27 de septiembre de 2026 con el mismo procedimiento que la corrida E1c del Anexo C. El recorrido completo, con 602 capturas, la bitácora con la hora de cada hallazgo y los guiones de Playwright que operaron la interfaz, está en `itz/tesis/evidencia/corrida-E3c-2026-09-26/`; aquí solo se muestran las pantallas que sostienen el capítulo 5.

### D.1 Requerimientos, diseño y descomposición

FIGURA: evidencia/corrida-E3c-2026-09-26/capturas/01-proyecto-limpio-ruta-del-proyecto.png | Proyecto E3c sin ninguna fase ejecutada

FIGURA: evidencia/corrida-E3c-2026-09-26/capturas/07-fase2-casos-de-prueba-terminado.png | Casos de prueba generados para las tres HUs del taller (101 en total)

FIGURA: evidencia/corrida-E3c-2026-09-26/capturas/13-fase3-descomposicion-terminado.png | Descomposición en 17 paquetes de trabajo al primer intento

FIGURA: evidencia/corrida-E3c-2026-09-26/capturas/36-fase3-completa-ruta-del-proyecto.png | Fase 3 completa: 17 de 17 paquetes fusionados

### D.2 Corrección con el registro de la integración continua

HU-001/PT-04 fue aprobado por la revisión, pero su integración continua quedó en rojo por una prueba de Vitest. La interfaz no ofrece la corrección para un paquete aprobado; la acción «avanzar HU», llamada por su API, corrigió con el extracto del registro del CI y fusionó el paquete con el CI en verde.

FIGURA: evidencia/corrida-E3c-2026-09-26/capturas/25h-HU-001-PT-04-con-ci-en-rojo.png | HU-001/PT-04 aprobado por la revisión, con la integración continua en rojo

FIGURA: evidencia/corrida-E3c-2026-09-26/capturas/25k-HU-001-avanzar-hu-terminado.png | «Avanzar HU» terminado: corrección con el registro del CI y fusión

### D.3 Despliegue

Las variables de entorno del backend se ajustaron a las que exige el código generado, y el release quedó bien en su tercer lanzamiento manual, después de corregir en Loom la ubicación de los servicios (ADR-0086) y la entrega de la cadena de conexión y de la URL de la API (ADR-0087).

FIGURA: evidencia/corrida-E3c-2026-09-26/capturas/40b-fase4-variables-ajustadas-al-codigo-generado.png | Variables de entorno ajustadas a las que exige el backend generado

FIGURA: evidencia/corrida-E3c-2026-09-26/capturas/39c-fase4-release-terminado.png | Release terminado: backend y frontend desplegados en Cloud Run

### D.4 Pruebas de humo antes y después de la asignación de cuentas por rol

La primera corrida de pruebas de humo de la HU-001 dejó 33 de 35 casos bloqueados porque Loom buscaba la cuenta de prueba por el texto exacto del rol. Con la asignación por actor principal (ADR-0088) y una cuenta por rol, la tercera corrida dio 28 aprobados, 4 fallidos y 3 bloqueados.

FIGURA: evidencia/corrida-E3c-2026-09-26/capturas/r1-42e-HU-001-resultado-del-smoke-testing.png | HU-001, primera corrida: casos bloqueados por falta de cuenta para el rol

FIGURA: evidencia/corrida-E3c-2026-09-26/capturas/42e-HU-001-resultado-del-smoke-testing.png | HU-001, tercera corrida, con cuentas por rol

FIGURA: evidencia/corrida-E3c-2026-09-26/capturas/43e-HU-002-resultado-del-smoke-testing.png | HU-002: resultado de las pruebas de humo

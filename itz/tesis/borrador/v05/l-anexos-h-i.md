@@ tesis_anexos+
CAPITULO: H
### Anexo H. Datos crudos y trazabilidad de las cifras

Los datos de las corridas y de los experimentos no se reproducen en el documento por su volumen. Están versionados en el repositorio público de la tesis (https://github.com/CarlosSotoGarcia/jcsoto-tech-lead), en la carpeta `itz/tesis/evidencia/`, y cada cifra de los capítulos 4 a 6 se puede recalcular a partir de ellos.

TABLA: Evidencia versionada de la tesis
| Carpeta | Contenido |
| corrida-E1c-2026-09-21 | Exportación de las colecciones de Loom de la corrida E1c (HUs y sus versiones, paquetes, revisiones, métricas, procesos, pruebas de humo y configuración del Proyecto con los secretos enmascarados), bitácora, guiones de Playwright que operaron la interfaz y artefactos de despliegue |
| corrida-E3c-2026-09-26 | Lo mismo para la corrida E3c, más las decisiones sobre los supuestos de las HUs |
| experimento-c-2026-09-27 | Las 58 revisiones del experimento de control, la calificación automática, la clave del cegado, la hoja de evaluación, el contexto de cada Pull Request, los guiones de exportación y de análisis y la bitácora de la corrida |
| cobertura-pi1 | Cálculo de la cobertura de los criterios de aceptación (PI1) |
| costos | Estimación del costo de los escenarios con API |
| infraestructura-gcp-2026-10-03 | Inventario de Google Cloud, costo real de la nube y de la API de Gemini, y el apagado de la infraestructura al cerrar los pilotos |

El guion `herramientas/verificar_cifras.py` recalcula desde esos archivos 86 cifras de los capítulos 4 a 6 y las compara con las del texto; el resultado está en `itz/tesis/trazabilidad-de-cifras.md`, y las 86 coinciden. Las capturas de pantalla de las corridas no se versionan por su tamaño y se conservan localmente. Las bases de datos de las dos aplicaciones desplegadas se exportaron al cerrar los pilotos y también se conservan fuera del repositorio, porque contienen las cuentas de prueba.

CAPITULO: I
### Anexo I. Manual de instalación

Este anexo resume cómo levantar Loom en un equipo de desarrollo. El detalle de cada paso está en el README del repositorio de la plataforma, que al cierre de este documento es privado.

### I.1 Requisitos

- uv, el gestor de proyectos de Python, con Python 3.13.
- Node.js 22 y npm.
- Docker Desktop, para la base de datos MongoDB.
- make (en Windows, GnuWin32 Make o WSL).
- Para operar las fases: una cuenta de Jira con su token de API, o archivos Markdown con las HUs; una cuenta de GitHub dedicada con un token de grano fino limitado a los repositorios del Proyecto; y un proveedor de IA, que puede ser una llave de la API de Anthropic, una llave de la API de Gemini o el CLI de Claude Code con una sesión iniciada.
- Para desplegar: un proyecto de Google Cloud con facturación y la CLI `gcloud` autenticada en el equipo.

### I.2 Instalación y arranque

Desde la carpeta del repositorio de la plataforma:

CODIGO:
make install        # dependencias del backend y del frontend
cp backend/.env.example backend/.env
make seed           # usuarios de la plataforma, uno por rol
make dev            # MongoDB, backend en :8000 y frontend en :4200
FIN-CODIGO

Antes de `make seed` hay que completar `backend/.env`: la conexión a MongoDB (`LOOM_MONGO_URI` y `LOOM_MONGO_DB_NAME`), el secreto con que se firman las sesiones (`LOOM_JWT_SECRET`) y la credencial del proveedor de IA que se vaya a usar (`LOOM_ANTHROPIC_API_KEY`, `LOOM_GEMINI_API_KEY`, o `LOOM_CLAUDE_CLI_PATH` y `LOOM_CLAUDE_CLI_MODEL` para el CLI). Las credenciales de Jira y de GitHub no van en ese archivo: se capturan en cada Proyecto, y la API no las vuelve a mostrar una vez guardadas. La ruta `http://localhost:8000/health` confirma que el backend responde y ve la base de datos. `make down` detiene todo.

### I.3 Primer Proyecto

1. Dar de alta el Proyecto con su nombre, su modo de arranque (nuevo, con arquitectura o avanzado), la fuente de HUs, los repositorios y el proveedor de IA.
2. Fase de Requerimientos: leer las HUs de la fuente y revisar su especificación y sus supuestos.
3. Fase de Diseño: generar los casos de prueba y la arquitectura, y aprobar la arquitectura.
4. Fase de Desarrollo: capturar la cuenta de desarrollo, descomponer en paquetes, confirmar los supuestos de cada HU y avanzar cada HU (generar, revisar, corregir y fusionar sus paquetes).
5. Fase de Implementación: configurar el despliegue (proyecto de Google Cloud, región y cuentas), generar y publicar el release, ejecutarlo, registrar la URL del ambiente y una cuenta de prueba por cada rol que usan los casos, y correr las pruebas de humo.

El Anexo C muestra estas pantallas en el orden en que se usaron en la corrida E1c.

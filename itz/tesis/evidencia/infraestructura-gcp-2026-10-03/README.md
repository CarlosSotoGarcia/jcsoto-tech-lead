# Infraestructura en Google Cloud al cierre de los pilotos (2026-10-03)

Inventario del proyecto de GCP `itz-inventario` (número 118746543308), donde Loom desplegó las aplicaciones de las corridas E1c y
E3c, tomado el 2026-10-03 antes de apagar los recursos que generan costo. Fuente: `gcloud` (solo lectura) y los informes de
facturación de la consola. No incluye secretos: de Secret Manager solo se listan los nombres.

## Recursos

| Recurso | Configuración | Creado | Notas |
|---|---|---|---|
| Cloud Run `inventarios-api` (E1c) | us-central1, 1 vCPU, 1 GiB, mínimo 0 y máximo 20 instancias, ingreso público | 2026-09-20 | 19 revisiones (incluye la primera etapa del piloto) |
| Cloud Run `inventarios-web` (E1c) | igual | 2026-09-20 | 11 revisiones |
| Cloud Run `taller-api` (E3c) | igual | 2026-09-27 | 3 revisiones |
| Cloud Run `taller-web` (E3c) | igual | 2026-09-27 | 2 revisiones |
| Cloud SQL `inventarios-db` | PostgreSQL 15, `db-f1-micro`, 10 GB SSD, zonal, IP pública, sin respaldos automáticos, encendida siempre | 2026-09-20 | Bases `inventarios` y `taller` en la misma instancia |
| Artifact Registry `inventarios` | Docker | 2026-09-19 | 1,354 MB |
| Artifact Registry `taller` | Docker | 2026-09-26 | 224 MB |
| Secret Manager | `db-password`, `jwt-secret`, `jwt-access-secret`, `database-url-taller` | — | Solo nombres |
| Cuentas de servicio | `inventarios-api-run`, `taller-api-run`, `loom-release-deployer`, `loom-itz-inventario` y la predeterminada de Compute | — | Una de ejecución por backend, una desplegadora para GitHub Actions |
| Workload Identity | Pool y proveedor `loom-github`, activo | — | Compartido por los dos proyectos (ADR-0085) |

Cloud Run escala a cero: con mínimo 0 instancias no cobra mientras no recibe tráfico. La instancia de Cloud SQL, en cambio, cobra
mientras está encendida aunque nadie la use.

## Construcciones (Cloud Build)

38 construcciones entre el 2026-09-20 y el 2026-09-27: 37 correctas y 1 fallida. Duración de cada una (minutos):

| Fecha | Imagen | Construcciones | Duración |
|---|---|---|---|
| 2026-09-20 | inventarios-api | 12 | 1.7 a 2.2 (1 fallida) |
| 2026-09-20 | inventarios-web | 5 | 3.2 a 4.2 |
| 2026-09-21 | inventarios-api | 10 | 1.9 a 2.8 |
| 2026-09-21 | inventarios-web | 6 | 3.2 a 4.0 |
| 2026-09-27 | taller-api | 3 | 4.0 a 4.5 |
| 2026-09-27 | taller-web | 2 | 2.5 a 2.6 |

Las del 20 de septiembre corresponden a la primera etapa del piloto; las del 21, a E1c; las del 27, a E3c.

## Costo real de la nube (1 de septiembre al 3 de octubre de 2026, en pesos mexicanos)

Proyecto `itz-inventario` (infraestructura de los pilotos): **MXN 69.92**.

| Servicio | Costo |
|---|---|
| Cloud SQL | MXN 69.07 (de ellos, MXN 56.43 por la instancia micro y el resto por almacenamiento) |
| Artifact Registry | MXN 0.82 |
| Cloud Storage | MXN 0.02 |
| Cloud Run | MXN 0.72 de uso, cubiertos por el nivel gratuito (costo neto 0) |
| Cloud Build, Secret Manager | Sin cargo en el periodo (nivel gratuito) |

Previsión de la consola para el periodo completo: MXN 74.20. Casi todo el costo es la base de datos encendida.

Proyecto `jsoto-itz` (API de Gemini): **MXN 94.37**, de los cuales MXN 93.53 son tokens de la API de Gemini y MXN 0.83
almacenamiento de imágenes de otros proyectos ajenos a la tesis.

| SKU | Uso (tokens) | Costo |
|---|---|---|
| Gemini 3.6 Flash, salida | 457,450 | MXN 29.10 |
| Gemini 3 Pro, salida | 137,618 | MXN 28.01 |
| Gemini 3 Pro, entrada | 753,284 | MXN 25.56 |
| Gemini 3.6 Flash, entrada | 596,153 | MXN 7.58 |
| Gemini 3 Pro, entrada en caché | 947,188 | MXN 3.21 |
| Gemini 3.6 Flash, entrada en caché | 57,369 | MXN 0.07 |

Es el costo real facturado de las llamadas a Gemini del periodo. Por las fechas, corresponde sobre todo a la corrida con Gemini de la
primera etapa del piloto (E2); conviene confirmarlo con el desglose diario antes de citarlo en la tesis. Es la única corrida de la tesis con costo de API facturado; las corridas E1c y E3c usaron el CLI de Claude con
suscripción y su costo es nocional.

## Observaciones para la tesis

- La base de datos tenía IP pública y no tenía respaldos automáticos; ya se declara como limitación de operación (apartado 1.5),
  pero no lo de los respaldos.
- El costo de la infraestructura de los dos pilotos fue bajo frente al costo nocional del modelo (MXN 69.92 en la nube contra
  16.67 y 120.99 USD nocionales de E1c y E3c).
- Los tiempos de construcción explican una parte del tiempo de release reportado (8.5 y 9.5 minutos).

## Apagado (2026-10-03)

Para dejar de generar costos, una vez tomado este inventario:

1. Se exportaron las bases `inventarios` y `taller` con la exportación de Cloud SQL (a un bucket temporal, borrado después) y se
   descargaron a una carpeta local fuera del repositorio, porque contienen las cuentas de prueba: `C:\jsoto\respaldos\itz-inventario-2026-10-03\`
   (`inventarios.sql.gz`, 7 tablas: 6 usuarios y 46 eventos de autenticación; `taller.sql.gz`, 8 tablas: 27 usuarios, 83 sesiones y
   196 eventos de auditoría). Se comprobó que los dos archivos están íntegros.
2. Se borró la instancia de Cloud SQL `inventarios-db`. Era casi todo el costo del proyecto.
3. Se conservaron los cuatro servicios de Cloud Run (escalan a cero y no cobran), las imágenes de Artifact Registry (menos de
   MXN 1 al mes), los secretos, las cuentas de servicio y la identidad federada, para que volver a levantar todo sea más sencillo.
   Sin base de datos, las dos aplicaciones responden con error hasta que se recree.

Para volver a levantarlas: correr el release de cada Proyecto desde Loom (fase 4), que crea la instancia, las bases, los usuarios
y los secretos y vuelve a desplegar. Dos cuidados: Google Cloud no permite reutilizar el nombre de una instancia borrada durante
alrededor de una semana, así que antes del 2026-10-10 hay que poner otro nombre de instancia en la configuración de despliegue del
Proyecto; y las cuentas de prueba por rol hay que sembrarlas de nuevo (o restaurar los respaldos con `gcloud sql import sql`).

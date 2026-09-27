# ADR-0087: El release entrega la cadena de conexión y la URL de la API al compilar el frontend

## Estado

Aceptada. Amplía el contrato del release con la aplicación desplegada ([ADR-0071](0071-el-release-crea-cloud-sql-secretos-y-variables-y-registra-los-fallos-de-arranque.md), [ADR-0086](0086-release-ubica-los-servicios-en-monorepos-con-workspaces.md)).

## Contexto

El contrato del release con la aplicación se había formado con el piloto E1c (Spring Boot y Angular): el backend recibía `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` y, por ser Java, `DB_URL` en formato JDBC; el frontend recibía `API_BASE_URL` en tiempo de ejecución, y el Angular generado la leía al arrancar el contenedor.

En el piloto E3c (NestJS con Prisma y React con Vite) ninguna de las dos cosas bastó:

- El backend no arrancó en Cloud Run: Prisma exige una sola cadena `DATABASE_URL` (`postgresql://…`) y el release no la daba para stacks que no son Java.
- El frontend fija la URL de la API al compilar (`ARG VITE_API_BASE_URL=/api/v1` en su Dockerfile) y su nginx no reenvía `/api` al backend. La `API_BASE_URL` en tiempo de ejecución no le llega a nada: en producción, la interfaz habría llamado a su propio dominio.

## Decisión

1. **Cadena de conexión para stacks que no son Java.** Además de las variables sueltas, el release arma `postgresql://<usuario>:<contraseña>@<ip>:5432/<base>?sslmode=require`, la guarda en Secret Manager como `database-url-<base>` (crea el secreto o agrega una versión solo si cambió) y la pasa al servicio como `DATABASE_URL`. Va como secreto porque contiene la contraseña. Java conserva `DB_URL` en formato JDBC.
2. **URL de la API al compilar el frontend.** El release lee los `ARG` del Dockerfile del frontend. Cada uno cuyo nombre contenga `API` y `URL` (por ejemplo `VITE_API_BASE_URL`) recibe como build-arg la URL del backend; si su valor por defecto es una ruta (`/api/v1`), se conserva al final. `API_BASE_URL` sigue llegando también en tiempo de ejecución, para los frontends que la leen al arrancar.
3. Los build-args viajan en el mismo `cloudbuild` temporal del [ADR-0086](0086-release-ubica-los-servicios-en-monorepos-con-workspaces.md), que ahora se usa también cuando hay build-args.

## Consecuencias

- Probado sin desplegar sobre el repositorio del E3c: el frontend recibe `VITE_API_BASE_URL=https://taller-api-…run.app/api/v1` y el backend no recibe build-args.
- La regla del nombre (`API` y `URL`) es una heurística. Un frontend con otro nombre para esa variable seguirá necesitando que el código generado la lea en tiempo de ejecución.
- El mismo piloto mostró que las variables de entorno del Proyecto se escriben a mano en la configuración y Loom no las contrasta con las que exige el código generado (en el E3c, `JWT_ACCESS_SECRET` y `FRONTEND_URL`). Queda como trabajo pendiente: leer el `.env.example` o el esquema de configuración de la aplicación y avisar de las variables que faltan.

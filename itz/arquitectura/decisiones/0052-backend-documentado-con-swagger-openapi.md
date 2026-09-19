# ADR-0052: El backend se genera documentado con Swagger/OpenAPI

## Estado

Aceptada. Amplía la skill 04 ([ADR-0044](0044-skill-04-arquitectura-fundacional-documento-y-aprobacion.md)) y las skills 05, 06 y 07.

## Contexto

El backend generado no tenía una documentación de API obligatoria: el contrato entre backend y frontend quedaba implícito en el código. Se pidió
que el backend se genere con Swagger.

## Decisión

1. **La arquitectura define la API.** El documento de arquitectura de un repositorio con backend incluye la sección «API y Swagger/OpenAPI»:
   librería del stack (springdoc-openapi con Spring Boot, `@nestjs/swagger`, la documentación integrada de FastAPI, Swashbuckle...), URL de la UI y
   del JSON de OpenAPI, convención de anotación de controladores y DTOs, y el contrato de endpoints por módulo (método, ruta, HUs). Es un campo
   obligatorio de la salida estructurada de la skill 04.
2. **El esqueleto lo deja listo.** El paquete base del backend (skill 05) configura Swagger/OpenAPI y la UI accesible; los paquetes de backend de cada
   HU documentan cada endpoint y lo listan en sus entregables.
3. **El agente lo aplica siempre.** La regla del agente de código (skill 06) exige endpoints documentados con la librería de la arquitectura o, si el
   documento no la trae, la estándar del stack; el README indica la URL de Swagger.
4. **La revisión lo verifica.** La skill 07 marca como observación «mayor» un endpoint sin documentar.

## Consecuencias

- Las arquitecturas ya aprobadas antes de este ADR no tienen la sección; para incluirla hay que regenerar y volver a aprobar la arquitectura
  (y, si ya hay paquetes fusionados, esos siguen como están). Mientras tanto la regla del agente (punto 3) ya exige Swagger en el código nuevo.
- El contrato de endpoints de la arquitectura sirve de referencia para el frontend, pero **no** se genera el código a partir de un OpenAPI
  previo (enfoque *contract-first*): sigue siendo código-primero con documentación.

## Pendiente

- Enfoque contract-first: generar el OpenAPI en la arquitectura y derivar de él controladores y cliente del frontend.
- Publicar el OpenAPI como artefacto (por ejemplo en el repositorio de control) para la tesis y las pruebas.

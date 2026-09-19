# ADR-0050: Entorno de desarrollo dockerizado y README en el primer paquete del esqueleto

## Estado

Aceptada. Ajusta la skill 05 ([ADR-0045](0045-skill-05-descomposicion-desde-arquitectura-fundacional.md)) y la
skill 06 ([ADR-0046](0046-skill-06-generacion-de-codigo-agente-con-tdd.md)).

## Contexto

El primer PR del esqueleto (`BASE/PT-01`) dejaba solo la configuración base del backend: nadie sabía cómo levantar el
aplicativo en desarrollo. Se pidió que desde el primer paso exista un README de despliegue en modo desarrollo y que
el desarrollo se haga con contenedores.

## Decisión

1. **El primer paquete del esqueleto es siempre de infra: el entorno de desarrollo dockerizado.** La planeación
   (skill 05) lo exige en su prompt: `docker-compose.yml` de desarrollo en la raíz con todos los servicios
   (backend, frontend, base de datos y lo que pida la arquitectura), Dockerfiles de desarrollo (código montado
   como volumen y recarga en caliente), `.env.example` y un `README.md` en la raíz con requisitos previos, cómo
   levantar (`docker compose up`), puertos y URLs, variables de entorno, cómo correr las pruebas en los
   contenedores y cómo detener y limpiar. Los demás paquetes del esqueleto dependen de él.
2. **Se hace cumplir.** Al terminar ese paquete el agente (skill 06) debe haber escrito el `README.md` y un archivo
   compose en la raíz; si no, `terminar` se rechaza (hasta 2 veces), igual que la compuerta de pruebas.
3. **El README se mantiene.** Toda generación de código incluye la regla de actualizar el README cuando el paquete
   cambia cómo se instala, configura, levanta o prueba el aplicativo.

## Consecuencias

- El compose puede referenciar servicios cuyo código llega en paquetes posteriores; el README lo indica.
- Los paquetes del esqueleto ya descompuestos con el prompt anterior no cumplen esto: hay que volver a
  descomponer (y regenerar el paquete si ya tenía PR).
- El despliegue a GCP (skill 10) sigue siendo aparte; esto es solo desarrollo local.

## Pendiente

- Verificar que el compose realmente levante (no se ejecuta código antes del PR; lo verifica la CI o una persona).

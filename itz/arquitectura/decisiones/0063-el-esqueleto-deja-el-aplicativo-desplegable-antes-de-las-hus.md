# ADR-0063: El esqueleto deja el aplicativo desplegable antes de las HUs

## Estado

Aceptada. Ajusta la skill 04 ([ADR-0044](0044-skill-04-arquitectura-fundacional-documento-y-aprobacion.md)), la skill 05 ([ADR-0045](0045-skill-05-descomposicion-desde-arquitectura-fundacional.md)) y la skill 10 (release, [ADR-0054](0054-release-py-en-lugar-de-release-sh.md)).

## Contexto

En el piloto de la tesis, ejecutar el release sobre el proyecto falló porque el repositorio solo tenía `Dockerfile.dev`. El `Dockerfile` de producción lo crea el último paquete del esqueleto («Dockerfiles de producción y CI»), pero las HUs no dependían de él: podían construirse y fusionarse sin que el aplicativo fuera desplegable, y el fallo aparecía hasta el release, con el error de gcloud.

## Decisión

1. **La arquitectura lo declara.** La sección Despliegue de la skill 04 define, por cada servicio que va a Cloud Run: el directorio de su Dockerfile de producción (llamado `Dockerfile`, distinto del de desarrollo), la imagen base, cómo se construye, el puerto, el healthcheck, las variables de entorno y qué hace el CI.
2. **El esqueleto lo construye.** El último paquete del esqueleto (capa infra) deja el aplicativo desplegable: Dockerfile de producción por servicio, según esa sección, y el CI.
3. **Las HUs esperan al esqueleto desplegable.** Cada paquete de HU depende, además de su paquete base por capa, de **todos los paquetes de infra del esqueleto**. Ninguna HU arranca hasta que el aplicativo se pueda construir y desplegar; así el primer release es posible desde la primera HU.
4. **El release avisa.** `release.py` comprueba que exista `<directorio>/Dockerfile` antes de llamar a gcloud y, si falta, se detiene nombrando el paquete que lo crea.

## Consecuencias

- El trabajo de las HUs empieza más tarde: hay que fusionar también los paquetes de infra del esqueleto.
- Los proyectos ya descompuestos antes de este ADR conservan sus dependencias; para desplegar basta generar y fusionar el paquete de Dockerfiles de producción. Volver a descomponer reemplazaría sus paquetes.
- No se verifica que el Dockerfile generado construya la imagen: eso lo comprueba el release en Cloud Build.

## Pendiente

- Comprobar en la revisión (skill 07) que un paquete de infra de despliegue construya la imagen, por ejemplo con `docker build`.

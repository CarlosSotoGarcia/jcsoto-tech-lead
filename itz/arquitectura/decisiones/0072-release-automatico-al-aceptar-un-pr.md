# ADR-0072: Release automático al aceptar un PR

## Estado

Aceptada. Complementa la ejecución del release desde la plataforma ([ADR-0055](0055-ejecutar-el-release-desde-la-plataforma.md)) y el release que crea Cloud SQL ([ADR-0071](0071-el-release-crea-cloud-sql-secretos-y-variables-y-registra-los-fallos-de-arranque.md)).

## Contexto

Fusionar un PR solo integra el código en la rama base: no existe ningún trigger de Cloud Build que despliegue, y el release se ejecutaba a mano desde el botón. En el piloto E1c esto obligaba a acordarse de ejecutarlo después de cada fusión antes de poder correr las pruebas de humo contra el ambiente.

## Decisión

1. **Opción por proyecto.** La configuración de despliegue tiene `release_al_fusionar` (apagada por omisión). Con ella encendida, aceptar un PR desde Loom (`POST /paquetes/fusionar`) lanza el release en segundo plano **solo si con esa fusión quedan fusionados todos los paquetes de su HU** (o del grupo BASE). Si aún faltan paquetes, la respuesta lista cuáles (`release_pendiente_de`) y no se despliega: una HU a medias no es desplegable. La respuesta indica `release_automatico`.
2. **Mismo camino que el botón.** Usa `ejecutar_release_stream`: `release.py` sobre la rama base más reciente y el `gcloud` de la máquina del backend.
3. **Una corrida a la vez.** Si llegan más fusiones mientras corre, se hace una sola corrida adicional al terminar, de modo que la última siempre despliega el estado final.
4. **El resultado queda en el proyecto** (`release_ejecutado_en`, `release_resultado`), incluido «Release automático FALLÓ» con el motivo. Un fallo del release nunca revierte ni bloquea la fusión.

## Consecuencias

- Cada HU completa puede generar un despliegue y su costo en GCP; por eso es una opción y no el comportamiento por omisión.
- Solo se dispara con fusiones hechas desde Loom; un PR fusionado directamente en GitHub no lo dispara (para eso haría falta el trigger de Cloud Build o un webhook).
- Los paquetes de infraestructura o de frontend que se fusionan antes de que existan los Dockerfiles de producción harán fallar el release automático; el resultado lo deja escrito.

## Pendiente

- Mostrar el estado del release automático en vivo en la pantalla del proyecto (hoy solo queda el resultado guardado).
- Webhook o trigger para PR fusionados fuera de Loom.

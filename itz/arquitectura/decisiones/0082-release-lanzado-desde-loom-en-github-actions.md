# ADR-0082: Release lanzado desde Loom en GitHub Actions

## Estado

Aceptada. Precisa el disparo del [ADR-0081](0081-despliegue-automatico-con-github-actions-y-workload-identity-federation.md) y del [ADR-0072](0072-release-automatico-al-aceptar-un-pr.md).

## Contexto

Con el workflow disparado por cada push a la rama base (ADR-0081), cada paquete fusionado desplegaría: HU incompletas llegarían a producción y, además, el release automático de Loom (ADR-0072) desplegaría por segunda vez desde la máquina del backend.

## Decisión

1. **El workflow `release.yml` solo se ejecuta por `workflow_dispatch`** (disparador «manual» del proyecto): un cambio en `main` no despliega por sí solo.
2. **Loom lanza el workflow cuando una HU queda completa**, con la API de GitHub y la cuenta de desarrollo, y sigue la corrida hasta que termina, dejando en el proyecto el resultado y el enlace a la ejecución. Así el release ya no depende de que `gcloud` esté autenticado en la máquina del backend y queda visible en GitHub Actions.
3. **Si el workflow todavía no está en la rama base** (el PR que lo publica no se fusionó), Loom ejecuta el release desde su máquina como antes.
4. **Los PR de despliegue que publica Loom se aceptan desde Loom** (`POST /despliegue/fusionar`), con la misma regla de checks en verde (ADR-0076).
5. **Un release por HU completa, no por paquete.** Ejecutarlo a mano sigue siendo posible desde Loom o con «Run workflow» en GitHub.

## Consecuencias

- Verificado en el piloto: el disparo llegó a GitHub Actions y el script se autenticó con la federación de identidad; la primera corrida falló porque el proyecto de GCP no tenía habilitada la API de Cloud Resource Manager, que ahora `release.py` habilita solo.
- El seguimiento de la corrida consulta a GitHub cada 20 s (tope de 30 min) y vive en la memoria del backend: si este se reinicia, el resultado se pierde aunque el workflow siga.

## Pendiente

- Confirmar de punta a punta una corrida completa en verde.

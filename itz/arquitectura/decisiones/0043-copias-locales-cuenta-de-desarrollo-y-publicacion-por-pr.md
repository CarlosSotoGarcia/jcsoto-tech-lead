# ADR-0043: Copias locales de los repositorios, cuenta de desarrollo por Proyecto y publicación por PR

## Estado

Aceptada. Concreta [ADR-0013](0013-cuenta-de-desarrollo-dedicada-para-acceso-a-repositorios.md) y
**reemplaza el mecanismo "solo una nota de texto"** de [ADR-0032](0032-mecanismo-de-credencial-de-la-cuenta-de-desarrollo.md)
para la cuenta de desarrollo, con el mismo criterio que ADR-0033 aplicó al token de Jira.

## Contexto

La skill de código (06) genera código, crea ramas, hace commits y abre PRs, y la skill de release
(ADR-0042) necesita publicar sus archivos en el repositorio del código. Los docs no decían dónde
queda el código descargado ni con qué credencial se trabaja. Además, la cuenta de desarrollo era
solo un campo de texto libre ("dónde guardé el token"): Loom no podía clonar ni empujar nada.

## Decisión

1. **Cuenta de desarrollo por Proyecto, capturada en la pestaña Desarrollo**: usuario de GitHub y
   token (PAT de grano fino). El token se guarda tal cual mientras no exista un gestor de secretos
   real (deuda documentada, igual que el token de Jira), **nunca se vuelve a exponer por la API**
   (ni en el detalle ni en la lista) y, al editar, dejarlo vacío conserva el guardado. El campo de
   nota `cuenta_desarrollo_secret_ref` desaparece. La Fase 3 cuenta como configurada cuando hay
   usuario y token.
2. **Carpeta de trabajo estática y no configurable**, como `loom_target/` (ADR-0035), ignorada por
   git:

```
loom/loom_repos/<proyecto_id>/<dueño>__<repo>/       clon de cada repositorio objetivo
loom/loom_repos/<proyecto_id>/_trabajo/<hash>/       git worktree de una rama de trabajo
```

3. **Cómo se gestionan los cambios**: se clona una vez y después solo `fetch`. Nunca se trabaja
   sobre la rama base del clon: cada trabajo crea su rama desde `origin/<rama_base>` en un
   **worktree** propio (permite trabajar en paralelo, ADR-0030), se hace commit con la identidad de
   la cuenta de desarrollo, `push` y se abre el PR. Al terminar se elimina el worktree; el clon
   permanece. Las ramas de las HUs siguen ADR-0021; la de despliegue es `loom/despliegue-gcp`.
   Si la rama ya existe en el remoto se reemplaza con `--force-with-lease` (es de Loom).
4. **La credencial no toca disco ni línea de comandos**: se pasa a git con variables de entorno
   (`GIT_CONFIG_*` con un `http.extraheader` limitado a github.com), no va en la URL ni en la
   configuración del clon, y se redacta de cualquier mensaje de error.
5. **Verificación**: botón "Probar conexión y credenciales" en la pestaña Desarrollo
   (`POST /proyectos/{id}/cuenta-desarrollo/verificar`). Solo lee. Usa lo escrito en el formulario
   aunque no esté guardado (vacío = lo guardado) y comprueba: conexión con GitHub, token válido,
   que el token pertenezca al usuario capturado, tipo de token y vencimiento, y por cada repositorio
   de Diseño si es accesible, si se puede escribir y si existe la rama base. Avisa lo que no puede
   comprobarse de antemano (el permiso *Workflows* de un token de grano fino).
6. **Primer uso: publicar el release.sh** (`POST /proyectos/{id}/despliegue/publicar`): sube los
   archivos de ADR-0042 a la rama `loom/despliegue-gcp` de cada repositorio que corresponda
   (monorepo: uno; multirepo: los del backend al repo de backend y los del frontend al de
   frontend; el LEEME va como `docs/despliegue-gcp.md`) y abre el PR, o reutiliza el abierto. El
   Proyecto guarda los PRs abiertos y la pestaña Implementación los muestra.
7. Por ahora solo GitHub.

## Consecuencias

- Requiere que la cuenta sea colaboradora con escritura y que el token tenga Contents, Pull requests
  y **Workflows** (Read and write); sin Workflows GitHub rechaza subir `.github/workflows/`.
- El clon vive en el disco donde corre Loom. En un despliegue efímero (contenedor) habría que volver
  a clonar tras un reinicio: es reproducible, no es fuente de verdad (lo es el remoto).
- Cambiar de cuenta se hace desde la misma pantalla y aplica a los siguientes clones/pushes.

## Pendiente

- Gestor de secretos real para los tokens (el de Jira y este).
- Flujo completo por paquete de trabajo de la skill 06 (rama `hu/{id_fuente}/{paquete_id}`) sobre
  esta misma base, y limpieza de clones y ramas ya fusionadas.
- Otros proveedores de Git además de GitHub.

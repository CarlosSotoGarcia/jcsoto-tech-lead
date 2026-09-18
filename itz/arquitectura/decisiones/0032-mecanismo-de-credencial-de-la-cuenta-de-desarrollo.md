# ADR-0032: Mecanismo de credencial de la cuenta de desarrollo: PAT de grano fino, GitHub App como evolución

## Estado

Aceptada. Resuelve el pendiente de [ADR-0013](0013-cuenta-de-desarrollo-dedicada-para-acceso-a-repositorios.md)
sobre el mecanismo concreto de la credencial.

## Contexto

ADR-0013 estableció que el sistema opera sobre los repositorios objetivo con una cuenta de desarrollo
dedicada, sin fijar el mecanismo concreto de la credencial. Para que la plataforma sea utilizable (dar
de alta un Proyecto real y que la cuenta de desarrollo pueda efectivamente crear ramas, commitear,
pushear y abrir PRs) hace falta decidir con qué mecanismo se le da acceso, al menos para el caso
concreto ya cubierto por el diseño: repositorios en GitHub.

## Decisión

Dos mecanismos válidos, ambos con permisos acotados exclusivamente a los repositorios que el Proyecto
declara (ADR-0005), nunca a nivel cuenta/organización completa:

1. **Personal Access Token de grano fino ("fine-grained PAT"), desde una cuenta de servicio dedicada**
   — mecanismo por defecto para dar de alta un Proyecto hoy. Se genera desde
   `Settings → Developer settings → Personal access tokens → Fine-grained tokens`, con **Repository
   access** limitado a los repos del Proyecto y permisos `Contents: Read and write` +
   `Pull requests: Read and write`. La cuenta que lo genera debe ser una cuenta de servicio separada de
   cualquier cuenta personal (refuerza ADR-0013: los commits no deben quedar a nombre de una persona).
2. **GitHub App** — evolución recomendada cuando Loom opera muchos Proyectos/repos a la vez. Mismos
   permisos, pero instalada solo en los repos del Proyecto; en vez de un token de larga vida, el backend
   intercambia la llave privada de la App por tokens de instalación de corta duración (~1h),
   auto-expirables. Más seguro y sin credencial fija que rotar a mano, a costa de más trabajo de
   implementación (firmar JWT, gestionar el ciclo de vida del token).

En ambos casos, la plataforma **nunca almacena el token en texto plano**: el campo
`cuenta_desarrollo_secret_ref` (RF-05, RNF-02) solo referencia dónde vive el secreto en un gestor
externo.

## Consecuencias

- Al dar de alta un Proyecto (RF-05), la ayuda visual de la plataforma debe guiar al usuario a generar
  el PAT de grano fino con esos permisos exactos — evita que alguien le dé de más (p. ej. acceso a todos
  los repos) o de menos (le falte `Pull requests: Read and write` y las skills no puedan abrir PRs).
- Este ADR cubre el caso de repositorios en GitHub, que es el único ejercitado hasta ahora en el
  diseño. Otros hosts (GitLab, Bitbucket) tienen mecanismos análogos (Project/Group Access Tokens,
  App passwords) pero quedan fuera de alcance de este ADR.
- No cambia nada de ADR-0013: sigue siendo una cuenta de servicio, con permisos mínimos, identidad
  distinguible en los commits/PRs.
- Pendiente (implementación, no de esta tesis): flujo de intercambio de JWT→token de instalación para
  la variante GitHub App, si se decide implementarla más adelante.

> **Nota posterior:** en la implementación, [ADR-0043](0043-copias-locales-cuenta-de-desarrollo-y-publicacion-por-pr.md)
> sustituye la "referencia a un secreto" por usuario y token capturados por Proyecto (guardados sin
> exponerse por la API, como el token de Jira), mientras no exista un gestor de secretos real.

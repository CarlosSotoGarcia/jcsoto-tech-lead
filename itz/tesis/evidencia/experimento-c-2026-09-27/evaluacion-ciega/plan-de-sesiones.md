# Plan de calificación por sesiones (experimento C)

Son 177 observaciones en 29 Pull Requests. La hoja las trae en orden aleatorio (`P01` a `P29`); para calificar conviene
otro orden: por proyecto y por historia de usuario, de modo que cada especificación se lee una sola vez. El orden en que se
califica no afecta el cegado, porque dentro de cada PR las observaciones de las dos revisiones ya están mezcladas.

Se proponen seis sesiones de entre 26 y 38 observaciones. Calcula de una hora a hora y media por sesión: unos diez minutos para
leer el contexto de cada PR la primera vez y uno o dos minutos por observación.

## Antes de empezar (una sola vez)

1. Lee [guia-del-evaluador.md](guia-del-evaluador.md): la rúbrica y las reglas.
2. Abre `hoja-de-evaluacion.xlsx` y activa el filtro de la columna `pr`.
3. No abras `clave/`, `datos/experimento_c-c1.json`, `segunda-opinion/` ni la colección `experimento_c` de Mongo.

## En cada PR

1. Abre su archivo de contexto (paquete, especificación y casos de prueba de la HU) y, la primera vez en cada proyecto, su
   documento de arquitectura (`contexto/arquitectura-E1c.md` o `contexto/arquitectura-E3c.md`).
2. Abre el enlace «cambio»: es el código que vio el revisor, antes de cualquier corrección.
3. Filtra la hoja por ese `pr` y califica todas sus observaciones de una vez.
4. Al terminar el PR, revisa si dos observaciones dicen lo mismo y anótalo en «misma que (id)».
5. Guarda la hoja y marca el PR en la lista de abajo.

## Sesión 1: E1c · esqueleto del proyecto (BASE) (38 observaciones)

| Hecho | PR | Paquete | Observaciones | Contexto | Cambio revisado |
|---|---|---|---|---|---|
| ☐ | P15 | BASE/PT-01 | 8 | [contexto/P15.md](contexto/P15.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/commit/36548ea718532ba5492b5c6f53df705ac90285cb) |
| ☐ | P20 | BASE/PT-02 | 8 | [contexto/P20.md](contexto/P20.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/commit/42f89f36fcae104899986fdaa10137bda340a7f9) |
| ☐ | P21 | BASE/PT-03 | 5 | [contexto/P21.md](contexto/P21.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/commit/e60e28f039ea908dfbf79888365a6edd15daaba3) |
| ☐ | P07 | BASE/PT-04 | 6 | [contexto/P07.md](contexto/P07.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/commit/6af0929375c71a6f00aa05ae4dc9f4c0a7f864f8) |
| ☐ | P11 | BASE/PT-05 | 11 | [contexto/P11.md](contexto/P11.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/commit/00878ad8f588cf596510dac833205b55f9b66ed6) |

## Sesión 2: E1c · HU-001 y primer paquete de la HU-002 (26 observaciones)

| Hecho | PR | Paquete | Observaciones | Contexto | Cambio revisado |
|---|---|---|---|---|---|
| ☐ | P28 | HU-001/PT-01 | 11 | [contexto/P28.md](contexto/P28.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/commit/15a41ba74c86c67c1e0cf558f5fadbf390a2df69) |
| ☐ | P24 | HU-001/PT-02 | 7 | [contexto/P24.md](contexto/P24.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/commit/eaf4a60169632945a69c6f35b8934f2436576d32) |
| ☐ | P03 | HU-002/PT-01 | 8 | [contexto/P03.md](contexto/P03.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/commit/ad518813767c7ccc1c19cd9bcd55107b16fbf2c7) |

## Sesión 3: E1c · resto de la HU-002 y HU-003 (29 observaciones)

| Hecho | PR | Paquete | Observaciones | Contexto | Cambio revisado |
|---|---|---|---|---|---|
| ☐ | P29 | HU-002/PT-02 | 11 | [contexto/P29.md](contexto/P29.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/commit/9130621e4884821f6e7717c175b39568f62137c3) |
| ☐ | P10 | HU-002/PT-03 | 6 | [contexto/P10.md](contexto/P10.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/commit/dd13f00d26b96f28bde6085b4a2a5ec394e317aa) |
| ☐ | P01 | HU-003/PT-01 | 7 | [contexto/P01.md](contexto/P01.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/commit/e8ab04c5e86814a122a5d1eb731b0cba574f7cf6) |
| ☐ | P14 | HU-003/PT-02 | 5 | [contexto/P14.md](contexto/P14.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/commit/70a57c434ccc1d0e4d9a3156fc4f4962d8000e16) |

## Sesión 4: E3c · esqueleto del proyecto (BASE) (26 observaciones)

| Hecho | PR | Paquete | Observaciones | Contexto | Cambio revisado |
|---|---|---|---|---|---|
| ☐ | P17 | BASE/PT-01 | 5 | [contexto/P17.md](contexto/P17.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/2e0e993fdb4043cfd88101c46de2e01efa9fd0e2) |
| ☐ | P12 | BASE/PT-02 | 5 | [contexto/P12.md](contexto/P12.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/378f39d48634cef060e079e9ed0a7e2a824d069c) |
| ☐ | P18 | BASE/PT-03 | 5 | [contexto/P18.md](contexto/P18.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/4d8ee22edf95f6e27fef03d5fcff44d3a22a1b58) |
| ☐ | P05 | BASE/PT-04 | 4 | [contexto/P05.md](contexto/P05.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/f945e01a2ea0a6b88e71c213d53409ede4087f54) |
| ☐ | P16 | BASE/PT-05 | 7 | [contexto/P16.md](contexto/P16.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/8ba1883a3b6d1c484f22d21f9b23794834650901) |

## Sesión 5: E3c · HU-001 y dos paquetes de la HU-002 (29 observaciones)

| Hecho | PR | Paquete | Observaciones | Contexto | Cambio revisado |
|---|---|---|---|---|---|
| ☐ | P08 | HU-001/PT-01 | 4 | [contexto/P08.md](contexto/P08.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/56ccf0fbf3d1a40b94b30e1fb5085b7340bf0bb0) |
| ☐ | P13 | HU-001/PT-02 | 5 | [contexto/P13.md](contexto/P13.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/e0585f9fd58a1fab3ce7c180dfc09ef05fb9ecc5) |
| ☐ | P26 | HU-001/PT-03 | 6 | [contexto/P26.md](contexto/P26.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/590bf84cea51f767dc151a501c7ba8a5b663b972) |
| ☐ | P04 | HU-001/PT-04 | 4 | [contexto/P04.md](contexto/P04.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/d3f9db367db5ada94eac53dc6d4b8046f3a946b7) |
| ☐ | P06 | HU-002/PT-01 | 5 | [contexto/P06.md](contexto/P06.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/b27f07051c14fb31a748c4fcb438422ef7b0e491) |
| ☐ | P22 | HU-002/PT-02 | 5 | [contexto/P22.md](contexto/P22.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/c2bb0d98dc8eb9115bbf0f134b601f44c09959f4) |

## Sesión 6: E3c · resto de la HU-002 y HU-003 (29 observaciones)

| Hecho | PR | Paquete | Observaciones | Contexto | Cambio revisado |
|---|---|---|---|---|---|
| ☐ | P19 | HU-002/PT-03 | 4 | [contexto/P19.md](contexto/P19.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/0e404b5cb40b4cc0a108b66000efca97fe029270) |
| ☐ | P09 | HU-002/PT-04 | 6 | [contexto/P09.md](contexto/P09.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/4052f3a3b02624c50569d94f2598efe975ef150e) |
| ☐ | P27 | HU-003/PT-01 | 5 | [contexto/P27.md](contexto/P27.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/cc2d281b8cc8b59caab6fe32fd4b72eec32e660b) |
| ☐ | P23 | HU-003/PT-02 | 5 | [contexto/P23.md](contexto/P23.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/40bbb1d5d27a6d20e085ed1ce42f58b6220f6aa7) |
| ☐ | P25 | HU-003/PT-03 | 7 | [contexto/P25.md](contexto/P25.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/e57e3c206201e038695f316e0a638652d8b1444b) |
| ☐ | P02 | HU-003/PT-04 | 2 | [contexto/P02.md](contexto/P02.md) | [cambio](https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli/commit/4c8d85938b88413355813e948fdf960b117a763d) |

## Bitácora de calificación

Anota cada sesión. El tiempo total y las dudas se reportan en la tesis como parte del método.

| Sesión | Fecha | Hora de inicio | Hora de fin | PRs calificados | Dudas o casos difíciles |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |

## Al terminar

Avisa para correr `python analizar.py c1`. Hasta entonces, no comentes con nadie a qué revisión crees que pertenece cada
observación: si lo sospechas por su contenido, califícala igual por lo que dice.

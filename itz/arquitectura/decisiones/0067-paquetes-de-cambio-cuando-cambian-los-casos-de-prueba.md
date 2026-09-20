# ADR-0067: Paquetes de cambio cuando cambian los casos de prueba

## Estado

Aceptada. Cierra el pendiente del [ADR-0066](0066-propagar-los-cambios-de-hu-a-casos-de-prueba-codigo-y-smoke.md) y reutiliza el mecanismo de los fixes ([ADR-0061](0061-generacion-de-fixes-desde-smoke-testing.md)).

## Decisión

1. **Cuándo aplica.** Una HU con código ya hecho cuyos casos de prueba cambiaron: todos sus paquetes se planearon con una versión anterior de los casos (ADR-0066) y están fusionados. `POST /hus/generar-cambios?hu=` (sin `hu`, todas las que lo necesiten). Se niega si aún hay paquetes sin fusionar, si el código ya está al día o si no se conoce qué cambió.
2. **Diagnóstico con IA.** Recibe la especificación vigente, la arquitectura, los paquetes existentes con los archivos que tocó cada PR, los casos **nuevos o modificados** (con cómo eran antes los modificados) y los criterios **eliminados**. Devuelve los paquetes: capa, entregables (siempre con pruebas nuevas o ajustadas), casos que cubre y a qué paquete existente corresponde el cambio. Los criterios eliminados se resuelven dentro de un paquete, indicando qué código y qué pruebas quitar o adaptar aunque no cubra casos.
3. **Un paquete normal.** Tipo `cambio`, nueva ronda, con la versión vigente de los casos (`tcs_version`), sin dependencias (lo anterior ya está fusionado). Entra al ciclo de las skills 06 y 07 y, al fusionarse, se vuelve a probar con smoke testing. Al tener paquetes con la versión vigente, el aviso de «código desactualizado» desaparece; el de smoke sigue hasta que se vuelva a probar.
4. **Arquitectura por contenido.** La arquitectura guarda la versión de la especificación de cada HU con la que se generó (`arquitectura_specs`); si sube, el proyecto avisa que quedó desactualizada.
5. **Interfaz.** El paso recomendado ofrece «Generar paquetes de cambio de HU-00N»; el smoke se recomienda solo cuando los paquetes de cambio ya están fusionados. Los paquetes de cambio llevan la etiqueta `cambio`.

## Consecuencias

- Un cambio de requisito recorre casos de prueba, código, revisión y smoke con el mismo ciclo que el resto.
- El diagnóstico puede equivocarse al ubicar el código a cambiar: la revisión (skill 07) y el smoke lo comprueban después.
- No hay límite de rondas de cambio (a diferencia de los fixes): cada una responde a un cambio real de requisito.
- Probado con un proyecto de prueba y un modelo real: un criterio nuevo, uno modificado y uno eliminado dieron dos paquetes (backend y frontend), atribuidos a sus paquetes de origen. No se ha corrido el ciclo completo de código y revisión sobre esos paquetes.

## Pendiente

- Detectar que un cambio de especificación afecta a HUs que dependen de la cambiada.

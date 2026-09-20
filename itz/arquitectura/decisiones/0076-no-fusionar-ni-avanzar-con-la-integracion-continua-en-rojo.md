# ADR-0076: No fusionar ni avanzar con la integración continua en rojo

## Estado

Aceptada. Endurece la aceptación de PR ([ADR-0051](0051-aceptar-y-fusionar-el-pr-desde-la-plataforma.md)) y el avance por HU ([ADR-0074](0074-avanzar-con-una-hu-de-punta-a-punta.md)).

## Contexto

Loom fusionaba un PR sin mirar sus checks de GitHub Actions. En el piloto E1c los PR #14 al #22 se fusionaron con el CI en rojo (falla de `mvn verify` por la migración V2 y del build de la imagen del frontend); los paquetes siguientes se construyeron encima de código que ya no pasaba el CI. Un paquete depende de los anteriores, así que un PR en rojo contamina todo lo que sigue.

## Decisión

1. **La fusión exige los checks en verde.** Antes de fusionar, Loom lee los check runs y los estados del commit más reciente de la rama del PR (`estado_checks_pr`: `verde`, `pendiente`, `fallido` o `sin_checks`). Con checks fallidos o sin terminar, la fusión se rechaza y el mensaje nombra los checks. Aplica al botón de aceptar y al avance por HU.
2. **El avance por HU espera y se detiene.** Antes de fusionar cada paquete, «Avanzar con esta HU» espera a que el CI termine (revisa cada 20 s, tope de 25 min). En verde, fusiona y sigue con el siguiente paquete; en rojo, se detiene, deja el PR abierto y nombra los checks que fallaron. No se pasa al siguiente paquete mientras el anterior no esté fusionado, lo cual ya exigían las dependencias entre paquetes.
3. **Repositorio sin checks.** Si tras 90 s el repositorio no reporta ninguno, se acepta y se avisa en el registro; sin CI no hay evidencia que exigir.
4. **Complemento recomendado en GitHub:** proteger la rama base con «Require status checks to pass» hace que ni siquiera un clic fuera de Loom pueda fusionar en rojo. Loom no lo configura por su cuenta: exige permisos de administrador y, en un repositorio privado, GitHub Pro (con el plan gratuito la API responde 403, como en el piloto). Queda preparado como `loom/scripts/proteger-rama.sh`, que se activa a mano con `scripts/proteger-rama.sh <dueño/repo> main`.

## Consecuencias

- Un CI lento alarga el avance; se ve en el registro qué check falta.
- Un CI en rojo por un defecto del código generado detiene la HU: falta que Loom lea el log del check y se lo devuelva al agente para corregir, igual que hace con la compilación local ([ADR-0070](0070-compuerta-de-compilacion-antes-de-abrir-o-corregir-un-pr.md)).
- No hay forma de forzar la fusión desde Loom con el CI en rojo; hay que hacerlo en GitHub, a conciencia.

## Pendiente

- Devolver al agente el log de los checks fallidos como una ronda de corrección más.
- Mostrar el estado del CI de cada PR en la lista de paquetes.

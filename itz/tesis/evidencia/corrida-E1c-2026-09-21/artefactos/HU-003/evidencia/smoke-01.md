---
hu_id: HU-003
tipo: smoke
corrida: 1
modo: completo
fecha: 2026-09-21
ambiente: https://inventarios-web-118746543308.us-central1.run.app
proveedor_ia: claude_cli
tcs_totales: 16
tcs_pasan: [TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015]
tcs_fallan: [TC-016]
tcs_bloqueados: []
porcentaje_pasan: 94%
porcentaje_fallan: 6%
porcentaje_bloqueados: 0%
regresiones: []
---

# Smoke testing — HU-003: Cerrar sesión manualmente y expirar sesión por inactividad

Corrida 1 (completo). Script de la HU: `smoke-01/HU-003_smoke.py`.

## Resumen

| Resultado | Casos | % |
|---|---:|---:|
| ✅ Pasa | 15 | 94% |
| ❌ Falla | 1 | 6% |
| ⛔ Bloqueado | 0 | 0% |
| **Total** | **16** | **100%** |

## Casos

| TC | Rol | Resultado | Cómo se resolvió | Motivo |
|---|---|---|---|---|
| TC-001 | usuario_final | ✅ Pasa | script |  |
| TC-002 | usuario_final | ✅ Pasa | script |  |
| TC-003 | usuario_final | ✅ Pasa | script |  |
| TC-004 | usuario_final | ✅ Pasa | script |  |
| TC-005 | usuario_final | ✅ Pasa | script |  |
| TC-006 | usuario_final | ✅ Pasa | script |  |
| TC-007 | usuario_final | ✅ Pasa | agente (el script estaba mal) | Tras cerrar sesión y pulsar atrás, la página permanece en /login mostrando «Iniciar sesión» y sin contenido protegido. |
| TC-008 | usuario_final | ✅ Pasa | script |  |
| TC-009 | usuario_final | ✅ Pasa | script |  |
| TC-010 | usuario_final | ✅ Pasa | script |  |
| TC-011 | usuario_final | ✅ Pasa | script |  |
| TC-012 | usuario_final | ✅ Pasa | script |  |
| TC-013 | usuario_final | ✅ Pasa | script |  |
| TC-014 | usuario_final | ✅ Pasa | script |  |
| TC-015 | usuario_final | ✅ Pasa | script |  |
| TC-016 | admin | ❌ Falla | agente (fallo confirmado) | Como admin, al abrir /bitacora la app redirige a /home, que solo muestra el encabezado "Inicio" y el botón "Cerrar sesión". No hay menú, enlace ni pantalla de b |

## TC-001 — ✅ Pasa



![captura](smoke-01/TC-001.png)

## TC-002 — ✅ Pasa



![captura](smoke-01/TC-002.png)

## TC-003 — ✅ Pasa



![captura](smoke-01/TC-003.png)

## TC-004 — ✅ Pasa



![captura](smoke-01/TC-004.png)

## TC-005 — ✅ Pasa



![captura](smoke-01/TC-005.png)

## TC-006 — ✅ Pasa



![captura](smoke-01/TC-006.png)

## TC-007 — ✅ Pasa

Tras cerrar sesión y pulsar atrás, la página permanece en /login mostrando «Iniciar sesión» y sin contenido protegido.

Verificación del agente de navegador:

1. ir a / — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Cerrar sesión» — ok: apareció «Cerrar sesión»
7. clic button «Cerrar sesión» — ok: clic
8. presionar «Alt+ArrowLeft» — ok: presionó Alt+ArrowLeft
9. verificar texto «Iniciar sesión» — ok: verificado: «Iniciar sesión» está visible

![captura](smoke-01/TC-007.png)

## TC-008 — ✅ Pasa



![captura](smoke-01/TC-008.png)

## TC-009 — ✅ Pasa



![captura](smoke-01/TC-009.png)

## TC-010 — ✅ Pasa



![captura](smoke-01/TC-010.png)

## TC-011 — ✅ Pasa



![captura](smoke-01/TC-011.png)

## TC-012 — ✅ Pasa



![captura](smoke-01/TC-012.png)

## TC-013 — ✅ Pasa



![captura](smoke-01/TC-013.png)

## TC-014 — ✅ Pasa



![captura](smoke-01/TC-014.png)

## TC-015 — ✅ Pasa



![captura](smoke-01/TC-015.png)

## TC-016 — ❌ Falla

Como admin, al abrir /bitacora la app redirige a /home, que solo muestra el encabezado "Inicio" y el botón "Cerrar sesión". No hay menú, enlace ni pantalla de bitácora/auditoría, así que no se puede ver el registro de cierre manual ni de expiración por inactividad. Se esperaba un registro por evento con usuario, fecha/hora y tipo. La funcionalidad no existe o no es accesible. · Script: AssertionError: Locator expected to be visible Actual value: None Error: element(s) not found Call log:

Verificación del agente de navegador:

1. ir a / — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Cerrar sesión» — ok: apareció «Cerrar sesión»
7. ir a /bitacora — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/bitacora

![captura](smoke-01/TC-016.png)

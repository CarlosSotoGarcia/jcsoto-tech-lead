"""Trazabilidad de cifras: recalcula desde la evidencia versionada las cifras que reporta la tesis y las compara.

    python herramientas/verificar_cifras.py        (desde itz/tesis; escribe trazabilidad-de-cifras.md)

Cada comprobación dice dónde aparece la cifra en la tesis, qué valor reporta, cómo se recalcula y de qué archivo sale. No usa la
base de datos: solo los JSON exportados en evidencia/. Una cifra que no coincide aparece como «NO COINCIDE» y el guion termina
con código 1."""

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
EV = RAIZ / "evidencia"
E1C, E3C, EXP, PI1 = EV / "corrida-E1c-2026-09-21" / "datos", EV / "corrida-E3c-2026-09-26" / "datos", EV / "experimento-c-2026-09-27", EV / "cobertura-pi1"


def cargar(ruta: Path):
    return json.loads(ruta.read_text(encoding="utf-8"))


def minutos(ms) -> float:
    return (ms or 0) / 60000


class Corrida:
    def __init__(self, carpeta: Path):
        self.carpeta = carpeta
        self.hus = cargar(carpeta / "hus.json")
        self.paquetes = cargar(carpeta / "paquetes.json")
        self.revisiones = cargar(carpeta / "revisiones.json")
        self.metricas = cargar(carpeta / "metricas.json")
        self.smoke = cargar(carpeta / "smoke.json")
        self.procesos = cargar(carpeta / "procesos.json")
        self.llamadas = [m for m in self.metricas if m.get("tipo") == "llamada"]
        self.primeras = [r for r in self.revisiones if r.get("tipo") == "revision" and str(r.get("ronda")) == "1"]
        self.todas_revisiones = [r for r in self.revisiones if r.get("tipo") == "revision"]

    def observaciones(self, revisiones) -> list[dict]:
        return [o for r in revisiones for o in r.get("observaciones") or []]

    def por(self, campo: str, revisiones=None) -> Counter:
        return Counter(o.get(campo) for o in self.observaciones(revisiones if revisiones is not None else self.primeras))

    def casos(self) -> list[int]:
        return [len(h.get("casos_prueba") or []) for h in sorted(self.hus, key=lambda h: h["id"])]

    def skill(self, nombre: str) -> dict:
        ll = [m for m in self.llamadas if m.get("skill") == nombre]
        return {"llamadas": len(ll), "in": sum(m.get("tokens_in") or 0 for m in ll), "out": sum(m.get("tokens_out") or 0 for m in ll),
                "min": round(minutos(sum(m.get("duracion_ms") or 0 for m in ll)), 1), "usd": round(sum(m.get("costo_usd") or 0 for m in ll), 2)}

    def costo(self) -> float:
        return round(sum(m.get("costo_usd") or 0 for m in self.llamadas), 2)

    def duracion_procesos(self, skill: str, estado: str = "terminada") -> list[float]:
        salida = []
        for p in self.procesos:
            if p.get("skill") == skill and p.get("estado") == estado and p.get("inicio") and p.get("fin"):
                salida.append((datetime.fromisoformat(p["fin"]) - datetime.fromisoformat(p["inicio"])).total_seconds() / 60)
        return salida

    def smoke_final(self) -> dict[str, dict]:
        """Última corrida de pruebas de humo de cada HU."""
        ultimo: dict[str, dict] = {}
        for s in sorted(self.smoke, key=lambda s: (s["hu_id"], s.get("corrida") or 0)):
            ultimo[s["hu_id"]] = s
        return ultimo

    def compuerta(self) -> Counter:
        return Counter(m.get("resultado") for m in self.metricas if m.get("tipo") == "compuerta")


e1, e3 = Corrida(E1C), Corrida(E3C)
resumen_c = cargar(EXP / "datos" / "resumen-c1.json")
h1 = cargar(EXP / "datos" / "resultados-c1-opinion.json")
crudo_c = cargar(EXP / "datos" / "experimento_c-c1.json")
metricas_c = cargar(EXP / "datos" / "metricas-c1.json")
opinion = cargar(EXP / "segunda-opinion" / "opinion-c1.json")
pi1 = cargar(PI1 / "cobertura-pi1.json")

RELEVANTES = ("relevante y correcta", "relevante pero mal sustentada")


def sf(corrida: Corrida, campo: str) -> int:
    return sum(s.get(campo) or 0 for s in corrida.smoke_final().values())


def pct(a: float, b: float, dec: int = 1) -> float:
    return round(100 * a / b, dec)


def cal(cond: str, nombre: str) -> int:
    return h1["por_condicion"][cond]["calificaciones"].get(nombre, 0)


def rel(cond: str) -> int:
    return sum(cal(cond, n) for n in RELEVANTES)


def entrada_media(cond: str) -> int:
    xs = [d["entrada_chars"] for d in crudo_c if d["condicion"] == cond]
    return round(sum(xs) / len(xs))


GEN_E1: dict[str, float] = {}
for _m in e1.llamadas:
    if _m.get("skill") == "generar-codigo":
        GEN_E1[_m.get("referencia")] = GEN_E1.get(_m.get("referencia"), 0) + minutos(_m.get("duracion_ms"))
REV_E1 = [minutos(r.get("duracion_ms")) for r in e1.primeras]

F1, F3, FC, FO, FP = "corrida-E1c-2026-09-21/datos/", "corrida-E3c-2026-09-26/datos/", "experimento-c-2026-09-27/datos/", "experimento-c-2026-09-27/segunda-opinion/opinion-c1.json", "cobertura-pi1/cobertura-pi1.json"

# (dónde aparece, cifra, valor en la tesis, valor recalculado, fuente)
COMPROBACIONES = [
    # ---- E1c ----
    ("5.2.1, T 5.2, T 5.12", "E1c: casos de prueba por HU", [14, 14, 16], e1.casos(), F1 + "hus.json"),
    ("5.2.1, T 5.12, T 4.2", "E1c: paquetes de trabajo", 12, len(e1.paquetes), F1 + "paquetes.json"),
    ("5.2.4, T 5.12, T 4.2", "E1c: observaciones de las 12 primeras revisiones", 66, len(e1.observaciones(e1.primeras)), F1 + "revisiones.json"),
    ("5.2.4, T 5.12", "E1c: bloqueantes, mayores y menores", [2, 24, 40], [e1.por("severidad")[k] for k in ("bloqueante", "mayor", "menor")], F1 + "revisiones.json"),
    ("5.2.4", "E1c: observaciones por fuente (buenas prácticas, criterios, pruebas, seguridad, arquitectura)", [23, 15, 14, 9, 5],
     [e1.por("fuente")[k] for k in ("buenas_practicas", "criterio_aceptacion", "pruebas", "seguridad", "arquitectura")], F1 + "revisiones.json"),
    ("5.2.4", "E1c: promedio de observaciones por paquete", 5.5, round(len(e1.observaciones(e1.primeras)) / 12, 1), F1 + "revisiones.json"),
    ("5.2.3, T 5.3", "E1c: compuerta de compilación (aprobada, fallida, omitida)", [10, 5, 2], [e1.compuerta()[k] for k in ("ok", "falla", "omitida")], F1 + "metricas.json (tipo compuerta)"),
    ("5.2.6, T 5.4, T 5.12", "E1c: pruebas de humo (aprobados, fallidos, bloqueados)", [36, 2, 6], [sf(e1, k) for k in ("pasan", "fallan", "bloqueados")], F1 + "smoke.json"),
    ("5.2.6", "E1c: porcentaje de casos aprobados", 82, round(100 * sf(e1, "pasan") / 44), F1 + "smoke.json"),
    ("T 5.4", "E1c: duración de las pruebas de humo por HU (min)", [5.3, 5.1, 3.3], [round(minutos(s["duracion_ms"]), 1) for _, s in sorted(e1.smoke_final().items())], F1 + "smoke.json"),
    ("T 5.2", "E1c: pruebas de humo, tiempo total (min)", 13.7, round(sum(minutos(s["duracion_ms"]) for s in e1.smoke), 1), F1 + "smoke.json"),
    ("5.2.8, T 5.6, T 5.12", "E1c: llamadas al modelo", 128, len(e1.llamadas), F1 + "metricas.json (tipo llamada)"),
    ("5.2.8, T 5.6", "E1c: tokens de entrada y de salida", [2146219, 516483], [sum(m.get("tokens_in") or 0 for m in e1.llamadas), sum(m.get("tokens_out") or 0 for m in e1.llamadas)], F1 + "metricas.json"),
    ("5.2.8", "E1c: tokens leídos de caché (millones)", 14.6, round(sum(m.get("tokens_cache") or 0 for m in e1.llamadas) / 1e6, 1), F1 + "metricas.json"),
    ("5.2.8, T 5.6, T 5.12", "E1c: costo nocional (USD)", 16.67, e1.costo(), F1 + "metricas.json"),
    ("T 5.6", "E1c: generar código (llamadas, tokens in, out, min, USD)", [15, 855897, 387314, 53.3, 9.27], list(e1.skill("generar-codigo").values()), F1 + "metricas.json"),
    ("T 5.6", "E1c: revisar código (llamadas, tokens in, out, min, USD)", [12, 528048, 24550, 5.5, 2.44], list(e1.skill("revisar-codigo").values()), F1 + "metricas.json"),
    ("T 5.6", "E1c: pruebas de humo (llamadas, tokens in, out, min, USD)", [81, 311216, 34958, 10.6, 2.19], list(e1.skill("smoke-testing").values()), F1 + "metricas.json"),
    ("T 5.6", "E1c: corregir código (llamadas, tokens in, out, min, USD)", [3, 155788, 16142, 2.6, 0.95], list(e1.skill("corregir-codigo").values()), F1 + "metricas.json"),
    ("T 5.6", "E1c: descomponer (llamadas, tokens in, out, min, USD)", [10, 146207, 23826, 4.5, 0.90], list(e1.skill("descomponer").values()), F1 + "metricas.json"),
    ("T 5.6", "E1c: arquitectura (llamadas, tokens in, out, min, USD)", [1, 53454, 12504, 2.0, 0.34], list(e1.skill("arquitectura").values()), F1 + "metricas.json"),
    ("T 5.6", "E1c: generar casos de prueba (llamadas, tokens in, out, min, USD)", [3, 46488, 10407, 1.7, 0.31], list(e1.skill("generar-tcs").values()), F1 + "metricas.json"),
    ("T 5.6", "E1c: leer y especificar HUs (llamadas, tokens in, out, min, USD)", [3, 49121, 6782, 1.4, 0.28], list(e1.skill("descubrir").values()), F1 + "metricas.json"),
    ("T 5.6", "E1c: tiempo de modelo total (min)", 81.5, round(minutos(sum(m.get("duracion_ms") or 0 for m in e1.llamadas)), 1), F1 + "metricas.json"),
    ("5.2.8", "E1c: generación como % del costo y del tiempo de modelo", [56, 65],
     [round(100 * e1.skill("generar-codigo")["usd"] / e1.costo()), round(100 * e1.skill("generar-codigo")["min"] / minutos(sum(m.get("duracion_ms") or 0 for m in e1.llamadas)))], F1 + "metricas.json"),
    ("5.2.8", "E1c: costo por paquete de revisar y de generar (USD)", [0.20, 0.77], [round(e1.skill("revisar-codigo")["usd"] / 12, 2), round(e1.skill("generar-codigo")["usd"] / 12, 2)], F1 + "metricas.json"),
    ("T 5.2", "E1c: generar el código de los 12 paquetes (min de proceso)", 70.7, round(sum(e1.duracion_procesos("generar-codigo")), 1), F1 + "procesos.json"),
    ("T 5.2", "E1c: revisar los 12 paquetes (min de proceso)", 6.6, round(sum(e1.duracion_procesos("revisar-codigo")), 1), F1 + "procesos.json"),
    ("T 5.2", "E1c: corregir un paquete (min de proceso)", 6.2, round(sum(e1.duracion_procesos("corregir-codigo")), 1), F1 + "procesos.json"),
    ("5.2.3", "E1c: generación por paquete, mínimo y máximo (min de modelo)", [0.9, 10.8], [round(min(GEN_E1.values()), 1), round(max(GEN_E1.values()), 1)], F1 + "metricas.json"),
    ("Anexo C", "E1c: proceso de generación por paquete, mínimo y máximo (min de reloj)", [1.0, 14.7], [round(min(e1.duracion_procesos("generar-codigo")), 1), round(max(e1.duracion_procesos("generar-codigo")), 1)], F1 + "procesos.json"),
    ("5.2.4", "E1c: duración de una revisión, mínimo y máximo (min)", [0.4, 0.8], [round(min(REV_E1), 1), round(max(REV_E1), 1)], F1 + "revisiones.json"),
    ("5.2.4", "E1c: revisiones que aprobaron y que dejaron observaciones", [2, 10], [sum(r["veredicto"] == "aprobado" for r in e1.primeras), sum(r["veredicto"] == "con_observaciones" for r in e1.primeras)], F1 + "revisiones.json"),
    ("5.2.2", "E1c: reintentos de la descomposición sin paquetes", 3, sum(1 for m in e1.metricas if m.get("tipo") == "reintento"), F1 + "metricas.json (tipo reintento)"),
    # ---- E3c ----
    ("5.2.10", "E3c: revisiones que aprobaron y que dejaron observaciones", [7, 10], [sum(r["veredicto"] == "aprobado" for r in e3.primeras), sum(r["veredicto"] == "con_observaciones" for r in e3.primeras)], F3 + "revisiones.json"),
    ("T 5.8", "E3c: observaciones y mayores de la primera revisión de cada paquete, en el orden de la tabla",
     [[4, 0], [4, 0], [3, 1], [3, 1], [6, 0], [4, 1], [5, 1], [2, 1], [3, 0], [7, 1], [5, 1], [3, 0], [3, 1], [3, 1], [1, 1], [0, 0], [3, 0]],
     [[len(r["observaciones"]), sum(o["severidad"] == "mayor" for o in r["observaciones"])] for r in sorted(e3.primeras, key=lambda r: r["referencia"])], F3 + "revisiones.json"),
    ("5.2.9", "E3c: procesos de generación terminados y cortados", [16, 3], [sum(p["skill"] == "generar-codigo" and p["estado"] == "terminada" for p in e3.procesos), sum(p["skill"] == "generar-codigo" and p["estado"] == "error" for p in e3.procesos)], F3 + "procesos.json"),
    ("5.2.9, T 5.7, T 5.12", "E3c: casos de prueba por HU", [35, 39, 27], e3.casos(), F3 + "hus.json"),
    ("5.2.9, T 5.12, T 4.2", "E3c: paquetes de trabajo", 17, len(e3.paquetes), F3 + "paquetes.json"),
    ("5.2.10, T 5.12, T 4.2", "E3c: observaciones de las 17 primeras revisiones", 59, len(e3.observaciones(e3.primeras)), F3 + "revisiones.json"),
    ("5.2.10, T 5.12", "E3c: bloqueantes, mayores y menores", [0, 10, 49], [e3.por("severidad")[k] for k in ("bloqueante", "mayor", "menor")], F3 + "revisiones.json"),
    ("5.2.10", "E3c: observaciones por fuente (buenas prácticas, arquitectura, pruebas, seguridad, criterios)", [22, 11, 10, 9, 7],
     [e3.por("fuente")[k] for k in ("buenas_practicas", "arquitectura", "pruebas", "seguridad", "criterio_aceptacion")], F3 + "revisiones.json"),
    ("5.2.10", "E3c: promedio de observaciones por paquete", 3.5, round(len(e3.observaciones(e3.primeras)) / 17, 1), F3 + "revisiones.json"),
    ("5.2.10", "E3c: revisiones de toda la corrida y sus observaciones", [19, 69], [len(e3.todas_revisiones), len(e3.observaciones(e3.todas_revisiones))], F3 + "revisiones.json"),
    ("5.2.10", "E3c: mayores y menores de las 19 revisiones", [12, 57], [e3.por("severidad", e3.todas_revisiones)[k] for k in ("mayor", "menor")], F3 + "revisiones.json"),
    ("5.2.10, T 5.12", "E3c: registros de la compuerta de compilación «omitida»", 21, e3.compuerta()["omitida"], F3 + "metricas.json (tipo compuerta)"),
    ("5.2.10", "E3c: rechazos de la compuerta de archivos obligatorios", 4, sum(1 for m in e3.metricas if m.get("tipo") == "compuerta" and m.get("resultado") != "omitida"), F3 + "metricas.json (tipo compuerta)"),
    ("5.2.11, T 5.9, T 5.12", "E3c: pruebas de humo, corrida final (aprobados, fallidos, bloqueados)", [68, 9, 24], [sf(e3, k) for k in ("pasan", "fallan", "bloqueados")], F3 + "smoke.json"),
    ("T 5.9", "E3c: pruebas de humo por HU (aprobados, fallidos, bloqueados)", [[28, 4, 3], [19, 4, 16], [21, 1, 5]],
     [[s["pasan"], s["fallan"], s["bloqueados"]] for _, s in sorted(e3.smoke_final().items())], F3 + "smoke.json"),
    ("T 5.9, T 5.7", "E3c: duración de la corrida final por HU y total (min)", [17.8, 34.7, 11.2, 63.7],
     [round(minutos(s["duracion_ms"]), 1) for _, s in sorted(e3.smoke_final().items())] + [round(sum(minutos(s["duracion_ms"]) for s in e3.smoke_final().values()), 1)], F3 + "smoke.json"),
    ("5.2.11", "E3c: casos bloqueados en las dos primeras corridas de la HU-001", [33, 33], [s["bloqueados"] for s in sorted(e3.smoke, key=lambda s: s.get("corrida") or 0) if s["hu_id"] == "HU-001"][:2], F3 + "smoke.json"),
    ("5.2.13, T 5.12", "E3c: llamadas al modelo", 532, len(e3.llamadas), F3 + "metricas.json"),
    ("5.2.13, T 5.12", "E3c: costo nocional (USD)", 120.99, e3.costo(), F3 + "metricas.json"),
    ("T 5.7", "E3c: generar el código, 16 procesos terminados (min)", 185.2, round(sum(e3.duracion_procesos("generar-codigo")), 1), F3 + "procesos.json"),
    ("T 5.7", "E3c: revisar los 17 paquetes (min de proceso)", 13.6, round(sum(e3.duracion_procesos("revisar-codigo")), 1), F3 + "procesos.json"),
    # ---- totales de las dos corridas ----
    ("resumen, 5.2.15", "Casos de prueba ejecutados en las dos corridas: total, aprobados, fallidos, bloqueados", [145, 104, 11, 30],
     [sum(e1.casos()) + sum(e3.casos())] + [sf(e1, k) + sf(e3, k) for k in ("pasan", "fallan", "bloqueados")], F1 + "smoke.json y " + F3 + "smoke.json"),
    # ---- experimento C ----
    ("5.2.14, T 5.13", "Exp. C: observaciones con contexto y con solo el diff", [85, 92], [resumen_c["contexto"]["observaciones"], resumen_c["solo_diff"]["observaciones"]], FC + "resumen-c1.json"),
    ("T 5.13", "Exp. C: contexto, bloqueantes, mayores y menores", [7, 21, 57], [resumen_c["contexto"]["por_severidad"].get(k, 0) for k in ("bloqueante", "mayor", "menor")], FC + "resumen-c1.json"),
    ("T 5.13", "Exp. C: solo diff, bloqueantes, mayores y menores", [2, 21, 69], [resumen_c["solo_diff"]["por_severidad"].get(k, 0) for k in ("bloqueante", "mayor", "menor")], FC + "resumen-c1.json"),
    ("T 5.13", "Exp. C: contexto por fuente (criterios, arquitectura, buenas prácticas, pruebas, seguridad)", [13, 19, 39, 9, 5],
     [resumen_c["contexto"]["por_fuente"].get(k, 0) for k in ("criterio_aceptacion", "arquitectura", "buenas_practicas", "pruebas", "seguridad")], FC + "resumen-c1.json"),
    ("T 5.13", "Exp. C: solo diff por fuente (criterios, arquitectura, buenas prácticas, pruebas, seguridad)", [0, 15, 50, 7, 20],
     [resumen_c["solo_diff"]["por_fuente"].get(k, 0) for k in ("criterio_aceptacion", "arquitectura", "buenas_practicas", "pruebas", "seguridad")], FC + "resumen-c1.json"),
    ("T 5.13", "Exp. C: costo nocional por condición (USD)", [14.81, 11.39], [resumen_c["contexto"]["costo_nocional_usd"], resumen_c["solo_diff"]["costo_nocional_usd"]], FC + "resumen-c1.json"),
    ("5.2.14", "Exp. C: minutos de modelo por condición", [92.4, 100.0], [resumen_c["contexto"]["duracion_min_total"], resumen_c["solo_diff"]["duracion_min_total"]], FC + "resumen-c1.json"),
    ("5.2.14", "Exp. C: entrada media por condición (caracteres)", [121611, 76529], [entrada_media("contexto"), entrada_media("solo_diff")], FC + "experimento_c-c1.json"),
    ("5.2.14", "Exp. C: diffs recortados a 140,000 caracteres", 3, resumen_c["diffs_recortados_140k"], FC + "resumen-c1.json"),
    ("5.2.14", "Exp. C: costo de la ejecución descartada (USD)", 12.90, resumen_c["fuera_del_experimento"]["experimento-c-contexto-descartada"]["costo_nocional_usd"], FC + "resumen-c1.json"),
    ("T 4.2", "Exp. C: observaciones por proyecto (E1c contexto y solo diff; E3c contexto y solo diff)", [44, 49, 41, 43],
     [h1["relevantes_y_total_por_proyecto"][p][c][1] for p in ("E1c", "E3c") for c in ("contexto", "solo_diff")], FC + "resultados-c1-opinion.json"),
    # ---- calificación automática ----
    ("5.2.14", "Evaluación automática: observaciones calificadas", 177, sum(len(p["calificaciones"]) for p in opinion["prs"]), FO),
    ("5.2.14", "Evaluación automática: minutos de modelo", 11.7, round(minutos(sum(p["duracion_ms"] for p in opinion["prs"])), 1), FO),
    ("T 5.14", "Con contexto: relevante y correcta, mal sustentada, ruido, falsa", [24, 4, 45, 12], [cal("contexto", n) for n in (*RELEVANTES, "ruido", "falsa")], FC + "resultados-c1-opinion.json"),
    ("T 5.14", "Solo diff: relevante y correcta, mal sustentada, ruido, falsa", [21, 7, 53, 11], [cal("solo_diff", n) for n in (*RELEVANTES, "ruido", "falsa")], FC + "resultados-c1-opinion.json"),
    ("T 5.14", "Con contexto: porcentajes de las cuatro calificaciones", [28.2, 4.7, 52.9, 14.1], [pct(cal("contexto", n), 85) for n in (*RELEVANTES, "ruido", "falsa")], FC + "resultados-c1-opinion.json"),
    ("T 5.14", "Solo diff: porcentajes de las cuatro calificaciones", [22.8, 7.6, 57.6, 12.0], [pct(cal("solo_diff", n), 92) for n in (*RELEVANTES, "ruido", "falsa")], FC + "resultados-c1-opinion.json"),
    ("T 5.14, 6.1", "Relevantes en sentido amplio por condición y su porcentaje", [28, 32.9, 28, 30.4], [rel("contexto"), pct(rel("contexto"), 85), rel("solo_diff"), pct(rel("solo_diff"), 92)], FC + "resultados-c1-opinion.json"),
    ("5.2.14, 6.1", "Prueba pareada amplia: a favor de contexto, a favor de solo diff, empates, p de Wilcoxon, r", [7, 7, 15, 1.0, 0.0],
     [h1["prueba_pareada_amplia"]["signos"][k] for k in ("a_favor_contexto", "a_favor_solo_diff", "empates")] + [h1["prueba_pareada_amplia"]["wilcoxon"]["p_bilateral"], h1["prueba_pareada_amplia"]["wilcoxon"]["r_rango_biserial"]], FC + "resultados-c1-opinion.json"),
    ("5.2.14", "Prueba pareada estricta: a favor de contexto, a favor de solo diff, empates, p de Wilcoxon, r", [8, 6, 15, 0.47, 0.2],
     [h1["prueba_pareada_estricta"]["signos"][k] for k in ("a_favor_contexto", "a_favor_solo_diff", "empates")] + [round(h1["prueba_pareada_estricta"]["wilcoxon"]["p_bilateral"], 2), h1["prueba_pareada_estricta"]["wilcoxon"]["r_rango_biserial"]], FC + "resultados-c1-opinion.json"),
    ("5.2.14", "Relevantes y total por proyecto (E1c contexto, E1c solo diff, E3c contexto, E3c solo diff)", [[18, 44], [17, 49], [10, 41], [11, 43]],
     [h1["relevantes_y_total_por_proyecto"][p][c] for p in ("E1c", "E3c") for c in ("contexto", "solo_diff")], FC + "resultados-c1-opinion.json"),
    ("T 5.15", "Relevantes y total por fuente, con contexto (criterios, arquitectura, buenas prácticas, pruebas, seguridad)", [[6, 13], [5, 19], [11, 39], [1, 9], [5, 5]],
     [h1["relevantes_y_total_por_fuente"][f]["contexto"] for f in ("criterio_aceptacion", "arquitectura", "buenas_practicas", "pruebas", "seguridad")], FC + "resultados-c1-opinion.json"),
    ("T 5.15", "Relevantes y total por fuente, solo diff (arquitectura, buenas prácticas, pruebas, seguridad)", [[5, 15], [10, 50], [1, 7], [12, 20]],
     [h1["relevantes_y_total_por_fuente"][f]["solo_diff"] for f in ("arquitectura", "buenas_practicas", "pruebas", "seguridad")], FC + "resultados-c1-opinion.json"),
    ("5.2.14", "Bloqueantes válidas y total; mayores válidas y total (contexto, solo diff)", [[4, 7], [1, 2], [12, 21], [13, 21]],
     [h1["relevantes_y_total_por_severidad"][s][c] for s in ("bloqueante", "mayor") for c in ("contexto", "solo_diff")], FC + "resultados-c1-opinion.json"),
    ("5.2.14, 6.1", "Pares equivalentes entre condiciones, con ambas relevantes, y hallazgos relevantes distintos", [18, 9, 47],
     [h1["equivalencias_entre_condiciones"][k] for k in ("pares_equivalentes", "pares_con_ambas_relevantes", "hallazgos_relevantes_distintos")], FC + "resultados-c1-opinion.json"),
    ("5.2.14", "PRs sin ninguna observación relevante en ninguna condición", 7, sum(1 for v in h1["por_pr"].values() if v["contexto"]["amplia"] == 0 and v["solo_diff"]["amplia"] == 0), FC + "resultados-c1-opinion.json"),
    # ---- PI1 ----
    ("5.2.15, T 5.16, 6.1.1", "PI1: criterios, cubiertos, explícitos, inferidos, casos", [110, 110, 33, 77, 145],
     [pi1["resumen"]["total"][k] for k in ("criterios", "cubiertos", "explicitos", "inferidos", "casos")], FP),
    ("5.2.15", "PI1: criterios inferidos en E1c y total de E1c", [32, 39], [pi1["resumen"]["E1c"]["inferidos"], pi1["resumen"]["E1c"]["criterios"]], FP),
    ("5.2.15", "PI1: casos por criterio en E3c y en E1c", [1.42, 1.13], [pi1["resumen"]["E3c"]["casos_por_criterio_media"], pi1["resumen"]["E1c"]["casos_por_criterio_media"]], FP),
    ("5.2.15", "PI1: supuestos abiertos en las seis HUs", 50, sum(f["supuestos"] for f in pi1["por_hu"]), FP),
    ("5.2.15", "PI1: porcentaje de criterios inferidos", 70, round(100 * pi1["resumen"]["total"]["inferidos"] / pi1["resumen"]["total"]["criterios"]), FP),
]


def iguales(a, b) -> bool:
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(iguales(x, y) for x, y in zip(a, b))
    if isinstance(a, float) or isinstance(b, float):
        return abs(float(a) - float(b)) < 0.051
    return a == b


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    filas, fallas = [], 0
    for donde, cifra, tesis, calculado, fuente in COMPROBACIONES:
        ok = iguales(tesis, calculado)
        fallas += not ok
        filas.append(f"| {donde} | {cifra} | {tesis} | {calculado} | `{fuente}` | {'Coincide' if ok else '**NO COINCIDE**'} |")
        if not ok:
            print("NO COINCIDE:", donde, "|", cifra, "| tesis:", tesis, "| recalculado:", calculado)
    md = ["# Trazabilidad de cifras", "",
          "Generado por `herramientas/verificar_cifras.py`, que recalcula cada cifra desde los archivos versionados en `evidencia/` y la",
          "compara con el valor que reporta la tesis (v04). No se edita a mano: se corrige el guion o el borrador y se vuelve a generar.", "",
          f"Comprobaciones: {len(filas)}. Coinciden: {len(filas) - fallas}. No coinciden: {fallas}.", "",
          "Las rutas son relativas a `itz/tesis/evidencia/`. «T» es tabla; los números sin «T» son apartados.", "",
          "| Dónde aparece | Cifra | Valor en la tesis | Valor recalculado | Fuente | Estado |", "|---|---|---|---|---|---|", *filas, "",
          "## Cifras que este guion no recalcula", "",
          "- Tiempos de reloj de las etapas cortas (leer HUs, generar casos, arquitectura, descomponer) y del release de las tablas 5.2 y 5.7: salen de `procesos.json`, pero dependen de qué intento se toma (el que terminó bien); se cotejaron a mano contra la bitácora de cada corrida.",
          "- Conteos de intervenciones de la persona (tablas 5.5 y 5.11) y de lanzamientos de release: provienen de la bitácora (`logs/bitacora.log`) y de los registros de hallazgos, no de una colección.",
          "- Cifras de trabajos ajenos (1.96 %, 12.5 %, 19 %, 55.8 %, reducción de hasta 28.9 %, entre otras): se cotejaron contra el resumen de cada fuente; su estado está en `referencias-candidatas.md`.",
          "- Costo real de la nube (MXN 69.92, Cloud SQL MXN 69.07) y duración de las 38 construcciones (1.7 a 4.5 min): salen de los informes de facturación de la consola y de `gcloud builds list`; están en `infraestructura-gcp-2026-10-03/README.md`.",
          "- Conteos de palabras y de cuartillas: los imprime `herramientas/llenar_tesis.py` al generar el documento."]
    (RAIZ / "trazabilidad-de-cifras.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"comprobaciones: {len(filas)} | coinciden: {len(filas) - fallas} | no coinciden: {fallas}")
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()

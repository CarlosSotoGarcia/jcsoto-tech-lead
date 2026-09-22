"""Gráficas del capítulo 5 (corrida E1c del 21-sep-2026). Los datos salen de las colecciones `metricas` y `revisiones` de Loom
(consultadas el 21-sep-2026) y se copian aquí para que la gráfica se pueda regenerar sin la base de datos.

Uso: python herramientas/graficas_cap5.py   (escribe PNG en itz/tesis/graficas/)"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SALIDA = Path(__file__).resolve().parents[1] / "graficas"
SALIDA.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

# minutos de generación de código y costo (USD) por paquete: suma de las llamadas del skill generar-codigo
PAQUETES = ["BASE/PT-01", "BASE/PT-02", "BASE/PT-03", "BASE/PT-04", "BASE/PT-05", "HU-001/PT-01", "HU-001/PT-02",
            "HU-002/PT-01", "HU-002/PT-02", "HU-002/PT-03", "HU-003/PT-01", "HU-003/PT-02"]
MINUTOS = [0.9, 4.3, 1.7, 2.4, 1.6, 8.7, 3.0, 4.4, 6.0, 2.2, 7.2, 10.8]
COSTO = [0.17, 0.52, 0.30, 0.34, 0.24, 1.34, 0.57, 0.80, 1.24, 0.49, 1.55, 1.69]

fig, ax = plt.subplots(figsize=(8, 4))
barras = ax.bar(PAQUETES, MINUTOS, color="#4a6fa5")
for b, c in zip(barras, COSTO):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.15, f"{c:.2f}", ha="center", fontsize=8)
ax.set_ylabel("Minutos de generación de código")
ax.set_title("Duración y costo (USD, sobre cada barra) por paquete", fontsize=10)
plt.xticks(rotation=45, ha="right")
fig.tight_layout()
fig.savefig(SALIDA / "g5-1-duracion-y-costo-por-paquete.png", dpi=200)
plt.close(fig)

# observaciones de las 12 revisiones, por fuente y severidad
FUENTES = ["buenas_practicas", "criterio_aceptacion", "pruebas", "seguridad", "arquitectura"]
ETIQ = ["Buenas prácticas", "Criterio de aceptación", "Pruebas", "Seguridad", "Arquitectura"]
DATOS = {  # (fuente, severidad) -> cantidad
    ("buenas_practicas", "bloqueante"): 1, ("buenas_practicas", "mayor"): 5, ("buenas_practicas", "menor"): 17,
    ("criterio_aceptacion", "mayor"): 10, ("criterio_aceptacion", "menor"): 5,
    ("pruebas", "bloqueante"): 1, ("pruebas", "mayor"): 1, ("pruebas", "menor"): 12,
    ("seguridad", "mayor"): 7, ("seguridad", "menor"): 2,
    ("arquitectura", "mayor"): 1, ("arquitectura", "menor"): 4,
}
COLORES = {"bloqueante": "#b3403a", "mayor": "#e0a030", "menor": "#8fa9c9"}
fig, ax = plt.subplots(figsize=(8, 3.6))
izq = [0] * len(FUENTES)
for sev in ("bloqueante", "mayor", "menor"):
    vals = [DATOS.get((f, sev), 0) for f in FUENTES]
    ax.barh(ETIQ, vals, left=izq, color=COLORES[sev], label={"bloqueante": "Bloqueantes", "mayor": "Mayores", "menor": "Menores"}[sev])
    izq = [a + b for a, b in zip(izq, vals)]
ax.invert_yaxis()
ax.set_xlabel("Observaciones (66 en 12 revisiones)")
ax.legend(loc="lower right", frameon=False)
fig.tight_layout()
fig.savefig(SALIDA / "g5-2-observaciones-por-fuente-y-severidad.png", dpi=200)
plt.close(fig)

# costo por skill (USD)
SKILLS = ["generar-codigo", "revisar-codigo", "smoke-testing", "corregir-codigo", "descomponer", "arquitectura", "generar-tcs", "descubrir"]
USD = [9.27, 2.44, 2.19, 0.95, 0.90, 0.34, 0.31, 0.28]
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.barh(SKILLS, USD, color="#4a6fa5")
for i, v in enumerate(USD):
    ax.text(v + 0.1, i, f"{v:.2f}", va="center", fontsize=9)
ax.invert_yaxis()
ax.set_xlabel("Costo nocional (USD, informado por el CLI)")
fig.tight_layout()
fig.savefig(SALIDA / "g5-3-costo-por-skill.png", dpi=200)
plt.close(fig)
print("gráficas en", SALIDA)

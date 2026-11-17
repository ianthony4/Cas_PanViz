"""Calcula los indicadores del tablero de evaluación (antes y después) y genera los gráficos.

Fuente única: 07_tablero/datos/*.csv, 05_pruebas/resultados_v*.csv y las actas de la sesión
(06_evidencias/sesion_equipo/*.csv y 04_prototipo/logs/usabilidad.csv).
Uso: python 07_tablero/calcular_indicadores.py
Salida: 07_tablero/datos/indicadores.csv, criterios_calculados.csv, pruebas.csv y graficos/*.png
"""

import csv
import json
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "07_tablero" / "datos"
SESION = RAIZ / "06_evidencias" / "sesion_equipo"
GRAFICOS = RAIZ / "07_tablero" / "graficos"
TOTAL_CRITERIOS, TOTAL_PRUEBAS = 24, 12
ESTADOS = ["Evidenciado", "Parcial", "No evidenciado", "No evaluable"]


def leer(ruta: Path) -> list:
    if not ruta.is_file():
        return []
    with ruta.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def estado_sesion() -> dict:
    """Qué evidencias de la sesión del equipo ya tienen contenido real."""
    rev = leer(SESION / "revisiones.csv")
    ent = leer(SESION / "entrevistas.csv")
    val = leer(SESION / "validacion_usuario.csv")
    usab = leer(RAIZ / "04_prototipo" / "logs" / "usabilidad.csv")
    tareas = {u["tarea"] for u in usab}
    return {
        "E22": bool(rev) and all(r["resultado"].strip() for r in rev),
        "E23": any(e["entrevista"] == "E1" for e in ent) and all(e["respuesta"].strip() for e in ent if e["entrevista"] == "E1"),
        "E24": any(e["entrevista"] == "E2" for e in ent) and all(e["respuesta"].strip() for e in ent if e["entrevista"] == "E2"),
        "E25": bool(val) and all(v["decision"].strip() for v in val) and {"T09", "T10"} <= tareas,
    }


def criterios_calculados(sesion: dict) -> list:
    filas = []
    for c in leer(DATOS / "criterios.csv"):
        despues, evid = c["estado_despues"], [e for e in c["evidencias_despues"].split(";") if e]
        req = [e for e in c["evidencia_sesion"].split(";") if e]
        if req and all(sesion.get(e) for e in req):
            despues = c["estado_si_sesion"]
            evid += req
        filas.append({**c, "estado_despues": despues, "evidencias_despues": ";".join(evid)})
    return filas


def pruebas() -> list:
    filas = []
    for version in ("v1", "v2"):
        for p in leer(RAIZ / "05_pruebas" / f"resultados_{version}.csv"):
            filas.append(p)
    return filas


def indicadores(criterios: list, prs: list) -> list:
    salida = []
    for momento, version in (("Antes", "v1"), ("Después", "v2")):
        col_e = "estado_antes" if momento == "Antes" else "estado_despues"
        col_ev = "evidencias_antes" if momento == "Antes" else "evidencias_despues"
        con_evid = sum(1 for c in criterios if c[col_ev].strip())
        evidenciados = sum(1 for c in criterios if c[col_e] == "Evidenciado")
        p = [x for x in prs if x["version"] == version and x["id"].startswith("T")]
        ejecutadas = [x for x in p if x["resultado"] != "No ejecutada"]
        aprobadas = [x for x in ejecutadas if x["resultado"] == "Aprobada"]
        hall = leer(DATOS / "hallazgos.csv")
        col_h = "estado_antes" if momento == "Antes" else "estado_despues"
        debiles = [h for h in hall if h["tipo"] == "Debilidad" and h[col_h] == "Abierto"]
        salida.append({
            "momento": momento, "version": version,
            "cobertura_documental": round(100 * con_evid / TOTAL_CRITERIOS, 1), "cobertura_num": con_evid,
            "criterios_evidenciados": round(100 * evidenciados / TOTAL_CRITERIOS, 1), "evidenciados_num": evidenciados,
            "ejecucion_pruebas": round(100 * len(ejecutadas) / TOTAL_PRUEBAS, 1), "ejecutadas_num": len(ejecutadas),
            "pendientes_num": TOTAL_PRUEBAS - len(ejecutadas),
            "exito_pruebas": round(100 * len(aprobadas) / len(ejecutadas), 1) if ejecutadas else "Sin datos",
            "aprobadas_num": len(aprobadas),
            "debilidades_abiertas": len(debiles),
        })
    return salida


def escribir(ruta: Path, filas: list) -> None:
    with ruta.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)


def graficos(criterios: list, ind: list) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    GRAFICOS.mkdir(exist_ok=True)
    colores = {"Evidenciado": "#2e7d4f", "Parcial": "#e0a526", "No evidenciado": "#b3261e", "No evaluable": "#8a8f98"}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    areas = ["OPD", "IPM", "RD", "RSKM", "VER", "VAL"]

    fig, ejes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    for eje, (col, titulo) in zip(ejes, (("estado_antes", "Antes (v1)"), ("estado_despues", "Después (v2)"))):
        base = [0] * len(areas)
        for est in ESTADOS:
            vals = [sum(1 for c in criterios if c["area"] == a and c[col] == est) for a in areas]
            eje.bar(areas, vals, bottom=base, color=colores[est], label=est, width=0.6)
            base = [b + v for b, v in zip(base, vals)]
        eje.set_title(titulo)
        eje.set_ylim(0, 4.5)
        eje.spines[["top", "right"]].set_visible(False)
    ejes[0].set_ylabel("Criterios (de 4 por área)")
    ejes[1].legend(loc="upper center", bbox_to_anchor=(-0.05, -0.12), ncol=4, frameon=False)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "criterios_por_area.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    nombres = ["Cobertura\ndocumental", "Criterios\nevidenciados", "Ejecución\nde pruebas", "Éxito\nde pruebas"]
    claves = ["cobertura_documental", "criterios_evidenciados", "ejecucion_pruebas", "exito_pruebas"]
    fig, eje = plt.subplots(figsize=(8, 3.4))
    x = range(len(claves))
    for desplaz, fila, color in ((-0.2, ind[0], "#9fb7cf"), (0.2, ind[1], "#1f5f99")):
        vals = [fila[k] if isinstance(fila[k], (int, float)) else 0 for k in claves]
        barras = eje.bar([i + desplaz for i in x], vals, width=0.38, color=color, label=f"{fila['momento']} ({fila['version']})")
        for b, v in zip(barras, vals):
            eje.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.0f}%", ha="center", fontsize=9)
    eje.set_xticks(list(x), nombres)
    eje.set_ylim(0, 112)
    eje.set_ylabel("%")
    eje.spines[["top", "right"]].set_visible(False)
    eje.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "indicadores_antes_despues.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    sesion = estado_sesion()
    crit = criterios_calculados(sesion)
    prs = pruebas()
    ind = indicadores(crit, prs)
    escribir(DATOS / "criterios_calculados.csv", crit)
    escribir(DATOS / "pruebas.csv", prs)
    escribir(DATOS / "indicadores.csv", ind)
    graficos(crit, ind)
    print("Sesión del equipo:", json.dumps(sesion))
    for fila in ind:
        print(fila)
    print("Estados después:", Counter(c["estado_despues"] for c in crit))


if __name__ == "__main__":
    main()

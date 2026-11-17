"""Construye el documento Grist PANVIZ_Evaluacion a partir de los CSV del tablero.

Requiere una instalación Grist Community (grist-core) local y su API key:
  GRIST_URL=http://localhost:8484 GRIST_KEY=... python 07_tablero/construir_grist.py
Salida: 07_tablero/PANVIZ_Evaluacion.grist y 07_tablero/export_csv/*.csv
Los indicadores se calculan con fórmulas dentro de Grist (no se copian valores).
"""

import csv
import os
import sys
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "07_tablero" / "datos"
URL = os.environ.get("GRIST_URL", "http://localhost:8484")
S = requests.Session()
S.headers["Authorization"] = f"Bearer {os.environ['GRIST_KEY']}"


def api(metodo, ruta, **kw):
    r = S.request(metodo, f"{URL}/api{ruta}", **kw)
    if not r.ok:
        sys.exit(f"{metodo} {ruta} -> {r.status_code}: {r.text[:400]}")
    return r.json() if r.headers.get("content-type", "").startswith("application/json") else r


def leer(nombre):
    with (DATOS / nombre).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def col(id_, tipo="Text", formula=None, label=None, **extra):
    campos = {"type": tipo, "label": label or id_.replace("_", " ")}
    if formula:
        campos.update(formula=formula, isFormula=True)
    campos.update(extra)
    return {"id": id_, "fields": campos}


ESTADOS = '{"choices": ["Evidenciado", "Parcial", "No evidenciado", "No evaluable"]}'
RESULTADOS = '{"choices": ["Aprobada", "Fallida", "No ejecutada"]}'

TABLAS = [
    {"id": "Evidencias", "columns": [
        col("Codigo", label="ID"), col("Tipo"), col("Archivo_o_enlace"), col("Version"), col("Fecha", "Date"),
        col("Autor"), col("Revisor"), col("Flujo"), col("Requiere_sesion", "Bool"),
        col("Criterios_que_respalda", "Any", "Criterios.lookupRecords().filter(lambda c: $id in (c.Evidencia_enlazada or [])) and \", \".join(c.Codigo for c in Criterios.all if $id in [e.id for e in c.Evidencia_enlazada])"),
    ]},
    {"id": "Criterios", "columns": [
        col("Codigo", label="ID"), col("Area", "Choice", widgetOptions='{"choices": ["OPD", "IPM", "RD", "RSKM", "VER", "VAL"]}'),
        col("Descripcion"), col("Responsable"),
        col("Estado", "Choice", widgetOptions=ESTADOS, label="Estado (después)"),
        col("Estado_antes", "Choice", widgetOptions=ESTADOS, label="Estado (antes)"),
        col("Justificacion"),
        col("Evidencia_enlazada", "RefList:Evidencias", label="Evidencia enlazada (después)"),
        col("Evidencia_antes", "RefList:Evidencias", label="Evidencia enlazada (antes)"),
    ]},
    {"id": "Pruebas", "columns": [
        col("Codigo", label="ID"), col("Version"), col("Commit"), col("Requisito"), col("Caracteristica"), col("Entrada"),
        col("Esperado"), col("Observado"), col("Duracion_s", "Numeric"),
        col("Resultado", "Choice", widgetOptions=RESULTADOS), col("Evidencia"),
    ]},
    {"id": "Hallazgos", "columns": [
        col("Codigo", label="ID"), col("Criterio", "Ref:Criterios"), col("Evidencia"),
        col("Tipo", "Choice", widgetOptions='{"choices": ["Debilidad", "Fortaleza", "Oportunidad de mejora"]}'),
        col("Impacto"), col("Observacion"), col("Accion"), col("Responsable"), col("Fecha_objetivo"),
        col("Estado", "Choice", widgetOptions='{"choices": ["Abierto", "Cerrado", "No identificado"]}', label="Estado (después)"),
        col("Estado_antes", "Choice", widgetOptions='{"choices": ["Abierto", "Cerrado", "No identificado"]}', label="Estado (antes)"),
    ]},
    {"id": "Aportes", "columns": [
        col("Criterio", "Ref:Criterios", label="ID de criterio"), col("Descripcion"),
        col("Referencia_evidencia", "Ref:Evidencias", label="Referencia de evidencia"), col("Autor"),
    ]},
    {"id": "Indicadores", "columns": [
        col("Momento"), col("Version"),
        col("Criterios_con_evidencia", "Int",
            "sum(1 for c in Criterios.all if (c.Evidencia_enlazada if $Momento == 'Después' else c.Evidencia_antes))"),
        col("Cobertura_documental", "Numeric", "round(100.0 * $Criterios_con_evidencia / 24, 1)", label="Cobertura documental %"),
        col("Criterios_evidenciados", "Int",
            "sum(1 for c in Criterios.all if (c.Estado if $Momento == 'Después' else c.Estado_antes) == 'Evidenciado')"),
        col("Pct_evidenciados", "Numeric", "round(100.0 * $Criterios_evidenciados / 24, 1)", label="Criterios evidenciados %"),
        col("Pruebas_ejecutadas", "Int",
            "sum(1 for p in Pruebas.lookupRecords(Version=$Version) if p.Codigo.startswith('T') and p.Resultado != 'No ejecutada')"),
        col("Pruebas_pendientes", "Int", "12 - $Pruebas_ejecutadas"),
        col("Ejecucion_pruebas", "Numeric", "round(100.0 * $Pruebas_ejecutadas / 12, 1)", label="Ejecución de pruebas %"),
        col("Exito_pruebas", "Any",
            "ok = sum(1 for p in Pruebas.lookupRecords(Version=$Version) if p.Codigo.startswith('T') and p.Resultado == 'Aprobada')\n"
            "return round(100.0 * ok / $Pruebas_ejecutadas, 1) if $Pruebas_ejecutadas else 'Sin datos'",
            label="Éxito de pruebas %"),
        col("Debilidades_abiertas", "Int",
            "sum(1 for h in Hallazgos.all if h.Tipo == 'Debilidad' and (h.Estado if $Momento == 'Después' else h.Estado_antes) == 'Abierto')"),
    ]},
]


def main():
    ws = api("GET", "/orgs/current/workspaces")[0]["id"]
    for d in api("GET", f"/workspaces/{ws}")["docs"]:
        if d["name"] == "PANVIZ_Evaluacion":
            api("DELETE", f"/docs/{d['id']}")
    doc = api("POST", f"/workspaces/{ws}/docs", json={"name": "PANVIZ_Evaluacion"})
    base = f"/docs/{doc}"
    # la columna calculada de Evidencias depende de Criterios: se crea después
    tablas = [dict(t) for t in TABLAS]
    tablas[0] = {"id": "Evidencias", "columns": [c for c in TABLAS[0]["columns"] if c["id"] != "Criterios_que_respalda"]}
    api("POST", f"{base}/tables", json={"tables": tablas})

    def cargar(tabla, filas):
        ids = []
        for i in range(0, len(filas), 100):
            r = api("POST", f"{base}/tables/{tabla}/records", json={"records": [{"fields": f} for f in filas[i:i + 100]]})
            ids += [x["id"] for x in r["records"]]
        return ids

    evid = leer("evidencias.csv")
    ids_e = dict(zip([e["id"] for e in evid], cargar("Evidencias", [
        {"Codigo": e["id"], "Tipo": e["tipo"], "Archivo_o_enlace": e["archivo"], "Version": e["version"], "Fecha": e["fecha"],
         "Autor": e["autor"], "Revisor": e["revisor"], "Flujo": e["flujo"], "Requiere_sesion": e["requiere_sesion"] == "si"}
        for e in evid])))

    def reflist(texto):
        refs = [ids_e[x] for x in texto.split(";") if x in ids_e]
        return ["L", *refs] if refs else None

    crit = leer("criterios_calculados.csv")
    ids_c = dict(zip([c["id"] for c in crit], cargar("Criterios", [
        {"Codigo": c["id"], "Area": c["area"], "Descripcion": c["descripcion"], "Responsable": c["responsable"],
         "Estado": c["estado_despues"], "Estado_antes": c["estado_antes"], "Justificacion": c["justificacion"],
         "Evidencia_enlazada": reflist(c["evidencias_despues"]), "Evidencia_antes": reflist(c["evidencias_antes"])}
        for c in crit])))

    cargar("Pruebas", [
        {"Codigo": p["id"], "Version": p["version"], "Commit": p["commit"], "Requisito": p["requisito"],
         "Caracteristica": p["caracteristica"], "Entrada": p["entrada"], "Esperado": p["esperado"],
         "Observado": p["observado"], "Duracion_s": float(p["duracion_s"] or 0), "Resultado": p["resultado"],
         "Evidencia": p["evidencia"]} for p in leer("pruebas.csv")])

    cargar("Hallazgos", [
        {"Codigo": h["id"], "Criterio": ids_c.get(h["criterio"]), "Evidencia": h["evidencia"], "Tipo": h["tipo"],
         "Impacto": h["impacto"], "Observacion": h["observacion"], "Accion": h["accion"], "Responsable": h["responsable"],
         "Fecha_objetivo": h["fecha_objetivo"], "Estado": h["estado_despues"], "Estado_antes": h["estado_antes"]}
        for h in leer("hallazgos.csv")])

    aportes_csv = RAIZ / "06_evidencias" / "sesion_equipo" / "aportes.csv"
    aportes = list(csv.DictReader(aportes_csv.open(encoding="utf-8"))) if aportes_csv.is_file() else []
    if aportes:
        cargar("Aportes", [{"Criterio": ids_c.get(a["criterio"]), "Descripcion": a["descripcion"],
                            "Referencia_evidencia": ids_e.get(a["referencia_evidencia"]), "Autor": a["autor"]} for a in aportes])

    cargar("Indicadores", [{"Momento": "Antes", "Version": "v1"}, {"Momento": "Después", "Version": "v2"}])

    api("POST", f"{base}/tables/Evidencias/columns", json={"columns": [
        col("Criterios_que_respalda", "Text",
            "\", \".join(sorted(c.Codigo for c in Criterios.all if $id in [e.id for e in (c.Evidencia_enlazada or [])]))",
            label="Criterios que respalda")]})

    # quitar la tabla vacía por defecto
    tablas_doc = {t["id"] for t in api("GET", f"{base}/tables")["tables"]}
    if "Table1" in tablas_doc:
        api("POST", f"{base}/apply", json=[["RemoveTable", "Table1"]])

    configurar_paginas(base)
    print(doc)


def configurar_paginas(base):
    """Página Tablero (indicadores, gráficos antes/después, hallazgos, criterios con filtros) y formulario."""
    import json as _json

    def g(t):
        return api("GET", f"{base}/tables/{t}/records")["records"]

    def aplicar(acciones):
        return api("POST", f"{base}/apply", json=acciones)["retValues"]

    tabs = {r["fields"]["tableId"]: r["id"] for r in g("_grist_Tables")}
    columnas = g("_grist_Tables_column")
    cols = {(c["fields"]["parentId"], c["fields"]["colId"]): c["id"] for c in columnas}
    por_ref = {v: k for k, v in tabs.items()}
    # las referencias muestran el código (E01, OPD-C1) en lugar del número de fila
    acc = []
    for c in columnas:
        t = c["fields"]["type"]
        if t.startswith(("Ref:", "RefList:")):
            destino = t.split(":")[1]
            acc.append(["UpdateRecord", "_grist_Tables_column", c["id"], {"visibleCol": cols[(tabs[destino], "Codigo")]}])
            acc.append(["SetDisplayFormula", por_ref[c["fields"]["parentId"]], None, c["id"], f"${c['fields']['colId']}.Codigo"])
    aplicar(acc)
    crit, hal = tabs["Criterios"], tabs["Hallazgos"]
    ind = aplicar([["CreateViewSection", tabs["Indicadores"], 0, "record", None, None]])[0]
    vista = ind["viewRef"]
    d, a, h, c = [x["sectionRef"] for x in aplicar([
        ["CreateViewSection", crit, vista, "chart", [cols[(crit, "Area")], cols[(crit, "Estado")]], None],
        ["CreateViewSection", crit, vista, "chart", [cols[(crit, "Area")], cols[(crit, "Estado_antes")]], None],
        ["CreateViewSection", hal, vista, "record", None, None],
        ["CreateViewSection", crit, vista, "record", None, None],
    ])]
    form = aplicar([["CreateViewSection", tabs["Aportes"], 0, "form", None, None]])[0]
    opts = _json.dumps({"multiseries": True, "stacked": True})
    vacio = _json.dumps({"excluded": []})
    aplicar([
        ["UpdateRecord", "_grist_Views", vista, {"name": "Tablero"}],
        ["UpdateRecord", "_grist_Views", form["viewRef"], {"name": "Formulario de aportes"}],
        ["UpdateRecord", "_grist_Views_section", ind["sectionRef"], {"title": "Indicadores (antes y después, calculados con fórmulas)"}],
        ["UpdateRecord", "_grist_Views_section", d, {"title": "Criterios por área y estado · DESPUÉS (v2)", "chartType": "bar", "options": opts}],
        ["UpdateRecord", "_grist_Views_section", a, {"title": "Criterios por área y estado · ANTES (v1)", "chartType": "bar", "options": opts}],
        ["UpdateRecord", "_grist_Views_section", h, {"title": "Hallazgos y acciones (filtrar por responsable)"}],
        ["UpdateRecord", "_grist_Views_section", c, {"title": "Criterios con evidencia enlazada (filtrar por área o responsable)"}],
        ["AddRecord", "_grist_Filters", None, {"viewSectionRef": c, "colRef": cols[(crit, "Area")], "filter": vacio, "pinned": True}],
        ["AddRecord", "_grist_Filters", None, {"viewSectionRef": c, "colRef": cols[(crit, "Responsable")], "filter": vacio, "pinned": True}],
        ["AddRecord", "_grist_Filters", None, {"viewSectionRef": h, "colRef": cols[(hal, "Responsable")], "filter": vacio, "pinned": True}],
        ["AddRecord", "_grist_Filters", None, {"viewSectionRef": h, "colRef": cols[(hal, "Tipo")], "filter": vacio, "pinned": True}],
    ])
    campos = sorted([f for f in g("_grist_Views_section_field") if f["fields"]["parentId"] == form["sectionRef"]],
                    key=lambda f: f["fields"]["parentPos"])
    layout = {"type": "Layout", "children": [
        {"type": "Paragraph", "text": "## **Registro de aportes · PANVIZ**", "alignment": "center"},
        {"type": "Paragraph", "text": "Cada integrante registra al menos tres aportes: el criterio que respalda, qué aportó y la evidencia del índice. El coordinador consolida y revisa duplicados.", "alignment": "center"},
        {"type": "Section", "children": [{"type": "Paragraph", "text": "### Aporte"}] + [{"type": "Field", "leaf": f["id"]} for f in campos]},
        {"type": "Submit"}]}
    aplicar([["UpdateRecord", "_grist_Views_section", form["sectionRef"], {"title": "Registro de aportes por estudiante", "layoutSpec": _json.dumps(layout)}]])


if __name__ == "__main__":
    main()

"""Genera el informe (Word) y datos.json para la presentación, a partir de los datos del trabajo.

Uso (desde la raíz del paquete): python 08_informe/generar_informe.py
Antes conviene ejecutar 07_tablero/calcular_indicadores.py para refrescar indicadores.
Las secciones que dependen de la sesión del equipo (entrevistas, revisión cruzada,
validación con usuario, T09/T10) se redactan según lo que contengan las actas.
"""

import csv
import json
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "08_informe"
NEGRO = RGBColor(0, 0, 0)


def leer(rel):
    ruta = RAIZ / rel
    if not ruta.is_file():
        return []
    with ruta.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- datos
def reunir():
    ind = {f["momento"]: f for f in leer("07_tablero/datos/indicadores.csv")}
    crit = leer("07_tablero/datos/criterios_calculados.csv")
    pr = {v: {p["id"]: p for p in leer(f"05_pruebas/resultados_{v}.csv")} for v in ("v1", "v2")}
    hall = leer("07_tablero/datos/hallazgos.csv")
    evid = leer("07_tablero/datos/evidencias.csv")
    ent = leer("06_evidencias/sesion_equipo/entrevistas.csv")
    rev = leer("06_evidencias/sesion_equipo/revisiones.csv")
    val = leer("06_evidencias/sesion_equipo/validacion_usuario.csv")
    usab = leer("04_prototipo/logs/usabilidad.csv")
    aportes = leer("06_evidencias/sesion_equipo/aportes.csv")
    obs_t03 = json.loads(pr["v2"]["T03"]["observado"] or "{}") if pr["v2"].get("T03") else {}
    obs_t04 = json.loads(pr["v2"]["T04"]["observado"] or "{}") if pr["v2"].get("T04") else {}
    sesion = {
        "entrevistas_hechas": bool(ent) and all(e["respuesta"].strip() for e in ent),
        "revisiones_hechas": bool(rev) and all(r["resultado"].strip() for r in rev),
        "validacion_hecha": bool(val) and all(v["decision"].strip() for v in val),
        "tareas": {u["tarea"]: u for u in usab},
    }
    areas = ["OPD", "IPM", "RD", "RSKM", "VER", "VAL"]
    estados = ["Evidenciado", "Parcial", "No evidenciado", "No evaluable"]
    por_area = {m: {a: {e: sum(1 for c in crit if c["area"] == a and c[col] == e) for e in estados} for a in areas}
                for m, col in (("antes", "estado_antes"), ("despues", "estado_despues"))}
    return dict(ind=ind, crit=crit, pr=pr, hall=hall, evid=evid, ent=ent, rev=rev, val=val, usab=usab,
                aportes=aportes, sesion=sesion, por_area=por_area, t03=obs_t03, t04=obs_t04)


# ---------------------------------------------------------------- formato
def preparar(doc):
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.top_margin = sec.bottom_margin = Cm(2.5)
    sec.left_margin = sec.right_margin = Cm(2.5)
    for nombre in ("Normal", "Heading 1", "Heading 2", "Heading 3", "Caption", "Title"):
        st = doc.styles[nombre]
        st.font.name = "Times New Roman"
        st.font.color.rgb = NEGRO
        st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        st.element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
        st.element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
        st.font.size = Pt(12)
    doc.styles["Normal"].paragraph_format.space_after = Pt(6)
    doc.styles["Normal"].paragraph_format.line_spacing = 1.15
    for nombre in ("Heading 1", "Heading 2"):
        st = doc.styles[nombre]
        st.font.bold = True
        st.font.italic = False
        st.paragraph_format.space_before = Pt(12 if nombre == "Heading 1" else 8)
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.keep_with_next = True
    # número de página al pie
    pie = sec.footer.paragraphs[0]
    pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = pie.add_run()
    for tag, texto in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = texto
        run._r.append(el)
    run.font.name, run.font.size, run.font.color.rgb = "Times New Roman", Pt(12), NEGRO


def h(doc, texto, nivel=1):
    p = doc.add_heading(texto, level=nivel)
    for r in p.runs:
        r.font.color.rgb, r.font.name, r.font.size = NEGRO, "Times New Roman", Pt(12)
    return p


def p(doc, texto, negrita_inicio=None):
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if negrita_inicio:
        r = par.add_run(negrita_inicio); r.bold = True
    par.add_run(texto)
    return par


def tabla(doc, filas, anchos=None, tam=10):
    t = doc.add_table(rows=len(filas), cols=len(filas[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    if anchos:
        t.autofit = False
        total = sum(anchos)
        anchos = [a * 16.0 / total for a in anchos]  # ajusta al ancho útil (16 cm)
        for j, col_ in enumerate(t.columns):
            col_.width = Cm(anchos[j])
        grid = t._tbl.tblGrid
        for j, gc in enumerate(grid.findall(qn("w:gridCol"))):
            gc.set(qn("w:w"), str(int(anchos[j] * 567)))
    for i, fila in enumerate(filas):
        for j, valor in enumerate(fila):
            celda = t.cell(i, j)
            celda.text = ""
            par = celda.paragraphs[0]
            par.paragraph_format.space_after = Pt(0)
            par.paragraph_format.line_spacing = 1.0
            run = par.add_run(str(valor))
            run.font.size, run.font.name, run.font.color.rgb = Pt(tam), "Times New Roman", NEGRO
            run.bold = i == 0
            if anchos:
                celda.width = Cm(anchos[j])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def leyenda(doc, texto):
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = par.add_run(texto); r.italic = True; r.font.size = Pt(10)
    return par


def figura(doc, ruta, ancho_cm, texto):
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.add_run().add_picture(str(ruta), width=Cm(ancho_cm))
    leyenda(doc, texto)


def pct(v):
    return f"{float(v):.1f} %".replace(".", ",") if v not in ("Sin datos", "") else "sin datos"


# ---------------------------------------------------------------- redacción
def redactar(doc, d):
    ia, idp = d["ind"]["Antes"], d["ind"]["Después"]
    s = d["sesion"]
    t09, t10 = s["tareas"].get("T09"), s["tareas"].get("T10")

    h(doc, "1. Introducción y alcance")
    p(doc, "Este informe presenta el piloto de adopción de procesos orientado a CMMI nivel 3 que el Equipo 04 desarrolló sobre "
      "PANVIZ, un sistema de salud pública que consolida registros de vigilancia epidemiológica. El caso trabaja la vigilancia "
      "de Infecciones Respiratorias Agudas (IRAS) en la Red Arequipa y la provincia de Caylloma, sobre el sistema y los datos "
      "del trabajo anterior del equipo. El responsable de vigilancia recibe notificaciones con campos incompletos, identificadores repetidos y fechas mal escritas, y necesita un tablero por distrito "
      "y grupo etario que le permita revisar la información antes de publicarla.")
    p(doc, "El trabajo combina dos frentes. Por un lado, el equipo definió un proceso estándar, lo adaptó a dos flujos de trabajo y "
      "reunió evidencia verificable de seis áreas de proceso de CMMI DEV v1.3: OPD, IPM, RD, RSKM, VER y VAL. Por otro lado, "
      "construyó un incremento pequeño del producto: un validador de importación con tablero, que se midió con doce pruebas "
      "basadas en ISO/IEC 25010:2023. La evaluación es una autoevaluación académica inspirada en SCAMPI C. No es una evaluación "
      "oficial y no demuestra que PANVIZ alcance el nivel 3. Las etiquetas que usamos para los criterios tampoco son calificaciones "
      "oficiales de SCAMPI.")
    p(doc, "Se trabajó solo con datos sintéticos: 30 notificaciones de IRAS con identificador, fecha, establecimiento, distrito, "
      "grupo etario, evento y estado de validación, de las cuales 6 son inválidas y tienen una causa conocida. Las 20 primeras "
      "provienen del dataset sintético original del equipo (15 válidas y 5 inválidas) y se agregaron 10 para llegar a las 30 que "
      "pide el enunciado. Esas 10 incorporan dos distritos de Caylloma (Majes y Chivay) y un distrito fuera del ámbito como sexto "
      "caso inválido. Los grupos etarios son las seis categorías MINSA del catálogo original. El tablero destaca los dos grupos que "
      "interesan al caso: la población infantil (menores de 5 años) y los adultos mayores (60 años a más).")

    h(doc, "2. Referentes y decisiones de método")
    p(doc, "Usamos CMMI DEV v1.3 como referencia histórica coherente con SCAMPI. En ese modelo, cubrir hasta el nivel 3 exige 18 áreas "
      "de proceso: siete de nivel 2 y once de nivel 3. En este piloto solo se muestrean seis áreas de nivel 3. Las áreas de nivel 2 "
      "(gestión de requisitos, planificación, seguimiento, configuración, aseguramiento de calidad, medición y gestión de "
      "proveedores) se registran como dependencias y no se evalúan.")
    p(doc, "La lectura principal fue el artículo técnico de la TMMi Foundation sobre el nuevo Método de Evaluación (MDD) y TAMAR "
      "(2023), en sus secciones de tipos de evaluación, fases y muestreo. De ella salieron tres decisiones. La primera fue tratar "
      "nuestro ejercicio como una evaluación de tipo Evaluation, la categoría del MDD que reemplaza a SCAMPI B y C. Ese tipo no "
      "produce calificaciones y admite el mayor grado de adaptación, lo que justifica trabajar con 24 criterios propios. La segunda "
      "fue seguir las tres fases que el MDD conserva de SCAMPI (planificar y preparar, conducir, y reportar) con un enfoque basado "
      "en verificación: primero se indexó la evidencia y después se verificó, combinando entrevistas con demostraciones en vivo. "
      "La tercera fue aplicar la idea de muestreo aleatorio: los dos flujos hacen de \"proyectos muestreados\" y, para la revisión "
      "cruzada, se sortearon 8 de las 21 evidencias documentales con una semilla fija (2026), de modo que otro grupo pueda repetir "
      "la selección.")
    p(doc, "Como complemento actual usamos la nota de calidad del CMMI Institute sobre hallazgos de evaluación (marzo de 2026). La nota "
      "recuerda que las debilidades se reportan siempre que existan, que no deben disfrazarse de oportunidades de mejora y que el "
      "simple cumplimiento de una práctica no es una fortaleza. Aplicamos esas tres reglas al redactar los hallazgos. De ISO/IEC "
      "33002:2015 tomamos la estructura del registro de la evaluación (propósito, alcance, muestra, responsables, evidencias y "
      "resultados), sin declarar conformidad completa con la norma. ISO/IEC 25010:2023 sirvió para elegir seis características de "
      "calidad del producto. Los umbrales usados son decisiones académicas, no exigencias numéricas de ISO ni de CMMI.")

    h(doc, "3. Proceso estándar y adaptación")
    p(doc, "El proceso estándar del equipo (PE-04) tiene seis actividades encadenadas: requisitos, riesgos, implementación, revisión, "
      "pruebas y cierre del ciclo. Para cada actividad se definieron sus entradas, lo que se hace, su salida, un responsable y quién "
      "la revisa. Se crearon plantillas de requisito, de revisión y de caso de prueba, una convención de nombres para archivos e "
      "identificadores, y una regla de versiones: etiquetas git en el código y número de versión en la cabecera de cada documento. "
      "Todo cambio registra su motivo, quién lo revisó y quién lo aprobó.")
    p(doc, "El mismo estándar se aplicó a los dos flujos del piloto. El flujo F1 (captura y validación) cubre la importación, las reglas "
      "y la persistencia. El flujo F2 (consolidación y visualización) cubre el resumen, la publicación protegida y la interfaz. "
      "La adaptación justificada es que la validación con usuario solo se exige en F2. F1 no tiene una interfaz propia y su "
      "resultado (qué registros se aceptan y cuáles se rechazan) se puede comprobar exactamente contra un oráculo calculado a mano. "
      "F2, en cambio, presenta información a una persona que debe decidir si la publica.")
    p(doc, "Al verificar la primera versión del prototipo aparecieron dos fallas reales y una debilidad de nuestras propias pruebas, que "
      "se describen en la sección 6. Las tres tenían algo en común: el proceso v1 no obligaba a pensar en la reimportación de "
      "datos ni a revisar la seguridad de la interfaz. Por eso la lección no se quedó en el código. Se publicó el proceso PE-04 v2, "
      "que agrega tres controles: los requisitos deben decir qué ocurre cuando un dato vuelve a llegar inválido, la lista de "
      "revisión exige escapar todo dato externo antes de mostrarlo, y toda prueba que actúe como oráculo debe ser revisada por otro "
      "integrante. Ese cambio quedó registrado como CP-01, con su motivo, su revisor y su aprobación.")

    h(doc, "4. Plan, muestra y criterios de preparación")
    p(doc, "El plan de evaluación (1–2 páginas) define el propósito, el alcance, los roles, las reglas de confidencialidad, la muestra y "
      "el cronograma. El equipo tiene cuatro integrantes y el enunciado propone cinco roles, así que el rol de evidencias y tablero "
      "se repartió. La revisión cruzada sigue un ciclo cerrado en el que nadie revisa su propio trabajo.")
    tabla(doc, [
        ["Integrante", "Responsabilidad principal", "Revisa a"],
        ["Anthony Chaisa", "Coordinación: plan, OPD, IPM, integración del informe", "Alexander (pruebas)"],
        ["Mario Champi", "Requisitos y riesgos (RD, RSKM), tablero Grist y usuario simulado", "Anthony (plan)"],
        ["Jael Huarca", "Implementación del prototipo, versiones y README", "Mario (trazabilidad y tablero)"],
        ["Alexander Villafuerte", "Doce pruebas, entrevistas y acta de usuario", "Jael (código y logs)"],
    ], anchos=[4, 8.5, 4])
    p(doc, "Para cada área se definieron cuatro criterios observables, 24 en total: que el activo exista, que se haya aplicado, que otro "
      "integrante lo haya revisado y que haya un registro de mejora o seguimiento. Cada criterio se clasifica como Evidenciado, "
      "Parcial, No evidenciado o No evaluable, con su justificación y un enlace a la evidencia. Se indexaron 26 evidencias. "
      "Veintiuna son documentales o de ejecución y se generaron durante el trabajo. Las otras cinco son las actas de la sesión del "
      "equipo: revisión cruzada, dos entrevistas y validación con usuario. Toda la trazabilidad usa una sola cadena: requisito, "
      "criterio de proceso, evidencia, prueba, hallazgo y acción. Por ejemplo, R4 (persistencia sin duplicados) se enlaza con el "
      "criterio VER-C4, la evidencia E16 (registro de defectos), las pruebas T05 y D01, el hallazgo H01 y la acción A01.")

    h(doc, "5. Incremento implementado")
    p(doc, "Ante la ausencia del código original de PANVIZ, se construyó un microprototipo reproducible en Python con una interfaz web "
      "local (FastAPI). Parte del sistema del trabajo anterior del equipo sobre IRAS: se mantuvieron su esquema de datos y su "
      "catálogo, y se rehicieron los módulos para cumplir esta actividad. El importador verifica que el CSV tenga las columnas "
      "obligatorias. El validador aplica seis reglas, cada una como una función independiente en un único módulo: campos "
      "obligatorios, fecha real en formato AAAA-MM-DD, evento igual a IRAS, grupo etario del catálogo MINSA, distrito dentro de "
      "Arequipa o Caylloma y, desde el cambio CR-01, fecha no futura. Aparte de esas reglas, el validador controla los "
      "duplicados por identificador. Los registros aceptados se guardan en disco con escritura atómica y se resumen por distrito "
      "y grupo etario. Los rechazados se muestran en una tabla separada, con su causa y un botón para corregirlos.")
    p(doc, "La operación de publicación está protegida. El permiso se comprueba en la lógica del servidor y no en la pantalla: un "
      "digitador puede importar y corregir, pero solo el responsable de vigilancia puede publicar, y cada intento queda en un log "
      "de acceso. Como el prototipo no tiene autenticación, el alcance de esta protección es local y así se declara: el usuario se "
      "identifica por nombre y su rol se resuelve en el servidor. Con los 30 registros sintéticos, el tablero muestra 24 casos "
      "aceptados en nueve distritos (10 en menores de 5 años y 6 en adultos de 60 años a más) y 6 rechazados con su causa. Estos valores coinciden con el cálculo manual que "
      "se hizo antes de ejecutar el programa.")
    figura(doc, RAIZ / "06_evidencias/capturas/v2_01_tablero_importado.png", 12,
           "Figura 1. Tablero del prototipo (v2.0) después de importar los 30 registros sintéticos.")

    h(doc, "6. Medición de la calidad del producto")
    p(doc, f"Se diseñaron dos pruebas por cada una de las seis características elegidas, doce en total. Diez están automatizadas con "
      f"pytest y dos (T09 y T10) requieren a un usuario simulado, al que la propia aplicación le mide el tiempo y los pasos. Cada "
      f"ejecución genera un registro con el requisito, la versión y el commit evaluados, los datos de entrada, el resultado esperado, "
      f"el observado, la duración y el resultado. Una prueba no ejecutada se mantiene visible y no se cuenta como aprobada. "
      f"El entorno fue Linux con Python 3.13. La importación de 30 filas tardó como máximo {d['t03'].get('maximo_s', '—')} s en "
      f"tres repeticiones y la actualización del resumen {d['t04'].get('maximo_s', '—')} s, muy por debajo de la meta de 2 s.")
    filas = [["Prueba", "Característica", "Meta", "v1.0", "v2.0"]]
    for tid in [f"T{i:02d}" for i in range(1, 13)] + ["D01", "D02"]:
        a, b = d["pr"]["v1"].get(tid, {}), d["pr"]["v2"].get(tid, {})
        filas.append([tid, b.get("caracteristica", ""), b.get("esperado", ""), a.get("resultado", "—"), b.get("resultado", "—")])
    tabla(doc, filas, anchos=[1.5, 3.8, 7.6, 2, 2], tam=9)
    leyenda(doc, "Tabla 2. Resultados de las pruebas antes (v1.0) y después (v2.0). Fuente: 05_pruebas/resultados_v1.csv y resultados_v2.csv.")
    p(doc, "Las doce pruebas planificadas no encontraron fallas en v1: las nueve que se pudieron ejecutar pasaron. Las fallas aparecieron "
      "en la verificación exploratoria y en la revisión de la interfaz, y ambas son reales. La primera (D01) surgió al importar un "
      "lote corregido en el que el registro IRAS-2026-001 llegaba con una fecha inexistente. El lote lo rechazó, pero el conjunto "
      "aceptado lo seguía conservando, de modo que el mismo identificador figuraba a la vez como aceptado y como rechazado, y el "
      "tablero contaba 4 casos en Cerro Colorado en lugar de 3. La causa era doble: el código unía los lotes sin retirar los "
      "rechazados, y el requisito R4 no decía qué hacer en ese caso. La segunda (D02) surgió al importar un CSV con una etiqueta "
      "HTML en el grupo etario: la tabla de rechazados la interpretaba como código y el navegador la ejecutaba. Como hubo fallas "
      "reales, no fue necesario introducir una versión defectuosa como experimento controlado.")
    p(doc, "Se escribieron dos pruebas de regresión que reproducen esas fallas y que fallan sobre v1.0. Después se corrigieron las causas, "
      "se aclaró R4 y se volvieron a ejecutar todas las pruebas sobre v2.0. Al escribir la prueba D02 encontramos además una "
      "debilidad en nuestra propia verificación: la primera versión de esa prueba marcaba como inseguras expresiones que ya estaban "
      "escapadas. Ese falso positivo se corrigió y quedó registrado como hallazgo, porque muestra que una prueba también puede "
      "estar equivocada. En la misma versión se incorporó la regla de fecha no futura modificando solo el módulo de reglas, y la "
      "prueba de mantenibilidad comprobó que la vista no cambió.")
    if t09 and t10:
        p(doc, f"Con el usuario simulado, la tarea T09 (corregir un registro rechazado) tomó {t09['segundos']} s y {t09['pasos']} pasos, "
          f"y la tarea T10 (localizar el resumen de un distrito) tomó {t10['segundos']} s y {t10['pasos']} pasos, ambas sin ayuda "
          f"del desarrollador. Observaciones del usuario: {t09['observacion'] or 'ninguna'}; {t10['observacion'] or 'ninguna'}.")
    else:
        p(doc, "Las pruebas T09 y T10 siguen sin ejecutar porque requieren la sesión con el usuario simulado. Figuran así en el registro "
          "y no se cuentan como aprobadas.")
    figura(doc, RAIZ / "06_evidencias/capturas/v1_05_prueba_inyeccion.png", 10,
           "Figura 2. Falla D02 en v1.0: el valor del CSV se ejecuta como HTML (título de la página cambiado y dos imágenes inyectadas).")

    h(doc, "7. Evaluación simulada y hallazgos")
    if s["revisiones_hechas"]:
        obs = "; ".join(f"{r['revisor']} sobre {r['autor']}: {r['resultado'].lower()}" + (f" ({r['observaciones']})" if r['observaciones'] else "")
                        for r in d["rev"])
        p(doc, f"La revisión cruzada siguió el ciclo definido en el plan, sobre la muestra aleatoria de evidencias. Resultados: {obs}.")
    else:
        p(doc, "La revisión cruzada sigue el ciclo definido en el plan y trabaja sobre la muestra aleatoria de evidencias (E04, E08, E11, "
          "E13, E14, E17, E20 y E26). Sus actas están preparadas, pero aún no tienen resultado, por lo que los cinco criterios de "
          "revisión por otro integrante figuran como No evidenciado.")
    if s["entrevistas_hechas"]:
        for clave, tema in (("E1", "el uso del proceso"), ("E2", "la validación de resultados")):
            filas_e = [e for e in d["ent"] if e["entrevista"] == clave]
            disc = [e["discrepancia"] for e in filas_e if e["discrepancia"].strip()]
            p(doc, f"La entrevista {clave}, sobre {tema}, fue conducida por {filas_e[0]['entrevistador']} con {filas_e[0]['entrevistado']}. "
              f"De sus {len(filas_e)} preguntas, {sum(1 for e in filas_e if e['evidencia_corroborada'].strip())} se corroboraron con "
              f"evidencia o con una demostración. " + (f"Discrepancias registradas: {'; '.join(disc)}." if disc else "No se registraron discrepancias."))
    else:
        p(doc, "Las dos entrevistas de cinco minutos (uso del proceso y validación de resultados) tienen su guía de preguntas, junto con la "
          "evidencia que cada respuesta debe corroborar. Al cierre de esta versión aún no tienen respuestas registradas.")
    if s["validacion_hecha"]:
        dec = "; ".join(f"{v['escenario']}: {v['decision']}" + (f" ({v['observacion']})" if v['observacion'] else "") for v in d["val"])
        p(doc, f"En la validación con el usuario simulado se obtuvieron estas decisiones: {dec}.")
    p(doc, "Los hallazgos se redactaron con su criterio, su evidencia, la observación, el impacto y la acción, y se clasificaron siguiendo "
      "la nota de 2026. Se registraron seis debilidades, una fortaleza y una oportunidad de mejora. Las dos fallas del producto se "
      "presentan como debilidades de verificación y de requisitos, no como detalles técnicos. La única fortaleza es una práctica "
      "que va más allá del cumplimiento: el oráculo se calculó a mano antes de ejecutar el código y cada prueba registra sola su "
      "valor observado, de modo que otro grupo puede repetir todo con un comando y compararlo con datos independientes del "
      "programa. Como los evaluadores son también autores, la independencia es limitada. Esa limitación se declara y se registra "
      "como una debilidad abierta.")
    filas = [["ID", "Tipo", "Criterio", "Observación", "Acción", "Estado"]]
    for x in d["hall"]:
        filas.append([x["id"], x["tipo"], x["criterio"], x["observacion"], x["accion"], x["estado_despues"]])
    tabla(doc, filas, anchos=[1, 2.2, 1.6, 6.2, 4.5, 1.5], tam=8)
    leyenda(doc, "Tabla 3. Hallazgos y acciones. Fuente: 07_tablero/datos/hallazgos.csv.")

    h(doc, "8. Tablero de control e indicadores")
    p(doc, "El tablero de la evaluación se construyó en Grist Community (licencia Apache 2.0), en una instalación local. El documento "
      "PANVIZ_Evaluacion tiene las tablas Criterios, Evidencias, Pruebas, Hallazgos y Aportes, todas relacionadas entre sí, y un "
      "formulario para que cada estudiante registre sus aportes. Los cinco indicadores no se copian como valores: son fórmulas "
      "dentro de Grist que se recalculan sobre las tablas. Para comprobarlos, también se calcularon con un script de Python "
      "independiente, y los dos cálculos coinciden. El tablero filtra por área y por responsable, y desde cada criterio se puede "
      "abrir el registro de la evidencia enlazada. El estado antes y el estado después se miden con la misma muestra de 24 "
      "criterios y las mismas reglas.")
    tabla(doc, [
        ["Indicador", "Antes (v1)", "Después (v2)"],
        ["Cobertura documental (criterios con evidencia válida / 24)", f"{pct(ia['cobertura_documental'])} ({ia['cobertura_num']}/24)", f"{pct(idp['cobertura_documental'])} ({idp['cobertura_num']}/24)"],
        ["Criterios evidenciados / 24", f"{pct(ia['criterios_evidenciados'])} ({ia['evidenciados_num']}/24)", f"{pct(idp['criterios_evidenciados'])} ({idp['evidenciados_num']}/24)"],
        ["Ejecución de pruebas / 12", f"{pct(ia['ejecucion_pruebas'])} ({ia['pendientes_num']} pendientes)", f"{pct(idp['ejecucion_pruebas'])} ({idp['pendientes_num']} pendientes)"],
        ["Éxito de pruebas (aprobadas / ejecutadas)", pct(ia["exito_pruebas"]), pct(idp["exito_pruebas"])],
        ["Debilidades abiertas", ia["debilidades_abiertas"], idp["debilidades_abiertas"]],
    ], anchos=[8.5, 4, 4])
    leyenda(doc, "Tabla 4. Indicadores del tablero. Fuente: Grist PANVIZ_Evaluacion y 07_tablero/datos/indicadores.csv.")
    figura(doc, RAIZ / "07_tablero/graficos/criterios_por_area.png", 13.5,
           "Figura 3. Estado de los 24 criterios por área, antes y después de la mejora.")
    p(doc, "La mejora se concentra en los criterios de seguimiento y mejora (OPD-C4, RD-C4, RSKM-C4 y VER-C4), que dependían de corregir "
      "las fallas y de publicar el proceso v2. Los criterios que siguen sin evidencia dependen de las actas de la sesión del equipo. "
      "Un indicador en verde no equivale a nivel 3: el tablero mide la preparación del piloto, no la madurez de la organización.")

    h(doc, "9. Plan de mejora y limitaciones")
    p(doc, "Se priorizaron tres acciones abiertas, cada una con un responsable y un plazo:")
    tabla(doc, [
        ["Acción", "Hallazgo", "Responsable", "Plazo"],
        ["A1. Toda prueba nueva que actúe como oráculo pasa por la revisión de otro integrante antes de usarse", "H03", "Alexander Villafuerte", "7 días (23/11/2026)"],
        ["A3. Repetir los escenarios VAL-1 y VAL-2 con un usuario externo al equipo", "H06", "Mario Champi", "7 días (23/11/2026)"],
        ["A2. Aplicar el proceso PE-04 v2 en un segundo proyecto y registrar su adaptación y sus mejoras", "H05", "Anthony Chaisa", "30 días (16/12/2026)"],
    ], anchos=[9, 2.3, 3.2, 3])
    p(doc, "Esta evaluación tiene dos limitaciones de muestra. La primera es que todo ocurrió en un solo equipo de cuatro personas, en "
      "un solo día, y que los evaluadores son también autores, así que no hay independencia real ni evidencia de uso sostenido "
      "del proceso. La segunda es que el producto se midió con 30 registros sintéticos en un entorno local, con un usuario "
      "simulado que pertenece al equipo, por lo que los tiempos y la usabilidad no se pueden extrapolar a una operación real.")
    p(doc, "Para una adopción organizacional sostenida harían falta al menos dos evidencias adicionales. La primera son registros de uso "
      "del proceso estándar en varios proyectos y durante varios ciclos, con mejoras aprobadas por un grupo responsable de los "
      "procesos. Eso respaldaría OPD y OPF a escala organizacional. La segunda es evidencia de las áreas de nivel 2 de las que "
      "depende el nivel 3, en particular auditorías de aseguramiento de calidad hechas por alguien ajeno al equipo y una serie "
      "histórica de mediciones.")

    h(doc, "10. Conclusiones")
    p(doc, "El piloto mostró que un proceso estándar pequeño, aplicado con disciplina, deja rastro verificable: cada requisito llega a "
      "una prueba, cada falla a un hallazgo y cada hallazgo a una acción con responsable. Lo más valioso no fueron las pruebas que "
      "pasaron, sino las dos fallas reales que encontró la verificación. Ambas revelaron brechas del proceso (un requisito "
      "incompleto y una lista de revisión sin control de seguridad) y terminaron cambiando el estándar, no solo el código. Los "
      f"indicadores pasaron de {pct(ia['criterios_evidenciados'])} a {pct(idp['criterios_evidenciados'])} de criterios evidenciados y "
      f"de {ia['debilidades_abiertas']} a {idp['debilidades_abiertas']} debilidades abiertas. Aun así, quedan pendientes la "
      "independencia de la evaluación, la validación con un usuario externo y la evidencia de uso sostenido, que son las "
      "condiciones que separan este piloto de una adopción real de nivel 3.")

    h(doc, "Referencias")
    for ref in [
        "[1] Balla, K., Cannegieter, J. J. y van Veenendaal, E. (2023). The New MDD and TAMAR. TMMi Foundation.",
        "[2] CMMI Institute (17 de marzo de 2026). Quality Tip: Appraisal Findings.",
        "[3] ISO/IEC 33002:2015. Information technology — Process assessment — Requirements for performing process assessment (confirmada en 2026).",
        "[4] ISO/IEC 25010:2023. Systems and software engineering — Product quality model.",
        "[5] CMMI Institute. Levels of Capability and Performance; Appraisal types. cmmiinstitute.com.",
        "[6] Grist Labs. Grist Community Edition (grist-core, licencia Apache 2.0) y Grist Desktop. support.getgrist.com.",
    ]:
        par = p(doc, ref)
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT


def anexos(doc, d):
    par = doc.add_paragraph(); par.add_run().add_break(WD_BREAK.PAGE)
    h(doc, "Anexo A. Matriz de los 24 criterios")
    filas = [["ID", "Criterio", "Antes", "Después", "Evidencia", "Justificación"]]
    for c in d["crit"]:
        filas.append([c["id"], c["descripcion"], c["estado_antes"], c["estado_despues"], c["evidencias_despues"].replace(";", ", ") or "—", c["justificacion"]])
    tabla(doc, filas, anchos=[1.6, 5, 1.9, 1.9, 2.2, 4.4], tam=8)
    h(doc, "Anexo B. Índice de evidencias")
    filas = [["ID", "Tipo", "Archivo", "Versión", "Autor", "Revisor", "Flujo"]]
    for e in d["evid"]:
        filas.append([e["id"], e["tipo"], e["archivo"], e["version"], e["autor"], e["revisor"], e["flujo"]])
    tabla(doc, filas, anchos=[1, 2.2, 5.6, 1.4, 2.6, 2.6, 1.2], tam=8)
    h(doc, "Anexo C. Actas de la sesión del equipo")
    if d["ent"] and any(e["respuesta"].strip() for e in d["ent"]):
        filas = [["Entr.", "Pregunta", "Respuesta", "Evidencia corroborada", "Discrepancia"]]
        for e in d["ent"]:
            filas.append([e["entrevista"], e["pregunta"], e["respuesta"], e["evidencia_corroborada"], e["discrepancia"]])
        tabla(doc, filas, anchos=[1.2, 4.5, 5.5, 3, 2.6], tam=8)
    else:
        p(doc, "Las guías de entrevista, las actas de revisión cruzada y el acta de validación están en 06_evidencias/sesion_equipo/ y se "
          "integran aquí al registrarse.")
    h(doc, "Anexo D. Registro de aportes por estudiante")
    if d["aportes"]:
        filas = [["Autor", "Criterio", "Descripción", "Evidencia"]] + [[a["autor"], a["criterio"], a["descripcion"], a["referencia_evidencia"]] for a in d["aportes"]]
        tabla(doc, filas, anchos=[3.5, 2, 8.5, 2], tam=8)
    else:
        p(doc, "Los aportes se registran con el formulario de Grist (página \"Formulario de aportes\") o en 06_evidencias/sesion_equipo/aportes.csv.")


def recortes():
    """Recortes de capturas para la presentación (08_informe/img)."""
    from PIL import Image
    (SALIDA / "img").mkdir(exist_ok=True)
    for origen, caja, destino in [
        ("06_evidencias/capturas/v1_05_prueba_inyeccion.png", "inferior", "d02_v1.png"),
        ("06_evidencias/capturas/v2_05_prueba_inyeccion.png", "inferior", "d02_v2.png"),
        ("06_evidencias/capturas/v2_03_publicacion_denegada.png", (0, 0, 1280, 420), "publicacion_denegada.png"),
        ("07_tablero/capturas/grist_01_tablero.png", (245, 60, 1345, 800), "grist_tablero.png"),
    ]:
        im = Image.open(RAIZ / origen)
        if caja == "inferior":  # fila inyectada y leyenda: zona inferior de la captura
            caja = (80, im.height - 345, 1280, im.height - 25)
        im.crop(caja).save(SALIDA / "img" / destino)


def main():
    recortes()
    d = reunir()
    datos = dict(d)
    (SALIDA / "datos.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    doc = Document()
    preparar(doc)
    redactar(doc, d)
    anexos(doc, d)
    destino = SALIDA / "Informe_Equipo04_PANVIZ.docx"
    doc.save(destino)
    print(destino)


if __name__ == "__main__":
    main()

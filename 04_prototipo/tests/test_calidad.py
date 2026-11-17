"""Pruebas T01-T12 por característica ISO/IEC 25010:2023.

Adecuación funcional: T01, T02 · Eficiencia de desempeño: T03, T04
Fiabilidad: T05, T06 · Seguridad: T07, T08
Capacidad de interacción: T09, T10 · Mantenibilidad: T11, T12
"""

import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

import pytest

from src import config, reglas, servicio
from src.seguridad import PermisoDenegado
from src.validador import validar
from src.importador import importar_csv

ROOT = Path(__file__).resolve().parent.parent
DATOS = config.ARCHIVO_ENTRADA_DEFAULT
LIMITE_SEGUNDOS = 2.0
LIMITE_TAREA = 90.0


def _sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


# ---------------- Adecuación funcional ----------------

def test_t01_rechaza_seis_invalidos_sembrados(entorno, oraculo, observar):
    """R2: los 6 registros inválidos sembrados se rechazan con su causa; los 24 válidos se aceptan."""
    r = servicio.importar(DATOS)
    rech = {(x["fila_datos"], x["campo"]) for x in servicio.estado()["rechazados"]}
    esperado = {(x["fila_datos"], x["campo"]) for x in oraculo["invalidos_sembrados"]}
    observar({"aceptados": r["aceptados_en_archivo"], "rechazados": r["rechazados"],
              "detectados_del_oraculo": len(rech & esperado), "falsos_rechazos": len(rech - esperado)})
    assert rech == esperado
    assert r["aceptados_en_archivo"] == oraculo["aceptados"]


def test_t02_totales_por_distrito_igual_calculo_manual(entorno, oraculo, observar):
    """R3: los casos por distrito y grupo etario coinciden con el cálculo manual del oráculo."""
    servicio.importar(DATOS)
    resumen = {f["distrito"]: f for f in servicio.estado()["resumen"]}
    diferencias = []
    for d, esp in oraculo["totales_por_distrito"].items():
        obs = resumen.get(d, {})
        for k, v in esp.items():
            if obs.get(k) != v:
                diferencias.append(f"{d}.{k}: esperado {v}, observado {obs.get(k)}")
    extra = set(resumen) - set(oraculo["totales_por_distrito"])
    total = sum(f["casos"] for f in resumen.values())
    infantil = sum(f["infantil_menor_5"] for f in resumen.values())
    mayor = sum(f["adulto_mayor_60"] for f in resumen.values())
    observar({"casos_total": total, "menores_5": infantil, "60_a_mas": mayor, "distritos": len(resumen),
              "diferencias": diferencias, "distritos_extra": sorted(extra)})
    assert not diferencias and not extra
    assert total == oraculo["aceptados"]
    assert infantil == oraculo["poblacion_infantil_menor_5"] and mayor == oraculo["adulto_mayor_60_mas"]


# ---------------- Eficiencia de desempeño ----------------

def test_t03_tiempo_importacion_30_filas(entorno, observar):
    """Importar 30 filas en <= 2 s (3 repeticiones, se informa el máximo)."""
    tiempos = []
    for _ in range(3):
        servicio.reiniciar_estado()
        t = time.perf_counter(); servicio.importar(DATOS); tiempos.append(time.perf_counter() - t)
    observar({"tiempos_s": [round(x, 4) for x in tiempos], "maximo_s": round(max(tiempos), 4),
              "entorno": f"{platform.system()} {platform.release()} / Python {platform.python_version()} / {platform.processor() or platform.machine()}"})
    assert max(tiempos) <= LIMITE_SEGUNDOS


def test_t04_tiempo_actualizacion_resumen(entorno, observar):
    """Actualizar el resumen (corrección + reimportación + resumen) en <= 2 s, 3 repeticiones."""
    servicio.importar(DATOS)
    tiempos = []
    for _ in range(3):
        t = time.perf_counter()
        servicio.corregir(20, "grupo_etario", "DESCONOCIDO")  # misma corrección: mismo trabajo en cada repetición
        servicio.estado()
        tiempos.append(time.perf_counter() - t)
    observar({"tiempos_s": [round(x, 4) for x in tiempos], "maximo_s": round(max(tiempos), 4)})
    assert max(tiempos) <= LIMITE_SEGUNDOS


# ---------------- Fiabilidad ----------------

def test_t05_importar_dos_veces_no_duplica(entorno, oraculo, observar):
    """Importar dos veces el mismo archivo no duplica ni pierde registros aceptados."""
    servicio.importar(DATOS)
    antes = servicio.estado()
    servicio.importar(DATOS)
    despues = servicio.estado()
    ids = [r["id"] for r in json.loads(config.ARCHIVO_ACEPTADOS.read_text(encoding="utf-8"))]
    casos = sum(f["casos"] for f in despues["resumen"])
    observar({"aceptados_antes": antes["aceptados"], "aceptados_despues": despues["aceptados"],
              "ids_unicos": len(set(ids)), "casos_en_resumen": casos})
    assert antes["aceptados"] == despues["aceptados"] == oraculo["aceptados"]
    assert len(ids) == len(set(ids))
    assert casos == oraculo["aceptados"]


def test_t06_reinicio_recupera_ultimo_conjunto(entorno, oraculo, observar):
    """Tras reiniciar el proceso se recupera el último conjunto aceptado y el publicado."""
    servicio.importar(DATOS)
    servicio.publicar("resp.vigilancia")
    env = dict(os.environ, PANVIZ_ESTADO_DIR=str(config.ESTADO_DIR), PANVIZ_LOGS_DIR=str(config.LOGS_DIR))
    codigo = ("import json; from src import servicio; e = servicio.estado(); "
              "print(json.dumps({'aceptados': e['aceptados'], 'publicado': len(e['publicado']['registros']), "
              "'version': e['publicado']['version']}))")
    salida = subprocess.run([sys.executable, "-c", codigo], cwd=ROOT, env=env, capture_output=True, text=True, check=True)
    nuevo = json.loads(salida.stdout)
    observar({"proceso_nuevo": nuevo, "archivos": sorted(p.name for p in config.ESTADO_DIR.iterdir())})
    assert nuevo["aceptados"] == oraculo["aceptados"]
    assert nuevo["publicado"] == oraculo["aceptados"] and nuevo["version"] == 1


# ---------------- Seguridad ----------------

def test_t07_publicacion_sin_permiso_denegada(entorno, observar):
    """Un usuario sin permiso no puede publicar; la denegación queda en el log de acceso."""
    from fastapi.testclient import TestClient
    from src.web import app
    servicio.importar(DATOS)
    with pytest.raises(PermisoDenegado):
        servicio.publicar("digitador01")
    http = TestClient(app).post("/api/publicar", json={"usuario": "digitador01"})
    desconocido = TestClient(app).post("/api/publicar", json={"usuario": "intruso"})
    log = config.LOG_ACCESO.read_text(encoding="utf-8").strip().splitlines()
    denegados = [l for l in log if l.endswith("DENEGADO") and "publicar" in l]
    observar({"http_digitador": http.status_code, "http_desconocido": desconocido.status_code,
              "lineas_denegadas_en_log": len(denegados), "ultima_linea": log[-1]})
    assert http.status_code == 403 and desconocido.status_code == 403
    assert len(denegados) == 3


def test_t08_rechazo_no_modifica_publicado(entorno, observar):
    """La publicación denegada no cambia el conjunto publicado (comparación de hash)."""
    servicio.importar(DATOS)
    servicio.publicar("resp.vigilancia")
    h0 = _sha(config.ARCHIVO_PUBLICADO)
    servicio.corregir(17, "establecimiento", "CS Cerro Colorado")  # cambia el conjunto aceptado
    with pytest.raises(PermisoDenegado):
        servicio.publicar("digitador01")
    h1 = _sha(config.ARCHIVO_PUBLICADO)
    publicado = json.loads(config.ARCHIVO_PUBLICADO.read_text(encoding="utf-8"))
    observar({"hash_antes": h0[:16], "hash_despues": h1[:16], "version": publicado["version"],
              "registros_publicados": len(publicado["registros"]), "aceptados_actuales": servicio.estado()["aceptados"]})
    assert h0 == h1 and publicado["version"] == 1


# ---------------- Capacidad de interacción ----------------

def _tarea_registrada(tarea: str):
    log = ROOT / "logs" / "usabilidad.csv"
    if not log.is_file():
        return None
    filas = [f for f in csv.DictReader(log.open(encoding="utf-8")) if f["tarea"] == tarea]
    return filas[-1] if filas else None


@pytest.mark.parametrize("tarea", ["T09", "T10"])
def test_t09_t10_tareas_de_usuario(tarea, observar):
    """T09: identificar y corregir un error. T10: localizar el resumen de un distrito. Meta <= 90 s sin ayuda."""
    fila = _tarea_registrada(tarea)
    if fila is None:
        pytest.skip(f"{tarea} no ejecutada: no hay sesión registrada en logs/usabilidad.csv")
    observar({tarea: fila})
    assert fila["completada"] == "True"
    assert float(fila["segundos"]) <= LIMITE_TAREA


# ---------------- Mantenibilidad ----------------

def test_t11_nueva_regla_sin_modificar_vista(entorno, observar):
    """Se añade una regla de validación en reglas.py sin cambiar la vista (web.py / index.html)."""
    regla = getattr(reglas, "regla_fecha_no_futura", None)
    if regla is None or regla not in reglas.REGLAS:
        pytest.skip("T11 no ejecutada: la regla regla_fecha_no_futura aún no se ha incorporado")
    futura = {"id": "X", "fecha_notificacion": "2029-01-01", "establecimiento": "CS Francisco Bolognesi",
              "distrito": "Cayma", "grupo_etario": "60 años a más", "evento": "IRAS", "_fila": 1}
    res = validar([futura])
    vista = {p: _sha(ROOT / p)[:16] for p in ("src/web.py", "src/templates/index.html")}
    referencias = [p for p in ("src/web.py", "src/templates/index.html")
                   if "regla_" in (ROOT / p).read_text(encoding="utf-8")]
    observar({"rechazo_futuro": res.rechazados[0].motivo if res.rechazados else None,
              "hash_vista": vista, "vista_referencia_reglas": referencias})
    assert res.rechazados and res.rechazados[0].campo == "fecha_notificacion"
    assert not referencias


def test_t12_regresion_tras_cambio(entorno, oraculo, observar):
    """Regresión: tras el cambio, el flujo completo sigue cumpliendo el oráculo y la seguridad."""
    r = servicio.importar(DATOS)
    servicio.importar(DATOS)
    e = servicio.estado()
    resumen = {f["distrito"]: f["casos"] for f in e["resumen"]}
    esperado = {d: v["casos"] for d, v in oraculo["totales_por_distrito"].items()}
    denegado = False
    try:
        servicio.publicar("digitador01")
    except PermisoDenegado:
        denegado = True
    observar({"rechazados": r["rechazados"], "aceptados": e["aceptados"], "resumen_ok": resumen == esperado,
              "publicacion_denegada": denegado})
    assert r["rechazados"] == oraculo["rechazados"] and e["aceptados"] == oraculo["aceptados"]
    assert resumen == esperado and denegado

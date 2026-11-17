"""Servidor web local de PANVIZ IRAS (FastAPI)."""

import csv
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from src import config, servicio
from src.importador import ErrorContrato
from src.seguridad import PermisoDenegado

app = FastAPI(title="PANVIZ IRAS", version="2.0")
PLANTILLA = Path(__file__).resolve().parent / "templates" / "index.html"


class Correccion(BaseModel):
    fila: int
    campo: str
    valor: str
    usuario: str


class Publicacion(BaseModel):
    usuario: str


class EventoTarea(BaseModel):
    tarea: str
    participante: str
    segundos: float
    pasos: int
    completada: bool
    observacion: str = ""


@app.get("/", response_class=HTMLResponse)
def inicio():
    return PLANTILLA.read_text(encoding="utf-8")


@app.get("/api/estado")
def api_estado(distrito: Optional[str] = None):
    return servicio.estado(distrito or None)


@app.get("/api/usuarios")
def api_usuarios():
    return config.USUARIOS


@app.post("/api/importar")
async def api_importar(usuario: str = Form(...), archivo: Optional[UploadFile] = File(None)):
    try:
        if archivo is None or not archivo.filename:
            return servicio.importar(config.ARCHIVO_ENTRADA_DEFAULT, usuario)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            shutil.copyfileobj(archivo.file, tmp)
        return servicio.importar(tmp.name, usuario)
    except PermisoDenegado as e:
        raise HTTPException(403, str(e))
    except ErrorContrato as e:
        raise HTTPException(400, str(e))


@app.post("/api/corregir")
def api_corregir(c: Correccion):
    try:
        return servicio.corregir(c.fila, c.campo, c.valor, c.usuario)
    except PermisoDenegado as e:
        raise HTTPException(403, str(e))
    except (ValueError, FileNotFoundError) as e:
        raise HTTPException(400, str(e))


@app.post("/api/publicar")
def api_publicar(p: Publicacion):
    try:
        pub = servicio.publicar(p.usuario)
        return {"version": pub["version"], "registros": len(pub["registros"])}
    except PermisoDenegado as e:
        raise HTTPException(403, str(e))


@app.post("/api/tarea")
def api_tarea(e: EventoTarea):
    """Registra la medición de una tarea de usuario (T09/T10)."""
    config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    nuevo = not config.LOG_USABILIDAD.is_file()
    with config.LOG_USABILIDAD.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["fecha", "tarea", "participante", "segundos", "pasos", "completada", "observacion"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), e.tarea, e.participante,
                    round(e.segundos, 1), e.pasos, e.completada, e.observacion])
    return {"ok": True}

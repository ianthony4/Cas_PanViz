"""Punto de entrada por consola.

Ejemplos:
  python -m src.app importar datos/iras_sinteticos_30.csv
  python -m src.app resumen
  python -m src.app publicar --usuario resp.vigilancia
  python -m src.app servidor
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import config, servicio
from src.seguridad import PermisoDenegado


def main() -> int:
    p = argparse.ArgumentParser(description="PANVIZ IRAS - prototipo local")
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("importar"); i.add_argument("archivo", nargs="?", default=str(config.ARCHIVO_ENTRADA_DEFAULT)); i.add_argument("--usuario", default="digitador01")
    r = sub.add_parser("resumen"); r.add_argument("--distrito")
    pb = sub.add_parser("publicar"); pb.add_argument("--usuario", required=True)
    sub.add_parser("reiniciar")
    s = sub.add_parser("servidor"); s.add_argument("--puerto", type=int, default=8000)
    a = p.parse_args()

    try:
        if a.cmd == "importar":
            print(json.dumps(servicio.importar(a.archivo, a.usuario), ensure_ascii=False, indent=2))
        elif a.cmd == "resumen":
            e = servicio.estado(a.distrito)
            print(f"Aceptados: {e['aceptados']}  Rechazados: {len(e['rechazados'])}")
            for f in e["resumen"]:
                print(f"  {f['distrito']:<30} casos={f['casos']:>2} menores_5={f['infantil_menor_5']:>2} "
                      f"60_a_mas={f['adulto_mayor_60']:>2}")
            for x in e["rechazados"]:
                print(f"  RECHAZO fila {x['fila_datos']:>2} {x['id']}: {x['motivo']}")
        elif a.cmd == "publicar":
            pub = servicio.publicar(a.usuario)
            print(f"Publicada versión {pub['version']} con {len(pub['registros'])} registros")
        elif a.cmd == "reiniciar":
            servicio.reiniciar_estado(); print("Estado borrado")
        elif a.cmd == "servidor":
            import uvicorn
            uvicorn.run("src.web:app", host="127.0.0.1", port=a.puerto)
    except PermisoDenegado as e:
        print(f"DENEGADO: {e}"); return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

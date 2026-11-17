"""Muestra aleatoria reproducible de evidencias para la revisión cruzada (semilla 2026)."""
import csv, random
from pathlib import Path
ids = [r["id"] for r in csv.DictReader((Path(__file__).parent / "datos" / "evidencias.csv").open(encoding="utf-8"))
       if r["requiere_sesion"] == "no"]
print(", ".join(sorted(random.Random(2026).sample(ids, 8))))

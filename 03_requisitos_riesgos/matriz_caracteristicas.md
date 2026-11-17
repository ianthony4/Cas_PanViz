# Matriz de relación: características de calidad, requisitos, pruebas, evidencias y áreas

La calidad del producto aporta evidencia sobre el proceso, pero no determina un nivel de madurez. Cada vínculo de esta tabla se justifica con la evidencia indicada.

| Característica ISO/IEC 25010:2023 | Requisito | Pruebas | Evidencia | Área VER/VAL | Vínculo con RD / RSKM |
|---|---|---|---|---|---|
| Adecuación funcional | R2, R3 | T01, T02 | E10, E14, E15 | VER | **RD:** el oráculo de T01 y T02 sale de los criterios de aceptación de R2 y R3 (RD-C2) |
| Eficiencia de desempeño | R1, R3 | T03, T04 | E15 (tiempos medidos) | VER | RSKM: RK3 (plazo) se mitigó automatizando las mediciones |
| Fiabilidad | R4 | T05, T06, D01 | E15, E16 | VER | **RSKM:** RK1 se materializó como D01, y **RD:** obligó a aclarar R4 (CRQ-01) |
| Seguridad | R5 | T07, T08, D02 | E17, E18, E16 | VER | **RSKM:** RK4 se materializó en la interfaz (D02) y se controló en v2 |
| Capacidad de interacción | R6 | T09, T10 | E25 (log de usabilidad y acta) | VAL | RSKM: RK5 (independencia limitada) afecta la validez de esta medición |
| Mantenibilidad | R2, R1–R5 | T11, T12 | E12 (diff de `reglas.py`), E15 | VER | **RD:** la solicitud CR-01 se resolvió cambiando un solo archivo |

**Lectura de la matriz.** Las dos fallas reales (D01 y D02) no fueron solo errores de programación. D01 muestra una brecha de **RD**, porque el requisito R4 no cubría la reimportación. D02 muestra una brecha de **VER**, porque la lista de revisión no tenía un ítem de seguridad de interfaz. Por eso las dos generaron cambios en el proceso (PE-04 v2) y no solo en el código.

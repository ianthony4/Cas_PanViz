# Escenarios de validación (VAL) con usuario simulado

**Usuario simulado:** responsable de vigilancia distrital, interpretado por Mario Champi · **Facilitador:** Alexander Villafuerte

La validación responde a una pregunta distinta de la verificación: no si el sistema cumple lo especificado, sino si **sirve para lo que el usuario necesita**, que es revisar la información antes de publicarla.

| Escenario | Situación | Tarea del usuario | Criterio de aceptación | Prueba asociada |
|---|---|---|---|---|
| VAL-1 | Un lunes llega el lote de la semana y el usuario debe decidir si los datos de Majes (Caylloma) son confiables | Encontrar el resumen de Majes y leer cuántos casos hay en total, en menores de 1 año y en 60 años a más (3, 1 y 1) | Lo encuentra en 90 s o menos, sin ayuda, y lee bien los tres valores | T10 |
| VAL-2 | El lote trae una notificación sin establecimiento (IRAS-2026-017, fila 17) y el usuario sabe que corresponde a "CS Cerro Colorado" | Encontrar el rechazado, corregirlo y publicar como responsable | Lo corrige en 90 s o menos, el registro pasa a aceptados (25) y la publicación se crea | T09 |

**Regla de decisión.** El usuario acepta un escenario si cumple su criterio y considera que la información le permite decidir. Si lo rechaza, la observación se registra como hallazgo de VAL y se le asigna una acción.

# Requisitos del incremento PANVIZ IRAS

**Versión:** 1.1 · **Fecha:** 16/11/2026 · **Elaboró:** Mario Champi · **Revisa:** Jael Huarca

**Necesidad del usuario.** El responsable de vigilancia recibe notificaciones de IRAS de establecimientos de la Red Arequipa y de Caylloma. Le interesan sobre todo la población infantil (menores de 5 años) y los adultos mayores (60 años a más). Algunas llegan incompletas, otras repetidas y otras con fechas mal escritas. Necesita revisar, antes de publicar, un tablero que muestre solo información confiable por distrito y por grupo etario, sin perder de vista qué se rechazó y por qué.

| ID | Flujo | Requisito | Criterio de aceptación | Característica | Pruebas | Riesgo |
|---|---|---|---|---|---|---|
| R1 | F1 | El sistema importa un CSV con las columnas id, fecha_notificacion, establecimiento, distrito, grupo_etario y evento, y rechaza archivos sin esas columnas | Las 30 filas se procesan en menos de 2 s y un archivo sin columnas obligatorias muestra un error claro | Desempeño | T03, T12 | RK3 |
| R2 | F1 | Cada registro se valida con estas reglas: campos obligatorios, fecha real en formato AAAA-MM-DD, ID no duplicado, evento igual a IRAS, grupo etario del catálogo MINSA (6 categorías) y distrito dentro de Arequipa o Caylloma. Desde CR-01 también se exige que la fecha no sea futura | Los 6 inválidos sembrados se rechazan con su causa exacta y ningún válido se rechaza | Adecuación funcional, mantenibilidad | T01, T11 | RK1 |
| R3 | F2 | El tablero muestra solo registros aceptados, agrupados por distrito y grupo etario, y los rechazados en una tabla aparte con su causa | Los casos coinciden con el cálculo manual: 24 casos en 9 distritos, 10 en menores de 5 años y 6 en 60 años a más | Adecuación funcional, desempeño | T02, T04 | RK2 |
| R4 | F1 | El conjunto aceptado se guarda en disco, se recupera después de reiniciar y no se duplica al reimportar. **(v1.1)** Si un ID aceptado antes llega inválido en un lote nuevo, sale del conjunto aceptado | Importar dos veces da 24 registros, el reinicio recupera 24 y ningún ID queda aceptado y rechazado a la vez | Fiabilidad | T05, T06, D01 | RK1 |
| R5 | F2 | Solo un usuario con rol responsable puede publicar. La comprobación se hace en la lógica del servidor y cada intento queda registrado | Un digitador recibe "denegado", el conjunto publicado no cambia y el log registra el intento | Seguridad | T07, T08, D02 | RK4 |
| R6 | F2 | Un usuario sin capacitación puede corregir un rechazado y encontrar el resumen de un distrito | Cada tarea toma 90 s o menos, sin ayuda | Capacidad de interacción | T09, T10 | RK5 |

**Cambios:** v1.0, versión inicial. v1.1 aclara R4 por el hallazgo H01 y agrega la regla RV6 a R2 por la solicitud CR-01.

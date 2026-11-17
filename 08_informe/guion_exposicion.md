# Guion de exposición · Equipo 04 · PANVIZ IRAS

**Duración:** 12 minutos de exposición y 5 de preguntas. Acompaña a `Presentacion_Equipo04_PANVIZ.pptx` (21 diapositivas).

| Bloque | Diapositivas | Tiempo | Expone |
|---|---|---|---|
| Contexto y alcance | 1–5 | 1 min 30 s | Anthony |
| Proceso estándar y adaptación | 6–8 | 2 min | Jael |
| Evidencia y evaluación | 9–12 | 2 min | Mario |
| Demostración del incremento y del tablero | 13–18 | 4 min | Jael (13–14), Alexander (15–17), Mario (18) |
| Resultados y plan de mejora | 19–20 | 1 min 30 s | Anthony |
| Limitaciones y cierre | 21 | 1 min | Alexander |

**Antes de empezar:**
- Dejen abiertos el prototipo (`python -m src.app servidor`, en http://127.0.0.1:8000) y Grist Desktop con `PANVIZ_Evaluacion.grist`, en la página Tablero.
- Si algo falla en vivo, usen las capturas de las diapositivas 14, 15, 17 y 18 como respaldo.

> Este guion refleja el estado actual del trabajo. Si llegan a hacer la sesión del equipo (entrevistas, revisión cruzada, T09 y T10), cambien las frases marcadas con **[si se hizo la sesión]**.

---

## Bloque 1 · Contexto y alcance (Anthony, 1 min 30 s)

### Diapositiva 1 · Portada
Buenos días. Somos el Equipo 04: Mario Champi, Jael Huarca, Alexander Villafuerte y yo, Anthony Chaisa. Vamos a presentar la revisión SCAMPI de un piloto de adopción de procesos orientado a CMMI nivel 3, aplicado a PANVIZ, un sistema de vigilancia de Infecciones Respiratorias Agudas. Antes de empezar, una aclaración importante: esto es una autoevaluación académica inspirada en SCAMPI C. No es una evaluación oficial y no demuestra que PANVIZ sea nivel 3.

### Diapositiva 2 · Notificaciones de IRAS que llegan con errores
El problema de partida es simple. El responsable de vigilancia recibe notificaciones de IRAS que no se pueden publicar tal como llegan: algunas vienen sin establecimiento, otras repetidas y otras con fechas que no existen. Él necesita ver casos confiables por distrito y por grupo de edad, en especial de los niños menores de cinco años y de los adultos mayores. Trabajamos con 30 notificaciones sintéticas. Las primeras 20 son las de nuestro trabajo anterior y agregamos diez para incluir Caylloma. Seis de las 30 son inválidas a propósito, y conocemos la causa de cada una.

### Diapositiva 3 · Qué evaluamos y qué quedó fuera
CMMI hasta el nivel 3 tiene 18 áreas de proceso. Nosotros evaluamos seis, las que ven en color: OPD, IPM, RD, RSKM, VER y VAL. Las áreas de nivel 2 quedaron solo como dependencias. El trabajo se dividió en dos flujos: el primero captura y valida los registros, y el segundo los consolida, los muestra y los publica.

### Diapositiva 4 · Equipo y roles
El enunciado pedía cinco roles y somos cuatro, así que repartimos el de evidencias y tablero entre Mario y yo. Cada uno revisa el trabajo de otro, en ciclo, para que nadie se revise a sí mismo. Lo decimos desde ya: como todos somos autores, la independencia de la evaluación es limitada.

### Diapositiva 5 · Tres decisiones de la lectura
De la lectura de TMMi sobre el nuevo método de evaluación tomamos tres decisiones:
- Tratar el trabajo como una evaluación de tipo *Evaluation*, que reemplaza a SCAMPI B y C y no da calificación.
- Seguir sus tres fases y verificar la evidencia antes de concluir.
- Usar muestreo aleatorio: sorteamos ocho evidencias con una semilla fija, para que otro grupo pueda repetir la selección.

De la nota del CMMI Institute de este año aplicamos dos reglas: una debilidad no se disfraza de oportunidad de mejora, y cumplir lo mínimo no se presenta como fortaleza. Le paso la palabra a Jael.

---

## Bloque 2 · Proceso estándar (Jael, 2 min)

### Diapositiva 6 · Proceso estándar PE-04
Nuestro proceso estándar tiene seis actividades: requisitos, riesgos, implementación, revisión, pruebas y cierre. Cada una tiene un dueño y alguien distinto que la revisa. Para que todo sea rastreable usamos plantillas e identificadores en una sola cadena, desde el requisito hasta la acción. El código se versiona con git: la versión 1 es el "antes" y la versión 2 es el "después".

### Diapositiva 7 · Un estándar, dos flujos
El mismo proceso se aplicó a los dos flujos y solo adaptamos una cosa, la adaptación A-01. En el flujo de captura no hay una pantalla que validar con un usuario, porque lo que importa es qué registros se aceptan y cuáles se rechazan, y eso se comprueba exactamente contra un resultado calculado a mano. Por eso la validación con usuario se hace solo en el flujo de visualización, donde una persona tiene que decidir si publica.

### Diapositiva 8 · Lo que aprendimos cambió el proceso
Esta es, para nosotros, la parte más importante. Al probar la versión 1 encontramos dos fallas reales, que Alexander va a mostrar. Las dos tenían una causa en el proceso, no solo en el código: el proceso no obligaba a pensar qué pasa cuando un dato vuelve a llegar, ni a revisar la seguridad de la pantalla. Por eso publicamos el proceso versión 2, con tres controles nuevos. Ese cambio quedó registrado con su motivo, quién lo revisó y quién lo aprobó. Le paso la palabra a Mario.

---

## Bloque 3 · Evidencia y evaluación (Mario, 2 min)

### Diapositiva 9 · 24 criterios
Para cada área nos hicimos cuatro preguntas: ¿existe el activo?, ¿se aplicó?, ¿lo revisó otro integrante? y ¿hay una mejora o un seguimiento? Eso da 24 criterios. Hoy 15 están evidenciados, uno es parcial y ocho no tienen evidencia. Esos ocho son casi todos de revisión por otro integrante y de validación con usuario, y dependen de una sesión del equipo que no pudimos completar. **[si se hizo la sesión: "que completamos en la sesión del equipo"]**

### Diapositiva 10 · Trazabilidad
Les muestro un ejemplo real de la cadena. El requisito R4 pide guardar los datos sin duplicar. Se mide con el criterio VER-C4, su evidencia es el registro de defectos E16, lo prueban T05 y D01, generó el hallazgo H01 y terminó en la acción A01, que ya está cerrada. Los seis requisitos tienen esa cadena completa.

### Diapositiva 11 · Evidencias y muestra
Indexamos 26 evidencias, cada una con archivo, versión, fecha, autor y revisor. Veintiuna son documentos o resultados de ejecución, y cinco son las actas de la sesión del equipo. Para la revisión cruzada sorteamos ocho. Como ven, las actas de entrevistas, revisión y validación figuran como pendientes. Preferimos mostrarlas así antes que presentar algo que no ocurrió.

### Diapositiva 12 · Antes y después
Con la misma muestra y las mismas reglas, los criterios evidenciados pasaron de 9 a 15 de 24. Lo que mejoró son los criterios de seguimiento y mejora, que dependían de corregir las fallas y de publicar el proceso versión 2. Un aviso: que un indicador esté en verde no significa nivel 3. Mide la preparación del piloto, no la madurez de una organización. Jael empieza la demostración.

---

## Bloque 4 · Demostración (4 min)

### Diapositiva 13 · El incremento (Jael)
El incremento es un validador de importación. Tiene seis reglas, cada una en una función aparte: campos obligatorios, fecha real, que el evento sea IRAS, grupo etario del catálogo MINSA, distrito dentro de Arequipa o Caylloma y, desde un cambio solicitado, que la fecha no sea futura. Además controla los identificadores duplicados. Con las 30 notificaciones acepta 24 y rechaza 6. De los aceptados, 10 son niños menores de cinco años y 6 son adultos de 60 a más. No hay ninguna diferencia con el cálculo que hicimos a mano antes de programar.

### Diapositiva 14 · Demostración en vivo (Jael)
*(Cambiar a la aplicación.)* Importo el archivo y aparecen 24 aceptados y 6 rechazados. Arriba está el resumen por distrito y por grupo de edad. Abajo, los rechazados con su causa: un ID repetido, un establecimiento vacío, una fecha que no existe, un evento que no es IRAS, un grupo etario que no está en el catálogo y un distrito fuera del ámbito. Filtro por Majes, en Caylloma: tiene tres casos, uno de ellos de un adulto mayor. Corrijo el registro sin establecimiento y pasa a aceptados. Le paso la palabra a Alexander.

### Diapositiva 15 · Publicación protegida (Alexander)
La publicación solo la puede hacer el responsable de vigilancia, y el permiso se revisa en el servidor, no solo en la pantalla. *(En vivo: elegir digitador01 y pulsar Publicar.)* Como ven, el digitador recibe "operación denegada" y el intento queda en el registro de accesos. La prueba T07 lo comprueba y la T08 verifica que, tras ese intento, lo publicado no cambió ni un byte. No tenemos inicio de sesión real, así que declaramos que esta protección es solo local.

### Diapositiva 16 · Doce pruebas
Diseñamos dos pruebas por cada una de las seis características de calidad de ISO 25010. Las diez automatizadas pasan en la versión 2. T09 y T10 miden a un usuario resolviendo tareas en menos de 90 segundos, y siguen como "no ejecutadas". **[si se hizo la sesión: "las medimos y tomaron X y Y segundos"]** No las contamos como aprobadas. Abajo están D01 y D02, que fallan en la versión 1 y pasan en la 2.

### Diapositiva 17 · Dos fallas reales (Alexander)
La primera falla, D01: si llegaba un lote corregido en el que un registro ya aceptado venía inválido, el sistema lo rechazaba pero lo seguía contando. Cerro Colorado mostraba 4 casos cuando eran 3. La causa estaba en el código y también en el requisito, que no decía qué hacer en ese caso. La segunda, D02: si el archivo traía código HTML, la tabla de rechazados lo ejecutaba. Aquí ven que en la versión 1 se ejecuta y en la versión 2 se muestra como texto. Las dos se reprodujeron con pruebas antes de corregirlas. Además, al escribir la prueba de D02 descubrimos que nuestra propia prueba daba falsos positivos, y eso también quedó como hallazgo. Mario muestra el tablero.

### Diapositiva 18 · Tablero en Grist (Mario)
*(Cambiar a Grist Desktop, página Tablero.)* Este es el tablero de la evaluación, en Grist Community, que es software libre. Las tablas de criterios, evidencias, pruebas y hallazgos están enlazadas, y los indicadores son fórmulas, no números copiados. Además los recalculamos con un script aparte y salen iguales. Filtro por área, por ejemplo VER, y desde un criterio abro directamente su evidencia. Los cambios: cobertura de 54 a 67 %, criterios evidenciados de 38 a 63 %, pruebas ejecutadas de 75 a 83 % y debilidades abiertas de 5 a 3. Anthony presenta los resultados.

---

## Bloque 5 · Resultados y plan de mejora (Anthony, 1 min 30 s)

### Diapositiva 19 · Hallazgos
Registramos seis debilidades, una fortaleza y una oportunidad de mejora:
- Tres debilidades ya están cerradas: las dos fallas del producto y la falta de controles en el proceso versión 1.
- Siguen abiertas tres: la prueba con falsos positivos, que el proceso solo se usó un día en un solo equipo, y que el usuario y los revisores somos los mismos autores.

La única fortaleza la consideramos así porque va más allá de cumplir: el resultado esperado se calculó a mano antes de programar y cada prueba registra sola lo que observó, así que cualquiera puede repetir todo con un comando.

### Diapositiva 20 · Plan de mejora
Priorizamos tres acciones:
- A siete días: que otro integrante revise toda prueba nueva antes de usarla, y repetir la validación con un usuario que no sea del equipo.
- A treinta días: aplicar el proceso versión 2 en un segundo proyecto.

Para una adopción de verdad faltarían dos evidencias: uso del proceso durante varios ciclos y proyectos, y auditorías de calidad hechas por alguien externo. Alexander cierra.

---

## Bloque 6 · Limitaciones y cierre (Alexander, 1 min)

### Diapositiva 21 · Limitaciones y conclusión
Tenemos dos limitaciones. La primera: fue un solo equipo, en un solo día, evaluando su propio trabajo. La segunda: el producto se midió con 30 registros sintéticos en una computadora local y con un usuario simulado, así que los tiempos no se pueden trasladar a una operación real.

Nuestra conclusión es que lo más valioso no fueron las pruebas que pasaron, sino las dos fallas que encontró la verificación. Esas fallas mostraron huecos en el proceso y terminaron cambiando el estándar, no solo el código. Muchas gracias. Quedamos atentos a sus preguntas.

---

## Preguntas probables (5 min)

**¿Esto demuestra que PANVIZ es nivel 3?**
No. Es una autoevaluación académica de seis de las 18 áreas. El nivel 3 exige procesos definidos a escala organizacional y sostenidos en el tiempo, y eso no lo tenemos.

**¿Por qué no indujeron una falla como pedía el enunciado?**
El enunciado pide inducirla solo si todas las pruebas pasan. Nosotros encontramos dos fallas reales en la versión 1, así que no hizo falta.

**¿Por qué T09 y T10 no están ejecutadas?**
Necesitan a una persona haciendo las tareas mientras se mide el tiempo, y no pudimos reunirnos todos. Preferimos dejarlas visibles como no ejecutadas antes que inventar tiempos. La aplicación ya trae el cronómetro para medirlas.

**¿Cuál es la diferencia entre verificación y validación aquí?**
La verificación comprueba que construimos lo especificado: las 12 pruebas contra el resultado calculado a mano. La validación comprueba que sirve para lo que el usuario necesita: los escenarios en los que el responsable revisa un distrito y corrige un registro antes de publicar.

**¿Por qué Grist?**
Es libre (Apache 2.0), funciona sin cuenta en la computadora, permite tablas enlazadas, formularios y gráficos, y sus indicadores son fórmulas, así que se pueden recalcular.

**¿De dónde salen los datos?**
Son sintéticos. Las primeras 20 notificaciones son las de nuestro trabajo anterior sobre IRAS y agregamos 10 para llegar a 30 e incluir Caylloma. No usamos datos reales de personas.

### Evidencia que cada uno debe saber ubicar (una que no elaboró)
- **Anthony:** los resultados de las pruebas de la versión 2 (`05_pruebas/resultados_v2.csv`), elaborados por Alexander.
- **Mario:** el commit que corrigió D01 (`f3ec0b8`, en `06_evidencias/historial_git.txt`), elaborado por Jael.
- **Jael:** la matriz de trazabilidad (`03_requisitos_riesgos/matriz_trazabilidad.csv`), elaborada por Mario.
- **Alexander:** el proceso estándar versión 2 (`02_procesos/proceso_estandar_v2.md`), elaborado por Anthony.

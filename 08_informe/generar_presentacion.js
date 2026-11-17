// Genera la presentación (21 diapositivas, fondo blanco) desde 08_informe/datos.json.
// Uso: NODE_PATH=<carpeta con pptxgenjs> node 08_informe/generar_presentacion.js
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const RAIZ = path.resolve(__dirname, "..");
const D = JSON.parse(fs.readFileSync(path.join(__dirname, "datos.json"), "utf8"));
const SALIDA = path.join(__dirname, "Presentacion_Equipo04_PANVIZ.pptx");
const APPLY_THEME = process.env.APPLY_THEME_JS || path.join(__dirname, "apply_theme.js");

const THEME = {
  name: "PANVIZ Teal",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F2A33", lt1: "FFFFFF", dk2: "0E4D64", lt2: "EAF3F5",
    accent1: "137C8B", accent2: "E07A1F", accent3: "2E7D4F", accent4: "B3261E",
    accent5: "5B6775", accent6: "9FB7CF", hlink: "137C8B", folHlink: "5B6775",
  },
};
const HEX = { verde: "2E7D4F", ambar: "E0A526", rojo: "B3261E", gris: "8A8F98", teal: "137C8B", azul: "0E4D64", claro: "9FB7CF" };
const COLOR_ESTADO = { "Evidenciado": HEX.verde, "Parcial": HEX.ambar, "No evidenciado": HEX.rojo, "No evaluable": HEX.gris };
const COLOR_RES = { "Aprobada": HEX.verde, "Fallida": HEX.rojo, "No ejecutada": HEX.gris };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Revisión SCAMPI del piloto PANVIZ IRAS";
pres.author = "Equipo 04";
const C = pres.SchemeColor;
const W = 13.333;

pres.defineSlideMaster({
  title: "PORTADA",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.0, w: 11.7, h: 1.6, fontSize: 44, bold: true, color: C.text2, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENIDO",
  background: { color: "FFFFFF" },
  margin: [0.5, 0.6, 0.7, 0.6],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.85, fontSize: 30, bold: true, color: C.text2, valign: "middle", margin: 0 }, text: "" } },
    { text: { text: "Equipo 04 · PANVIZ IRAS · Revisión SCAMPI", options: { x: 0.6, y: 7.0, w: 6, h: 0.3, fontSize: 10, color: C.accent5, margin: 0 } } },
  ],
  slideNumber: { x: 12.2, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: C.accent5, align: "right" },
});

let n = 0;
function nueva(titulo, seccion, notas) {
  const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: seccion });
  s.addText(titulo, { placeholder: "title" });
  if (notas) s.addNotes(notas);
  n++;
  return s;
}
function txt(s, texto, o) { s.addText(texto, Object.assign({ isTextBox: true, fontSize: 15, color: C.text1, valign: "top", margin: 0 }, o)); }
function tarjeta(s, x, y, w, h, nombre) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: nombre });
}
function circulo(s, x, y, d, etiqueta, color, tam) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: color || C.accent1 }, line: { color: color || C.accent1 } });
  s.addText(etiqueta, { isTextBox: true, x, y, w: d, h: d, align: "center", valign: "middle", fontSize: tam || 16, bold: true, color: C.background1, margin: 0 });
}
function stat(s, x, y, w, valor, etiqueta, color) {
  txt(s, valor, { x, y, w, h: 0.95, fontSize: 48, bold: true, color: color || C.text2, fontFace: THEME.headFontFace });
  txt(s, etiqueta, { x, y: y + 0.95, w, h: 0.5, fontSize: 13, color: C.accent5 });
}
function pngSize(f) { const b = fs.readFileSync(f); return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) }; }
function imagen(s, rel, x, y, wMax, hMax, nombre) {
  const f = path.join(RAIZ, rel); const { w, h } = pngSize(f);
  const k = Math.min(wMax / w, hMax / h);
  s.addImage({ path: f, x: x + (wMax - w * k) / 2, y, w: w * k, h: h * k, altText: nombre, line: { color: "D9DEE4", width: 0.75 } });
}
function imagenRecorte(s, rel, x, y, wFin, hFin, rect, nombre) {
  const f = path.join(RAIZ, rel); const { w, h } = pngSize(f);
  s.addImage({ path: f, x, y, w: wFin, h: hFin, altText: nombre, sizing: { type: "crop", x: rect.x * wFin / (rect.w), y: rect.y * hFin / rect.h, w: wFin * w / rect.w, h: hFin * h / rect.h } });
}

const ia = D.ind["Antes"], idp = D.ind["Después"];
const pct = v => (v === "Sin datos" ? "sin datos" : `${Math.round(parseFloat(v))} %`);
const ses = D.sesion;
const t09 = ses.tareas["T09"], t10 = ses.tareas["T10"];

// ---------- 1 Portada
pres.addSection({ title: "Portada" });
{
  const s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Portada" });
  n++;
  txt(s, "CALIDAD DE SOFTWARE · TRABAJO PARCIAL 9", { x: 0.8, y: 1.2, w: 11, h: 0.4, fontSize: 14, bold: true, color: C.accent1, charSpacing: 2 });
  s.addText("Revisión SCAMPI del piloto PANVIZ IRAS", { placeholder: "title" });
  txt(s, "Adopción de procesos orientada a CMMI nivel 3 para la vigilancia de Infecciones Respiratorias Agudas en la Red Arequipa y Caylloma", { x: 0.8, y: 3.55, w: 9.5, h: 0.9, fontSize: 18, color: C.accent5 });
  ["OPD", "IPM", "RD", "RSKM", "VER", "VAL"].forEach((a, i) => circulo(s, 0.8 + i * 1.05, 4.75, 0.85, a, i % 2 ? C.text2 : C.accent1, a.length > 3 ? 12 : 14));
  txt(s, "Equipo 04: Anthony Chaisa · Mario Champi · Jael Huarca · Alexander Villafuerte", { x: 0.8, y: 6.05, w: 11.5, h: 0.4, fontSize: 15, color: C.text1 });
  txt(s, "Universidad Nacional de San Agustín de Arequipa · 17 de noviembre de 2026", { x: 0.8, y: 6.45, w: 11.5, h: 0.4, fontSize: 13, color: C.accent5 });
  s.addNotes("Presenta: Anthony. Saludo, nombre del trabajo y del equipo. Aclarar desde el inicio que es una autoevaluación académica inspirada en SCAMPI C, no una evaluación oficial.");
}

// ---------- 2 Caso
pres.addSection({ title: "Contexto y alcance" });
{
  const s = nueva("Notificaciones de IRAS que llegan con errores", "Contexto y alcance",
    "Anthony (contexto, 1 min en total con la diapositiva 3). El responsable de vigilancia necesita un tablero por distrito y grupo etario, pero los registros llegan incompletos, duplicados y con fechas mal escritas. Solo usamos datos sintéticos: el dataset original del equipo (20 notificaciones) ampliado a 30, con dos distritos de Caylloma. Interesan sobre todo la población infantil (menores de 5) y los adultos mayores (60 a más).");
  const prob = [["1", "Campos incompletos", "Establecimiento vacío, evento distinto de IRAS o grupo etario fuera del catálogo MINSA"], ["2", "Registros repetidos", "El mismo ID llega dos veces, o en lotes corregidos"], ["3", "Fechas inválidas", "Fechas inexistentes o en formato distinto a AAAA-MM-DD"]];
  prob.forEach(([k, t, d], i) => {
    const y = 1.6 + i * 1.5;
    circulo(s, 0.6, y, 0.7, k, C.accent2, 18);
    txt(s, t, { x: 1.55, y: y - 0.02, w: 5.2, h: 0.4, fontSize: 18, bold: true, color: C.text2 });
    txt(s, d, { x: 1.55, y: y + 0.4, w: 5.2, h: 0.6, fontSize: 15, color: C.text1 });
  });
  tarjeta(s, 7.2, 1.5, 5.5, 4.9, "cifras");
  stat(s, 7.6, 1.75, 2.4, "30", "notificaciones sintéticas de IRAS");
  stat(s, 10.2, 1.75, 2.4, "6", "inválidos con causa conocida", HEX.rojo);
  stat(s, 7.6, 3.95, 2.4, "9", "distritos: 7 de la Red Arequipa y 2 de Caylloma");
  stat(s, 10.2, 3.95, 2.4, "6", "grupos etarios del catálogo MINSA");
}

// ---------- 3 Alcance
{
  const s = nueva("Qué evaluamos y qué quedó fuera", "Contexto y alcance",
    "Anthony. Muestreamos 6 de las 18 áreas de CMMI DEV v1.3 hasta nivel 3. Las áreas de nivel 2 se registran solo como dependencias. Hay dos flujos: F1 captura y validación, F2 consolidación y visualización.");
  const areas = ["REQM", "PP", "PMC", "SAM", "MA", "PPQA", "CM", "RD", "TS", "PI", "VER", "VAL", "OPF", "OPD", "OT", "IPM", "RSKM", "DAR"];
  const mues = ["RD", "VER", "VAL", "OPD", "IPM", "RSKM"];
  areas.forEach((a, i) => {
    const x = 0.6 + (i % 6) * 0.98, y = 1.75 + Math.floor(i / 6) * 0.98;
    const on = mues.includes(a);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 0.86, h: 0.86, rectRadius: 0.08, fill: { color: on ? C.accent1 : C.background2 }, line: { color: on ? C.accent1 : "D9DEE4" } });
    s.addText(a, { isTextBox: true, x, y, w: 0.86, h: 0.86, align: "center", valign: "middle", fontSize: 11, bold: on, color: on ? C.background1 : C.accent5, margin: 0 });
  });
  txt(s, "Primera fila: nivel 2 (dependencias). Filas 2 y 3: nivel 3. En color, las 6 áreas muestreadas.", { x: 0.6, y: 4.8, w: 5.8, h: 0.7, fontSize: 12, color: C.accent5 });
  txt(s, "Dentro del alcance", { x: 7.0, y: 1.6, w: 5.7, h: 0.4, fontSize: 18, bold: true, color: C.text2 });
  txt(s, [
    { text: "F1 · Captura y validación de registros", options: { bullet: true, breakLine: true } },
    { text: "F2 · Consolidación, tablero y publicación", options: { bullet: true, breakLine: true } },
    { text: "Un incremento: validador + tablero + permiso", options: { bullet: true } },
  ], { x: 7.0, y: 2.05, w: 5.7, h: 1.5, fontSize: 15, paraSpaceAfter: 6 });
  txt(s, "Fuera del alcance", { x: 7.0, y: 3.75, w: 5.7, h: 0.4, fontSize: 18, bold: true, color: C.accent4 });
  txt(s, [
    { text: "12 áreas restantes; nivel 2 solo como dependencia", options: { bullet: true, breakLine: true } },
    { text: "No es evaluación oficial ni calificación SCAMPI", options: { bullet: true, breakLine: true } },
    { text: "No demuestra que PANVIZ sea nivel 3", options: { bullet: true } },
  ], { x: 7.0, y: 4.2, w: 5.7, h: 1.5, fontSize: 15, paraSpaceAfter: 6 });
}

// ---------- 4 Equipo
{
  const s = nueva("Cuatro integrantes, cinco roles y una revisión en ciclo", "Contexto y alcance",
    "Anthony. Éramos 4 para 5 roles: el rol de evidencias y tablero se repartió entre Mario y Anthony. Nadie revisa su propio trabajo. Limitación: todos somos autores, la independencia es limitada.");
  const eq = [
    ["Anthony Chaisa", "Coordinación", "Plan, OPD, IPM, informe", "Revisa las pruebas de Alexander"],
    ["Mario Champi", "Requisitos y tablero", "RD, RSKM, Grist; usuario simulado", "Revisa el plan de Anthony"],
    ["Jael Huarca", "Implementación", "Prototipo, versiones, README", "Revisa trazabilidad y tablero de Mario"],
    ["Alexander Villafuerte", "Pruebas y validación", "12 pruebas, entrevistas, acta", "Revisa código y logs de Jael"],
  ];
  eq.forEach(([nom, rol, resp, rev], i) => {
    const x = 0.6 + i * 3.08;
    tarjeta(s, x, 1.6, 2.85, 3.9, "tarjeta-" + i);
    circulo(s, x + 0.25, 1.85, 0.75, nom.split(" ").map(p => p[0]).join(""), i % 2 ? C.text2 : C.accent1, 16);
    txt(s, nom, { x: x + 0.25, y: 2.8, w: 2.4, h: 0.65, fontSize: 17, bold: true, color: C.text2 });
    txt(s, rol, { x: x + 0.25, y: 3.45, w: 2.4, h: 0.4, fontSize: 14, bold: true, color: C.accent1 });
    txt(s, resp, { x: x + 0.25, y: 3.85, w: 2.4, h: 0.7, fontSize: 13 });
    txt(s, rev, { x: x + 0.25, y: 4.65, w: 2.4, h: 0.7, fontSize: 13, italic: true, color: C.accent5 });
  });
  txt(s, "Ciclo: Mario → Anthony → Alexander → Jael → Mario. Todos somos autores: la independencia es limitada y lo declaramos.", { x: 0.6, y: 5.85, w: 12.1, h: 0.5, fontSize: 15, color: C.text1 });
}

// ---------- 5 Lectura
{
  const s = nueva("Tres decisiones que tomamos de la lectura", "Contexto y alcance",
    "Anthony. Lectura TMMi 2023 (secciones 2.2 a 2.4). Tipo Evaluation del MDD, que reemplaza SCAMPI B y C y no califica. Fases planificar, conducir y reportar, con verificación primero. Muestreo aleatorio con semilla. La nota CMMI 2026 guió la redacción de hallazgos.");
  const dec = [
    ["1", "Tipo de evaluación", "Tratamos el ejercicio como una evaluación de tipo Evaluation del MDD, que reemplaza a SCAMPI B/C. No produce calificaciones y admite adaptar el método: por eso usamos 24 criterios propios."],
    ["2", "Fases", "Planificar, conducir y reportar. Basada en verificación: primero indexamos la evidencia y luego la verificamos, con entrevistas y demostración en vivo."],
    ["3", "Muestreo", "Los dos flujos son los proyectos muestreados. Para la revisión cruzada sorteamos 8 de 21 evidencias con la semilla 2026, una selección que otros pueden repetir."],
  ];
  dec.forEach(([k, t, d], i) => {
    const x = 0.6 + i * 4.1;
    tarjeta(s, x, 1.6, 3.85, 3.7, "decision-" + k);
    circulo(s, x + 0.3, 1.85, 0.7, k, C.accent1, 20);
    txt(s, t, { x: x + 0.3, y: 2.75, w: 3.3, h: 0.45, fontSize: 19, bold: true, color: C.text2 });
    txt(s, d, { x: x + 0.3, y: 3.25, w: 3.3, h: 1.95, fontSize: 14 });
  });
  txt(s, [
    { text: "CMMI Institute, 2026: ", options: { bold: true, color: C.text2 } },
    { text: "las debilidades no se disfrazan de oportunidades de mejora y el simple cumplimiento no es una fortaleza." },
  ], { x: 0.6, y: 5.65, w: 12.1, h: 0.7, fontSize: 15 });
}

// ---------- 6 Proceso
pres.addSection({ title: "Proceso estándar" });
{
  const s = nueva("Proceso estándar PE-04: seis actividades con dueño", "Proceso estándar",
    "Jael (2 min, junto con las diapositivas 7 y 8). Cada actividad tiene entradas, salida, responsable y revisor. Hay plantillas de requisito, revisión y prueba. Convención de identificadores R, C, E, T, H, A. Versiones con etiquetas git.");
  const act = [["Requisitos", "Mario", "Jael"], ["Riesgos", "Mario", "Anthony"], ["Implementación", "Jael", "Alexander"], ["Revisión", "Revisor", "Coord."], ["Pruebas", "Alexander", "Anthony"], ["Cierre", "Anthony", "Equipo"]];
  act.forEach(([a, r, v], i) => {
    const x = 0.6 + i * 2.07;
    circulo(s, x + 0.55, 1.8, 0.8, String(i + 1), i % 2 ? C.text2 : C.accent1, 20);
    if (i < 5) s.addShape(pres.shapes.LINE, { x: x + 1.45, y: 2.2, w: 1.1, h: 0, line: { color: C.accent6, width: 2, endArrowType: "triangle" } });
    txt(s, a, { x, y: 2.8, w: 1.9, h: 0.45, fontSize: 16, bold: true, color: C.text2, align: "center" });
    txt(s, `Dueño: ${r}`, { x, y: 3.25, w: 1.9, h: 0.35, fontSize: 13, align: "center" });
    txt(s, `Revisa: ${v}`, { x, y: 3.6, w: 1.9, h: 0.35, fontSize: 13, align: "center", color: C.accent5 });
  });
  tarjeta(s, 0.6, 4.45, 12.1, 1.9, "convenciones");
  txt(s, "Convenciones del estándar", { x: 0.9, y: 4.6, w: 5, h: 0.4, fontSize: 16, bold: true, color: C.text2 });
  txt(s, [
    { text: "Plantillas de requisito, revisión y caso de prueba", options: { bullet: true, breakLine: true } },
    { text: "Identificadores en una sola cadena: R → C → E → T → H → A", options: { bullet: true, breakLine: true } },
    { text: "Código con etiquetas git v1.0 y v2.0; cada cambio registra motivo, revisor y aprobación", options: { bullet: true } },
  ], { x: 0.9, y: 5.0, w: 11.5, h: 1.3, fontSize: 14, paraSpaceAfter: 4 });
}

// ---------- 7 Adaptación
{
  const s = nueva("Un estándar, dos flujos: la adaptación justificada", "Proceso estándar",
    "Jael. Las mismas actividades en F1 y F2. La adaptación A-01: la validación con usuario solo se exige en F2, porque F1 se comprueba exactamente contra un oráculo manual.");
  const filas = [
    ["Actividad", "F1 · Captura y validación", "F2 · Consolidación y visualización"],
    ["Requisitos", "R1, R2, R4", "R3, R5, R6"],
    ["Implementación", "importador, reglas, validador, repositorio", "resumen, seguridad, web, vista"],
    ["Pruebas", "T01, T02, T05, T06, T11 contra oráculo", "T03, T04, T07, T08, T12 + T09, T10 con usuario"],
    ["Validación", "No aplica (oráculo exacto)", "Escenarios VAL-1 y VAL-2 con usuario"],
  ].map((f, i) => f.map(c => ({ text: c, options: { bold: i === 0, color: i === 0 ? "FFFFFF" : "1F2A33", fill: { color: i === 0 ? HEX.azul : (i % 2 ? "FFFFFF" : "EAF3F5") } } })));
  s.addTable(filas, { x: 0.6, y: 1.6, w: 7.6, colW: [1.8, 2.9, 2.9], fontSize: 13, fontFace: "Calibri", border: { type: "solid", color: "D9DEE4", pt: 0.75 }, valign: "middle", rowH: 0.62 });
  tarjeta(s, 8.6, 1.6, 4.1, 3.6, "adaptacion");
  txt(s, "A-01", { x: 8.9, y: 1.8, w: 3.5, h: 0.6, fontSize: 30, bold: true, color: C.accent2, fontFace: THEME.headFontFace });
  txt(s, "La validación con usuario solo se hace en F2. F1 no tiene interfaz propia, y lo que se acepta o rechaza se comprueba exactamente contra el oráculo.", { x: 8.9, y: 2.5, w: 3.5, h: 2.5, fontSize: 15 });
}

// ---------- 8 Proceso v2
{
  const s = nueva("Lo que aprendimos cambió el proceso, no solo el código", "Proceso estándar",
    "Jael. Las dos fallas reales y el falso positivo de nuestra prueba tenían una causa en el proceso. El proceso PE-04 v2 agrega tres controles, registrados como cambio CP-01 con revisor y aprobación.");
  const ctr = [
    ["Requisitos", "Cada requisito dice qué pasa si un dato vuelve a llegar inválido", "H01 · D01"],
    ["Revisión", "La lista exige escapar todo dato externo antes de mostrarlo", "H02 · D02"],
    ["Pruebas", "Toda prueba oráculo nueva la revisa otro integrante antes de usarse", "H03"],
  ];
  ctr.forEach(([a, c, o], i) => {
    const y = 1.6 + i * 1.6;
    tarjeta(s, 0.6, y, 12.1, 1.35, "control-" + i);
    circulo(s, 0.85, y + 0.28, 0.8, "v2", C.accent1, 16);
    txt(s, a, { x: 1.95, y: y + 0.2, w: 2.4, h: 0.45, fontSize: 18, bold: true, color: C.text2 });
    txt(s, c, { x: 1.95, y: y + 0.65, w: 7.8, h: 0.6, fontSize: 15 });
    txt(s, o, { x: 10.2, y: y + 0.4, w: 2.3, h: 0.5, fontSize: 16, bold: true, color: C.accent2, align: "right" });
  });
  txt(s, "Cambio CP-01 · revisó Mario Champi · aprobó el equipo · 02_procesos/registro_cambios.md", { x: 0.6, y: 6.45, w: 12.1, h: 0.35, fontSize: 12, color: C.accent5 });
}

// ---------- 9 Criterios
pres.addSection({ title: "Evidencia y evaluación" });
{
  const s = nueva("24 criterios: cuatro preguntas para cada área", "Evidencia y evaluación",
    "Mario (2 min, junto con las diapositivas 10 a 12). Para cada área: ¿existe el activo? ¿se aplicó? ¿lo revisó otro integrante? ¿hay mejora o seguimiento? Cada criterio tiene justificación y evidencia enlazada. 'No evaluable' nunca significa cumplimiento.");
  const cols = ["¿Existe?", "¿Se aplicó?", "¿Lo revisó otro?", "¿Mejora o seguimiento?"];
  const areas = ["OPD", "IPM", "RD", "RSKM", "VER", "VAL"];
  cols.forEach((c, j) => txt(s, c, { x: 2.0 + j * 2.0, y: 1.5, w: 1.9, h: 0.4, fontSize: 13, bold: true, color: C.text2, align: "center" }));
  areas.forEach((a, i) => {
    const y = 1.95 + i * 0.72;
    txt(s, a, { x: 0.6, y, w: 1.2, h: 0.6, fontSize: 16, bold: true, color: C.text2, valign: "middle" });
    for (let j = 0; j < 4; j++) {
      const c = D.crit.find(x => x.id === `${a}-C${j + 1}`);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 2.0 + j * 2.0, y, w: 1.9, h: 0.6, rectRadius: 0.06, fill: { color: COLOR_ESTADO[c.estado_despues] }, line: { color: COLOR_ESTADO[c.estado_despues] } });
      s.addText(c.estado_despues, { isTextBox: true, x: 2.0 + j * 2.0, y, w: 1.9, h: 0.6, align: "center", valign: "middle", fontSize: 12, bold: true, color: C.background1, margin: 0 });
    }
  });
  const cnt = e => D.crit.filter(c => c.estado_despues === e).length;
  tarjeta(s, 10.3, 1.95, 2.4, 4.25, "conteo");
  stat(s, 10.55, 2.1, 2.0, String(cnt("Evidenciado")), "Evidenciado", HEX.verde);
  stat(s, 10.55, 3.45, 2.0, String(cnt("Parcial")), "Parcial", HEX.ambar);
  stat(s, 10.55, 4.8, 2.0, String(cnt("No evidenciado")), "No evidenciado", HEX.rojo);
  txt(s, "Estado después de la mejora (v2). En rojo, sobre todo, la revisión por otro integrante y VAL, que dependen de las actas de la sesión.", { x: 0.6, y: 6.35, w: 9.6, h: 0.5, fontSize: 12, color: C.accent5 });
}

// ---------- 10 Trazabilidad
{
  const s = nueva("Trazabilidad: una sola cadena de requisito a acción", "Evidencia y evaluación",
    "Mario. Ejemplo real: R4 (persistir sin duplicar) → criterio VER-C4 → evidencia E16 (registro de defectos) → pruebas T05 y D01 → hallazgo H01 → acción A01, corrección cerrada. Una captura aislada no basta: cada evidencia tiene archivo, versión, fecha y responsable.");
  const ch = [["R", "Requisito", "R4", "Persistir sin duplicar ni dejar obsoletos"], ["C", "Criterio", "VER-C4", "Defectos registrados y re-verificados"], ["E", "Evidencia", "E16", "Registro de defectos"], ["T", "Prueba", "T05 · D01", "Reimportación y lote corregido"], ["H", "Hallazgo", "H01", "Debilidad: el registro obsoleto seguía contando"], ["A", "Acción", "A01", "Corrección y R4 aclarado: cerrada"]];
  ch.forEach(([k, t, ej, d], i) => {
    const x = 0.6 + i * 2.07;
    circulo(s, x + 0.45, 1.75, 1.0, k, i % 2 ? C.text2 : C.accent1, 28);
    if (i < 5) s.addShape(pres.shapes.LINE, { x: x + 1.55, y: 2.25, w: 0.9, h: 0, line: { color: C.accent6, width: 2, endArrowType: "triangle" } });
    txt(s, t, { x, y: 2.95, w: 1.9, h: 0.4, fontSize: 15, bold: true, color: C.text2, align: "center" });
    tarjeta(s, x + 0.05, 3.5, 1.8, 2.2, "ejemplo-" + k);
    txt(s, ej, { x: x + 0.15, y: 3.65, w: 1.6, h: 0.45, fontSize: 17, bold: true, color: C.accent2, align: "center" });
    txt(s, d, { x: x + 0.15, y: 4.15, w: 1.6, h: 1.45, fontSize: 13, align: "center" });
  });
  txt(s, "6 de 6 requisitos trazados a pruebas · matriz en 03_requisitos_riesgos/matriz_trazabilidad.csv", { x: 0.6, y: 6.1, w: 12.1, h: 0.4, fontSize: 14, color: C.accent5 });
}

// ---------- 11 Evidencias y sesión
{
  const s = nueva("26 evidencias indexadas y una muestra sorteada", "Evidencia y evaluación",
    "Mario. 21 evidencias documentales o de ejecución y 5 actas de la sesión del equipo. Muestra aleatoria con semilla 2026 para la revisión cruzada. Mostrar el estado de las entrevistas y de la revisión.");
  stat(s, 0.6, 1.6, 2.8, "26", "evidencias indexadas");
  stat(s, 3.6, 1.6, 2.8, "21", "documentales y de ejecución");
  stat(s, 6.6, 1.6, 2.8, "8", "sorteadas (semilla 2026)", HEX.teal);
  stat(s, 9.6, 1.6, 2.8, "5", "actas de la sesión del equipo", HEX.ambar);
  ["E04", "E08", "E11", "E13", "E14", "E17", "E20", "E26"].forEach((e, i) => circulo(s, 0.6 + i * 0.95, 3.55, 0.8, e, C.accent1, 13));
  txt(s, "Muestra para la revisión cruzada", { x: 8.35, y: 3.75, w: 4.3, h: 0.4, fontSize: 14, color: C.accent5 });
  const st = [["Revisión cruzada (4 actas)", ses.revisiones_hechas], ["Entrevista 1 · uso del proceso", ses.entrevistas_hechas], ["Entrevista 2 · validación de resultados", ses.entrevistas_hechas], ["Validación con usuario (VAL-1, VAL-2)", ses.validacion_hecha]];
  st.forEach(([t, ok], i) => {
    const x = 0.6 + (i % 2) * 6.1, y = 4.75 + Math.floor(i / 2) * 0.75;
    s.addShape(pres.shapes.OVAL, { x, y: y + 0.08, w: 0.32, h: 0.32, fill: { color: ok ? HEX.verde : HEX.ambar }, line: { color: ok ? HEX.verde : HEX.ambar } });
    txt(s, `${t}: ${ok ? "realizada" : "pendiente"}`, { x: x + 0.5, y, w: 5.4, h: 0.5, fontSize: 15, valign: "middle" });
  });
}

// ---------- 12 Criterios antes/después (gráfico)
{
  const s = nueva("Criterios por área: antes y después de la mejora", "Evidencia y evaluación",
    "Mario. Misma muestra y mismas reglas. Mejoraron OPD-C4, RD-C4, RSKM-C4 y VER-C4 al corregir las fallas y publicar el proceso v2. Lo que sigue en rojo depende de la revisión por pares y de la validación con usuario.");
  const areas = ["OPD", "IPM", "RD", "RSKM", "VER", "VAL"];
  const estados = ["Evidenciado", "Parcial", "No evidenciado"];
  const serie = m => estados.map(e => ({ name: e, labels: areas, values: areas.map(a => D.por_area[m][a][e]) }));
  const opc = titulo => ({ barDir: "col", barGrouping: "stacked", chartColors: [HEX.verde, HEX.ambar, HEX.rojo], showTitle: true, title: titulo, titleFontSize: 16, titleColor: "0E4D64", titleFontFace: "+mn-lt",
    showLegend: true, legendPos: "b", legendFontSize: 12, legendFontFace: "+mn-lt", catAxisLabelFontSize: 12, valAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
    catAxisLabelColor: "5B6775", valAxisLabelColor: "5B6775", valAxisMaxVal: 4, valAxisMajorUnit: 1, valGridLine: { color: "E3E7EB", size: 0.5 }, catGridLine: { style: "none" },
    showValue: true, dataLabelPosition: "ctr", dataLabelColor: "FFFFFF", dataLabelFontSize: 11, dataLabelFontFace: "+mn-lt" });
  s.addChart(pres.charts.BAR, serie("antes"), Object.assign({ x: 0.6, y: 1.45, w: 5.9, h: 4.6 }, opc(`Antes (v1) · ${ia.evidenciados_num}/24 evidenciados`)));
  s.addChart(pres.charts.BAR, serie("despues"), Object.assign({ x: 6.8, y: 1.45, w: 5.9, h: 4.6 }, opc(`Después (v2) · ${idp.evidenciados_num}/24 evidenciados`)));
  txt(s, "Un indicador en verde no equivale a nivel 3: mide la preparación del piloto, no la madurez de la organización.", { x: 0.6, y: 6.25, w: 12.1, h: 0.45, fontSize: 14, italic: true, color: C.accent5 });
}

// ---------- 13 Incremento
pres.addSection({ title: "Demostración" });
{
  const s = nueva("El incremento: validar antes de publicar", "Demostración",
    "Jael inicia la demostración (4 min en total, diapositivas 13 a 18). Se importa el CSV de 30 filas: 24 casos aceptados (10 en menores de 5 años y 6 en 60 a más) y 6 rechazados con su causa. Los resultados coinciden con el oráculo calculado a mano antes de ejecutar.");
  txt(s, "Reglas del validador (reglas.py)", { x: 0.6, y: 1.55, w: 6, h: 0.4, fontSize: 18, bold: true, color: C.text2 });
  const r = ["Campos obligatorios presentes", "Fecha real en formato AAAA-MM-DD", "Evento igual a IRAS", "Grupo etario del catálogo MINSA", "Distrito en Arequipa o Caylloma", "Fecha no futura (CR-01, v2)", "Sin ID duplicado (validador)"];
  r.forEach((t, i) => { circulo(s, 0.6, 2.1 + i * 0.6, 0.42, String(i + 1), i === 5 ? C.accent2 : C.accent1, 12); txt(s, t, { x: 1.2, y: 2.1 + i * 0.6, w: 5.2, h: 0.42, fontSize: 15, valign: "middle" }); });
  tarjeta(s, 7.0, 1.55, 5.7, 4.7, "resultado");
  stat(s, 7.4, 1.8, 2.5, "24", "registros aceptados", HEX.verde);
  stat(s, 10.0, 1.8, 2.5, "6", "rechazados con causa", HEX.rojo);
  stat(s, 7.4, 3.75, 2.5, "10 · 6", "casos en menores de 5 años · en 60 a más");
  stat(s, 10.0, 3.75, 2.5, "0", "diferencias con el oráculo manual", HEX.teal);
}

// ---------- 14 Tablero PANVIZ
{
  const s = nueva("Demostración: tablero por distrito y grupo etario", "Demostración",
    "Jael. Mostrar en vivo: importar, filtrar por Majes (3 casos: menor de 1 año, 5 a 9 años y 60 a más), ver la tabla de rechazados y corregir uno. Respaldo: video de hasta 3 minutos.");
  imagen(s, "06_evidencias/capturas/v2_02_filtro_majes.png", 0.6, 1.45, 7.6, 5.3, "Tablero PANVIZ v2 filtrado por Majes");
  txt(s, "Qué muestra", { x: 8.6, y: 1.6, w: 4.1, h: 0.4, fontSize: 18, bold: true, color: C.text2 });
  txt(s, [
    { text: "Solo los casos aceptados, por distrito y los 6 grupos etarios MINSA", options: { bullet: true, breakLine: true } },
    { text: "Los rechazados quedan visibles, con su causa y un botón para corregirlos", options: { bullet: true, breakLine: true } },
    { text: "Filtro por distrito: Majes (Caylloma) tiene 3 casos, uno de ellos de 60 a más", options: { bullet: true, breakLine: true } },
    { text: "Cronómetro integrado para medir las tareas T09 y T10", options: { bullet: true } },
  ], { x: 8.6, y: 2.1, w: 4.1, h: 3.8, fontSize: 15, paraSpaceAfter: 8 });
}

// ---------- 15 Seguridad
{
  const s = nueva("Publicación protegida en la lógica, no en la pantalla", "Demostración",
    "Alexander. El digitador intenta publicar y recibe 'denegado'; el intento queda en el log de acceso. T07 comprueba HTTP 403 y el registro en el log. T08 comprueba que el hash del conjunto publicado no cambia. Alcance local, sin autenticación real: así lo declaramos.");
  imagen(s, "08_informe/img/publicacion_denegada.png", 0.6, 1.5, 7.4, 2.45, "Publicación denegada para el digitador");
  const log = fs.readFileSync(path.join(RAIZ, "06_evidencias/acceso_log_demo.txt"), "utf8").trim().split("\n").slice(0, 4).map(l => l.replace(/\t/g, "  ")).join("\n");
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 4.3, w: 7.4, h: 1.6, fill: { color: "1F2A33" }, line: { color: "1F2A33" } });
  s.addText(log, { isTextBox: true, x: 0.8, y: 4.4, w: 7.1, h: 1.4, fontFace: "Courier New", fontSize: 12, color: "FFFFFF", valign: "middle", margin: 0 });
  txt(s, "logs/acceso.log (demostración v2)", { x: 0.6, y: 5.95, w: 7.4, h: 0.35, fontSize: 11, color: C.accent5 });
  const t07 = D.pr.v2.T07 || {}, t08 = D.pr.v2.T08 || {};
  [["T07", "Publicación sin permiso", "HTTP 403 y 3 intentos en el log", t07.resultado], ["T08", "El rechazo no altera lo publicado", "Hash idéntico; sigue en la versión 1", t08.resultado]].forEach(([id, t, d, r], i) => {
    const y = 1.5 + i * 2.25;
    tarjeta(s, 8.4, y, 4.3, 2.0, id);
    txt(s, id, { x: 8.7, y: y + 0.2, w: 1.5, h: 0.5, fontSize: 24, bold: true, color: C.text2, fontFace: THEME.headFontFace });
    txt(s, r || "—", { x: 10.3, y: y + 0.25, w: 2.2, h: 0.4, fontSize: 15, bold: true, color: COLOR_RES[r] || HEX.gris, align: "right" });
    txt(s, t, { x: 8.7, y: y + 0.8, w: 3.8, h: 0.4, fontSize: 15, bold: true });
    txt(s, d, { x: 8.7, y: y + 1.2, w: 3.8, h: 0.6, fontSize: 14, color: C.accent5 });
  });
}

// ---------- 16 Pruebas
{
  const s = nueva("Doce pruebas, seis características de ISO/IEC 25010", "Demostración",
    "Alexander. Dos pruebas por característica. Las 10 automatizadas pasan en v2. T09 y T10 se miden con el usuario simulado; si no se ejecutan, quedan como 'No ejecutada' y no se cuentan como aprobadas. D01 y D02 reproducen las fallas reales.");
  const head = ["Característica", "Prueba", "Meta", "v1.0", "v2.0"].map(t => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: HEX.azul } } }));
  const ids = ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T09", "T10", "T11", "T12", "D01", "D02"];
  const metas = { T01: "6 inválidos rechazados con causa exacta", T02: "Totales = cálculo manual", T03: "Importar 30 filas ≤ 2 s", T04: "Actualizar resumen ≤ 2 s", T05: "Reimportar sin duplicar", T06: "Recuperar tras reinicio", T07: "Publicación sin permiso denegada", T08: "Lo publicado no cambia", T09: "Corregir un error ≤ 90 s", T10: "Hallar un distrito ≤ 90 s", T11: "Regla nueva sin tocar la vista", T12: "Regresión completa", D01: "Lote corregido sin obsoletos", D02: "Vista escapa datos del CSV" };
  const filas = [head].concat(ids.map((id, i) => {
    const a = (D.pr.v1[id] || {}).resultado || "—", b = (D.pr.v2[id] || {}).resultado || "—";
    const car = ((D.pr.v2[id] || {}).caracteristica || "").replace(" (defecto H01)", "").replace(" (defecto H02)", "");
    const fondo = i % 2 ? "FFFFFF" : "EAF3F5";
    return [{ text: car, options: { fill: { color: fondo } } }, { text: id, options: { bold: true, fill: { color: fondo } } }, { text: metas[id], options: { fill: { color: fondo } } },
      { text: a, options: { bold: true, color: COLOR_RES[a] || "5B6775", fill: { color: fondo } } }, { text: b, options: { bold: true, color: COLOR_RES[b] || "5B6775", fill: { color: fondo } } }];
  }));
  s.addTable(filas, { x: 0.6, y: 1.4, w: 12.1, colW: [3.0, 0.9, 4.6, 1.8, 1.8], fontSize: 12, fontFace: "Calibri", color: "1F2A33", border: { type: "solid", color: "D9DEE4", pt: 0.5 }, rowH: 0.34, valign: "middle", margin: [0, 0.08, 0, 0.08] });
}

// ---------- 17 Fallas reales
{
  const s = nueva("Dos fallas reales encontradas al verificar v1", "Demostración",
    "Alexander. D01: el lote corregido rechazaba IRAS-2026-001, pero el tablero lo seguía contando (4 casos en Cerro Colorado en vez de 3). D02: la tabla de rechazados ejecutaba HTML recibido en el CSV. Ambas se reprodujeron con pruebas que fallan en v1 y pasan en v2. No hizo falta inducir una falla.");
  tarjeta(s, 0.6, 1.5, 5.0, 4.9, "d01");
  txt(s, "D01 · Registro obsoleto", { x: 0.9, y: 1.7, w: 4.5, h: 0.45, fontSize: 19, bold: true, color: C.text2 });
  stat(s, 0.9, 2.3, 2.1, "4", "casos en Cerro Colorado (v1)", HEX.rojo);
  stat(s, 3.2, 2.3, 2.1, "3", "casos en Cerro Colorado (v2)", HEX.verde);
  txt(s, "Causa: el lote nuevo no retiraba los ID rechazados y R4 no definía ese caso. Corrección: el último lote manda y R4 se aclaró (v1.1).", { x: 0.9, y: 4.0, w: 4.45, h: 2.2, fontSize: 14 });
  txt(s, "D02 · Inyección HTML", { x: 6.0, y: 1.55, w: 6.5, h: 0.45, fontSize: 19, bold: true, color: C.text2 });
  imagen(s, "08_informe/img/d02_v1.png", 6.0, 2.05, 6.7, 1.75, "v1: el HTML se ejecuta");
  txt(s, "v1.0: se crean 2 elementos <img> y el título cambia a «INYECTADO»", { x: 6.0, y: 3.88, w: 6.7, h: 0.35, fontSize: 12, color: HEX.rojo });
  imagen(s, "08_informe/img/d02_v2.png", 6.0, 4.3, 6.7, 1.75, "v2: el valor se muestra como texto");
  txt(s, "v2.0: el valor se muestra como texto gracias a esc()", { x: 6.0, y: 6.13, w: 6.7, h: 0.35, fontSize: 12, color: HEX.verde });
}

// ---------- 18 Grist
{
  const s = nueva("Tablero de evaluación en Grist Community", "Demostración",
    "Mario. Documento PANVIZ_Evaluacion con tablas relacionadas, filtros por área y responsable, y enlaces a la evidencia. Los indicadores son fórmulas de Grist y un script de Python independiente da los mismos valores. Formulario de aportes por estudiante.");
  imagen(s, "08_informe/img/grist_tablero.png", 0.6, 1.45, 7.6, 5.2, "Tablero Grist");
  const ind = [["Cobertura documental", ia.cobertura_documental, idp.cobertura_documental], ["Criterios evidenciados", ia.criterios_evidenciados, idp.criterios_evidenciados], ["Ejecución de pruebas", ia.ejecucion_pruebas, idp.ejecucion_pruebas], ["Éxito de pruebas", ia.exito_pruebas, idp.exito_pruebas]];
  ind.forEach(([t, a, b], i) => {
    const y = 1.45 + i * 1.02;
    txt(s, t, { x: 8.6, y, w: 4.1, h: 0.35, fontSize: 14, color: C.accent5 });
    txt(s, [{ text: pct(a), options: { color: C.accent6 } }, { text: "  →  ", options: { color: C.accent5 } }, { text: pct(b), options: { color: C.text2 } }], { x: 8.6, y: y + 0.32, w: 4.1, h: 0.6, fontSize: 26, bold: true, fontFace: THEME.headFontFace });
  });
  txt(s, "Debilidades abiertas", { x: 8.6, y: 5.53, w: 4.1, h: 0.35, fontSize: 14, color: C.accent5 });
  txt(s, [{ text: String(ia.debilidades_abiertas), options: { color: C.accent6 } }, { text: "  →  ", options: { color: C.accent5 } }, { text: String(idp.debilidades_abiertas), options: { color: C.accent4 } }], { x: 8.6, y: 5.85, w: 4.1, h: 0.6, fontSize: 26, bold: true, fontFace: THEME.headFontFace });
}

// ---------- 19 Hallazgos
pres.addSection({ title: "Resultados y mejora" });
{
  const s = nueva("Hallazgos: seis debilidades, una fortaleza", "Resultados y mejora",
    "Anthony (2 min, junto con la diapositiva 20). Aplicamos la nota CMMI 2026: las debilidades se muestran como tales. La fortaleza no es mero cumplimiento: el oráculo es independiente del código y cualquiera puede repetir las pruebas con un comando.");
  const col = { "Debilidad": HEX.rojo, "Fortaleza": HEX.verde, "Oportunidad de mejora": HEX.ambar };
  const corto = { H01: "Registro obsoleto seguía contando (D01)", H02: "La vista ejecutaba HTML del CSV (D02)", H03: "La prueba oráculo dio falsos positivos", H04: "El estándar v1 no tenía controles de reimportación ni de seguridad", H05: "Estándar usado en un solo equipo y durante un día", H06: "Usuario y revisores también son autores", H07: "Oráculo manual previo y observación registrada automáticamente", H08: "Riesgos sin umbral de disparo" };
  D.hall.forEach((hx, i) => {
    const x = 0.6 + (i % 2) * 6.15, y = 1.5 + Math.floor(i / 2) * 1.2;
    tarjeta(s, x, y, 5.95, 1.0, hx.id);
    circulo(s, x + 0.2, y + 0.17, 0.66, hx.id, col[hx.tipo], 13);
    txt(s, corto[hx.id] || hx.observacion, { x: x + 1.05, y: y + 0.12, w: 3.6, h: 0.75, fontSize: 14, valign: "middle" });
    txt(s, `${hx.tipo === "Oportunidad de mejora" ? "Oport." : hx.tipo}\n${hx.estado_despues}`, { x: x + 4.6, y: y + 0.12, w: 1.2, h: 0.75, fontSize: 12, bold: true, color: col[hx.tipo], align: "right", valign: "middle" });
  });
}

// ---------- 20 Acciones
{
  const s = nueva("Plan de mejora: tres acciones priorizadas", "Resultados y mejora",
    "Anthony. Tres acciones abiertas con responsable y plazo de 7 o 30 días. Además, dos evidencias que harían falta para una adopción organizacional sostenida.");
  const acc = [["A1", "Revisión por pares de toda prueba oráculo nueva", "Alexander Villafuerte", "7 días · 23/11", "H03"], ["A3", "Repetir VAL-1 y VAL-2 con un usuario externo al equipo", "Mario Champi", "7 días · 23/11", "H06"], ["A2", "Aplicar PE-04 v2 en un segundo proyecto y registrar la adaptación", "Anthony Chaisa", "30 días · 16/12", "H05"]];
  acc.forEach(([id, t, r, p, h], i) => {
    const x = 0.6 + i * 4.1;
    tarjeta(s, x, 1.5, 3.85, 3.0, id);
    circulo(s, x + 0.3, 1.75, 0.75, id, i < 2 ? C.accent2 : C.accent1, 16);
    txt(s, p, { x: x + 1.2, y: 1.85, w: 2.45, h: 0.5, fontSize: 15, bold: true, color: i < 2 ? C.accent2 : C.accent1, align: "right" });
    txt(s, t, { x: x + 0.3, y: 2.7, w: 3.3, h: 1.0, fontSize: 16, bold: true, color: C.text2 });
    txt(s, `${r} · ${h}`, { x: x + 0.3, y: 3.85, w: 3.3, h: 0.4, fontSize: 13, color: C.accent5 });
  });
  txt(s, "Evidencias adicionales necesarias para una adopción sostenida", { x: 0.6, y: 4.85, w: 12.1, h: 0.4, fontSize: 18, bold: true, color: C.text2 });
  txt(s, [
    { text: "Uso del estándar en varios proyectos y ciclos, con mejoras aprobadas por un grupo de procesos (OPD/OPF)", options: { bullet: true, breakLine: true } },
    { text: "Evidencia de las áreas de nivel 2: auditorías PPQA por alguien ajeno al equipo y una serie histórica de medición (MA)", options: { bullet: true } },
  ], { x: 0.6, y: 5.3, w: 12.1, h: 1.2, fontSize: 15, paraSpaceAfter: 6 });
}

// ---------- 21 Limitaciones y conclusión
pres.addSection({ title: "Limitaciones" });
{
  const s = nueva("Limitaciones y conclusión", "Limitaciones",
    "Mario y Alexander (1 min). Dos limitaciones de la muestra y la idea final. Luego, preguntas (5 min). Cada integrante debe poder ubicar en vivo una evidencia que no elaboró.");
  [["Un equipo, un día, autores evaluándose", "Cuatro personas en un solo día; no hay independencia real ni evidencia de uso sostenido del proceso."], ["Producto y usuario simulados", "30 registros sintéticos en un entorno local y un usuario del propio equipo: los tiempos no se extrapolan a la operación real."]].forEach(([t, d], i) => {
    const x = 0.6 + i * 6.15;
    tarjeta(s, x, 1.5, 5.95, 2.2, "limite-" + i);
    circulo(s, x + 0.3, 1.75, 0.6, String(i + 1), C.accent5, 16);
    txt(s, t, { x: x + 1.1, y: 1.75, w: 4.6, h: 0.6, fontSize: 17, bold: true, color: C.text2 });
    txt(s, d, { x: x + 1.1, y: 2.4, w: 4.6, h: 1.2, fontSize: 14 });
  });
  txt(s, "Lo más valioso no fueron las pruebas que pasaron, sino las dos fallas que encontró la verificación: revelaron brechas del proceso y terminaron cambiando el estándar, no solo el código.", { x: 0.6, y: 4.2, w: 12.1, h: 1.3, fontSize: 22, italic: true, color: C.text2, fontFace: THEME.headFontFace });
  txt(s, `Criterios evidenciados: ${pct(ia.criterios_evidenciados)} → ${pct(idp.criterios_evidenciados)} · Debilidades abiertas: ${ia.debilidades_abiertas} → ${idp.debilidades_abiertas} · Ninguna cifra equivale a nivel 3.`, { x: 0.6, y: 5.75, w: 12.1, h: 0.5, fontSize: 15, color: C.accent5 });
}

(async () => {
  await pres.writeFile({ fileName: SALIDA });
  if (APPLY_THEME) { const { applyTheme } = require(APPLY_THEME); await applyTheme(SALIDA, THEME); }
  console.log(`${SALIDA} · ${n} diapositivas`);
})();

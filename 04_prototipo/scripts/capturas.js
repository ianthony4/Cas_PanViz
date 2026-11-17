// Capturas de evidencia del prototipo con Playwright.
// Uso: node scripts/capturas.js <url> <carpeta_salida> <etiqueta>
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const path = require('path');

(async () => {
  const [url, salida, etiqueta] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  page.on('dialog', d => d.accept());
  const foto = async nombre => page.screenshot({ path: path.join(salida, `${etiqueta}_${nombre}.png`), fullPage: true });

  await page.goto(url);
  await page.waitForSelector('#usuario option', { state: 'attached' });
  await page.selectOption('#usuario', 'digitador01');
  await page.click('#btnImportar');
  await page.waitForTimeout(600);
  await foto('01_tablero_importado');

  await page.selectOption('#filtro', 'Majes');
  await page.waitForTimeout(400);
  await foto('02_filtro_majes');
  await page.selectOption('#filtro', '');

  await page.click('#btnPublicar');  // digitador01: debe ser denegado
  await page.waitForTimeout(400);
  await foto('03_publicacion_denegada');

  await page.selectOption('#usuario', 'resp.vigilancia');
  await page.click('#btnPublicar');
  await page.waitForTimeout(400);
  await foto('04_publicacion_permitida');

  // Intento de inyección HTML a través del CSV
  const csv = 'id,fecha_notificacion,establecimiento,distrito,grupo_etario,evento,estado_validacion\n' +
    'IRAS-X-1,2026-01-12,CS Francisco Bolognesi,Cayma,<img src=x onerror="document.title=\'INYECTADO\'">,IRAS,PENDIENTE\n';
  await page.setInputFiles('#archivo', { name: 'inyeccion.csv', mimeType: 'text/csv', buffer: Buffer.from(csv) });
  await page.click('#btnImportar');
  await page.waitForTimeout(800);
  const titulo = await page.title();
  const imgs = await page.locator('#tRech img').count();
  await page.evaluate(([t, n]) => {
    const d = document.createElement('div');
    d.style.cssText = 'position:fixed;bottom:8px;right:8px;background:#222;color:#fff;padding:6px 10px;font:13px monospace;z-index:9';
    d.textContent = `document.title = "${t}" · <img> en tabla de rechazados = ${n}`;
    document.body.appendChild(d);
  }, [titulo, imgs]);
  await foto('05_prueba_inyeccion');
  console.log(JSON.stringify({ etiqueta, titulo, imgs }));
  await browser.close();
})();

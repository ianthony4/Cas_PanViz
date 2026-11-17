// Capturas del tablero en Grist. Uso: node capturar_grist.js <url_base> <docId> <carpeta>
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
(async () => {
  const [base, doc, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1600, height: 1250 } });
  await p.goto(`${base}/login`);
  await p.goto(`${base}/o/docs/${doc}`);
  await p.waitForTimeout(4000);
  for (let i = 0; i < 3; i++) await p.keyboard.press('Escape');
  await p.locator('.test-onboarding-close, .test-floating-popup-close-btn').first().click({ timeout: 2000 }).catch(() => {});
  const shots = [['Tablero', 'grist_01_tablero'], ['Formulario de aportes', 'grist_02_formulario_aportes'], ['Criterios', 'grist_03_criterios'], ['Indicadores', 'grist_04_indicadores']];
  for (const [pagina, name] of shots) {
    await p.locator('.test-treeview-itemHeader', { hasText: pagina }).first().click();
    await p.waitForTimeout(3500);
    await p.locator('.test-right-panel-close, .test-right-tool-close').first().click({ timeout: 1000 }).catch(() => {});
    await p.locator('.test-onboarding-close, .test-floating-popup-close-btn').first().click({ timeout: 1000 }).catch(() => {});
    await p.waitForTimeout(800);
    await p.screenshot({ path: `${out}/${name}.png` });
    console.log(name, p.url());
  }
  await b.close();
})();

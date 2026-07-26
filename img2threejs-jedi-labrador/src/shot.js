const { chromium } = require('playwright-core');
const path = require('path');

(async () => {
  const views = process.argv.slice(2);
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--no-sandbox'],
  });
  const page = await browser.newPage({ viewport: { width: 980, height: 920 } });
  page.on('console', (m) => console.log('[page]', m.text()));
  page.on('pageerror', (e) => console.log('[pageerror]', e.message));
  await page.goto('file://' + path.resolve(__dirname, 'harness.html'));
  await page.waitForFunction('window.__renderDone === true', { timeout: 30000 });
  if (process.env.STRIP_MAPS === '1') {
    await page.evaluate(() => window.__stripMaps());
  }
  for (const v of views.length ? views : ['reference']) {
    await page.evaluate((name) => window.__setView(name), v);
    if (process.env.STRIP_MAPS === '1') { await page.evaluate(() => window.__stripMaps()); }
    await page.waitForTimeout(200);
    await page.screenshot({ path: path.resolve(__dirname, '..', `${process.env.SHOT_PREFIX || 'render'}-${v}.png`) });
    console.log('shot', v);
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });

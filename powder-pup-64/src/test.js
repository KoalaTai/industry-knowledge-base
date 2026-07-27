const { chromium } = require('playwright-core');
const path = require('path');

(async () => {
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--no-sandbox'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

  await page.goto('file://' + path.resolve(__dirname, 'index.html'));
  await page.waitForTimeout(1200);

  const s0 = await page.evaluate(() => window.__game.state);
  console.log('state after load:', s0);
  await page.screenshot({ path: path.join(__dirname, 'shot-title.png') });

  // start
  await page.keyboard.press('Enter');
  await page.waitForTimeout(2500);
  const s1 = await page.evaluate(() => ({ state: window.__game.state, score: Math.floor(window.__game.score), dist: Math.floor(window.__game.dist), frames: window.__game.frames }));
  console.log('after start:', JSON.stringify(s1));
  await page.screenshot({ path: path.join(__dirname, 'shot-play.png') });

  // steer + jump + trick
  await page.keyboard.down('ArrowRight');
  await page.waitForTimeout(500);
  await page.keyboard.press('Space');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(__dirname, 'shot-trick.png') });
  await page.keyboard.up('ArrowRight');
  await page.waitForTimeout(2000);

  const s2 = await page.evaluate(() => ({ state: window.__game.state, score: Math.floor(window.__game.score), hearts: window.__game.hearts, frames: window.__game.frames }));
  console.log('after play:', JSON.stringify(s2));

  // pause / resume
  await page.keyboard.press('KeyP');
  const sp = await page.evaluate(() => window.__game.state);
  await page.keyboard.press('KeyP');
  const sr = await page.evaluate(() => window.__game.state);
  console.log('pause/resume:', sp, '->', sr);

  // run until crash (force low hearts, drive into obstacles)
  await page.evaluate(() => window.__game.forceCrash());
  const t0 = Date.now();
  let over = false;
  while (Date.now() - t0 < 30000) {
    await page.waitForTimeout(500);
    const st = await page.evaluate(() => window.__game.state);
    if (st === 'over') { over = true; break; }
  }
  console.log('reached game over:', over);
  await page.screenshot({ path: path.join(__dirname, 'shot-over.png') });

  // restart works
  await page.keyboard.press('Enter');
  await page.waitForTimeout(800);
  const s3 = await page.evaluate(() => ({ state: window.__game.state, hearts: window.__game.hearts }));
  console.log('after restart:', JSON.stringify(s3));

  // fps estimate
  const f0 = await page.evaluate(() => window.__game.frames);
  await page.waitForTimeout(3000);
  const f1 = await page.evaluate(() => window.__game.frames);
  console.log('fps ~', Math.round((f1 - f0) / 3));

  console.log('page errors:', errors.length ? errors : 'none');
  await browser.close();
  if (errors.length) process.exit(1);
})().catch((e) => { console.error(e); process.exit(1); });

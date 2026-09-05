// End-to-end checks for the built site: console errors, leftover placeholders, and one interaction per tool.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const http = require('http');

const SITE = path.join(__dirname, '..', 'site');
const PORT = 8765;
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.xml': 'application/xml', '.txt': 'text/plain' };

function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      let p = decodeURIComponent(req.url.split('?')[0]);
      if (p.endsWith('/')) p += 'index.html';
      const f = path.join(SITE, p);
      if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('404'); }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
      fs.createReadStream(f).pipe(res);
    });
    srv.listen(PORT, () => resolve(srv));
  });
}

function allPages() {
  const out = [];
  (function walk(d) { for (const e of fs.readdirSync(d)) { const f = path.join(d, e); if (fs.statSync(f).isDirectory()) walk(f); else if (e.endsWith('.html')) out.push('/' + path.relative(SITE, f).replace(/\\/g, '/')); } })(SITE);
  return out.sort();
}

async function makePng(page) { // returns a Buffer of a 1200x800 PNG generated in-browser
  const data = await page.evaluate(() => { const c = document.createElement('canvas'); c.width = 1200; c.height = 800; const x = c.getContext('2d'); x.fillStyle = '#39c'; x.fillRect(0, 0, 1200, 800); x.fillStyle = '#fc3'; x.beginPath(); x.arc(600, 400, 250, 0, 7); x.fill(); return c.toDataURL('image/png'); });
  return Buffer.from(data.split(',')[1], 'base64');
}

(async () => {
  const srv = await serve();
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ locale: 'it-IT', acceptDownloads: true });
  const page = await ctx.newPage();
  const problems = [];
  page.on('pageerror', (e) => problems.push(['pageerror', page.url(), e.message]));
  page.on('console', (m) => { if (m.type() === 'error') problems.push(['console', page.url(), m.text()]); });
  page.on('response', (r) => { if (r.status() >= 400) problems.push(['http', r.url(), r.status()]); });

  // 1. load every page
  const pages = allPages();
  for (const p of pages) {
    await page.goto(`http://localhost:${PORT}${p}`, { waitUntil: 'load' });
    const html = await page.content();
    if (html.includes('{{')) problems.push(['placeholder', p, (html.match(/\{\{\w+\}\}/g) || []).slice(0, 5).join(',')]);
    const title = await page.title();
    if (!title) problems.push(['notitle', p, '']);
    const langSwitch = await page.$('a.lang');
    if (langSwitch && !p.startsWith('/404')) { const href = await langSwitch.getAttribute('href'); const target = new URL(href, `http://localhost:${PORT}${p}`).pathname; const tf = path.join(SITE, target.endsWith('/') ? target + 'index.html' : target); if (!fs.existsSync(tf)) problems.push(['badlang', p, target]); }
    // check all internal links resolve
    const links = await page.$$eval('a[href]', (as) => as.map((a) => a.getAttribute('href')));
    for (const h of links) {
      if (/^(https?:|mailto:|#|javascript:)/.test(h) || h.startsWith('blob:')) continue;
      const target = new URL(h, `http://localhost:${PORT}${p}`).pathname.split('#')[0];
      const tf = path.join(SITE, target.endsWith('/') ? target + 'index.html' : target);
      if (!fs.existsSync(tf)) problems.push(['badlink', p, h]);
    }
  }
  console.log('Loaded', pages.length, 'pages');

  // 2. interactions (Italian versions)
  const base = `http://localhost:${PORT}/it/`;
  const results = {};
  async function go(slug) { await page.goto(base + slug + '/', { waitUntil: 'load' }); }
  async function text(sel) { return (await page.textContent(sel) || '').trim(); }

  await go('calcolo-eta'); await page.fill('#dob', '1990-03-15'); await page.fill('#at', '2026-09-05'); await page.dispatchEvent('#at', 'input');
  results.age = await text('#main');
  await go('giorni-tra-due-date'); await page.fill('#d1', '2026-09-01'); await page.fill('#d2', '2026-09-10'); await page.dispatchEvent('#d2', 'input'); results.days = await text('#main') + ' | ' + await text('#work');
  await go('aggiungi-giorni-a-una-data'); await page.fill('#start', '2026-09-05'); await page.dispatchEvent('#start', 'input'); await page.click('[data-q="60"]'); results.addDays = await text('#main');
  await go('timer-online'); await page.click('[data-p="1"]'); await page.click('#tstart'); await page.waitForTimeout(1500); results.timer = await text('#tdisp');
  await page.click('.tabs button[data-tab="s"]'); await page.click('#sstart'); await page.waitForTimeout(700); await page.click('#slap'); results.stopwatch = await text('#sdisp') + ' laps:' + (await page.$$('#lapbody tr')).length;
  await go('conta-parole'); await page.fill('#txt', 'Ciao mondo. Questa è una prova! Funziona? Sì.\n\nSecondo paragrafo.'); results.words = await text('#w') + 'w ' + await text('#c') + 'c ' + await text('#s') + 's ' + await text('#p') + 'p';
  await go('maiuscolo-minuscolo'); await page.fill('#txt', 'ciao è una prova. seconda frase!'); await page.click('[data-m="sentence"]'); results.caseSentence = await page.inputValue('#res'); await page.click('[data-m="upper"]'); results.caseUpper = await page.inputValue('#res');
  await go('generatore-password'); results.pw = (await page.inputValue('#pw')).length + ' chars, ' + await text('#str'); await page.click('.tabs button[data-tab="pp"]'); results.pp = await page.inputValue('#pw');
  await go('rimuovi-righe-duplicate'); await page.fill('#txt', 'b\na\n\nb\nc\nA'); await page.selectOption('#sort', 'az'); results.lines = JSON.stringify(await page.inputValue('#res')) + ' ' + await text('#info');
  await go('calcolo-percentuale'); results.pct = await text('#r1') + ' | ' + await text('#r2') + ' | ' + await text('#r3') + ' | ' + await text('#r4');
  await go('calcolo-sconto'); results.discount = await text('#final') + ' ' + await text('#save') + ' ' + await text('#eff'); await page.fill('#disc2', '20'); await page.dispatchEvent('#disc2', 'input'); results.discount2 = await text('#final') + ' ' + await text('#eff');
  await go('numeri-romani'); results.roman = await text('#out'); await page.fill('#rom', 'XIV'); await page.dispatchEvent('#rom', 'input'); results.roman2 = await page.inputValue('#num'); await page.fill('#rom', 'IIII'); await page.dispatchEvent('#rom', 'input'); results.roman3 = await text('#msg');
  await go('convertitore-unita-di-misura'); results.units = await text('#out'); await page.selectOption('#cat', 'temp'); await page.fill('#val', '100'); await page.dispatchEvent('#val', 'input'); results.temp = await text('#out');
  await go('numeri-casuali'); await page.fill('#cnt', '5'); await page.check('#uniq'); await page.click('#gen'); results.random = await text('#main'); await page.click('.tabs button[data-tab="d"]'); await page.click('#roll'); results.dice = await text('#main') + ' ' + await text('#sub');
  await go('calcolo-bmi'); results.bmi = await text('#val') + ' ' + await text('#cat') + ' ' + await text('#range');
  await go('calcolo-calorie-giornaliere'); results.cal = await text('#bmr') + ' / ' + await text('#tdee');
  await go('calcolo-rata-mutuo'); results.loan = await text('#pmt') + ' ' + await text('#int'); await page.click('#toggle'); results.loanRows = (await page.$$('#rows tr')).length;
  await go('calcolo-iva'); results.vat = await text('#net') + ' ' + await text('#vat') + ' ' + await text('#gross'); await page.selectOption('#mode', 'remove'); await page.fill('#amt', '122'); await page.dispatchEvent('#amt', 'input'); results.vat2 = await text('#net') + ' ' + await text('#vat');
  await go('dividi-il-conto'); results.split = await text('#each') + ' ' + await text('#grand'); await page.click('[data-t="10"]'); await page.selectOption('#round', '1'); results.split2 = await text('#each') + ' ' + await text('#tipt') + ' | ' + await text('#extra');
  // images
  const png = await makePng(page);
  await go('ridimensiona-comprimi-immagini');
  await page.setInputFiles('#file', { name: 'test.png', mimeType: 'image/png', buffer: png });
  await page.waitForSelector('#out:not(.hide)', { timeout: 10000 }); results.resize = await text('#origcap') + ' -> ' + await text('#rescap');
  await go('converti-immagini');
  await page.setInputFiles('#file', [{ name: 'a.png', mimeType: 'image/png', buffer: png }, { name: 'b.png', mimeType: 'image/png', buffer: png }]);
  await page.selectOption('#fmt', 'image/webp'); await page.click('#go'); await page.waitForFunction(() => document.querySelectorAll('#list a').length === 2, null, { timeout: 10000 });
  results.convert = await page.$$eval('#list tr', (trs) => trs.map((t) => t.children[2].textContent).join(','));
  await go('generatore-codice-qr'); results.qr = await text('#info');
  const [dl] = await Promise.all([page.waitForEvent('download'), page.click('#png')]); results.qrDownload = dl.suggestedFilename();
  const [dl2] = await Promise.all([page.waitForEvent('download'), page.click('#svg')]); results.qrSvg = dl2.suggestedFilename();
  await page.click('.tabs button[data-tab="wifi"]'); await page.fill('#ssid', 'CasaMia'); await page.fill('#wpass', 'segreto;123'); await page.dispatchEvent('#wpass', 'input'); results.qrWifi = await text('#info');
  // home search
  await page.goto(base, { waitUntil: 'load' }); await page.fill('#tool-search', 'iva'); results.search = (await page.$$eval('.card', (cs) => cs.filter((c) => c.style.display !== 'none').map((c) => c.querySelector('b').textContent))).join(' | ');
  // root redirect
  await page.goto(`http://localhost:${PORT}/`, { waitUntil: 'load' }); await page.waitForTimeout(300); results.rootRedirect = page.url();

  // 3. English spot checks
  await page.goto(`http://localhost:${PORT}/en/vat-calculator/`, { waitUntil: 'load' }); results.vatEn = await text('#net') + ' ' + await text('#gross') + ' rate=' + await page.inputValue('#rate');
  await page.goto(`http://localhost:${PORT}/en/loan-calculator/`, { waitUntil: 'load' }); results.loanEn = await text('#pmt');

  console.log(JSON.stringify(results, null, 1));
  console.log('PROBLEMS:', problems.length); problems.forEach((p) => console.log('  ', p.join(' | ')));

  // 4. screenshots
  fs.mkdirSync('/tmp/shots', { recursive: true });
  const shots = [['it/', 'home-it-desktop', 1280, false], ['en/', 'home-en-mobile', 390, false], ['it/calcolo-rata-mutuo/', 'loan-it-mobile', 390, false], ['en/qr-code-generator/', 'qr-en-desktop', 1280, false], ['it/calcolo-eta/', 'age-it-dark', 390, true], ['it/ridimensiona-comprimi-immagini/', 'resize-it-desktop', 1280, false]];
  for (const [p, name, w, dark] of shots) {
    const c2 = await browser.newContext({ viewport: { width: w, height: w > 600 ? 900 : 844 }, colorScheme: dark ? 'dark' : 'light', locale: 'it-IT', deviceScaleFactor: 1 });
    const pg = await c2.newPage(); await pg.goto(`http://localhost:${PORT}/${p}`, { waitUntil: 'load' });
    await pg.screenshot({ path: `/tmp/shots/${name}.png`, fullPage: name.startsWith('home') ? false : false });
    await c2.close();
  }
  await browser.close(); srv.close();
})();

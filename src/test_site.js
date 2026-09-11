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
      const target = new URL(h, page.url()).pathname.split('#')[0];
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
  // --- v1.1.0: countdown pages, numbers to words, weighted average, colf tools ---
  function isoLocal(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function daysFromToday(y, m, d) { const t = new Date(); const a = Date.UTC(t.getFullYear(), t.getMonth(), t.getDate()); const b = Date.UTC(y, m - 1, d); return Math.round((b - a) / 86400000); }
  const now = new Date(), thisYear = now.getFullYear();
  const xmasYear = (now.getMonth() === 11 && now.getDate() > 25) ? thisYear + 1 : thisYear;
  await go('quanti-giorni-mancano-a-natale'); await page.waitForTimeout(1200);
  results.natale = await text('#main') + ' | ' + await text('#sub') + ' | years=' + (await page.$$('#year option')).length + ' | expected=' + daysFromToday(xmasYear, 12, 25) + ' | tick=' + await text('#tick');
  await go('quanti-giorni-mancano-a-pasqua'); results.pasqua = await text('#sub') + ' | ' + await page.inputValue('#year');
  await page.selectOption('#year', '2028'); results.pasqua2028 = await text('#sub');
  await go('quanti-giorni-mancano-a-carnevale'); results.carnevale = await text('#sub');
  await go('quanti-giorni-mancano'); await page.fill('#target', thisYear + '-12-31'); await page.dispatchEvent('#target', 'input'); results.generic = await text('#main') + ' expected=' + daysFromToday(thisYear, 12, 31) + ' | ' + await page.inputValue('#msgcopy');
  await page.fill('#target', '2020-01-01'); await page.dispatchEvent('#target', 'input'); results.genericPast = await text('#main') + ' | ' + await text('#sub');
  await go('quanti-giorni-mancano-al-mio-compleanno'); await page.fill('#dob', '1990-03-15'); await page.dispatchEvent('#dob', 'input'); results.compleanno = await text('#main') + ' | ' + await text('#sub');
  await go('quanti-giorni-mancano-all-inizio-della-scuola'); results.scuola = await page.inputValue('#target') + ' | ' + await text('#main');
  // numbers to words
  await go('numeri-in-lettere');
  const nw = {};
  async function nwCase(val, mode, lang, style) { await page.fill('#num', val); if (mode) await page.selectOption('#mode', mode); if (lang) await page.selectOption('#lang', lang); if (style) await page.selectOption('#style', style); await page.dispatchEvent('#num', 'input'); return await text('#main'); }
  nw.a = await nwCase('1234,56', 'num', 'it'); nw.b = await nwCase('1234,56', 'eur'); nw.c = await nwCase('1234,56', 'chk'); nw.d = await nwCase('21', 'num'); nw.e = await nwCase('108'); nw.f = await nwCase('1000000'); nw.g = await nwCase('23'); nw.h = await nwCase('2003'); nw.i = await nwCase('180'); nw.j = await nwCase('1,01', 'eur'); nw.k = await nwCase('0'); nw.l = await nwCase('-45'); nw.m = await nwCase('3000000000'); nw.n = await nwCase('1000001');
  nw.en1 = await nwCase('1042', 'num', 'en', 'uk'); nw.en2 = await nwCase('1042', 'num', 'en', 'us'); nw.en3 = await nwCase('1234,56', 'eur', 'en', 'us'); nw.en4 = await nwCase('1234,56', 'chk'); nw.en5 = await nwCase('205', 'num', 'en', 'uk'); nw.en6 = await nwCase('12,5', 'num', 'en', 'us');
  nw.tableRows = (await page.$$('#tbl tr')).length; nw.err = await (async () => { await page.fill('#num', 'abc'); await page.dispatchEvent('#num', 'input'); return await text('#err'); })();
  results.numWords = nw;
  // weighted average
  await go('calcolo-media-ponderata-voto-di-laurea');
  const exams = [[28, 12], [24, 6], [30, 9]];
  for (let i = 0; i < exams.length; i++) { await page.fill(`#rows tr:nth-child(${i + 1}) .g`, String(exams[i][0])); await page.fill(`#rows tr:nth-child(${i + 1}) .c`, String(exams[i][1])); }
  await page.dispatchEvent('#rows tr:nth-child(3) .c', 'input');
  results.media = await text('#main') + ' | ' + await text('#aavg') + ' | ' + await text('#tot') + ' | ' + await text('#base') + ' | ' + await text('#final');
  await page.check('#rows tr:nth-child(3) .l'); await page.selectOption('#lodev', '33'); results.mediaLode = await text('#main');
  await page.fill('#gavg', '28'); await page.fill('#gcfu', '30'); await page.dispatchEvent('#gcfu', 'input'); results.mediaGoal = await text('#goal');
  await page.click('.tabs button[data-tab="avg"]'); await page.fill('#avgin', '27'); await page.dispatchEvent('#avgin', 'input'); results.mediaKnown = await text('#base') + ' | ' + await text('#final');
  // colf: tredicesima
  await go('calcolo-tredicesima-colf-badante'); await page.fill('#start', thisYear + '-01-01'); await page.fill('#end', thisYear + '-12-31'); await page.dispatchEvent('#end', 'input');
  results.tredicesima = await text('#main') + ' | ' + await text('#mon');
  await page.fill('#start', thisYear + '-08-01'); await page.dispatchEvent('#start', 'input'); results.tredicesima5 = await text('#main') + ' | ' + await text('#mon');
  await page.fill('#start', thisYear + '-08-20'); await page.dispatchEvent('#start', 'input'); results.tredicesima4 = await text('#mon');
  await page.selectOption('#type', 'm'); await page.fill('#monthly', '1200'); await page.fill('#kind', '200'); await page.fill('#start', thisYear + '-01-01'); await page.dispatchEvent('#start', 'input'); results.tredicesimaM = await text('#main');
  // colf: ferie
  await go('calcolo-ferie-colf-badante'); await page.fill('#start', thisYear + '-01-01'); await page.fill('#end', thisYear + '-12-31'); await page.fill('#taken', '10'); await page.dispatchEvent('#taken', 'input');
  results.ferie = await text('#main') + ' | ' + await text('#year') + ' | ' + await text('#val');
  await page.selectOption('#type', 'm'); await page.selectOption('#wdays', '5'); await page.fill('#monthly', '1300'); await page.dispatchEvent('#monthly', 'input'); results.ferieM = await text('#main') + ' | ' + await text('#year') + ' | ' + await text('#val');
  // colf: tfr
  await go('calcolo-tfr-colf-badante'); await page.fill('#start', '2025-01-01'); await page.fill('#end', '2026-12-31'); await page.dispatchEvent('#end', 'input');
  results.tfr = await text('#main') + ' | ' + await text('#quota') + ' | ' + await text('#years') + ' rows=' + (await page.$$('#rows tr')).length;
  await page.fill('#infl', '2'); await page.dispatchEvent('#infl', 'input'); results.tfrReval = await text('#main') + ' | ' + await text('#reval');
  await page.fill('#end', '2024-01-01'); await page.dispatchEvent('#end', 'input'); results.tfrErr = await page.$eval('#err', (e) => e.classList.contains('hide') ? 'hidden' : e.textContent);
  // --- v1.2.0: working days, hours worked, proportions, running pace ---
  const v12 = {};
  await go('calcolo-giorni-lavorativi');
  async function wd(a, b) { await page.fill('#d1', a); await page.fill('#d2', b); await page.dispatchEvent('#d2', 'input'); return await text('#main'); }
  v12.sept = await wd('2026-09-01', '2026-09-30');
  v12.y2026 = await wd('2026-01-01', '2026-12-31') + ' | hol=' + await text('#s3') + ' | rows=' + (await page.$$('#list tr')).length;
  await page.selectOption('#patron', 'milano'); await page.dispatchEvent('#patron', 'change'); v12.milano = await text('#main');
  await page.selectOption('#patron', ''); await page.selectOption('#week', '6'); await page.dispatchEvent('#week', 'change'); v12.sixDays = await text('#main');
  await page.selectOption('#week', '5'); await page.dispatchEvent('#week', 'change');
  v12.oct2027 = await wd('2027-10-01', '2027-10-08') + ' | ' + (await page.$$eval('#list tr', (trs) => trs.map((t) => t.children[1].textContent).join(',')));
  await page.selectOption('#patron', 'custom'); await page.fill('#pdate', '2026-10-05'); await page.dispatchEvent('#pdate', 'input'); v12.custom = await wd('2026-10-01', '2026-10-09');
  await page.selectOption('#patron', '');
  await page.click('.tabs button[data-tab="add"]');
  async function addw(s, n, back) { await page.fill('#start', s); await page.fill('#n', String(n)); if (back) await page.check('#back'); else await page.uncheck('#back'); await page.dispatchEvent('#n', 'input'); return await text('#main'); }
  v12.add10 = await addw('2026-09-11', 10); v12.back10 = await addw('2026-09-11', 10, true); v12.xmas = await addw('2026-12-23', 3) + ' | skipped=' + await text('#s3');
  results.workingDays = v12;
  const h = {};
  await go('calcolo-ore-lavorate'); h.def = await text('#wmain') + ' | ' + await text('#wsub') + ' | over=' + await text('#wover');
  await page.fill('#wk tr:nth-child(1) .ti', '22:00'); await page.fill('#wk tr:nth-child(1) .to', '06:00'); await page.fill('#wk tr:nth-child(1) .tb', '0'); await page.dispatchEvent('#wk tr:nth-child(1) .tb', 'input');
  h.night = await text('#wmain') + ' | mon=' + await text('#wk tr:nth-child(1) .tr');
  await page.fill('#wk tr:nth-child(6) .ti', '08:00'); await page.fill('#wk tr:nth-child(6) .to', '12:30'); await page.dispatchEvent('#wk tr:nth-child(6) .to', 'input');
  await page.fill('#rate', '10'); await page.dispatchEvent('#rate', 'input'); h.pay = await text('#wmain') + ' | ' + await text('#wpay') + ' | over=' + await text('#wover') + ' | avg=' + await text('#wavg');
  await page.fill('#wk tr:nth-child(2) .tb', '600'); await page.dispatchEvent('#wk tr:nth-child(2) .tb', 'input'); h.brkErr = await page.$eval('#werr', (e) => !e.classList.contains('hide'));
  await page.click('.tabs button[data-tab="sum"]'); h.sum = await text('#smain') + ' | ' + await text('#ssub');
  await page.selectOption('#srows tr:nth-child(2) .ss', '-1'); await page.dispatchEvent('#srows tr:nth-child(2) .ss', 'change'); h.sumMinus = await text('#smain');
  await page.fill('#srows tr:nth-child(4) .sh', '30'); await page.dispatchEvent('#srows tr:nth-child(4) .sh', 'input'); h.sumDays = await text('#smain') + ' | ' + await text('#ssub');
  await page.click('.tabs button[data-tab="dec"]'); h.dec = await text('#dres') + ' | ' + await text('#dsub') + ' || ' + await text('#dres2') + ' | ' + await text('#dsub2');
  await page.fill('#dh', '0'); await page.fill('#dm', '135'); await page.dispatchEvent('#dm', 'input'); h.dec135 = await text('#dres') + ' | ' + await text('#dsub');
  results.hours = h;
  const pr = {};
  await go('calcolo-proporzioni'); pr.three = await text('#tres') + ' | ' + await text('#tsub');
  await page.fill('#ta', '4'); await page.fill('#tb', '6'); await page.fill('#tc', '3'); await page.check('input[name="kind"][value="i"]'); await page.dispatchEvent('#tc', 'input'); pr.inv = await text('#tres') + ' | ' + await text('#tsub');
  await page.click('.tabs button[data-tab="prop"]'); pr.prop = await text('#pres') + ' | ' + await text('#psub');
  await page.fill('#pd', '15'); await page.dispatchEvent('#pd', 'input'); pr.check = await text('#pres');
  await page.fill('#pd', '14'); await page.dispatchEvent('#pd', 'input'); pr.checkNo = await text('#pres') + ' | ' + await text('#psub');
  await page.fill('#pa', ''); await page.dispatchEvent('#pa', 'input'); pr.findA = await text('#pres');
  await page.fill('#pb', ''); await page.dispatchEvent('#pb', 'input'); pr.twoEmpty = await text('#psub');
  await page.click('.tabs button[data-tab="recipe"]'); pr.recipe = await text('#rfac') + ' | ' + JSON.stringify(await page.inputValue('#rout'));
  await page.selectOption('#by', 'pan'); await page.dispatchEvent('#by', 'change'); pr.pan = await text('#rfac') + ' | ' + await text('#rsub');
  await page.selectOption('#s2', 'q'); await page.fill('#a2', '30'); await page.fill('#b2', '20'); await page.dispatchEvent('#b2', 'input'); pr.panRect = await text('#rfac') + ' | ' + await text('#rsub') + ' | b2visible=' + await page.$eval('#wb2', (e) => !e.classList.contains('hide'));
  await page.selectOption('#by', 'factor'); await page.fill('#fx', '2'); await page.fill('#ing', '1 1/2 cucchiai di olio\n½ limone\n1.000 g di farina\n2,5 dl di panna\nsale q.b.'); await page.dispatchEvent('#ing', 'input'); pr.parse = JSON.stringify(await page.inputValue('#rout'));
  results.proportion = pr;
  const rp = {};
  await go('calcolo-passo-corsa'); rp.def = await text('#pmain') + ' | ' + await text('#pkmh') + ' | ' + await text('#pmi') + ' | 400m=' + await text('#p400') + ' | riegel=' + (await page.$$eval('#riegel tr', (trs) => trs.map((t) => t.children[0].textContent + ' ' + t.children[1].textContent).join(', '))) + ' | splits=' + (await page.$$('#splits tr')).length;
  await page.click('[data-d="21.0975"]'); await page.fill('#th', '1'); await page.fill('#tm', '45'); await page.dispatchEvent('#tm', 'input'); rp.half = await text('#pmain') + ' | ' + await text('#pkmh') + ' | splits=' + (await page.$$('#splits tr')).length;
  await page.click('.tabs button[data-tab="time"]'); rp.time = await text('#tmain') + ' | ' + await text('#tsub') + ' | rows=' + (await page.$$('#ttable tr')).length;
  await page.click('[data-d2="42.195"]'); await page.fill('#pm', '5'); await page.fill('#ps', '41'); await page.dispatchEvent('#ps', 'input'); rp.mar = await text('#tmain');
  await page.selectOption('#pu', 'mi'); await page.fill('#pm', '8'); await page.fill('#ps', '0'); await page.dispatchEvent('#ps', 'input'); rp.mile = await text('#tmain') + ' | ' + await text('#tsub');
  await page.click('.tabs button[data-tab="conv"]'); rp.conv = await text('#cres') + ' | ' + await text('#csub') + ' || ' + await text('#cres2') + ' | ' + await text('#csub2') + ' | tread=' + (await page.$$('#treadmill tr')).length;
  results.running = rp;
  // home search
  await page.goto(base, { waitUntil: 'load' }); await page.fill('#tool-search', 'iva'); results.search = (await page.$$eval('.card', (cs) => cs.filter((c) => c.style.display !== 'none').map((c) => c.querySelector('b').textContent))).join(' | ');
  // root redirect
  await page.goto(`http://localhost:${PORT}/`, { waitUntil: 'load' }); await page.waitForTimeout(300); results.rootRedirect = page.url();

  // 3. English spot checks
  await page.goto(`http://localhost:${PORT}/en/vat-calculator/`, { waitUntil: 'load' }); results.vatEn = await text('#net') + ' ' + await text('#gross') + ' rate=' + await page.inputValue('#rate');
  await page.goto(`http://localhost:${PORT}/en/loan-calculator/`, { waitUntil: 'load' }); results.loanEn = await text('#pmt');
  await page.goto(`http://localhost:${PORT}/en/days-until-christmas/`, { waitUntil: 'load' }); results.xmasEn = await text('#main') + ' | ' + await text('#sub');
  await page.goto(`http://localhost:${PORT}/en/numbers-to-words/`, { waitUntil: 'load' }); results.wordsEn = await text('#main') + ' | lang=' + await page.inputValue('#lang');
  await page.goto(`http://localhost:${PORT}/en/13th-month-pay-domestic-worker-italy/`, { waitUntil: 'load' }); results.tredEn = await text('#main');

  console.log(JSON.stringify(results, null, 1));
  console.log('PROBLEMS:', problems.length); problems.forEach((p) => console.log('  ', p.join(' | ')));

  // 4. screenshots
  fs.mkdirSync('/tmp/shots', { recursive: true });
  const shots = [['it/', 'home-it-desktop', 1280, false], ['en/', 'home-en-mobile', 390, false], ['it/calcolo-rata-mutuo/', 'loan-it-mobile', 390, false], ['en/qr-code-generator/', 'qr-en-desktop', 1280, false], ['it/calcolo-eta/', 'age-it-dark', 390, true], ['it/ridimensiona-comprimi-immagini/', 'resize-it-desktop', 1280, false], ['it/quanti-giorni-mancano-a-natale/', 'natale-it-mobile', 390, false], ['it/calcolo-media-ponderata-voto-di-laurea/', 'media-it-desktop', 1280, false], ['it/numeri-in-lettere/', 'lettere-it-desktop', 1280, false], ['it/calcolo-tredicesima-colf-badante/', 'tredicesima-it-mobile', 390, false], ['en/days-until-easter/', 'easter-en-desktop', 1280, true], ['it/', 'home-it-v11', 1280, false], ['it/calcolo-giorni-lavorativi/', 'v12-giorni-lavorativi-it-desktop', 1280, false], ['it/calcolo-ore-lavorate/', 'v12-ore-lavorate-it-desktop', 1280, false], ['it/calcolo-proporzioni/', 'v12-proporzioni-it-mobile', 390, false], ['it/calcolo-passo-corsa/', 'v12-passo-corsa-it-mobile', 390, false], ['en/working-days-calculator-italy/', 'v12-working-days-en-dark', 390, true]];
  for (const [p, name, w, dark] of shots) {
    const c2 = await browser.newContext({ viewport: { width: w, height: w > 600 ? 900 : 844 }, colorScheme: dark ? 'dark' : 'light', locale: 'it-IT', deviceScaleFactor: 1 });
    const pg = await c2.newPage(); await pg.goto(`http://localhost:${PORT}/${p}`, { waitUntil: 'load' });
    await pg.screenshot({ path: `/tmp/shots/${name}.png`, fullPage: name.startsWith('home') ? false : false });
    await c2.close();
  }
  await browser.close(); srv.close();
})();

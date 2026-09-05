// Renders QR codes with qr.js in headless Chromium and saves PNGs for decoding with OpenCV.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const qrjs = fs.readFileSync(path.join(__dirname, 'assets/qr.js'), 'utf8');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent('<canvas id="c"></canvas>');
  await page.addScriptTag({ content: qrjs });
  const tests = [
    ['https://rapidotools.com/', 'M'],
    ['Ciao mondo! Àèìòù €', 'L'],
    ['A'.repeat(100), 'Q'],
    ['https://rapidotools.com/it/generatore-codice-qr/?utm_source=test&utm_medium=qr&utm_campaign=verifica-lunga-2026', 'H'],
    ['Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 'M'],
    ['x'.repeat(700), 'L'],
    ['WIFI:T:WPA;S:CasaMia;P:password123;;', 'M'],
  ];
  fs.mkdirSync('/tmp/qrtest', { recursive: true });
  const out = [];
  for (let i = 0; i < tests.length; i++) {
    const [text, ecl] = tests[i];
    const info = await page.evaluate(([t, e]) => {
      const qr = RTQR.encode(t, e);
      if (!qr) return null;
      RTQR.draw(qr, document.getElementById('c'), 6, 4);
      return { version: qr.version, ecl: qr.ecl, mask: qr.mask, size: qr.size, data: document.getElementById('c').toDataURL('image/png') };
    }, [text, ecl]);
    if (!info) { out.push({ i, error: 'too long' }); continue; }
    fs.writeFileSync(`/tmp/qrtest/qr${i}.png`, Buffer.from(info.data.split(',')[1], 'base64'));
    fs.writeFileSync(`/tmp/qrtest/qr${i}.txt`, text);
    out.push({ i, version: info.version, ecl: info.ecl, mask: info.mask, size: info.size });
  }
  console.log(JSON.stringify(out));
  await browser.close();
})();

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const qrjs = fs.readFileSync(path.join(__dirname, 'assets/qr.js'), 'utf8');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent('<canvas id="c"></canvas>');
  await page.addScriptTag({ content: qrjs });
  fs.mkdirSync('/tmp/qrsweep', { recursive: true });
  const out = [];
  let n = 0;
  // various lengths to hit many versions, all ECLs, boost off
  const lengths = [1, 5, 17, 32, 53, 78, 106, 134, 154, 192, 230, 271, 321, 367, 425, 458, 520, 586, 644, 718, 792, 858, 929, 1003, 1091, 1171, 1273, 1367, 1465, 1528, 1628, 1732, 1840, 1952, 2068, 2188, 2303, 2431, 2563, 2699, 2809, 2953];
  for (const len of lengths) {
    for (const ecl of ['L', 'M', 'Q', 'H']) {
      const text = Array.from({ length: len }, (_, i) => 'abcdefghijklmnopqrstuvwxyz0123456789 .:/-'[(i * 7 + len) % 41]).join('');
      const info = await page.evaluate(([t, e]) => {
        const qr = RTQR.encode(t, e, false);
        if (!qr) return null;
        const scale = qr.size > 100 ? 3 : 4;
        RTQR.draw(qr, document.getElementById('c'), scale, 4);
        return { version: qr.version, ecl: qr.ecl, mask: qr.mask, data: document.getElementById('c').toDataURL('image/png') };
      }, [text, ecl]);
      if (!info) { out.push({ len, ecl, error: 'too long' }); continue; }
      fs.writeFileSync(`/tmp/qrsweep/q${n}.png`, Buffer.from(info.data.split(',')[1], 'base64'));
      fs.writeFileSync(`/tmp/qrsweep/q${n}.txt`, text);
      out.push({ n, len, ecl: info.ecl, version: info.version, mask: info.mask });
      n++;
    }
  }
  fs.writeFileSync('/tmp/qrsweep/index.json', JSON.stringify(out));
  console.log('generated', n);
  await browser.close();
})();

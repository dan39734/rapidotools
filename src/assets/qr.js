/* Minimal QR Code encoder (byte mode, all versions 1-40, ECC L/M/Q/H).
   Original implementation for Rapido Tools, structured after the public-domain-style
   reference algorithm described in ISO/IEC 18004. No external dependencies. */
window.RTQR = (function () {
  var ECC = { L: { ord: 0, fb: 1 }, M: { ord: 1, fb: 0 }, Q: { ord: 2, fb: 3 }, H: { ord: 3, fb: 2 } };
  var ECC_CODEWORDS_PER_BLOCK = [
    [-1, 7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28, 28, 28, 30, 30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
    [-1, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28],
    [-1, 13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
    [-1, 17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]];
  var NUM_ECC_BLOCKS = [
    [-1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 7, 8, 8, 9, 9, 10, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 24, 25],
    [-1, 1, 1, 1, 2, 2, 4, 4, 4, 5, 5, 5, 8, 9, 9, 10, 10, 11, 13, 14, 16, 17, 17, 18, 20, 21, 23, 25, 26, 28, 29, 31, 33, 35, 37, 38, 40, 43, 45, 47, 49],
    [-1, 1, 1, 2, 2, 4, 4, 6, 6, 8, 8, 8, 10, 12, 16, 12, 17, 16, 18, 21, 20, 23, 23, 25, 27, 29, 34, 34, 35, 38, 40, 43, 45, 48, 51, 53, 56, 59, 62, 65, 68],
    [-1, 1, 1, 2, 4, 4, 4, 5, 6, 8, 8, 11, 11, 16, 16, 18, 16, 19, 21, 25, 25, 25, 34, 30, 32, 35, 37, 40, 42, 45, 48, 51, 54, 57, 60, 63, 66, 70, 74, 77, 81]];

  function rawDataModules(ver) {
    var r = (16 * ver + 128) * ver + 64;
    if (ver >= 2) { var n = Math.floor(ver / 7) + 2; r -= (25 * n - 10) * n - 55; if (ver >= 7) r -= 36; }
    return r;
  }
  function dataCodewords(ver, ecl) {
    return Math.floor(rawDataModules(ver) / 8) - ECC_CODEWORDS_PER_BLOCK[ecl.ord][ver] * NUM_ECC_BLOCKS[ecl.ord][ver];
  }
  function utf8(str) { return Array.prototype.slice.call(new TextEncoder().encode(str)); }
  function gfMul(x, y) { var z = 0; for (var i = 7; i >= 0; i--) { z = (z << 1) ^ ((z >>> 7) * 0x11D); z ^= ((y >>> i) & 1) * x; } return z; }
  function rsDivisor(deg) {
    var r = []; for (var i = 0; i < deg - 1; i++) r.push(0); r.push(1);
    var root = 1;
    for (var i = 0; i < deg; i++) {
      for (var j = 0; j < r.length; j++) { r[j] = gfMul(r[j], root); if (j + 1 < r.length) r[j] ^= r[j + 1]; }
      root = gfMul(root, 0x02);
    }
    return r;
  }
  function rsRemainder(data, div) {
    var res = div.map(function () { return 0; });
    data.forEach(function (b) {
      var f = b ^ res.shift(); res.push(0);
      div.forEach(function (c, i) { res[i] ^= gfMul(c, f); });
    });
    return res;
  }
  function alignPositions(ver) {
    if (ver === 1) return [];
    var n = Math.floor(ver / 7) + 2, size = ver * 4 + 17;
    var step = ver === 32 ? 26 : Math.ceil((ver * 4 + 4) / (n * 2 - 2)) * 2;
    var res = [6];
    for (var pos = size - 7; res.length < n; pos -= step) res.splice(1, 0, pos);
    return res;
  }
  function getBit(x, i) { return ((x >>> i) & 1) !== 0; }

  function encode(text, eclName, boost) {
    var ecl = ECC[eclName] || ECC.M;
    var data = utf8(text);
    var ver, bitsNeeded;
    for (ver = 1; ver <= 40; ver++) {
      var cap = dataCodewords(ver, ecl) * 8;
      bitsNeeded = 4 + (ver <= 9 ? 8 : 16) + data.length * 8;
      if (bitsNeeded <= cap) break;
      if (ver === 40) return null; // too long
    }
    if (boost !== false) { // raise ECC while it still fits
      [ECC.M, ECC.Q, ECC.H].forEach(function (e) { if (e.ord > ecl.ord && bitsNeeded <= dataCodewords(ver, e) * 8) ecl = e; });
    }
    // bit buffer
    var bb = [];
    function push(val, len) { for (var i = len - 1; i >= 0; i--) bb.push((val >>> i) & 1); }
    push(4, 4); push(data.length, ver <= 9 ? 8 : 16);
    data.forEach(function (b) { push(b, 8); });
    var capBits = dataCodewords(ver, ecl) * 8;
    push(0, Math.min(4, capBits - bb.length));
    push(0, (8 - bb.length % 8) % 8);
    for (var pb = 0xEC; bb.length < capBits; pb ^= 0xEC ^ 0x11) push(pb, 8);
    var cw = []; for (var i = 0; i < bb.length; i += 8) { var v = 0; for (var j = 0; j < 8; j++) v = (v << 1) | bb[i + j]; cw.push(v); }
    // split into blocks + ECC
    var nb = NUM_ECC_BLOCKS[ecl.ord][ver], be = ECC_CODEWORDS_PER_BLOCK[ecl.ord][ver];
    var raw = Math.floor(rawDataModules(ver) / 8), nShort = nb - raw % nb, shortLen = Math.floor(raw / nb);
    var blocks = [], div = rsDivisor(be), k = 0;
    for (var b = 0; b < nb; b++) {
      var len = shortLen - be + (b < nShort ? 0 : 1);
      var dat = cw.slice(k, k + len); k += len;
      var ecc = rsRemainder(dat, div);
      if (b < nShort) dat.push(-1);
      blocks.push(dat.concat(ecc));
    }
    var out = [];
    for (var i = 0; i < blocks[0].length; i++) for (var b = 0; b < nb; b++) { if (i === shortLen - be && b < nShort) continue; out.push(blocks[b][i]); }
    // matrix
    var size = ver * 4 + 17;
    var mod = [], fn = [];
    for (var y = 0; y < size; y++) { mod.push(new Array(size).fill(false)); fn.push(new Array(size).fill(false)); }
    function setF(x, y, dark) { mod[y][x] = dark; fn[y][x] = true; }
    function finder(x, y) { for (var dy = -4; dy <= 4; dy++) for (var dx = -4; dx <= 4; dx++) { var d = Math.max(Math.abs(dx), Math.abs(dy)), xx = x + dx, yy = y + dy; if (xx >= 0 && xx < size && yy >= 0 && yy < size) setF(xx, yy, d !== 2 && d !== 4); } }
    function align(x, y) { for (var dy = -2; dy <= 2; dy++) for (var dx = -2; dx <= 2; dx++) setF(x + dx, y + dy, Math.max(Math.abs(dx), Math.abs(dy)) !== 1); }
    function formatBits(mask) {
      var d = ecl.fb << 3 | mask, rem = d;
      for (var i = 0; i < 10; i++) rem = (rem << 1) ^ ((rem >>> 9) * 0x537);
      var bits = (d << 10 | rem) ^ 0x5412;
      for (var i = 0; i <= 5; i++) setF(8, i, getBit(bits, i));
      setF(8, 7, getBit(bits, 6)); setF(8, 8, getBit(bits, 7)); setF(7, 8, getBit(bits, 8));
      for (var i = 9; i < 15; i++) setF(14 - i, 8, getBit(bits, i));
      for (var i = 0; i < 8; i++) setF(size - 1 - i, 8, getBit(bits, i));
      for (var i = 8; i < 15; i++) setF(8, size - 15 + i, getBit(bits, i));
      setF(8, size - 8, true);
    }
    function versionBits() {
      if (ver < 7) return;
      var rem = ver; for (var i = 0; i < 12; i++) rem = (rem << 1) ^ ((rem >>> 11) * 0x1F25);
      var bits = ver << 12 | rem;
      for (var i = 0; i < 18; i++) { var c = getBit(bits, i), a = size - 11 + i % 3, b = Math.floor(i / 3); setF(a, b, c); setF(b, a, c); }
    }
    for (var i = 0; i < size; i++) { setF(6, i, i % 2 === 0); setF(i, 6, i % 2 === 0); }
    finder(3, 3); finder(size - 4, 3); finder(3, size - 4);
    var ap = alignPositions(ver), na = ap.length;
    for (var i = 0; i < na; i++) for (var j = 0; j < na; j++) { if ((i === 0 && j === 0) || (i === 0 && j === na - 1) || (i === na - 1 && j === 0)) continue; align(ap[i], ap[j]); }
    formatBits(0); versionBits();
    // place data
    var bi = 0, total = out.length * 8;
    for (var right = size - 1; right >= 1; right -= 2) {
      if (right === 6) right = 5;
      for (var vert = 0; vert < size; vert++) for (var j = 0; j < 2; j++) {
        var x = right - j, up = ((right + 1) & 2) === 0, y = up ? size - 1 - vert : vert;
        if (!fn[y][x] && bi < total) { mod[y][x] = getBit(out[bi >>> 3], 7 - (bi & 7)); bi++; }
      }
    }
    // masking
    function applyMask(m) {
      for (var y = 0; y < size; y++) for (var x = 0; x < size; x++) {
        var inv;
        switch (m) {
          case 0: inv = (x + y) % 2 === 0; break; case 1: inv = y % 2 === 0; break; case 2: inv = x % 3 === 0; break; case 3: inv = (x + y) % 3 === 0; break;
          case 4: inv = (Math.floor(x / 3) + Math.floor(y / 2)) % 2 === 0; break; case 5: inv = x * y % 2 + x * y % 3 === 0; break;
          case 6: inv = (x * y % 2 + x * y % 3) % 2 === 0; break; default: inv = ((x + y) % 2 + x * y % 3) % 2 === 0;
        }
        if (!fn[y][x] && inv) mod[y][x] = !mod[y][x];
      }
    }
    function penalty() {
      var res = 0;
      function addHist(run, h) { if (h[0] === 0) run += size; h.pop(); h.unshift(run); }
      function countPat(h) { var n = h[1]; var core = n > 0 && h[2] === n && h[3] === n * 3 && h[4] === n && h[5] === n; return (core && h[0] >= n * 4 && h[6] >= n ? 1 : 0) + (core && h[6] >= n * 4 && h[0] >= n ? 1 : 0); }
      function term(color, run, h) { if (color) { addHist(run, h); run = 0; } run += size; addHist(run, h); return countPat(h); }
      for (var y = 0; y < size; y++) {
        var rc = false, rx = 0, h = [0, 0, 0, 0, 0, 0, 0];
        for (var x = 0; x < size; x++) {
          if (mod[y][x] === rc) { rx++; if (rx === 5) res += 3; else if (rx > 5) res++; }
          else { addHist(rx, h); if (!rc) res += countPat(h) * 40; rc = mod[y][x]; rx = 1; }
        }
        res += term(rc, rx, h) * 40;
      }
      for (var x = 0; x < size; x++) {
        var rc = false, ry = 0, h = [0, 0, 0, 0, 0, 0, 0];
        for (var y = 0; y < size; y++) {
          if (mod[y][x] === rc) { ry++; if (ry === 5) res += 3; else if (ry > 5) res++; }
          else { addHist(ry, h); if (!rc) res += countPat(h) * 40; rc = mod[y][x]; ry = 1; }
        }
        res += term(rc, ry, h) * 40;
      }
      for (var y = 0; y < size - 1; y++) for (var x = 0; x < size - 1; x++) { var c = mod[y][x]; if (c === mod[y][x + 1] && c === mod[y + 1][x] && c === mod[y + 1][x + 1]) res += 3; }
      var dark = 0; mod.forEach(function (row) { row.forEach(function (c) { if (c) dark++; }); });
      var tot = size * size, kk = Math.ceil(Math.abs(dark * 20 - tot * 10) / tot) - 1; res += kk * 10;
      return res;
    }
    var best = -1, minP = Infinity;
    for (var m = 0; m < 8; m++) { applyMask(m); formatBits(m); var p = penalty(); if (p < minP) { minP = p; best = m; } applyMask(m); }
    applyMask(best); formatBits(best);
    return { size: size, modules: mod, version: ver, ecl: ['L', 'M', 'Q', 'H'][ecl.ord], mask: best };
  }
  function draw(qr, canvas, scale, border, dark, light) {
    scale = scale || 8; border = border === undefined ? 4 : border;
    var px = (qr.size + border * 2) * scale;
    canvas.width = px; canvas.height = px;
    var ctx = canvas.getContext('2d');
    ctx.fillStyle = light || '#ffffff'; ctx.fillRect(0, 0, px, px);
    ctx.fillStyle = dark || '#000000';
    for (var y = 0; y < qr.size; y++) for (var x = 0; x < qr.size; x++) if (qr.modules[y][x]) ctx.fillRect((x + border) * scale, (y + border) * scale, scale, scale);
  }
  return { encode: encode, draw: draw };
})();

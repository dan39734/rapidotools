/* Rapido Tools – shared helpers (no dependencies) */
window.RT = (function () {
  var lang = document.documentElement.lang || 'it';
  var locale = lang === 'it' ? 'it-IT' : 'en-US';
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function num(v) {
    if (v === null || v === undefined) return NaN;
    var s = String(v).trim().replace(/\s/g, '');
    if (!s) return NaN;
    // accept both 1.234,56 and 1,234.56 and 1234.56 / 1234,56
    var lastComma = s.lastIndexOf(','), lastDot = s.lastIndexOf('.');
    if (lastComma > -1 && lastDot > -1) {
      if (lastComma > lastDot) s = s.replace(/\./g, '').replace(',', '.');
      else s = s.replace(/,/g, '');
    } else if (lastComma > -1) {
      s = s.replace(',', '.');
    }
    return parseFloat(s);
  }
  function fmt(n, d) {
    if (!isFinite(n)) return '–';
    return new Intl.NumberFormat(locale, { maximumFractionDigits: d === undefined ? 2 : d }).format(n);
  }
  function fmtFixed(n, d) {
    if (!isFinite(n)) return '–';
    return new Intl.NumberFormat(locale, { minimumFractionDigits: d, maximumFractionDigits: d }).format(n);
  }
  function money(n, cur) {
    if (!isFinite(n)) return '–';
    if (!cur && lang !== 'it') return fmtFixed(n, 2); // English: currency-neutral
    try { return new Intl.NumberFormat(locale, { style: 'currency', currency: cur || 'EUR' }).format(n); }
    catch (e) { return fmtFixed(n, 2); }
  }
  function date(d, opts) {
    return new Intl.DateTimeFormat(locale, opts || { day: 'numeric', month: 'long', year: 'numeric' }).format(d);
  }
  function weekday(d) { return new Intl.DateTimeFormat(locale, { weekday: 'long' }).format(d); }
  function copy(text, btn) {
    var done = function () {
      if (!btn) return;
      var old = btn.textContent; btn.textContent = btn.getAttribute('data-done') || '✓';
      setTimeout(function () { btn.textContent = old; }, 1400);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallback(text); done(); });
    } else { fallback(text); done(); }
    function fallback(t) {
      var ta = document.createElement('textarea'); ta.value = t; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (e) { } document.body.removeChild(ta);
    }
  }
  function download(blobOrUrl, filename) {
    var a = document.createElement('a');
    var url = typeof blobOrUrl === 'string' ? blobOrUrl : URL.createObjectURL(blobOrUrl);
    a.href = url; a.download = filename; document.body.appendChild(a); a.click(); document.body.removeChild(a);
    if (typeof blobOrUrl !== 'string') setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
  }
  function bytes(n) {
    if (n < 1024) return n + ' B';
    if (n < 1048576) return fmt(n / 1024, 1) + ' KB';
    return fmt(n / 1048576, 2) + ' MB';
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function isoToday() { var d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function parseDate(s) { // yyyy-mm-dd -> local Date
    if (!s) return null; var p = s.split('-'); if (p.length !== 3) return null;
    var d = new Date(+p[0], +p[1] - 1, +p[2]); return isNaN(d) ? null : d;
  }
  function daysBetween(a, b) { // whole days, ignoring DST
    var ua = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
    var ub = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());
    return Math.round((ub - ua) / 86400000);
  }
  function live(container, fn) { // run fn on any input change inside container
    $$('input,select,textarea', container).forEach(function (el) {
      el.addEventListener('input', fn); el.addEventListener('change', fn);
    });
    fn();
  }
  function onClick(sel, fn) { $$(sel).forEach(function (el) { el.addEventListener('click', function (e) { fn(e, el); }); }); }
  function beep(times) {
    try {
      var ctx = new (window.AudioContext || window.webkitAudioContext)();
      var t = ctx.currentTime;
      for (var i = 0; i < (times || 3); i++) {
        var o = ctx.createOscillator(), g = ctx.createGain();
        o.type = 'sine'; o.frequency.value = 880; o.connect(g); g.connect(ctx.destination);
        g.gain.setValueAtTime(0.0001, t + i * 0.35); g.gain.exponentialRampToValueAtTime(0.4, t + i * 0.35 + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, t + i * 0.35 + 0.3);
        o.start(t + i * 0.35); o.stop(t + i * 0.35 + 0.32);
      }
    } catch (e) { }
  }
  // language switch memory + home search
  document.addEventListener('DOMContentLoaded', function () {
    $$('a[data-setlang]').forEach(function (a) {
      a.addEventListener('click', function () { try { localStorage.setItem('rt-lang', a.getAttribute('data-setlang')); } catch (e) { } });
    });
    var search = $('#tool-search');
    if (search) {
      var cards = $$('.card[data-search]'), cats = $$('.cat'), empty = $('.empty');
      search.addEventListener('input', function () {
        var q = search.value.trim().toLowerCase();
        var shown = 0;
        cards.forEach(function (c) { var ok = !q || c.getAttribute('data-search').indexOf(q) > -1; c.style.display = ok ? '' : 'none'; if (ok) shown++; });
        cats.forEach(function (s) { var any = $$('.card', s).some(function (c) { return c.style.display !== 'none'; }); s.style.display = any ? '' : 'none'; });
        if (empty) empty.style.display = shown ? 'none' : 'block';
      });
    }
    $$('[data-copy]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var src = $(btn.getAttribute('data-copy'));
        if (src) copy(src.value !== undefined ? src.value : src.textContent, btn);
      });
    });
  });
  return { lang: lang, locale: locale, $: $, $$: $$, num: num, fmt: fmt, fmtFixed: fmtFixed, money: money, date: date, weekday: weekday,
    copy: copy, download: download, bytes: bytes, pad: pad, isoToday: isoToday, parseDate: parseDate, daysBetween: daysBetween, live: live, onClick: onClick, beep: beep };
})();

TOOL = {
    "id": "roman",
    "cat": "numbers",
    "icon": "🏛️",
    "slug": {"it": "numeri-romani", "en": "roman-numerals"},
    "title": {"it": "Convertitore numeri romani", "en": "Roman numerals converter"},
    "short": {"it": "Da numero a romano e viceversa, da 1 a 3999, con tabella", "en": "Number to Roman and back, from 1 to 3999, with a reference table"},
    "keywords": {"it": ["numeri romani da 1 a 100", "2026 in numeri romani", "MMXXVI", "come si scrive in romano"], "en": ["2026 in roman numerals", "MMXXVI", "roman numeral chart", "convert roman"]},
    "meta": {
        "it": "Converti un numero in numeri romani e un numero romano in cifre arabe (da 1 a 3999). Con le regole di scrittura, gli anni in romano e la tabella da 1 a 100.",
        "en": "Convert a number to Roman numerals and a Roman numeral to Arabic digits (from 1 to 3999). With writing rules, years in Roman numerals and a chart from 1 to 100.",
    },
    "intro": {
        "it": "Scrivi un numero (per esempio 2026) o un numero romano (MMXXVI): la conversione avviene mentre digiti, in entrambe le direzioni.",
        "en": "Type a number (for example 2026) or a Roman numeral (MMXXVI): the conversion happens as you type, in both directions.",
    },
    "strings": {
        "it": {"num": "Numero (1–3999)", "rom": "Numero romano", "bad": "Numero romano non valido", "range": "Inserisci un numero intero tra 1 e 3999", "table": "Tabella rapida", "year": "Anno corrente"},
        "en": {"num": "Number (1–3999)", "rom": "Roman numeral", "bad": "Invalid Roman numeral", "range": "Enter a whole number between 1 and 3999", "table": "Quick chart", "year": "Current year"},
    },
    "ui": """
<div class="row">
  <div class="field"><label for="num">{{num}}</label><input type="text" inputmode="numeric" id="num" value="2026"></div>
  <div class="field"><label for="rom">{{rom}}</label><input type="text" id="rom" value="MMXXVI" style="text-transform:uppercase" autocapitalize="characters"></div>
</div>
<p class="msg" id="msg"></p>
<div class="result">
  <div class="big" id="out"></div>
  <div class="sub" id="explain"></div>
</div>
<div class="lbl" style="margin-top:14px">{{table}}</div>
<div class="table-wrap"><table id="tbl"></table></div>
""",
    "js": r"""
var num = RT.$('#num'), rom = RT.$('#rom'), out = RT.$('#out'), msg = RT.$('#msg'), explain = RT.$('#explain');
var MAP = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'], [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'], [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I']];
function toRoman(n) { var s = '', parts = []; MAP.forEach(function (p) { while (n >= p[0]) { s += p[1]; parts.push(p[1] + '=' + p[0]); n -= p[0]; } }); return [s, parts]; }
function fromRoman(s) { var r = toRomanStrict(s); return r; }
function toRomanStrict(s) {
  s = s.toUpperCase().trim(); if (!/^[MDCLXVI]+$/.test(s)) return NaN;
  var i = 0, n = 0;
  MAP.forEach(function (p) { while (s.substr(i, p[1].length) === p[1]) { n += p[0]; i += p[1].length; } });
  if (i !== s.length) return NaN;
  return toRoman(n)[0] === s ? n : NaN;
}
var lock = false;
num.addEventListener('input', function () {
  if (lock) return; lock = true;
  var n = parseInt(num.value.replace(/\D/g, ''), 10);
  if (n >= 1 && n <= 3999) { var r = toRoman(n); rom.value = r[0]; out.textContent = n + ' = ' + r[0]; explain.textContent = r[1].join(' + '); msg.textContent = ''; }
  else { out.textContent = '–'; explain.textContent = ''; msg.textContent = T.range; }
  lock = false;
});
rom.addEventListener('input', function () {
  if (lock) return; lock = true;
  var n = toRomanStrict(rom.value);
  if (isFinite(n)) { num.value = n; out.textContent = rom.value.toUpperCase() + ' = ' + n; explain.textContent = toRoman(n)[1].join(' + '); msg.textContent = ''; }
  else { out.textContent = '–'; explain.textContent = ''; msg.textContent = rom.value ? T.bad : ''; }
  lock = false;
});
num.dispatchEvent(new Event('input'));
var tbl = RT.$('#tbl'), rows = '';
var list = [];
for (var i = 1; i <= 20; i++) list.push(i);
[30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2026, 2500, 3000, 3999].forEach(function (x) { list.push(x); });
for (var j = 0; j < list.length; j += 4) { rows += '<tr>' + list.slice(j, j + 4).map(function (x) { return '<td><b>' + x + '</b> ' + toRoman(x)[0] + '</td>'; }).join('') + '</tr>'; }
tbl.innerHTML = rows;
""",
    "article": {
        "it": """
<h2>Come funzionano i numeri romani</h2>
<p>Si usano sette lettere: <strong>I</strong> = 1, <strong>V</strong> = 5, <strong>X</strong> = 10, <strong>L</strong> = 50, <strong>C</strong> = 100, <strong>D</strong> = 500, <strong>M</strong> = 1000. Le lettere si scrivono dalla più grande alla più piccola e si sommano: MMXXVI = 1000 + 1000 + 10 + 10 + 5 + 1 = 2026.</p>
<h2>La regola della sottrazione</h2>
<p>Quando una lettera più piccola precede una più grande, si sottrae: IV = 4, IX = 9, XL = 40, XC = 90, CD = 400, CM = 900. Si può sottrarre solo I, X e C, e solo dalle due lettere immediatamente superiori: 99 si scrive XCIX, non IC. Una stessa lettera non si ripete più di tre volte di seguito (4 è IV, non IIII, con l'eccezione tradizionale degli orologi).</p>
<h2>Dove si usano ancora</h2>
<ul>
<li>Anni sui monumenti, nei titoli di coda dei film e nelle date di fondazione: MCMXCIX = 1999, MMXXVI = 2026.</li>
<li>Nomi di papi e sovrani (Giovanni XXIII, Luigi XIV), secoli (XXI secolo), capitoli e volumi.</li>
<li>Edizioni di eventi come Olimpiadi e Super Bowl, numeri delle ore sui quadranti.</li>
</ul>
<p>Il sistema romano non ha lo zero e non prevede numeri superiori a 3999 senza notazioni speciali (una barra sopra la lettera moltiplica per 1000); per questo il convertitore si ferma a MMMCMXCIX.</p>
""",
        "en": """
<h2>How Roman numerals work</h2>
<p>Seven letters are used: <strong>I</strong> = 1, <strong>V</strong> = 5, <strong>X</strong> = 10, <strong>L</strong> = 50, <strong>C</strong> = 100, <strong>D</strong> = 500, <strong>M</strong> = 1000. Letters are written from largest to smallest and added up: MMXXVI = 1000 + 1000 + 10 + 10 + 5 + 1 = 2026.</p>
<h2>The subtraction rule</h2>
<p>When a smaller letter comes before a larger one, it is subtracted: IV = 4, IX = 9, XL = 40, XC = 90, CD = 400, CM = 900. Only I, X and C can be subtracted, and only from the next two larger letters: 99 is XCIX, not IC. The same letter is never repeated more than three times in a row (4 is IV, not IIII, with the traditional exception of clock faces).</p>
<h2>Where they are still used</h2>
<ul>
<li>Years on monuments, in film credits and founding dates: MCMXCIX = 1999, MMXXVI = 2026.</li>
<li>Names of popes and monarchs (John XXIII, Louis XIV), centuries (21st century), chapters and volumes.</li>
<li>Editions of events such as the Olympics and the Super Bowl, hour marks on clock faces.</li>
</ul>
<p>The Roman system has no zero and no standard way to write numbers above 3999 (a bar over a letter multiplies it by 1000), which is why the converter stops at MMMCMXCIX.</p>
""",
    },
    "faq": {
        "it": [
            ("Come si scrive 2026 in numeri romani?", "MMXXVI: MM (2000) + XX (20) + VI (6)."),
            ("Perché il convertitore dice che IIII o IC non sono validi?", "Perché non rispettano le regole standard: 4 si scrive IV e 99 si scrive XCIX. Il convertitore accetta solo la forma canonica, la stessa usata su monumenti e documenti."),
            ("Qual è il numero romano più grande?", "Con la notazione normale 3999, cioè MMMCMXCIX. Per numeri più grandi si usa una barra sopra le lettere, che moltiplica per mille."),
        ],
        "en": [
            ("How do you write 2026 in Roman numerals?", "MMXXVI: MM (2000) + XX (20) + VI (6)."),
            ("Why does the converter say IIII or IC are invalid?", "Because they break the standard rules: 4 is written IV and 99 is XCIX. The converter accepts only the canonical form, the same one used on monuments and documents."),
            ("What is the largest Roman numeral?", "With standard notation 3999, i.e. MMMCMXCIX. Larger numbers use a bar over the letters, which multiplies them by a thousand."),
        ],
    },
}

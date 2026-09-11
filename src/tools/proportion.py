"""Proporzioni: regola del tre (diretta/inversa), a : b = c : d con l'incognita dove si vuole, dosi delle ricette (persone o stampo)."""

_JS = r"""
var mode = 'three';
var FR = { '½': 1 / 2, '¼': 1 / 4, '¾': 3 / 4, '⅓': 1 / 3, '⅔': 2 / 3, '⅛': 1 / 8 };
function v(id) { return RT.num(RT.$('#' + id).value); }
function f(n) { return RT.fmt(n, 6); }
// --- rule of three
function calcThree() {
  var a = v('ta'), b = v('tb'), c = v('tc'), inv = RT.$('input[name="kind"]:checked').value === 'i', res = RT.$('#tres'), sub = RT.$('#tsub');
  if (![a, b, c].every(isFinite)) { res.textContent = '–'; sub.textContent = T.fill3; return; }
  if ((!inv && a === 0) || (inv && c === 0)) { res.textContent = '–'; sub.textContent = T.div0; return; }
  var x = inv ? a * b / c : b * c / a;
  res.textContent = 'x = ' + f(x);
  sub.textContent = inv ? 'x = ' + f(a) + ' × ' + f(b) + ' ÷ ' + f(c) + ' (' + T.inverse_s + ')' : 'x = ' + f(b) + ' × ' + f(c) + ' ÷ ' + f(a) + ' (' + T.direct_s + ')';
}
// --- a : b = c : d
function calcProp() {
  var ids = ['pa', 'pb', 'pc', 'pd'], vals = ids.map(function (id) { return RT.$('#' + id).value.trim() === '' ? null : v(id); });
  var res = RT.$('#pres'), sub = RT.$('#psub'), empty = vals.filter(function (x) { return x === null; }).length;
  if (vals.some(function (x) { return x !== null && !isFinite(x); })) { res.textContent = '–'; sub.textContent = T.invalid; return; }
  if (empty > 1) { res.textContent = '–'; sub.textContent = T.one_empty; return; }
  var a = vals[0], b = vals[1], c = vals[2], d = vals[3];
  if (empty === 0) {
    var ok = Math.abs(a * d - b * c) <= 1e-9 * Math.max(1, Math.abs(a * d), Math.abs(b * c));
    res.textContent = ok ? T.is_ok : T.is_not;
    sub.textContent = f(a) + ' × ' + f(d) + (ok ? ' = ' : ' ≠ ') + f(b) + ' × ' + f(c) + ' (' + f(a * d) + (ok ? ' = ' : ' ≠ ') + f(b * c) + ')';
    return;
  }
  var x, how;
  if (a === null) { if (d === 0) return fail0(); x = b * c / d; how = f(b) + ' × ' + f(c) + ' ÷ ' + f(d); }
  else if (b === null) { if (c === 0) return fail0(); x = a * d / c; how = f(a) + ' × ' + f(d) + ' ÷ ' + f(c); }
  else if (c === null) { if (b === 0) return fail0(); x = a * d / b; how = f(a) + ' × ' + f(d) + ' ÷ ' + f(b); }
  else { if (a === 0) return fail0(); x = b * c / a; how = f(b) + ' × ' + f(c) + ' ÷ ' + f(a); }
  res.textContent = 'x = ' + f(x);
  sub.textContent = 'x = ' + how;
  function fail0() { res.textContent = '–'; sub.textContent = T.div0; }
}
// --- recipe
function parseLead(s) {
  var m, val = null;
  if ((m = s.match(/^(\s*)(\d+)\s+(\d+)\s*\/\s*(\d+)/))) val = +m[2] + m[3] / m[4];
  else if ((m = s.match(/^(\s*)(\d+)\s*\/\s*(\d+)/))) val = m[2] / m[3];
  else if ((m = s.match(/^(\s*)(\d*)\s*([½¼¾⅓⅔⅛])/))) val = (m[2] ? +m[2] : 0) + FR[m[3]];
  else if ((m = s.match(/^(\s*)(\d{1,3}(?:\.\d{3})+|\d{1,3}(?:,\d{3})+|\d+(?:[.,]\d+)?)(?![\d\/])/))) {
    var t = m[2], thou = RT.lang === 'it' ? /^\d{1,3}(\.\d{3})+$/ : /^\d{1,3}(,\d{3})+$/;
    val = thou.test(t) ? parseFloat(t.replace(/[.,]/g, '')) : parseFloat(t.replace(',', '.'));
  }
  if (val === null || !isFinite(val)) return null;
  return { pre: m[1], val: val, rest: s.slice(m[0].length) };
}
function fq(x) {
  if (x >= 10) return RT.fmt(Math.round(x), 0);
  if (x >= 1) return RT.fmt(Math.round(x * 10) / 10, 1);
  return RT.fmt(Math.round(x * 100) / 100, 2);
}
function area(shape, a, b) { return shape === 'r' ? Math.PI * a * a / 4 : a * b; }
function panUi(n) {
  var round = RT.$('#s' + n).value === 'r';
  RT.$('#la' + n).textContent = round ? T.diam : T.side1;
  RT.$('#wb' + n).classList.toggle('hide', round);
}
function factor() {
  var by = RT.$('#by').value;
  ['people', 'pan', 'factor'].forEach(function (k) { RT.$('#w-' + k).classList.toggle('hide', k !== by); });
  if (by === 'people') {
    var p1 = v('p1'), p2 = v('p2');
    if (!(p1 > 0) || !(p2 > 0)) return null;
    return { k: p2 / p1, sub: T.people_sub.replace('{a}', RT.fmt(p1, 2)).replace('{b}', RT.fmt(p2, 2)) };
  }
  if (by === 'pan') {
    panUi(1); panUi(2);
    var s1 = RT.$('#s1').value, s2 = RT.$('#s2').value, A1 = area(s1, v('a1'), v('b1')), A2 = area(s2, v('a2'), v('b2'));
    if (!(A1 > 0) || !(A2 > 0)) return null;
    return { k: A2 / A1, sub: T.pan_sub.replace('{a}', RT.fmt(A1, 0)).replace('{b}', RT.fmt(A2, 0)) };
  }
  var k = v('fx');
  return k > 0 ? { k: k, sub: '' } : null;
}
function calcRecipe() {
  var F = factor(), res = RT.$('#rfac'), sub = RT.$('#rsub'), outTa = RT.$('#rout');
  if (!F) { res.textContent = '–'; sub.textContent = T.invalid; outTa.value = ''; return; }
  res.textContent = T.factor_is.replace('{k}', RT.fmt(F.k, 3));
  sub.textContent = F.sub;
  outTa.value = RT.$('#ing').value.split('\n').map(function (line) {
    var p = parseLead(line);
    return p ? p.pre + fq(p.val * F.k) + p.rest : line;
  }).join('\n');
}
function calc() { if (mode === 'three') calcThree(); else if (mode === 'prop') calcProp(); else calcRecipe(); }
RT.$$('.tabs button').forEach(function (b) {
  b.addEventListener('click', function () {
    RT.$$('.tabs button').forEach(function (x) { x.classList.toggle('on', x === b); });
    mode = b.getAttribute('data-tab');
    ['three', 'prop', 'recipe'].forEach(function (k) { RT.$('#tab-' + k).classList.toggle('hide', k !== mode); });
    calc();
  });
});
RT.$('#ing').value = T.sample;
RT.live(document.getElementById('tool'), calc);
"""

TOOL = {
    "id": "proportion",
    "cat": "numbers",
    "icon": "🧮",
    "slug": {"it": "calcolo-proporzioni", "en": "proportion-calculator"},
    "title": {"it": "Calcolo proporzioni e dosi delle ricette", "en": "Proportion calculator and recipe scaler"},
    "short": {"it": "Regola del tre, proporzioni a : b = c : x e dosi di una ricetta per più persone o un altro stampo", "en": "Rule of three, a : b = c : x proportions and recipe scaling for more people or another pan"},
    "keywords": {
        "it": ["proporzioni", "calcolo proporzione", "proporzione con la x", "regola del tre", "proporzionalità inversa", "dosi ricetta", "dosi per persone", "teglia", "tortiera", "stampo", "conversione dosi torta"],
        "en": ["proportion calculator", "rule of three", "inverse proportion", "recipe scaler", "scale recipe", "cake pan size converter", "recipe converter"],
    },
    "meta": {
        "it": "Risolvi una proporzione (a : b = c : x) e la regola del tre, diretta o inversa, con i passaggi. Adatta le dosi di una ricetta a più o meno persone o a una tortiera più grande o più piccola, rotonda o rettangolare.",
        "en": "Solve a proportion (a : b = c : x) and the rule of three, direct or inverse, with the working shown. Scale a recipe for more or fewer people or for a bigger or smaller round or rectangular pan.",
    },
    "intro": {
        "it": "Tre strumenti: la regola del tre (diretta o inversa), la proporzione con l'incognita nella casella che vuoi e le dosi di una ricetta da adattare alle persone o allo stampo.",
        "en": "Three tools: the rule of three (direct or inverse), a proportion with the unknown in any box, and a recipe scaler for a different number of people or a different pan.",
    },
    "strings": {
        "it": {
            "tab_three": "Regola del tre", "tab_prop": "a : b = c : d", "tab_recipe": "Dosi ricetta",
            "if_": "Se", "goes_with": "corrisponde a", "then_": "allora", "goes_with_x": "corrisponde a x",
            "direct": "Diretta (se uno cresce, cresce anche l'altro)", "inverse": "Inversa (se uno cresce, l'altro cala)",
            "direct_s": "proporzionalità diretta", "inverse_s": "proporzionalità inversa",
            "fill3": "Inserisci i tre numeri.", "div0": "Impossibile: si dovrebbe dividere per zero.",
            "leave_empty": "Lascia vuota la casella da trovare. Se le riempi tutte, controllo se la proporzione è giusta.",
            "one_empty": "Lascia vuota una sola casella.", "is_ok": "La proporzione è corretta ✓", "is_not": "Non è una proporzione ✗",
            "by_l": "Adatta le dosi in base a", "by_people": "Numero di persone", "by_pan": "Dimensione dello stampo", "by_factor": "Un moltiplicatore",
            "p_from": "Persone della ricetta", "p_to": "Persone che vuoi servire",
            "pan_from": "Stampo della ricetta", "pan_to": "Il tuo stampo", "round": "Rotondo", "rect": "Rettangolare o quadrato",
            "diam": "Diametro (cm)", "side1": "Lato lungo (cm)", "side2": "Lato corto (cm)",
            "factor_l": "Moltiplica per", "ing_l": "Ingredienti (uno per riga, con la quantità all'inizio)",
            "factor_is": "Dosi × {k}", "people_sub": "Da {a} a {b} persone", "pan_sub": "Superficie: da {a} cm² a {b} cm²",
            "res_l": "Nuove dosi",
            "sample": "250 g farina 00\n150 g zucchero\n3 uova\n100 ml latte\n80 g burro\n1/2 bustina di lievito\n1 pizzico di sale\nscorza di limone q.b.",
        },
        "en": {
            "tab_three": "Rule of three", "tab_prop": "a : b = c : d", "tab_recipe": "Recipe scaler",
            "if_": "If", "goes_with": "goes with", "then_": "then", "goes_with_x": "goes with x",
            "direct": "Direct (when one grows, so does the other)", "inverse": "Inverse (when one grows, the other shrinks)",
            "direct_s": "direct proportion", "inverse_s": "inverse proportion",
            "fill3": "Enter the three numbers.", "div0": "Impossible: it would mean dividing by zero.",
            "leave_empty": "Leave the box you want to find empty. If you fill them all, I check whether the proportion holds.",
            "one_empty": "Leave only one box empty.", "is_ok": "The proportion is correct ✓", "is_not": "Not a proportion ✗",
            "by_l": "Scale the recipe by", "by_people": "Number of people", "by_pan": "Pan size", "by_factor": "A multiplier",
            "p_from": "People in the recipe", "p_to": "People you want to serve",
            "pan_from": "Pan in the recipe", "pan_to": "Your pan", "round": "Round", "rect": "Rectangular or square",
            "diam": "Diameter (cm)", "side1": "Long side (cm)", "side2": "Short side (cm)",
            "factor_l": "Multiply by", "ing_l": "Ingredients (one per line, quantity first)",
            "factor_is": "Quantities × {k}", "people_sub": "From {a} to {b} people", "pan_sub": "Area: from {a} cm² to {b} cm²",
            "res_l": "New quantities",
            "sample": "250 g plain flour\n150 g sugar\n3 eggs\n100 ml milk\n80 g butter\n1/2 sachet baking powder\n1 pinch of salt\nlemon zest to taste",
        },
    },
    "ui": """
<div class="tabs" role="tablist">
  <button type="button" class="on" data-tab="three">{{tab_three}}</button>
  <button type="button" data-tab="prop">{{tab_prop}}</button>
  <button type="button" data-tab="recipe">{{tab_recipe}}</button>
</div>
<div id="tab-three">
  <div class="inline"><span>{{if_}}</span><input type="text" inputmode="decimal" id="ta" value="3" style="width:100px" aria-label="A"><span>{{goes_with}}</span><input type="text" inputmode="decimal" id="tb" value="12" style="width:100px" aria-label="B"><span>{{then_}}</span><input type="text" inputmode="decimal" id="tc" value="5" style="width:100px" aria-label="C"><span>{{goes_with_x}}</span></div>
  <div style="margin-top:10px">
    <label class="check"><input type="radio" name="kind" value="d" checked> {{direct}}</label>
    <label class="check"><input type="radio" name="kind" value="i"> {{inverse}}</label>
  </div>
  <div class="result"><div class="big" id="tres"></div><div class="sub" id="tsub"></div></div>
</div>
<div id="tab-prop" class="hide">
  <div class="inline" style="font-size:1.3rem;font-weight:700">
    <input type="text" inputmode="decimal" id="pa" value="2" style="width:90px" aria-label="a"><span>:</span>
    <input type="text" inputmode="decimal" id="pb" value="5" style="width:90px" aria-label="b"><span>=</span>
    <input type="text" inputmode="decimal" id="pc" value="6" style="width:90px" aria-label="c"><span>:</span>
    <input type="text" inputmode="decimal" id="pd" value="" style="width:90px" aria-label="d" placeholder="x">
  </div>
  <p class="msg">{{leave_empty}}</p>
  <div class="result"><div class="big" id="pres"></div><div class="sub" id="psub"></div></div>
</div>
<div id="tab-recipe" class="hide">
  <div class="field"><label for="by">{{by_l}}</label><select id="by"><option value="people">{{by_people}}</option><option value="pan">{{by_pan}}</option><option value="factor">{{by_factor}}</option></select></div>
  <div class="row" id="w-people">
    <div class="field"><label for="p1">{{p_from}}</label><input type="number" id="p1" min="1" step="1" value="4"></div>
    <div class="field"><label for="p2">{{p_to}}</label><input type="number" id="p2" min="1" step="1" value="6"></div>
  </div>
  <div id="w-pan" class="hide">
    <div class="row">
      <div class="field"><label for="s1">{{pan_from}}</label><select id="s1"><option value="r">{{round}}</option><option value="q">{{rect}}</option></select></div>
      <div class="field"><label for="a1" id="la1">{{diam}}</label><input type="text" inputmode="decimal" id="a1" value="24"></div>
      <div class="field hide" id="wb1"><label for="b1">{{side2}}</label><input type="text" inputmode="decimal" id="b1" value="20"></div>
    </div>
    <div class="row">
      <div class="field"><label for="s2">{{pan_to}}</label><select id="s2"><option value="r">{{round}}</option><option value="q">{{rect}}</option></select></div>
      <div class="field"><label for="a2" id="la2">{{diam}}</label><input type="text" inputmode="decimal" id="a2" value="28"></div>
      <div class="field hide" id="wb2"><label for="b2">{{side2}}</label><input type="text" inputmode="decimal" id="b2" value="20"></div>
    </div>
  </div>
  <div class="row hide" id="w-factor"><div class="field"><label for="fx">{{factor_l}}</label><input type="text" inputmode="decimal" id="fx" value="1,5"></div></div>
  <div class="field"><label for="ing">{{ing_l}}</label><textarea id="ing" style="min-height:190px"></textarea></div>
  <div class="result">
    <div class="big" id="rfac"></div>
    <div class="sub" id="rsub"></div>
    <div class="out" style="margin-top:10px"><textarea id="rout" readonly aria-label="{{res_l}}" style="min-height:190px"></textarea><button class="btn small copy" type="button" data-copy="#rout" data-done="{{copied}}">{{copy}}</button></div>
  </div>
</div>
""",
    "js": _JS,
    "article": {
        "it": """
<h2>La regola del tre: proporzionalità diretta e inversa</h2>
<p>Due grandezze sono <strong>direttamente proporzionali</strong> quando, se una raddoppia, raddoppia anche l'altra: se 3 kg di mele costano 12 €, 5 kg costano 12 × 5 ÷ 3 = <strong>20 €</strong>. Sono <strong>inversamente proporzionali</strong> quando, se una raddoppia, l'altra si dimezza: se 4 operai finiscono un lavoro in 6 giorni, 3 operai ci mettono 4 × 6 ÷ 3 = <strong>8 giorni</strong>. Nella prima scheda scrivi i tre numeri che conosci e scegli il tipo di proporzionalità.</p>
<h2>Come si risolve una proporzione a : b = c : d</h2>
<p>In una proporzione il prodotto dei medi (b e c) è uguale al prodotto degli estremi (a e d): a × d = b × c. Per trovare un estremo si moltiplicano i medi e si divide per l'altro estremo; per trovare un medio si moltiplicano gli estremi e si divide per l'altro medio. Esempio: 2 : 5 = 6 : x → x = 5 × 6 ÷ 2 = <strong>15</strong>. Nella seconda scheda puoi lasciare vuota qualsiasi casella; se le riempi tutte e quattro, il calcolatore controlla se la proporzione è giusta.</p>
<h2>Come adattare le dosi di una ricetta</h2>
<p>Per cambiare il numero di persone si moltiplica ogni ingrediente per il rapporto tra le persone: da 4 a 6 persone il fattore è 6 ÷ 4 = 1,5, quindi 250 g di farina diventano 375 g. Per cambiare stampo conta la <strong>superficie</strong>, non il diametro: una tortiera da 28 cm ha una superficie 1,36 volte quella da 24 cm (28² ÷ 24²), quindi le dosi vanno moltiplicate per 1,36 e non per 28 ÷ 24 = 1,17. Il calcolatore fa il conto anche tra stampi rotondi e rettangolari, a parità di altezza dell'impasto.</p>
<p>Le uova si arrotondano all'intero più vicino oppure si pesano: un uovo medio sgusciato pesa circa 50 grammi. Lievito, sale e spezie seguono lo stesso fattore. Per la cottura non c'è una regola fissa: in uno stampo più grande e più basso la torta cuoce un po' prima, in uno più alto un po' dopo, quindi fai la prova dello stecchino.</p>
""",
        "en": """
<h2>The rule of three: direct and inverse proportion</h2>
<p>Two quantities are <strong>directly proportional</strong> when doubling one doubles the other: if 3 kg of apples cost 12, then 5 kg cost 12 × 5 ÷ 3 = <strong>20</strong>. They are <strong>inversely proportional</strong> when doubling one halves the other: if 4 workers finish a job in 6 days, 3 workers take 4 × 6 ÷ 3 = <strong>8 days</strong>. In the first tab, type the three numbers you know and choose the type of proportion.</p>
<h2>How to solve a proportion a : b = c : d</h2>
<p>In a proportion the product of the means (b and c) equals the product of the extremes (a and d): a × d = b × c. To find an extreme, multiply the means and divide by the other extreme; to find a mean, multiply the extremes and divide by the other mean. Example: 2 : 5 = 6 : x → x = 5 × 6 ÷ 2 = <strong>15</strong>. In the second tab you can leave any box empty; if you fill all four, the calculator checks whether the proportion holds.</p>
<h2>How to scale a recipe</h2>
<p>To change the number of servings, multiply every ingredient by the ratio between the people: from 4 to 6 people the factor is 6 ÷ 4 = 1.5, so 250 g of flour becomes 375 g. To change the pan, what matters is the <strong>area</strong>, not the diameter: a 28 cm round pan has 1.36 times the area of a 24 cm one (28² ÷ 24²), so the quantities are multiplied by 1.36, not by 28 ÷ 24 = 1.17. The calculator also converts between round and rectangular pans, assuming the same batter depth.</p>
<p>Round eggs to the nearest whole egg or weigh them: a medium egg without its shell weighs about 50 grams. Baking powder, salt and spices follow the same factor. There is no fixed rule for baking time: in a bigger, shallower pan the cake bakes a little faster, in a deeper one a little slower, so check with a skewer.</p>
""",
    },
    "faq": {
        "it": [
            ("Come si calcola una proporzione con la x?", "Si moltiplicano i due numeri «in croce» e si divide per il terzo: in 2 : 5 = 6 : x, x = 5 × 6 ÷ 2 = 15."),
            ("Da una tortiera da 24 cm a una da 26 cm come cambiano le dosi?", "Si moltiplicano per (26 ÷ 24)², cioè per circa 1,17: 200 g di farina diventano circa 235 g."),
            ("Posso scrivere frazioni come 1/2 o ½?", "Sì: all'inizio di ogni riga il calcolatore riconosce numeri interi e decimali (2,5), frazioni (1/2, 1 1/2) e i simboli ½, ¼, ¾. Le righe senza numero, come «sale q.b.», restano uguali."),
        ],
        "en": [
            ("How do I solve a proportion with x?", "Multiply the two numbers diagonally across and divide by the third: in 2 : 5 = 6 : x, x = 5 × 6 ÷ 2 = 15."),
            ("How do quantities change from a 24 cm to a 26 cm pan?", "Multiply them by (26 ÷ 24)², about 1.17: 200 g of flour becomes about 235 g."),
            ("Can I type fractions like 1/2 or ½?", "Yes: at the start of each line the calculator reads whole and decimal numbers (2.5), fractions (1/2, 1 1/2) and the symbols ½, ¼, ¾. Lines without a number, like \"salt to taste\", stay as they are."),
        ],
    },
}

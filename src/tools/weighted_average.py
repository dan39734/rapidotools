TOOL = {
    "id": "weighted_average",
    "cat": "work",
    "icon": "🎓",
    "slug": {"it": "calcolo-media-ponderata-voto-di-laurea", "en": "weighted-average-degree-grade-calculator"},
    "title": {"it": "Calcolo media ponderata e voto di laurea", "en": "Weighted average and degree grade calculator (Italian university)"},
    "short": {"it": "Media ponderata degli esami con i CFU, base in 110esimi e voto di laurea", "en": "Weighted average of your exams with CFU credits, base out of 110 and final degree grade"},
    "keywords": {"it": ["media ponderata", "media universitaria", "voto di laurea", "media esami", "cfu", "110", "media aritmetica"], "en": ["weighted average", "gpa", "degree grade", "italian university", "cfu credits", "110 cum laude"]},
    "meta": {
        "it": "Calcola la media ponderata degli esami universitari (voti × CFU), la media aritmetica, la base di laurea in 110esimi e il voto di laurea con i punti della tesi. Scopri anche che voto ti serve per raggiungere la media che vuoi.",
        "en": "Work out the weighted average of your university exams (marks × CFU credits), the arithmetic average, the base out of 110 and your final degree grade with thesis points. Also find the mark you need to reach your target average.",
    },
    "intro": {
        "it": "Inserisci voto e CFU di ogni esame (o direttamente la tua media): ottieni media ponderata e aritmetica, la base di laurea in 110esimi e il voto finale con i punti aggiuntivi della tesi.",
        "en": "Enter the mark and CFU credits of each exam (or your average directly): get the weighted and arithmetic averages, the base out of 110 and the final grade with thesis points.",
    },
    "strings": {
        "it": {
            "tab_exams": "Inserisco gli esami", "tab_avg": "Conosco già la media", "exam": "Esame", "grade": "Voto", "cfu": "CFU", "lode": "30 e lode", "add": "+ Aggiungi esame", "remove": "Togli",
            "lode_val": "Valore della lode", "avg_in": "Media ponderata", "cfu_in": "CFU sostenuti (facoltativo)",
            "wavg": "Media ponderata", "aavg": "Media aritmetica", "tot": "CFU totali", "n": "Esami inseriti", "base": "Base di laurea (in 110esimi)", "base_round": "arrotondata",
            "bonus": "Punti aggiuntivi (tesi, bonus)", "final": "Voto di laurea previsto", "final_sub": "= base {base} + {bonus} punti, arrotondato",
            "lode_note": "Con 110 la lode viene decisa dalla commissione secondo il regolamento del tuo corso.",
            "goal_title": "Che voto mi serve?", "goal_avg": "Media che voglio raggiungere", "goal_cfu": "CFU ancora da sostenere", "goal_res": "Voto medio necessario nei prossimi esami",
            "goal_ok": "Fattibile: ti basta una media di {v} nei CFU che restano.", "goal_no": "Non raggiungibile: servirebbe una media di {v}, sopra il 30.", "goal_done": "Hai già raggiunto questa media.",
            "empty": "Inserisci almeno un esame con voto e CFU.", "copy_res": "Copia il riepilogo",
            "summary": "Media ponderata {w} · media aritmetica {a} · {cfu} CFU · base di laurea {b}/110 · voto previsto {f}",
        },
        "en": {
            "tab_exams": "Enter my exams", "tab_avg": "I already know my average", "exam": "Exam", "grade": "Mark", "cfu": "CFU", "lode": "30 cum laude", "add": "+ Add exam", "remove": "Remove",
            "lode_val": "Value of cum laude", "avg_in": "Weighted average", "cfu_in": "Credits earned (optional)",
            "wavg": "Weighted average", "aavg": "Arithmetic average", "tot": "Total CFU", "n": "Exams entered", "base": "Degree base (out of 110)", "base_round": "rounded",
            "bonus": "Extra points (thesis, bonus)", "final": "Expected degree grade", "final_sub": "= base {base} + {bonus} points, rounded",
            "lode_note": "At 110, honours (lode) are awarded by the board according to your course rules.",
            "goal_title": "What mark do I need?", "goal_avg": "Average I want to reach", "goal_cfu": "Credits still to take", "goal_res": "Average mark needed in the next exams",
            "goal_ok": "Feasible: you need an average of {v} in the remaining credits.", "goal_no": "Not reachable: you would need an average of {v}, above 30.", "goal_done": "You have already reached this average.",
            "empty": "Enter at least one exam with mark and credits.", "copy_res": "Copy the summary",
            "summary": "Weighted average {w} · arithmetic average {a} · {cfu} CFU · degree base {b}/110 · expected grade {f}",
        },
    },
    "ui": """
<div class="tabs" role="tablist">
  <button type="button" class="on" data-tab="ex">{{tab_exams}}</button>
  <button type="button" data-tab="avg">{{tab_avg}}</button>
</div>
<div id="tab-ex">
  <div class="table-wrap"><table id="exams"><thead><tr><th>{{exam}}</th><th>{{grade}}</th><th>{{lode}}</th><th>{{cfu}}</th><th></th></tr></thead><tbody id="rows"></tbody></table></div>
  <div class="inline" style="margin-top:10px">
    <button class="btn small" type="button" id="add">{{add}}</button>
    <button class="btn small" type="button" id="reset">{{reset}}</button>
    <label class="check" style="margin-left:auto">{{lode_val}} <select id="lodev" style="width:auto"><option value="30">30</option><option value="31">31</option><option value="32">32</option><option value="33">33</option></select></label>
  </div>
</div>
<div id="tab-avg" class="hide">
  <div class="row">
    <div class="field"><label for="avgin">{{avg_in}}</label><input type="number" id="avgin" min="18" max="30" step="0.01" placeholder="es. 26,5"></div>
    <div class="field"><label for="cfuin">{{cfu_in}}</label><input type="number" id="cfuin" min="0" step="1" placeholder="es. 120"></div>
  </div>
</div>
<p class="msg" id="empty">{{empty}}</p>
<div class="result hide" id="out">
  <div class="big" id="main"></div>
  <div class="sub" id="sub"></div>
  <div class="stats">
    <div class="stat"><b id="aavg"></b><span>{{aavg}}</span></div>
    <div class="stat"><b id="tot"></b><span>{{tot}}</span></div>
    <div class="stat"><b id="base"></b><span>{{base}}</span></div>
    <div class="stat"><b id="n"></b><span>{{n}}</span></div>
  </div>
  <div class="row" style="margin-top:14px;align-items:flex-end">
    <div class="field"><label for="bonus">{{bonus}}</label><input type="number" id="bonus" min="0" max="20" step="0.5" value="4"></div>
    <div class="stat" style="flex:2 1 200px"><b id="final" style="font-size:1.6rem"></b><span id="finalsub"></span></div>
  </div>
  <p class="msg hide" id="lodenote">{{lode_note}}</p>
  <p class="btns"><button class="btn small" type="button" data-copy="#summary" data-done="{{copied}}">{{copy_res}}</button><input type="hidden" id="summary"></p>
</div>
<h2 style="font-size:1.1rem;margin-top:22px">{{goal_title}}</h2>
<div class="row">
  <div class="field"><label for="gavg">{{goal_avg}}</label><input type="number" id="gavg" min="18" max="30" step="0.1" placeholder="es. 27"></div>
  <div class="field"><label for="gcfu">{{goal_cfu}}</label><input type="number" id="gcfu" min="1" step="1" placeholder="es. 60"></div>
</div>
<p class="msg" id="goal"></p>
""",
    "js": r"""
var rows = RT.$('#rows'), out = RT.$('#out'), empty = RT.$('#empty'), lodev = RT.$('#lodev'), bonus = RT.$('#bonus');
var mode = 'ex';
function addRow(grade, cfu) {
  var tr = document.createElement('tr');
  var i = rows.children.length + 1;
  tr.innerHTML = '<td class="mono">' + i + '</td>' +
    '<td><input type="number" class="g" min="18" max="30" step="1" style="min-width:70px" value="' + (grade || '') + '" aria-label="' + T.grade + ' ' + i + '"></td>' +
    '<td style="text-align:center"><input type="checkbox" class="l" aria-label="' + T.lode + ' ' + i + '"></td>' +
    '<td><input type="number" class="c" min="1" max="60" step="1" style="min-width:70px" value="' + (cfu || '') + '" aria-label="' + T.cfu + ' ' + i + '"></td>' +
    '<td><button type="button" class="btn small rm" aria-label="' + T.remove + '">✕</button></td>';
  rows.appendChild(tr);
  RT.$$('input', tr).forEach(function (el) { el.addEventListener('input', calc); el.addEventListener('change', calc); });
  RT.$('.rm', tr).addEventListener('click', function () { tr.remove(); renumber(); calc(); });
}
function renumber() { RT.$$('tr', rows).forEach(function (tr, i) { tr.firstChild.textContent = i + 1; }); }
function collect() {
  var lv = +lodev.value, sum = 0, cfu = 0, n = 0, plain = 0;
  RT.$$('tr', rows).forEach(function (tr) {
    var g = RT.num(RT.$('.g', tr).value), c = RT.num(RT.$('.c', tr).value), l = RT.$('.l', tr).checked;
    if (!isFinite(g) || !isFinite(c) || c <= 0 || g < 18 || g > 30) return;
    if (l && g === 30) g = lv;
    sum += g * c; cfu += c; plain += g; n++;
  });
  return { w: cfu ? sum / cfu : NaN, a: n ? plain / n : NaN, cfu: cfu, n: n };
}
function calc() {
  var r;
  if (mode === 'ex') r = collect();
  else { var w = RT.num(RT.$('#avgin').value), c = RT.num(RT.$('#cfuin').value); r = { w: (w >= 18 && w <= 33) ? w : NaN, a: NaN, cfu: isFinite(c) ? c : 0, n: NaN }; }
  if (!isFinite(r.w)) { out.classList.add('hide'); empty.classList.remove('hide'); goal(r); return; }
  empty.classList.add('hide'); out.classList.remove('hide');
  var base = r.w * 110 / 30, b = RT.num(bonus.value) || 0, fin = Math.round(base + b), capped = Math.min(110, fin);
  RT.$('#main').textContent = T.wavg + ': ' + RT.fmtFixed(r.w, 2);
  RT.$('#sub').textContent = RT.fmt(r.w, 3) + ' / 30';
  RT.$('#aavg').textContent = isFinite(r.a) ? RT.fmtFixed(r.a, 2) : '–';
  RT.$('#tot').textContent = RT.fmt(r.cfu, 0);
  RT.$('#base').textContent = RT.fmtFixed(base, 2) + ' (' + T.base_round + ': ' + Math.round(base) + ')';
  RT.$('#n').textContent = isFinite(r.n) ? r.n : '–';
  RT.$('#final').textContent = capped + ' / 110' + (fin > 110 ? ' (' + fin + ')' : '');
  RT.$('#finalsub').textContent = T.final + ' ' + T.final_sub.replace('{base}', RT.fmtFixed(base, 2)).replace('{bonus}', RT.fmt(b, 1));
  RT.$('#lodenote').classList.toggle('hide', capped < 110);
  RT.$('#summary').value = T.summary.replace('{w}', RT.fmtFixed(r.w, 2)).replace('{a}', isFinite(r.a) ? RT.fmtFixed(r.a, 2) : '–').replace('{cfu}', RT.fmt(r.cfu, 0)).replace('{b}', RT.fmtFixed(base, 2)).replace('{f}', capped);
  goal(r);
}
function goal(r) {
  var g = RT.num(RT.$('#gavg').value), c = RT.num(RT.$('#gcfu').value), el = RT.$('#goal');
  el.className = 'msg';
  if (!isFinite(g) || !isFinite(c) || c <= 0 || !isFinite(r.w) || !(r.cfu > 0)) { el.textContent = ''; return; }
  var need = (g * (r.cfu + c) - r.w * r.cfu) / c;
  if (need <= r.w && g <= r.w) { el.textContent = T.goal_done; el.className = 'msg ok'; return; }
  if (need > 30) { el.textContent = T.goal_no.replace('{v}', RT.fmtFixed(need, 2)); el.className = 'msg bad'; return; }
  el.textContent = T.goal_ok.replace('{v}', RT.fmtFixed(Math.max(need, 18), 2)); el.className = 'msg ok';
}
RT.$$('.tabs button').forEach(function (b) {
  b.addEventListener('click', function () {
    RT.$$('.tabs button').forEach(function (x) { x.classList.toggle('on', x === b); });
    mode = b.getAttribute('data-tab');
    RT.$('#tab-ex').classList.toggle('hide', mode !== 'ex'); RT.$('#tab-avg').classList.toggle('hide', mode !== 'avg');
    calc();
  });
});
RT.$('#add').addEventListener('click', function () { addRow(); RT.$('.g', rows.lastChild).focus(); });
RT.$('#reset').addEventListener('click', function () { rows.innerHTML = ''; for (var i = 0; i < 6; i++) addRow(); calc(); });
[[28, 12], [24, 6], [30, 9]].forEach(function (e) { addRow(e[0], e[1]); }); for (var i = 0; i < 3; i++) addRow();
['#lodev', '#bonus', '#avgin', '#cfuin', '#gavg', '#gcfu'].forEach(function (s) { var el = RT.$(s); el.addEventListener('input', calc); el.addEventListener('change', calc); });
calc();
""",
    "article": {
        "it": """
<h2>Come si calcola la media ponderata</h2>
<p>La media ponderata «pesa» ogni voto per i crediti dell'esame: si moltiplica ogni voto per i suoi CFU, si sommano i prodotti e si divide per il totale dei CFU. Un esame da 12 CFU conta il doppio di uno da 6. È la media che quasi tutte le università usano per il voto di laurea; la <strong>media aritmetica</strong> (somma dei voti diviso il numero degli esami) è mostrata per confronto.</p>
<p><em>Esempio:</em> 28 (12 CFU), 24 (6 CFU), 30 (9 CFU) → (28×12 + 24×6 + 30×9) ÷ 27 = 750 ÷ 27 = <strong>27,78</strong>.</p>
<h2>Dalla media al voto di laurea</h2>
<p>La base di laurea si ottiene riportando la media in centodecimi: <strong>media × 110 ÷ 30</strong>. Con 27,78 di media la base è 101,85. A questa la commissione aggiunge i punti della tesi (di solito da 0 a 7 per le triennali, fino a 10–11 per le magistrali) e gli eventuali bonus (laurea in corso, Erasmus, lodi): il totale si arrotonda all'intero più vicino e non può superare 110. La lode si assegna con voto pieno secondo il regolamento del corso: alcuni atenei la propongono da 112 o 113 punti «virtuali».</p>
<h2>Le lodi e le regole del tuo ateneo</h2>
<ul>
<li>Nella maggior parte delle università la lode vale <strong>30</strong> nella media; in alcune vale 31, 32 o 33: scegli il valore nel menu.</li>
<li>Alcuni corsi escludono dalla media i voti più bassi o gli esami a scelta, oppure calcolano i punti tesi in modo diverso: il regolamento didattico del tuo corso ha la parola finale. Questo calcolatore usa la formula standard.</li>
<li>Se conosci già la media dal portale studenti, usa la scheda «Conosco già la media» per calcolare solo la base e il voto finale.</li>
</ul>
<h2>Che voto mi serve?</h2>
<p>Nella sezione in fondo inserisci la media che vuoi raggiungere e i CFU che devi ancora sostenere: il calcolatore ti dice il voto medio che ti serve nei prossimi esami. Se il risultato supera 30, l'obiettivo non è raggiungibile con i crediti che restano.</p>
""",
        "en": """
<h2>How the weighted average is calculated</h2>
<p>Italian universities grade exams out of 30 and weight each mark by the exam's credits (CFU): multiply each mark by its credits, add up the products and divide by the total credits. A 12-credit exam counts twice as much as a 6-credit one. This is the average almost every university uses for the degree grade; the <strong>arithmetic average</strong> (sum of the marks divided by the number of exams) is shown for comparison.</p>
<p><em>Example:</em> 28 (12 CFU), 24 (6 CFU), 30 (9 CFU) → (28×12 + 24×6 + 30×9) ÷ 27 = 750 ÷ 27 = <strong>27.78</strong>.</p>
<h2>From the average to the degree grade</h2>
<p>The degree base converts the average to a scale of 110: <strong>average × 110 ÷ 30</strong>. With an average of 27.78 the base is 101.85. The board then adds thesis points (usually 0–7 for bachelor's degrees, up to 10–11 for master's) and any bonus (graduating on time, Erasmus, honours): the total is rounded to the nearest whole number and cannot exceed 110. "110 e lode" (cum laude) is awarded at the board's discretion according to the course rules.</p>
<h2>Honours and your university's rules</h2>
<ul>
<li>In most universities "30 e lode" counts as <strong>30</strong> in the average; in some it counts 31, 32 or 33: pick the value from the menu.</li>
<li>Some courses exclude the lowest marks or elective exams, or compute thesis points differently: your course regulations have the final say. This calculator uses the standard formula.</li>
<li>If you already know your average from the student portal, use the "I already know my average" tab to compute only the base and the final grade.</li>
</ul>
<h2>What mark do I need?</h2>
<p>In the section at the bottom, enter the average you want and the credits you still have to take: the calculator tells you the average mark you need in your next exams. If the result is above 30, the target is out of reach with the remaining credits.</p>
""",
    },
    "faq": {
        "it": [
            ("Che differenza c'è tra media ponderata e media aritmetica?", "La ponderata tiene conto dei CFU di ogni esame, l'aritmetica no. Per il voto di laurea conta quasi sempre la ponderata."),
            ("Come si passa dalla media in trentesimi ai centodecimi?", "Si moltiplica per 110 e si divide per 30: una media di 27 corrisponde a 99 su 110."),
            ("Il calcolatore salva i miei esami?", "No: i dati restano nella pagina e spariscono quando la chiudi. Puoi copiare il riepilogo con il pulsante."),
        ],
        "en": [
            ("What is the difference between weighted and arithmetic average?", "The weighted average takes each exam's credits into account, the arithmetic one doesn't. The degree grade almost always uses the weighted one."),
            ("How do you convert an average out of 30 to a grade out of 110?", "Multiply by 110 and divide by 30: an average of 27 corresponds to 99 out of 110."),
            ("Does the calculator save my exams?", "No: the data stays on the page and disappears when you close it. You can copy the summary with the button."),
        ],
    },
}

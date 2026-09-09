from tools._colf import JS_COMMON, UI_PAY, STR_PAY, CCNL_NOTE

_S_IT = dict(STR_PAY["it"])
_S_IT.update({
    "start": "Data di assunzione", "end": "Data di cessazione (o di oggi)", "infl": "Inflazione media annua per la rivalutazione (%)", "infl_hint": "Coefficiente = 1,5 % fisso + 75 % dell'inflazione (con 0 resta solo l'1,5 %)",
    "annual": "Retribuzione annua utile (13 mensilità)", "quota": "Quota TFR per anno intero (÷ 13,5)", "years": "Anzianità maturata", "reval": "Rivalutazione stimata",
    "result": "TFR lordo maturato", "y": "anni", "m": "mesi", "year": "Anno", "months_col": "Mesi", "quota_col": "Quota", "reval_col": "Rivalutazione", "fund": "Totale a fine anno",
    "invalid": "Inserisci la retribuzione e un periodo valido (la cessazione deve venire dopo l'assunzione).",
})
_S_EN = dict(STR_PAY["en"])
_S_EN.update({
    "start": "Hiring date", "end": "End date (or today)", "infl": "Average annual inflation for revaluation (%)", "infl_hint": "Coefficient = 1.5% fixed + 75% of inflation (with 0 only the 1.5% applies)",
    "annual": "Annual pay counted (13 months)", "quota": "TFR for a full year (÷ 13.5)", "years": "Seniority accrued", "reval": "Estimated revaluation",
    "result": "Gross TFR accrued", "y": "years", "m": "months", "year": "Year", "months_col": "Months", "quota_col": "Quota", "reval_col": "Revaluation", "fund": "Total at year end",
    "invalid": "Enter the pay and a valid period (the end date must come after the hiring date).",
})

TOOL = {
    "id": "colf_tfr",
    "cat": "work",
    "icon": "💼",
    "slug": {"it": "calcolo-tfr-colf-badante", "en": "tfr-severance-domestic-worker-italy"},
    "title": {"it": "Calcolo TFR colf e badante", "en": "TFR (severance pay) for domestic workers in Italy (colf, badante)"},
    "short": {"it": "Trattamento di fine rapporto di colf, badanti e baby sitter, anno per anno", "en": "End-of-employment pay (TFR) for housekeepers and carers, year by year"},
    "keywords": {"it": ["tfr colf", "tfr badante", "liquidazione colf", "trattamento di fine rapporto", "lavoro domestico", "calcolo tfr"], "en": ["tfr", "severance pay", "domestic worker", "colf", "badante", "end of employment italy"]},
    "meta": {
        "it": "Calcola il TFR (liquidazione) di colf, badanti e baby sitter: retribuzione annua diviso 13,5 per ogni anno, quote per i mesi maturati con la regola dei 15 giorni, rivalutazione annuale stimata e tabella anno per anno. Gratis, secondo il CCNL lavoro domestico.",
        "en": "Work out the TFR (severance pay) of a domestic worker in Italy: annual pay divided by 13.5 for each year, pro rata for the months accrued (15-day rule), estimated yearly revaluation and a year-by-year table. Free, under the national contract.",
    },
    "intro": {
        "it": "Inserisci la paga (a ore o mensile) e le date di assunzione e cessazione: ottieni il TFR lordo maturato, con la quota di ogni anno e la rivalutazione stimata.",
        "en": "Enter the pay (hourly or monthly) and the hiring and end dates: you get the gross TFR accrued, with each year's quota and the estimated revaluation.",
    },
    "strings": {"it": _S_IT, "en": _S_EN},
    "ui": UI_PAY + """
<div class="row">
  <div class="field"><label for="start">{{start}}</label><input type="date" id="start"></div>
  <div class="field"><label for="end">{{end}}</label><input type="date" id="end"></div>
  <div class="field"><label for="infl">{{infl}}</label><input type="number" id="infl" min="0" max="20" step="0.1" value="0"><span class="msg" style="margin:0">{{infl_hint}}</span></div>
</div>
<p class="msg">{{rule}}</p>
<p class="msg bad hide" id="err">{{invalid}}</p>
<div class="result hide" id="out">
  <div class="big" id="main"></div>
  <div class="sub" id="sub"></div>
  <div class="stats">
    <div class="stat"><b id="annual"></b><span>{{annual}}</span></div>
    <div class="stat"><b id="quota"></b><span>{{quota}}</span></div>
    <div class="stat"><b id="years"></b><span>{{years}}</span></div>
    <div class="stat"><b id="reval"></b><span>{{reval}}</span></div>
  </div>
  <div class="table-wrap" style="margin-top:14px"><table><thead><tr><th>{{year}}</th><th>{{months_col}}</th><th>{{quota_col}}</th><th>{{reval_col}}</th><th>{{fund}}</th></tr></thead><tbody id="rows"></tbody></table></div>
</div>
""",
    "js": JS_COMMON + r"""
setDefaultDates('#start', '#end', 2);
var out = RT.$('#out'), err = RT.$('#err'), rows = RT.$('#rows');
function calc() {
  var mp = monthlyPay(), a = RT.parseDate(RT.$('#start').value), b = RT.parseDate(RT.$('#end').value);
  var infl = RT.num(RT.$('#infl').value) || 0;
  if (!isFinite(mp) || !a || !b || b < a) { out.classList.add('hide'); err.classList.remove('hide'); return; }
  err.classList.add('hide'); out.classList.remove('hide');
  var annual = mp * 13, quota = annual / 13.5, coef = 0.015 + 0.75 * infl / 100;
  var fund = 0, totalMonths = 0, totalReval = 0, html = '';
  for (var y = a.getFullYear(); y <= b.getFullYear(); y++) {
    var ys = new Date(y, 0, 1), ye = new Date(y, 11, 31);
    var s = a > ys ? a : ys, e = b < ye ? b : ye;
    var n = monthsWorked(s, e); if (n > 12) n = 12;
    var rev = (y > a.getFullYear()) ? fund * coef : 0; // revaluation of the fund accrued up to the previous year
    var q = quota * n / 12;
    fund += rev + q; totalMonths += n; totalReval += rev;
    html += '<tr><td>' + y + '</td><td>' + n + '</td><td>' + RT.money(q, 'EUR') + '</td><td>' + RT.money(rev, 'EUR') + '</td><td>' + RT.money(fund, 'EUR') + '</td></tr>';
  }
  rows.innerHTML = html;
  RT.$('#main').textContent = T.result + ': ' + RT.money(fund, 'EUR');
  RT.$('#sub').textContent = RT.money(annual, 'EUR') + ' ÷ 13,5 × ' + totalMonths + '/12';
  RT.$('#annual').textContent = RT.money(annual, 'EUR');
  RT.$('#quota').textContent = RT.money(quota, 'EUR');
  RT.$('#years').textContent = Math.floor(totalMonths / 12) + ' ' + T.y + ', ' + (totalMonths % 12) + ' ' + T.m;
  RT.$('#reval').textContent = RT.money(totalReval, 'EUR');
}
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>Come si calcola il TFR di colf e badanti</h2>
<p>Il trattamento di fine rapporto (la «liquidazione») spetta a ogni lavoratrice domestica alla fine del rapporto, qualunque sia il motivo. Per ogni anno di lavoro si accantona la <strong>retribuzione annua utile divisa per 13,5</strong>; per le frazioni di anno la quota è proporzionale ai mesi, contando come intero il mese in cui il rapporto è durato almeno 15 giorni. Nella retribuzione utile entrano la paga base, la tredicesima e, per le conviventi, l'indennità di vitto e alloggio; il calcolatore usa quindi <strong>13 mensilità</strong> della retribuzione mensile di riferimento (per chi è a ore: paga oraria × ore settimanali × 52 ÷ 12).</p>
<p><em>Esempio:</em> 9 € l'ora per 20 ore a settimana → 780 € al mese → 10.140 € l'anno → quota TFR di <strong>751,11 €</strong> per ogni anno intero, 62,59 € al mese.</p>
<h2>La rivalutazione</h2>
<p>Ogni 31 dicembre il TFR accantonato fino all'anno precedente si rivaluta con un coefficiente pari all'<strong>1,5% fisso più il 75% dell'aumento dell'inflazione</strong> (indice ISTAT FOI). Il coefficiente esatto lo pubblica l'ISTAT ogni anno; il calcolatore lo stima dall'inflazione media annua che inserisci (con 0 resta solo la parte fissa dell'1,5%; negli ultimi anni l'inflazione italiana è oscillata tra l'1% e l'8%). Sulla rivalutazione si applica un'imposta sostitutiva del 17%, mentre il TFR è soggetto a tassazione separata: l'importo mostrato è <strong>lordo</strong>.</p>
<h2>Quando e come si paga</h2>
<ul>
<li>Il TFR si paga con l'ultima busta paga, insieme alla tredicesima maturata e alle ferie non godute.</li>
<li>Il datore può, se la lavoratrice è d'accordo, anticipare il TFR maturato una volta l'anno (non oltre il 70%) o pagarlo ogni anno: in questo caso ogni anno riparte da zero e non c'è rivalutazione.</li>
<li>Se cambiano ore o paga durante il rapporto, il calcolo va fatto per periodi e poi sommato; questo strumento assume una retribuzione costante.</li>
</ul>
""" + CCNL_NOTE["it"],
        "en": """
<h2>How the TFR is calculated for domestic workers</h2>
<p>The TFR (<em>trattamento di fine rapporto</em>, severance pay) is due to every domestic worker in Italy at the end of employment, whatever the reason. For each year of work the employer sets aside the <strong>annual pay divided by 13.5</strong>; for fractions of a year the quota is pro rata to the months, counting as a whole month any month in which the employment lasted at least 15 days. The pay counted includes the base pay, the 13th month and, for live-in workers, the board and lodging allowance; the calculator therefore uses <strong>13 months</strong> of the reference monthly pay (for hourly workers: hourly rate × weekly hours × 52 ÷ 12).</p>
<p><em>Example:</em> €9 per hour for 20 hours a week → €780 a month → €10,140 a year → TFR quota of <strong>€751.11</strong> for each full year, €62.59 per month.</p>
<h2>Revaluation</h2>
<p>Every 31 December the TFR set aside up to the previous year is revalued with a coefficient equal to <strong>1.5% fixed plus 75% of inflation</strong> (ISTAT FOI index). The exact coefficient is published by ISTAT every year; the calculator estimates it from the average annual inflation you enter (with 0 only the fixed 1.5% applies; in recent years Italian inflation has ranged between 1% and 8%). Revaluation is taxed at 17%, while the TFR itself is subject to separate taxation: the amount shown is <strong>gross</strong>.</p>
<h2>When and how it is paid</h2>
<ul>
<li>The TFR is paid with the final payslip, together with the accrued 13th month and the untaken holidays.</li>
<li>With the worker's agreement the employer may advance the accrued TFR once a year (up to 70%) or pay it every year: in that case each year starts from zero and there is no revaluation.</li>
<li>If hours or pay change during the employment, the calculation must be done by periods and added up; this tool assumes a constant pay.</li>
</ul>
""" + CCNL_NOTE["en"],
    },
    "faq": {
        "it": [
            ("Quanto TFR matura una colf in un anno?", "La retribuzione annua (13 mensilità, indennità di vitto e alloggio compresa per le conviventi) divisa per 13,5: circa il 7,4% di quanto guadagna in un anno."),
            ("Il TFR spetta anche se la colf si licenzia?", "Sì, il TFR spetta sempre alla fine del rapporto, sia per dimissioni sia per licenziamento, in proporzione al periodo lavorato."),
            ("Posso pagare il TFR ogni anno invece che alla fine?", "Sì, se la lavoratrice è d'accordo: il CCNL consente di liquidarlo annualmente o di anticiparne fino al 70%. Va scritto nella busta paga."),
        ],
        "en": [
            ("How much TFR does a domestic worker accrue in a year?", "The annual pay (13 months, board and lodging allowance included for live-in workers) divided by 13.5: about 7.4% of what she earns in a year."),
            ("Is the TFR due if the worker resigns?", "Yes, the TFR is always due at the end of employment, whether the worker resigns or is dismissed, pro rata to the period worked."),
            ("Can I pay the TFR every year instead of at the end?", "Yes, with the worker's agreement: the contract allows paying it yearly or advancing up to 70% of it. It must be recorded on the payslip."),
        ],
    },
}

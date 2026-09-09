from tools._colf import JS_COMMON, STR_PAY, CCNL_NOTE

_S_IT = dict(STR_PAY["it"])
_S_IT.update({
    "type_h": "A ore (ferie calcolate in ore)", "type_m": "A giornate (convivente o tempo pieno)",
    "wdays": "Giorni di lavoro a settimana", "taken": "Ferie già godute nel periodo", "unit_h": "ore", "unit_d": "giorni",
    "year_ent": "Ferie in un anno intero", "accrued": "Ferie maturate nel periodo", "left": "Ferie residue", "value": "Valore delle ferie residue (lordo)",
    "per_month": "al mese", "invalid": "Inserisci le ore settimanali (o i giorni), la paga e un periodo valido.",
    "left_sub": "{acc} maturate − {tk} godute",
})
_S_EN = dict(STR_PAY["en"])
_S_EN.update({
    "type_h": "Hourly (holidays counted in hours)", "type_m": "By days (live-in or full time)",
    "wdays": "Working days per week", "taken": "Holidays already taken in the period", "unit_h": "hours", "unit_d": "days",
    "year_ent": "Holidays in a full year", "accrued": "Holidays accrued in the period", "left": "Holidays left", "value": "Value of the holidays left (gross)",
    "per_month": "per month", "invalid": "Enter the weekly hours (or days), the pay and a valid period.",
    "left_sub": "{acc} accrued − {tk} taken",
})

TOOL = {
    "id": "colf_ferie",
    "cat": "work",
    "icon": "🌴",
    "slug": {"it": "calcolo-ferie-colf-badante", "en": "holiday-entitlement-domestic-worker-italy"},
    "title": {"it": "Calcolo ferie colf e badante", "en": "Holiday entitlement for domestic workers in Italy (colf, badante)"},
    "short": {"it": "Ferie maturate in ore o giorni, residuo e valore da liquidare", "en": "Holidays accrued in hours or days, balance and pay-out value"},
    "keywords": {"it": ["ferie colf", "ferie badante", "ferie colf a ore", "26 giorni", "ferie maturate", "lavoro domestico", "calcolo ferie"], "en": ["holiday entitlement", "domestic worker", "colf", "badante", "annual leave italy"]},
    "meta": {
        "it": "Calcola le ferie di colf, badanti e baby sitter secondo il CCNL lavoro domestico: 26 giorni l'anno, maturazione mensile con la regola dei 15 giorni, conversione in ore per chi lavora a ore, ferie residue e valore da pagare a fine rapporto.",
        "en": "Work out the holidays of a domestic worker in Italy under the national contract: 26 days a year, monthly accrual with the 15-day rule, conversion into hours for hourly workers, balance and pay-out value at the end of employment.",
    },
    "intro": {
        "it": "Inserisci ore o giorni di lavoro a settimana, la paga e il periodo: ottieni le ferie maturate (in ore o in giorni), quelle residue e quanto valgono se vanno pagate a fine rapporto.",
        "en": "Enter the weekly hours or days, the pay and the period: you get the holidays accrued (in hours or days), the balance and their value if they must be paid out at the end of employment.",
    },
    "strings": {"it": _S_IT, "en": _S_EN},
    "ui": """
<div class="row">
  <div class="field"><label for="type">{{type}}</label><select id="type"><option value="h">{{type_h}}</option><option value="m">{{type_m}}</option></select></div>
  <div class="field only-h"><label for="hours">{{hours}}</label><input type="number" id="hours" min="1" max="60" step="0.5" value="20"></div>
  <div class="field only-h"><label for="rate">{{rate}}</label><input type="number" id="rate" min="0" step="0.01" value="9"></div>
  <div class="field only-m hide"><label for="wdays">{{wdays}}</label><select id="wdays"><option>6</option><option>5</option><option>4</option><option>3</option><option>2</option><option>1</option></select></div>
  <div class="field only-m hide"><label for="monthly">{{monthly}}</label><input type="number" id="monthly" min="0" step="0.01" placeholder="es. 1200"></div>
</div>
<div class="row">
  <div class="field"><label for="start">{{start}}</label><input type="date" id="start"></div>
  <div class="field"><label for="end">{{end}}</label><input type="date" id="end"></div>
  <div class="field"><label for="taken">{{taken}} (<span id="unit1"></span>)</label><input type="number" id="taken" min="0" step="0.5" value="0"></div>
</div>
<p class="msg">{{rule}}</p>
<p class="msg bad hide" id="err">{{invalid}}</p>
<div class="result hide" id="out">
  <div class="big" id="main"></div>
  <div class="sub" id="sub"></div>
  <div class="stats">
    <div class="stat"><b id="year"></b><span>{{year_ent}}</span></div>
    <div class="stat"><b id="acc"></b><span>{{accrued}}</span></div>
    <div class="stat"><b id="mon"></b><span>{{months}}</span></div>
    <div class="stat"><b id="val"></b><span>{{value}}</span></div>
  </div>
</div>
""",
    "js": JS_COMMON + r"""
setDefaultDates('#start', '#end', 0);
var out = RT.$('#out'), err = RT.$('#err');
function calc() {
  var hourly = RT.$('#type').value === 'h', unit = hourly ? T.unit_h : T.unit_d;
  RT.$('#unit1').textContent = unit;
  var a = RT.parseDate(RT.$('#start').value), b = RT.parseDate(RT.$('#end').value), n = monthsWorked(a, b);
  var perYear, valueEach;
  if (hourly) { var h = RT.num(RT.$('#hours').value), r = RT.num(RT.$('#rate').value); perYear = h * 26 / 6; valueEach = r; if (!(h > 0)) perYear = NaN; }
  else { var wd = +RT.$('#wdays').value, m = RT.num(RT.$('#monthly').value); perYear = 26 * wd / 6; valueEach = m > 0 ? m / 26 * 6 / wd : NaN; }
  if (!isFinite(perYear) || !n) { out.classList.add('hide'); err.classList.remove('hide'); return; }
  err.classList.add('hide'); out.classList.remove('hide');
  var acc = perYear / 12 * n, tk = RT.num(RT.$('#taken').value) || 0, left = acc - tk;
  RT.$('#main').textContent = T.left + ': ' + RT.fmt(left, 2) + ' ' + unit;
  RT.$('#sub').textContent = T.left_sub.replace('{acc}', RT.fmt(acc, 2) + ' ' + unit).replace('{tk}', RT.fmt(tk, 2) + ' ' + unit);
  RT.$('#year').textContent = RT.fmt(perYear, 2) + ' ' + unit + ' (' + RT.fmt(perYear / 12, 2) + ' ' + T.per_month + ')';
  RT.$('#acc').textContent = RT.fmt(acc, 2) + ' ' + unit;
  RT.$('#mon').textContent = n;
  RT.$('#val').textContent = isFinite(valueEach) ? RT.money(Math.max(left, 0) * valueEach, 'EUR') : '–';
}
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>Quante ferie spettano a colf e badanti</h2>
<p>Il CCNL del lavoro domestico riconosce <strong>26 giorni lavorativi di ferie all'anno</strong>, calcolati su una settimana di sei giorni (dal lunedì al sabato): corrispondono a un mese di calendario. Le ferie maturano <strong>in dodicesimi</strong>, cioè 26 ÷ 12 = 2,17 giorni per ogni mese di lavoro; un mese conta se il rapporto è durato almeno 15 giorni. Vanno godute, di regola tra giugno e settembre e in non più di due periodi, e <strong>non possono essere pagate</strong> al posto del riposo finché il rapporto è in corso: si liquidano in denaro solo quelle non godute alla cessazione.</p>
<h3>Chi lavora a ore: ferie in ore</h3>
<p>Per part-time e lavoratrici a ore le ferie si esprimono in ore: <strong>ore settimanali × 26 ÷ 6</strong> (cioè ore settimanali × 4,33) in un anno intero. Con 20 ore a settimana spettano 86,67 ore l'anno, 7,22 al mese; con 6 ore a settimana, 26 ore l'anno. Ogni ora di ferie si paga con la paga oraria normale.</p>
<h3>Chi lavora a giornate</h3>
<p>Con la settimana di sei giorni spettano 26 giorni; con meno giorni a settimana i giorni di ferie sono in proporzione (5 giorni → 21,67; 3 giorni → 13). Per le conviventi ogni giorno di ferie vale 1/26 della retribuzione mensile, indennità di vitto e alloggio compresa, che spetta anche durante le ferie.</p>
<h2>Come usare il calcolatore</h2>
<ul>
<li><strong>Ferie maturate finora:</strong> periodo dal 1° gennaio (o dall'assunzione) a oggi.</li>
<li><strong>Ferie residue:</strong> inserisci quelle già godute nello stesso periodo.</li>
<li><strong>Liquidazione a fine rapporto:</strong> periodo fino all'ultimo giorno di lavoro; il valore delle ferie residue va nell'ultima busta paga insieme a tredicesima e TFR.</li>
</ul>
""" + CCNL_NOTE["it"],
        "en": """
<h2>How many holidays domestic workers get</h2>
<p>The Italian contract for domestic work grants <strong>26 working days of paid holiday a year</strong>, calculated on a six-day week (Monday to Saturday): the equivalent of one calendar month. Holidays accrue <strong>in twelfths</strong>, i.e. 26 ÷ 12 = 2.17 days for each month of work; a month counts if the employment lasted at least 15 days. They must be taken, normally between June and September and in no more than two periods, and <strong>cannot be paid in lieu</strong> while the employment lasts: only the days not taken at the end of employment are paid out.</p>
<h3>Hourly workers: holidays in hours</h3>
<p>For part-time and hourly workers holidays are expressed in hours: <strong>weekly hours × 26 ÷ 6</strong> (i.e. weekly hours × 4.33) in a full year. With 20 hours a week that is 86.67 hours a year, 7.22 a month; with 6 hours a week, 26 hours a year. Each hour of holiday is paid at the normal hourly rate.</p>
<h3>Workers paid by the day or month</h3>
<p>With a six-day week the entitlement is 26 days; with fewer days a week it is proportional (5 days → 21.67; 3 days → 13). For live-in workers each day of holiday is worth 1/26 of the monthly pay, board and lodging allowance included, which is also due during holidays.</p>
<h2>How to use the calculator</h2>
<ul>
<li><strong>Holidays accrued so far:</strong> period from 1 January (or from hiring) to today.</li>
<li><strong>Balance:</strong> enter the holidays already taken in the same period.</li>
<li><strong>Final settlement:</strong> period up to the last day of work; the value of the holidays left goes on the final payslip together with the 13th month and the TFR.</li>
</ul>
""" + CCNL_NOTE["en"],
    },
    "faq": {
        "it": [
            ("Quanti giorni di ferie matura una colf in un mese?", "2,17 giorni (26 ÷ 12) su una settimana di sei giorni; per chi lavora a ore, ore settimanali × 26 ÷ 6 ÷ 12 ore al mese."),
            ("Le ferie non godute si possono pagare?", "Solo alla fine del rapporto di lavoro. Durante il rapporto vanno godute: il contratto vieta di sostituirle con denaro."),
            ("Durante le ferie la badante convivente ha diritto a vitto e alloggio?", "Sì: la retribuzione delle ferie comprende anche l'indennità sostitutiva di vitto e alloggio, se la lavoratrice non li usufruisce."),
        ],
        "en": [
            ("How many holiday days does a domestic worker accrue in a month?", "2.17 days (26 ÷ 12) on a six-day week; for hourly workers, weekly hours × 26 ÷ 6 ÷ 12 hours per month."),
            ("Can untaken holidays be paid instead?", "Only at the end of the employment. During the employment they must be taken: the contract forbids replacing them with money."),
            ("Is a live-in carer entitled to board and lodging during holidays?", "Yes: holiday pay also includes the board and lodging allowance if the worker doesn't use them."),
        ],
    },
}

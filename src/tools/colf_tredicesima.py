from tools._colf import JS_COMMON, UI_PAY, STR_PAY, CCNL_NOTE

_S_IT = dict(STR_PAY["it"])
_S_IT.update({
    "accrual": "Rateo mensile (1/12)", "result": "Tredicesima lorda", "of": "su 12 mesi", "months_sub": "{n} mesi maturati × {r} al mese",
    "invalid": "Inserisci la paga e le ore (o la retribuzione mensile) e un periodo valido.",
})
_S_EN = dict(STR_PAY["en"])
_S_EN.update({
    "accrual": "Monthly accrual (1/12)", "result": "Gross 13th-month pay", "of": "out of 12 months", "months_sub": "{n} months accrued × {r} per month",
    "invalid": "Enter the rate and hours (or the monthly pay) and a valid period.",
})

TOOL = {
    "id": "colf_tredicesima",
    "cat": "work",
    "icon": "🎁",
    "slug": {"it": "calcolo-tredicesima-colf-badante", "en": "13th-month-pay-domestic-worker-italy"},
    "title": {"it": "Calcolo tredicesima colf e badante", "en": "13th-month pay for domestic workers in Italy (colf, badante)"},
    "short": {"it": "Tredicesima di colf, badanti e baby sitter, a ore o mensili, anche per pochi mesi", "en": "Christmas bonus (tredicesima) for housekeepers and carers, hourly or monthly, even for a few months"},
    "keywords": {"it": ["tredicesima colf", "tredicesima badante", "tredicesima colf a ore", "tredicesima baby sitter", "lavoro domestico", "calcolo tredicesima"], "en": ["tredicesima", "13th month", "domestic worker", "colf", "badante", "italy"]},
    "meta": {
        "it": "Calcola la tredicesima di colf, badanti e baby sitter secondo il CCNL lavoro domestico: a ore o mensile, con i mesi maturati nell'anno (regola dei 15 giorni), l'indennità di vitto e alloggio e il rateo mensile. Gratis, con esempi.",
        "en": "Work out the 13th-month pay of a domestic worker in Italy (colf, badante, babysitter) under the national contract: hourly or monthly, with the months accrued in the year (15-day rule) and the monthly accrual. Free, with examples.",
    },
    "intro": {
        "it": "Inserisci paga oraria e ore settimanali (oppure la retribuzione mensile) e il periodo lavorato nell'anno: ottieni la tredicesima lorda da pagare entro dicembre, calcolata come dice il contratto.",
        "en": "Enter the hourly rate and weekly hours (or the monthly pay) and the period worked in the year: you get the gross 13th-month pay due by December, calculated as the contract says.",
    },
    "strings": {"it": _S_IT, "en": _S_EN},
    "ui": UI_PAY + """
<div class="row">
  <div class="field"><label for="start">{{start}}</label><input type="date" id="start"></div>
  <div class="field"><label for="end">{{end}}</label><input type="date" id="end"></div>
</div>
<p class="msg">{{rule}}</p>
<p class="msg bad hide" id="err">{{invalid}}</p>
<div class="result hide" id="out">
  <div class="big" id="main"></div>
  <div class="sub" id="sub"></div>
  <div class="stats">
    <div class="stat"><b id="mp"></b><span>{{month_pay}}</span></div>
    <div class="stat"><b id="acc"></b><span>{{accrual}}</span></div>
    <div class="stat"><b id="mon"></b><span>{{months}}</span></div>
  </div>
</div>
""",
    "js": JS_COMMON + r"""
setDefaultDates('#start', '#end', 0);
var out = RT.$('#out'), err = RT.$('#err');
function calc() {
  var mp = monthlyPay(), a = RT.parseDate(RT.$('#start').value), b = RT.parseDate(RT.$('#end').value);
  var n = monthsWorked(a, b);
  if (!isFinite(mp) || !n) { out.classList.add('hide'); err.classList.remove('hide'); return; }
  err.classList.add('hide'); out.classList.remove('hide');
  var acc = mp / 12, tot = acc * Math.min(n, 12);
  RT.$('#main').textContent = T.result + ': ' + RT.money(tot, 'EUR');
  RT.$('#sub').textContent = T.months_sub.replace('{n}', Math.min(n, 12)).replace('{r}', RT.money(acc, 'EUR'));
  RT.$('#mp').textContent = RT.money(mp, 'EUR');
  RT.$('#acc').textContent = RT.money(acc, 'EUR');
  RT.$('#mon').textContent = Math.min(n, 12) + ' ' + T.of;
}
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>Come si calcola la tredicesima di colf e badanti</h2>
<p>La tredicesima è una mensilità in più, pari alla <strong>retribuzione globale di fatto</strong> di un mese, che matura in dodicesimi: ogni mese di lavoro dà diritto a 1/12. Si paga <strong>entro il mese di dicembre</strong> (di solito con la paga di dicembre o prima di Natale) e, se il rapporto finisce durante l'anno, si liquida in proporzione ai mesi maturati insieme all'ultima busta paga. Un mese conta come maturato se il rapporto è durato <strong>almeno 15 giorni</strong> in quel mese.</p>
<h3>Colf o badante a ore (non convivente)</h3>
<p>Per chi è pagato a ore si parte dalla retribuzione media mensile: <strong>paga oraria × ore settimanali × 52 ÷ 12</strong>. Il rateo mensile è un dodicesimo di questa cifra.</p>
<p><em>Esempio:</em> 9 € l'ora per 20 ore a settimana → 9 × 20 × 52 ÷ 12 = 780 € al mese → rateo 65 € → tredicesima di <strong>780 €</strong> per un anno intero, di 325 € se il rapporto è iniziato ad agosto (5 mesi).</p>
<h3>Colf o badante convivente (mensile)</h3>
<p>Si usa la retribuzione mensile lorda <strong>più l'indennità sostitutiva di vitto e alloggio</strong>, che fa parte della retribuzione globale di fatto e quindi entra anche nella tredicesima; il valore giornaliero dell'indennità è fissato ogni anno dalle tabelle del CCNL. Chi non è convivente non ha l'indennità.</p>
<h2>Cose da sapere</h2>
<ul>
<li>La tredicesima matura anche durante ferie, malattia e infortunio; durante la maternità matura solo per la quota a carico del datore (20%).</li>
<li>Se l'orario è cambiato durante l'anno, il calcolo va fatto per ogni periodo con le sue ore e poi sommato.</li>
<li>Sulla tredicesima si pagano i <strong>contributi INPS</strong> come sulle altre retribuzioni: la quota a carico della lavoratrice viene trattenuta e i contributi si versano con il trimestre di dicembre.</li>
<li>Il datore di lavoro domestico non è sostituto d'imposta: la tredicesima si paga lorda e la lavoratrice la dichiara con il resto del reddito.</li>
</ul>
""" + CCNL_NOTE["it"],
        "en": """
<h2>How the 13th-month pay is calculated for domestic workers</h2>
<p>In Italy every domestic worker – housekeeper (colf), carer (badante), babysitter – is entitled to a 13th monthly salary, the <em>tredicesima</em>, equal to one month of <strong>total actual pay</strong>. It accrues in twelfths: each month of work earns 1/12. It is paid <strong>by December</strong> (usually with the December pay or before Christmas) and, if the employment ends during the year, it is paid pro rata with the final payslip. A month counts if the employment lasted <strong>at least 15 days</strong> in that month.</p>
<h3>Hourly workers (non live-in)</h3>
<p>Start from the average monthly pay: <strong>hourly rate × weekly hours × 52 ÷ 12</strong>. The monthly accrual is one twelfth of that.</p>
<p><em>Example:</em> €9 per hour for 20 hours a week → 9 × 20 × 52 ÷ 12 = €780 a month → accrual €65 → 13th-month pay of <strong>€780</strong> for a full year, €325 if the employment started in August (5 months).</p>
<h3>Live-in workers (monthly pay)</h3>
<p>Use the gross monthly pay <strong>plus the board and lodging allowance</strong> (indennità di vitto e alloggio), which is part of the total actual pay and therefore also of the 13th month; its daily value is set every year by the contract tables. Non live-in workers have no allowance.</p>
<h2>Good to know</h2>
<ul>
<li>The 13th month also accrues during holidays, sickness and injury; during maternity leave only the employer's share (20%) accrues.</li>
<li>If the hours changed during the year, calculate each period with its own hours and add them up.</li>
<li><strong>INPS contributions</strong> are due on the 13th month as on any other pay: the worker's share is withheld and contributions are paid with the December quarter.</li>
<li>Domestic employers are not withholding agents: the 13th month is paid gross and the worker declares it with the rest of her income.</li>
</ul>
""" + CCNL_NOTE["en"],
    },
    "faq": {
        "it": [
            ("Quando va pagata la tredicesima alla colf?", "Entro dicembre, in genere con la paga di dicembre o prima di Natale. Se il rapporto termina prima, si paga con l'ultima busta paga in proporzione ai mesi maturati."),
            ("La badante ha iniziato a metà anno: quanto le spetta?", "Un dodicesimo della mensilità per ogni mese in cui ha lavorato almeno 15 giorni: inserisci la data di inizio nel calcolatore e il conto è automatico."),
            ("L'indennità di vitto e alloggio entra nella tredicesima?", "Sì, per le conviventi: fa parte della retribuzione globale di fatto su cui si calcola la tredicesima."),
        ],
        "en": [
            ("When must the 13th month be paid?", "By December, usually with the December pay or before Christmas. If the employment ends earlier, it is paid with the final payslip, pro rata to the months accrued."),
            ("The carer started mid-year: how much is due?", "One twelfth of the monthly pay for every month in which she worked at least 15 days: enter the start date and the calculator does the rest."),
            ("Is the board and lodging allowance included?", "Yes, for live-in workers: it is part of the total actual pay on which the 13th month is calculated."),
        ],
    },
}

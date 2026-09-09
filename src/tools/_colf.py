"""Shared pieces for the colf/badanti tools (tredicesima, ferie, TFR). Not a tool itself."""

# JS helpers injected at the top of each colf tool script
JS_COMMON = r"""
function monthsWorked(a, b) { // months counted in [a, b] with the CCNL rule: a fraction of month counts if >= 15 days
  if (!a || !b || b < a) return 0;
  var n = 0, cur = new Date(a.getFullYear(), a.getMonth(), 1), end = new Date(b.getFullYear(), b.getMonth(), 1);
  while (cur <= end) {
    var ms = new Date(cur.getFullYear(), cur.getMonth(), 1), me = new Date(cur.getFullYear(), cur.getMonth() + 1, 0);
    var s = a > ms ? a : ms, e = b < me ? b : me;
    if (RT.daysBetween(s, e) + 1 >= 15) n++;
    cur.setMonth(cur.getMonth() + 1);
  }
  return n;
}
function monthlyPay() { // reference monthly pay from the "type" selector
  var hourly = RT.$('#type').value === 'h';
  if (hourly) { var r = RT.num(RT.$('#rate').value), h = RT.num(RT.$('#hours').value); return (r > 0 && h > 0) ? r * h * 52 / 12 : NaN; }
  var m = RT.num(RT.$('#monthly').value), k = RT.num(RT.$('#kind').value) || 0; return m > 0 ? m + k : NaN;
}
function toggleType() {
  var hourly = RT.$('#type').value === 'h';
  RT.$$('.only-h').forEach(function (el) { el.classList.toggle('hide', !hourly); });
  RT.$$('.only-m').forEach(function (el) { el.classList.toggle('hide', hourly); });
}
function setDefaultDates(startId, endId, yearsBack) {
  var t = new Date(), s = RT.$(startId), e = RT.$(endId);
  if (s && !s.value) s.value = (t.getFullYear() - (yearsBack || 0)) + '-01-01';
  if (e && !e.value) e.value = yearsBack ? RT.isoToday() : t.getFullYear() + '-12-31';
}
RT.$('#type').addEventListener('change', toggleType); toggleType();
"""

# UI block for the pay inputs (hourly vs monthly)
UI_PAY = """
<div class="row">
  <div class="field"><label for="type">{{type}}</label><select id="type"><option value="h">{{type_h}}</option><option value="m">{{type_m}}</option></select></div>
  <div class="field only-h"><label for="rate">{{rate}}</label><input type="number" id="rate" min="0" step="0.01" value="9"></div>
  <div class="field only-h"><label for="hours">{{hours}}</label><input type="number" id="hours" min="1" max="60" step="0.5" value="20"></div>
  <div class="field only-m hide"><label for="monthly">{{monthly}}</label><input type="number" id="monthly" min="0" step="0.01" placeholder="es. 1200"></div>
  <div class="field only-m hide"><label for="kind">{{kind}}</label><input type="number" id="kind" min="0" step="0.01" placeholder="0"></div>
</div>
"""

STR_PAY = {
    "it": {
        "type": "Tipo di rapporto", "type_h": "A ore (non convivente)", "type_m": "Mensile (convivente o tempo pieno)",
        "rate": "Paga oraria lorda (€)", "hours": "Ore a settimana", "monthly": "Retribuzione mensile lorda (€)", "kind": "Indennità vitto e alloggio al mese (€, se convivente)",
        "start": "Inizio del periodo", "end": "Fine del periodo", "months": "Mesi maturati", "month_pay": "Retribuzione mensile di riferimento",
        "rule": "Regola del contratto: un mese conta se il rapporto è durato almeno 15 giorni in quel mese.",
    },
    "en": {
        "type": "Type of contract", "type_h": "Hourly (non live-in)", "type_m": "Monthly (live-in or full time)",
        "rate": "Gross hourly rate (€)", "hours": "Hours per week", "monthly": "Gross monthly pay (€)", "kind": "Board and lodging allowance per month (€, live-in only)",
        "start": "Start of the period", "end": "End of the period", "months": "Months accrued", "month_pay": "Reference monthly pay",
        "rule": "Contract rule: a month counts if the employment lasted at least 15 days in that month.",
    },
}

# Shared paragraph about the CCNL, appended to each article
CCNL_NOTE = {
    "it": """
<h2>Il contratto di riferimento</h2>
<p>Le regole applicate sono quelle del <strong>CCNL sulla disciplina del rapporto di lavoro domestico</strong> (colf, badanti, baby sitter), firmato da Fidaldo, Domina e dai sindacati di categoria, che vale per tutti i rapporti regolari in Italia. Gli importi sono <strong>lordi</strong>: contributi INPS (con la quota a carico del lavoratore) e tasse vanno considerati a parte. Questo calcolatore serve per una stima veloce; per la busta paga ufficiale e i casi particolari (part-time verticale, cambi di orario durante l'anno, assenze lunghe) rivolgiti a un'associazione datoriale, a un consulente del lavoro o a un servizio di elaborazione paghe.</p>
""",
    "en": """
<h2>The reference contract</h2>
<p>The rules applied are those of the <strong>Italian national collective agreement for domestic work</strong> (CCNL lavoro domestico: housekeepers, carers, babysitters), which covers every regular domestic employment in Italy. Amounts are <strong>gross</strong>: INPS social contributions (including the worker's share) and taxes are separate. This calculator is meant for a quick estimate; for the official payslip and special cases (vertical part-time, changes of hours during the year, long absences) ask an employers' association, a labour consultant or a payroll service.</p>
""",
}

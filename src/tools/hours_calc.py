"""Calcolo ore lavorate (foglio ore settimanale), somma di ore e minuti, ore decimali."""


def _min_table(lang):
    sep = "," if lang == "it" else "."
    head = "<tr><th>%s</th><th>%s</th></tr>" % (("Minuti", "Ore decimali") if lang == "it" else ("Minutes", "Decimal hours"))
    rows = []
    for m in range(5, 61, 5):
        v = ("%.2f" % (m / 60)).rstrip("0").rstrip(".").replace(".", sep)
        rows.append("<tr><td>%d</td><td>%s</td></tr>" % (m, v))
    return '<div class="table-wrap" style="max-width:320px"><table>%s%s</table></div>' % (head, "".join(rows))


_JS = r"""
var mode = 'week', wk = RT.$('#wk'), srows = RT.$('#srows');
function toMin(v) { if (!v) return NaN; var p = String(v).split(':'); if (p.length < 2) return NaN; var h = +p[0], m = +p[1]; return (isFinite(h) && isFinite(m)) ? h * 60 + m : NaN; }
function hm(mins) {
  var neg = mins < 0, a = Math.round(Math.abs(mins)), h = Math.floor(a / 60), m = a % 60;
  return (neg ? '−' : '') + RT.fmt(h, 0) + ' h ' + RT.pad(m) + ' min';
}
function hms(secs) {
  var a = Math.round(Math.abs(secs)), h = Math.floor(a / 3600), m = Math.floor(a % 3600 / 60), s = a % 60;
  return RT.fmt(h, 0) + ' h ' + RT.pad(m) + ' min' + (s ? ' ' + RT.pad(s) + ' s' : '');
}
function clock(mins) { var a = Math.round(mins); return Math.floor(a / 60) + ':' + RT.pad(a % 60); }
function hoursWord(x) { return Math.abs(x) === 1 ? T.hour_w : T.hours_w; }
// weekly timesheet rows
T.days.forEach(function (d, i) {
  var tr = document.createElement('tr'), on = i < 5;
  tr.innerHTML = '<td><b></b></td>' +
    '<td><input type="time" class="ti" style="min-width:96px"></td>' +
    '<td><input type="time" class="to" style="min-width:96px"></td>' +
    '<td><input type="number" class="tb" min="0" max="720" step="5" style="min-width:70px"></td>' +
    '<td class="mono tr" style="white-space:nowrap"></td>';
  tr.querySelector('b').textContent = d;
  RT.$('.ti', tr).value = on ? '09:00' : ''; RT.$('.to', tr).value = on ? '18:00' : ''; RT.$('.tb', tr).value = on ? '60' : '';
  RT.$('.ti', tr).setAttribute('aria-label', T.in_l + ' – ' + d); RT.$('.to', tr).setAttribute('aria-label', T.out_l + ' – ' + d); RT.$('.tb', tr).setAttribute('aria-label', T.brk_l + ' – ' + d);
  wk.appendChild(tr);
});
function calcWeek() {
  var tot = 0, days = 0, bad = false;
  RT.$$('tr', wk).forEach(function (tr) {
    var a = toMin(RT.$('.ti', tr).value), b = toMin(RT.$('.to', tr).value), br = RT.num(RT.$('.tb', tr).value), cell = RT.$('.tr', tr);
    if (!isFinite(a) || !isFinite(b)) { cell.textContent = ''; return; }
    var span = b - a, night = span < 0; if (night) span += 1440;
    if (!isFinite(br) || br < 0) br = 0;
    var w = span - br;
    if (w < 0) { cell.textContent = '⚠'; bad = true; return; }
    cell.textContent = clock(w) + (night ? ' 🌙' : '');
    tot += w; if (w > 0) days++;
  });
  var dec = tot / 60;
  RT.$('#wmain').textContent = hm(tot);
  RT.$('#wsub').textContent = T.week_sub.replace('{d}', RT.fmtFixed(dec, 2)).replace('{n}', days);
  RT.$('#wavg').textContent = days ? hm(tot / days) : '–';
  RT.$('#wdec').textContent = RT.fmtFixed(dec, 2);
  var std = RT.num(RT.$('#std').value), over = isFinite(std) && std > 0 ? Math.max(0, tot - std * 60) : 0;
  RT.$('#wover').textContent = hm(over); RT.$('#woverl').textContent = T.over_l.replace('{s}', RT.fmt(isFinite(std) ? std : 0, 1));
  var rate = RT.num(RT.$('#rate').value), pay = isFinite(rate) && rate > 0 ? rate * dec : NaN;
  RT.$('#wpay').textContent = isFinite(pay) ? RT.money(pay) : '–';
  RT.$('#werr').classList.toggle('hide', !bad);
  RT.$('#wsum').value = T.summary.replace('{t}', hm(tot)).replace('{d}', RT.fmtFixed(dec, 2)).replace('{n}', days).replace('{a}', days ? hm(tot / days) : '–') + (isFinite(pay) ? ' · ' + T.pay_l + ' ' + RT.money(pay) : '');
}
function addSRow(sign, h, m) {
  var tr = document.createElement('tr');
  tr.innerHTML = '<td><select class="ss" style="width:auto"><option value="1">+</option><option value="-1">−</option></select></td>' +
    '<td><input type="number" class="sh" min="0" step="1" style="min-width:70px"></td>' +
    '<td><input type="number" class="sm" min="0" step="1" style="min-width:70px"></td>' +
    '<td><button type="button" class="btn small rm">✕</button></td>';
  RT.$('.ss', tr).value = sign === -1 ? '-1' : '1'; RT.$('.sh', tr).value = h === undefined ? '' : h; RT.$('.sm', tr).value = m === undefined ? '' : m;
  RT.$('.ss', tr).setAttribute('aria-label', T.sign_l); RT.$('.sh', tr).setAttribute('aria-label', T.hours_l); RT.$('.sm', tr).setAttribute('aria-label', T.minutes_l); RT.$('.rm', tr).setAttribute('aria-label', T.remove_l);
  srows.appendChild(tr);
  RT.$$('input,select', tr).forEach(function (el) { el.addEventListener('input', calc); el.addEventListener('change', calc); });
  RT.$('.rm', tr).addEventListener('click', function () { tr.remove(); calc(); });
}
function calcSum() {
  var tot = 0;
  RT.$$('tr', srows).forEach(function (tr) {
    var h = RT.num(RT.$('.sh', tr).value), m = RT.num(RT.$('.sm', tr).value);
    if (!isFinite(h) && !isFinite(m)) return;
    tot += ((isFinite(h) ? h * 60 : 0) + (isFinite(m) ? m : 0)) * +RT.$('.ss', tr).value;
  });
  RT.$('#smain').textContent = hm(tot);
  var sub = T.sum_sub.replace('{d}', RT.fmtFixed(tot / 60, 2)).replace('{m}', RT.fmt(tot, 0));
  if (Math.abs(tot) >= 1440) { var a = Math.round(Math.abs(tot)), g = Math.floor(a / 1440), r = a % 1440; sub += ' · ' + (g === 1 ? T.as_day : T.as_days).replace('{g}', g).replace('{h}', Math.floor(r / 60)).replace('{m}', RT.pad(r % 60)); }
  RT.$('#ssub').textContent = sub;
}
function calcDec() {
  var h = RT.num(RT.$('#dh').value), m = RT.num(RT.$('#dm').value);
  if (!isFinite(h) && !isFinite(m)) { RT.$('#dres').textContent = '–'; RT.$('#dsub').textContent = ''; }
  else {
    var mins = (isFinite(h) ? h * 60 : 0) + (isFinite(m) ? m : 0), d = mins / 60;
    RT.$('#dres').textContent = RT.fmt(d, 4) + ' ' + hoursWord(d);
    RT.$('#dsub').textContent = T.dec_sub.replace('{hm}', hm(mins)).replace('{m}', RT.fmt(mins, 2));
  }
  var x = RT.num(RT.$('#dd').value);
  if (!isFinite(x)) { RT.$('#dres2').textContent = '–'; RT.$('#dsub2').textContent = ''; }
  else { RT.$('#dres2').textContent = hms(x * 3600); RT.$('#dsub2').textContent = T.dec_sub2.replace('{d}', RT.fmt(x, 4) + ' ' + hoursWord(x)).replace('{m}', RT.fmt(x * 60, 2)); }
}
function calc() { if (mode === 'week') calcWeek(); else if (mode === 'sum') calcSum(); else calcDec(); }
RT.$$('.tabs button').forEach(function (b) {
  b.addEventListener('click', function () {
    RT.$$('.tabs button').forEach(function (x) { x.classList.toggle('on', x === b); });
    mode = b.getAttribute('data-tab');
    ['week', 'sum', 'dec'].forEach(function (k) { RT.$('#tab-' + k).classList.toggle('hide', k !== mode); });
    calc();
  });
});
RT.$('#copymon').addEventListener('click', function () {
  var rows = RT.$$('tr', wk), first = rows[0];
  for (var i = 1; i < 5; i++) { ['.ti', '.to', '.tb'].forEach(function (c) { RT.$(c, rows[i]).value = RT.$(c, first).value; }); }
  calc();
});
RT.$('#wclear').addEventListener('click', function () { RT.$$('input', wk).forEach(function (el) { el.value = ''; }); calc(); });
RT.$('#sadd').addEventListener('click', function () { addSRow(1); RT.$('.sh', srows.lastChild).focus(); });
RT.$('#sreset').addEventListener('click', function () { srows.innerHTML = ''; for (var i = 0; i < 4; i++) addSRow(1); calc(); });
addSRow(1, 7, 30); addSRow(1, 8, 15); addSRow(1, 6, 45); addSRow(1);
RT.live(document.getElementById('tool'), calc);
"""

TOOL = {
    "id": "hours_calc",
    "cat": "work",
    "icon": "🕘",
    "slug": {"it": "calcolo-ore-lavorate", "en": "hours-worked-calculator"},
    "title": {"it": "Calcolo ore lavorate, somma ore e minuti", "en": "Hours worked calculator: add hours and minutes"},
    "short": {"it": "Ore tra entrata e uscita con la pausa, totale della settimana, somma di ore e ore decimali", "en": "Hours between clock-in and clock-out with breaks, weekly total, adding times and decimal hours"},
    "keywords": {
        "it": ["calcolo ore", "ore lavorate", "somma ore", "calcolatrice ore", "ore e minuti", "ore decimali", "minuti in centesimi", "ore in centesimi", "foglio ore", "straordinari", "turno di notte"],
        "en": ["time card calculator", "hours calculator", "add hours and minutes", "decimal hours", "timesheet", "minutes to hours", "overtime"],
    },
    "meta": {
        "it": "Calcola le ore lavorate tra entrata e uscita togliendo la pausa, anche con il turno di notte, con il totale della settimana, gli straordinari e la paga. Somma ore e minuti e converti in ore decimali (7:45 = 7,75).",
        "en": "Work out hours worked between clock-in and clock-out minus breaks, overnight shifts included, with the weekly total, overtime and pay. Add hours and minutes and convert to decimal hours (7:45 = 7.75).",
    },
    "intro": {
        "it": "Tre strumenti in uno: il foglio ore della settimana (entrata, uscita e pausa → ore lavorate, straordinari e paga), la somma di ore e minuti, e la conversione tra ore e minuti e ore decimali.",
        "en": "Three tools in one: a weekly timesheet (clock-in, clock-out and break → hours worked, overtime and pay), an hours-and-minutes adder, and a converter between hours and minutes and decimal hours.",
    },
    "strings": {
        "it": {
            "tab_week": "Ore lavorate", "tab_sum": "Somma ore", "tab_dec": "Ore decimali",
            "days": ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"],
            "day_h": "Giorno", "in_l": "Entrata", "out_l": "Uscita", "brk_l": "Pausa (min)", "worked_h": "Ore",
            "copy_mon": "Copia il lunedì fino a venerdì", "clear": "Svuota",
            "rate_l": "Paga oraria (facoltativa)", "rate_ph": "es. 9,50", "std_l": "Ore settimanali da contratto",
            "week_sub": "= {d} ore decimali · {n} giorni lavorati", "avg_day": "Media al giorno", "dec_l": "Ore decimali", "over_l": "Ore oltre le {s} settimanali", "pay_l": "Paga lorda",
            "brk_err": "In un giorno la pausa è più lunga del tempo tra entrata e uscita: controlla i valori segnati con ⚠.",
            "copy_res": "Copia il riepilogo", "summary": "Totale settimana: {t} ({d} ore) · {n} giorni · media {a} al giorno",
            "sign_l": "Più o meno", "hours_l": "Ore", "minutes_l": "Minuti", "remove_l": "Togli", "add_row": "+ Aggiungi riga",
            "sum_sub": "= {d} ore decimali · {m} minuti", "as_day": "{g} giorno {h} h {m} min", "as_days": "{g} giorni {h} h {m} min",
            "to_dec_t": "Da ore e minuti a ore decimali", "from_dec_t": "Da ore decimali a ore e minuti", "dec_in": "Ore decimali (es. 7,3)",
            "dec_sub": "{hm} = {m} minuti", "dec_sub2": "{d} = {m} minuti", "hour_w": "ora", "hours_w": "ore",
        },
        "en": {
            "tab_week": "Hours worked", "tab_sum": "Add hours", "tab_dec": "Decimal hours",
            "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "day_h": "Day", "in_l": "In", "out_l": "Out", "brk_l": "Break (min)", "worked_h": "Hours",
            "copy_mon": "Copy Monday to Friday", "clear": "Clear",
            "rate_l": "Hourly rate (optional)", "rate_ph": "e.g. 15.50", "std_l": "Contract hours per week",
            "week_sub": "= {d} decimal hours · {n} days worked", "avg_day": "Average per day", "dec_l": "Decimal hours", "over_l": "Hours above {s} a week", "pay_l": "Gross pay",
            "brk_err": "On one day the break is longer than the time between in and out: check the values marked ⚠.",
            "copy_res": "Copy the summary", "summary": "Weekly total: {t} ({d} hours) · {n} days · average {a} per day",
            "sign_l": "Plus or minus", "hours_l": "Hours", "minutes_l": "Minutes", "remove_l": "Remove", "add_row": "+ Add row",
            "sum_sub": "= {d} decimal hours · {m} minutes", "as_day": "{g} day {h} h {m} min", "as_days": "{g} days {h} h {m} min",
            "to_dec_t": "From hours and minutes to decimal hours", "from_dec_t": "From decimal hours to hours and minutes", "dec_in": "Decimal hours (e.g. 7.3)",
            "dec_sub": "{hm} = {m} minutes", "dec_sub2": "{d} = {m} minutes", "hour_w": "hour", "hours_w": "hours",
        },
    },
    "ui": """
<div class="tabs" role="tablist">
  <button type="button" class="on" data-tab="week">{{tab_week}}</button>
  <button type="button" data-tab="sum">{{tab_sum}}</button>
  <button type="button" data-tab="dec">{{tab_dec}}</button>
</div>
<div id="tab-week">
  <div class="table-wrap"><table><thead><tr><th>{{day_h}}</th><th>{{in_l}}</th><th>{{out_l}}</th><th>{{brk_l}}</th><th>{{worked_h}}</th></tr></thead><tbody id="wk"></tbody></table></div>
  <div class="inline" style="margin-top:10px">
    <button class="btn small" type="button" id="copymon">{{copy_mon}}</button>
    <button class="btn small" type="button" id="wclear">{{clear}}</button>
  </div>
  <div class="row" style="margin-top:12px">
    <div class="field"><label for="rate">{{rate_l}}</label><input type="text" inputmode="decimal" id="rate" placeholder="{{rate_ph}}"></div>
    <div class="field"><label for="std">{{std_l}}</label><input type="number" id="std" min="0" max="80" step="0.5" value="40"></div>
  </div>
  <p class="msg warn hide" id="werr">{{brk_err}}</p>
  <div class="result">
    <div class="big" id="wmain"></div>
    <div class="sub" id="wsub"></div>
    <div class="stats">
      <div class="stat"><b id="wavg"></b><span>{{avg_day}}</span></div>
      <div class="stat"><b id="wdec"></b><span>{{dec_l}}</span></div>
      <div class="stat"><b id="wover"></b><span id="woverl"></span></div>
      <div class="stat"><b id="wpay"></b><span>{{pay_l}}</span></div>
    </div>
    <p class="btns"><button class="btn small" type="button" data-copy="#wsum" data-done="{{copied}}">{{copy_res}}</button><input type="hidden" id="wsum"></p>
  </div>
</div>
<div id="tab-sum" class="hide">
  <div class="table-wrap"><table><thead><tr><th></th><th>{{hours_l}}</th><th>{{minutes_l}}</th><th></th></tr></thead><tbody id="srows"></tbody></table></div>
  <div class="inline" style="margin-top:10px">
    <button class="btn small" type="button" id="sadd">{{add_row}}</button>
    <button class="btn small" type="button" id="sreset">{{reset}}</button>
  </div>
  <div class="result">
    <div class="big" id="smain"></div>
    <div class="sub" id="ssub"></div>
  </div>
</div>
<div id="tab-dec" class="hide">
  <h3 style="font-size:1rem;margin-top:0">{{to_dec_t}}</h3>
  <div class="row">
    <div class="field"><label for="dh">{{hours_l}}</label><input type="number" id="dh" min="0" step="1" value="7"></div>
    <div class="field"><label for="dm">{{minutes_l}}</label><input type="number" id="dm" min="0" step="1" value="45"></div>
  </div>
  <div class="result" style="margin-top:0"><div class="big" id="dres"></div><div class="sub" id="dsub"></div></div>
  <h3 style="font-size:1rem">{{from_dec_t}}</h3>
  <div class="row">
    <div class="field"><label for="dd">{{dec_in}}</label><input type="text" inputmode="decimal" id="dd" value="7,3"></div>
  </div>
  <div class="result" style="margin-top:0"><div class="big" id="dres2"></div><div class="sub" id="dsub2"></div></div>
</div>
""",
    "js": _JS,
    "article": {
        "it": f"""
<h2>Come si calcolano le ore lavorate</h2>
<p>Per ogni giorno si fa l'ora di uscita meno l'ora di entrata e si toglie la pausa. Dalle 8:30 alle 17:15 con 45 minuti di pausa: 17:15 − 8:30 = 8 h 45 min, meno 45 minuti = <strong>8 ore</strong>. Se esci dopo mezzanotte (turno di notte, per esempio dalle 22:00 alle 6:00) il calcolatore capisce da solo che l'uscita è il giorno dopo e conta 8 ore; la riga viene segnata con 🌙.</p>
<p>Il totale della settimana si legge in ore e minuti (per esempio 38 h 30 min) e in ore decimali (38,50): sono queste ultime da moltiplicare per la paga oraria, 38,5 × 10 € = 385 €. Se inserisci le ore settimanali previste dal contratto (spesso 40, in molti contratti 36 o 38) vedi anche le ore in più: se e come vengano pagate come straordinario lo stabilisce il tuo contratto.</p>
<h2>Ore e minuti in ore decimali (ore in centesimi)</h2>
<p>Buste paga, fatture e fogli di calcolo usano spesso le ore decimali, dette anche «in centesimi»: 7 ore e 45 minuti non sono 7,45 ma <strong>7,75</strong>, perché 45 minuti sono tre quarti d'ora. Per convertire si dividono i minuti per 60 (45 ÷ 60 = 0,75); per tornare indietro si moltiplica la parte decimale per 60 (0,3 × 60 = 18 minuti, quindi 7,3 ore = 7 h 18 min).</p>
{_min_table("it")}
<h2>Sommare e sottrarre ore e minuti</h2>
<p>Quando si sommano degli orari i minuti si riportano ogni 60, non ogni 100: 2 h 40 min + 1 h 30 min = <strong>4 h 10 min</strong> (e non 3,70). La scheda «Somma ore» fa il riporto per te, accetta anche le sottrazioni (scegli «−» nella riga) e, se il totale supera le 24 ore, lo mostra anche in giorni: utile per sommare le ore di un mese, i tempi di un progetto o le ore di volo.</p>
""",
        "en": f"""
<h2>How hours worked are calculated</h2>
<p>For each day, subtract the clock-in time from the clock-out time and remove the break. From 8:30 to 17:15 with a 45-minute break: 17:15 − 8:30 = 8 h 45 min, minus 45 minutes = <strong>8 hours</strong>. If you finish after midnight (a night shift such as 22:00 to 6:00) the calculator understands that you clocked out the next day and counts 8 hours; the row is marked with 🌙.</p>
<p>The weekly total is shown in hours and minutes (for example 38 h 30 min) and in decimal hours (38.50): multiply the decimal hours by your hourly rate, 38.5 × 10 = 385. If you enter your contract hours per week (often 40, or 36–38 in many contracts) you also see the hours above them; whether and how they are paid as overtime depends on your contract.</p>
<h2>Hours and minutes to decimal hours</h2>
<p>Payroll, invoices and spreadsheets often use decimal hours: 7 hours 45 minutes is not 7.45 but <strong>7.75</strong>, because 45 minutes are three quarters of an hour. To convert, divide the minutes by 60 (45 ÷ 60 = 0.75); to go back, multiply the decimal part by 60 (0.3 × 60 = 18 minutes, so 7.3 hours = 7 h 18 min).</p>
{_min_table("en")}
<h2>Adding and subtracting hours and minutes</h2>
<p>When you add times, minutes carry over every 60, not every 100: 2 h 40 min + 1 h 30 min = <strong>4 h 10 min</strong> (not 3.70). The "Add hours" tab does the carrying for you, handles subtractions (choose "−" in a row) and, when the total goes over 24 hours, also shows it in days: handy for monthly hours, project time or flight hours.</p>
""",
    },
    "faq": {
        "it": [
            ("7 ore e 30 minuti in decimali quanto fa?", "7,5. I minuti si dividono per 60: 30 ÷ 60 = 0,5. Allo stesso modo 15 minuti sono 0,25 e 45 minuti 0,75."),
            ("Come si calcolano le ore di un turno di notte?", "Inserisci entrata e uscita così come sono: se l'uscita è prima dell'entrata (per esempio 22:00 e 6:00) il calcolatore conta il passaggio della mezzanotte."),
            ("Posso calcolare la paga della settimana?", "Sì: inserisci la paga oraria e il calcolatore la moltiplica per le ore decimali. È una stima lorda: tasse, contributi e maggiorazioni dipendono dal tuo contratto."),
            ("Il calcolatore salva i miei orari?", "No: i dati restano nella pagina e spariscono quando la chiudi. Puoi copiare il riepilogo con il pulsante."),
        ],
        "en": [
            ("What is 7 hours 30 minutes in decimal?", "7.5. Divide the minutes by 60: 30 ÷ 60 = 0.5. Likewise 15 minutes are 0.25 and 45 minutes 0.75."),
            ("How do I calculate a night shift?", "Enter clock-in and clock-out as they are: if clock-out is earlier than clock-in (for example 22:00 and 6:00) the calculator counts across midnight."),
            ("Can I work out my weekly pay?", "Yes: enter your hourly rate and it is multiplied by the decimal hours. It is a gross estimate: taxes, contributions and premiums depend on your contract."),
            ("Does the calculator save my times?", "No: the data stays on the page and disappears when you close it. You can copy the summary with the button."),
        ],
    },
}

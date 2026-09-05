TOOL = {
    "id": "days_between",
    "cat": "date",
    "icon": "📆",
    "slug": {"it": "giorni-tra-due-date", "en": "days-between-dates"},
    "title": {"it": "Giorni tra due date", "en": "Days between two dates"},
    "short": {"it": "Quanti giorni, settimane e giorni lavorativi separano due date", "en": "Days, weeks and working days between two dates"},
    "keywords": {"it": ["quanti giorni mancano", "differenza tra date", "conta giorni", "giorni lavorativi"], "en": ["date difference", "day counter", "how many days until", "business days"]},
    "meta": {
        "it": "Calcola quanti giorni, settimane, mesi e giorni lavorativi ci sono tra due date. Perfetto per scadenze, ferie, conto alla rovescia e durate.",
        "en": "Count the days, weeks, months and working days between two dates. Perfect for deadlines, holidays, countdowns and durations.",
    },
    "intro": {
        "it": "Scegli una data di inizio e una di fine: ottieni subito i giorni totali, le settimane, i mesi e i giorni lavorativi (lunedì–venerdì) che le separano.",
        "en": "Pick a start date and an end date to instantly get the total days, weeks, months and working days (Monday–Friday) between them.",
    },
    "strings": {
        "it": {
            "from": "Data di inizio", "to": "Data di fine", "include": "Includi anche il giorno finale",
            "days": "giorni", "day": "giorno", "weeks": "settimane", "week": "settimana", "months": "mesi", "month": "mese", "years": "anni", "year": "anno",
            "total": "Giorni totali", "work": "Giorni lavorativi (lun–ven)", "weekend": "Giorni di weekend", "wk": "Settimane e giorni", "ym": "Anni, mesi e giorni",
            "hours": "ore", "from_wd": "Inizio", "to_wd": "Fine", "swap": "Inverti", "today": "Oggi",
            "past": "La data di fine è precedente a quella di inizio: le date sono state invertite nel calcolo.",
        },
        "en": {
            "from": "Start date", "to": "End date", "include": "Include the end date too",
            "days": "days", "day": "day", "weeks": "weeks", "week": "week", "months": "months", "month": "month", "years": "years", "year": "year",
            "total": "Total days", "work": "Working days (Mon–Fri)", "weekend": "Weekend days", "wk": "Weeks and days", "ym": "Years, months and days",
            "hours": "hours", "from_wd": "Start", "to_wd": "End", "swap": "Swap", "today": "Today",
            "past": "The end date is before the start date: the dates were swapped for the calculation.",
        },
    },
    "ui": """
<div class="row">
  <div class="field"><label for="d1">{{from}}</label><input type="date" id="d1"></div>
  <div class="field"><label for="d2">{{to}}</label><input type="date" id="d2"></div>
</div>
<div class="inline">
  <label class="check"><input type="checkbox" id="incl"> {{include}}</label>
  <button class="btn small" type="button" id="swap">⇄ {{swap}}</button>
  <button class="btn small" type="button" id="today">{{today}}</button>
</div>
<p class="msg warn hide" id="past">{{past}}</p>
<div class="result hide" id="out">
  <div class="big" id="main"></div>
  <div class="sub" id="sub"></div>
  <div class="stats">
    <div class="stat"><b id="wk"></b><span>{{wk}}</span></div>
    <div class="stat"><b id="ym"></b><span>{{ym}}</span></div>
    <div class="stat"><b id="work"></b><span>{{work}}</span></div>
    <div class="stat"><b id="wend"></b><span>{{weekend}}</span></div>
  </div>
</div>
""",
    "js": r"""
var d1 = RT.$('#d1'), d2 = RT.$('#d2'), incl = RT.$('#incl'), out = RT.$('#out'), past = RT.$('#past');
d1.value = RT.isoToday();
var end = new Date(); end.setDate(end.getDate() + 30);
d2.value = end.getFullYear() + '-' + RT.pad(end.getMonth() + 1) + '-' + RT.pad(end.getDate());
function pl(n, one, many) { return RT.fmt(n, 0) + ' ' + (n === 1 ? one : many); }
function ymd(a, b) {
  var y = b.getFullYear() - a.getFullYear(), m = b.getMonth() - a.getMonth(), d = b.getDate() - a.getDate();
  if (d < 0) { m--; d += new Date(b.getFullYear(), b.getMonth(), 0).getDate(); }
  if (m < 0) { y--; m += 12; }
  return [y, m, d];
}
function calc() {
  var a = RT.parseDate(d1.value), b = RT.parseDate(d2.value);
  if (!a || !b) { out.classList.add('hide'); return; }
  var swapped = false;
  if (b < a) { var t = a; a = b; b = t; swapped = true; }
  past.classList.toggle('hide', !swapped);
  var total = RT.daysBetween(a, b) + (incl.checked ? 1 : 0);
  // working days
  var work = 0, wend = 0, cur = new Date(a.getFullYear(), a.getMonth(), a.getDate());
  var lastExclusive = incl.checked ? total : total; // iterate `total` days starting at a
  for (var i = 0; i < total; i++) {
    var wd = cur.getDay(); if (wd === 0 || wd === 6) wend++; else work++;
    cur.setDate(cur.getDate() + 1);
  }
  RT.$('#main').textContent = pl(total, T.day, T.days);
  RT.$('#sub').textContent = T.from_wd + ': ' + RT.weekday(a) + ' ' + RT.date(a) + ' → ' + T.to_wd + ': ' + RT.weekday(b) + ' ' + RT.date(b) + ' · ' + RT.fmt(total * 24, 0) + ' ' + T.hours;
  RT.$('#wk').textContent = pl(Math.floor(total / 7), T.week, T.weeks) + (total % 7 ? ' + ' + pl(total % 7, T.day, T.days) : '');
  var r = ymd(a, b); if (incl.checked) { var b2 = new Date(b); b2.setDate(b2.getDate() + 1); r = ymd(a, b2); }
  RT.$('#ym').textContent = pl(r[0], T.year, T.years) + ', ' + pl(r[1], T.month, T.months) + ', ' + pl(r[2], T.day, T.days);
  RT.$('#work').textContent = RT.fmt(work, 0);
  RT.$('#wend').textContent = RT.fmt(wend, 0);
  out.classList.remove('hide');
}
RT.$('#swap').addEventListener('click', function () { var t = d1.value; d1.value = d2.value; d2.value = t; calc(); });
RT.$('#today').addEventListener('click', function () { d1.value = RT.isoToday(); calc(); });
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>Come si contano i giorni tra due date</h2>
<p>Il calcolatore conta i giorni che vanno dalla data di inizio alla data di fine. Per impostazione predefinita il giorno finale <em>non</em> è incluso: dal 1° al 10 settembre risultano 9 giorni, cioè la distanza tra le due date. Se ti serve la durata di un periodo «compresi gli estremi», per esempio i giorni di una vacanza dal 1° al 10 settembre (10 giorni), spunta «Includi anche il giorno finale».</p>
<h2>Giorni lavorativi e weekend</h2>
<p>I giorni lavorativi sono quelli dal lunedì al venerdì; sabato e domenica contano come weekend. Le festività nazionali non vengono sottratte, perché cambiano da paese a paese e da anno ad anno: se nel periodo ci sono festivi infrasettimanali, toglili a mano dal totale.</p>
<h2>Esempi pratici</h2>
<ul>
<li><strong>Quanti giorni mancano a una data?</strong> Metti oggi come inizio (pulsante «Oggi») e la data dell'evento come fine.</li>
<li><strong>Durata di un contratto o di un abbonamento:</strong> inizio e fine del contratto, senza includere il giorno finale se la scadenza è «entro il».</li>
<li><strong>Giorni di ferie o di malattia:</strong> spunta «Includi anche il giorno finale» e leggi i giorni lavorativi.</li>
<li><strong>Quanto tempo è passato?</strong> Inserisci la data passata come inizio: il risultato mostra anche anni, mesi e giorni.</li>
</ul>
<p>Anni bisestili e mesi di lunghezza diversa sono gestiti automaticamente.</p>
""",
        "en": """
<h2>How days between dates are counted</h2>
<p>The calculator counts the days from the start date to the end date. By default the end date is <em>not</em> included: from 1 to 10 September gives 9 days, i.e. the distance between the two dates. If you need the length of a period "inclusive", such as a holiday from 1 to 10 September (10 days), tick "Include the end date too".</p>
<h2>Working days and weekends</h2>
<p>Working days are Monday to Friday; Saturday and Sunday count as weekend. Public holidays are not subtracted, because they differ by country and year: if the period contains weekday holidays, subtract them by hand.</p>
<h2>Practical examples</h2>
<ul>
<li><strong>How many days until an event?</strong> Set today as the start (the "Today" button) and the event date as the end.</li>
<li><strong>Length of a contract or subscription:</strong> start and end of the contract, without including the end date if the deadline is "by".</li>
<li><strong>Holiday or sick days:</strong> tick "Include the end date too" and read the working days.</li>
<li><strong>How much time has passed?</strong> Enter the past date as the start: the result also shows years, months and days.</li>
</ul>
<p>Leap years and months of different lengths are handled automatically.</p>
""",
    },
    "faq": {
        "it": [
            ("Il giorno finale è compreso nel conteggio?", "No, per impostazione predefinita si contano i giorni «di distanza» tra le due date. Spunta «Includi anche il giorno finale» per contare entrambi gli estremi, come si fa per ferie o soggiorni."),
            ("Vengono tolte le festività?", "No. Vengono esclusi solo sabato e domenica nel conteggio dei giorni lavorativi; le festività nazionali vanno sottratte a mano."),
            ("Posso usare date nel passato o molto lontane nel futuro?", "Sì, qualsiasi data accettata dal calendario funziona, anche a distanza di decenni. Se la fine è prima dell'inizio, le date vengono invertite automaticamente."),
        ],
        "en": [
            ("Is the end date included in the count?", "No, by default the calculator counts the days \"between\" the two dates. Tick \"Include the end date too\" to count both ends, as you would for holidays or stays."),
            ("Are public holidays removed?", "No. Only Saturdays and Sundays are excluded from the working-day count; national holidays must be subtracted by hand."),
            ("Can I use dates in the past or far in the future?", "Yes, any valid calendar date works, even decades apart. If the end date is before the start, the dates are swapped automatically."),
        ],
    },
}

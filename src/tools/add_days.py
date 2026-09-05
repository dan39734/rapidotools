TOOL = {
    "id": "add_days",
    "cat": "date",
    "icon": "➕",
    "slug": {"it": "aggiungi-giorni-a-una-data", "en": "add-days-to-date"},
    "title": {"it": "Aggiungi o sottrai giorni a una data", "en": "Add or subtract days from a date"},
    "short": {"it": "Che giorno sarà tra 30, 60 o 90 giorni? Anche settimane, mesi e giorni lavorativi", "en": "What date is 30, 60 or 90 days from now? Weeks, months and working days too"},
    "keywords": {"it": ["tra 30 giorni", "tra 60 giorni", "tra 90 giorni", "calcolo scadenza", "data futura"], "en": ["30 days from today", "60 days from today", "90 days from today", "date calculator", "deadline"]},
    "meta": {
        "it": "Calcola la data che cade dopo (o prima) un certo numero di giorni, settimane, mesi o anni. Anche solo giorni lavorativi: perfetto per scadenze e termini.",
        "en": "Find the date that falls a number of days, weeks, months or years after (or before) a given date. Working days too: perfect for deadlines and notice periods.",
    },
    "intro": {
        "it": "Parti da una data, indica quanto tempo aggiungere o togliere e leggi la data risultante con il giorno della settimana. Utile per scadenze a 30, 60 o 90 giorni, preavvisi e termini di consegna.",
        "en": "Start from a date, choose how much time to add or subtract and read the resulting date with its weekday. Great for 30-, 60- or 90-day deadlines, notice periods and delivery dates.",
    },
    "strings": {
        "it": {
            "start": "Data di partenza", "amount": "Quantità", "unit": "Unità", "dir": "Operazione", "add": "Aggiungi", "sub": "Sottrai",
            "days": "giorni", "workdays": "giorni lavorativi (lun–ven)", "weeks": "settimane", "months": "mesi", "years": "anni",
            "result": "Data risultante", "today": "Oggi", "quick": "Scorciatoie", "diff": "differenza effettiva",
            "week_no": "Settimana n.", "day_of_year": "giorno dell'anno",
        },
        "en": {
            "start": "Start date", "amount": "Amount", "unit": "Unit", "dir": "Operation", "add": "Add", "sub": "Subtract",
            "days": "days", "workdays": "working days (Mon–Fri)", "weeks": "weeks", "months": "months", "years": "years",
            "result": "Resulting date", "today": "Today", "quick": "Shortcuts", "diff": "actual difference",
            "week_no": "Week no.", "day_of_year": "day of the year",
        },
    },
    "ui": """
<div class="row">
  <div class="field"><label for="start">{{start}}</label><input type="date" id="start"></div>
  <div class="field"><label for="dir">{{dir}}</label><select id="dir"><option value="1">{{add}}</option><option value="-1">{{sub}}</option></select></div>
</div>
<div class="row">
  <div class="field"><label for="n">{{amount}}</label><input type="number" id="n" value="30" min="0" step="1" inputmode="numeric"></div>
  <div class="field"><label for="unit">{{unit}}</label><select id="unit">
    <option value="d">{{days}}</option><option value="w">{{workdays}}</option><option value="wk">{{weeks}}</option><option value="m">{{months}}</option><option value="y">{{years}}</option></select></div>
</div>
<div class="inline"><span class="lbl">{{quick}}:</span>
  <button class="btn small" type="button" data-q="7">+7</button><button class="btn small" type="button" data-q="14">+14</button>
  <button class="btn small" type="button" data-q="30">+30</button><button class="btn small" type="button" data-q="60">+60</button>
  <button class="btn small" type="button" data-q="90">+90</button><button class="btn small" type="button" data-q="180">+180</button>
  <button class="btn small" type="button" data-q="365">+365</button></div>
<div class="result hide" id="out">
  <div class="sub">{{result}}</div>
  <div class="big" id="main"></div>
  <div class="sub" id="sub"></div>
</div>
""",
    "js": r"""
var start = RT.$('#start'), n = RT.$('#n'), unit = RT.$('#unit'), dir = RT.$('#dir'), out = RT.$('#out');
start.value = RT.isoToday();
function weekNumber(d) { // ISO 8601
  var t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  var day = t.getUTCDay() || 7; t.setUTCDate(t.getUTCDate() + 4 - day);
  var y0 = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
  return Math.ceil(((t - y0) / 86400000 + 1) / 7);
}
function calc() {
  var s = RT.parseDate(start.value), q = parseInt(n.value, 10), sign = parseInt(dir.value, 10);
  if (!s || isNaN(q) || q < 0) { out.classList.add('hide'); return; }
  var r = new Date(s.getFullYear(), s.getMonth(), s.getDate());
  var u = unit.value;
  if (u === 'd') r.setDate(r.getDate() + sign * q);
  else if (u === 'wk') r.setDate(r.getDate() + sign * q * 7);
  else if (u === 'm' || u === 'y') {
    var months = sign * (u === 'm' ? q : q * 12);
    var target = new Date(r.getFullYear(), r.getMonth() + months, 1);
    var dim = new Date(target.getFullYear(), target.getMonth() + 1, 0).getDate();
    r = new Date(target.getFullYear(), target.getMonth(), Math.min(s.getDate(), dim));
  } else { // working days
    var left = q;
    while (left > 0) { r.setDate(r.getDate() + sign); var wd = r.getDay(); if (wd !== 0 && wd !== 6) left--; }
  }
  RT.$('#main').textContent = RT.weekday(r) + ' ' + RT.date(r);
  var diff = RT.daysBetween(s, r);
  var y0 = new Date(r.getFullYear(), 0, 1), doy = RT.daysBetween(y0, r) + 1;
  RT.$('#sub').textContent = RT.fmt(Math.abs(diff), 0) + ' ' + T.days + ' (' + T.diff + ') · ' + T.week_no + ' ' + weekNumber(r) + ' · ' + doy + '° ' + T.day_of_year;
  out.classList.remove('hide');
}
RT.$$('[data-q]').forEach(function (b) { b.addEventListener('click', function () { n.value = b.getAttribute('data-q'); unit.value = 'd'; dir.value = '1'; calc(); }); });
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>A cosa serve</h2>
<p>Molte scadenze sono espresse come «entro 30 giorni», «60 giorni dalla consegna», «preavviso di 15 giorni lavorativi» o «tra 6 mesi». Contare sul calendario è lento e si sbaglia facilmente, soprattutto a cavallo di mesi di lunghezza diversa o di un anno bisestile. Questo strumento fa il conto per te e mostra anche il giorno della settimana, così vedi subito se la scadenza cade di sabato o domenica.</p>
<h2>Come si contano mesi e anni</h2>
<p>Aggiungere un mese significa spostarsi allo stesso giorno del mese successivo: dal 15 marzo al 15 aprile. Se il giorno non esiste nel mese di arrivo (per esempio 31 gennaio + 1 mese), il risultato è l'ultimo giorno disponibile, cioè il 28 o 29 febbraio. Lo stesso vale per gli anni: 29 febbraio 2024 + 1 anno = 28 febbraio 2025.</p>
<h2>Giorni lavorativi</h2>
<p>Con «giorni lavorativi» si saltano sabato e domenica: 10 giorni lavorativi da un lunedì portano al venerdì della settimana dopo. Le festività nazionali non sono considerate, perché variano da paese a paese.</p>
<h2>Esempi</h2>
<ul>
<li>Fattura con pagamento a 60 giorni emessa il 5 settembre: scade il 4 novembre.</li>
<li>Recesso con preavviso di 30 giorni comunicato il 20 gennaio: decorre dal 19 febbraio.</li>
<li>Garanzia di 2 anni da un acquisto del 10 giugno 2026: termina il 10 giugno 2028.</li>
</ul>
""",
        "en": """
<h2>What it is for</h2>
<p>Many deadlines are phrased as "within 30 days", "60 days from delivery", "15 working days' notice" or "in 6 months". Counting on a calendar is slow and error-prone, especially across months of different lengths or a leap year. This tool does the counting for you and shows the weekday, so you can see at once whether a deadline lands on a Saturday or Sunday.</p>
<h2>How months and years are counted</h2>
<p>Adding a month means moving to the same day of the following month: 15 March becomes 15 April. If that day does not exist in the target month (for example 31 January + 1 month), the result is the last available day, i.e. 28 or 29 February. The same applies to years: 29 February 2024 + 1 year = 28 February 2025.</p>
<h2>Working days</h2>
<p>With "working days", Saturdays and Sundays are skipped: 10 working days from a Monday lands on the Friday of the following week. Public holidays are not considered, since they vary by country.</p>
<h2>Examples</h2>
<ul>
<li>An invoice payable in 60 days issued on 5 September is due on 4 November.</li>
<li>A 30-day notice given on 20 January runs until 19 February.</li>
<li>A 2-year warranty on a purchase made on 10 June 2026 ends on 10 June 2028.</li>
</ul>
""",
    },
    "faq": {
        "it": [
            ("Che giorno sarà tra 30 giorni?", "Premi la scorciatoia «+30» con la data di oggi come partenza: il risultato mostra la data e il giorno della settimana."),
            ("Cosa succede se il giorno non esiste nel mese di arrivo?", "Il calcolatore usa l'ultimo giorno del mese: 31 gennaio più un mese diventa 28 (o 29) febbraio."),
            ("Posso andare indietro nel tempo?", "Sì: scegli «Sottrai» per sapere, per esempio, quale data era 90 giorni fa."),
        ],
        "en": [
            ("What date is 30 days from today?", "Press the \"+30\" shortcut with today as the start date: the result shows the date and its weekday."),
            ("What if the day doesn't exist in the target month?", "The calculator uses the last day of that month: 31 January plus one month becomes 28 (or 29) February."),
            ("Can I go back in time?", "Yes: choose \"Subtract\" to find, for example, which date it was 90 days ago."),
        ],
    },
}

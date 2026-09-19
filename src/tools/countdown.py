"""«Quanti giorni mancano a…» – generic countdown plus one page per popular event (Natale, Pasqua, …).

Each preset is a full tool page with its own slug, texts, guide and FAQ, so that searches like
«quanti giorni mancano a natale» land on a dedicated page. All pages share the same JS engine.
"""
import json

# ---------------------------------------------------------------------------------------------
# Shared JavaScript (config injected as JSON in __CFG__)
# ---------------------------------------------------------------------------------------------
JS = r"""
var CFG = __CFG__;
var out = RT.$('#out'), main = RT.$('#main'), sub = RT.$('#sub'), tick = RT.$('#tick');
var target = RT.$('#target'), yearSel = RT.$('#year'), dob = RT.$('#dob'), note = RT.$('#note');
var timer = null;
function easter(y) { // Gregorian computus (Meeus/Jones/Butcher)
  var a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25),
      g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4,
      l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451),
      mo = Math.floor((h + l - 7 * m + 114) / 31), da = ((h + l - 7 * m + 114) % 31) + 1;
  return new Date(y, mo - 1, da);
}
function today0() { var n = new Date(); return new Date(n.getFullYear(), n.getMonth(), n.getDate()); }
var YEARLY = { fixed: 1, easter: 1, blackfriday: 1 };
function occ(y) { // the event's date in year y
  if (CFG.type === 'easter') { var d = easter(y); d.setDate(d.getDate() + CFG.off); return d; }
  if (CFG.type === 'blackfriday') { // day after the 4th Thursday of November
    var n1 = new Date(y, 10, 1), thu = 1 + ((4 - n1.getDay() + 7) % 7) + 21; return new Date(y, 10, thu + 1);
  }
  return new Date(y, CFG.m - 1, CFG.d);
}
function pl(n, one, many) { return RT.fmt(n, 0) + ' ' + (n === 1 ? one : many); }
function iso(d) { return d.getFullYear() + '-' + RT.pad(d.getMonth() + 1) + '-' + RT.pad(d.getDate()); }
function workdays(a, b) { var n = 0, c = new Date(a); while (c < b) { var w = c.getDay(); if (w !== 0 && w !== 6) n++; c.setDate(c.getDate() + 1); } return n; }
function fillYears() {
  if (!yearSel) return;
  var t = today0(), y = t.getFullYear(), first = occ(y) >= t ? y : y + 1;
  yearSel.innerHTML = '';
  for (var i = 0; i < 4; i++) { var o = document.createElement('option'); o.value = first + i; o.textContent = first + i; yearSel.appendChild(o); }
}
function getTarget() {
  var t = today0();
  if (YEARLY[CFG.type]) return occ(+yearSel.value);
  if (CFG.type === 'birthday') {
    var b = RT.parseDate(dob.value); if (!b) return null;
    var d = new Date(t.getFullYear(), b.getMonth(), b.getDate());
    if (d < t) d = new Date(t.getFullYear() + 1, b.getMonth(), b.getDate());
    return d;
  }
  return RT.parseDate(target.value);
}
function render() {
  var d = getTarget();
  if (!d) { out.classList.add('hide'); if (timer) { clearInterval(timer); timer = null; } return; }
  var t = today0(), days = RT.daysBetween(t, d);
  var when = RT.weekday(d) + ' ' + RT.date(d);
  if (days === 0) { main.textContent = T.today_msg; }
  else if (days < 0) { main.textContent = pl(-days, T.day_ago, T.days_ago); }
  else { main.textContent = pl(days, T.day, T.days); }
  var extra = '';
  if (CFG.type === 'birthday') { var b = RT.parseDate(dob.value); var age = d.getFullYear() - b.getFullYear(); extra = ' · ' + T.turning.replace('{n}', age); }
  sub.textContent = (days >= 0 ? T.on : T.was) + ' ' + when + extra;
  var w = Math.floor(Math.abs(days) / 7), r = Math.abs(days) % 7;
  RT.$('#wk').textContent = pl(w, T.week, T.weeks) + (r ? ' + ' + pl(r, T.day, T.days) : '');
  RT.$('#hrs').textContent = RT.fmt(Math.abs(days) * 24, 0);
  RT.$('#work').textContent = days > 0 ? RT.fmt(workdays(t, d), 0) : '0';
  var jan1 = new Date(t.getFullYear(), 0, 1);
  RT.$('#since').textContent = RT.fmt(RT.daysBetween(jan1, t) + 1, 0);
  RT.$('#msgcopy').value = (days > 0 ? T.share.replace('{n}', pl(days, T.day, T.days)) : days === 0 ? T.share_today : T.share_past.replace('{n}', pl(-days, T.day, T.days))).replace('{when}', RT.date(d));
  out.classList.remove('hide');
  if (!timer) timer = setInterval(tickFn, 1000);
  tickFn();
}
function tickFn() {
  var d = getTarget(); if (!d) return;
  var now = new Date(), diff = d - now;
  if (diff <= 0) { tick.textContent = ''; return; }
  var s = Math.floor(diff / 1000), dd = Math.floor(s / 86400), hh = Math.floor(s % 86400 / 3600), mm = Math.floor(s % 3600 / 60), ss = s % 60;
  tick.textContent = T.tick.replace('{d}', dd).replace('{h}', RT.pad(hh)).replace('{m}', RT.pad(mm)).replace('{s}', RT.pad(ss));
}
if (YEARLY[CFG.type]) { fillYears(); yearSel.addEventListener('change', render); }
if (CFG.type === 'custom') {
  var t0 = today0(), def = new Date(t0.getFullYear(), CFG.m - 1, CFG.d); if (def < t0) def = new Date(t0.getFullYear() + 1, CFG.m - 1, CFG.d);
  target.value = iso(def);
}
if (CFG.type === 'generic') { var t1 = today0(), x = new Date(t1.getFullYear(), 11, 25); if (x < t1) x = new Date(t1.getFullYear() + 1, 11, 25); target.value = iso(x); }
if (target) target.addEventListener('input', render);
if (target) target.addEventListener('change', render);
if (dob) { dob.addEventListener('input', render); dob.addEventListener('change', render); }
render();
"""

# ---------------------------------------------------------------------------------------------
# Strings shared by every countdown page
# ---------------------------------------------------------------------------------------------
BASE_STRINGS = {
    "it": {
        "target": "Data dell'evento", "year": "Anno", "dob": "La tua data di nascita",
        "day": "giorno", "days": "giorni", "day_ago": "giorno fa", "days_ago": "giorni fa", "week": "settimana", "weeks": "settimane",
        "today_msg": "È oggi! 🎉", "on": "Cade di", "was": "È stato", "turning": "compirai {n} anni",
        "wk": "Settimane e giorni", "hours": "Ore", "work": "Giorni lavorativi (lun–ven)", "since": "Giorno dell'anno di oggi",
        "tick": "{d} giorni, {h} ore, {m} minuti e {s} secondi", "copy_msg": "Copia la frase",
        "share": "Mancano {n} a {event} ({when})", "share_today": "Oggi è {event}!", "share_past": "{event} è stato {n} fa ({when})",
        "others": "Altri conti alla rovescia",
    },
    "en": {
        "target": "Event date", "year": "Year", "dob": "Your date of birth",
        "day": "day", "days": "days", "day_ago": "day ago", "days_ago": "days ago", "week": "week", "weeks": "weeks",
        "today_msg": "It's today! 🎉", "on": "Falls on", "was": "It was", "turning": "you'll turn {n}",
        "wk": "Weeks and days", "hours": "Hours", "work": "Working days (Mon–Fri)", "since": "Today's day of the year",
        "tick": "{d} days, {h} hours, {m} minutes and {s} seconds", "copy_msg": "Copy the sentence",
        "share": "{n} to go until {event} ({when})", "share_today": "Today is {event}!", "share_past": "{event} was {n} ago ({when})",
        "others": "Other countdowns",
    },
}

UI_RESULT = """
<div class="result hide" id="out">
  <div class="big" id="main"></div>
  <div class="sub" id="sub"></div>
  <p class="msg" id="tick" style="font-variant-numeric:tabular-nums"></p>
  <div class="stats">
    <div class="stat"><b id="wk"></b><span>{{wk}}</span></div>
    <div class="stat"><b id="hrs"></b><span>{{hours}}</span></div>
    <div class="stat"><b id="work"></b><span>{{work}}</span></div>
    <div class="stat"><b id="since"></b><span>{{since}}</span></div>
  </div>
  <div class="inline" style="margin-top:12px"><input type="text" id="msgcopy" readonly style="flex:1 1 220px"><button class="btn small" type="button" data-copy="#msgcopy" data-done="{{copied}}">{{copy_msg}}</button></div>
</div>
"""

UI_FIXED = """
<div class="row">
  <div class="field"><label for="year">{{year}}</label><select id="year"></select></div>
</div>
""" + UI_RESULT

UI_CUSTOM = """
<div class="row">
  <div class="field"><label for="target">{{target}}</label><input type="date" id="target"></div>
</div>
""" + UI_RESULT

UI_BIRTHDAY = """
<div class="row">
  <div class="field"><label for="dob">{{dob}}</label><input type="date" id="dob"></div>
</div>
""" + UI_RESULT


# ---------------------------------------------------------------------------------------------
# Presets: one page each
# ---------------------------------------------------------------------------------------------
PRESETS = [
    {
        "id": "countdown_natale", "icon": "🎄", "cfg": {"type": "fixed", "m": 12, "d": 25},
        "slug": {"it": "quanti-giorni-mancano-a-natale", "en": "days-until-christmas"},
        "title": {"it": "Quanti giorni mancano a Natale?", "en": "How many days until Christmas?"},
        "seo_title": {"it": "Quanti giorni mancano a Natale? Countdown al 25 dicembre", "en": "How many days until Christmas? Countdown to 25 December"},
        "event": {"it": "Natale", "en": "Christmas"},
        "short": {"it": "Conto alla rovescia al 25 dicembre, aggiornato al secondo", "en": "Countdown to 25 December, updated every second"},
        "keywords": {"it": ["natale", "conto alla rovescia natale", "quanto manca a natale", "giorni a natale"], "en": ["christmas countdown", "days to christmas", "how long until christmas"]},
        "meta": {
            "it": "Quanti giorni mancano a Natale? Il conto alla rovescia al 25 dicembre aggiornato al secondo: giorni, ore e minuti che mancano, il giorno della settimana in cui cade e i giorni lavorativi che restano per i regali.",
            "en": "How many days until Christmas? Live countdown to 25 December with days, weeks, hours, minutes and seconds, the weekday it falls on and the working days left.",
        },
        "intro": {
            "it": "Natale è il 25 dicembre. Qui sotto trovi quanti giorni mancano esattamente — e quante ore, minuti e secondi — in che giorno della settimana cade e quanti giorni lavorativi restano per regali e spedizioni.",
            "en": "Christmas is on 25 December. Below you'll find exactly how many days are left — and how many hours, minutes and seconds — which weekday it falls on and how many working days are left for presents and deliveries.",
        },
        "article": {
            "it": """
<h2>Quanti giorni mancano al 25 dicembre?</h2>
<p>Il numero grande in cima alla pagina è la risposta: i giorni interi che separano oggi dal <strong>25 dicembre</strong>, oggi escluso. Se Natale è già passato, il conteggio salta automaticamente al Natale dell'anno prossimo; con il menu «Anno» puoi guardare anche più avanti, per esempio per sapere in che giorno della settimana cadrà il Natale tra due anni.</p>
<h2>Tra quante ore è Natale?</h2>
<p>Sotto ai giorni scorre la riga con <strong>ore, minuti e secondi</strong>, che si aggiorna da sola e arriva alla mezzanotte con cui inizia il 25 dicembre. Usa l'orologio del tuo dispositivo, quindi il conteggio è quello del posto in cui sei.</p>
<h2>Natale cade sempre lo stesso giorno?</h2>
<p>Sì: il 25 dicembre è una data fissa, quindi cambia solo il giorno della settimana. Il 24 dicembre è la Vigilia, il 26 è Santo Stefano (festivo in Italia) e il 6 gennaio l'Epifania chiude le feste. Per le vacanze scolastiche di Natale, di solito dal 23 dicembre al 6 gennaio, controlla il calendario della tua regione. Subito dopo arrivano <a href="../quanti-giorni-mancano-a-capodanno/">Capodanno</a> e <a href="../quanti-giorni-mancano-alla-befana/">la Befana</a>; per una data qualsiasi c'è il <a href="../quanti-giorni-mancano/">conto alla rovescia libero</a>.</p>
<h2>A cosa serve sapere quanti giorni mancano</h2>
<ul>
<li><strong>Regali e spedizioni:</strong> i giorni lavorativi mostrati nel riquadro sono quelli utili per consegne e uffici.</li>
<li><strong>Calendario dell'Avvento:</strong> parte il 1° dicembre: se mancano più di 24 giorni, l'Avvento non è ancora iniziato.</li>
<li><strong>Organizzazione:</strong> viaggi, cena, addobbi: copia la frase con il conteggio e mandala in chat per mettere fretta a tutti.</li>
</ul>
""",
            "en": """
<h2>How many days until 25 December?</h2>
<p>The big number at the top of the page is the answer: the whole days between today and <strong>25 December</strong>, today excluded. Once Christmas has passed, the count automatically moves to next year's Christmas; with the "Year" menu you can look further ahead, for instance to see which weekday Christmas falls on in two years.</p>
<h2>How many hours until Christmas?</h2>
<p>Under the days runs the line with <strong>hours, minutes and seconds</strong>, which updates on its own and ends at the midnight that starts 25 December. It uses your device's clock, so the count matches wherever you are.</p>
<h2>Does Christmas always fall on the same date?</h2>
<p>Yes: 25 December is a fixed date, so only the weekday changes. 24 December is Christmas Eve, 26 December is Boxing Day (St Stephen's Day) and 6 January, Epiphany, closes the holiday season. Right after come <a href="../days-until-new-year/">New Year</a> and <a href="../days-until-epiphany/">Epiphany</a>; for any other date there is the <a href="../days-until/">free countdown</a>.</p>
<h2>Why the number matters</h2>
<ul>
<li><strong>Gifts and deliveries:</strong> the working days in the box are the ones that count for shipping and offices.</li>
<li><strong>Advent calendar:</strong> it starts on 1 December: if more than 24 days are left, Advent hasn't begun yet.</li>
<li><strong>Planning:</strong> trips, dinner, decorations: copy the sentence with the count and send it to the family chat.</li>
</ul>
""",
        },
        "faq": {
            "it": [
                ("Quanti giorni mancano al 25 dicembre?", "Sono i giorni interi che separano oggi da Natale: li trovi nel numero grande in cima alla pagina, aggiornato ogni giorno. Se il 25 dicembre è già passato, il conteggio salta da solo all'anno prossimo."),
                ("Tra quante ore è Natale?", "La riga sotto al conteggio dei giorni mostra ore, minuti e secondi che mancano e scorre in tempo reale fino alla mezzanotte con cui inizia il 25 dicembre."),
                ("Il conteggio include il giorno di Natale?", "No: mostra i giorni interi che mancano. Il 24 dicembre il risultato è «1 giorno», il 25 dicembre diventa «È oggi!»."),
                ("Che giorno della settimana sarà Natale?", "Lo leggi sotto il numero grande, insieme alla data completa. Scegli un altro anno dal menu per vedere gli anni successivi."),
                ("Quanti giorni lavorativi mancano?", "Il riquadro «Giorni lavorativi» conta solo i giorni da lunedì a venerdì, senza togliere le festività: l'8 dicembre, se cade in settimana, va sottratto a mano."),
            ],
            "en": [
                ("How many days until 25 December?", "The whole days between today and Christmas: you'll find them in the big number at the top of the page. Once 25 December has passed, the count moves to next year by itself."),
                ("How many hours until Christmas?", "The line under the days shows the hours, minutes and seconds left and runs in real time until the midnight that starts 25 December."),
                ("Does the count include Christmas Day?", "No: it shows the whole days left. On 24 December the result is \"1 day\"; on 25 December it becomes \"It's today!\"."),
                ("Which weekday will Christmas be?", "You can read it under the big number, together with the full date. Pick another year from the menu to see the following years."),
                ("How many working days are left?", "The \"Working days\" box counts Monday to Friday only, without removing public holidays."),
            ],
        },
    },
    {
        "id": "countdown_capodanno", "icon": "🎆", "cfg": {"type": "fixed", "m": 1, "d": 1},
        "slug": {"it": "quanti-giorni-mancano-a-capodanno", "en": "days-until-new-year"},
        "title": {"it": "Quanti giorni mancano a Capodanno?", "en": "How many days until New Year?"},
        "event": {"it": "Capodanno", "en": "New Year's Day"},
        "short": {"it": "Conto alla rovescia al 1° gennaio e alla fine dell'anno", "en": "Countdown to 1 January and to the end of the year"},
        "keywords": {"it": ["capodanno", "fine anno", "quanto manca a capodanno", "conto alla rovescia anno nuovo"], "en": ["new year countdown", "days until new year", "end of year"]},
        "meta": {
            "it": "Quanti giorni mancano a Capodanno? Conto alla rovescia al 1° gennaio con giorni, settimane, ore, minuti e secondi, più i giorni che restano dell'anno in corso.",
            "en": "How many days until New Year? Countdown to 1 January with days, weeks, hours, minutes and seconds, plus the days left in the current year.",
        },
        "intro": {
            "it": "Conta i giorni che mancano alla mezzanotte del 31 dicembre: il risultato è anche il numero di giorni che restano dell'anno in corso.",
            "en": "Counts the days left until midnight on 31 December: the result is also the number of days remaining in the current year.",
        },
        "article": {
            "it": """
<h2>Giorni a Capodanno = giorni che restano dell'anno</h2>
<p>Il 1° gennaio è il primo giorno dell'anno nuovo, quindi i giorni che mancano a Capodanno sono esattamente i giorni che restano dell'anno in corso, oggi escluso. Il riquadro «Giorno dell'anno di oggi» ti dice a che punto sei: il 1° gennaio è il giorno 1, il 31 dicembre è il 365 (366 negli anni bisestili).</p>
<h2>Quando finisce l'anno, precisamente</h2>
<p>Il cambio d'anno avviene alla mezzanotte tra il 31 dicembre e il 1° gennaio, ora locale: la riga con ore, minuti e secondi conta fino a quel momento. In Italia il 1° gennaio è festivo; il 31 dicembre è un giorno lavorativo normale, anche se molti uffici chiudono prima.</p>
<h2>Idee per usare il conteggio</h2>
<ul>
<li><strong>Obiettivi dell'anno:</strong> quanti giorni hai ancora per chiudere i buoni propositi.</li>
<li><strong>Scadenze fiscali e lavorative:</strong> molte scadono il 31 dicembre: guarda i giorni lavorativi.</li>
<li><strong>Festa di Capodanno:</strong> copia la frase con il conto alla rovescia e condividila con gli invitati.</li>
</ul>
""",
            "en": """
<h2>Days to New Year = days left in the year</h2>
<p>1 January is the first day of the new year, so the days left until New Year's Day are exactly the days remaining in the current year, today excluded. The "Today's day of the year" box shows where you are: 1 January is day 1, 31 December is day 365 (366 in leap years).</p>
<h2>When exactly the year ends</h2>
<p>The year changes at midnight between 31 December and 1 January, local time: the line with hours, minutes and seconds counts down to that moment. 1 January is a public holiday in most countries; 31 December is usually a normal working day, although many offices close early.</p>
<h2>Ways to use the count</h2>
<ul>
<li><strong>Yearly goals:</strong> how many days you still have to finish your resolutions.</li>
<li><strong>Deadlines:</strong> many tax and work deadlines fall on 31 December: check the working days.</li>
<li><strong>New Year's Eve party:</strong> copy the countdown sentence and share it with your guests.</li>
</ul>
""",
        },
        "faq": {
            "it": [
                ("Il 31 dicembre quanti giorni mancano?", "Uno: il calcolatore conta i giorni interi fino al 1° gennaio. La riga sotto mostra le ore, i minuti e i secondi che mancano alla mezzanotte."),
                ("Quanti giorni ha l'anno in corso?", "365, oppure 366 se è bisestile (divisibile per 4, tranne i secoli non divisibili per 400). Il prossimo anno bisestile è il 2028."),
                ("Posso vedere Capodanno di un altro anno?", "Sì, scegli l'anno dal menu: il calcolatore mostra il giorno della settimana e i giorni mancanti."),
            ],
            "en": [
                ("How many days are left on 31 December?", "One: the calculator counts whole days until 1 January. The line below shows the hours, minutes and seconds left until midnight."),
                ("How many days does the current year have?", "365, or 366 in a leap year (divisible by 4, except centuries not divisible by 400). The next leap year is 2028."),
                ("Can I see New Year's Day of another year?", "Yes, pick the year from the menu: the calculator shows the weekday and the days left."),
            ],
        },
    },
    {
        "id": "countdown_befana", "icon": "🧹", "cfg": {"type": "fixed", "m": 1, "d": 6},
        "slug": {"it": "quanti-giorni-mancano-alla-befana", "en": "days-until-epiphany"},
        "title": {"it": "Quanti giorni mancano alla Befana?", "en": "How many days until Epiphany?"},
        "event": {"it": "la Befana", "en": "Epiphany"},
        "short": {"it": "Conto alla rovescia al 6 gennaio, l'Epifania", "en": "Countdown to 6 January, the Epiphany"},
        "keywords": {"it": ["befana", "epifania", "6 gennaio", "quanto manca alla befana"], "en": ["epiphany", "6 january", "twelfth night"]},
        "meta": {
            "it": "Quanti giorni mancano alla Befana? Conto alla rovescia al 6 gennaio (Epifania) con giorni, settimane, ore e minuti, e il giorno della settimana in cui cade.",
            "en": "How many days until Epiphany? Countdown to 6 January with days, weeks, hours and minutes, and the weekday it falls on.",
        },
        "intro": {
            "it": "L'Epifania, cioè la Befana, è il 6 gennaio: qui vedi quanti giorni mancano e in che giorno della settimana cade.",
            "en": "Epiphany – in Italy the day of the Befana – is on 6 January: see how many days are left and which weekday it falls on.",
        },
        "article": {
            "it": """
<h2>La Befana chiude le feste</h2>
<p>Il 6 gennaio, festa dell'Epifania, è l'ultimo giorno festivo delle vacanze di Natale: «l'Epifania tutte le feste porta via». In Italia è giorno festivo a tutti gli effetti, quindi negozi e uffici seguono l'orario domenicale e le scuole riaprono nei giorni successivi (di solito il 7 gennaio o il primo giorno feriale utile).</p>
<h2>Come si usa il conto alla rovescia</h2>
<p>Il numero grande sono i giorni interi che mancano al 6 gennaio; se la Befana è già passata, il conteggio va all'anno prossimo. Scegli un altro anno dal menu per sapere in anticipo se il 6 gennaio cadrà in un giorno feriale o nel weekend, utile per organizzare le ferie del «ponte».</p>
<h2>Calze e regali dell'ultimo minuto</h2>
<p>I giorni lavorativi che restano ti dicono quanto tempo hai per le spedizioni. Le calze si preparano la sera del 5 gennaio: il conteggio del 5 mostra «1 giorno».</p>
""",
            "en": """
<h2>Epiphany closes the holiday season</h2>
<p>6 January, the feast of the Epiphany, is the last day of the Christmas holidays in many countries. In Italy it is a full public holiday, when the Befana – a kindly old witch – fills children's stockings with sweets, and schools reopen on the following working day.</p>
<h2>How to use the countdown</h2>
<p>The big number is the whole days left until 6 January; once Epiphany has passed, the count moves to next year. Pick another year from the menu to know in advance whether 6 January will fall on a weekday or at the weekend.</p>
<h2>Last-minute stockings</h2>
<p>The working days shown tell you how much time is left for deliveries. Stockings are prepared on the evening of 5 January: on that day the count shows "1 day".</p>
""",
        },
        "faq": {
            "it": [
                ("La Befana è festivo in Italia?", "Sì, il 6 gennaio è una festività nazionale: scuole, uffici pubblici e la maggior parte dei negozi sono chiusi."),
                ("Quando riaprono le scuole dopo la Befana?", "Di solito il primo giorno feriale dopo il 6 gennaio, ma dipende dal calendario scolastico regionale."),
                ("Perché si dice che la Befana porta via le feste?", "Perché l'Epifania è l'ultima festività del periodo natalizio iniziato l'8 dicembre: dal 7 gennaio si torna alla normalità."),
            ],
            "en": [
                ("Is Epiphany a public holiday?", "In Italy, Spain, Austria and several other countries yes; elsewhere it is a religious feast on a normal working day."),
                ("What is the Befana?", "An Italian folk figure: an old woman who flies on a broom on the night of 5 January and leaves sweets (or coal) in children's stockings."),
                ("Why is it called Twelfth Night?", "Because 6 January is the twelfth day after Christmas and traditionally ends the Christmas season."),
            ],
        },
    },
    {
        "id": "countdown_san_valentino", "icon": "💘", "cfg": {"type": "fixed", "m": 2, "d": 14},
        "slug": {"it": "quanti-giorni-mancano-a-san-valentino", "en": "days-until-valentines-day"},
        "title": {"it": "Quanti giorni mancano a San Valentino?", "en": "How many days until Valentine's Day?"},
        "event": {"it": "San Valentino", "en": "Valentine's Day"},
        "short": {"it": "Conto alla rovescia al 14 febbraio", "en": "Countdown to 14 February"},
        "keywords": {"it": ["san valentino", "14 febbraio", "festa degli innamorati", "quanto manca a san valentino"], "en": ["valentine's day countdown", "14 february", "valentines"]},
        "meta": {
            "it": "Quanti giorni mancano a San Valentino? Conto alla rovescia al 14 febbraio con giorni, settimane, ore e minuti, e il giorno della settimana in cui cade la festa degli innamorati.",
            "en": "How many days until Valentine's Day? Countdown to 14 February with days, weeks, hours and minutes, and the weekday it falls on.",
        },
        "intro": {
            "it": "Conta i giorni che mancano al 14 febbraio, la festa degli innamorati, e scopri in che giorno della settimana cade quest'anno.",
            "en": "Counts the days left until 14 February and shows which weekday Valentine's Day falls on this year.",
        },
        "article": {
            "it": """
<h2>Il conto alla rovescia a San Valentino</h2>
<p>San Valentino è sempre il 14 febbraio, quindi il calcolatore ti dice i giorni interi che mancano e il giorno della settimana: se cade nel weekend è più facile organizzare una cena o un viaggio, se cade in settimana meglio prenotare per tempo. Dopo il 14 febbraio il conteggio passa all'anno successivo.</p>
<h2>Quando prenotare e ordinare</h2>
<ul>
<li><strong>Ristoranti:</strong> i tavoli migliori si esauriscono 2–3 settimane prima.</li>
<li><strong>Regali online:</strong> guarda i giorni lavorativi: sono quelli utili per le consegne.</li>
<li><strong>Fiori:</strong> ordinali qualche giorno prima; il 14 i prezzi salgono.</li>
</ul>
<h2>Non è l'unica festa degli innamorati</h2>
<p>In alcune regioni si festeggia anche il 12 giugno (Dia dos Namorados, in Brasile) o il 14 marzo (White Day, in Giappone). Con lo strumento generico «Quanti giorni mancano a una data» puoi contare i giorni a qualsiasi data.</p>
""",
            "en": """
<h2>The Valentine's Day countdown</h2>
<p>Valentine's Day is always on 14 February, so the calculator tells you the whole days left and the weekday: at the weekend a dinner or a trip is easier to organise, on a weekday it's better to book early. After 14 February the count moves to next year.</p>
<h2>When to book and order</h2>
<ul>
<li><strong>Restaurants:</strong> the best tables go 2–3 weeks in advance.</li>
<li><strong>Online gifts:</strong> check the working days: those are the ones that count for deliveries.</li>
<li><strong>Flowers:</strong> order a few days ahead; prices rise on the 14th.</li>
</ul>
<h2>Other dates for lovers</h2>
<p>Some countries celebrate on other days too, such as 12 June (Dia dos Namorados in Brazil) or 14 March (White Day in Japan). With the generic "Days until a date" tool you can count down to any date.</p>
""",
        },
        "faq": {
            "it": [
                ("San Valentino cade sempre il 14 febbraio?", "Sì, la data è fissa; cambia solo il giorno della settimana, che leggi sotto il numero grande."),
                ("Il 14 febbraio è festivo?", "No, in Italia è un giorno lavorativo normale."),
                ("Posso vedere quando cadrà l'anno prossimo?", "Sì, scegli l'anno dal menu in alto."),
            ],
            "en": [
                ("Is Valentine's Day always on 14 February?", "Yes, the date is fixed; only the weekday changes, and you can read it under the big number."),
                ("Is 14 February a public holiday?", "No, it is a normal working day almost everywhere."),
                ("Can I see when it falls next year?", "Yes, pick the year from the menu at the top."),
            ],
        },
    },
    {
        "id": "countdown_carnevale", "icon": "🎭", "cfg": {"type": "easter", "off": -47},
        "slug": {"it": "quanti-giorni-mancano-a-carnevale", "en": "days-until-carnival"},
        "title": {"it": "Quanti giorni mancano a Carnevale?", "en": "How many days until Carnival (Mardi Gras)?"},
        "event": {"it": "Carnevale (martedì grasso)", "en": "Mardi Gras"},
        "short": {"it": "Conto alla rovescia al martedì grasso, calcolato dalla Pasqua", "en": "Countdown to Shrove Tuesday, worked out from Easter"},
        "keywords": {"it": ["carnevale", "martedì grasso", "giovedì grasso", "quando è carnevale", "date carnevale"], "en": ["carnival", "mardi gras", "shrove tuesday", "pancake day", "when is carnival"]},
        "meta": {
            "it": "Quanti giorni mancano a Carnevale? Data del martedì grasso di quest'anno e dei prossimi (dipende dalla Pasqua), con giorni, settimane e ore che mancano, più giovedì grasso e mercoledì delle Ceneri.",
            "en": "How many days until Carnival? This year's and the next years' Mardi Gras date (it depends on Easter), with the days, weeks and hours left.",
        },
        "intro": {
            "it": "Carnevale non ha una data fissa: il martedì grasso cade 47 giorni prima di Pasqua. Qui vedi la data di quest'anno e dei prossimi, con il conto alla rovescia.",
            "en": "Carnival has no fixed date: Shrove Tuesday falls 47 days before Easter. Here you see this year's and the next years' date, with a live countdown.",
        },
        "article": {
            "it": """
<h2>Quando è Carnevale: la regola</h2>
<p>Il martedì grasso, ultimo giorno di Carnevale, cade <strong>47 giorni prima della domenica di Pasqua</strong>; il giorno dopo è il mercoledì delle Ceneri, inizio della Quaresima. Poiché la Pasqua si sposta tra il 22 marzo e il 25 aprile, il martedì grasso può cadere tra il 3 febbraio e il 9 marzo. Il calcolatore calcola la Pasqua con l'algoritmo del calendario gregoriano e da lì il martedì grasso, quindi non serve aggiornarlo di anno in anno.</p>
<h2>Le altre date del Carnevale</h2>
<ul>
<li><strong>Giovedì grasso:</strong> 5 giorni prima del martedì grasso (52 giorni prima di Pasqua), l'inizio della settimana di festa in molte città.</li>
<li><strong>Domenica di Carnevale:</strong> 2 giorni prima del martedì grasso.</li>
<li><strong>Carnevale ambrosiano (Milano e diocesi):</strong> finisce il sabato dopo le Ceneri, 4 giorni dopo il martedì grasso.</li>
</ul>
<h2>Sfilate e vacanze</h2>
<p>I carnevali di Venezia, Viareggio, Ivrea, Putignano e Cento organizzano le sfilate nei weekend precedenti: con il menu «Anno» puoi conoscere le date con anni di anticipo. Alcune regioni concedono uno o due giorni di vacanza scolastica intorno al martedì grasso: controlla il calendario regionale.</p>
""",
            "en": """
<h2>When Carnival is: the rule</h2>
<p>Shrove Tuesday (Mardi Gras), the last day of Carnival, falls <strong>47 days before Easter Sunday</strong>; the next day is Ash Wednesday, the start of Lent. Because Easter moves between 22 March and 25 April, Mardi Gras can fall anywhere between 3 February and 9 March. The calculator computes Easter with the Gregorian calendar algorithm and derives Mardi Gras from it, so it never needs updating.</p>
<h2>Other Carnival dates</h2>
<ul>
<li><strong>Fat Thursday:</strong> 5 days before Shrove Tuesday (52 days before Easter), the start of the festive week in many cities.</li>
<li><strong>Carnival Sunday:</strong> 2 days before Shrove Tuesday.</li>
<li><strong>Pancake Day:</strong> the British name for Shrove Tuesday.</li>
</ul>
<h2>Parades and holidays</h2>
<p>Venice, Rio, New Orleans, Cologne and Viareggio hold their parades in the weekends before Shrove Tuesday: with the "Year" menu you can find the dates years in advance.</p>
""",
        },
        "faq": {
            "it": [
                ("Perché Carnevale cambia data ogni anno?", "Perché dipende dalla Pasqua, che è la prima domenica dopo la prima luna piena di primavera. Il martedì grasso è 47 giorni prima."),
                ("Quando è giovedì grasso?", "Cinque giorni prima del martedì grasso mostrato dal calcolatore."),
                ("Il Carnevale ambrosiano quando finisce?", "Il sabato successivo al mercoledì delle Ceneri, cioè quattro giorni dopo il martedì grasso: vale per Milano e le parrocchie di rito ambrosiano."),
            ],
            "en": [
                ("Why does Carnival change date every year?", "Because it depends on Easter, the first Sunday after the first full moon of spring. Shrove Tuesday is 47 days earlier."),
                ("When is Fat Thursday?", "Five days before the Shrove Tuesday shown by the calculator."),
                ("Is Mardi Gras a public holiday?", "In a few places (for example Louisiana, Rio de Janeiro and some German cities) yes; in most countries it is a normal day."),
            ],
        },
    },
    {
        "id": "countdown_pasqua", "icon": "🐣", "cfg": {"type": "easter", "off": 0},
        "slug": {"it": "quanti-giorni-mancano-a-pasqua", "en": "days-until-easter"},
        "title": {"it": "Quanti giorni mancano a Pasqua?", "en": "How many days until Easter?"},
        "event": {"it": "Pasqua", "en": "Easter"},
        "short": {"it": "Data di Pasqua di quest'anno e dei prossimi, con conto alla rovescia", "en": "This year's and the next years' Easter date, with a countdown"},
        "keywords": {"it": ["pasqua", "quando è pasqua", "data pasqua", "pasquetta", "quanto manca a pasqua"], "en": ["easter countdown", "when is easter", "easter date", "easter monday"]},
        "meta": {
            "it": "Quanti giorni mancano a Pasqua? Data della Pasqua di quest'anno e degli anni prossimi calcolata con l'algoritmo ufficiale, con giorni, settimane e ore che mancano, Pasquetta e Venerdì Santo.",
            "en": "How many days until Easter? This year's and the next years' Easter date calculated with the official algorithm, with the days, weeks and hours left, Easter Monday and Good Friday.",
        },
        "intro": {
            "it": "Pasqua cambia data ogni anno: il calcolatore la trova con la regola del calendario e conta i giorni che mancano. Pasquetta è il giorno dopo.",
            "en": "Easter changes date every year: the calculator finds it with the calendar rule and counts the days left. Easter Monday is the day after.",
        },
        "article": {
            "it": """
<h2>Come si calcola la data di Pasqua</h2>
<p>La Pasqua cristiana cade la <strong>prima domenica dopo la prima luna piena di primavera</strong> (dopo il 21 marzo), quindi tra il 22 marzo e il 25 aprile. La data si ottiene con un calcolo astronomico-calendariale fissato nel 1582 con il calendario gregoriano; il calcolatore usa lo stesso algoritmo (detto di Gauss o di Meeus), perciò è esatto per qualsiasi anno.</p>
<h2>I giorni intorno a Pasqua</h2>
<ul>
<li><strong>Venerdì Santo:</strong> 2 giorni prima (non festivo in Italia).</li>
<li><strong>Pasquetta (lunedì dell'Angelo):</strong> il giorno dopo, festivo in Italia.</li>
<li><strong>Vacanze scolastiche:</strong> di solito dal giovedì prima al martedì dopo Pasqua, secondo il calendario regionale.</li>
<li><strong>Carnevale:</strong> il martedì grasso è 47 giorni prima; la Quaresima inizia il mercoledì successivo.</li>
</ul>
<h2>Pasqua ortodossa</h2>
<p>Le Chiese ortodosse seguono il calendario giuliano e la loro Pasqua cade spesso una o più settimane dopo; il calcolatore mostra la data della Pasqua cattolica e protestante.</p>
""",
            "en": """
<h2>How the Easter date is worked out</h2>
<p>Western Easter falls on the <strong>first Sunday after the first full moon of spring</strong> (after 21 March), so between 22 March and 25 April. The date comes from a calendar rule fixed in 1582 with the Gregorian calendar; the calculator uses the same algorithm (Gauss / Meeus), so it is exact for any year.</p>
<h2>The days around Easter</h2>
<ul>
<li><strong>Good Friday:</strong> 2 days before (a public holiday in the UK, Germany and many other countries).</li>
<li><strong>Easter Monday:</strong> the day after, a public holiday in most of Europe.</li>
<li><strong>Carnival:</strong> Shrove Tuesday is 47 days earlier; Lent starts the next day.</li>
</ul>
<h2>Orthodox Easter</h2>
<p>Orthodox churches follow the Julian calendar and their Easter often falls one or more weeks later; the calculator shows the Western (Catholic and Protestant) date.</p>
""",
        },
        "faq": {
            "it": [
                ("Quando è Pasquetta?", "Il lunedì subito dopo la domenica di Pasqua mostrata dal calcolatore. In Italia è festivo."),
                ("Perché Pasqua non ha una data fissa?", "Perché è legata alla luna piena di primavera, che cade in giorni diversi ogni anno: per questo oscilla tra il 22 marzo e il 25 aprile."),
                ("La data è affidabile anche per gli anni futuri?", "Sì: il calcolo usa l'algoritmo ufficiale del calendario gregoriano, valido per qualsiasi anno."),
            ],
            "en": [
                ("When is Easter Monday?", "The Monday right after the Easter Sunday shown by the calculator."),
                ("Why doesn't Easter have a fixed date?", "Because it is tied to the spring full moon, which falls on different days each year: that is why it moves between 22 March and 25 April."),
                ("Is the date reliable for future years too?", "Yes: the calculation uses the official Gregorian calendar algorithm, valid for any year."),
            ],
        },
    },
    {
        "id": "countdown_estate", "icon": "☀️", "cfg": {"type": "fixed", "m": 6, "d": 21},
        "slug": {"it": "quanti-giorni-mancano-all-estate", "en": "days-until-summer"},
        "title": {"it": "Quanti giorni mancano all'estate?", "en": "How many days until summer?"},
        "event": {"it": "l'estate", "en": "summer"},
        "short": {"it": "Conto alla rovescia al 21 giugno, inizio dell'estate", "en": "Countdown to 21 June, the start of summer"},
        "keywords": {"it": ["estate", "inizio estate", "solstizio", "quanto manca all'estate", "vacanze estive"], "en": ["summer countdown", "first day of summer", "solstice"]},
        "meta": {
            "it": "Quanti giorni mancano all'estate? Conto alla rovescia al 21 giugno, inizio dell'estate astronomica, con giorni, settimane e ore che mancano. Per l'estate meteorologica conta dal 1° giugno.",
            "en": "How many days until summer? Countdown to 21 June, the start of astronomical summer, with the days, weeks and hours left. Meteorological summer starts on 1 June.",
        },
        "intro": {
            "it": "L'estate astronomica inizia con il solstizio, il 21 giugno (a volte il 20). Qui conti i giorni che mancano e scopri in che giorno della settimana cade.",
            "en": "Astronomical summer starts with the solstice on 21 June (sometimes the 20th). Count the days left and see which weekday it falls on.",
        },
        "article": {
            "it": """
<h2>Quando inizia l'estate</h2>
<p>Ci sono due date «ufficiali». L'<strong>estate astronomica</strong> inizia con il solstizio, che nell'emisfero nord cade il 21 giugno (in alcuni anni il 20) e dura fino all'equinozio del 22–23 settembre. L'<strong>estate meteorologica</strong>, usata dai servizi meteo, va dal 1° giugno al 31 agosto. Il calcolatore conta fino al 21 giugno; se ti interessa il 1° giugno, usa lo strumento generico «Quanti giorni mancano a una data».</p>
<h2>Le altre date dell'estate</h2>
<ul>
<li><strong>Fine della scuola:</strong> tra il 6 e il 10 giugno secondo la regione (pagina dedicata «Quanti giorni mancano alla fine della scuola»).</li>
<li><strong>Ferragosto:</strong> 15 agosto, cuore delle vacanze italiane.</li>
<li><strong>Fine dell'estate:</strong> equinozio d'autunno, 22 o 23 settembre.</li>
</ul>
<h2>Perché il solstizio cambia giorno</h2>
<p>L'anno solare dura circa 365 giorni e 6 ore: gli anni bisestili riallineano il calendario, e per questo il solstizio oscilla tra il 20 e il 21 giugno. Per il conto alla rovescia la differenza di un giorno è trascurabile.</p>
""",
            "en": """
<h2>When summer starts</h2>
<p>There are two "official" dates. <strong>Astronomical summer</strong> begins with the solstice, which in the northern hemisphere falls on 21 June (in some years the 20th) and lasts until the equinox on 22–23 September. <strong>Meteorological summer</strong>, used by weather services, runs from 1 June to 31 August. The calculator counts down to 21 June; for 1 June use the generic "Days until a date" tool.</p>
<h2>Other summer dates</h2>
<ul>
<li><strong>Last day of school:</strong> varies by country and region (see the dedicated page).</li>
<li><strong>Midsummer:</strong> 24 June in many European countries.</li>
<li><strong>End of summer:</strong> the autumn equinox, 22 or 23 September.</li>
</ul>
<h2>Why the solstice moves</h2>
<p>The solar year lasts about 365 days and 6 hours: leap years realign the calendar, which is why the solstice drifts between 20 and 21 June. For a countdown the one-day difference hardly matters.</p>
""",
        },
        "faq": {
            "it": [
                ("L'estate inizia il 21 giugno o il 1° giugno?", "Il 21 giugno per l'astronomia (solstizio), il 1° giugno per la meteorologia. Il calcolatore usa il 21 giugno."),
                ("E nell'emisfero sud?", "Le stagioni sono invertite: lì l'estate inizia intorno al 21 dicembre."),
                ("Posso contare i giorni alle mie vacanze?", "Sì, con lo strumento «Quanti giorni mancano a una data» inserisci la data di partenza."),
            ],
            "en": [
                ("Does summer start on 21 June or 1 June?", "21 June astronomically (the solstice), 1 June meteorologically. The calculator uses 21 June."),
                ("What about the southern hemisphere?", "Seasons are reversed: there summer starts around 21 December."),
                ("Can I count the days to my holiday?", "Yes, use the generic \"Days until a date\" tool with your departure date."),
            ],
        },
    },
    {
        "id": "countdown_ferragosto", "icon": "🏖️", "cfg": {"type": "fixed", "m": 8, "d": 15},
        "slug": {"it": "quanti-giorni-mancano-a-ferragosto", "en": "days-until-ferragosto"},
        "title": {"it": "Quanti giorni mancano a Ferragosto?", "en": "How many days until Ferragosto (15 August)?"},
        "event": {"it": "Ferragosto", "en": "Ferragosto"},
        "short": {"it": "Conto alla rovescia al 15 agosto", "en": "Countdown to 15 August, Italy's midsummer holiday"},
        "keywords": {"it": ["ferragosto", "15 agosto", "quanto manca a ferragosto", "vacanze agosto"], "en": ["ferragosto", "15 august", "assumption day", "italian holiday"]},
        "meta": {
            "it": "Quanti giorni mancano a Ferragosto? Conto alla rovescia al 15 agosto con giorni, settimane, ore e minuti, e il giorno della settimana in cui cade.",
            "en": "How many days until Ferragosto? Countdown to 15 August, Italy's summer holiday (Assumption Day), with days, weeks, hours and the weekday it falls on.",
        },
        "intro": {
            "it": "Il 15 agosto è la festa più attesa dell'estate italiana: qui conti i giorni che mancano e vedi se quest'anno cade in settimana o nel weekend.",
            "en": "15 August is the most awaited holiday of the Italian summer: count the days left and see whether it falls on a weekday or at the weekend this year.",
        },
        "article": {
            "it": """
<h2>Ferragosto, il 15 agosto</h2>
<p>Ferragosto è una data fissa: il 15 agosto, festa dell'Assunzione e giorno festivo nazionale. Il nome viene dalle <em>Feriae Augusti</em>, le feste istituite dall'imperatore Augusto nel 18 a.C. Il calcolatore conta i giorni interi che mancano e ti dice il giorno della settimana: quando cade di martedì o giovedì, molti fanno il «ponte».</p>
<h2>Come organizzarsi</h2>
<ul>
<li><strong>Prenotazioni:</strong> spiagge, ristoranti e traghetti si riempiono settimane prima: i giorni lavorativi mostrati sono quelli utili per gli uffici.</li>
<li><strong>Chiusure:</strong> molte aziende chiudono nella settimana di Ferragosto; negozi e uffici pubblici seguono l'orario festivo il 15.</li>
<li><strong>Traffico:</strong> i giorni da bollino nero sono di solito il weekend prima e quello dopo.</li>
</ul>
<h2>E dopo Ferragosto?</h2>
<p>Per molti segna il giro di boa dell'estate: la scuola riprende a metà settembre (pagina «Quanti giorni mancano all'inizio della scuola») e l'estate astronomica finisce il 22–23 settembre.</p>
""",
            "en": """
<h2>Ferragosto, 15 August</h2>
<p>Ferragosto is a fixed date: 15 August, the feast of the Assumption and a national public holiday in Italy. The name comes from the <em>Feriae Augusti</em>, the festivities established by Emperor Augustus in 18 BC. The calculator counts the whole days left and tells you the weekday: when it falls on a Tuesday or Thursday, many Italians take a long weekend.</p>
<h2>Planning ahead</h2>
<ul>
<li><strong>Bookings:</strong> beaches, restaurants and ferries fill up weeks before: the working days shown are the ones offices are open.</li>
<li><strong>Closures:</strong> many businesses close for the whole week; shops and public offices keep holiday hours on the 15th.</li>
<li><strong>Traffic:</strong> the busiest days on Italian motorways are usually the weekend before and the one after.</li>
</ul>
<h2>After Ferragosto</h2>
<p>For many it marks the turning point of summer: schools reopen in mid-September and astronomical summer ends on 22–23 September.</p>
""",
        },
        "faq": {
            "it": [
                ("Ferragosto è festivo?", "Sì, il 15 agosto è festa nazionale in Italia: scuole, uffici e la maggior parte dei negozi sono chiusi."),
                ("Perché si chiama Ferragosto?", "Dal latino Feriae Augusti, «riposo di Augusto»: le feste dell'antica Roma nel mese dedicato all'imperatore."),
                ("Quando cade Ferragosto l'anno prossimo?", "Scegli l'anno dal menu: il calcolatore mostra il giorno della settimana e i giorni che mancano."),
            ],
            "en": [
                ("Is Ferragosto a public holiday?", "Yes, 15 August is a national holiday in Italy (and Assumption Day is a holiday in several other Catholic countries)."),
                ("Where does the name come from?", "From the Latin Feriae Augusti, \"Augustus' rest\": the ancient Roman festivities in the month named after the emperor."),
                ("When does Ferragosto fall next year?", "Pick the year from the menu: the calculator shows the weekday and the days left."),
            ],
        },
    },
    {
        "id": "countdown_halloween", "icon": "🎃", "cfg": {"type": "fixed", "m": 10, "d": 31},
        "slug": {"it": "quanti-giorni-mancano-a-halloween", "en": "days-until-halloween"},
        "title": {"it": "Quanti giorni mancano a Halloween?", "en": "How many days until Halloween?"},
        "seo_title": {"it": "Quanti giorni mancano a Halloween? Conto alla rovescia", "en": "How many days until Halloween? Live countdown"},
        "event": {"it": "Halloween", "en": "Halloween"},
        "short": {"it": "Conto alla rovescia al 31 ottobre", "en": "Countdown to 31 October"},
        "keywords": {"it": ["halloween", "31 ottobre", "quanto manca a halloween", "festa di halloween"], "en": ["halloween countdown", "days to halloween", "31 october"]},
        "meta": {
            "it": "Quanti giorni mancano a Halloween? Il conto alla rovescia al 31 ottobre aggiornato al secondo: giorni, ore e minuti che mancano e il giorno della settimana in cui cade.",
            "en": "How many days until Halloween? A countdown to 31 October updated every second: the days, hours and minutes left and the weekday it falls on.",
        },
        "intro": {
            "it": "Halloween è il 31 ottobre. Qui sotto trovi quanti giorni mancano esattamente — e quante ore, minuti e secondi — e in che giorno della settimana cade quest'anno.",
            "en": "Halloween is on 31 October. Below you'll find exactly how many days are left — and how many hours, minutes and seconds — and which weekday it falls on this year.",
        },
        "article": {
            "it": """
<h2>Tra quanti giorni è Halloween?</h2>
<p>Il numero grande in cima alla pagina è la risposta: sono i giorni interi che mancano al <strong>31 ottobre</strong>, oggi escluso. Il giorno prima leggerai «1 giorno», il 31 ottobre «È oggi!». Halloween è una data fissa, quindi non cambia mai: cambia solo il giorno della settimana, che trovi scritto sotto al conteggio insieme alla data completa.</p>
<h2>Tra quante ore è Halloween?</h2>
<p>Sotto ai giorni scorre la riga con <strong>ore, minuti e secondi</strong>, che si aggiorna da sola e arriva alla mezzanotte con cui inizia il 31 ottobre. Usa l'orologio del tuo dispositivo, quindi il conteggio è quello del posto in cui sei.</p>
<h2>Cosa preparare, e quando</h2>
<ul>
<li><strong>Costumi e decorazioni:</strong> ordinali online guardando i giorni lavorativi che restano per le consegne.</li>
<li><strong>Zucche:</strong> intagliale non più di 3–4 giorni prima, altrimenti si rovinano.</li>
<li><strong>Feste a scuola e in ufficio:</strong> spesso anticipate al venerdì precedente se il 31 cade nel weekend.</li>
</ul>
<h2>Le date vicine</h2>
<p>Il 1° novembre è Ognissanti (festivo in Italia) e il 2 novembre la Commemorazione dei defunti: il ponte dei Santi è tra i più usati per una breve vacanza d'autunno. Dopo Halloween il conto alla rovescia più cercato è quello di <a href="../quanti-giorni-mancano-a-natale/">quanti giorni mancano a Natale</a>, seguito da <a href="../quanti-giorni-mancano-a-capodanno/">Capodanno</a>. Per una data qualsiasi — un compleanno, un viaggio, una scadenza — c'è il <a href="../quanti-giorni-mancano/">conto alla rovescia libero</a>.</p>
""",
            "en": """
<h2>How many days until Halloween?</h2>
<p>The big number at the top of the page is the answer: the whole days left until <strong>31 October</strong>, today excluded. The day before you'll read "1 day"; on 31 October it becomes "It's today!". Halloween is a fixed date, so only the weekday changes — you can read it under the count, together with the full date.</p>
<h2>How many hours until Halloween?</h2>
<p>Under the days runs the line with <strong>hours, minutes and seconds</strong>, which updates on its own and ends at the midnight that starts 31 October. It uses your device's clock, so the count matches wherever you are.</p>
<h2>What to prepare, and when</h2>
<ul>
<li><strong>Costumes and decorations:</strong> order online keeping an eye on the working days left for deliveries.</li>
<li><strong>Pumpkins:</strong> carve them no more than 3–4 days ahead, or they spoil.</li>
<li><strong>School and office parties:</strong> often moved to the previous Friday when the 31st falls at the weekend.</li>
</ul>
<h2>Nearby dates</h2>
<p>1 November is All Saints' Day and 2 November All Souls' Day; in many countries the first days of November are a popular short autumn break. After Halloween the most searched countdown is <a href="../days-until-christmas/">how many days until Christmas</a>, followed by <a href="../days-until-new-year/">New Year</a>. For any other date there is the <a href="../days-until/">free countdown</a>.</p>
""",
        },
        "faq": {
            "it": [
                ("Tra quanti giorni è Halloween?", "Sono i giorni interi che mancano al 31 ottobre: li trovi nel numero grande in cima alla pagina, aggiornato ogni giorno. Se Halloween è già passato, il conteggio salta da solo all'anno prossimo."),
                ("Tra quante ore è Halloween?", "La riga sotto al conteggio dei giorni mostra ore, minuti e secondi che mancano e scorre in tempo reale fino alla mezzanotte con cui inizia il 31 ottobre."),
                ("Che giorno della settimana cade Halloween quest'anno?", "Lo leggi sotto il numero grande, insieme alla data completa. Con il menu «Anno» vedi anche gli anni successivi."),
                ("Halloween è festivo in Italia?", "No, il 31 ottobre è un giorno normale; è festivo il giorno dopo, 1° novembre (Ognissanti)."),
                ("Il conteggio include il 31 ottobre?", "No: mostra i giorni interi che mancano; il 31 ottobre il risultato è «È oggi!»."),
            ],
            "en": [
                ("How many days until Halloween?", "The whole days left until 31 October: you'll find them in the big number at the top of the page. Once Halloween has passed, the count moves to next year by itself."),
                ("How many hours until Halloween?", "The line under the days shows the hours, minutes and seconds left and runs in real time until the midnight that starts 31 October."),
                ("What weekday is Halloween this year?", "Read it under the big number, together with the full date. With the \"Year\" menu you can see the following years too."),
                ("Is Halloween a public holiday?", "No, 31 October is a normal day; in Italy and several other countries the following day, 1 November, is a holiday."),
                ("Does the count include 31 October?", "No: it shows the whole days left; on 31 October the result is \"It's today!\"."),
            ],
        },
    },
    {
        "id": "countdown_black_friday", "icon": "🛍️", "cfg": {"type": "blackfriday"},
        "slug": {"it": "quanti-giorni-mancano-al-black-friday", "en": "days-until-black-friday"},
        "title": {"it": "Quanti giorni mancano al Black Friday?", "en": "How many days until Black Friday?"},
        "seo_title": {"it": "Quanti giorni mancano al Black Friday? Conto alla rovescia", "en": "How many days until Black Friday? Live countdown"},
        "event": {"it": "il Black Friday", "en": "Black Friday"},
        "short": {"it": "Conto alla rovescia al venerdì degli sconti di fine novembre", "en": "Countdown to the Friday of deals at the end of November"},
        "keywords": {"it": ["black friday", "quando è il black friday", "sconti novembre", "cyber monday"], "en": ["black friday countdown", "when is black friday", "cyber monday"]},
        "meta": {
            "it": "Quanti giorni mancano al Black Friday? Il conto alla rovescia aggiornato al secondo, con la data esatta di quest'anno (il venerdì dopo il quarto giovedì di novembre) e quella del Cyber Monday.",
            "en": "How many days until Black Friday? A countdown updated every second, with this year's exact date (the Friday after the fourth Thursday of November) and Cyber Monday's.",
        },
        "intro": {
            "it": "Il Black Friday non ha una data fissa: è il venerdì dopo il quarto giovedì di novembre, quindi cade tra il 23 e il 29. Qui sotto trovi la data esatta di quest'anno e quanti giorni, ore, minuti e secondi mancano.",
            "en": "Black Friday has no fixed date: it's the Friday after the fourth Thursday of November, so it falls between the 23rd and the 29th. Below you'll find this year's exact date and how many days, hours, minutes and seconds are left.",
        },
        "article": {
            "it": """
<h2>Quando è il Black Friday?</h2>
<p>Il Black Friday è il giorno dopo il <em>Thanksgiving</em> americano, che cade il quarto giovedì di novembre: per questo la data cambia ogni anno ma resta sempre nell'ultima settimana del mese. Il calcolatore la trova da solo per l'anno scelto nel menu e conta i giorni interi che mancano, oggi escluso; la riga con ore, minuti e secondi arriva alla mezzanotte con cui inizia il venerdì.</p>
<h2>Le date del Black Friday</h2>
<ul>
<li><strong>2025:</strong> venerdì 28 novembre</li>
<li><strong>2026:</strong> venerdì 27 novembre</li>
<li><strong>2027:</strong> venerdì 26 novembre</li>
<li><strong>2028:</strong> venerdì 24 novembre</li>
</ul>
<h2>Cyber Monday e «Black Week»</h2>
<p>Il <strong>Cyber Monday</strong> è il lunedì successivo, tre giorni dopo il Black Friday, dedicato in origine agli acquisti online. Ormai molti negozi anticipano gli sconti a tutta la settimana («Black Week») o all'intero mese di novembre: il conteggio qui sopra vale per il venerdì ufficiale, che resta il giorno delle offerte più aggressive.</p>
<h2>Come prepararsi</h2>
<ul>
<li><strong>Lista dei desideri:</strong> segna i prezzi qualche settimana prima, così riconosci gli sconti veri da quelli gonfiati.</li>
<li><strong>Consegne:</strong> i giorni lavorativi nel riquadro dicono quanto tempo hai perché gli ordini arrivino prima di <a href="../quanti-giorni-mancano-a-natale/">Natale</a>.</li>
<li><strong>Altre date utili:</strong> <a href="../quanti-giorni-mancano-all-immacolata/">l'Immacolata</a> apre la stagione dei regali; per qualsiasi altra scadenza c'è il <a href="../quanti-giorni-mancano/">conto alla rovescia libero</a>.</li>
</ul>
""",
            "en": """
<h2>When is Black Friday?</h2>
<p>Black Friday is the day after American Thanksgiving, which falls on the fourth Thursday of November: that's why the date changes every year but always stays in the last week of the month. The calculator finds it for the year chosen in the menu and counts the whole days left, today excluded; the line with hours, minutes and seconds ends at the midnight that starts the Friday.</p>
<h2>Black Friday dates</h2>
<ul>
<li><strong>2025:</strong> Friday 28 November</li>
<li><strong>2026:</strong> Friday 27 November</li>
<li><strong>2027:</strong> Friday 26 November</li>
<li><strong>2028:</strong> Friday 24 November</li>
</ul>
<h2>Cyber Monday and "Black Week"</h2>
<p><strong>Cyber Monday</strong> is the following Monday, three days after Black Friday, originally dedicated to online shopping. Many shops now stretch the deals over the whole week ("Black Week") or the entire month of November: the count above is for the official Friday, still the day with the most aggressive offers.</p>
<h2>How to prepare</h2>
<ul>
<li><strong>Wish list:</strong> note prices a few weeks ahead, so you can tell real discounts from inflated ones.</li>
<li><strong>Deliveries:</strong> the working days in the box tell you how long you have for orders to arrive before <a href="../days-until-christmas/">Christmas</a>.</li>
<li><strong>Other dates:</strong> for any other deadline there is the <a href="../days-until/">free countdown</a>.</li>
</ul>
""",
        },
        "faq": {
            "it": [
                ("Quando è il Black Friday quest'anno?", "La data esatta è scritta sotto il numero grande: è il venerdì dopo il quarto giovedì di novembre. Nel 2026 è il 27 novembre, nel 2027 il 26 novembre."),
                ("Tra quanti giorni è il Black Friday?", "Sono i giorni interi che mancano al venerdì degli sconti: li trovi nel numero grande in cima alla pagina, aggiornato ogni giorno. Passato il Black Friday, il conteggio salta da solo all'anno prossimo."),
                ("Quando è il Cyber Monday?", "Il lunedì subito dopo il Black Friday, cioè tre giorni più tardi: nel 2026 è il 30 novembre."),
                ("Il Black Friday è festivo in Italia?", "No, è un normale giorno lavorativo: negli Stati Uniti è il ponte dopo il Thanksgiving, in Italia è solo la giornata degli sconti."),
            ],
            "en": [
                ("When is Black Friday this year?", "The exact date is written under the big number: it's the Friday after the fourth Thursday of November. In 2026 it's 27 November, in 2027 it's 26 November."),
                ("How many days until Black Friday?", "The whole days left until the Friday of deals: you'll find them in the big number at the top of the page. Once Black Friday has passed, the count moves to next year by itself."),
                ("When is Cyber Monday?", "The Monday right after Black Friday, three days later: in 2026 it's 30 November."),
                ("Is Black Friday a public holiday?", "Not in Europe: it's a normal working day. In the United States it's the long weekend after Thanksgiving."),
            ],
        },
    },
    {
        "id": "countdown_avvento", "icon": "🕯️", "cfg": {"type": "fixed", "m": 12, "d": 1},
        "slug": {"it": "quanti-giorni-mancano-al-1-dicembre", "en": "days-until-1-december"},
        "title": {"it": "Quanti giorni mancano al 1° dicembre?", "en": "How many days until 1 December?"},
        "seo_title": {"it": "Quanti giorni mancano al 1° dicembre? Countdown all'Avvento", "en": "How many days until 1 December? Advent countdown"},
        "event": {"it": "il 1° dicembre", "en": "1 December"},
        "short": {"it": "Conto alla rovescia al primo giorno del calendario dell'Avvento", "en": "Countdown to the first day of the Advent calendar"},
        "keywords": {"it": ["1 dicembre", "calendario dell'avvento", "avvento", "inizio dicembre", "quanto manca a dicembre"], "en": ["1 december", "advent calendar", "advent countdown", "december countdown"]},
        "meta": {
            "it": "Quanti giorni mancano al 1° dicembre? Conto alla rovescia aggiornato al secondo al primo giorno del calendario dell'Avvento, con il giorno della settimana in cui cade e i giorni che restano poi fino a Natale.",
            "en": "How many days until 1 December? A countdown updated every second to the first day of the Advent calendar, with the weekday it falls on and the days left until Christmas.",
        },
        "intro": {
            "it": "Il 1° dicembre si apre la prima casella del calendario dell'Avvento e parte il mese di Natale. Qui sotto trovi quanti giorni, ore, minuti e secondi mancano e in che giorno della settimana cade.",
            "en": "On 1 December the first door of the Advent calendar opens and the Christmas month begins. Below you'll find how many days, hours, minutes and seconds are left and which weekday it falls on.",
        },
        "article": {
            "it": """
<h2>Tra quanti giorni è il 1° dicembre?</h2>
<p>Il numero grande in cima alla pagina è la risposta: i giorni interi che mancano al <strong>1° dicembre</strong>, oggi escluso. Il 30 novembre leggerai «1 giorno», il 1° dicembre «È oggi!». Sotto ai giorni scorre la riga con ore, minuti e secondi, che arriva alla mezzanotte con cui inizia il mese.</p>
<h2>Il calendario dell'Avvento</h2>
<p>Il calendario dell'Avvento va dal 1° al 24 dicembre: 24 caselle, una al giorno, fino alla <a href="../quanti-giorni-mancano-alla-vigilia-di-natale/">Vigilia</a>. Se ne stai preparando uno in casa — cioccolatini, bigliettini, piccoli regali — i giorni mostrati qui sopra sono quelli che hai per finirlo. L'Avvento liturgico invece comincia la quarta domenica prima di Natale, quindi tra il 27 novembre e il 3 dicembre.</p>
<h2>Cosa parte a dicembre</h2>
<ul>
<li><strong>Addobbi:</strong> tradizionalmente si fanno all'<a href="../quanti-giorni-mancano-all-immacolata/">Immacolata</a>, l'8 dicembre, ma molti cominciano già il 1°.</li>
<li><strong>Regali:</strong> dal 1° dicembre al 25 ci sono 24 giorni, e i giorni lavorativi utili per le consegne sono meno di venti.</li>
<li><strong>Le altre date:</strong> <a href="../quanti-giorni-mancano-a-natale/">Natale</a>, <a href="../quanti-giorni-mancano-a-capodanno/">Capodanno</a>, oppure il <a href="../quanti-giorni-mancano/">conto alla rovescia libero</a> per qualsiasi giorno.</li>
</ul>
""",
            "en": """
<h2>How many days until 1 December?</h2>
<p>The big number at the top of the page is the answer: the whole days left until <strong>1 December</strong>, today excluded. On 30 November you'll read "1 day"; on 1 December it becomes "It's today!". Under the days runs the line with hours, minutes and seconds, ending at the midnight that starts the month.</p>
<h2>The Advent calendar</h2>
<p>The Advent calendar runs from 1 to 24 December: 24 doors, one a day, until <a href="../days-until-christmas-eve/">Christmas Eve</a>. If you're making one at home — chocolates, notes, small gifts — the days shown above are the ones you have left to finish it. Liturgical Advent instead begins on the fourth Sunday before Christmas, so between 27 November and 3 December.</p>
<h2>What starts in December</h2>
<ul>
<li><strong>Decorations:</strong> in Italy they traditionally go up on <a href="../days-until-immaculate-conception/">8 December</a>, but many start on the 1st.</li>
<li><strong>Presents:</strong> from 1 to 25 December there are 24 days, and fewer than twenty working days for deliveries.</li>
<li><strong>Other dates:</strong> <a href="../days-until-christmas/">Christmas</a>, <a href="../days-until-new-year/">New Year</a>, or the <a href="../days-until/">free countdown</a> for any day.</li>
</ul>
""",
        },
        "faq": {
            "it": [
                ("Quanti giorni mancano a dicembre?", "Il conteggio in cima alla pagina arriva al 1° dicembre, cioè all'inizio del mese: sono i giorni interi che mancano, oggi escluso."),
                ("Quando si apre il calendario dell'Avvento?", "La prima casella si apre il 1° dicembre e l'ultima il 24, la Vigilia di Natale: 24 caselle in tutto."),
                ("Quando inizia l'Avvento?", "Quello del calendario il 1° dicembre; quello liturgico la quarta domenica prima di Natale, tra il 27 novembre e il 3 dicembre."),
                ("Il conteggio include il 1° dicembre?", "No: mostra i giorni interi che mancano; il 1° dicembre il risultato è «È oggi!»."),
            ],
            "en": [
                ("How many days until December?", "The count at the top of the page runs to 1 December, the start of the month: the whole days left, today excluded."),
                ("When does the Advent calendar open?", "The first door opens on 1 December and the last on 24 December, Christmas Eve: 24 doors in all."),
                ("When does Advent start?", "The calendar on 1 December; liturgical Advent on the fourth Sunday before Christmas, between 27 November and 3 December."),
                ("Does the count include 1 December?", "No: it shows the whole days left; on 1 December the result is \"It's today!\"."),
            ],
        },
    },
    {
        "id": "countdown_immacolata", "icon": "🎄", "cfg": {"type": "fixed", "m": 12, "d": 8},
        "slug": {"it": "quanti-giorni-mancano-all-immacolata", "en": "days-until-immaculate-conception"},
        "title": {"it": "Quanti giorni mancano all'Immacolata?", "en": "How many days until 8 December (Immaculate Conception)?"},
        "seo_title": {"it": "Quanti giorni mancano all'8 dicembre? Countdown all'Immacolata", "en": "How many days until 8 December? Immaculate Conception countdown"},
        "event": {"it": "l'Immacolata", "en": "8 December"},
        "short": {"it": "Conto alla rovescia all'8 dicembre, festa e giorno dell'albero", "en": "Countdown to 8 December, Italy's public holiday and tree-decorating day"},
        "keywords": {"it": ["immacolata", "8 dicembre", "otto dicembre", "ponte dell'immacolata", "albero di natale"], "en": ["8 december", "immaculate conception", "italy holiday december", "christmas tree day"]},
        "meta": {
            "it": "Quanti giorni mancano all'8 dicembre? Conto alla rovescia all'Immacolata aggiornato al secondo, con il giorno della settimana in cui cade e se quest'anno c'è il ponte.",
            "en": "How many days until 8 December? A countdown to the Immaculate Conception, Italy's public holiday, updated every second, with the weekday it falls on and whether it makes a long weekend.",
        },
        "intro": {
            "it": "L'Immacolata è l'8 dicembre, festa nazionale e per tradizione il giorno in cui si fa l'albero di Natale. Qui sotto trovi quanti giorni, ore, minuti e secondi mancano e in che giorno della settimana cade quest'anno.",
            "en": "The Immaculate Conception is on 8 December, a public holiday in Italy and traditionally the day the Christmas tree goes up. Below you'll find how many days, hours, minutes and seconds are left and which weekday it falls on this year.",
        },
        "article": {
            "it": """
<h2>Tra quanti giorni è l'8 dicembre?</h2>
<p>Il numero grande in cima alla pagina è la risposta: i giorni interi che mancano all'<strong>8 dicembre</strong>, oggi escluso. È una data fissa, quindi cambia solo il giorno della settimana, scritto sotto al conteggio insieme alla data completa. La riga con ore, minuti e secondi si aggiorna da sola.</p>
<h2>C'è il ponte dell'Immacolata?</h2>
<p>Dipende dal giorno della settimana: se l'8 dicembre cade di <strong>martedì o giovedì</strong> basta un giorno di ferie per un ponte di quattro giorni; di <strong>lunedì o venerdì</strong> il weekend è lungo da solo; di sabato o domenica la festa si perde (in Italia non viene recuperata). Nel 2026 l'8 dicembre è un martedì.</p>
<h2>Cosa si fa l'8 dicembre</h2>
<ul>
<li><strong>L'albero e il presepe:</strong> per tradizione si preparano proprio in questo giorno e si smontano all'Epifania, il 6 gennaio.</li>
<li><strong>Mercatini e luminarie:</strong> in molte città si accendono nel weekend dell'Immacolata.</li>
<li><strong>I regali:</strong> da qui a <a href="../quanti-giorni-mancano-a-natale/">Natale</a> restano 17 giorni, e meno di quindici lavorativi per le consegne. La <a href="../quanti-giorni-mancano-alla-vigilia-di-natale/">Vigilia</a> è il 24. Per qualsiasi altra data c'è il <a href="../quanti-giorni-mancano/">conto alla rovescia libero</a>.</li>
</ul>
""",
            "en": """
<h2>How many days until 8 December?</h2>
<p>The big number at the top of the page is the answer: the whole days left until <strong>8 December</strong>, today excluded. It's a fixed date, so only the weekday changes — it's written under the count together with the full date. The line with hours, minutes and seconds updates on its own.</p>
<h2>Is it a long weekend?</h2>
<p>It depends on the weekday: when 8 December falls on a <strong>Tuesday or Thursday</strong>, one day off makes a four-day break; on a <strong>Monday or Friday</strong> the weekend is long by itself; on a Saturday or Sunday the holiday is lost (Italy doesn't move it). In 2026, 8 December is a Tuesday.</p>
<h2>What happens on 8 December</h2>
<ul>
<li><strong>Tree and nativity scene:</strong> in Italy they traditionally go up on this day and come down on Epiphany, 6 January.</li>
<li><strong>Markets and lights:</strong> many cities switch on their Christmas lights on this weekend.</li>
<li><strong>Presents:</strong> from here to <a href="../days-until-christmas/">Christmas</a> there are 17 days, and fewer than fifteen working days for deliveries. <a href="../days-until-christmas-eve/">Christmas Eve</a> is the 24th. For any other date there is the <a href="../days-until/">free countdown</a>.</li>
</ul>
""",
        },
        "faq": {
            "it": [
                ("Quanti giorni mancano all'8 dicembre?", "Sono i giorni interi che separano oggi dall'Immacolata: li trovi nel numero grande in cima alla pagina, aggiornato ogni giorno. Passato l'8 dicembre, il conteggio salta da solo all'anno prossimo."),
                ("L'8 dicembre è festivo?", "Sì, in Italia l'Immacolata Concezione è festa nazionale: scuole, uffici e la maggior parte dei negozi sono chiusi."),
                ("Che giorno cade l'Immacolata quest'anno?", "Lo leggi sotto il numero grande, insieme alla data completa. Nel 2026 è martedì, nel 2027 mercoledì."),
                ("Quando si fa l'albero di Natale?", "Per tradizione l'8 dicembre, festa dell'Immacolata, e si toglie il 6 gennaio. Molti lo fanno prima, già dal 1° dicembre."),
            ],
            "en": [
                ("How many days until 8 December?", "The whole days between today and the Immaculate Conception: you'll find them in the big number at the top of the page. Once 8 December has passed, the count moves to next year by itself."),
                ("Is 8 December a public holiday?", "Yes, in Italy the Immaculate Conception is a national holiday: schools, offices and most shops are closed."),
                ("What weekday is 8 December this year?", "Read it under the big number, together with the full date. In 2026 it's a Tuesday, in 2027 a Wednesday."),
                ("When does the Christmas tree go up in Italy?", "Traditionally on 8 December, and it comes down on 6 January. Many families start earlier, from 1 December."),
            ],
        },
    },
    {
        "id": "countdown_inverno", "icon": "❄️", "cfg": {"type": "fixed", "m": 12, "d": 21},
        "slug": {"it": "quanti-giorni-mancano-all-inverno", "en": "days-until-winter"},
        "title": {"it": "Quanti giorni mancano all'inverno?", "en": "How many days until winter?"},
        "seo_title": {"it": "Quanti giorni mancano all'inverno? Countdown al 21 dicembre", "en": "How many days until winter? Countdown to 21 December"},
        "event": {"it": "l'inverno", "en": "winter"},
        "short": {"it": "Conto alla rovescia al solstizio del 21 dicembre, il giorno più corto", "en": "Countdown to the solstice on 21 December, the shortest day"},
        "keywords": {"it": ["inverno", "inizio inverno", "solstizio d'inverno", "21 dicembre", "giorno più corto"], "en": ["winter countdown", "first day of winter", "winter solstice", "21 december", "shortest day"]},
        "meta": {
            "it": "Quanti giorni mancano all'inverno? Conto alla rovescia al 21 dicembre, il solstizio e il giorno più corto dell'anno, aggiornato al secondo, con il giorno della settimana in cui cade.",
            "en": "How many days until winter? A countdown to 21 December, the solstice and shortest day of the year, updated every second, with the weekday it falls on.",
        },
        "intro": {
            "it": "L'inverno astronomico comincia con il solstizio, il 21 dicembre (a volte il 22): il giorno più corto dell'anno. Qui sotto trovi quanti giorni, ore, minuti e secondi mancano e in che giorno della settimana cade.",
            "en": "Astronomical winter begins with the solstice, on 21 December (sometimes the 22nd): the shortest day of the year. Below you'll find how many days, hours, minutes and seconds are left and which weekday it falls on.",
        },
        "article": {
            "it": """
<h2>Tra quanti giorni inizia l'inverno?</h2>
<p>Il numero grande in cima alla pagina è la risposta: i giorni interi che mancano al <strong>21 dicembre</strong>, oggi escluso. Sotto scorre la riga con ore, minuti e secondi, che arriva alla mezzanotte con cui inizia il giorno del solstizio.</p>
<h2>Quando inizia l'inverno: 21 o 22 dicembre?</h2>
<p>L'inverno astronomico parte con il <strong>solstizio</strong>, il momento in cui il Sole raggiunge il punto più basso nel cielo dell'emisfero nord. Nella maggior parte degli anni cade il 21 dicembre (nel 2026 alle 21:50 ora italiana), qualche volta il 22: il calcolatore usa il 21. L'<em>inverno meteorologico</em>, quello delle statistiche del clima, inizia invece il 1° dicembre e dura fino al 28 febbraio; la primavera astronomica comincia con l'equinozio del 20 marzo.</p>
<h2>Il giorno più corto dell'anno</h2>
<p>Al solstizio la luce dura meno che in qualsiasi altro giorno: a Milano circa 8 ore e 45 minuti, a Palermo circa 9 ore e 30. Dal giorno dopo le giornate si allungano di nuovo, anche se all'inizio di pochi secondi. Il freddo più intenso arriva di solito a gennaio, perché terra e mare si raffreddano con ritardo.</p>
<h2>Le date vicine</h2>
<p>Tre giorni dopo il solstizio c'è la <a href="../quanti-giorni-mancano-alla-vigilia-di-natale/">Vigilia</a>, poi <a href="../quanti-giorni-mancano-a-natale/">Natale</a> e <a href="../quanti-giorni-mancano-a-capodanno/">Capodanno</a>; dall'altra parte dell'anno c'è il conto alla rovescia all'<a href="../quanti-giorni-mancano-all-estate/">estate</a>. Per qualsiasi data usa il <a href="../quanti-giorni-mancano/">conto alla rovescia libero</a>.</p>
""",
            "en": """
<h2>How many days until winter starts?</h2>
<p>The big number at the top of the page is the answer: the whole days left until <strong>21 December</strong>, today excluded. Under it runs the line with hours, minutes and seconds, ending at the midnight that starts the day of the solstice.</p>
<h2>When does winter start: 21 or 22 December?</h2>
<p>Astronomical winter begins with the <strong>solstice</strong>, the moment the Sun reaches its lowest point in the northern sky. Most years it falls on 21 December (in 2026 at 20:50 UTC), occasionally on the 22nd: the calculator uses the 21st. <em>Meteorological winter</em>, the one used for climate statistics, runs from 1 December to 28 February; astronomical spring begins with the equinox on 20 March.</p>
<h2>The shortest day of the year</h2>
<p>At the solstice daylight is shorter than on any other day: about 7 h 50 min in London, about 8 h 45 min in Milan. From the next day on, days get longer again, by a few seconds at first. The coldest weather usually comes in January, because land and sea cool down with a delay.</p>
<h2>Nearby dates</h2>
<p>Three days after the solstice comes <a href="../days-until-christmas-eve/">Christmas Eve</a>, then <a href="../days-until-christmas/">Christmas</a> and <a href="../days-until-new-year/">New Year</a>; on the other side of the year there is the countdown to <a href="../days-until-summer/">summer</a>. For any date use the <a href="../days-until/">free countdown</a>.</p>
""",
        },
        "faq": {
            "it": [
                ("Quando inizia l'inverno?", "Con il solstizio, il 21 dicembre nella maggior parte degli anni (a volte il 22). L'inverno meteorologico invece parte il 1° dicembre."),
                ("Tra quanti giorni è l'inverno?", "Sono i giorni interi che mancano al 21 dicembre: li trovi nel numero grande in cima alla pagina, aggiornato ogni giorno."),
                ("Qual è il giorno più corto dell'anno?", "Il giorno del solstizio d'inverno, il 21 dicembre: da lì in poi la luce torna ad allungarsi."),
                ("Quando finisce l'inverno?", "Con l'equinozio di primavera, il 20 marzo (a volte il 21). Quello meteorologico finisce il 28 febbraio."),
            ],
            "en": [
                ("When does winter start?", "With the solstice, on 21 December most years (sometimes the 22nd). Meteorological winter starts on 1 December instead."),
                ("How many days until winter?", "The whole days left until 21 December: you'll find them in the big number at the top of the page, updated every day."),
                ("What is the shortest day of the year?", "The day of the winter solstice, 21 December: from then on daylight gets longer again."),
                ("When does winter end?", "With the spring equinox, on 20 March (sometimes the 21st). Meteorological winter ends on 28 February."),
            ],
        },
    },
    {
        "id": "countdown_vigilia", "icon": "🌟", "cfg": {"type": "fixed", "m": 12, "d": 24},
        "slug": {"it": "quanti-giorni-mancano-alla-vigilia-di-natale", "en": "days-until-christmas-eve"},
        "title": {"it": "Quanti giorni mancano alla Vigilia di Natale?", "en": "How many days until Christmas Eve?"},
        "seo_title": {"it": "Quanti giorni mancano alla Vigilia di Natale? Countdown al 24", "en": "How many days until Christmas Eve? Countdown to 24 December"},
        "event": {"it": "la Vigilia di Natale", "en": "Christmas Eve"},
        "short": {"it": "Conto alla rovescia al 24 dicembre, la sera dei regali", "en": "Countdown to 24 December, the night before Christmas"},
        "keywords": {"it": ["vigilia", "vigilia di natale", "24 dicembre", "cenone della vigilia", "notte di natale"], "en": ["christmas eve countdown", "24 december", "night before christmas"]},
        "meta": {
            "it": "Quanti giorni mancano alla Vigilia di Natale? Conto alla rovescia al 24 dicembre aggiornato al secondo: giorni, ore e minuti che mancano, il giorno della settimana in cui cade e i giorni lavorativi per gli ultimi regali.",
            "en": "How many days until Christmas Eve? A countdown to 24 December updated every second: the days, hours and minutes left, the weekday it falls on and the working days for last-minute presents.",
        },
        "intro": {
            "it": "La Vigilia è il 24 dicembre, la sera del cenone e, in molte famiglie, dei regali. Qui sotto trovi quanti giorni, ore, minuti e secondi mancano e in che giorno della settimana cade quest'anno.",
            "en": "Christmas Eve is on 24 December, the night of the big dinner and, in many families, of the presents. Below you'll find how many days, hours, minutes and seconds are left and which weekday it falls on this year.",
        },
        "article": {
            "it": """
<h2>Tra quanti giorni è la Vigilia di Natale?</h2>
<p>Il numero grande in cima alla pagina è la risposta: i giorni interi che mancano al <strong>24 dicembre</strong>, oggi escluso. Il 23 leggerai «1 giorno», il 24 «È oggi!» e il giorno dopo il conteggio passa da solo alla Vigilia dell'anno prossimo. Sotto scorre la riga con ore, minuti e secondi, che arriva alla mezzanotte con cui inizia il 24.</p>
<h2>Vigilia o Natale: quale conto alla rovescia usare?</h2>
<p>Se in famiglia i regali si aprono la sera del 24, o alla mezzanotte, questo è il conteggio giusto; se li aprite la mattina del 25 usa il <a href="../quanti-giorni-mancano-a-natale/">conto alla rovescia a Natale</a>, che segna sempre un giorno in più. Il 24 dicembre non è festivo in Italia: negozi e uffici sono aperti, spesso con orario ridotto nel pomeriggio.</p>
<h2>Cosa cade prima e dopo</h2>
<ul>
<li><strong>Prima:</strong> <a href="../quanti-giorni-mancano-all-immacolata/">l'Immacolata</a> (8 dicembre) e il <a href="../quanti-giorni-mancano-all-inverno/">solstizio d'inverno</a> (21 dicembre); il calendario dell'Avvento chiude proprio il 24.</li>
<li><strong>Dopo:</strong> Natale, Santo Stefano (26 dicembre, festivo), <a href="../quanti-giorni-mancano-a-capodanno/">Capodanno</a> e <a href="../quanti-giorni-mancano-alla-befana/">la Befana</a>, che chiude le feste.</li>
<li><strong>Regali dell'ultimo minuto:</strong> i giorni lavorativi nel riquadro sono quelli utili perché un ordine arrivi in tempo. Per qualsiasi altra data c'è il <a href="../quanti-giorni-mancano/">conto alla rovescia libero</a>.</li>
</ul>
""",
            "en": """
<h2>How many days until Christmas Eve?</h2>
<p>The big number at the top of the page is the answer: the whole days left until <strong>24 December</strong>, today excluded. On the 23rd you'll read "1 day", on the 24th "It's today!", and the day after the count moves by itself to next year's Christmas Eve. Under it runs the line with hours, minutes and seconds, ending at the midnight that starts the 24th.</p>
<h2>Christmas Eve or Christmas Day: which countdown?</h2>
<p>If your family opens presents on the evening of the 24th, or at midnight, this is the right count; if you open them on the morning of the 25th, use the <a href="../days-until-christmas/">countdown to Christmas</a>, which always shows one day more. 24 December is not a public holiday in Italy: shops and offices are open, often with shorter hours in the afternoon.</p>
<h2>What comes before and after</h2>
<ul>
<li><strong>Before:</strong> <a href="../days-until-immaculate-conception/">8 December</a> and the <a href="../days-until-winter/">winter solstice</a> (21 December); the Advent calendar ends on the 24th.</li>
<li><strong>After:</strong> Christmas, Boxing Day (26 December), <a href="../days-until-new-year/">New Year</a> and <a href="../days-until-epiphany/">Epiphany</a>, which closes the season.</li>
<li><strong>Last-minute presents:</strong> the working days in the box are the ones that count for an order to arrive in time. For any other date there is the <a href="../days-until/">free countdown</a>.</li>
</ul>
""",
        },
        "faq": {
            "it": [
                ("Quanti giorni mancano al 24 dicembre?", "Sono i giorni interi che separano oggi dalla Vigilia: li trovi nel numero grande in cima alla pagina, aggiornato ogni giorno. Passato il 24, il conteggio salta da solo all'anno prossimo."),
                ("Tra quante ore è la Vigilia di Natale?", "La riga sotto al conteggio dei giorni mostra ore, minuti e secondi che mancano e scorre in tempo reale fino alla mezzanotte con cui inizia il 24 dicembre."),
                ("La Vigilia di Natale è festiva?", "No, in Italia il 24 dicembre è un giorno lavorativo; sono festivi il 25 (Natale) e il 26 (Santo Stefano)."),
                ("Che giorno cade la Vigilia quest'anno?", "Lo leggi sotto il numero grande, insieme alla data completa. Con il menu «Anno» vedi anche gli anni successivi."),
            ],
            "en": [
                ("How many days until 24 December?", "The whole days between today and Christmas Eve: you'll find them in the big number at the top of the page. Once the 24th has passed, the count moves to next year by itself."),
                ("How many hours until Christmas Eve?", "The line under the days shows the hours, minutes and seconds left and runs in real time until the midnight that starts 24 December."),
                ("Is Christmas Eve a public holiday?", "Not in Italy: 24 December is a working day; 25 and 26 December are the holidays."),
                ("What weekday is Christmas Eve this year?", "Read it under the big number, together with the full date. With the \"Year\" menu you can see the following years too."),
            ],
        },
    },
    {
        "id": "countdown_inizio_scuola", "icon": "🎒", "cfg": {"type": "custom", "m": 9, "d": 15},
        "slug": {"it": "quanti-giorni-mancano-all-inizio-della-scuola", "en": "days-until-school-starts"},
        "title": {"it": "Quanti giorni mancano all'inizio della scuola?", "en": "How many days until school starts?"},
        "event": {"it": "l'inizio della scuola", "en": "the first day of school"},
        "short": {"it": "Conto alla rovescia al primo giorno di scuola della tua regione", "en": "Countdown to the first day of school (set your date)"},
        "keywords": {"it": ["inizio scuola", "primo giorno di scuola", "rientro a scuola", "calendario scolastico", "quanto manca alla scuola"], "en": ["back to school countdown", "first day of school", "school start"]},
        "meta": {
            "it": "Quanti giorni mancano all'inizio della scuola? Inserisci la data di inizio del calendario scolastico della tua regione e ottieni il conto alla rovescia con giorni, settimane, ore e minuti.",
            "en": "How many days until school starts? Enter the first day of school from your school calendar and get a countdown with days, weeks, hours and minutes.",
        },
        "intro": {
            "it": "In Italia la scuola riparte tra il 5 e il 16 settembre a seconda della regione: inserisci la data del tuo calendario scolastico (è preimpostato il 15 settembre) e conta i giorni che mancano.",
            "en": "Enter the first day of school from your school calendar (15 September is preset) and count the days left until the return to class.",
        },
        "article": {
            "it": """
<h2>Quando inizia la scuola: dipende dalla regione</h2>
<p>La data di inizio delle lezioni la decide ogni regione (e le province autonome di Trento e Bolzano) con il proprio calendario scolastico, di solito tra il 5 e il 16 settembre: le prime a partire sono di norma Bolzano e la Provincia di Trento, tra le ultime Sicilia, Puglia e Sardegna. Per questo il calcolatore ti chiede la data: trovi quella giusta sul sito della tua regione o della scuola, poi il conto alla rovescia fa il resto. Le scuole dell'infanzia e alcune scuole paritarie possono aprire qualche giorno prima.</p>
<h2>Come usare il conteggio</h2>
<ul>
<li><strong>Compiti delle vacanze:</strong> dividi le pagine che restano per i giorni mancanti e sai quanto fare al giorno.</li>
<li><strong>Libri e materiale:</strong> ordina guardando i giorni lavorativi, che sono quelli utili per le consegne.</li>
<li><strong>Ultimi giorni di vacanza:</strong> copia la frase con il conteggio e condividila in famiglia.</li>
</ul>
<h2>Le altre date dell'anno scolastico</h2>
<p>Le lezioni finiscono tra il 6 e il 10 giugno (pagina «Quanti giorni mancano alla fine della scuola»); le vacanze di Natale vanno in genere dal 23 dicembre al 6 gennaio, quelle di Pasqua dal giovedì prima al martedì dopo Pasqua.</p>
""",
            "en": """
<h2>When school starts: it depends where you live</h2>
<p>The first day of school is set by each region, state or school district: in Italy between 5 and 16 September, in the UK in early September, in most of the US between early August and early September. That's why the calculator asks for the date: find it on your school's or region's calendar, and the countdown does the rest.</p>
<h2>How to use the count</h2>
<ul>
<li><strong>Summer homework:</strong> divide the pages left by the days left and you know how much to do each day.</li>
<li><strong>Books and supplies:</strong> order them keeping an eye on the working days, the ones that count for deliveries.</li>
<li><strong>Last days of holiday:</strong> copy the sentence with the count and share it with the family.</li>
</ul>
<h2>Other school-year dates</h2>
<p>In Italy lessons end between 6 and 10 June (see the "last day of school" page); Christmas holidays usually run from 23 December to 6 January, Easter holidays from the Thursday before to the Tuesday after Easter.</p>
""",
        },
        "faq": {
            "it": [
                ("Perché devo inserire la data io?", "Perché ogni regione fissa una data diversa, che cambia di anno in anno. Il 15 settembre è solo un valore indicativo: sostituiscilo con quello del tuo calendario scolastico."),
                ("Dove trovo la data di inizio della mia regione?", "Sul sito della regione (calendario scolastico regionale) o sul sito della scuola; le scuole possono anticipare l'inizio con delibera del consiglio d'istituto."),
                ("Il conteggio include il primo giorno di scuola?", "No: conta i giorni interi che mancano. La sera prima mostra «1 giorno»."),
            ],
            "en": [
                ("Why do I have to enter the date myself?", "Because every region, state or district sets a different date, which changes every year. 15 September is only a placeholder: replace it with the date on your school calendar."),
                ("Where do I find the date?", "On your school's website or on the regional/state school calendar."),
                ("Does the count include the first day of school?", "No: it counts the whole days left. The evening before it shows \"1 day\"."),
            ],
        },
    },
    {
        "id": "countdown_fine_scuola", "icon": "🏁", "cfg": {"type": "custom", "m": 6, "d": 8},
        "slug": {"it": "quanti-giorni-mancano-alla-fine-della-scuola", "en": "days-until-school-ends"},
        "title": {"it": "Quanti giorni mancano alla fine della scuola?", "en": "How many days until school ends?"},
        "event": {"it": "la fine della scuola", "en": "the last day of school"},
        "short": {"it": "Conto alla rovescia all'ultimo giorno di lezione", "en": "Countdown to the last day of lessons (set your date)"},
        "keywords": {"it": ["fine scuola", "ultimo giorno di scuola", "quanto manca alla fine della scuola", "vacanze estive"], "en": ["last day of school countdown", "school ends", "summer break"]},
        "meta": {
            "it": "Quanti giorni mancano alla fine della scuola? Inserisci l'ultimo giorno di lezione del tuo calendario scolastico e ottieni il conto alla rovescia con giorni, settimane, giorni di scuola (lun–ven) e ore.",
            "en": "How many days until school ends? Enter the last day of lessons from your school calendar and get a countdown with days, weeks, school days (Mon–Fri) and hours.",
        },
        "intro": {
            "it": "In Italia le lezioni finiscono tra il 6 e il 10 giugno secondo la regione: inserisci l'ultimo giorno di scuola del tuo calendario (è preimpostato l'8 giugno) e conta i giorni, e i giorni di scuola, che mancano.",
            "en": "Enter the last day of school from your calendar (8 June is preset) and count the days – and the school days – left until the summer break.",
        },
        "article": {
            "it": """
<h2>Quando finisce la scuola</h2>
<p>L'ultimo giorno di lezione lo fissa il calendario scolastico regionale: nella maggior parte delle regioni cade tra il 6 e il 10 giugno; le scuole dell'infanzia continuano fino al 30 giugno. Per gli studenti dell'ultimo anno delle superiori la fine vera è l'esame di maturità, che inizia con la prima prova scritta nella terza settimana di giugno; per la terza media c'è l'esame entro fine giugno.</p>
<h2>Giorni di calendario e giorni di scuola</h2>
<p>Il numero grande sono i giorni di calendario; il riquadro «Giorni lavorativi (lun–ven)» corrisponde ai giorni di scuola per chi fa la settimana corta, senza contare le festività (2 giugno, Pasquetta, ponti) e i giorni di chiusura decisi dall'istituto: sottraili a mano. Chi va a scuola anche il sabato aggiunge un giorno a settimana.</p>
<h2>Idee per gli ultimi giorni</h2>
<ul>
<li><strong>Interrogazioni e verifiche:</strong> gli ultimi voti si mettono di solito entro la fine di maggio: programma il ripasso sui giorni che restano.</li>
<li><strong>Gita di fine anno e feste di classe:</strong> copia la frase con il conteggio e mettila nella chat di classe.</li>
<li><strong>Centri estivi:</strong> le iscrizioni aprono in primavera: la data di fine scuola ti dice da quando servono.</li>
</ul>
""",
            "en": """
<h2>When school ends</h2>
<p>The last day of lessons is set by each region, state or school district: in Italy between 6 and 10 June, in the UK around 20 July, in the US from late May to mid-June. Enter the date from your school calendar and the countdown does the rest.</p>
<h2>Calendar days and school days</h2>
<p>The big number is calendar days; the "Working days (Mon–Fri)" box corresponds to school days, without subtracting public holidays and school closures: subtract those by hand.</p>
<h2>Ideas for the last weeks</h2>
<ul>
<li><strong>Tests and exams:</strong> plan revision on the days left.</li>
<li><strong>End-of-year trip and class parties:</strong> copy the sentence with the count and post it in the class chat.</li>
<li><strong>Summer camps:</strong> registrations open in spring: the last day of school tells you from when you need them.</li>
</ul>
""",
        },
        "faq": {
            "it": [
                ("Perché devo inserire la data?", "Perché ogni regione fissa la sua, e cambia ogni anno. L'8 giugno è solo indicativo: sostituiscilo con la data del tuo calendario scolastico."),
                ("Quanti giorni di scuola mancano davvero?", "Guarda «Giorni lavorativi (lun–ven)» e togli le festività e le chiusure della tua scuola; se fai lezione anche il sabato, aggiungi un giorno per settimana."),
                ("La scuola dell'infanzia finisce lo stesso giorno?", "No, di norma continua fino al 30 giugno."),
            ],
            "en": [
                ("Why do I have to enter the date?", "Because every region, state or district sets its own, and it changes every year. 8 June is only a placeholder: replace it with the date on your school calendar."),
                ("How many school days are really left?", "Look at \"Working days (Mon–Fri)\" and subtract public holidays and your school's closures."),
                ("Does the count include the last day?", "No: it counts the whole days left. The evening before it shows \"1 day\"."),
            ],
        },
    },
    {
        "id": "countdown_compleanno", "icon": "🎂", "cfg": {"type": "birthday"},
        "slug": {"it": "quanti-giorni-mancano-al-mio-compleanno", "en": "days-until-my-birthday"},
        "title": {"it": "Quanti giorni mancano al mio compleanno?", "en": "How many days until my birthday?"},
        "event": {"it": "il tuo compleanno", "en": "your birthday"},
        "short": {"it": "Inserisci la data di nascita: giorni al prossimo compleanno e anni che compi", "en": "Enter your date of birth: days to your next birthday and the age you'll turn"},
        "keywords": {"it": ["compleanno", "prossimo compleanno", "quanto manca al mio compleanno", "conto alla rovescia compleanno"], "en": ["birthday countdown", "days until my birthday", "next birthday"]},
        "meta": {
            "it": "Quanti giorni mancano al tuo compleanno? Inserisci la data di nascita: il calcolatore trova il prossimo compleanno, conta giorni, settimane, ore e minuti e ti dice quanti anni compirai e in che giorno della settimana.",
            "en": "How many days until your birthday? Enter your date of birth: the calculator finds your next birthday, counts days, weeks, hours and minutes and tells you the age you'll turn and the weekday.",
        },
        "intro": {
            "it": "Scrivi la tua data di nascita: il calcolatore trova il prossimo compleanno, conta i giorni che mancano e ti dice quanti anni compirai.",
            "en": "Type your date of birth: the calculator finds your next birthday, counts the days left and tells you how old you'll turn.",
        },
        "article": {
            "it": """
<h2>Come funziona</h2>
<p>Dalla data di nascita il calcolatore prende giorno e mese e cerca la prossima volta che ricorrono: se il compleanno di quest'anno è già passato, conta fino a quello dell'anno prossimo. Il giorno del compleanno il risultato è «È oggi!». Sotto il numero grande leggi il giorno della settimana e gli anni che compirai; la riga con ore, minuti e secondi si aggiorna da sola.</p>
<h2>Nati il 29 febbraio</h2>
<p>Negli anni non bisestili il 29 febbraio non esiste: il calcolatore in quel caso conta fino al 1° marzo, cioè al giorno successivo al 28 febbraio, che è la scelta più usata anche dagli uffici anagrafe.</p>
<h2>Idee</h2>
<ul>
<li><strong>Festa:</strong> i giorni lavorativi che restano sono quelli utili per prenotare il locale e ordinare la torta.</li>
<li><strong>Lista dei regali:</strong> copia la frase con il conteggio e mandala a chi ti chiede sempre «quando è il tuo compleanno?».</li>
<li><strong>Età esatta:</strong> per sapere quanti anni, mesi e giorni hai oggi usa lo strumento «Calcolo età».</li>
</ul>
""",
            "en": """
<h2>How it works</h2>
<p>From your date of birth the calculator takes the day and month and looks for the next time they come round: if this year's birthday has already passed, it counts down to next year's. On your birthday the result is "It's today!". Under the big number you can read the weekday and the age you'll turn; the line with hours, minutes and seconds updates on its own.</p>
<h2>Born on 29 February?</h2>
<p>In non-leap years 29 February doesn't exist: the calculator then counts down to 1 March, the day after 28 February, which is the most common convention.</p>
<h2>Ideas</h2>
<ul>
<li><strong>Party:</strong> the working days left are the ones you can use to book a venue and order the cake.</li>
<li><strong>Wish list:</strong> copy the sentence with the count and send it to whoever keeps asking "when is your birthday?".</li>
<li><strong>Exact age:</strong> to know your age today in years, months and days use the "Age calculator".</li>
</ul>
""",
        },
        "faq": {
            "it": [
                ("I miei dati vengono salvati?", "No: la data resta nel tuo browser e sparisce quando chiudi la pagina. Nulla viene inviato a un server."),
                ("Posso usarlo per il compleanno di un'altra persona?", "Certo: inserisci la sua data di nascita e vedrai quanti anni compirà e quanti giorni mancano."),
                ("Che succede se oggi è il mio compleanno?", "Il risultato mostra «È oggi!» e il conteggio delle ore si ferma."),
            ],
            "en": [
                ("Is my data saved?", "No: the date stays in your browser and disappears when you close the page. Nothing is sent to a server."),
                ("Can I use it for someone else's birthday?", "Of course: enter their date of birth and you'll see the age they'll turn and the days left."),
                ("What if today is my birthday?", "The result shows \"It's today!\" and the hours counter stops."),
            ],
        },
    },
]


def _others_html(lang, exclude_id, all_pages, rel="../"):
    """Chip list linking to the other countdown pages (used inside the article)."""
    items = []
    for p in all_pages:
        if p["id"] == exclude_id:
            continue
        items.append('<a class="btn small" href="%s%s/">%s %s</a>' % (rel, p["slug"][lang], p["icon"], p["title"][lang].rstrip("?")))
    return '<h2>%s</h2><p class="btns">%s</p>' % (BASE_STRINGS[lang]["others"], " ".join(items))


def _a(event):
    """Italian 'a' + article contraction: 'il Black Friday' -> 'al Black Friday', 'la Befana' -> 'alla Befana'."""
    for art, al in (("il ", "al "), ("lo ", "allo "), ("la ", "alla "), ("l'", "all'"), ("i ", "ai "), ("gli ", "agli "), ("le ", "alle ")):
        if event.startswith(art):
            return al + event[len(art):]
    return "a " + event


def _strings(p, lang):
    s = dict(BASE_STRINGS[lang])
    ev = p["event"][lang]
    if lang == "it":
        s["share"] = s["share"].replace("a {event}", _a(ev))
        s["share_past"] = s["share_past"].replace("{event}", ev[0].upper() + ev[1:])
    for k in ("share", "share_today", "share_past"):
        s[k] = s[k].replace("{event}", ev)
    return s


def make_tool(p, all_pages):
    cfg = dict(p["cfg"])
    if cfg["type"] in ("fixed", "easter", "blackfriday"):
        ui = UI_FIXED
    elif cfg["type"] == "birthday":
        ui = UI_BIRTHDAY
    else:
        ui = UI_CUSTOM
    article = {lang: p["article"][lang] + _others_html(lang, p["id"], all_pages) for lang in ("it", "en")}
    return {
        "id": p["id"], "cat": "date", "icon": p["icon"],
        "slug": p["slug"], "title": p["title"], "short": p["short"], "keywords": p["keywords"],
        "meta": p["meta"], "intro": p["intro"], "seo_title": p.get("seo_title"),
        "strings": {"it": _strings(p, "it"), "en": _strings(p, "en")},
        "ui": ui,
        "js": JS.replace("__CFG__", json.dumps(cfg)),
        "article": article,
        "faq": p["faq"],
        "home": p.get("home", False),
    }


GENERIC = {
    "id": "countdown", "icon": "⏳", "cfg": {"type": "generic"},
    "slug": {"it": "quanti-giorni-mancano", "en": "days-until"},
    "title": {"it": "Quanti giorni mancano a una data?", "en": "How many days until a date?"},
    "event": {"it": "quella data", "en": "that date"},
    "short": {"it": "Conto alla rovescia a qualsiasi data: giorni, settimane, ore e secondi", "en": "Countdown to any date: days, weeks, hours and seconds"},
    "keywords": {"it": ["conto alla rovescia", "countdown", "quanto manca", "giorni mancanti", "quanti giorni sono passati", "natale", "capodanno", "befana", "san valentino", "carnevale", "pasqua", "estate", "ferragosto", "halloween", "scuola", "compleanno"], "en": ["countdown", "days until", "how long until", "days left", "days since", "christmas", "new year", "epiphany", "valentine", "carnival", "easter", "summer", "ferragosto", "halloween", "school", "birthday"]},
    "home": True,
    "meta": {
        "it": "Quanti giorni mancano a una data? Conto alla rovescia a qualsiasi giorno con giorni, settimane, ore, minuti e secondi in tempo reale, giorni lavorativi e giorno della settimana. Pagine pronte per Natale, Capodanno, Pasqua, estate e altre feste.",
        "en": "How many days until a date? Live countdown to any day with days, weeks, hours, minutes and seconds, working days and weekday. Ready-made pages for Christmas, New Year, Easter, summer and more.",
    },
    "intro": {
        "it": "Scegli una data: il calcolatore conta i giorni, le settimane, le ore e i secondi che mancano (o che sono passati) e ti dice in che giorno della settimana cade. Per le feste più cercate ci sono le pagine pronte qui sotto.",
        "en": "Pick a date: the calculator counts the days, weeks, hours and seconds left (or passed) and tells you the weekday. For the most popular events there are ready-made pages below.",
    },
    "article": {
        "it": """
<h2>Come funziona il conto alla rovescia</h2>
<p>Il numero grande sono i giorni interi tra oggi e la data scelta, oggi escluso: il giorno prima dell'evento mancano «1 giorno», il giorno stesso compare «È oggi!». Se la data è nel passato, il calcolatore ti dice quanti giorni sono passati. La riga con ore, minuti e secondi arriva alla mezzanotte di inizio della data e si aggiorna da sola; il conteggio usa l'ora del tuo dispositivo.</p>
<h2>Cosa trovi nel riquadro</h2>
<ul>
<li><strong>Settimane e giorni:</strong> lo stesso numero espresso in settimane intere più i giorni che avanzano.</li>
<li><strong>Ore:</strong> i giorni moltiplicati per 24.</li>
<li><strong>Giorni lavorativi:</strong> quelli da lunedì a venerdì, senza togliere le festività.</li>
<li><strong>Giorno dell'anno di oggi:</strong> a che punto dell'anno siamo (1 = 1° gennaio).</li>
</ul>
<h2>Esempi</h2>
<ul>
<li><strong>Quanti giorni mancano alle vacanze, a un esame, a un matrimonio, a una scadenza:</strong> inserisci la data.</li>
<li><strong>Quanti giorni sono passati dal 1° gennaio, da un evento, dall'inizio di una dieta:</strong> inserisci una data passata.</li>
<li><strong>Feste e ricorrenze:</strong> usa le pagine pronte, che trovano da sole la data giusta ogni anno, Pasqua e Carnevale compresi.</li>
</ul>
""",
        "en": """
<h2>How the countdown works</h2>
<p>The big number is the whole days between today and the chosen date, today excluded: the day before the event "1 day" is left, on the day itself "It's today!" appears. If the date is in the past, the calculator tells you how many days have passed. The line with hours, minutes and seconds runs to midnight at the start of the date and updates on its own, using your device's clock.</p>
<h2>What's in the box</h2>
<ul>
<li><strong>Weeks and days:</strong> the same number as whole weeks plus the remaining days.</li>
<li><strong>Hours:</strong> the days multiplied by 24.</li>
<li><strong>Working days:</strong> Monday to Friday, without removing public holidays.</li>
<li><strong>Today's day of the year:</strong> where we are in the year (1 = 1 January).</li>
</ul>
<h2>Examples</h2>
<ul>
<li><strong>Days until a holiday, an exam, a wedding, a deadline:</strong> enter the date.</li>
<li><strong>Days since 1 January, since an event, since the start of a diet:</strong> enter a past date.</li>
<li><strong>Holidays and celebrations:</strong> use the ready-made pages, which find the right date every year by themselves, Easter and Carnival included.</li>
</ul>
""",
    },
    "faq": {
        "it": [
            ("Il giorno di oggi è compreso nel conteggio?", "No: si contano i giorni interi che mancano. Se vuoi contare anche oggi, aggiungi 1."),
            ("Vengono tolte le festività dai giorni lavorativi?", "No, solo sabato e domenica. Per un conteggio con le festività italiane usa «Giorni tra due date» e sottrai i festivi a mano."),
            ("Posso contare i giorni da una data passata?", "Sì: inserisci una data precedente a oggi e il calcolatore mostra quanti giorni sono passati."),
        ],
        "en": [
            ("Is today included in the count?", "No: it counts the whole days left. If you want to include today, add 1."),
            ("Are public holidays removed from the working days?", "No, only Saturdays and Sundays. Use \"Days between two dates\" and subtract holidays by hand if you need to."),
            ("Can I count the days since a past date?", "Yes: enter a date before today and the calculator shows how many days have passed."),
        ],
    },
}

_ALL = [GENERIC] + PRESETS


def _generic_tool():
    t = make_tool(GENERIC, _ALL)
    # the generic page uses a free date input
    t["ui"] = UI_CUSTOM
    t["js"] = JS.replace("__CFG__", json.dumps({"type": "generic"}))
    t["strings"]["it"].update({"share": "Mancano {n} al {when}", "share_today": "È oggi, {when}!", "share_past": "Sono passati {n} dal {when}"})
    t["strings"]["en"].update({"share": "{n} to go until {when}", "share_today": "It's today, {when}!", "share_past": "{n} have passed since {when}"})
    return t


TOOLS = [_generic_tool()] + [make_tool(p, _ALL) for p in PRESETS]

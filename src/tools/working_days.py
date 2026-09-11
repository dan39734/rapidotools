"""Giorni lavorativi tra due date (festività nazionali italiane + santo patrono) e scadenze in giorni lavorativi."""
import datetime as _dt

# --- build-time helpers (same rules as the page script) ---------------------------------------
MONTHS = {
    "it": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
}
WEEKDAYS = {
    "it": ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"],
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
}
HOLIDAY_NAMES = {
    "it": {"newyear": "Capodanno", "epiphany": "Epifania", "easter": "Pasqua", "eastermon": "Lunedì dell'Angelo (Pasquetta)",
           "liberation": "Festa della Liberazione", "labour": "Festa del Lavoro", "republic": "Festa della Repubblica",
           "assumption": "Ferragosto (Assunzione)", "francis": "San Francesco d'Assisi", "allsaints": "Ognissanti",
           "immaculate": "Immacolata Concezione", "christmas": "Natale", "stephen": "Santo Stefano"},
    "en": {"newyear": "New Year's Day", "epiphany": "Epiphany", "easter": "Easter Sunday", "eastermon": "Easter Monday (Pasquetta)",
           "liberation": "Liberation Day", "labour": "Labour Day", "republic": "Republic Day",
           "assumption": "Assumption Day (Ferragosto)", "francis": "St Francis of Assisi", "allsaints": "All Saints' Day",
           "immaculate": "Immaculate Conception", "christmas": "Christmas Day", "stephen": "St Stephen's Day"},
}


def _easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mo = (h + l - 7 * m + 114) // 31
    da = (h + l - 7 * m + 114) % 31 + 1
    return _dt.date(y, mo, da)


def _holidays(y):
    e = _easter(y)
    out = [(_dt.date(y, 1, 1), "newyear"), (_dt.date(y, 1, 6), "epiphany"), (e, "easter"), (e + _dt.timedelta(days=1), "eastermon"),
           (_dt.date(y, 4, 25), "liberation"), (_dt.date(y, 5, 1), "labour"), (_dt.date(y, 6, 2), "republic"),
           (_dt.date(y, 8, 15), "assumption")]
    if y >= 2026:
        out.append((_dt.date(y, 10, 4), "francis"))
    out += [(_dt.date(y, 11, 1), "allsaints"), (_dt.date(y, 12, 8), "immaculate"), (_dt.date(y, 12, 25), "christmas"),
            (_dt.date(y, 12, 26), "stephen")]
    return sorted(out)


def _workdays_month(y, m):
    hol = {d for d, _ in _holidays(y)}
    d, n = _dt.date(y, m, 1), 0
    while d.month == m:
        if d.weekday() < 5 and d not in hol:
            n += 1
        d += _dt.timedelta(days=1)
    return n


def _fmt_day(d, lang):
    if lang == "it":
        return "%s %s %s" % (WEEKDAYS["it"][d.weekday()], "1°" if d.day == 1 else d.day, MONTHS["it"][d.month - 1])
    return "%s %d %s" % (WEEKDAYS["en"][d.weekday()], d.day, MONTHS["en"][d.month - 1])


def _holiday_table(lang, years=(2026, 2027)):
    head = "<tr><th>%s</th>%s</tr>" % ("Festività" if lang == "it" else "Holiday", "".join("<th>%d</th>" % y for y in years))
    rows = []
    keys = [k for _, k in _holidays(years[-1])]
    for k in keys:
        cells = []
        for y in years:
            match = [d for d, kk in _holidays(y) if kk == k]
            if match:
                d = match[0]
                weekend = d.weekday() >= 5
                cells.append("<td>%s%s</td>" % (_fmt_day(d, lang), " ✱" if weekend else ""))
            else:
                cells.append("<td>–</td>")
        rows.append("<tr><td>%s</td>%s</tr>" % (HOLIDAY_NAMES[lang][k], "".join(cells)))
    return '<div class="table-wrap"><table>%s%s</table></div>' % (head, "".join(rows))


def _month_table(lang, years=(2026, 2027)):
    head = "<tr><th>%s</th>%s</tr>" % ("Mese" if lang == "it" else "Month", "".join("<th>%d</th>" % y for y in years))
    rows = []
    for m in range(1, 13):
        rows.append("<tr><td>%s</td>%s</tr>" % (MONTHS[lang][m - 1].capitalize(), "".join("<td>%d</td>" % _workdays_month(y, m) for y in years)))
    tot = "<tr><td><strong>%s</strong></td>%s</tr>" % ("Totale" if lang == "it" else "Total", "".join(
        "<td><strong>%d</strong></td>" % sum(_workdays_month(y, m) for m in range(1, 13)) for y in years))
    return '<div class="table-wrap"><table>%s%s%s</table></div>' % (head, "".join(rows), tot)


def _year_total(y):
    return sum(_workdays_month(y, m) for m in range(1, 13))


def _sept_example():
    d, wend, work = _dt.date(2026, 9, 1), 0, 0
    hol = {x for x, _ in _holidays(2026)}
    while d.month == 9:
        if d.weekday() >= 5:
            wend += 1
        elif d not in hol:
            work += 1
        d += _dt.timedelta(days=1)
    return wend, work


_SEPT_WEND, _SEPT_WORK = _sept_example()
_T26, _T27 = _year_total(2026), _year_total(2027)
_E26, _E27 = _easter(2026) + _dt.timedelta(days=1), _easter(2027) + _dt.timedelta(days=1)

# patron saints of the main cities (source: it.wikipedia «Santi patroni cattolici delle città capoluogo di provincia italiane»)
CITIES = [
    ["ancona", "Ancona", "Ancona", 5, 4, "San Ciriaco"],
    ["bari", "Bari", "Bari", 12, 6, "San Nicola"],
    ["bergamo", "Bergamo", "Bergamo", 8, 26, "Sant'Alessandro"],
    ["bologna", "Bologna", "Bologna", 10, 4, "San Petronio"],
    ["brescia", "Brescia", "Brescia", 2, 15, "Santi Faustino e Giovita"],
    ["cagliari", "Cagliari", "Cagliari", 10, 30, "San Saturnino"],
    ["catania", "Catania", "Catania", 2, 5, "Sant'Agata"],
    ["firenze", "Firenze", "Florence", 6, 24, "San Giovanni Battista"],
    ["genova", "Genova", "Genoa", 6, 24, "San Giovanni Battista"],
    ["lecce", "Lecce", "Lecce", 8, 26, "Sant'Oronzo"],
    ["messina", "Messina", "Messina", 6, 3, "Madonna della Lettera"],
    ["milano", "Milano", "Milan", 12, 7, "Sant'Ambrogio"],
    ["modena", "Modena", "Modena", 1, 31, "San Geminiano"],
    ["napoli", "Napoli", "Naples", 9, 19, "San Gennaro"],
    ["padova", "Padova", "Padua", 6, 13, "Sant'Antonio"],
    ["palermo", "Palermo", "Palermo", 7, 15, "Santa Rosalia"],
    ["parma", "Parma", "Parma", 1, 13, "Sant'Ilario"],
    ["pescara", "Pescara", "Pescara", 10, 10, "San Cetteo"],
    ["pisa", "Pisa", "Pisa", 6, 17, "San Ranieri"],
    ["reggio-calabria", "Reggio Calabria", "Reggio Calabria", 4, 23, "San Giorgio"],
    ["roma", "Roma", "Rome", 6, 29, "Santi Pietro e Paolo"],
    ["salerno", "Salerno", "Salerno", 9, 21, "San Matteo"],
    ["taranto", "Taranto", "Taranto", 5, 10, "San Cataldo"],
    ["torino", "Torino", "Turin", 6, 24, "San Giovanni Battista"],
    ["trento", "Trento", "Trento", 6, 26, "San Vigilio"],
    ["trieste", "Trieste", "Trieste", 11, 3, "San Giusto"],
    ["udine", "Udine", "Udine", 7, 12, "Santi Ermacora e Fortunato"],
    ["venezia", "Venezia", "Venice", 4, 25, "San Marco"],
    ["verona", "Verona", "Verona", 5, 21, "San Zeno"],
]

_JS = r"""
var CITIES = __CITIES__;
var CITY = {}; CITIES.forEach(function (c) { CITY[c[0]] = c; });
var mode = 'range', out = RT.$('#out'), err = RT.$('#err');
var d1 = RT.$('#d1'), d2 = RT.$('#d2'), start = RT.$('#start'), nIn = RT.$('#n'), back = RT.$('#back');
var week = RT.$('#week'), psel = RT.$('#patron'), pdate = RT.$('#pdate'), pwrap = RT.$('#pwrap'), hpd = RT.$('#hpd');
// fill the patron menu (alphabetical in the page language)
(function () {
  var it = RT.lang === 'it', list = CITIES.slice().sort(function (a, b) { return (it ? a[1] : a[2]).localeCompare(it ? b[1] : b[2]); });
  list.forEach(function (c) {
    var o = document.createElement('option'); o.value = c[0];
    var day = RT.date(new Date(2000, c[3] - 1, c[4]), { day: 'numeric', month: 'long' });
    o.textContent = it ? c[1] + ' – ' + c[5] + ' (' + day + ')' : c[2] + ' (' + day + ')';
    psel.appendChild(o);
  });
  var o = document.createElement('option'); o.value = 'custom'; o.textContent = T.patron_custom; psel.appendChild(o);
})();
function easter(y) { // Gregorian computus (Meeus/Jones/Butcher)
  var a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25),
      g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4,
      l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451),
      mo = Math.floor((h + l - 7 * m + 114) / 31), da = ((h + l - 7 * m + 114) % 31) + 1;
  return new Date(y, mo - 1, da);
}
var HC = {};
function holidays(y) {
  if (HC[y]) return HC[y];
  var h = {};
  function add(m, d, name) { h[m + '-' + d] = name; }
  add(1, 1, T.h_newyear); add(1, 6, T.h_epiphany);
  var e = easter(y), em = new Date(y, e.getMonth(), e.getDate() + 1);
  add(e.getMonth() + 1, e.getDate(), T.h_easter); add(em.getMonth() + 1, em.getDate(), T.h_eastermon);
  add(4, 25, T.h_liberation); add(5, 1, T.h_labour); add(6, 2, T.h_republic); add(8, 15, T.h_assumption);
  if (y >= 2026) add(10, 4, T.h_francis);
  add(11, 1, T.h_allsaints); add(12, 8, T.h_immaculate); add(12, 25, T.h_christmas); add(12, 26, T.h_stephen);
  return (HC[y] = h);
}
function patron() {
  var v = psel.value;
  pwrap.classList.toggle('hide', v !== 'custom');
  if (!v) return null;
  if (v === 'custom') { var p = RT.parseDate(pdate.value); return p ? { m: p.getMonth() + 1, d: p.getDate(), name: T.h_patron } : null; }
  var c = CITY[v]; return { m: c[3], d: c[4], name: T.h_patron_of.replace('{s}', c[5]).replace('{c}', RT.lang === 'it' ? c[1] : c[2]) };
}
function info(d, P) {
  var wd = d.getDay(), m = d.getMonth() + 1, day = d.getDate();
  var name = holidays(d.getFullYear())[m + '-' + day] || null;
  if (P && P.m === m && P.d === day) name = name ? name + ' + ' + P.name : P.name;
  var weekend = wd === 0 || (wd === 6 && week.value === '5');
  return { hol: name, weekend: weekend, work: !weekend && !name };
}
function pl(n, one, many) { return RT.fmt(n, 0) + ' ' + (n === 1 ? one : many); }
function full(d) { return RT.weekday(d) + ' ' + RT.date(d); }
function table(rows) {
  var body = RT.$('#list'); body.innerHTML = '';
  rows.forEach(function (r) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td></td><td></td><td></td>';
    tr.children[0].textContent = full(r[0]); tr.children[1].textContent = r[1];
    tr.children[2].textContent = r[2] ? T.on_weekend : T.lost; tr.children[2].className = r[2] ? 'msg' : 'msg warn';
    body.appendChild(tr);
  });
  RT.$('#listwrap').classList.toggle('hide', !rows.length);
  RT.$('#nolist').classList.toggle('hide', rows.length > 0);
}
function fail(msg) { out.classList.add('hide'); err.textContent = msg || ''; err.classList.toggle('hide', !msg); }
function calcRange() {
  var a = RT.parseDate(d1.value), b = RT.parseDate(d2.value);
  if (!a || !b) return fail('');
  if (b < a) { var t = a; a = b; b = t; }
  var total = RT.daysBetween(a, b) + 1;
  if (total > 36600) return fail(T.too_long);
  var P = patron(), work = 0, wend = 0, hol = 0, rows = [], cur = new Date(a.getFullYear(), a.getMonth(), a.getDate());
  for (var i = 0; i < total; i++) {
    var r = info(cur, P);
    if (r.work) work++; else if (r.weekend) wend++; else hol++;
    if (r.hol && rows.length < 80) rows.push([new Date(cur), r.hol, r.weekend]);
    cur.setDate(cur.getDate() + 1);
  }
  fail('');
  RT.$('#main').textContent = pl(work, T.wday, T.wdays);
  RT.$('#sub').textContent = T.range_sub.replace('{a}', full(a)).replace('{b}', full(b));
  RT.$('#s1').textContent = RT.fmt(total, 0); RT.$('#l1').textContent = T.total;
  RT.$('#s2').textContent = RT.fmt(wend, 0); RT.$('#l2').textContent = week.value === '5' ? T.weekends5 : T.weekends6;
  RT.$('#s3').textContent = RT.fmt(hol, 0); RT.$('#l3').textContent = T.hol_lost;
  var h = RT.num(hpd.value); if (!isFinite(h) || h < 0) h = 0;
  RT.$('#s4').textContent = RT.fmt(work * h, 2); RT.$('#l4').textContent = T.hours.replace('{h}', RT.fmt(h, 2));
  table(rows); out.classList.remove('hide');
}
function calcAdd() {
  var s = RT.parseDate(start.value), n = RT.num(nIn.value);
  if (!s || !isFinite(n)) return fail('');
  n = Math.round(n);
  if (n < 1 || n > 5000) return fail(T.bad_n);
  var P = patron(), cur = new Date(s.getFullYear(), s.getMonth(), s.getDate()), step = back.checked ? -1 : 1, count = 0, wend = 0, hol = 0, rows = [];
  while (count < n) {
    cur.setDate(cur.getDate() + step);
    var r = info(cur, P);
    if (r.work) count++; else if (r.weekend) wend++; else hol++;
    if (r.hol && !r.work && rows.length < 80) rows.push([new Date(cur), r.hol, r.weekend]);
  }
  fail('');
  RT.$('#main').textContent = full(cur);
  RT.$('#sub').textContent = (back.checked ? T.add_sub_back : T.add_sub).replace('{n}', pl(n, T.wday, T.wdays)).replace('{d}', full(s));
  RT.$('#s1').textContent = RT.fmt(Math.abs(RT.daysBetween(s, cur)), 0); RT.$('#l1').textContent = T.cal_days;
  RT.$('#s2').textContent = RT.fmt(wend, 0); RT.$('#l2').textContent = week.value === '5' ? T.weekends5 : T.weekends6;
  RT.$('#s3').textContent = RT.fmt(hol, 0); RT.$('#l3').textContent = T.hol_skipped;
  RT.$('#s4').textContent = RT.date(cur, { day: '2-digit', month: '2-digit', year: 'numeric' }); RT.$('#l4').textContent = T.short_date;
  table(rows); out.classList.remove('hide');
}
function calc() { if (mode === 'range') calcRange(); else calcAdd(); }
RT.$$('.tabs button').forEach(function (b) {
  b.addEventListener('click', function () {
    RT.$$('.tabs button').forEach(function (x) { x.classList.toggle('on', x === b); });
    mode = b.getAttribute('data-tab');
    RT.$('#tab-range').classList.toggle('hide', mode !== 'range'); RT.$('#tab-add').classList.toggle('hide', mode !== 'add');
    calc();
  });
});
d1.value = RT.isoToday();
var t0 = new Date(); var end = new Date(t0.getFullYear(), t0.getMonth() + 1, 0);
if (RT.daysBetween(t0, end) < 7) end = new Date(t0.getFullYear(), t0.getMonth() + 2, 0);
d2.value = end.getFullYear() + '-' + RT.pad(end.getMonth() + 1) + '-' + RT.pad(end.getDate());
start.value = RT.isoToday();
RT.$('#today').addEventListener('click', function () { d1.value = RT.isoToday(); calc(); });
RT.live(document.getElementById('tool'), calc);
"""

TOOL = {
    "id": "working_days",
    "cat": "date",
    "icon": "🗓️",
    "slug": {"it": "calcolo-giorni-lavorativi", "en": "working-days-calculator-italy"},
    "title": {"it": "Calcolo giorni lavorativi (con festività italiane)", "en": "Working days calculator with Italian public holidays"},
    "short": {"it": "Giorni lavorativi tra due date senza weekend, festivi e santo patrono", "en": "Working days between two dates, excluding weekends and Italian holidays"},
    "keywords": {
        "it": ["giorni lavorativi", "giorni feriali", "giorni festivi", "festività 2026", "festività 2027", "santo patrono", "scadenza giorni lavorativi", "pasquetta", "4 ottobre"],
        "en": ["business days", "working days italy", "italian public holidays", "workdays between dates", "add business days", "italy holidays 2026"],
    },
    "meta": {
        "it": "Calcola i giorni lavorativi tra due date togliendo sabati, domeniche, festività nazionali italiane (anche il 4 ottobre dal 2026) e santo patrono. Trova la scadenza dopo N giorni lavorativi. Tabelle 2026 e 2027.",
        "en": "Count the working days between two dates excluding weekends, Italian public holidays (including 4 October from 2026) and the local patron saint's day. Find the date N working days ahead. Tables for 2026 and 2027.",
    },
    "intro": {
        "it": "Scegli due date: il calcolatore conta i giorni lavorativi togliendo weekend e festività nazionali, ti dice quali festivi cadono nel periodo e quante ore di lavoro ci sono. Con la seconda scheda trovi la data che cade dopo un certo numero di giorni lavorativi.",
        "en": "Pick two dates to count the working days without weekends and Italian public holidays, see which holidays fall in the period and how many working hours there are. The second tab finds the date a given number of working days ahead.",
    },
    "strings": {
        "it": {
            "tab_range": "Tra due date", "tab_add": "Aggiungi giorni lavorativi", "from": "Data di inizio", "to": "Data di fine", "today": "Oggi",
            "start": "Data di partenza", "ndays": "Giorni lavorativi da aggiungere", "back": "Conta all'indietro (prima della data)",
            "week": "Settimana lavorativa", "week5": "Lunedì–venerdì", "week6": "Lunedì–sabato",
            "patron": "Santo patrono (facoltativo)", "patron_none": "Nessuno", "patron_custom": "Altra data…", "pdate": "Giorno della festa patronale (vale ogni anno)",
            "hpd_l": "Ore di lavoro al giorno",
            "wday": "giorno lavorativo", "wdays": "giorni lavorativi",
            "range_sub": "Da {a} a {b}, compresi entrambi",
            "add_sub": "{n} dopo {d} (la data di partenza non si conta)", "add_sub_back": "{n} prima di {d} (la data di partenza non si conta)",
            "total": "Giorni di calendario", "cal_days": "Giorni di calendario trascorsi", "weekends5": "Sabati e domeniche", "weekends6": "Domeniche",
            "hol_lost": "Festivi in giorni lavorativi", "hol_skipped": "Festivi saltati", "hours": "Ore di lavoro ({h} al giorno)", "short_date": "Data in cifre",
            "list_t": "Festività nel periodo", "col_date": "Data", "col_name": "Festività", "col_state": "Effetto",
            "lost": "giorno lavorativo in meno", "on_weekend": "cade nel fine settimana", "none": "Nessuna festività nel periodo.",
            "too_long": "Periodo troppo lungo: scegli al massimo 100 anni.", "bad_n": "Inserisci un numero di giorni tra 1 e 5000.",
            "h_newyear": "Capodanno", "h_epiphany": "Epifania", "h_easter": "Pasqua", "h_eastermon": "Lunedì dell'Angelo (Pasquetta)",
            "h_liberation": "Festa della Liberazione", "h_labour": "Festa del Lavoro", "h_republic": "Festa della Repubblica",
            "h_assumption": "Ferragosto (Assunzione)", "h_francis": "San Francesco d'Assisi", "h_allsaints": "Ognissanti",
            "h_immaculate": "Immacolata Concezione", "h_christmas": "Natale", "h_stephen": "Santo Stefano",
            "h_patron": "Santo patrono", "h_patron_of": "Santo patrono: {s} ({c})",
        },
        "en": {
            "tab_range": "Between two dates", "tab_add": "Add working days", "from": "Start date", "to": "End date", "today": "Today",
            "start": "Starting date", "ndays": "Working days to add", "back": "Count backwards (before the date)",
            "week": "Working week", "week5": "Monday–Friday", "week6": "Monday–Saturday",
            "patron": "Patron saint's day (optional)", "patron_none": "None", "patron_custom": "Other date…", "pdate": "Patron saint's day (repeats every year)",
            "hpd_l": "Working hours per day",
            "wday": "working day", "wdays": "working days",
            "range_sub": "From {a} to {b}, both included",
            "add_sub": "{n} after {d} (the starting date is not counted)", "add_sub_back": "{n} before {d} (the starting date is not counted)",
            "total": "Calendar days", "cal_days": "Calendar days elapsed", "weekends5": "Saturdays and Sundays", "weekends6": "Sundays",
            "hol_lost": "Holidays on working days", "hol_skipped": "Holidays skipped", "hours": "Working hours ({h} a day)", "short_date": "Date in figures",
            "list_t": "Holidays in the period", "col_date": "Date", "col_name": "Holiday", "col_state": "Effect",
            "lost": "one working day less", "on_weekend": "falls on the weekend", "none": "No public holidays in the period.",
            "too_long": "The period is too long: choose at most 100 years.", "bad_n": "Enter a number of days between 1 and 5000.",
            "h_newyear": "New Year's Day", "h_epiphany": "Epiphany", "h_easter": "Easter Sunday", "h_eastermon": "Easter Monday (Pasquetta)",
            "h_liberation": "Liberation Day", "h_labour": "Labour Day", "h_republic": "Republic Day",
            "h_assumption": "Assumption Day (Ferragosto)", "h_francis": "St Francis of Assisi", "h_allsaints": "All Saints' Day",
            "h_immaculate": "Immaculate Conception", "h_christmas": "Christmas Day", "h_stephen": "St Stephen's Day",
            "h_patron": "Patron saint's day", "h_patron_of": "Patron saint's day: {c} ({s})",
        },
    },
    "ui": """
<div class="tabs" role="tablist">
  <button type="button" class="on" data-tab="range">{{tab_range}}</button>
  <button type="button" data-tab="add">{{tab_add}}</button>
</div>
<div id="tab-range">
  <div class="row">
    <div class="field"><label for="d1">{{from}}</label><input type="date" id="d1"></div>
    <div class="field"><label for="d2">{{to}}</label><input type="date" id="d2"></div>
    <div class="field"><label for="hpd">{{hpd_l}}</label><input type="number" id="hpd" min="0" max="24" step="0.5" value="8"></div>
  </div>
  <div class="inline"><button class="btn small" type="button" id="today">{{today}}</button></div>
</div>
<div id="tab-add" class="hide">
  <div class="row">
    <div class="field"><label for="start">{{start}}</label><input type="date" id="start"></div>
    <div class="field"><label for="n">{{ndays}}</label><input type="number" id="n" min="1" max="5000" step="1" value="10"></div>
  </div>
  <label class="check"><input type="checkbox" id="back"> {{back}}</label>
</div>
<div class="row" style="margin-top:12px">
  <div class="field"><label for="week">{{week}}</label><select id="week"><option value="5">{{week5}}</option><option value="6">{{week6}}</option></select></div>
  <div class="field"><label for="patron">{{patron}}</label><select id="patron"><option value="">{{patron_none}}</option></select></div>
  <div class="field hide" id="pwrap"><label for="pdate">{{pdate}}</label><input type="date" id="pdate"></div>
</div>
<p class="msg bad hide" id="err"></p>
<div class="result hide" id="out">
  <div class="big" id="main"></div>
  <div class="sub" id="sub"></div>
  <div class="stats">
    <div class="stat"><b id="s1"></b><span id="l1"></span></div>
    <div class="stat"><b id="s2"></b><span id="l2"></span></div>
    <div class="stat"><b id="s3"></b><span id="l3"></span></div>
    <div class="stat"><b id="s4"></b><span id="l4"></span></div>
  </div>
  <h3 style="font-size:1rem;margin-top:16px">{{list_t}}</h3>
  <div class="table-wrap" id="listwrap"><table><thead><tr><th>{{col_date}}</th><th>{{col_name}}</th><th>{{col_state}}</th></tr></thead><tbody id="list"></tbody></table></div>
  <p class="msg hide" id="nolist">{{none}}</p>
</div>
""",
    "js": _JS.replace("__CITIES__", __import__("json").dumps(CITIES, ensure_ascii=False)),
    "article": {
        "it": f"""
<h2>Come si calcolano i giorni lavorativi</h2>
<p>Si contano tutti i giorni dalla data di inizio alla data di fine, <strong>compresi entrambi</strong>, e si tolgono i sabati e le domeniche (solo le domeniche se lavori dal lunedì al sabato) e le festività che cadono in un giorno feriale. Una festività che cade di domenica non toglie nulla, perché quel giorno non si lavorava comunque.</p>
<p><em>Esempio:</em> dal 1° al 30 settembre 2026 ci sono 30 giorni, di cui {_SEPT_WEND} tra sabati e domeniche e nessuna festività: i giorni lavorativi sono <strong>{_SEPT_WORK}</strong>. Con 8 ore al giorno fanno {_SEPT_WORK * 8} ore di lavoro.</p>
<h2>Le festività nazionali in Italia</h2>
<p>In tutta Italia sono festivi il 1° gennaio (Capodanno), il 6 gennaio (Epifania), la Pasqua e il Lunedì dell'Angelo (Pasquetta), il 25 aprile (Liberazione), il 1° maggio (Festa del Lavoro), il 2 giugno (Festa della Repubblica), il 15 agosto (Ferragosto), il 1° novembre (Ognissanti), l'8 dicembre (Immacolata), il 25 e il 26 dicembre (Natale e Santo Stefano). <strong>Dal 2026 è di nuovo festivo anche il 4 ottobre</strong>, San Francesco d'Assisi patrono d'Italia (legge 8 ottobre 2025, n. 151): nel 2026 cade di domenica, dal 2027 vale un giorno di riposo in più. Pasquetta cambia data ogni anno perché segue la Pasqua: il calcolatore la ricava con l'algoritmo del calendario gregoriano.</p>
<p>Le festività del 2026 e del 2027, con il giorno della settimana (✱ = cade di sabato o di domenica):</p>
{_holiday_table("it")}
<h2>Giorni lavorativi mese per mese</h2>
<p>Quanti giorni lavorativi ci sono in ogni mese, con la settimana dal lunedì al venerdì e le festività nazionali (senza santo patrono). Nel 2026 i giorni lavorativi sono <strong>{_T26}</strong>, nel 2027 <strong>{_T27}</strong>.</p>
{_month_table("it")}
<h2>Il santo patrono</h2>
<p>Ogni comune festeggia anche il proprio santo patrono, che in molti contratti di lavoro è un giorno festivo: per esempio il 29 giugno a Roma, il 7 dicembre a Milano, il 19 settembre a Napoli, il 24 giugno a Torino, Firenze e Genova. Scegli la tua città dal menu oppure «Altra data…» e inserisci il giorno della festa patronale del tuo comune: verrà tolto ogni anno, se cade in un giorno lavorativo.</p>
<h2>Scadenze in giorni lavorativi</h2>
<p>Con la scheda «Aggiungi giorni lavorativi» trovi la data che cade N giorni lavorativi dopo (o prima di) una data. La data di partenza non si conta: si parte dal giorno lavorativo successivo. È il modo in cui si calcolano, per esempio, i tempi di consegna o un preavviso espressi «in giorni lavorativi». Per i termini legali e fiscali verifica sempre le regole specifiche: molti si contano in giorni di calendario.</p>
""",
        "en": f"""
<h2>How working days are counted</h2>
<p>The calculator counts every day from the start date to the end date, <strong>both included</strong>, then removes Saturdays and Sundays (only Sundays if you work Monday to Saturday) and the public holidays that fall on a weekday. A holiday that falls on a Sunday removes nothing, because that day was not a working day anyway.</p>
<p><em>Example:</em> from 1 to 30 September 2026 there are 30 days, {_SEPT_WEND} of them Saturdays and Sundays and no holidays: that makes <strong>{_SEPT_WORK}</strong> working days, or {_SEPT_WORK * 8} working hours at 8 hours a day.</p>
<h2>Public holidays in Italy</h2>
<p>Nationwide holidays in Italy are 1 January (New Year's Day), 6 January (Epiphany), Easter Sunday and Easter Monday (Pasquetta), 25 April (Liberation Day), 1 May (Labour Day), 2 June (Republic Day), 15 August (Ferragosto), 1 November (All Saints' Day), 8 December (Immaculate Conception), 25 and 26 December (Christmas and St Stephen's Day). <strong>From 2026, 4 October is a public holiday again</strong>: St Francis of Assisi, patron saint of Italy (Law no. 151 of 8 October 2025). In 2026 it falls on a Sunday; from 2027 it gives an extra day off. Easter Monday moves every year with Easter, which the calculator works out with the Gregorian calendar algorithm.</p>
<p>Italian public holidays in 2026 and 2027 with the day of the week (✱ = falls on a Saturday or Sunday):</p>
{_holiday_table("en")}
<h2>Working days month by month</h2>
<p>Working days in each month with a Monday-to-Friday week and national holidays (no patron saint). Italy has <strong>{_T26}</strong> working days in 2026 and <strong>{_T27}</strong> in 2027.</p>
{_month_table("en")}
<h2>The patron saint's day</h2>
<p>Every Italian town also celebrates its patron saint, a day off under many employment contracts: for example 29 June in Rome, 7 December in Milan, 19 September in Naples, 24 June in Turin, Florence and Genoa. Pick your city from the menu, or choose "Other date…" and enter your town's patron saint's day: it is removed every year when it falls on a working day.</p>
<h2>Deadlines in working days</h2>
<p>The "Add working days" tab finds the date that falls N working days after (or before) a given date. The starting date itself is not counted: counting starts from the next working day. This is how delivery times or notice periods expressed "in working days" are usually worked out. For legal or tax deadlines always check the specific rules: many are counted in calendar days.</p>
""",
    },
    "faq": {
        "it": [
            ("Il 4 ottobre è festivo?", "Sì: dal 2026 il 4 ottobre, San Francesco d'Assisi, è di nuovo festa nazionale (legge n. 151 del 2025). Nel 2026 cade di domenica; nel 2027 cade di lunedì ed è il primo anno in cui toglie un giorno lavorativo."),
            ("Il sabato è un giorno lavorativo?", "Dipende dal tuo orario: nella maggior parte degli uffici no. Se lavori anche il sabato scegli «Lunedì–sabato» e il calcolatore toglierà solo le domeniche e i festivi."),
            ("La data di inizio e quella di fine sono comprese?", "Sì, nel calcolo tra due date sono comprese entrambe. Nella scheda «Aggiungi giorni lavorativi», invece, la data di partenza non si conta."),
            ("Quando cade Pasquetta?", f"Il Lunedì dell'Angelo è il giorno dopo Pasqua e cambia ogni anno: nel 2026 è il {_E26.day} aprile, nel 2027 il {_E27.day} marzo. Il calcolatore lo trova da solo per qualsiasi anno."),
        ],
        "en": [
            ("Is 4 October a public holiday in Italy?", "Yes: from 2026, 4 October (St Francis of Assisi) is a national holiday again (Law no. 151 of 2025). In 2026 it falls on a Sunday; in 2027 it falls on a Monday, the first year it removes a working day."),
            ("Is Saturday a working day?", "It depends on your schedule: for most offices it isn't. If you also work on Saturdays, choose \"Monday–Saturday\" and only Sundays and holidays will be removed."),
            ("Are the start and end dates included?", "Yes, when counting between two dates both are included. In the \"Add working days\" tab the starting date is not counted."),
            ("When is Easter Monday?", f"Easter Monday (Pasquetta) is the day after Easter and moves every year: in 2026 it is {_E26.day} April, in 2027 {_E27.day} March. The calculator works it out for any year."),
        ],
    },
}

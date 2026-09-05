TOOL = {
    "id": "age",
    "cat": "date",
    "icon": "🎂",
    "slug": {"it": "calcolo-eta", "en": "age-calculator"},
    "title": {"it": "Calcolo età", "en": "Age calculator"},
    "short": {"it": "Anni, mesi e giorni esatti da una data di nascita", "en": "Exact years, months and days from a date of birth"},
    "keywords": {"it": ["quanti anni ho", "età esatta", "compleanno", "data di nascita"], "en": ["how old am i", "birthday", "date of birth"]},
    "meta": {
        "it": "Calcola l'età esatta in anni, mesi e giorni da una data di nascita, i giorni totali vissuti e quanto manca al prossimo compleanno. Gratis, senza registrazione.",
        "en": "Work out your exact age in years, months and days from a date of birth, the total days lived and how long until your next birthday. Free, no sign-up.",
    },
    "intro": {
        "it": "Inserisci la data di nascita e scopri subito l'età esatta in anni, mesi e giorni, oltre ai giorni totali e al conto alla rovescia per il prossimo compleanno.",
        "en": "Enter a date of birth to instantly see the exact age in years, months and days, plus total days lived and the countdown to the next birthday.",
    },
    "strings": {
        "it": {
            "dob": "Data di nascita", "at": "Età al giorno", "today": "Oggi",
            "years": "anni", "months": "mesi", "days": "giorni", "weeks": "settimane", "hours": "ore",
            "total_days": "Giorni totali", "total_weeks": "Settimane totali", "total_months": "Mesi totali",
            "next_bd": "Prossimo compleanno", "in_days": "tra {n} giorni", "today_bd": "È oggi: auguri! 🎉",
            "born_on": "Nato/a di", "turning": "compirai {n} anni", "err": "La data di nascita deve essere precedente alla data scelta.",
            "y1": "anno", "m1": "mese", "d1": "giorno",
        },
        "en": {
            "dob": "Date of birth", "at": "Age on", "today": "Today",
            "years": "years", "months": "months", "days": "days", "weeks": "weeks", "hours": "hours",
            "total_days": "Total days", "total_weeks": "Total weeks", "total_months": "Total months",
            "next_bd": "Next birthday", "in_days": "in {n} days", "today_bd": "It's today: happy birthday! 🎉",
            "born_on": "Born on a", "turning": "turning {n}", "err": "The date of birth must be before the chosen date.",
            "y1": "year", "m1": "month", "d1": "day",
        },
    },
    "ui": """
<div class="row">
  <div class="field"><label for="dob">{{dob}}</label><input type="date" id="dob" max="2100-12-31"></div>
  <div class="field"><label for="at">{{at}}</label><input type="date" id="at"></div>
</div>
<p class="msg bad hide" id="err">{{err}}</p>
<div class="result hide" id="out">
  <div class="big" id="main"></div>
  <div class="sub" id="born"></div>
  <div class="stats">
    <div class="stat"><b id="tdays"></b><span>{{total_days}}</span></div>
    <div class="stat"><b id="tweeks"></b><span>{{total_weeks}}</span></div>
    <div class="stat"><b id="tmonths"></b><span>{{total_months}}</span></div>
    <div class="stat"><b id="nbd"></b><span>{{next_bd}}</span></div>
  </div>
</div>
""",
    "js": r"""
var dob = RT.$('#dob'), at = RT.$('#at'), out = RT.$('#out'), err = RT.$('#err');
at.value = RT.isoToday();
function plural(n, one, many) { return n + ' ' + (n === 1 ? one : many); }
function calc() {
  var b = RT.parseDate(dob.value), a = RT.parseDate(at.value);
  if (!b || !a) { out.classList.add('hide'); err.classList.add('hide'); return; }
  if (a < b) { out.classList.add('hide'); err.classList.remove('hide'); return; }
  err.classList.add('hide');
  var y = a.getFullYear() - b.getFullYear(), m = a.getMonth() - b.getMonth(), d = a.getDate() - b.getDate();
  if (d < 0) { m--; d += new Date(a.getFullYear(), a.getMonth(), 0).getDate(); }
  if (m < 0) { y--; m += 12; }
  var total = RT.daysBetween(b, a);
  RT.$('#main').textContent = plural(y, T.y1, T.years) + ', ' + plural(m, T.m1, T.months) + ', ' + plural(d, T.d1, T.days);
  RT.$('#born').textContent = T.born_on + ' ' + RT.weekday(b) + ' (' + RT.date(b) + ')';
  RT.$('#tdays').textContent = RT.fmt(total, 0);
  RT.$('#tweeks').textContent = RT.fmt(Math.floor(total / 7), 0);
  RT.$('#tmonths').textContent = RT.fmt(y * 12 + m, 0);
  var nb = new Date(a.getFullYear(), b.getMonth(), b.getDate());
  if (nb.getMonth() !== b.getMonth()) nb = new Date(a.getFullYear(), b.getMonth() + 1, 0);
  if (nb <= a) { nb = new Date(a.getFullYear() + 1, b.getMonth(), b.getDate()); if (nb.getMonth() !== b.getMonth()) nb = new Date(a.getFullYear() + 1, b.getMonth() + 1, 0); }
  var left = RT.daysBetween(a, nb);
  var same = a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
  RT.$('#nbd').textContent = same ? T.today_bd : T.in_days.replace('{n}', left) + ' · ' + T.turning.replace('{n}', nb.getFullYear() - b.getFullYear());
  out.classList.remove('hide');
}
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>Come funziona il calcolo dell'età</h2>
<p>L'età «anagrafica» si conta in anni compiuti: si diventa più vecchi di un anno solo al compleanno, non prima. Questo calcolatore fa la stessa cosa, ma aggiunge anche i mesi e i giorni trascorsi dall'ultimo compleanno, così sai esattamente quanto tempo è passato dalla nascita. Per esempio, una persona nata il 15 marzo 1990 ha, il 5 settembre 2026, 36 anni, 5 mesi e 21 giorni.</p>
<p>Il campo «Età al giorno» è impostato su oggi, ma puoi cambiarlo per sapere quanti anni avevi (o avrai) in una data qualsiasi: utile per documenti, concorsi, iscrizioni e limiti di età.</p>
<h2>Cosa significano i numeri</h2>
<ul>
<li><strong>Anni, mesi, giorni:</strong> gli anni compiuti, i mesi interi passati dall'ultimo compleanno e i giorni rimanenti.</li>
<li><strong>Giorni totali:</strong> tutti i giorni vissuti, contando gli anni bisestili. Una persona di 30 anni ha vissuto circa 10.957 giorni.</li>
<li><strong>Settimane e mesi totali:</strong> gli stessi giorni espressi in settimane intere e in mesi compiuti.</li>
<li><strong>Prossimo compleanno:</strong> quanti giorni mancano e quanti anni compirai.</li>
</ul>
<h2>Anni bisestili e 29 febbraio</h2>
<p>Il calcolo tiene conto degli anni bisestili: i giorni totali sono esatti. Chi è nato il 29 febbraio, negli anni non bisestili, festeggia il compleanno il 28 febbraio: il calcolatore segue la stessa regola per il conto alla rovescia.</p>
""",
        "en": """
<h2>How the age calculation works</h2>
<p>Your "official" age is counted in completed years: you turn a year older only on your birthday, not before. This calculator does the same, but also adds the months and days elapsed since your last birthday, so you know exactly how much time has passed since you were born. For example, someone born on 15 March 1990 is, on 5 September 2026, 36 years, 5 months and 21 days old.</p>
<p>The "Age on" field defaults to today, but you can change it to find out how old you were (or will be) on any date: handy for forms, applications, enrolments and age limits.</p>
<h2>What the numbers mean</h2>
<ul>
<li><strong>Years, months, days:</strong> completed years, whole months since the last birthday, and the remaining days.</li>
<li><strong>Total days:</strong> every day lived, leap years included. A 30-year-old has lived about 10,957 days.</li>
<li><strong>Total weeks and months:</strong> the same span expressed in whole weeks and completed months.</li>
<li><strong>Next birthday:</strong> how many days are left and what age you will turn.</li>
</ul>
<h2>Leap years and 29 February</h2>
<p>The calculation accounts for leap years, so the total days are exact. People born on 29 February celebrate on 28 February in non-leap years; the countdown follows the same rule.</p>
""",
    },
    "faq": {
        "it": [
            ("Come si calcola l'età esatta?", "Si contano gli anni compiuti, poi i mesi interi trascorsi dall'ultimo compleanno e infine i giorni rimanenti. Il calcolatore fa tutto in automatico, tenendo conto della lunghezza dei mesi e degli anni bisestili."),
            ("Quanti giorni ha vissuto una persona di 18 anni?", "Circa 6.574 giorni (18 anni × 365,25 giorni). Inserisci la data di nascita per avere il numero esatto."),
            ("Posso calcolare l'età a una data futura?", "Sì: cambia il campo «Età al giorno» con la data che ti interessa, per esempio quella di un concorso o di una scadenza."),
        ],
        "en": [
            ("How is exact age calculated?", "Count the completed years, then the whole months since the last birthday, then the remaining days. The calculator does it automatically, taking month lengths and leap years into account."),
            ("How many days has an 18-year-old lived?", "About 6,574 days (18 years × 365.25 days). Enter the date of birth to get the exact number."),
            ("Can I calculate age on a future date?", "Yes: change the \"Age on\" field to the date you are interested in, such as an exam or a deadline."),
        ],
    },
}

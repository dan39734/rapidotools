TOOL = {
    "id": "loan",
    "cat": "money",
    "icon": "🏠",
    "slug": {"it": "calcolo-rata-mutuo", "en": "loan-calculator"},
    "title": {"it": "Calcolo rata mutuo e prestito", "en": "Loan and mortgage payment calculator"},
    "short": {"it": "Rata mensile, interessi totali e piano di ammortamento", "en": "Monthly payment, total interest and amortisation schedule"},
    "keywords": {"it": ["rata mutuo", "simulazione mutuo", "piano di ammortamento", "interessi prestito", "tasso fisso", "quanto pago al mese"], "en": ["mortgage payment", "monthly payment", "amortization schedule", "loan interest", "fixed rate"]},
    "meta": {
        "it": "Calcola la rata mensile di un mutuo o prestito a tasso fisso, il totale degli interessi e il piano di ammortamento completo (metodo francese). Gratis e senza registrazione.",
        "en": "Calculate the monthly payment on a fixed-rate mortgage or loan, the total interest and the full amortisation schedule. Free, no sign-up.",
    },
    "intro": {
        "it": "Inserisci importo, tasso annuo e durata: ottieni la rata mensile, quanto pagherai in tutto e quanto di interessi, con il piano di ammortamento mese per mese.",
        "en": "Enter the amount, annual rate and term to get the monthly payment, the total you will repay, the total interest, and a month-by-month amortisation schedule.",
    },
    "strings": {
        "it": {
            "amount": "Importo del finanziamento", "rate": "Tasso annuo (TAN) %", "years": "Durata (anni)", "months": "Mesi aggiuntivi", "payment": "Rata mensile", "total": "Totale da restituire", "interest": "Interessi totali",
            "schedule": "Mostra piano di ammortamento", "hide": "Nascondi piano", "n": "Rata", "quota_i": "Interessi", "quota_c": "Capitale", "residuo": "Debito residuo", "year": "Anno",
            "note": "Il calcolo usa il metodo francese (rata costante) e non include spese, assicurazioni e imposte: il TAEG reale sarà leggermente più alto.",
        },
        "en": {
            "amount": "Loan amount", "rate": "Annual interest rate %", "years": "Term (years)", "months": "Extra months", "payment": "Monthly payment", "total": "Total repaid", "interest": "Total interest",
            "schedule": "Show amortisation schedule", "hide": "Hide schedule", "n": "Payment", "quota_i": "Interest", "quota_c": "Principal", "residuo": "Balance", "year": "Year",
            "note": "The calculation uses a standard fixed-payment (annuity) formula and excludes fees, insurance and taxes: the real APR will be slightly higher.",
        },
    },
    "ui": """
<div class="row">
  <div class="field"><label for="amt">{{amount}}</label><input type="text" inputmode="decimal" id="amt" value="150000"></div>
  <div class="field"><label for="rate">{{rate}}</label><input type="text" inputmode="decimal" id="rate" value="3.5"></div>
</div>
<div class="row">
  <div class="field"><label for="yrs">{{years}}</label><input type="text" inputmode="numeric" id="yrs" value="25"></div>
  <div class="field"><label for="mos">{{months}}</label><input type="text" inputmode="numeric" id="mos" value="0"></div>
</div>
<div class="result hide" id="out">
  <div class="sub">{{payment}}</div><div class="big" id="pmt"></div>
  <div class="stats"><div class="stat"><b id="tot"></b><span>{{total}}</span></div><div class="stat"><b id="int"></b><span>{{interest}}</span></div></div>
  <div class="btns"><button class="btn small" type="button" id="toggle">{{schedule}}</button></div>
  <div class="table-wrap hide" id="sched" style="max-height:420px;overflow:auto;margin-top:10px"><table><thead><tr><th>{{n}}</th><th>{{quota_i}}</th><th>{{quota_c}}</th><th>{{residuo}}</th></tr></thead><tbody id="rows"></tbody></table></div>
</div>
<p class="msg">{{note}}</p>
""",
    "js": r"""
var out = RT.$('#out'), sched = RT.$('#sched'), rows = RT.$('#rows'), toggle = RT.$('#toggle');
var open = false;
toggle.addEventListener('click', function () { open = !open; sched.classList.toggle('hide', !open); toggle.textContent = open ? T.hide : T.schedule; if (open) calc(); });
function calc() {
  var P = RT.num(RT.$('#amt').value), r = RT.num(RT.$('#rate').value) / 100 / 12, n = Math.round((RT.num(RT.$('#yrs').value) || 0) * 12 + (RT.num(RT.$('#mos').value) || 0));
  if (!(P > 0) || !(n > 0) || !isFinite(r) || r < 0) { out.classList.add('hide'); return; }
  var pmt = r === 0 ? P / n : P * r / (1 - Math.pow(1 + r, -n));
  RT.$('#pmt').textContent = RT.money(pmt); RT.$('#tot').textContent = RT.money(pmt * n); RT.$('#int').textContent = RT.money(pmt * n - P);
  out.classList.remove('hide');
  if (open) {
    var bal = P, html = '', yi = 0, yc = 0;
    for (var i = 1; i <= n; i++) {
      var ip = bal * r, cp = pmt - ip; bal = Math.max(0, bal - cp); yi += ip; yc += cp;
      html += '<tr><td>' + i + '</td><td>' + RT.money(ip) + '</td><td>' + RT.money(cp) + '</td><td>' + RT.money(bal) + '</td></tr>';
      if (i % 12 === 0 || i === n) { html += '<tr style="background:var(--soft);font-weight:600"><td>' + T.year + ' ' + Math.ceil(i / 12) + '</td><td>' + RT.money(yi) + '</td><td>' + RT.money(yc) + '</td><td></td></tr>'; yi = 0; yc = 0; }
    }
    rows.innerHTML = html;
  }
}
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>Come si calcola la rata</h2>
<p>Per un mutuo o un prestito a tasso fisso con rata costante (il cosiddetto ammortamento «alla francese», usato da quasi tutte le banche italiane) la formula è:</p>
<p><strong>Rata = C × i ÷ (1 − (1 + i)<sup>−n</sup>)</strong>, dove C è il capitale, i il tasso mensile (tasso annuo ÷ 12) e n il numero di rate.</p>
<p>Esempio: 150.000 € al 3,5% per 25 anni. Tasso mensile 0,2917%, 300 rate: rata di circa <strong>751 €</strong>, per un totale di 225.300 € di cui 75.300 € di interessi.</p>
<h2>Leggere il piano di ammortamento</h2>
<p>Ogni rata è composta da una quota di interessi e una quota di capitale. All'inizio gli interessi sono alti perché il debito è grande; col passare degli anni la quota capitale cresce e gli interessi calano. Per questo estinguere in anticipo conviene di più nei primi anni, e per questo dopo 5 anni di un mutuo venticinquennale hai restituito molto meno di un quinto del capitale.</p>
<h2>TAN, TAEG e costi accessori</h2>
<p>Il calcolatore usa il <strong>TAN</strong> (tasso annuo nominale). Il <strong>TAEG</strong> include anche spese di istruttoria, perizia, assicurazioni obbligatorie e imposte, ed è il numero giusto per confrontare le offerte di banche diverse. Per un mutuo casa in Italia ci sono anche l'imposta sostitutiva (0,25% per la prima casa) e le spese notarili.</p>
<h2>Quanto incide la durata</h2>
<p>Allungare la durata abbassa la rata ma aumenta molto gli interessi totali: gli stessi 150.000 € al 3,5% costano 75.300 € di interessi in 25 anni e circa 92.500 € in 30 anni. Prova durate diverse per trovare l'equilibrio tra rata sostenibile e costo complessivo. Come regola prudente, la rata non dovrebbe superare un terzo del reddito mensile netto.</p>
""",
        "en": """
<h2>How the payment is calculated</h2>
<p>For a fixed-rate mortgage or loan with a constant payment (a standard amortising loan) the formula is:</p>
<p><strong>Payment = P × i ÷ (1 − (1 + i)<sup>−n</sup>)</strong>, where P is the principal, i the monthly rate (annual rate ÷ 12) and n the number of payments.</p>
<p>Example: 150,000 at 3.5% over 25 years. Monthly rate 0.2917%, 300 payments: a payment of about <strong>751</strong>, for a total of 225,300 of which 75,300 is interest.</p>
<h2>Reading the amortisation schedule</h2>
<p>Every payment is made up of an interest part and a principal part. Early on, interest is high because the balance is large; over the years the principal part grows and the interest shrinks. That is why paying off early saves more in the first years, and why after 5 years of a 25-year mortgage you have repaid far less than a fifth of the principal.</p>
<h2>Interest rate vs APR</h2>
<p>The calculator uses the nominal annual interest rate. The <strong>APR</strong> also includes arrangement fees, valuation, compulsory insurance and taxes, and is the right number for comparing offers from different lenders. Depending on the country there may be additional closing costs, notary or stamp duty.</p>
<h2>How much the term matters</h2>
<p>A longer term lowers the payment but greatly increases the total interest: the same 150,000 at 3.5% costs 75,300 in interest over 25 years and about 92,500 over 30 years. Try different terms to find the balance between an affordable payment and the overall cost. As a prudent rule, the payment should not exceed a third of your net monthly income.</p>
""",
    },
    "faq": {
        "it": [
            ("Il calcolo vale anche per prestiti personali e finanziamenti auto?", "Sì: la formula della rata costante è la stessa per mutui, prestiti personali e finanziamenti. Inserisci importo, TAN e durata."),
            ("Perché la rata reale della banca è un po' diversa?", "Perché la banca può usare giorni effettivi invece di mesi uguali, arrotondare in modo diverso e aggiungere spese e assicurazioni. La differenza è di solito di pochi euro."),
            ("Come uso il piano di ammortamento?", "Premi «Mostra piano di ammortamento»: per ogni rata vedi quota interessi, quota capitale e debito residuo, con i totali di ogni anno. Il debito residuo ti dice quanto dovresti pagare per estinguere il mutuo in quel momento."),
        ],
        "en": [
            ("Does this work for personal and car loans too?", "Yes: the constant-payment formula is the same for mortgages, personal loans and financing. Enter the amount, the interest rate and the term."),
            ("Why is my lender's payment slightly different?", "Because lenders may count actual days instead of equal months, round differently and add fees and insurance. The difference is usually a few units of currency."),
            ("How do I use the amortisation schedule?", "Press \"Show amortisation schedule\": for every payment you see the interest part, the principal part and the remaining balance, with yearly totals. The balance tells you how much you would need to pay to settle the loan at that point."),
        ],
    },
}

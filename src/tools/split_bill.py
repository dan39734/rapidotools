TOOL = {
    "id": "split_bill",
    "cat": "money",
    "icon": "🍽️",
    "slug": {"it": "dividi-il-conto", "en": "split-bill-calculator"},
    "title": {"it": "Dividi il conto e calcola la mancia", "en": "Split the bill and calculate the tip"},
    "short": {"it": "Quanto paga ciascuno, con mancia e arrotondamento", "en": "How much each person pays, with tip and rounding"},
    "keywords": {"it": ["conto alla romana", "calcolo mancia", "dividere spesa", "quota a testa"], "en": ["tip calculator", "bill splitter", "per person", "gratuity"]},
    "meta": {
        "it": "Dividi il conto del ristorante tra amici in un attimo: quota a testa, mancia in percentuale, arrotondamento e totale. Funziona anche offline, dal telefono.",
        "en": "Split a restaurant bill between friends in seconds: per-person share, percentage tip, rounding and total. Works offline, on your phone.",
    },
    "intro": {
        "it": "Inserisci il totale del conto, in quanti siete e l'eventuale mancia: ottieni subito quanto deve mettere ciascuno, con l'opzione di arrotondare per non litigare sugli spiccioli.",
        "en": "Enter the bill total, how many of you there are and the tip, if any: you get each person's share instantly, with an option to round up so nobody argues over small change.",
    },
    "strings": {
        "it": {
            "total": "Totale del conto", "people": "Numero di persone", "tip": "Mancia %", "round": "Arrotonda la quota a testa", "r0": "No", "r1": "A 1 €", "r5": "A 5 €", "r05": "A 0,50 €",
            "each": "A testa", "tip_total": "Mancia totale", "grand": "Totale con mancia", "extra": "Con l'arrotondamento la mancia diventa", "quick": "Mancia rapida", "q125": "12,5%",
        },
        "en": {
            "total": "Bill total", "people": "Number of people", "tip": "Tip %", "round": "Round each share", "r0": "No", "r1": "To 1", "r5": "To 5", "r05": "To 0.50",
            "each": "Per person", "tip_total": "Total tip", "grand": "Total with tip", "extra": "With rounding the tip becomes", "quick": "Quick tip", "q125": "12.5%",
        },
    },
    "ui": """
<div class="row">
  <div class="field"><label for="tot">{{total}}</label><input type="text" inputmode="decimal" id="tot" value="86.50"></div>
  <div class="field"><label for="ppl">{{people}}</label><input type="number" inputmode="numeric" id="ppl" value="4" min="1"></div>
  <div class="field"><label for="tip">{{tip}}</label><input type="text" inputmode="decimal" id="tip" value="0"></div>
</div>
<div class="inline"><span class="lbl">{{quick}}:</span>
  <button class="btn small" type="button" data-t="0">0%</button><button class="btn small" type="button" data-t="5">5%</button><button class="btn small" type="button" data-t="10">10%</button>
  <button class="btn small" type="button" data-t="12.5">{{q125}}</button><button class="btn small" type="button" data-t="15">15%</button><button class="btn small" type="button" data-t="18">18%</button><button class="btn small" type="button" data-t="20">20%</button></div>
<div class="field" style="margin-top:12px"><label for="round">{{round}}</label><select id="round"><option value="0">{{r0}}</option><option value="0.5">{{r05}}</option><option value="1">{{r1}}</option><option value="5">{{r5}}</option></select></div>
<div class="result hide" id="out">
  <div class="sub">{{each}}</div><div class="big" id="each"></div>
  <div class="stats"><div class="stat"><b id="tipt"></b><span>{{tip_total}}</span></div><div class="stat"><b id="grand"></b><span>{{grand}}</span></div></div>
  <p class="msg hide" id="extra"></p>
</div>
""",
    "js": r"""
var out = RT.$('#out');
function calc() {
  var tot = RT.num(RT.$('#tot').value), n = parseInt(RT.$('#ppl').value, 10), tip = RT.num(RT.$('#tip').value) || 0, step = +RT.$('#round').value;
  if (!(tot >= 0) || !(n >= 1)) { out.classList.add('hide'); return; }
  var tipAmt = tot * tip / 100, grand = tot + tipAmt, each = grand / n;
  var extra = RT.$('#extra'); extra.classList.add('hide');
  if (step > 0) { var r = Math.ceil(each / step - 1e-9) * step; if (r > each + 1e-9) { extra.textContent = T.extra + ' ' + RT.money(r * n - tot) + ' (' + RT.fmt((r * n - tot) / tot * 100, 1) + '%)'; extra.classList.remove('hide'); } each = r; grand = r * n; tipAmt = grand - tot; }
  RT.$('#each').textContent = RT.money(each); RT.$('#tipt').textContent = RT.money(tipAmt); RT.$('#grand').textContent = RT.money(grand);
  out.classList.remove('hide');
}
RT.$$('[data-t]').forEach(function (b) { b.addEventListener('click', function () { RT.$('#tip').value = b.getAttribute('data-t'); calc(); }); });
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>Come funziona</h2>
<p>Il conto viene diviso in parti uguali («alla romana»): totale più mancia, diviso per il numero di persone. Se scegli un arrotondamento, la quota a testa viene arrotondata per eccesso alla cifra scelta (50 centesimi, 1 o 5 euro) e la differenza va ad aumentare la mancia: il calcolatore ti mostra quanto diventa, così decidi se ti sta bene.</p>
<h2>La mancia in Italia e all'estero</h2>
<p>In Italia la mancia non è obbligatoria: il servizio è spesso incluso nel «coperto» o nel prezzo, e lasciare qualche euro o arrotondare è un gesto apprezzato ma facoltativo. All'estero le abitudini cambiano molto: negli Stati Uniti si lascia il 15-20% del conto prima delle tasse, e non lasciarla è considerato scortese; nel Regno Unito il 10-12,5% se il servizio non è già in conto; in Germania e Austria si arrotonda o si lascia il 5-10%; in Giappone non si lascia mancia.</p>
<h2>Consigli pratici</h2>
<ul>
<li>Se qualcuno ha ordinato molto meno degli altri, dividere in parti uguali può essere ingiusto: calcola prima la sua quota a parte e sottraila dal totale.</li>
<li>Per i pagamenti con app o bonifico, arrotondare a 1 € evita decimali scomodi.</li>
<li>Controlla se sullo scontrino il servizio è già incluso: in quel caso la mancia è un extra.</li>
</ul>
""",
        "en": """
<h2>How it works</h2>
<p>The bill is split into equal shares: total plus tip, divided by the number of people. If you choose a rounding option, each share is rounded up to the chosen amount (0.50, 1 or 5) and the difference goes towards the tip: the calculator shows what the tip becomes, so you can decide whether that suits you.</p>
<h2>Tipping customs</h2>
<p>Tipping habits vary a lot. In the United States 15-20% of the pre-tax bill is customary at restaurants, and leaving nothing is considered rude; in the United Kingdom 10-12.5% when service is not already added; in Germany and Austria people round up or leave 5-10%; in Italy and Spain tipping is optional, with a couple of euros or rounding up as a nice gesture; in Japan tips are not expected and may even be refused.</p>
<h2>Practical tips</h2>
<ul>
<li>If someone ordered much less than the others, equal shares can be unfair: work out their part separately and subtract it from the total first.</li>
<li>For app or bank payments, rounding to 1 avoids awkward decimals.</li>
<li>Check whether a service charge is already on the receipt: in that case the tip is an extra.</li>
</ul>
""",
    },
    "faq": {
        "it": [
            ("Come si divide un conto in modo equo?", "Il modo più semplice è dividere in parti uguali. Se le ordinazioni sono molto diverse, ognuno paga il suo e si divide solo ciò che è stato condiviso (antipasti, bevande, coperto)."),
            ("Quanta mancia si lascia in Italia?", "Non c'è una regola: è facoltativa. Molti arrotondano o lasciano il 5-10% quando il servizio è stato particolarmente buono."),
            ("L'arrotondamento aumenta la mancia?", "Sì: la differenza tra la quota arrotondata per eccesso e quella esatta va ad aggiungersi alla mancia, e il calcolatore te la mostra."),
        ],
        "en": [
            ("How do you split a bill fairly?", "The simplest way is equal shares. If orders differ a lot, everyone pays for their own and only shared items (starters, drinks, service) are divided."),
            ("How much should I tip?", "It depends on the country: 15-20% in the US, 10-12.5% in the UK when service is not included, rounding up or 5-10% in much of Europe."),
            ("Does rounding increase the tip?", "Yes: the difference between the rounded-up share and the exact one is added to the tip, and the calculator shows it."),
        ],
    },
}

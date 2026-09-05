TOOL = {
    "id": "discount",
    "cat": "numbers",
    "icon": "🏷️",
    "slug": {"it": "calcolo-sconto", "en": "discount-calculator"},
    "title": {"it": "Calcolo sconto", "en": "Discount calculator"},
    "short": {"it": "Prezzo finale e risparmio con uno o due sconti, o sconto a partire dai prezzi", "en": "Final price and savings with one or two discounts, or the discount from two prices"},
    "keywords": {"it": ["prezzo scontato", "saldi", "sconto del 30%", "doppio sconto", "quanto risparmio"], "en": ["sale price", "30% off", "double discount", "how much do i save", "percent off"]},
    "meta": {
        "it": "Calcola il prezzo scontato e quanto risparmi con uno sconto in percentuale, anche con un secondo sconto extra, oppure scopri lo sconto applicato tra prezzo pieno e prezzo finale.",
        "en": "Work out the sale price and how much you save with a percentage discount, even with an extra second discount, or find the discount applied between full and final price.",
    },
    "intro": {
        "it": "Scrivi il prezzo e lo sconto: vedi subito il prezzo finale e il risparmio. Puoi aggiungere un secondo sconto (come nei saldi «extra 20%») o calcolare la percentuale di sconto partendo dai due prezzi.",
        "en": "Enter the price and the discount to instantly see the final price and your savings. Add a second discount (like an 'extra 20%' sale) or work out the discount percentage from the two prices.",
    },
    "strings": {
        "it": {
            "tab1": "Prezzo scontato", "tab2": "Sconto tra due prezzi", "price": "Prezzo pieno", "disc": "Sconto %", "disc2": "Secondo sconto % (facoltativo)",
            "final": "Prezzo finale", "save": "Risparmi", "eff": "Sconto effettivo totale", "full": "Prezzo pieno", "paid": "Prezzo finale", "discount": "Sconto applicato", "per": "Risparmio",
            "quick": "Sconti rapidi",
        },
        "en": {
            "tab1": "Sale price", "tab2": "Discount between two prices", "price": "Full price", "disc": "Discount %", "disc2": "Second discount % (optional)",
            "final": "Final price", "save": "You save", "eff": "Effective total discount", "full": "Full price", "paid": "Final price", "discount": "Discount applied", "per": "Savings",
            "quick": "Quick discounts",
        },
    },
    "ui": """
<div class="tabs"><button type="button" class="on" data-tab="1">{{tab1}}</button><button type="button" data-tab="2">{{tab2}}</button></div>
<div id="tab-1">
  <div class="row">
    <div class="field"><label for="price">{{price}}</label><input type="text" inputmode="decimal" id="price" value="80"></div>
    <div class="field"><label for="disc">{{disc}}</label><input type="text" inputmode="decimal" id="disc" value="30"></div>
    <div class="field"><label for="disc2">{{disc2}}</label><input type="text" inputmode="decimal" id="disc2" value=""></div>
  </div>
  <div class="inline"><span class="lbl">{{quick}}:</span>
    <button class="btn small" type="button" data-d="10">10%</button><button class="btn small" type="button" data-d="15">15%</button><button class="btn small" type="button" data-d="20">20%</button>
    <button class="btn small" type="button" data-d="25">25%</button><button class="btn small" type="button" data-d="30">30%</button><button class="btn small" type="button" data-d="40">40%</button>
    <button class="btn small" type="button" data-d="50">50%</button><button class="btn small" type="button" data-d="70">70%</button></div>
  <div class="result">
    <div class="sub">{{final}}</div><div class="big" id="final"></div>
    <div class="stats"><div class="stat"><b id="save"></b><span>{{save}}</span></div><div class="stat"><b id="eff"></b><span>{{eff}}</span></div></div>
  </div>
</div>
<div id="tab-2" class="hide">
  <div class="row">
    <div class="field"><label for="full">{{full}}</label><input type="text" inputmode="decimal" id="full" value="120"></div>
    <div class="field"><label for="paid">{{paid}}</label><input type="text" inputmode="decimal" id="paid" value="89.90"></div>
  </div>
  <div class="result">
    <div class="sub">{{discount}}</div><div class="big" id="pct"></div>
    <div class="stats"><div class="stat"><b id="saved"></b><span>{{per}}</span></div></div>
  </div>
</div>
""",
    "js": r"""
var tabs = RT.$$('.tabs button');
tabs.forEach(function (b) { b.addEventListener('click', function () { tabs.forEach(function (x) { x.classList.toggle('on', x === b); }); RT.$('#tab-1').classList.toggle('hide', b.getAttribute('data-tab') !== '1'); RT.$('#tab-2').classList.toggle('hide', b.getAttribute('data-tab') !== '2'); }); });
function calc() {
  var p = RT.num(RT.$('#price').value), d = RT.num(RT.$('#disc').value), d2 = RT.num(RT.$('#disc2').value);
  if (isFinite(p) && isFinite(d)) {
    var f = p * (1 - d / 100); if (isFinite(d2)) f = f * (1 - d2 / 100);
    RT.$('#final').textContent = RT.money(f); RT.$('#save').textContent = RT.money(p - f); RT.$('#eff').textContent = p ? RT.fmt((p - f) / p * 100, 2) + ' %' : '–';
  } else { RT.$('#final').textContent = '–'; RT.$('#save').textContent = '–'; RT.$('#eff').textContent = '–'; }
  var full = RT.num(RT.$('#full').value), paid = RT.num(RT.$('#paid').value);
  if (isFinite(full) && isFinite(paid) && full > 0) { RT.$('#pct').textContent = RT.fmt((full - paid) / full * 100, 2) + ' %'; RT.$('#saved').textContent = RT.money(full - paid); }
  else { RT.$('#pct').textContent = '–'; RT.$('#saved').textContent = '–'; }
}
RT.$$('[data-d]').forEach(function (b) { b.addEventListener('click', function () { RT.$('#disc').value = b.getAttribute('data-d'); calc(); }); });
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>Come si calcola uno sconto</h2>
<p>Il prezzo scontato si ottiene moltiplicando il prezzo pieno per (100 − sconto) ÷ 100. Un capo da 80 € con il 30% di sconto costa 80 × 0,70 = <strong>56 €</strong>, e risparmi 24 €. In alternativa calcola prima lo sconto (80 × 30 ÷ 100 = 24) e sottrailo.</p>
<h2>Il doppio sconto non si somma</h2>
<p>Nei saldi capita di vedere «−30% e un ulteriore −20% alla cassa». Il totale non è il 50%: il secondo sconto si applica al prezzo già ribassato. Da 80 € si passa a 56 €, poi a 56 × 0,80 = <strong>44,80 €</strong>, cioè uno sconto effettivo del 44%. Il calcolatore mostra proprio lo sconto effettivo totale, così non ti fai ingannare.</p>
<h2>Trovare lo sconto da due prezzi</h2>
<p>Se conosci il prezzo pieno e quello finale, lo sconto è (pieno − finale) ÷ pieno × 100. Da 120 € a 89,90 € lo sconto è del 25,08%. Utile per confrontare offerte diverse o per verificare che il cartellino dica il vero.</p>
<h2>Consigli per gli acquisti</h2>
<ul>
<li>Confronta sempre il prezzo finale, non la percentuale: un 40% su un prezzo gonfiato può costare più di un 20% su un prezzo onesto.</li>
<li>Nei negozi online controlla se lo sconto si applica prima o dopo le spese di spedizione.</li>
<li>Per gli sconti a mente: il 25% è un quarto, il 50% la metà, il 10% si trova spostando la virgola.</li>
</ul>
""",
        "en": """
<h2>How a discount is calculated</h2>
<p>The sale price is the full price multiplied by (100 − discount) ÷ 100. An $80 item at 30% off costs 80 × 0.70 = <strong>$56</strong>, and you save $24. Alternatively, work out the discount first (80 × 30 ÷ 100 = 24) and subtract it.</p>
<h2>Double discounts don't add up</h2>
<p>Sales often advertise "30% off plus an extra 20% at checkout". The total is not 50%: the second discount applies to the already reduced price. From $80 you go to $56, then to 56 × 0.80 = <strong>$44.80</strong>, an effective discount of 44%. The calculator shows exactly that effective total discount, so you are not misled.</p>
<h2>Finding the discount from two prices</h2>
<p>If you know the full price and the final price, the discount is (full − final) ÷ full × 100. From $120 to $89.90 the discount is 25.08%. Handy for comparing offers or checking that a price tag tells the truth.</p>
<h2>Shopping tips</h2>
<ul>
<li>Always compare the final price, not the percentage: 40% off an inflated price can cost more than 20% off an honest one.</li>
<li>In online shops, check whether the discount applies before or after shipping costs.</li>
<li>For mental maths: 25% is a quarter, 50% is half, 10% is the number with the decimal point moved one place.</li>
</ul>
""",
    },
    "faq": {
        "it": [
            ("Come si calcola il 30% di sconto su un prezzo?", "Moltiplica il prezzo per 0,70 (cioè 100% − 30%). Su 80 € ottieni 56 €."),
            ("Due sconti del 20% fanno il 40%?", "No: il secondo si applica al prezzo già scontato, quindi due sconti del 20% equivalgono al 36% (0,8 × 0,8 = 0,64)."),
            ("Il calcolatore gestisce i centesimi?", "Sì, i risultati sono mostrati con due decimali e nella valuta della lingua scelta; puoi inserire i decimali con la virgola o con il punto."),
        ],
        "en": [
            ("How do I take 30% off a price?", "Multiply the price by 0.70 (that is 100% − 30%). On $80 you get $56."),
            ("Do two 20% discounts equal 40%?", "No: the second applies to the already discounted price, so two 20% discounts equal 36% (0.8 × 0.8 = 0.64)."),
            ("Does the calculator handle cents?", "Yes, results are shown with two decimals; you can enter decimals with a point or a comma."),
        ],
    },
}

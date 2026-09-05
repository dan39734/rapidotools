TOOL = {
    "id": "percentage",
    "cat": "numbers",
    "icon": "％",
    "slug": {"it": "calcolo-percentuale", "en": "percentage-calculator"},
    "title": {"it": "Calcolo percentuale", "en": "Percentage calculator"},
    "short": {"it": "Quanto è il 20% di 150, che percentuale è 30 su 200, variazione tra due numeri", "en": "What is 20% of 150, what percent is 30 of 200, change between two numbers"},
    "keywords": {"it": ["calcolare la percentuale", "percentuale di un numero", "aumento percentuale", "variazione percentuale"], "en": ["percent of a number", "percentage increase", "percentage change", "percent difference"]},
    "meta": {
        "it": "Calcola la percentuale di un numero, che percentuale è un numero rispetto a un altro, l'aumento o la diminuzione percentuale e il valore con la percentuale aggiunta o tolta. Con formule ed esempi.",
        "en": "Work out a percentage of a number, what percent one number is of another, percentage increase or decrease and a value with a percentage added or removed. With formulas and examples.",
    },
    "intro": {
        "it": "Quattro calcoli in uno: la percentuale di un numero, il rapporto tra due numeri in percentuale, la variazione tra un valore iniziale e uno finale, e un numero aumentato o diminuito di una percentuale.",
        "en": "Four calculations in one: a percentage of a number, one number as a percentage of another, the change between a starting and a final value, and a number increased or decreased by a percentage.",
    },
    "strings": {
        "it": {
            "q1a": "Quanto è il", "q1b": "% di", "q2a": "Il numero", "q2b": "è che percentuale di", "q3a": "Variazione da", "q3b": "a", "q4a": "Il numero", "q4b": "aumentato o diminuito del", "q4c": "% (usa il meno per diminuire)",
            "res": "Risultato", "inc": "Aumento", "dec": "Diminuzione", "of": "di", "is": "è il",
        },
        "en": {
            "q1a": "What is", "q1b": "% of", "q2a": "The number", "q2b": "is what percent of", "q3a": "Change from", "q3b": "to", "q4a": "The number", "q4b": "increased or decreased by", "q4c": "% (use a minus sign to decrease)",
            "res": "Result", "inc": "Increase", "dec": "Decrease", "of": "of", "is": "is",
        },
    },
    "ui": """
<div class="result" style="margin-top:0">
  <div class="inline"><span>{{q1a}}</span><input type="text" inputmode="decimal" id="p1" value="20" style="width:90px"><span>{{q1b}}</span><input type="text" inputmode="decimal" id="n1" value="150" style="width:110px"><span>?</span></div>
  <div class="big" id="r1" style="font-size:1.5rem;margin-top:8px"></div>
</div>
<div class="result">
  <div class="inline"><span>{{q2a}}</span><input type="text" inputmode="decimal" id="a2" value="30" style="width:100px"><span>{{q2b}}</span><input type="text" inputmode="decimal" id="b2" value="200" style="width:110px"><span>?</span></div>
  <div class="big" id="r2" style="font-size:1.5rem;margin-top:8px"></div>
</div>
<div class="result">
  <div class="inline"><span>{{q3a}}</span><input type="text" inputmode="decimal" id="a3" value="80" style="width:100px"><span>{{q3b}}</span><input type="text" inputmode="decimal" id="b3" value="100" style="width:100px"><span>?</span></div>
  <div class="big" id="r3" style="font-size:1.5rem;margin-top:8px"></div>
</div>
<div class="result">
  <div class="inline"><span>{{q4a}}</span><input type="text" inputmode="decimal" id="a4" value="1200" style="width:100px"><span>{{q4b}}</span><input type="text" inputmode="decimal" id="p4" value="15" style="width:80px"><span>{{q4c}}</span></div>
  <div class="big" id="r4" style="font-size:1.5rem;margin-top:8px"></div>
</div>
""",
    "js": r"""
function v(id) { return RT.num(RT.$('#' + id).value); }
function calc() {
  var p1 = v('p1'), n1 = v('n1'); RT.$('#r1').textContent = isFinite(p1 * n1) ? RT.fmt(p1 * n1 / 100, 4) : '–';
  var a2 = v('a2'), b2 = v('b2'); RT.$('#r2').textContent = isFinite(a2 / b2) && b2 !== 0 ? RT.fmt(a2 / b2 * 100, 2) + ' %' : '–';
  var a3 = v('a3'), b3 = v('b3');
  if (isFinite(a3) && isFinite(b3) && a3 !== 0) { var ch = (b3 - a3) / Math.abs(a3) * 100; RT.$('#r3').textContent = (ch >= 0 ? '+' : '−') + RT.fmt(Math.abs(ch), 2) + ' % (' + (ch >= 0 ? T.inc : T.dec) + ' ' + RT.fmt(Math.abs(b3 - a3), 4) + ')'; } else RT.$('#r3').textContent = '–';
  var a4 = v('a4'), p4 = v('p4'); RT.$('#r4').textContent = isFinite(a4 * p4) ? RT.fmt(a4 * (1 + p4 / 100), 4) : '–';
}
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>Le formule</h2>
<ul>
<li><strong>Percentuale di un numero:</strong> numero × percentuale ÷ 100. Il 20% di 150 = 150 × 20 ÷ 100 = <strong>30</strong>.</li>
<li><strong>Che percentuale è A di B:</strong> A ÷ B × 100. 30 su 200 = 30 ÷ 200 × 100 = <strong>15%</strong>.</li>
<li><strong>Variazione percentuale:</strong> (finale − iniziale) ÷ iniziale × 100. Da 80 a 100 = (100 − 80) ÷ 80 × 100 = <strong>+25%</strong>. Da 100 a 80 invece è −20%: la base del calcolo è sempre il valore di partenza, per questo salita e discesa non sono simmetriche.</li>
<li><strong>Aumentare o diminuire di una percentuale:</strong> numero × (1 + percentuale ÷ 100). 1.200 aumentato del 15% = 1.200 × 1,15 = <strong>1.380</strong>; diminuito del 15% = 1.200 × 0,85 = 1.020.</li>
</ul>
<h2>Trucchi per calcolare a mente</h2>
<p>Il 10% si ottiene spostando la virgola di un posto (10% di 240 = 24); il 5% è la metà del 10%; l'1% è un centesimo. Per il 15% somma 10% e 5%: 15% di 240 = 24 + 12 = 36. E ricorda che a% di b è uguale a b% di a: l'8% di 50 è lo stesso del 50% di 8, cioè 4.</p>
<h2>Attenzione ai punti percentuali</h2>
<p>Se un tasso passa dal 2% al 3% è aumentato di <em>un punto percentuale</em>, ma in termini relativi è cresciuto del 50%. Le due cose vengono spesso confuse nelle notizie e nelle pubblicità.</p>
""",
        "en": """
<h2>The formulas</h2>
<ul>
<li><strong>Percentage of a number:</strong> number × percentage ÷ 100. 20% of 150 = 150 × 20 ÷ 100 = <strong>30</strong>.</li>
<li><strong>What percent A is of B:</strong> A ÷ B × 100. 30 out of 200 = 30 ÷ 200 × 100 = <strong>15%</strong>.</li>
<li><strong>Percentage change:</strong> (final − initial) ÷ initial × 100. From 80 to 100 = (100 − 80) ÷ 80 × 100 = <strong>+25%</strong>. From 100 to 80 it is −20%: the base is always the starting value, which is why rises and falls are not symmetrical.</li>
<li><strong>Increase or decrease by a percentage:</strong> number × (1 + percentage ÷ 100). 1,200 increased by 15% = 1,200 × 1.15 = <strong>1,380</strong>; decreased by 15% = 1,200 × 0.85 = 1,020.</li>
</ul>
<h2>Mental-maths shortcuts</h2>
<p>10% is the number with the decimal point moved one place (10% of 240 = 24); 5% is half of 10%; 1% is one hundredth. For 15% add 10% and 5%: 15% of 240 = 24 + 12 = 36. And remember that a% of b equals b% of a: 8% of 50 is the same as 50% of 8, i.e. 4.</p>
<h2>Mind the percentage points</h2>
<p>If a rate goes from 2% to 3% it has risen by <em>one percentage point</em>, but in relative terms it has grown by 50%. The two are often confused in news and advertising.</p>
""",
    },
    "faq": {
        "it": [
            ("Come si calcola la percentuale tra due numeri?", "Dividi il primo numero per il secondo e moltiplica per 100: 45 su 60 = 45 ÷ 60 × 100 = 75%."),
            ("Come calcolo lo sconto in percentuale?", "Usa la variazione: (prezzo scontato − prezzo pieno) ÷ prezzo pieno × 100. Per i prezzi c'è anche il nostro calcolatore di sconto dedicato."),
            ("Posso usare la virgola per i decimali?", "Sì, il calcolatore accetta sia la virgola sia il punto."),
        ],
        "en": [
            ("How do I calculate the percentage between two numbers?", "Divide the first number by the second and multiply by 100: 45 out of 60 = 45 ÷ 60 × 100 = 75%."),
            ("How do I work out a discount percentage?", "Use the change formula: (sale price − full price) ÷ full price × 100. For prices there is also our dedicated discount calculator."),
            ("Can I use a comma for decimals?", "Yes, the calculator accepts both a comma and a point."),
        ],
    },
}

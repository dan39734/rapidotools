TOOL = {
    "id": "bmi",
    "cat": "health",
    "icon": "⚖️",
    "slug": {"it": "calcolo-bmi", "en": "bmi-calculator"},
    "title": {"it": "Calcolo BMI (indice di massa corporea)", "en": "BMI calculator (body mass index)"},
    "short": {"it": "Il tuo indice di massa corporea, la fascia di peso e il peso forma", "en": "Your body mass index, weight category and healthy weight range"},
    "keywords": {"it": ["imc", "indice di massa corporea", "peso forma", "peso ideale", "sovrappeso", "sottopeso"], "en": ["body mass index", "healthy weight", "ideal weight", "overweight", "underweight"]},
    "meta": {
        "it": "Calcola il BMI (indice di massa corporea) da peso e altezza, scopri in quale fascia ti trovi secondo l'OMS e qual è l'intervallo di peso normale per la tua altezza.",
        "en": "Calculate your BMI (body mass index) from weight and height, see which WHO category you fall into and the normal weight range for your height.",
    },
    "intro": {
        "it": "Inserisci altezza e peso: ottieni il BMI, la categoria (sottopeso, normopeso, sovrappeso, obesità) e l'intervallo di peso considerato normale per la tua altezza. Valido per adulti.",
        "en": "Enter your height and weight to get your BMI, its category (underweight, normal, overweight, obese) and the weight range considered normal for your height. For adults.",
    },
    "strings": {
        "it": {
            "metric": "Metrico (cm, kg)", "imperial": "Imperiale (ft, lb)", "height": "Altezza", "weight": "Peso", "ft": "piedi", "inch": "pollici", "lb": "libbre", "cm": "cm", "kg": "kg",
            "bmi": "Il tuo BMI", "cat": "Categoria", "range": "Peso normale per la tua altezza", "diff_lose": "per rientrare nella fascia normale dovresti perdere circa", "diff_gain": "per rientrare nella fascia normale dovresti prendere circa", "ok": "Sei nella fascia di peso normale",
            "c1": "Sottopeso", "c2": "Normopeso", "c3": "Sovrappeso", "c4": "Obesità (classe I)", "c5": "Obesità (classe II)", "c6": "Obesità (classe III)",
            "disclaimer": "Il BMI è un indicatore statistico per adulti: non distingue massa muscolare e grasso e non sostituisce una valutazione medica.",
        },
        "en": {
            "metric": "Metric (cm, kg)", "imperial": "Imperial (ft, lb)", "height": "Height", "weight": "Weight", "ft": "feet", "inch": "inches", "lb": "pounds", "cm": "cm", "kg": "kg",
            "bmi": "Your BMI", "cat": "Category", "range": "Normal weight for your height", "diff_lose": "to reach the normal range you would need to lose about", "diff_gain": "to reach the normal range you would need to gain about", "ok": "You are in the normal weight range",
            "c1": "Underweight", "c2": "Normal weight", "c3": "Overweight", "c4": "Obesity (class I)", "c5": "Obesity (class II)", "c6": "Obesity (class III)",
            "disclaimer": "BMI is a statistical indicator for adults: it does not distinguish muscle from fat and is no substitute for medical advice.",
        },
    },
    "ui": """
<div class="tabs"><button type="button" class="on" data-u="m">{{metric}}</button><button type="button" data-u="i">{{imperial}}</button></div>
<div class="row" id="metric">
  <div class="field"><label for="hcm">{{height}} ({{cm}})</label><input type="text" inputmode="decimal" id="hcm" value="175"></div>
  <div class="field"><label for="wkg">{{weight}} ({{kg}})</label><input type="text" inputmode="decimal" id="wkg" value="72"></div>
</div>
<div class="row hide" id="imperial">
  <div class="field"><label for="hft">{{height}} ({{ft}})</label><input type="text" inputmode="numeric" id="hft" value="5"></div>
  <div class="field"><label for="hin">{{height}} ({{inch}})</label><input type="text" inputmode="decimal" id="hin" value="9"></div>
  <div class="field"><label for="wlb">{{weight}} ({{lb}})</label><input type="text" inputmode="decimal" id="wlb" value="160"></div>
</div>
<div class="result hide" id="out">
  <div class="sub">{{bmi}}</div><div class="big" id="val"></div>
  <div class="sub" id="cat"></div>
  <div class="meter" style="background:linear-gradient(90deg,#74c0fc 0 20%,#69db7c 20% 42%,#ffd43b 42% 55%,#ff922b 55% 70%,#ff6b6b 70% 100%);position:relative;height:12px"><i id="mark" style="position:absolute;top:-4px;width:4px;height:20px;background:var(--fg);border-radius:2px"></i></div>
  <div class="stats"><div class="stat"><b id="range"></b><span>{{range}}</span></div><div class="stat"><b id="diff" style="font-size:1rem"></b><span id="difflbl"></span></div></div>
</div>
<p class="msg">{{disclaimer}}</p>
""",
    "js": r"""
var unit = 'm';
var tabs = RT.$$('.tabs button');
tabs.forEach(function (b) { b.addEventListener('click', function () { unit = b.getAttribute('data-u'); tabs.forEach(function (x) { x.classList.toggle('on', x === b); }); RT.$('#metric').classList.toggle('hide', unit !== 'm'); RT.$('#imperial').classList.toggle('hide', unit !== 'i'); calc(); }); });
function calc() {
  var h, w; // metres, kg
  if (unit === 'm') { h = RT.num(RT.$('#hcm').value) / 100; w = RT.num(RT.$('#wkg').value); }
  else { h = ((RT.num(RT.$('#hft').value) || 0) * 12 + (RT.num(RT.$('#hin').value) || 0)) * 0.0254; w = RT.num(RT.$('#wlb').value) * 0.45359237; }
  var out = RT.$('#out');
  if (!(h > 0.5 && h < 2.8 && w > 10 && w < 700)) { out.classList.add('hide'); return; }
  var bmi = w / (h * h);
  var cat = bmi < 18.5 ? T.c1 : bmi < 25 ? T.c2 : bmi < 30 ? T.c3 : bmi < 35 ? T.c4 : bmi < 40 ? T.c5 : T.c6;
  RT.$('#val').textContent = RT.fmtFixed(bmi, 1); RT.$('#cat').textContent = T.cat + ': ' + cat;
  RT.$('#mark').style.left = Math.min(98, Math.max(0, (bmi - 12) / 30 * 100)) + '%';
  var lo = 18.5 * h * h, hi = 24.9 * h * h;
  function kgOut(x) { return unit === 'm' ? RT.fmt(x, 1) + ' kg' : RT.fmt(x / 0.45359237, 0) + ' lb'; }
  RT.$('#range').textContent = kgOut(lo) + ' – ' + kgOut(hi);
  if (w > hi) { RT.$('#diff').textContent = kgOut(w - hi); RT.$('#difflbl').textContent = T.diff_lose; }
  else if (w < lo) { RT.$('#diff').textContent = kgOut(lo - w); RT.$('#difflbl').textContent = T.diff_gain; }
  else { RT.$('#diff').textContent = '✓'; RT.$('#difflbl').textContent = T.ok; }
  out.classList.remove('hide');
}
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>Cos'è il BMI</h2>
<p>Il BMI (Body Mass Index, in italiano IMC, indice di massa corporea) mette in relazione peso e altezza con la formula <strong>peso in kg ÷ (altezza in metri)²</strong>. Una persona alta 1,75 m che pesa 72 kg ha un BMI di 72 ÷ (1,75 × 1,75) = 23,5. È l'indicatore usato dall'Organizzazione Mondiale della Sanità per classificare il peso degli adulti su grandi numeri.</p>
<h2>Le fasce dell'OMS</h2>
<div class="table-wrap"><table>
<tr><th>BMI</th><th>Categoria</th></tr>
<tr><td>meno di 18,5</td><td>Sottopeso</td></tr>
<tr><td>18,5 – 24,9</td><td>Normopeso</td></tr>
<tr><td>25 – 29,9</td><td>Sovrappeso</td></tr>
<tr><td>30 – 34,9</td><td>Obesità di classe I</td></tr>
<tr><td>35 – 39,9</td><td>Obesità di classe II</td></tr>
<tr><td>40 e oltre</td><td>Obesità di classe III</td></tr>
</table></div>
<h2>I limiti del BMI</h2>
<p>Il BMI è un numero semplice e per questo imperfetto: non distingue il grasso dai muscoli (un atleta muscoloso può risultare «sovrappeso»), non tiene conto di età, sesso e distribuzione del grasso, e non vale per bambini e adolescenti, per i quali si usano tabelle per età, né in gravidanza. La circonferenza della vita e la composizione corporea completano il quadro. Per valutazioni personali rivolgiti al medico o a un dietista.</p>
<h2>Il peso «normale» per la tua altezza</h2>
<p>L'intervallo mostrato dal calcolatore corrisponde a un BMI tra 18,5 e 24,9: per 1,75 m va da circa 57 a 76 kg. Non è un obiettivo da raggiungere a tutti i costi, ma un riferimento statistico.</p>
""",
        "en": """
<h2>What BMI is</h2>
<p>BMI (Body Mass Index) relates weight to height with the formula <strong>weight in kg ÷ (height in metres)²</strong>. A person 1.75 m tall weighing 72 kg has a BMI of 72 ÷ (1.75 × 1.75) = 23.5. It is the indicator the World Health Organization uses to classify adult weight across large populations.</p>
<h2>WHO categories</h2>
<div class="table-wrap"><table>
<tr><th>BMI</th><th>Category</th></tr>
<tr><td>below 18.5</td><td>Underweight</td></tr>
<tr><td>18.5 – 24.9</td><td>Normal weight</td></tr>
<tr><td>25 – 29.9</td><td>Overweight</td></tr>
<tr><td>30 – 34.9</td><td>Obesity class I</td></tr>
<tr><td>35 – 39.9</td><td>Obesity class II</td></tr>
<tr><td>40 and above</td><td>Obesity class III</td></tr>
</table></div>
<h2>Limits of BMI</h2>
<p>BMI is a simple number and therefore imperfect: it does not tell fat from muscle (a muscular athlete may read as "overweight"), it ignores age, sex and fat distribution, and it does not apply to children and teenagers, who use age-specific charts, or during pregnancy. Waist circumference and body composition complete the picture. For personal assessments see a doctor or a dietitian.</p>
<h2>The "normal" weight for your height</h2>
<p>The range shown by the calculator corresponds to a BMI between 18.5 and 24.9: for 1.75 m (5 ft 9 in) it goes from about 57 to 76 kg (125 to 168 lb). It is a statistical reference, not a target to hit at any cost.</p>
""",
    },
    "faq": {
        "it": [
            ("Come si calcola il BMI?", "Peso in chilogrammi diviso per l'altezza in metri al quadrato. Esempio: 70 kg e 1,70 m → 70 ÷ 2,89 = 24,2."),
            ("Qual è il BMI ideale?", "Per gli adulti la fascia «normopeso» va da 18,5 a 24,9. Molti studi indicano la zona 20–25 come quella associata al minor rischio, ma il valore ottimale dipende dalla persona."),
            ("Il BMI vale anche per i bambini?", "No: per bambini e ragazzi fino a 18 anni si usano curve di crescita per età e sesso, non le soglie degli adulti."),
        ],
        "en": [
            ("How is BMI calculated?", "Weight in kilograms divided by height in metres squared. Example: 70 kg and 1.70 m → 70 ÷ 2.89 = 24.2. In imperial units: weight in pounds × 703 ÷ height in inches squared."),
            ("What is the ideal BMI?", "For adults the \"normal\" range is 18.5 to 24.9. Many studies point to 20–25 as the range with the lowest risk, but the optimal value depends on the person."),
            ("Does BMI apply to children?", "No: for children and teenagers up to 18, age- and sex-specific growth charts are used, not adult thresholds."),
        ],
    },
}

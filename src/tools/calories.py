TOOL = {
    "id": "calories",
    "cat": "health",
    "icon": "🍎",
    "slug": {"it": "calcolo-calorie-giornaliere", "en": "calorie-calculator"},
    "title": {"it": "Calcolo del fabbisogno calorico giornaliero", "en": "Daily calorie needs calculator"},
    "short": {"it": "Metabolismo basale, calorie di mantenimento e per dimagrire o aumentare", "en": "Basal metabolic rate, maintenance calories and targets to lose or gain weight"},
    "keywords": {"it": ["quante calorie al giorno", "metabolismo basale", "tdee", "calorie per dimagrire", "fabbisogno energetico"], "en": ["how many calories a day", "bmr", "tdee", "calories to lose weight", "maintenance calories"]},
    "meta": {
        "it": "Calcola il metabolismo basale e le calorie giornaliere di mantenimento in base a sesso, età, peso, altezza e attività fisica, con gli obiettivi per perdere o mettere peso. Formula di Mifflin-St Jeor.",
        "en": "Calculate your basal metabolic rate and daily maintenance calories from sex, age, weight, height and activity level, with targets for losing or gaining weight. Mifflin-St Jeor formula.",
    },
    "intro": {
        "it": "Inserisci i tuoi dati e il livello di attività: ottieni il metabolismo basale, le calorie per mantenere il peso e quelle indicative per dimagrire o aumentare in modo graduale.",
        "en": "Enter your details and activity level to get your basal metabolic rate, the calories to maintain your weight and indicative targets to lose or gain weight gradually.",
    },
    "strings": {
        "it": {
            "metric": "Metrico (cm, kg)", "imperial": "Imperiale (ft, lb)", "sex": "Sesso", "m": "Uomo", "f": "Donna", "age": "Età (anni)", "height": "Altezza", "weight": "Peso", "ft": "piedi", "inch": "pollici",
            "activity": "Attività fisica", "a1": "Sedentaria (poco o niente esercizio)", "a2": "Leggera (1–3 allenamenti a settimana)", "a3": "Moderata (3–5 allenamenti a settimana)", "a4": "Intensa (6–7 allenamenti a settimana)", "a5": "Molto intensa (lavoro fisico + allenamenti)",
            "bmr": "Metabolismo basale (BMR)", "tdee": "Mantenimento (TDEE)", "kcal": "kcal/giorno", "goals": "Obiettivi indicativi",
            "lose1": "Dimagrire lentamente (−0,25 kg/sett.)", "lose2": "Dimagrire (−0,5 kg/sett.)", "gain1": "Aumentare lentamente (+0,25 kg/sett.)", "gain2": "Aumentare (+0,5 kg/sett.)",
            "warn": "Valore molto basso: sotto le 1.200 kcal (donne) o 1.500 kcal (uomini) servirebbe la supervisione di un professionista.",
            "disclaimer": "Stima statistica per adulti sani: le esigenze reali variano da persona a persona. Per diete e condizioni particolari rivolgiti a un medico o dietista.",
        },
        "en": {
            "metric": "Metric (cm, kg)", "imperial": "Imperial (ft, lb)", "sex": "Sex", "m": "Male", "f": "Female", "age": "Age (years)", "height": "Height", "weight": "Weight", "ft": "feet", "inch": "inches",
            "activity": "Activity level", "a1": "Sedentary (little or no exercise)", "a2": "Light (1–3 workouts a week)", "a3": "Moderate (3–5 workouts a week)", "a4": "Active (6–7 workouts a week)", "a5": "Very active (physical job + training)",
            "bmr": "Basal metabolic rate (BMR)", "tdee": "Maintenance (TDEE)", "kcal": "kcal/day", "goals": "Indicative targets",
            "lose1": "Lose weight slowly (−0.5 lb/week)", "lose2": "Lose weight (−1 lb/week)", "gain1": "Gain slowly (+0.5 lb/week)", "gain2": "Gain (+1 lb/week)",
            "warn": "Very low value: below 1,200 kcal (women) or 1,500 kcal (men) you would need professional supervision.",
            "disclaimer": "Statistical estimate for healthy adults: real needs vary from person to person. For diets and medical conditions consult a doctor or dietitian.",
        },
    },
    "ui": """
<div class="tabs"><button type="button" class="on" data-u="m">{{metric}}</button><button type="button" data-u="i">{{imperial}}</button></div>
<div class="row">
  <div class="field"><label for="sex">{{sex}}</label><select id="sex"><option value="m">{{m}}</option><option value="f">{{f}}</option></select></div>
  <div class="field"><label for="age">{{age}}</label><input type="text" inputmode="numeric" id="age" value="35"></div>
</div>
<div class="row" id="metric">
  <div class="field"><label for="hcm">{{height}} (cm)</label><input type="text" inputmode="decimal" id="hcm" value="175"></div>
  <div class="field"><label for="wkg">{{weight}} (kg)</label><input type="text" inputmode="decimal" id="wkg" value="72"></div>
</div>
<div class="row hide" id="imperial">
  <div class="field"><label for="hft">{{height}} ({{ft}})</label><input type="text" inputmode="numeric" id="hft" value="5"></div>
  <div class="field"><label for="hin">{{height}} ({{inch}})</label><input type="text" inputmode="decimal" id="hin" value="9"></div>
  <div class="field"><label for="wlb">{{weight}} (lb)</label><input type="text" inputmode="decimal" id="wlb" value="160"></div>
</div>
<div class="field"><label for="act">{{activity}}</label><select id="act">
  <option value="1.2">{{a1}}</option><option value="1.375" selected>{{a2}}</option><option value="1.55">{{a3}}</option><option value="1.725">{{a4}}</option><option value="1.9">{{a5}}</option></select></div>
<div class="result hide" id="out">
  <div class="stats">
    <div class="stat"><b id="bmr"></b><span>{{bmr}} · {{kcal}}</span></div>
    <div class="stat" style="border-color:var(--accent)"><b id="tdee"></b><span>{{tdee}} · {{kcal}}</span></div>
  </div>
  <div class="lbl" style="margin-top:14px">{{goals}}</div>
  <div class="table-wrap"><table>
    <tr><td>{{lose2}}</td><td><b id="l2"></b> {{kcal}}</td></tr>
    <tr><td>{{lose1}}</td><td><b id="l1"></b> {{kcal}}</td></tr>
    <tr><td>{{gain1}}</td><td><b id="g1"></b> {{kcal}}</td></tr>
    <tr><td>{{gain2}}</td><td><b id="g2"></b> {{kcal}}</td></tr>
  </table></div>
  <p class="msg warn hide" id="warn">{{warn}}</p>
</div>
<p class="msg">{{disclaimer}}</p>
""",
    "js": r"""
var unit = 'm';
var tabs = RT.$$('.tabs button');
tabs.forEach(function (b) { b.addEventListener('click', function () { unit = b.getAttribute('data-u'); tabs.forEach(function (x) { x.classList.toggle('on', x === b); }); RT.$('#metric').classList.toggle('hide', unit !== 'm'); RT.$('#imperial').classList.toggle('hide', unit !== 'i'); calc(); }); });
function calc() {
  var h, w, age = RT.num(RT.$('#age').value), sex = RT.$('#sex').value, act = +RT.$('#act').value;
  if (unit === 'm') { h = RT.num(RT.$('#hcm').value); w = RT.num(RT.$('#wkg').value); }
  else { h = ((RT.num(RT.$('#hft').value) || 0) * 12 + (RT.num(RT.$('#hin').value) || 0)) * 2.54; w = RT.num(RT.$('#wlb').value) * 0.45359237; }
  var out = RT.$('#out');
  if (!(h > 100 && h < 260 && w > 25 && w < 400 && age >= 15 && age < 110)) { out.classList.add('hide'); return; }
  var bmr = 10 * w + 6.25 * h - 5 * age + (sex === 'm' ? 5 : -161);
  var tdee = bmr * act;
  RT.$('#bmr').textContent = RT.fmt(Math.round(bmr), 0); RT.$('#tdee').textContent = RT.fmt(Math.round(tdee), 0);
  RT.$('#l2').textContent = RT.fmt(Math.round(tdee - 500), 0); RT.$('#l1').textContent = RT.fmt(Math.round(tdee - 250), 0);
  RT.$('#g1').textContent = RT.fmt(Math.round(tdee + 250), 0); RT.$('#g2').textContent = RT.fmt(Math.round(tdee + 500), 0);
  RT.$('#warn').classList.toggle('hide', !(tdee - 500 < (sex === 'm' ? 1500 : 1200)));
  out.classList.remove('hide');
}
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>Come viene calcolato il fabbisogno</h2>
<p>Il calcolatore usa la formula di <strong>Mifflin-St Jeor</strong>, quella considerata più accurata per gli adulti dalle principali associazioni di dietisti:</p>
<ul>
<li>Uomini: BMR = 10 × peso (kg) + 6,25 × altezza (cm) − 5 × età + 5</li>
<li>Donne: BMR = 10 × peso (kg) + 6,25 × altezza (cm) − 5 × età − 161</li>
</ul>
<p>Il <strong>metabolismo basale (BMR)</strong> è l'energia che il corpo consuma a riposo completo per respirare, far circolare il sangue e mantenere la temperatura. Moltiplicandolo per un coefficiente di attività si ottiene il <strong>TDEE</strong>, le calorie che consumi in una giornata tipo: 1,2 per chi è sedentario fino a 1,9 per chi fa lavori fisici e si allena ogni giorno. Esempio: un uomo di 35 anni, 175 cm e 72 kg ha un BMR di circa 1.640 kcal e, con attività leggera, un mantenimento di circa 2.260 kcal.</p>
<h2>Dimagrire o aumentare di peso</h2>
<p>Un chilo di grasso corporeo corrisponde a circa 7.000 kcal. Un deficit di 500 kcal al giorno porta quindi a perdere circa mezzo chilo a settimana, un ritmo considerato sostenibile; 250 kcal al giorno equivalgono a circa 250 g a settimana. Lo stesso vale, al contrario, per aumentare. Deficit più aggressivi fanno perdere anche massa muscolare e sono difficili da mantenere.</p>
<h2>Consigli per usare bene questi numeri</h2>
<ul>
<li>Sono una stima: la differenza reale può essere del ±10-15%. Pesati per due o tre settimane e correggi di 100-200 kcal se il peso non si muove come previsto.</li>
<li>Non scendere sotto le 1.200 kcal (donne) o 1.500 kcal (uomini) senza il parere di un professionista.</li>
<li>Scegli il livello di attività con onestà: la maggior parte delle persone lo sovrastima.</li>
<li>Le proteine (1,2-1,6 g per kg di peso) aiutano a conservare i muscoli durante una dieta.</li>
</ul>
""",
        "en": """
<h2>How the calculation works</h2>
<p>The calculator uses the <strong>Mifflin-St Jeor</strong> equation, considered the most accurate for adults by the main dietetic associations:</p>
<ul>
<li>Men: BMR = 10 × weight (kg) + 6.25 × height (cm) − 5 × age + 5</li>
<li>Women: BMR = 10 × weight (kg) + 6.25 × height (cm) − 5 × age − 161</li>
</ul>
<p>The <strong>basal metabolic rate (BMR)</strong> is the energy your body burns at complete rest to breathe, circulate blood and keep its temperature. Multiplying it by an activity factor gives the <strong>TDEE</strong>, the calories you burn on a typical day: 1.2 for sedentary people up to 1.9 for those with physical jobs who also train daily. Example: a 35-year-old man, 175 cm and 72 kg, has a BMR of about 1,640 kcal and, with light activity, a maintenance level of about 2,260 kcal.</p>
<h2>Losing or gaining weight</h2>
<p>A pound of body fat holds roughly 3,500 kcal. A deficit of 500 kcal a day therefore means losing about one pound (0.5 kg) a week, a pace considered sustainable; 250 kcal a day is about half a pound a week. The same applies in reverse for gaining. Harsher deficits also burn muscle and are hard to keep up.</p>
<h2>Using these numbers well</h2>
<ul>
<li>They are an estimate: the real figure can differ by ±10-15%. Weigh yourself for two or three weeks and adjust by 100-200 kcal if your weight is not moving as expected.</li>
<li>Don't go below 1,200 kcal (women) or 1,500 kcal (men) without professional advice.</li>
<li>Pick your activity level honestly: most people overestimate it.</li>
<li>Protein (1.2-1.6 g per kg of body weight) helps preserve muscle while dieting.</li>
</ul>
""",
    },
    "faq": {
        "it": [
            ("Quante calorie servono al giorno?", "Dipende da sesso, età, corporatura e attività: in media circa 2.000-2.500 kcal per una donna e 2.500-3.000 per un uomo. Il calcolatore dà il valore per i tuoi dati."),
            ("Che differenza c'è tra BMR e TDEE?", "Il BMR è il consumo a riposo assoluto; il TDEE aggiunge l'energia spesa per muoversi, lavorare e digerire, ed è il numero da usare per pianificare i pasti."),
            ("Quante calorie devo togliere per perdere mezzo chilo a settimana?", "Circa 500 kcal al giorno rispetto al mantenimento, cioè 3.500 kcal a settimana."),
        ],
        "en": [
            ("How many calories do I need a day?", "It depends on sex, age, build and activity: on average about 2,000-2,500 kcal for a woman and 2,500-3,000 for a man. The calculator gives the value for your details."),
            ("What is the difference between BMR and TDEE?", "BMR is your absolute resting expenditure; TDEE adds the energy spent moving, working and digesting, and is the number to use when planning meals."),
            ("How many calories should I cut to lose a pound a week?", "About 500 kcal a day below maintenance, i.e. 3,500 kcal a week."),
        ],
    },
}

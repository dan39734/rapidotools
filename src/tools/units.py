TOOL = {
    "id": "units",
    "cat": "numbers",
    "icon": "📏",
    "slug": {"it": "convertitore-unita-di-misura", "en": "unit-converter"},
    "title": {"it": "Convertitore di unità di misura", "en": "Unit converter"},
    "short": {"it": "Lunghezza, peso, temperatura, volume, area, velocità, dati", "en": "Length, weight, temperature, volume, area, speed, data"},
    "keywords": {"it": ["pollici in cm", "miglia in km", "fahrenheit in celsius", "libbre in kg", "once in grammi", "piedi in metri", "conversione unità"], "en": ["inches to cm", "miles to km", "fahrenheit to celsius", "pounds to kg", "ounces to grams", "feet to meters"]},
    "meta": {
        "it": "Converti unità di lunghezza, peso, temperatura, volume, area, velocità e dati: pollici in cm, miglia in km, Fahrenheit in Celsius, libbre in kg e molto altro. Gratis, nel browser.",
        "en": "Convert units of length, weight, temperature, volume, area, speed and data: inches to cm, miles to km, Fahrenheit to Celsius, pounds to kg and much more. Free, in your browser.",
    },
    "intro": {
        "it": "Scegli la categoria, scrivi il valore e seleziona le unità di partenza e di arrivo: il risultato si aggiorna subito, con una tabella dei valori vicini per orientarti.",
        "en": "Pick a category, type the value and choose the units to convert from and to: the result updates instantly, with a table of nearby values for reference.",
    },
    "strings": {
        "it": {
            "cat": "Categoria", "value": "Valore", "from": "Da", "to": "A", "swap": "Inverti", "table": "Valori vicini",
            "length": "Lunghezza", "weight": "Peso e massa", "temp": "Temperatura", "volume": "Volume", "area": "Area", "speed": "Velocità", "data": "Dati digitali",
            "u_mm": "millimetri (mm)", "u_cm": "centimetri (cm)", "u_m": "metri (m)", "u_km": "chilometri (km)", "u_in": "pollici (in)", "u_ft": "piedi (ft)", "u_yd": "iarde (yd)", "u_mi": "miglia (mi)", "u_nmi": "miglia nautiche",
            "u_mg": "milligrammi (mg)", "u_g": "grammi (g)", "u_kg": "chilogrammi (kg)", "u_t": "tonnellate (t)", "u_oz": "once (oz)", "u_lb": "libbre (lb)", "u_st": "stone (st)",
            "u_c": "gradi Celsius (°C)", "u_f": "gradi Fahrenheit (°F)", "u_k": "kelvin (K)",
            "u_ml": "millilitri (ml)", "u_cl": "centilitri (cl)", "u_l": "litri (l)", "u_m3": "metri cubi (m³)", "u_tsp": "cucchiaini (tsp)", "u_tbsp": "cucchiai (tbsp)", "u_floz": "once fluide (fl oz)", "u_cup": "tazze (cup US)", "u_pt": "pinte (pt US)", "u_gal": "galloni (gal US)",
            "u_cm2": "centimetri quadrati (cm²)", "u_m2": "metri quadrati (m²)", "u_ha": "ettari (ha)", "u_km2": "chilometri quadrati (km²)", "u_in2": "pollici quadrati (in²)", "u_ft2": "piedi quadrati (ft²)", "u_ac": "acri (ac)",
            "u_ms": "metri al secondo (m/s)", "u_kmh": "chilometri orari (km/h)", "u_mph": "miglia orarie (mph)", "u_kn": "nodi (kn)",
            "u_b": "byte (B)", "u_kb": "kilobyte (KB)", "u_mb": "megabyte (MB)", "u_gb": "gigabyte (GB)", "u_tb": "terabyte (TB)", "u_mbit": "megabit (Mb)", "u_gbit": "gigabit (Gb)",
        },
        "en": {
            "cat": "Category", "value": "Value", "from": "From", "to": "To", "swap": "Swap", "table": "Nearby values",
            "length": "Length", "weight": "Weight & mass", "temp": "Temperature", "volume": "Volume", "area": "Area", "speed": "Speed", "data": "Digital data",
            "u_mm": "millimetres (mm)", "u_cm": "centimetres (cm)", "u_m": "metres (m)", "u_km": "kilometres (km)", "u_in": "inches (in)", "u_ft": "feet (ft)", "u_yd": "yards (yd)", "u_mi": "miles (mi)", "u_nmi": "nautical miles",
            "u_mg": "milligrams (mg)", "u_g": "grams (g)", "u_kg": "kilograms (kg)", "u_t": "tonnes (t)", "u_oz": "ounces (oz)", "u_lb": "pounds (lb)", "u_st": "stone (st)",
            "u_c": "degrees Celsius (°C)", "u_f": "degrees Fahrenheit (°F)", "u_k": "kelvin (K)",
            "u_ml": "millilitres (ml)", "u_cl": "centilitres (cl)", "u_l": "litres (l)", "u_m3": "cubic metres (m³)", "u_tsp": "teaspoons (tsp)", "u_tbsp": "tablespoons (tbsp)", "u_floz": "fluid ounces (fl oz)", "u_cup": "cups (US)", "u_pt": "pints (US)", "u_gal": "gallons (US)",
            "u_cm2": "square centimetres (cm²)", "u_m2": "square metres (m²)", "u_ha": "hectares (ha)", "u_km2": "square kilometres (km²)", "u_in2": "square inches (in²)", "u_ft2": "square feet (ft²)", "u_ac": "acres (ac)",
            "u_ms": "metres per second (m/s)", "u_kmh": "kilometres per hour (km/h)", "u_mph": "miles per hour (mph)", "u_kn": "knots (kn)",
            "u_b": "bytes (B)", "u_kb": "kilobytes (KB)", "u_mb": "megabytes (MB)", "u_gb": "gigabytes (GB)", "u_tb": "terabytes (TB)", "u_mbit": "megabits (Mb)", "u_gbit": "gigabits (Gb)",
        },
    },
    "ui": """
<div class="row">
  <div class="field"><label for="cat">{{cat}}</label><select id="cat"></select></div>
  <div class="field"><label for="val">{{value}}</label><input type="text" inputmode="decimal" id="val" value="1"></div>
</div>
<div class="row">
  <div class="field"><label for="from">{{from}}</label><select id="from"></select></div>
  <div class="field" style="flex:0 0 auto;justify-content:flex-end"><button class="btn" type="button" id="swap">⇄ {{swap}}</button></div>
  <div class="field"><label for="to">{{to}}</label><select id="to"></select></div>
</div>
<div class="result"><div class="big" id="out"></div><div class="sub" id="sub"></div></div>
<div class="lbl" style="margin-top:14px">{{table}}</div>
<div class="table-wrap"><table id="tbl"></table></div>
""",
    "js": r"""
var CATS = {
  length: { units: { mm: 0.001, cm: 0.01, m: 1, km: 1000, 'in': 0.0254, ft: 0.3048, yd: 0.9144, mi: 1609.344, nmi: 1852 }, def: ['in', 'cm'] },
  weight: { units: { mg: 0.000001, g: 0.001, kg: 1, t: 1000, oz: 0.028349523125, lb: 0.45359237, st: 6.35029318 }, def: ['lb', 'kg'] },
  temp: { units: { c: 1, f: 1, k: 1 }, def: ['f', 'c'], special: true },
  volume: { units: { ml: 0.001, cl: 0.01, l: 1, m3: 1000, tsp: 0.00492892159375, tbsp: 0.01478676478125, floz: 0.0295735295625, cup: 0.2365882365, pt: 0.473176473, gal: 3.785411784 }, def: ['gal', 'l'] },
  area: { units: { cm2: 0.0001, m2: 1, ha: 10000, km2: 1000000, in2: 0.00064516, ft2: 0.09290304, ac: 4046.8564224 }, def: ['ft2', 'm2'] },
  speed: { units: { ms: 1, kmh: 1 / 3.6, mph: 0.44704, kn: 0.514444444 }, def: ['mph', 'kmh'] },
  data: { units: { b: 1, kb: 1000, mb: 1e6, gb: 1e9, tb: 1e12, mbit: 125000, gbit: 125000000 }, def: ['gb', 'mb'] }
};
var cat = RT.$('#cat'), from = RT.$('#from'), to = RT.$('#to'), val = RT.$('#val'), out = RT.$('#out'), sub = RT.$('#sub'), tbl = RT.$('#tbl');
Object.keys(CATS).forEach(function (k) { var o = document.createElement('option'); o.value = k; o.textContent = T[k]; cat.appendChild(o); });
function fill() {
  var c = CATS[cat.value]; from.innerHTML = ''; to.innerHTML = '';
  Object.keys(c.units).forEach(function (u) { [from, to].forEach(function (sel) { var o = document.createElement('option'); o.value = u; o.textContent = T['u_' + u]; sel.appendChild(o); }); });
  from.value = c.def[0]; to.value = c.def[1];
}
function toC(v, u) { return u === 'c' ? v : u === 'f' ? (v - 32) * 5 / 9 : v - 273.15; }
function fromC(v, u) { return u === 'c' ? v : u === 'f' ? v * 9 / 5 + 32 : v + 273.15; }
function conv(v, a, b) { var c = CATS[cat.value]; if (c.special) return fromC(toC(v, a), b); return v * c.units[a] / c.units[b]; }
function nice(n) { if (!isFinite(n)) return '–'; var a = Math.abs(n); var d = a === 0 ? 0 : a >= 1000 ? 2 : a >= 1 ? 4 : a >= 0.001 ? 6 : 10; return RT.fmt(n, d); }
function short(u) { var s = T['u_' + u]; var m = s.match(/\(([^)]+)\)/); return m ? m[1] : s; }
function calc() {
  var v = RT.num(val.value), a = from.value, b = to.value;
  if (!isFinite(v)) { out.textContent = '–'; sub.textContent = ''; tbl.innerHTML = ''; return; }
  var r = conv(v, a, b);
  out.textContent = nice(v) + ' ' + short(a) + ' = ' + nice(r) + ' ' + short(b);
  sub.textContent = CATS[cat.value].special ? '' : '1 ' + short(a) + ' = ' + nice(conv(1, a, b)) + ' ' + short(b) + ' · 1 ' + short(b) + ' = ' + nice(conv(1, b, a)) + ' ' + short(a);
  var base = CATS[cat.value].special ? [v - 20, v - 10, v - 5, v, v + 5, v + 10, v + 20] : [v * 0.25, v * 0.5, v, v * 2, v * 5, v * 10, v * 100];
  tbl.innerHTML = '<tr><th>' + short(a) + '</th><th>' + short(b) + '</th></tr>' + base.map(function (x) { return '<tr><td>' + nice(x) + '</td><td>' + nice(conv(x, a, b)) + '</td></tr>'; }).join('');
}
cat.addEventListener('change', function () { fill(); calc(); });
RT.$('#swap').addEventListener('click', function () { var t = from.value; from.value = to.value; to.value = t; calc(); });
[from, to].forEach(function (s) { s.addEventListener('change', calc); }); val.addEventListener('input', calc);
fill(); calc();
""",
    "article": {
        "it": """
<h2>Le conversioni più richieste</h2>
<ul>
<li><strong>Lunghezza:</strong> 1 pollice = 2,54 cm; 1 piede = 30,48 cm; 1 iarda = 0,9144 m; 1 miglio = 1,609 km; 1 miglio nautico = 1,852 km.</li>
<li><strong>Peso:</strong> 1 libbra = 453,6 g; 1 oncia = 28,35 g; 1 stone = 6,35 kg; 1 kg = 2,205 libbre.</li>
<li><strong>Temperatura:</strong> °F = °C × 9/5 + 32; °C = (°F − 32) × 5/9. 0 °C = 32 °F, 100 °C = 212 °F, 37 °C = 98,6 °F. Il kelvin è °C + 273,15.</li>
<li><strong>Volume:</strong> 1 gallone USA = 3,785 l; 1 oncia fluida = 29,57 ml; 1 tazza USA = 236,6 ml; 1 cucchiaio = 14,8 ml; 1 cucchiaino = 4,9 ml.</li>
<li><strong>Area:</strong> 1 acro = 4.047 m²; 1 ettaro = 10.000 m²; 1 piede quadrato = 0,0929 m².</li>
<li><strong>Velocità:</strong> 1 mph = 1,609 km/h; 1 nodo = 1,852 km/h; 1 m/s = 3,6 km/h.</li>
<li><strong>Dati:</strong> 1 byte = 8 bit; 1 GB = 1.000 MB (unità decimali, quelle usate da produttori e operatori); 100 Mbit/s = 12,5 MB/s.</li>
</ul>
<h2>Sistema metrico e unità anglosassoni</h2>
<p>Il sistema metrico (metri, chilogrammi, litri) è usato quasi ovunque; le unità anglosassoni (pollici, libbre, galloni, Fahrenheit) restano comuni negli Stati Uniti e in parte nel Regno Unito. Attenzione alle differenze: il gallone e la pinta britannici sono più grandi di quelli americani (1 gallone UK = 4,546 l); qui usiamo le misure USA, le più diffuse online e nelle ricette.</p>
<h2>Come usare la tabella</h2>
<p>Sotto il risultato trovi una tabella con valori vicini a quello inserito (per la temperatura, a intervalli di 5 e 10 gradi): comoda per farsi un'idea senza rifare il calcolo, per esempio quando leggi una ricetta americana o controlli le previsioni del tempo in un altro paese.</p>
""",
        "en": """
<h2>The most requested conversions</h2>
<ul>
<li><strong>Length:</strong> 1 inch = 2.54 cm; 1 foot = 30.48 cm; 1 yard = 0.9144 m; 1 mile = 1.609 km; 1 nautical mile = 1.852 km.</li>
<li><strong>Weight:</strong> 1 pound = 453.6 g; 1 ounce = 28.35 g; 1 stone = 6.35 kg; 1 kg = 2.205 pounds.</li>
<li><strong>Temperature:</strong> °F = °C × 9/5 + 32; °C = (°F − 32) × 5/9. 0 °C = 32 °F, 100 °C = 212 °F, 37 °C = 98.6 °F. Kelvin is °C + 273.15.</li>
<li><strong>Volume:</strong> 1 US gallon = 3.785 l; 1 fluid ounce = 29.57 ml; 1 US cup = 236.6 ml; 1 tablespoon = 14.8 ml; 1 teaspoon = 4.9 ml.</li>
<li><strong>Area:</strong> 1 acre = 4,047 m²; 1 hectare = 10,000 m²; 1 square foot = 0.0929 m².</li>
<li><strong>Speed:</strong> 1 mph = 1.609 km/h; 1 knot = 1.852 km/h; 1 m/s = 3.6 km/h.</li>
<li><strong>Data:</strong> 1 byte = 8 bits; 1 GB = 1,000 MB (decimal units, the ones used by manufacturers and providers); 100 Mbit/s = 12.5 MB/s.</li>
</ul>
<h2>Metric and imperial units</h2>
<p>The metric system (metres, kilograms, litres) is used almost everywhere; imperial and US customary units (inches, pounds, gallons, Fahrenheit) remain common in the United States and partly in the UK. Mind the differences: the British gallon and pint are larger than the American ones (1 UK gallon = 4.546 l); this converter uses US measures, the most common online and in recipes.</p>
<h2>Using the table</h2>
<p>Below the result you get a table of values near the one you entered (for temperature, in steps of 5 and 10 degrees): handy for getting a feel without redoing the calculation, for example when reading a recipe or checking the weather forecast in another country.</p>
""",
    },
    "faq": {
        "it": [
            ("Quanti centimetri sono un pollice?", "Esattamente 2,54 cm. Uno schermo da 15,6 pollici misura quindi circa 39,6 cm in diagonale."),
            ("Come si convertono i gradi Fahrenheit in Celsius a mente?", "Sottrai 30 e dividi per 2: 70 °F ≈ 20 °C (il valore esatto è 21,1 °C). Per il contrario raddoppia e aggiungi 30."),
            ("Le tazze delle ricette americane quanto valgono?", "Una tazza USA è 236,6 ml, circa 240 ml; un cucchiaio (tablespoon) 14,8 ml e un cucchiaino (teaspoon) 4,9 ml."),
        ],
        "en": [
            ("How many centimetres in an inch?", "Exactly 2.54 cm. A 15.6-inch screen therefore measures about 39.6 cm diagonally."),
            ("How do I convert Fahrenheit to Celsius in my head?", "Subtract 30 and halve it: 70 °F ≈ 20 °C (the exact value is 21.1 °C). For the reverse, double and add 30."),
            ("How much is a cup in millilitres?", "A US cup is 236.6 ml, roughly 240 ml; a tablespoon is 14.8 ml and a teaspoon 4.9 ml."),
        ],
    },
}

"""Passo di corsa: passo da distanza e tempo (con previsioni di Riegel), tempo da passo, conversione km/h ↔ min/km."""

HALF, MARATHON, MILE = 21.0975, 42.195, 1.609344


def _t(s):
    s = round(s)
    h, m, x = s // 3600, s % 3600 // 60, s % 60
    return "%d:%02d:%02d" % (h, m, x) if h else "%d:%02d" % (m, x)


_R_HALF = _t(3000 * (HALF / 10) ** 1.06)
_R_MAR = _t(3000 * (MARATHON / 10) ** 1.06)
_P_4H = _t(4 * 3600 / MARATHON)

_JS = r"""
var mode = 'pace', MILE = 1.609344, HALF = 21.0975, MAR = 42.195;
var STD = [[1, '1 km'], [5, '5 km'], [10, '10 km'], [15, '15 km'], [HALF, T.half], [30, '30 km'], [MAR, T.marathon]];
function v(id) { return RT.num(RT.$('#' + id).value); }
function tm(s) { // h:mm:ss or m:ss
  s = Math.round(s); var h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60;
  return h ? h + ':' + RT.pad(m) + ':' + RT.pad(x) : m + ':' + RT.pad(x);
}
function secs(h, m, s) { h = isFinite(h) ? h : 0; m = isFinite(m) ? m : 0; s = isFinite(s) ? s : 0; return h * 3600 + m * 60 + s; }
function kmh(paceSec) { return 3600 / paceSec; }
function rows(el, list) {
  el.innerHTML = '';
  list.forEach(function (r) { var tr = document.createElement('tr'); r.forEach(function (c) { var td = document.createElement('td'); td.textContent = c; tr.appendChild(td); }); el.appendChild(tr); });
}
function calcPace() {
  var d = v('dist'), t = secs(v('th'), v('tm'), v('ts')), out = RT.$('#pout'), err = RT.$('#perr');
  if (!(d > 0) || !(t > 0)) { out.classList.add('hide'); err.classList.toggle('hide', !(RT.$('#dist').value || RT.$('#tm').value)); return; }
  err.classList.add('hide'); out.classList.remove('hide');
  var p = t / d;
  RT.$('#pmain').textContent = tm(p) + ' ' + T.per_km;
  RT.$('#psub').textContent = T.pace_sub.replace('{d}', RT.fmt(d, 4)).replace('{t}', tm(t));
  RT.$('#pkmh').textContent = RT.fmt(kmh(p), 2) + ' km/h';
  RT.$('#pmi').textContent = tm(p * MILE) + ' ' + T.per_mi;
  RT.$('#p400').textContent = tm(p * 0.4);
  RT.$('#pmph').textContent = RT.fmt(kmh(p) / MILE, 2) + ' mph';
  rows(RT.$('#riegel'), STD.filter(function (s) { return s[0] > 1 && Math.abs(s[0] - d) > 1e-6; }).map(function (s) {
    var t2 = t * Math.pow(s[0] / d, 1.06); return [s[1], tm(t2), tm(t2 / s[0]) + ' ' + T.per_km];
  }));
  var sp = [], n = Math.floor(d + 1e-9);
  for (var k = 1; k <= n && k <= 100; k++) sp.push([k + ' km', tm(p * k)]);
  if (d - n > 0.001 && n < 100) sp.push([RT.fmt(d, 3) + ' km', tm(t)]);
  rows(RT.$('#splits'), sp);
}
function calcTime() {
  var p = secs(0, v('pm'), v('ps')), unit = RT.$('#pu').value, d = v('dist2'), out = RT.$('#tout');
  if (!(p > 0) || !(d > 0)) { out.classList.add('hide'); return; }
  out.classList.remove('hide');
  var pk = unit === 'mi' ? p / MILE : p; // seconds per km
  RT.$('#tmain').textContent = tm(pk * d);
  RT.$('#tsub').textContent = T.time_sub.replace('{d}', RT.fmt(d, 4)).replace('{p}', tm(pk) + ' ' + T.per_km).replace('{s}', RT.fmt(kmh(pk), 2));
  rows(RT.$('#ttable'), STD.map(function (s) { return [s[1], tm(pk * s[0])]; }));
}
function calcConv() {
  var s = v('kmh'), r1 = RT.$('#cres'), s1 = RT.$('#csub');
  if (s > 0) { r1.textContent = tm(3600 / s) + ' ' + T.per_km; s1.textContent = T.conv_sub.replace('{mi}', tm(3600 / s * MILE) + ' ' + T.per_mi).replace('{mph}', RT.fmt(s / MILE, 2)); }
  else { r1.textContent = '–'; s1.textContent = ''; }
  var p = secs(0, v('cm'), v('cs')), r2 = RT.$('#cres2'), s2 = RT.$('#csub2');
  if (p > 0) { r2.textContent = RT.fmt(kmh(p), 2) + ' km/h'; s2.textContent = T.conv_sub2.replace('{mph}', RT.fmt(kmh(p) / MILE, 2)).replace('{mi}', tm(p * MILE) + ' ' + T.per_mi); }
  else { r2.textContent = '–'; s2.textContent = ''; }
}
function calc() { if (mode === 'pace') calcPace(); else if (mode === 'time') calcTime(); else calcConv(); }
RT.$$('.tabs button').forEach(function (b) {
  b.addEventListener('click', function () {
    RT.$$('.tabs button').forEach(function (x) { x.classList.toggle('on', x === b); });
    mode = b.getAttribute('data-tab');
    ['pace', 'time', 'conv'].forEach(function (k) { RT.$('#tab-' + k).classList.toggle('hide', k !== mode); });
    calc();
  });
});
RT.$$('[data-d]').forEach(function (b) { b.addEventListener('click', function () { RT.$('#dist').value = RT.fmt(+b.getAttribute('data-d'), 4); calc(); }); });
RT.$$('[data-d2]').forEach(function (b) { b.addEventListener('click', function () { RT.$('#dist2').value = RT.fmt(+b.getAttribute('data-d2'), 4); calc(); }); });
(function () { // treadmill table 6–20 km/h
  var list = [];
  for (var s = 6; s <= 20.001; s += 0.5) list.push([RT.fmt(s, 1), tm(3600 / s), tm(3600 / s * MILE), tm(3600 / s * 10), tm(3600 / s * HALF)]);
  rows(RT.$('#treadmill'), list);
})();
RT.live(document.getElementById('tool'), calc);
"""

TOOL = {
    "id": "running_pace",
    "cat": "health",
    "icon": "🏃",
    "slug": {"it": "calcolo-passo-corsa", "en": "running-pace-calculator"},
    "title": {"it": "Calcolo passo di corsa e tempo di gara", "en": "Running pace calculator and race time"},
    "short": {"it": "Passo al km, velocità in km/h e tempi su 5 km, 10 km, mezza maratona e maratona", "en": "Pace per km and per mile, speed and finish times for 5K, 10K, half marathon and marathon"},
    "keywords": {
        "it": ["passo corsa", "ritmo corsa", "min/km", "minuti al km", "km/h in min/km", "tempo maratona", "mezza maratona", "calcolo passo", "tapis roulant", "andatura", "riegel"],
        "en": ["pace calculator", "running pace", "min per km", "min per mile", "marathon time", "half marathon pace", "treadmill speed", "race time predictor"],
    },
    "meta": {
        "it": "Calcola il passo di corsa (minuti al km) da distanza e tempo, il tempo finale partendo dal passo e la conversione km/h ↔ min/km per il tapis roulant. Con previsione dei tempi su 5 km, 10 km, mezza maratona e maratona.",
        "en": "Work out your running pace (min per km or mile) from distance and time, your finish time from a pace, and convert km/h ↔ min/km for the treadmill. With predicted times for 5K, 10K, half marathon and marathon.",
    },
    "intro": {
        "it": "Inserisci distanza e tempo per sapere a che passo hai corso e quanto potresti fare su altre distanze, oppure parti dal passo per sapere in quanto chiudi una gara. C'è anche il convertitore tra km/h e min/km.",
        "en": "Enter a distance and a time to get your pace and predicted times for other distances, or start from a pace to get your finish time. There is also a km/h ↔ min/km converter.",
    },
    "strings": {
        "it": {
            "tab_pace": "Calcola il passo", "tab_time": "Calcola il tempo", "tab_conv": "Km/h ↔ min/km",
            "dist_l": "Distanza (km)", "half": "Mezza maratona", "marathon": "Maratona", "time_l": "Tempo", "h_l": "ore", "m_l": "minuti", "s_l": "secondi",
            "per_km": "/km", "per_mi": "/miglio", "pace_sub": "Passo medio su {d} km in {t}",
            "speed_l": "Velocità media", "mi_l": "Passo al miglio", "lap_l": "Tempo ogni 400 m (un giro di pista)", "mph_l": "Velocità in miglia orarie",
            "riegel_t": "Tempi previsti su altre distanze (formula di Riegel)", "col_dist": "Distanza", "col_time": "Tempo", "col_pace": "Passo",
            "splits_t": "Parziali chilometro per chilometro", "perr": "Inserisci una distanza e un tempo maggiori di zero.",
            "pace_in": "Passo", "unit_l": "Unità", "u_km": "min/km", "u_mi": "min/miglio", "dist2_l": "Distanza della gara (km)",
            "time_sub": "{d} km a {p} ({s} km/h)", "std_t": "Tempi a questo passo",
            "kmh_l": "Velocità (km/h)", "conv_sub": "= {mi} · {mph} mph", "conv2_t": "Da passo a velocità", "conv_sub2": "= {mph} mph · {mi}",
            "tread_t": "Tabella per il tapis roulant", "col_kmh": "km/h", "col_mkm": "min/km", "col_mmi": "min/miglio", "col_10": "10 km", "col_half": "Mezza",
        },
        "en": {
            "tab_pace": "Find your pace", "tab_time": "Find your time", "tab_conv": "Km/h ↔ min/km",
            "dist_l": "Distance (km)", "half": "Half marathon", "marathon": "Marathon", "time_l": "Time", "h_l": "hours", "m_l": "minutes", "s_l": "seconds",
            "per_km": "/km", "per_mi": "/mile", "pace_sub": "Average pace over {d} km in {t}",
            "speed_l": "Average speed", "mi_l": "Pace per mile", "lap_l": "Time per 400 m (one track lap)", "mph_l": "Speed in miles per hour",
            "riegel_t": "Predicted times for other distances (Riegel formula)", "col_dist": "Distance", "col_time": "Time", "col_pace": "Pace",
            "splits_t": "Kilometre splits", "perr": "Enter a distance and a time greater than zero.",
            "pace_in": "Pace", "unit_l": "Unit", "u_km": "min/km", "u_mi": "min/mile", "dist2_l": "Race distance (km)",
            "time_sub": "{d} km at {p} ({s} km/h)", "std_t": "Times at this pace",
            "kmh_l": "Speed (km/h)", "conv_sub": "= {mi} · {mph} mph", "conv2_t": "From pace to speed", "conv_sub2": "= {mph} mph · {mi}",
            "tread_t": "Treadmill table", "col_kmh": "km/h", "col_mkm": "min/km", "col_mmi": "min/mile", "col_10": "10K", "col_half": "Half",
        },
    },
    "ui": """
<div class="tabs" role="tablist">
  <button type="button" class="on" data-tab="pace">{{tab_pace}}</button>
  <button type="button" data-tab="time">{{tab_time}}</button>
  <button type="button" data-tab="conv">{{tab_conv}}</button>
</div>
<div id="tab-pace">
  <div class="field"><label for="dist">{{dist_l}}</label><input type="text" inputmode="decimal" id="dist" value="10"></div>
  <div class="inline" style="margin:-4px 0 14px">
    <button class="btn small" type="button" data-d="5">5 km</button><button class="btn small" type="button" data-d="10">10 km</button>
    <button class="btn small" type="button" data-d="21.0975">{{half}}</button><button class="btn small" type="button" data-d="42.195">{{marathon}}</button>
  </div>
  <div class="lbl">{{time_l}}</div>
  <div class="row" style="margin-top:6px">
    <div class="field" style="flex:1 1 70px"><label for="th">{{h_l}}</label><input type="number" id="th" min="0" step="1" value="0"></div>
    <div class="field" style="flex:1 1 70px"><label for="tm">{{m_l}}</label><input type="number" id="tm" min="0" step="1" value="55"></div>
    <div class="field" style="flex:1 1 70px"><label for="ts">{{s_l}}</label><input type="number" id="ts" min="0" max="59" step="1" value="0"></div>
  </div>
  <p class="msg bad hide" id="perr">{{perr}}</p>
  <div class="result hide" id="pout">
    <div class="big" id="pmain"></div>
    <div class="sub" id="psub"></div>
    <div class="stats">
      <div class="stat"><b id="pkmh"></b><span>{{speed_l}}</span></div>
      <div class="stat"><b id="pmi"></b><span>{{mi_l}}</span></div>
      <div class="stat"><b id="p400"></b><span>{{lap_l}}</span></div>
      <div class="stat"><b id="pmph"></b><span>{{mph_l}}</span></div>
    </div>
    <h3 style="font-size:1rem;margin-top:16px">{{riegel_t}}</h3>
    <div class="table-wrap"><table><thead><tr><th>{{col_dist}}</th><th>{{col_time}}</th><th>{{col_pace}}</th></tr></thead><tbody id="riegel"></tbody></table></div>
    <details style="margin-top:12px"><summary style="cursor:pointer;font-weight:600">{{splits_t}}</summary>
      <div class="table-wrap laps"><table><tbody id="splits"></tbody></table></div>
    </details>
  </div>
</div>
<div id="tab-time" class="hide">
  <div class="lbl">{{pace_in}}</div>
  <div class="row" style="margin-top:6px">
    <div class="field" style="flex:1 1 70px"><label for="pm">{{m_l}}</label><input type="number" id="pm" min="0" step="1" value="5"></div>
    <div class="field" style="flex:1 1 70px"><label for="ps">{{s_l}}</label><input type="number" id="ps" min="0" max="59" step="1" value="15"></div>
    <div class="field" style="flex:1 1 110px"><label for="pu">{{unit_l}}</label><select id="pu"><option value="km">{{u_km}}</option><option value="mi">{{u_mi}}</option></select></div>
  </div>
  <div class="field"><label for="dist2">{{dist2_l}}</label><input type="text" inputmode="decimal" id="dist2" value="21,0975"></div>
  <div class="inline" style="margin:-4px 0 14px">
    <button class="btn small" type="button" data-d2="5">5 km</button><button class="btn small" type="button" data-d2="10">10 km</button>
    <button class="btn small" type="button" data-d2="21.0975">{{half}}</button><button class="btn small" type="button" data-d2="42.195">{{marathon}}</button>
  </div>
  <div class="result hide" id="tout">
    <div class="big" id="tmain"></div>
    <div class="sub" id="tsub"></div>
    <h3 style="font-size:1rem;margin-top:16px">{{std_t}}</h3>
    <div class="table-wrap"><table><thead><tr><th>{{col_dist}}</th><th>{{col_time}}</th></tr></thead><tbody id="ttable"></tbody></table></div>
  </div>
</div>
<div id="tab-conv" class="hide">
  <div class="field"><label for="kmh">{{kmh_l}}</label><input type="text" inputmode="decimal" id="kmh" value="12"></div>
  <div class="result" style="margin-top:0"><div class="big" id="cres"></div><div class="sub" id="csub"></div></div>
  <h3 style="font-size:1rem">{{conv2_t}}</h3>
  <div class="row">
    <div class="field" style="flex:1 1 70px"><label for="cm">{{m_l}}</label><input type="number" id="cm" min="0" step="1" value="5"></div>
    <div class="field" style="flex:1 1 70px"><label for="cs">{{s_l}}</label><input type="number" id="cs" min="0" max="59" step="1" value="30"></div>
  </div>
  <div class="result" style="margin-top:0"><div class="big" id="cres2"></div><div class="sub" id="csub2"></div></div>
  <h3 style="font-size:1rem">{{tread_t}}</h3>
  <div class="table-wrap laps" style="max-height:320px"><table><thead><tr><th>{{col_kmh}}</th><th>{{col_mkm}}</th><th>{{col_mmi}}</th><th>{{col_10}}</th><th>{{col_half}}</th></tr></thead><tbody id="treadmill"></tbody></table></div>
</div>
""",
    "js": _JS,
    "article": {
        "it": f"""
<h2>Come si calcola il passo di corsa</h2>
<p>Il passo (o ritmo) è il tempo che impieghi a percorrere un chilometro: si divide il tempo totale per i chilometri. 10 km in 55 minuti → 55 ÷ 10 = 5,5 minuti, cioè <strong>5:30 al km</strong> (5 minuti e 30 secondi, non 5,30). La velocità in km/h è l'inverso: 60 ÷ 5,5 = 10,9 km/h. Nella prima scheda trovi anche il passo al miglio, il tempo per un giro di pista da 400 metri e i parziali chilometro per chilometro.</p>
<h2>Da km/h a min/km (tapis roulant)</h2>
<p>Il tapis roulant mostra la velocità in km/h, gli orologi e le app di corsa il passo in min/km. Per passare dall'una all'altro si divide 60 per la velocità: a 12 km/h il passo è 60 ÷ 12 = 5 minuti al km; a 10,5 km/h è 5,71 minuti, cioè 5:43 al km. La terza scheda ha una tabella da 6 a 20 km/h con i tempi sui 10 km e sulla mezza maratona.</p>
<h2>I tempi previsti con la formula di Riegel</h2>
<p>Dal risultato di una gara il calcolatore stima i tempi su altre distanze con la formula di Pete Riegel: <strong>T2 = T1 × (D2 ÷ D1)<sup>1,06</sup></strong>. L'esponente 1,06 tiene conto del fatto che, allungando la distanza, il ritmo cala un po'. Esempio: chi corre i 10 km in 50 minuti può puntare alla mezza maratona in circa {_R_HALF} e alla maratona in circa {_R_MAR}. È una stima: funziona bene se sei allenato per la distanza più lunga, mentre per la maratona tende a essere ottimistica senza i lunghi.</p>
<h2>Le distanze delle gare</h2>
<p>I 5 km e i 10 km sono le distanze più comuni delle corse su strada; la mezza maratona misura 21,0975 km e la maratona 42,195 km. Un miglio corrisponde a 1,609 km, per questo il passo al miglio è circa 1,6 volte quello al chilometro.</p>
""",
        "en": f"""
<h2>How running pace is calculated</h2>
<p>Pace is the time it takes you to run one kilometre (or one mile): divide the total time by the distance. 10 km in 55 minutes → 55 ÷ 10 = 5.5 minutes, i.e. <strong>5:30 per km</strong> (5 minutes 30 seconds, not 5.30). Speed in km/h is the inverse: 60 ÷ 5.5 = 10.9 km/h. The first tab also shows the pace per mile, the time for a 400-metre track lap and the kilometre splits.</p>
<h2>From km/h to min/km (treadmill)</h2>
<p>Treadmills show speed in km/h, while running watches and apps show pace in min/km. To convert, divide 60 by the speed: at 12 km/h the pace is 60 ÷ 12 = 5 minutes per km; at 10.5 km/h it is 5.71 minutes, i.e. 5:43 per km. The third tab has a table from 6 to 20 km/h with 10K and half-marathon times.</p>
<h2>Predicted times with the Riegel formula</h2>
<p>From a race result the calculator estimates your times over other distances with Pete Riegel's formula: <strong>T2 = T1 × (D2 ÷ D1)<sup>1.06</sup></strong>. The 1.06 exponent reflects the fact that pace drops a little as the distance grows. Example: a 50-minute 10K runner can aim for a half marathon in about {_R_HALF} and a marathon in about {_R_MAR}. It is an estimate: it works well if you are trained for the longer distance, and it tends to be optimistic for the marathon without long runs.</p>
<h2>Race distances</h2>
<p>5K and 10K are the most common road race distances; the half marathon is 21.0975 km and the marathon 42.195 km. A mile is 1.609 km, which is why pace per mile is about 1.6 times pace per kilometre.</p>
""",
    },
    "faq": {
        "it": [
            ("5:30 al km quanti km/h sono?", "10,91 km/h: 5:30 sono 5,5 minuti e 60 ÷ 5,5 = 10,91."),
            ("A che passo si corre una maratona in 4 ore?", f"A {_P_4H} al km: 4 ore sono 240 minuti, divisi per 42,195 km fanno 5,69 minuti, cioè 5 minuti e 41 secondi."),
            ("Che passo serve per correre 10 km in 50 minuti?", "5:00 al km, cioè 12 km/h."),
            ("Il calcolatore tiene conto delle salite?", "No: calcola il passo medio come su un percorso piatto. Salite, vento e caldo rallentano; per le previsioni usa una gara recente su un percorso simile."),
        ],
        "en": [
            ("What is 5:30 per km in km/h?", "10.91 km/h: 5:30 is 5.5 minutes and 60 ÷ 5.5 = 10.91."),
            ("What pace do I need for a 4-hour marathon?", f"{_P_4H} per km (about 9:09 per mile): 240 minutes divided by 42.195 km is 5.69 minutes, i.e. 5 minutes 41 seconds."),
            ("What pace do I need to run 10 km in 50 minutes?", "5:00 per km, i.e. 12 km/h."),
            ("Does the calculator account for hills?", "No: it works out the average pace as if on a flat course. Hills, wind and heat slow you down; for predictions use a recent race on a similar course."),
        ],
    },
}

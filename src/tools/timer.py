TOOL = {
    "id": "timer",
    "cat": "date",
    "icon": "⏱️",
    "slug": {"it": "timer-online", "en": "online-timer"},
    "title": {"it": "Timer e cronometro online", "en": "Online timer and stopwatch"},
    "short": {"it": "Conto alla rovescia con suono e cronometro con giri", "en": "Countdown with alarm and stopwatch with laps"},
    "keywords": {"it": ["timer 5 minuti", "timer 10 minuti", "pomodoro", "cronometro online", "conto alla rovescia"], "en": ["5 minute timer", "10 minute timer", "pomodoro", "stopwatch", "countdown"]},
    "meta": {
        "it": "Timer online gratuito con suono alla fine e cronometro con giri. Preset da 1 a 60 minuti, tempo personalizzato, funziona su telefono e PC senza installare nulla.",
        "en": "Free online timer with an alarm at the end and a stopwatch with laps. Presets from 1 to 60 minutes, custom time, works on phone and desktop with nothing to install.",
    },
    "intro": {
        "it": "Imposta un conto alla rovescia con un tocco (1, 5, 10, 25 minuti…) o un tempo a piacere: alla fine suona un avviso. Nella seconda scheda trovi un cronometro con i giri.",
        "en": "Set a countdown with one tap (1, 5, 10, 25 minutes…) or any custom time: an alarm sounds at the end. The second tab has a stopwatch with laps.",
    },
    "strings": {
        "it": {
            "timer": "Timer", "stopwatch": "Cronometro", "min": "Minuti", "sec": "Secondi", "start": "Avvia", "pause": "Pausa", "resume": "Riprendi", "reset": "Azzera",
            "lap": "Giro", "laps": "Giri", "done": "Tempo scaduto!", "presets": "Preset", "set": "Imposta", "total": "Totale", "sound": "Suono alla fine",
        },
        "en": {
            "timer": "Timer", "stopwatch": "Stopwatch", "min": "Minutes", "sec": "Seconds", "start": "Start", "pause": "Pause", "resume": "Resume", "reset": "Reset",
            "lap": "Lap", "laps": "Laps", "done": "Time's up!", "presets": "Presets", "set": "Set", "total": "Total", "sound": "Sound at the end",
        },
    },
    "ui": """
<div class="tabs"><button type="button" class="on" data-tab="t">{{timer}}</button><button type="button" data-tab="s">{{stopwatch}}</button></div>
<div id="tab-t">
  <div class="inline"><span class="lbl">{{presets}}:</span>
    <button class="btn small" type="button" data-p="1">1 min</button><button class="btn small" type="button" data-p="3">3 min</button>
    <button class="btn small" type="button" data-p="5">5 min</button><button class="btn small" type="button" data-p="10">10 min</button>
    <button class="btn small" type="button" data-p="15">15 min</button><button class="btn small" type="button" data-p="20">20 min</button>
    <button class="btn small" type="button" data-p="25">25 min</button><button class="btn small" type="button" data-p="30">30 min</button>
    <button class="btn small" type="button" data-p="45">45 min</button><button class="btn small" type="button" data-p="60">60 min</button></div>
  <div class="row" style="margin-top:12px">
    <div class="field"><label for="tm">{{min}}</label><input type="number" id="tm" value="5" min="0" max="999" inputmode="numeric"></div>
    <div class="field"><label for="ts">{{sec}}</label><input type="number" id="ts" value="0" min="0" max="59" inputmode="numeric"></div>
  </div>
  <label class="check"><input type="checkbox" id="snd" checked> {{sound}}</label>
  <div class="timer-display" id="tdisp">05:00</div>
  <p class="msg ok hide" id="tdone" style="text-align:center;font-size:1.2rem;font-weight:700">🔔 {{done}}</p>
  <div class="btns" style="justify-content:center">
    <button class="btn primary" type="button" id="tstart">{{start}}</button>
    <button class="btn" type="button" id="treset">{{reset}}</button>
  </div>
</div>
<div id="tab-s" class="hide">
  <div class="timer-display" id="sdisp">00:00.0</div>
  <div class="btns" style="justify-content:center">
    <button class="btn primary" type="button" id="sstart">{{start}}</button>
    <button class="btn" type="button" id="slap" disabled>{{lap}}</button>
    <button class="btn" type="button" id="sreset">{{reset}}</button>
  </div>
  <div class="laps table-wrap hide" id="laps"><table><thead><tr><th>#</th><th>{{lap}}</th><th>{{total}}</th></tr></thead><tbody id="lapbody"></tbody></table></div>
</div>
""",
    "js": r"""
var tabs = RT.$$('.tabs button');
tabs.forEach(function (b) { b.addEventListener('click', function () {
  tabs.forEach(function (x) { x.classList.toggle('on', x === b); });
  RT.$('#tab-t').classList.toggle('hide', b.getAttribute('data-tab') !== 't');
  RT.$('#tab-s').classList.toggle('hide', b.getAttribute('data-tab') !== 's');
}); });
var baseTitle = document.title;
// ---- timer
var tm = RT.$('#tm'), ts = RT.$('#ts'), tdisp = RT.$('#tdisp'), tstart = RT.$('#tstart'), tdone = RT.$('#tdone');
var tEnd = 0, tLeft = 0, tRunning = false, tTick = null;
function fmtT(ms) { var s = Math.max(0, Math.ceil(ms / 1000)); var h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60; return (h ? h + ':' + RT.pad(m) : RT.pad(m)) + ':' + RT.pad(x); }
function tSet() { var ms = ((parseInt(tm.value, 10) || 0) * 60 + (parseInt(ts.value, 10) || 0)) * 1000; tLeft = ms; tdisp.textContent = fmtT(ms); tdone.classList.add('hide'); }
function tRender() { var left = tEnd - Date.now(); tdisp.textContent = fmtT(left); document.title = fmtT(left) + ' – ' + baseTitle; if (left <= 0) tFinish(); }
function tFinish() { clearInterval(tTick); tRunning = false; tLeft = 0; tstart.textContent = T.start; tdone.classList.remove('hide'); document.title = '🔔 ' + T.done; if (RT.$('#snd').checked) RT.beep(4); }
tstart.addEventListener('click', function () {
  if (tRunning) { clearInterval(tTick); tRunning = false; tLeft = tEnd - Date.now(); tstart.textContent = T.resume; return; }
  if (tLeft <= 0) tSet(); if (tLeft <= 0) return;
  tEnd = Date.now() + tLeft; tRunning = true; tstart.textContent = T.pause; tdone.classList.add('hide');
  tTick = setInterval(tRender, 200); tRender();
});
RT.$('#treset').addEventListener('click', function () { clearInterval(tTick); tRunning = false; tstart.textContent = T.start; document.title = baseTitle; tSet(); });
RT.$$('[data-p]').forEach(function (b) { b.addEventListener('click', function () { tm.value = b.getAttribute('data-p'); ts.value = 0; clearInterval(tTick); tRunning = false; tstart.textContent = T.start; tSet(); }); });
[tm, ts].forEach(function (el) { el.addEventListener('input', function () { if (!tRunning) tSet(); }); });
tSet();
// ---- stopwatch
var sdisp = RT.$('#sdisp'), sstart = RT.$('#sstart'), slap = RT.$('#slap'), lapbody = RT.$('#lapbody'), lapsBox = RT.$('#laps');
var sStartAt = 0, sAcc = 0, sRunning = false, sTick = null, lastLap = 0, lapN = 0;
function fmtS(ms) { var h = Math.floor(ms / 3600000), m = Math.floor(ms % 3600000 / 60000), s = Math.floor(ms % 60000 / 1000), d = Math.floor(ms % 1000 / 100); return (h ? h + ':' + RT.pad(m) : RT.pad(m)) + ':' + RT.pad(s) + '.' + d; }
function sNow() { return sAcc + (sRunning ? Date.now() - sStartAt : 0); }
function sRender() { sdisp.textContent = fmtS(sNow()); }
sstart.addEventListener('click', function () {
  if (sRunning) { sAcc = sNow(); sRunning = false; clearInterval(sTick); sstart.textContent = T.resume; slap.disabled = true; sRender(); return; }
  sStartAt = Date.now(); sRunning = true; sstart.textContent = T.pause; slap.disabled = false; sTick = setInterval(sRender, 100);
});
slap.addEventListener('click', function () {
  var now = sNow(); lapN++; var tr = document.createElement('tr');
  tr.innerHTML = '<td>' + lapN + '</td><td>' + fmtS(now - lastLap) + '</td><td>' + fmtS(now) + '</td>';
  lapbody.insertBefore(tr, lapbody.firstChild); lastLap = now; lapsBox.classList.remove('hide');
});
RT.$('#sreset').addEventListener('click', function () { clearInterval(sTick); sRunning = false; sAcc = 0; lastLap = 0; lapN = 0; lapbody.innerHTML = ''; lapsBox.classList.add('hide'); sstart.textContent = T.start; slap.disabled = true; sRender(); });
""",
    "article": {
        "it": """
<h2>Come usare il timer</h2>
<p>Scegli un preset (per esempio 5 o 10 minuti) oppure scrivi minuti e secondi, poi premi <strong>Avvia</strong>. Il tempo rimanente compare in grande e anche nel titolo della scheda del browser, così lo vedi pure mentre lavori in un'altra pagina. Puoi mettere in pausa e riprendere; alla fine compare l'avviso «Tempo scaduto» e, se hai lasciato la spunta, suona un segnale acustico.</p>
<h2>Idee d'uso</h2>
<ul>
<li><strong>Tecnica del pomodoro:</strong> 25 minuti di lavoro concentrato e 5 di pausa; dopo quattro «pomodori» una pausa più lunga.</li>
<li><strong>Cucina:</strong> pasta, uova, lievitazione, infusione del tè.</li>
<li><strong>Studio ed esami:</strong> simula il tempo a disposizione per una prova.</li>
<li><strong>Sport:</strong> intervalli, plank, stretching, riposo tra le serie.</li>
<li><strong>Bambini:</strong> tempo dei compiti, dei giochi o dello schermo.</li>
</ul>
<h2>Il cronometro</h2>
<p>Nella scheda «Cronometro» premi Avvia e usa <strong>Giro</strong> per registrare i tempi parziali: la tabella mostra la durata di ogni giro e il tempo totale. Il decimo di secondo è sufficiente per la maggior parte degli usi quotidiani.</p>
<h2>Precisione e limiti</h2>
<p>Il timer si basa sull'orologio del dispositivo, quindi resta preciso anche se il browser rallenta l'aggiornamento della pagina. Perché il suono parta, la scheda deve restare aperta (anche in secondo piano); alcuni telefoni sospendono le pagine inattive per risparmiare batteria, quindi per tempi lunghi tieni lo schermo acceso o usa la sveglia del telefono.</p>
""",
        "en": """
<h2>How to use the timer</h2>
<p>Pick a preset (for example 5 or 10 minutes) or type minutes and seconds, then press <strong>Start</strong>. The remaining time is shown in large digits and in the browser tab title, so you can see it while working in another page. You can pause and resume; at the end a "Time's up" notice appears and, if the box is ticked, an alarm sounds.</p>
<h2>Ideas for using it</h2>
<ul>
<li><strong>Pomodoro technique:</strong> 25 minutes of focused work and a 5-minute break; after four "pomodoros", a longer break.</li>
<li><strong>Cooking:</strong> pasta, eggs, dough proofing, tea steeping.</li>
<li><strong>Study and exams:</strong> simulate the time allowed for a test.</li>
<li><strong>Sport:</strong> intervals, planks, stretching, rest between sets.</li>
<li><strong>Kids:</strong> homework, play or screen time.</li>
</ul>
<h2>The stopwatch</h2>
<p>In the "Stopwatch" tab press Start and use <strong>Lap</strong> to record split times: the table shows each lap's duration and the total time. Tenths of a second are enough for most everyday uses.</p>
<h2>Accuracy and limits</h2>
<p>The timer relies on the device clock, so it stays accurate even if the browser slows down page updates. For the sound to play the tab must stay open (in the background is fine); some phones suspend inactive pages to save battery, so for long timers keep the screen on or use your phone's alarm.</p>
""",
    },
    "faq": {
        "it": [
            ("Il timer suona anche se cambio scheda?", "Sì, purché la scheda resti aperta nel browser. Se blocchi il telefono o chiudi il browser, il suono potrebbe non partire."),
            ("Posso impostare più di 60 minuti?", "Sì: scrivi i minuti che vuoi nel campo «Minuti», per esempio 90 o 120."),
            ("Il cronometro è preciso?", "Usa l'orologio del dispositivo e mostra i decimi di secondo: più che sufficiente per allenamenti, giochi e prove di velocità."),
        ],
        "en": [
            ("Does the timer ring if I switch tabs?", "Yes, as long as the tab stays open in the browser. If you lock your phone or close the browser, the sound may not play."),
            ("Can I set more than 60 minutes?", "Yes: type any number of minutes in the \"Minutes\" field, for example 90 or 120."),
            ("Is the stopwatch accurate?", "It uses the device clock and shows tenths of a second: more than enough for workouts, games and speed tests."),
        ],
    },
}

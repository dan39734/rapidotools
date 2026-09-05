TOOL = {
    "id": "random",
    "cat": "numbers",
    "icon": "🎲",
    "slug": {"it": "numeri-casuali", "en": "random-number-generator"},
    "title": {"it": "Generatore di numeri casuali, dadi e testa o croce", "en": "Random number generator, dice and coin flip"},
    "short": {"it": "Estrai numeri tra un minimo e un massimo, lancia dadi, tira una moneta", "en": "Draw numbers between a minimum and a maximum, roll dice, flip a coin"},
    "keywords": {"it": ["numero casuale da 1 a 10", "estrazione casuale", "lancia dadi online", "sorteggio", "tira moneta"], "en": ["random number 1 to 10", "dice roller", "coin toss", "raffle", "pick a number"]},
    "meta": {
        "it": "Genera numeri casuali tra un minimo e un massimo (anche senza ripetizioni), lancia uno o più dadi da 4 a 100 facce e tira una moneta. Ideale per sorteggi, giochi e decisioni.",
        "en": "Generate random numbers between a minimum and a maximum (with or without repeats), roll one or more dice from 4 to 100 sides and flip a coin. Ideal for raffles, games and decisions.",
    },
    "intro": {
        "it": "Imposta l'intervallo e quanti numeri vuoi, oppure scegli i dadi da lanciare o affidati alla moneta: i risultati usano il generatore crittografico del browser, quindi sono davvero imprevedibili.",
        "en": "Set the range and how many numbers you want, or pick the dice to roll or leave it to the coin: results use the browser's cryptographic generator, so they are truly unpredictable.",
    },
    "strings": {
        "it": {
            "tab_n": "Numeri", "tab_d": "Dadi", "tab_c": "Testa o croce", "min": "Minimo", "max": "Massimo", "count": "Quanti numeri", "unique": "Senza ripetizioni", "sorted": "In ordine crescente",
            "gen": "Genera", "roll": "Lancia", "flip": "Tira la moneta", "dice": "Tipo di dado", "ndice": "Numero di dadi", "sum": "Somma", "heads": "Testa", "tails": "Croce",
            "err_range": "Il massimo deve essere maggiore o uguale al minimo.", "err_unique": "Per estrarre senza ripetizioni servono almeno tanti numeri quanti ne chiedi.", "history": "Storico",
        },
        "en": {
            "tab_n": "Numbers", "tab_d": "Dice", "tab_c": "Coin flip", "min": "Minimum", "max": "Maximum", "count": "How many numbers", "unique": "No repeats", "sorted": "Sort ascending",
            "gen": "Generate", "roll": "Roll", "flip": "Flip the coin", "dice": "Die type", "ndice": "Number of dice", "sum": "Total", "heads": "Heads", "tails": "Tails",
            "err_range": "The maximum must be greater than or equal to the minimum.", "err_unique": "Drawing without repeats needs at least as many numbers as you ask for.", "history": "History",
        },
    },
    "ui": """
<div class="tabs"><button type="button" class="on" data-tab="n">{{tab_n}}</button><button type="button" data-tab="d">{{tab_d}}</button><button type="button" data-tab="c">{{tab_c}}</button></div>
<div id="tab-n">
  <div class="row">
    <div class="field"><label for="min">{{min}}</label><input type="number" id="min" value="1" inputmode="numeric"></div>
    <div class="field"><label for="max">{{max}}</label><input type="number" id="max" value="100" inputmode="numeric"></div>
    <div class="field"><label for="cnt">{{count}}</label><input type="number" id="cnt" value="1" min="1" max="1000" inputmode="numeric"></div>
  </div>
  <div class="inline"><label class="check"><input type="checkbox" id="uniq"> {{unique}}</label><label class="check"><input type="checkbox" id="sorted"> {{sorted}}</label></div>
  <p class="msg bad hide" id="err"></p>
  <div class="btns"><button class="btn primary" type="button" id="gen">{{gen}}</button></div>
</div>
<div id="tab-d" class="hide">
  <div class="row">
    <div class="field"><label for="die">{{dice}}</label><select id="die"><option value="4">D4</option><option value="6" selected>D6</option><option value="8">D8</option><option value="10">D10</option><option value="12">D12</option><option value="20">D20</option><option value="100">D100</option></select></div>
    <div class="field"><label for="nd">{{ndice}}</label><input type="number" id="nd" value="2" min="1" max="50" inputmode="numeric"></div>
  </div>
  <div class="btns"><button class="btn primary" type="button" id="roll">🎲 {{roll}}</button></div>
</div>
<div id="tab-c" class="hide">
  <div class="btns"><button class="btn primary" type="button" id="flip">🪙 {{flip}}</button></div>
</div>
<div class="result hide" id="out"><div class="big" id="main" style="word-break:break-word"></div><div class="sub" id="sub"></div></div>
<p class="msg" id="hist"></p>
""",
    "js": r"""
var tabs = RT.$$('.tabs button'), cur = 'n', hist = [];
tabs.forEach(function (b) { b.addEventListener('click', function () { cur = b.getAttribute('data-tab'); tabs.forEach(function (x) { x.classList.toggle('on', x === b); }); ['n', 'd', 'c'].forEach(function (k) { RT.$('#tab-' + k).classList.toggle('hide', k !== cur); }); RT.$('#out').classList.add('hide'); }); });
function rnd(n) { var a = new Uint32Array(1); var max = Math.floor(4294967296 / n) * n; do { crypto.getRandomValues(a); } while (a[0] >= max); return a[0] % n; }
function show(main, sub) { RT.$('#main').textContent = main; RT.$('#sub').textContent = sub || ''; RT.$('#out').classList.remove('hide'); hist.unshift(main); hist = hist.slice(0, 8); RT.$('#hist').textContent = hist.length > 1 ? T.history + ': ' + hist.slice(1).join(' | ') : ''; }
RT.$('#gen').addEventListener('click', function () {
  var err = RT.$('#err'); err.classList.add('hide');
  var lo = parseInt(RT.$('#min').value, 10), hi = parseInt(RT.$('#max').value, 10), n = Math.min(1000, Math.max(1, parseInt(RT.$('#cnt').value, 10) || 1));
  if (isNaN(lo) || isNaN(hi) || hi < lo) { err.textContent = T.err_range; err.classList.remove('hide'); return; }
  var span = hi - lo + 1, res = [];
  if (RT.$('#uniq').checked) {
    if (n > span) { err.textContent = T.err_unique; err.classList.remove('hide'); return; }
    if (span <= 100000) { var pool = []; for (var i = lo; i <= hi; i++) pool.push(i); for (var k = 0; k < n; k++) { var j = k + rnd(pool.length - k); var t = pool[k]; pool[k] = pool[j]; pool[j] = t; res.push(pool[k]); } }
    else { var seen = {}; while (res.length < n) { var x = lo + rnd(span); if (!seen[x]) { seen[x] = 1; res.push(x); } } }
  } else { for (var m = 0; m < n; m++) res.push(lo + rnd(span)); }
  if (RT.$('#sorted').checked) res.sort(function (a, b) { return a - b; });
  show(res.join(', '), n > 1 ? T.sum + ': ' + RT.fmt(res.reduce(function (a, b) { return a + b; }, 0), 0) : '');
});
RT.$('#roll').addEventListener('click', function () {
  var sides = +RT.$('#die').value, n = Math.min(50, Math.max(1, parseInt(RT.$('#nd').value, 10) || 1)), res = [];
  for (var i = 0; i < n; i++) res.push(1 + rnd(sides));
  show(res.join(' + '), (n > 1 ? T.sum + ': ' + res.reduce(function (a, b) { return a + b; }, 0) + ' · ' : '') + n + '×D' + sides);
});
RT.$('#flip').addEventListener('click', function () { show(rnd(2) ? '🪙 ' + T.heads : '🪙 ' + T.tails); });
""",
    "article": {
        "it": """
<h2>Come funziona</h2>
<p>I numeri vengono estratti con <code>crypto.getRandomValues</code>, il generatore crittografico del browser: è lo stesso meccanismo usato per creare chiavi e password, quindi non c'è nessuno schema ripetitivo e nessun modo di prevedere il prossimo risultato. Ogni valore dell'intervallo ha esattamente la stessa probabilità di uscire.</p>
<h2>Numeri</h2>
<p>Imposta minimo e massimo (entrambi inclusi) e quanti numeri vuoi. Con «Senza ripetizioni» ottieni un'estrazione come quella del lotto o di una tombola: ogni numero può uscire una volta sola, utile per sorteggiare i vincitori di un concorso o l'ordine di intervento in una riunione. «In ordine crescente» rende più facile leggere una lista lunga.</p>
<h2>Dadi</h2>
<p>Puoi lanciare da 1 a 50 dadi a 4, 6, 8, 10, 12, 20 o 100 facce, quelli dei giochi da tavolo e dei giochi di ruolo. Il risultato mostra i singoli lanci e la somma. Per «2d6» scegli D6 e 2 dadi; per un tiro salvezza con vantaggio lancia 2 D20 e tieni il più alto.</p>
<h2>Testa o croce</h2>
<p>Una moneta equa al 50%: per decidere chi inizia, chi lava i piatti o quale film guardare. Lo storico sotto il risultato mostra gli ultimi lanci.</p>
<h2>Idee d'uso</h2>
<ul>
<li>Sorteggi tra i partecipanti a un evento (assegna a ciascuno un numero e estrai).</li>
<li>Scegliere a caso un esercizio, una ricetta, una domanda d'esame da ripassare.</li>
<li>Simulazioni e giochi in classe, esempi di statistica, bingo e tombola.</li>
</ul>
""",
        "en": """
<h2>How it works</h2>
<p>Numbers are drawn with <code>crypto.getRandomValues</code>, the browser's cryptographic generator: the same mechanism used to create keys and passwords, so there is no repeating pattern and no way to predict the next result. Every value in the range has exactly the same chance of coming up.</p>
<h2>Numbers</h2>
<p>Set the minimum and maximum (both included) and how many numbers you want. With "No repeats" you get a draw like a lottery or a raffle: each number can come up only once, useful for picking contest winners or the speaking order in a meeting. "Sort ascending" makes a long list easier to read.</p>
<h2>Dice</h2>
<p>Roll 1 to 50 dice with 4, 6, 8, 10, 12, 20 or 100 sides, the ones used in board games and role-playing games. The result shows each roll and the total. For "2d6" choose D6 and 2 dice; for a saving throw with advantage roll 2 D20 and keep the higher.</p>
<h2>Coin flip</h2>
<p>A fair 50/50 coin: to decide who starts, who does the dishes or which film to watch. The history under the result shows the latest flips.</p>
<h2>Ideas</h2>
<ul>
<li>Draws among event participants (give everyone a number and draw).</li>
<li>Pick a random exercise, recipe or exam question to revise.</li>
<li>Classroom games and simulations, statistics examples, bingo.</li>
</ul>
""",
    },
    "faq": {
        "it": [
            ("I numeri sono davvero casuali?", "Sì. Vengono generati con il generatore crittografico del browser, non con una formula prevedibile, e ogni numero dell'intervallo ha la stessa probabilità."),
            ("Posso estrarre numeri senza ripetizioni?", "Sì: spunta «Senza ripetizioni». Il numero di estrazioni non può superare l'ampiezza dell'intervallo."),
            ("Quanti numeri posso generare in una volta?", "Fino a 1.000 per estrazione; per i dadi fino a 50 lanci insieme."),
        ],
        "en": [
            ("Are the numbers truly random?", "Yes. They are generated with the browser's cryptographic generator, not a predictable formula, and every number in the range is equally likely."),
            ("Can I draw numbers without repeats?", "Yes: tick \"No repeats\". The number of draws cannot exceed the size of the range."),
            ("How many numbers can I generate at once?", "Up to 1,000 per draw; for dice up to 50 rolls at a time."),
        ],
    },
}

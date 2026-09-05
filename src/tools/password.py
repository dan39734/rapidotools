WORDS_IT = ("albero amico ancora aprile arancia argento aria autunno banana barca bianco bosco bottiglia caffe calore campo cane carta casa castello cavallo cena chiave cielo cinema citta collina colore coniglio corda cucina cuore delfino dente domenica donna erba estate farfalla ferro festa fiore fiume foglia forchetta formica fragola freddo frutta fuoco gatto gelato giallo giardino giornale giovedi girasole grano isola lago lampada latte legno leone lettera libro limone luce luna lupo mano mare martedi matita mattina medusa mela mercato miele montagna musica nave neve notte nuvola oceano olio ombra onda orologio orso ospite pane panna pesce piano pianta piazza pietra pioggia pizza ponte porta prato primavera quadro radice ragno rana regalo riso rosa rosso ruota sabbia sale scuola sedia sera serpente sole specchio spiaggia stella strada tavolo tazza teatro terra tetto tigre torre treno uccello uovo valle vento verde vetro viaggio vino viola volpe zaino zucchero").split()
WORDS_EN = ("apple anchor arrow autumn badger bamboo basket beach bench berry bird blanket bottle branch bread breeze bridge butter cabin candle canyon carrot castle cherry cloud coffee comet copper coral cotton cricket crystal dolphin donkey dragon eagle ember engine falcon feather fiddle forest fossil garden garlic ginger glacier goose guitar hammer harbor hazel honey island jacket jungle kettle lantern lemon lily lobster maple marble meadow melon mirror monkey mountain muffin needle nickel noodle oak ocean olive orbit orchid otter oyster paddle panda parrot pebble pencil pepper piano pillow pirate planet plum pocket puzzle rabbit radio rainbow river rocket saddle salmon sandal shadow silver spider spoon square summer sunset thunder tiger tomato tulip turtle umbrella valley velvet violin walnut walrus willow window winter yogurt zebra").split()

TOOL = {
    "id": "password",
    "cat": "text",
    "icon": "🔑",
    "slug": {"it": "generatore-password", "en": "password-generator"},
    "title": {"it": "Generatore di password sicure", "en": "Strong password generator"},
    "short": {"it": "Password casuali o frasi facili da ricordare, con misura della robustezza", "en": "Random passwords or memorable passphrases, with strength rating"},
    "keywords": {"it": ["password sicura", "password casuale", "genera password", "passphrase"], "en": ["random password", "secure password", "passphrase generator", "strong password"]},
    "meta": {
        "it": "Genera password sicure e casuali (lettere, numeri, simboli) o frasi segrete facili da ricordare. Creazione nel browser: nessuna password viene inviata o salvata.",
        "en": "Generate strong random passwords (letters, numbers, symbols) or easy-to-remember passphrases. Created in your browser: no password is sent or stored anywhere.",
    },
    "intro": {
        "it": "Scegli lunghezza e caratteri, oppure crea una frase segreta di parole casuali: la password viene generata sul tuo dispositivo con un generatore crittografico e non lascia mai il browser.",
        "en": "Choose length and character types, or build a passphrase from random words: the password is generated on your device with a cryptographic generator and never leaves the browser.",
    },
    "strings": {
        "it": {
            "tab_pw": "Password casuale", "tab_pp": "Frase segreta", "length": "Lunghezza", "upper": "Maiuscole (A-Z)", "lower": "Minuscole (a-z)", "digits": "Numeri (0-9)", "symbols": "Simboli (!@#$%…)",
            "ambig": "Evita caratteri ambigui (l, 1, I, O, 0)", "generate": "Genera", "again": "Genera di nuovo", "strength": "Robustezza",
            "weak": "Debole", "fair": "Discreta", "good": "Buona", "strong": "Forte", "very": "Molto forte", "bits": "bit di entropia",
            "words": "Numero di parole", "sep": "Separatore", "cap": "Iniziali maiuscole", "addnum": "Aggiungi un numero", "lang_words": "Lingua delle parole", "it": "Italiano", "en": "Inglese", "space": "spazio", "none": "nessuno",
            "err": "Seleziona almeno un tipo di carattere.",
        },
        "en": {
            "tab_pw": "Random password", "tab_pp": "Passphrase", "length": "Length", "upper": "Uppercase (A-Z)", "lower": "Lowercase (a-z)", "digits": "Numbers (0-9)", "symbols": "Symbols (!@#$%…)",
            "ambig": "Avoid ambiguous characters (l, 1, I, O, 0)", "generate": "Generate", "again": "Generate again", "strength": "Strength",
            "weak": "Weak", "fair": "Fair", "good": "Good", "strong": "Strong", "very": "Very strong", "bits": "bits of entropy",
            "words": "Number of words", "sep": "Separator", "cap": "Capitalise words", "addnum": "Add a number", "lang_words": "Word language", "it": "Italian", "en": "English", "space": "space", "none": "none",
            "err": "Select at least one character type.",
        },
    },
    "ui": """
<div class="tabs"><button type="button" class="on" data-tab="pw">{{tab_pw}}</button><button type="button" data-tab="pp">{{tab_pp}}</button></div>
<div id="tab-pw">
  <div class="field"><label for="len">{{length}}: <b id="lenv">16</b></label><input type="range" id="len" min="6" max="64" value="16"></div>
  <div class="row">
    <label class="check"><input type="checkbox" id="up" checked> {{upper}}</label>
    <label class="check"><input type="checkbox" id="lo" checked> {{lower}}</label>
    <label class="check"><input type="checkbox" id="di" checked> {{digits}}</label>
    <label class="check"><input type="checkbox" id="sy" checked> {{symbols}}</label>
  </div>
  <label class="check"><input type="checkbox" id="am"> {{ambig}}</label>
</div>
<div id="tab-pp" class="hide">
  <div class="row">
    <div class="field"><label for="nw">{{words}}</label><select id="nw"><option>3</option><option selected>4</option><option>5</option><option>6</option><option>7</option></select></div>
    <div class="field"><label for="sep">{{sep}}</label><select id="sep"><option value="-">-</option><option value=".">.</option><option value="_">_</option><option value=" ">{{space}}</option><option value="">{{none}}</option></select></div>
    <div class="field"><label for="wl">{{lang_words}}</label><select id="wl"><option value="it">{{it}}</option><option value="en">{{en}}</option></select></div>
  </div>
  <label class="check"><input type="checkbox" id="cap" checked> {{cap}}</label>
  <label class="check"><input type="checkbox" id="addnum" checked> {{addnum}}</label>
</div>
<p class="msg bad hide" id="err">{{err}}</p>
<div class="result">
  <div class="out"><input type="text" id="pw" class="mono" readonly style="font-size:1.15rem;padding-right:90px"><button class="btn small copy" type="button" data-copy="#pw" data-done="{{copied}}" style="top:6px">{{copy}}</button></div>
  <div class="meter"><i id="bar"></i></div>
  <div class="sub"><span id="str"></span> · <span id="bits"></span> {{bits}}</div>
  <div class="btns"><button class="btn primary" type="button" id="gen">{{again}}</button></div>
</div>
""",
    "js": r"""
var WORDS = { it: %s, en: %s };
var tab = 'pw';
var tabs = RT.$$('.tabs button');
tabs.forEach(function (b) { b.addEventListener('click', function () { tab = b.getAttribute('data-tab'); tabs.forEach(function (x) { x.classList.toggle('on', x === b); }); RT.$('#tab-pw').classList.toggle('hide', tab !== 'pw'); RT.$('#tab-pp').classList.toggle('hide', tab !== 'pp'); gen(); }); });
RT.$('#wl').value = RT.lang;
function rnd(n) { var a = new Uint32Array(1); var max = Math.floor(4294967296 / n) * n; do { crypto.getRandomValues(a); } while (a[0] >= max); return a[0] %% n; }
function pick(s) { return s[rnd(s.length)]; }
function shuffle(arr) { for (var i = arr.length - 1; i > 0; i--) { var j = rnd(i + 1); var t = arr[i]; arr[i] = arr[j]; arr[j] = t; } return arr; }
function rate(bits) {
  var lvl = bits < 40 ? [T.weak, 'var(--bad)', 20] : bits < 60 ? [T.fair, 'var(--warn)', 40] : bits < 80 ? [T.good, 'var(--ok)', 60] : bits < 100 ? [T.strong, 'var(--ok)', 80] : [T.very, 'var(--ok)', 100];
  RT.$('#str').textContent = lvl[0]; RT.$('#bar').style.background = lvl[1]; RT.$('#bar').style.width = lvl[2] + '%%'; RT.$('#bits').textContent = Math.round(bits);
}
function gen() {
  RT.$('#err').classList.add('hide');
  if (tab === 'pw') {
    var sets = [], am = RT.$('#am').checked;
    var U = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', L = 'abcdefghijklmnopqrstuvwxyz', D = '0123456789', S = '!@#$%%^&*()-_=+[]{};:,.?/~';
    if (am) { U = U.replace(/[IO]/g, ''); L = L.replace(/[l]/g, ''); D = D.replace(/[01]/g, ''); }
    if (RT.$('#up').checked) sets.push(U); if (RT.$('#lo').checked) sets.push(L); if (RT.$('#di').checked) sets.push(D); if (RT.$('#sy').checked) sets.push(S);
    if (!sets.length) { RT.$('#err').classList.remove('hide'); RT.$('#pw').value = ''; return; }
    var len = +RT.$('#len').value, all = sets.join(''), out = [];
    sets.forEach(function (s) { out.push(pick(s)); });
    while (out.length < len) out.push(pick(all));
    RT.$('#pw').value = shuffle(out).join('');
    rate(len * Math.log2(all.length));
  } else {
    var list = WORDS[RT.$('#wl').value], n = +RT.$('#nw').value, sep = RT.$('#sep').value, cap = RT.$('#cap').checked, an = RT.$('#addnum').checked;
    var w = []; for (var i = 0; i < n; i++) { var x = pick(list); if (cap) x = x.charAt(0).toUpperCase() + x.slice(1); w.push(x); }
    if (an) w.splice(rnd(n + 1), 0, String(rnd(100)));
    RT.$('#pw').value = w.join(sep);
    rate(n * Math.log2(list.length) + (an ? Math.log2(100) : 0));
  }
}
RT.$('#len').addEventListener('input', function () { RT.$('#lenv').textContent = RT.$('#len').value; gen(); });
RT.$$('#tab-pw input, #tab-pp input, #tab-pp select').forEach(function (el) { el.addEventListener('change', gen); });
RT.$('#gen').addEventListener('click', gen);
gen();
""" % (WORDS_IT, WORDS_EN),
    "article": {
        "it": """
<h2>Cosa rende sicura una password</h2>
<p>Due cose: la <strong>lunghezza</strong> e la <strong>casualità</strong>. Una password di 8 caratteri, anche con simboli, può essere indovinata da un computer in poche ore; una di 16 caratteri casuali richiede secoli. Le parole del dizionario, le date di nascita e le sostituzioni «furbe» come P@ssw0rd sono le prime cose che i programmi di attacco provano, quindi non aggiungono sicurezza reale.</p>
<p>La <strong>robustezza</strong> mostrata sotto la password è espressa in bit di entropia: ogni bit raddoppia il numero di tentativi necessari. Sopra i 60 bit sei al sicuro dagli attacchi comuni; sopra gli 80 anche da quelli più determinati.</p>
<h2>Password casuale o frase segreta?</h2>
<p>La password casuale (es. <code>x7#Kq2!mVp9$Lw4R</code>) è ideale se usi un gestore di password che la ricorda per te. La <strong>frase segreta</strong> (es. <code>Volpe-Lampada-Miele-Treno-42</code>) è altrettanto sicura con 4-5 parole, ma è molto più facile da ricordare e da digitare: perfetta per la password principale del gestore, del computer o della posta elettronica.</p>
<h2>Consigli pratici</h2>
<ul>
<li>Usa una password diversa per ogni servizio: se un sito viene violato, gli altri restano al sicuro.</li>
<li>Affidati a un gestore di password (quello del browser va già bene) invece di riusare la stessa ovunque.</li>
<li>Attiva la verifica in due passaggi dove possibile: è la protezione più efficace.</li>
<li>Non inviare password via email o chat e non salvarle in un file di testo.</li>
</ul>
<p>Le password vengono generate con il generatore crittografico del browser e non vengono mai trasmesse o salvate: quando chiudi la pagina spariscono.</p>
""",
        "en": """
<h2>What makes a password strong</h2>
<p>Two things: <strong>length</strong> and <strong>randomness</strong>. An 8-character password, even with symbols, can be guessed by a computer in hours; 16 random characters take centuries. Dictionary words, birth dates and "clever" substitutions like P@ssw0rd are the first things cracking programs try, so they add no real security.</p>
<p>The <strong>strength</strong> shown under the password is expressed in bits of entropy: every bit doubles the number of guesses needed. Above 60 bits you are safe from common attacks; above 80 from determined ones too.</p>
<h2>Random password or passphrase?</h2>
<p>A random password (e.g. <code>x7#Kq2!mVp9$Lw4R</code>) is ideal if a password manager remembers it for you. A <strong>passphrase</strong> (e.g. <code>Falcon-Lantern-Honey-Rocket-42</code>) is just as strong with 4-5 words but far easier to remember and type: perfect for the master password of your manager, your computer or your email.</p>
<h2>Practical tips</h2>
<ul>
<li>Use a different password for every service: if one site is breached, the others stay safe.</li>
<li>Rely on a password manager (the one built into your browser is fine) instead of reusing the same password everywhere.</li>
<li>Turn on two-step verification wherever possible: it is the most effective protection.</li>
<li>Never send passwords by email or chat, and don't keep them in a text file.</li>
</ul>
<p>Passwords are generated with the browser's cryptographic generator and are never transmitted or stored: when you close the page they are gone.</p>
""",
    },
    "faq": {
        "it": [
            ("Quanto deve essere lunga una password?", "Almeno 12 caratteri casuali; 16 o più per gli account importanti. Con una frase segreta, 4 parole bastano, 5 sono ottime."),
            ("Le password generate qui sono davvero casuali?", "Sì: usano crypto.getRandomValues, il generatore crittografico del browser, lo stesso usato dai gestori di password."),
            ("Posso fidarmi a generare una password su un sito?", "In questo caso sì, perché la generazione avviene solo nel tuo browser e nulla viene inviato a un server. Puoi verificarlo staccando la connessione: lo strumento continua a funzionare."),
        ],
        "en": [
            ("How long should a password be?", "At least 12 random characters; 16 or more for important accounts. With a passphrase, 4 words are enough and 5 are excellent."),
            ("Are the passwords generated here truly random?", "Yes: they use crypto.getRandomValues, the browser's cryptographic generator, the same one used by password managers."),
            ("Is it safe to generate a password on a website?", "Here it is, because generation happens only in your browser and nothing is sent to a server. You can check by going offline: the tool keeps working."),
        ],
    },
}

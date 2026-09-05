TOOL = {
    "id": "case_converter",
    "cat": "text",
    "icon": "Aa",
    "slug": {"it": "maiuscolo-minuscolo", "en": "case-converter"},
    "title": {"it": "Convertitore maiuscolo / minuscolo", "en": "Uppercase / lowercase converter"},
    "short": {"it": "Trasforma un testo in MAIUSCOLO, minuscolo, Iniziali Maiuscole o Frase", "en": "Turn text into UPPERCASE, lowercase, Title Case or Sentence case"},
    "keywords": {"it": ["tutto maiuscolo", "tutto minuscolo", "iniziali maiuscole", "cambia caso", "trasforma testo"], "en": ["capitalize", "title case", "sentence case", "change case", "all caps"]},
    "meta": {
        "it": "Converti un testo in maiuscolo, minuscolo, con le iniziali maiuscole o in stile frase con un clic. Funziona con lettere accentate, gratis e senza registrazione.",
        "en": "Convert text to uppercase, lowercase, Title Case or Sentence case in one click. Works with accented letters, free and with no sign-up.",
    },
    "intro": {
        "it": "Incolla il testo, scegli la trasformazione e copia il risultato. Gestisce correttamente accenti e apostrofi, e conserva a capo e spazi.",
        "en": "Paste your text, choose a transformation and copy the result. Handles accents and apostrophes correctly and keeps line breaks and spacing.",
    },
    "strings": {
        "it": {
            "ph": "Scrivi o incolla qui il testo…", "upper": "MAIUSCOLO", "lower": "minuscolo", "title": "Iniziali Maiuscole", "sentence": "Stile frase", "invert": "iNVERTI", "alt": "aLtErNaTo",
            "clear": "Svuota", "out": "Risultato", "chars": "caratteri", "trim": "Rimuovi spazi doppi",
        },
        "en": {
            "ph": "Type or paste your text here…", "upper": "UPPERCASE", "lower": "lowercase", "title": "Title Case", "sentence": "Sentence case", "invert": "iNVERT", "alt": "aLtErNaTiNg",
            "clear": "Clear", "out": "Result", "chars": "characters", "trim": "Remove double spaces",
        },
    },
    "ui": """
<div class="field"><textarea id="txt" placeholder="{{ph}}" rows="6" autofocus></textarea></div>
<div class="btns">
  <button class="btn primary" type="button" data-m="upper">{{upper}}</button>
  <button class="btn primary" type="button" data-m="lower">{{lower}}</button>
  <button class="btn primary" type="button" data-m="title">{{title}}</button>
  <button class="btn primary" type="button" data-m="sentence">{{sentence}}</button>
  <button class="btn" type="button" data-m="invert">{{invert}}</button>
  <button class="btn" type="button" data-m="alt">{{alt}}</button>
  <button class="btn" type="button" data-m="trim">{{trim}}</button>
  <button class="btn" type="button" id="clear">{{clear}}</button>
</div>
<div class="field out" style="margin-top:14px"><label for="res">{{out}}</label><textarea id="res" rows="6" readonly></textarea><button class="btn small copy" type="button" data-copy="#res" data-done="{{copied}}" style="top:32px">{{copy}}</button></div>
<p class="msg" id="info"></p>
""",
    "js": r"""
var txt = RT.$('#txt'), res = RT.$('#res'), info = RT.$('#info');
var lc = RT.lang === 'it' ? 'it-IT' : 'en-US';
function titleCase(s) { return s.toLocaleLowerCase(lc).replace(/(^|[\s\-("'«“])(\p{L})/gu, function (m, pre, ch) { return pre + ch.toLocaleUpperCase(lc); }); }
function sentenceCase(s) { return s.toLocaleLowerCase(lc).replace(/(^\s*|[.!?…]\s+|\n\s*)(\p{L})/gu, function (m, pre, ch) { return pre + ch.toLocaleUpperCase(lc); }).replace(/\bi\b/g, RT.lang === 'en' ? 'I' : 'i'); }
function invert(s) { return s.split('').map(function (c) { var u = c.toLocaleUpperCase(lc); return c === u ? c.toLocaleLowerCase(lc) : u; }).join(''); }
function alt(s) { var i = 0; return s.split('').map(function (c) { if (!/\p{L}/u.test(c)) return c; return (i++ % 2 === 0) ? c.toLocaleLowerCase(lc) : c.toLocaleUpperCase(lc); }).join(''); }
var ops = { upper: function (s) { return s.toLocaleUpperCase(lc); }, lower: function (s) { return s.toLocaleLowerCase(lc); }, title: titleCase, sentence: sentenceCase, invert: invert, alt: alt,
  trim: function (s) { return s.replace(/[ \t]{2,}/g, ' ').replace(/^[ \t]+|[ \t]+$/gm, '').replace(/\n{3,}/g, '\n\n'); } };
RT.$$('[data-m]').forEach(function (b) { b.addEventListener('click', function () { var v = txt.value; res.value = ops[b.getAttribute('data-m')](v); info.textContent = RT.fmt(res.value.length, 0) + ' ' + T.chars; }); });
RT.$('#clear').addEventListener('click', function () { txt.value = ''; res.value = ''; info.textContent = ''; txt.focus(); });
""",
    "article": {
        "it": """
<h2>Le trasformazioni disponibili</h2>
<ul>
<li><strong>MAIUSCOLO:</strong> tutte le lettere in maiuscolo, accenti compresi (è → È). Utile per titoli, targhe, codici e moduli che lo richiedono.</li>
<li><strong>minuscolo:</strong> tutte le lettere in minuscolo, per «spegnere» un testo scritto tutto in maiuscolo.</li>
<li><strong>Iniziali Maiuscole:</strong> la prima lettera di ogni parola in maiuscolo, come nei titoli in inglese o nei nomi propri (Mario Rossi, Via Giuseppe Verdi).</li>
<li><strong>Stile frase:</strong> maiuscola solo all'inizio di ogni frase, dopo punto, punto esclamativo o interrogativo, e a inizio riga. È lo stile corretto per i testi in italiano.</li>
<li><strong>iNVERTI e aLtErNaTo:</strong> scambiano o alternano maiuscole e minuscole; servono per correggere un testo scritto con il blocco maiuscole attivo o per effetti scherzosi.</li>
<li><strong>Rimuovi spazi doppi:</strong> elimina spazi ripetuti e spazi a inizio e fine riga, tipici dei testi copiati da PDF o email.</li>
</ul>
<h2>Quando serve</h2>
<p>Capita spesso di ricevere un elenco di nomi tutto in maiuscolo, un titolo scritto in minuscolo o un testo con il blocco maiuscole rimasto acceso. Riscriverlo a mano è noioso: con questo strumento lo sistemi in un secondo e lo copi con un clic. Ricorda che in italiano, a differenza dell'inglese, i titoli usano lo stile frase (solo la prima parola e i nomi propri in maiuscolo) e che i nomi di mesi e giorni vanno in minuscolo.</p>
""",
        "en": """
<h2>Available transformations</h2>
<ul>
<li><strong>UPPERCASE:</strong> every letter capitalised, accents included (é → É). Handy for headings, codes and forms that require it.</li>
<li><strong>lowercase:</strong> every letter in small case, to "calm down" a text typed in all caps.</li>
<li><strong>Title Case:</strong> the first letter of every word capitalised, as in headlines or proper names (John Smith, Baker Street).</li>
<li><strong>Sentence case:</strong> a capital only at the start of each sentence, after a full stop, exclamation or question mark, and at the start of a line. The pronoun "I" is capitalised too.</li>
<li><strong>iNVERT and aLtErNaTiNg:</strong> swap or alternate upper and lower case; useful to fix a text typed with Caps Lock on, or for playful effects.</li>
<li><strong>Remove double spaces:</strong> deletes repeated spaces and spaces at the start and end of lines, typical of text copied from PDFs or emails.</li>
</ul>
<h2>When you need it</h2>
<p>It happens all the time: a list of names arrives in all caps, a headline is typed in lowercase, or Caps Lock was left on. Retyping is tedious; with this tool you fix it in a second and copy the result with one click. Note that Title Case applies capitals to every word, including small words like "of" and "the": adjust those by hand if your style guide requires it.</p>
""",
    },
    "faq": {
        "it": [
            ("Le lettere accentate vengono convertite?", "Sì: è diventa È, à diventa À e così via, e anche il contrario. Lo strumento usa le regole della lingua italiana."),
            ("Il testo viene salvato da qualche parte?", "No. Tutto avviene nel tuo browser: il testo non viene inviato a nessun server."),
            ("Come scrivo i titoli in italiano?", "In italiano i titoli vanno in stile frase: maiuscola solo sulla prima parola e sui nomi propri. Le iniziali maiuscole su tutte le parole sono una convenzione inglese."),
        ],
        "en": [
            ("Are accented letters converted?", "Yes: é becomes É, ñ becomes Ñ and so on, and vice versa."),
            ("Is my text stored anywhere?", "No. Everything happens in your browser: the text is not sent to any server."),
            ("Does Title Case leave small words in lowercase?", "No, it capitalises every word. If your style guide keeps words like \"of\", \"and\" or \"the\" in lowercase, adjust them by hand after converting."),
        ],
    },
}

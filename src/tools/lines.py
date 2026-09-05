TOOL = {
    "id": "lines",
    "cat": "text",
    "icon": "🧹",
    "slug": {"it": "rimuovi-righe-duplicate", "en": "remove-duplicate-lines"},
    "title": {"it": "Rimuovi righe duplicate e ordina elenchi", "en": "Remove duplicate lines and sort lists"},
    "short": {"it": "Pulisci un elenco: via doppioni e righe vuote, ordine alfabetico", "en": "Clean up a list: drop duplicates and blank lines, sort alphabetically"},
    "keywords": {"it": ["ordina alfabeticamente", "elimina duplicati", "pulisci elenco", "righe vuote"], "en": ["sort alphabetically", "dedupe", "unique lines", "clean list"]},
    "meta": {
        "it": "Elimina le righe duplicate e vuote da un elenco, ordina in ordine alfabetico o numerico, togli gli spazi in eccesso. Tutto nel browser, gratis e senza registrazione.",
        "en": "Remove duplicate and blank lines from a list, sort alphabetically or numerically, trim extra spaces. All in your browser, free and with no sign-up.",
    },
    "intro": {
        "it": "Incolla un elenco (email, nomi, codici, indirizzi) e ottieni una versione pulita: senza doppioni, senza righe vuote e, se vuoi, in ordine alfabetico.",
        "en": "Paste a list (emails, names, codes, addresses) and get a clean version: no duplicates, no blank lines and, if you like, sorted alphabetically.",
    },
    "strings": {
        "it": {
            "ph": "Una voce per riga…", "dedupe": "Rimuovi righe duplicate", "nocase": "Ignora maiuscole/minuscole nel confronto", "empty": "Rimuovi righe vuote", "trim": "Togli spazi a inizio e fine riga",
            "sort": "Ordinamento", "none": "Nessuno (ordine originale)", "az": "A → Z", "za": "Z → A", "num": "Numerico crescente", "len": "Per lunghezza", "rev": "Inverti ordine", "shuffle": "Mescola",
            "out": "Risultato", "in_lines": "righe in ingresso", "out_lines": "righe in uscita", "removed": "rimosse", "clear": "Svuota", "prefix": "Aggiungi numerazione",
        },
        "en": {
            "ph": "One item per line…", "dedupe": "Remove duplicate lines", "nocase": "Ignore upper/lower case when comparing", "empty": "Remove blank lines", "trim": "Trim spaces at start and end of lines",
            "sort": "Sort", "none": "None (original order)", "az": "A → Z", "za": "Z → A", "num": "Numeric ascending", "len": "By length", "rev": "Reverse order", "shuffle": "Shuffle",
            "out": "Result", "in_lines": "input lines", "out_lines": "output lines", "removed": "removed", "clear": "Clear", "prefix": "Add numbering",
        },
    },
    "ui": """
<div class="field"><textarea id="txt" placeholder="{{ph}}" rows="8" autofocus></textarea></div>
<div class="row">
  <div>
    <label class="check"><input type="checkbox" id="dedupe" checked> {{dedupe}}</label>
    <label class="check"><input type="checkbox" id="nocase"> {{nocase}}</label>
    <label class="check"><input type="checkbox" id="empty" checked> {{empty}}</label>
    <label class="check"><input type="checkbox" id="trim" checked> {{trim}}</label>
    <label class="check"><input type="checkbox" id="prefix"> {{prefix}}</label>
  </div>
  <div class="field"><label for="sort">{{sort}}</label><select id="sort">
    <option value="none">{{none}}</option><option value="az">{{az}}</option><option value="za">{{za}}</option><option value="num">{{num}}</option><option value="len">{{len}}</option><option value="rev">{{rev}}</option><option value="shuffle">{{shuffle}}</option></select></div>
</div>
<div class="btns"><button class="btn small" type="button" id="clear">{{clear}}</button></div>
<div class="field out" style="margin-top:14px"><label for="res">{{out}}</label><textarea id="res" rows="8" readonly></textarea><button class="btn small copy" type="button" data-copy="#res" data-done="{{copied}}" style="top:32px">{{copy}}</button></div>
<p class="msg" id="info"></p>
""",
    "js": r"""
var txt = RT.$('#txt'), res = RT.$('#res'), info = RT.$('#info');
var coll = new Intl.Collator(RT.locale, { numeric: true, sensitivity: 'base' });
function run() {
  var lines = txt.value.split(/\r?\n/), inN = lines.length;
  if (RT.$('#trim').checked) lines = lines.map(function (l) { return l.trim(); });
  if (RT.$('#empty').checked) lines = lines.filter(function (l) { return l.trim() !== ''; });
  if (RT.$('#dedupe').checked) { var seen = {}, nc = RT.$('#nocase').checked; lines = lines.filter(function (l) { var k = nc ? l.toLowerCase() : l; if (seen[k]) return false; seen[k] = 1; return true; }); }
  var s = RT.$('#sort').value;
  if (s === 'az') lines.sort(coll.compare); else if (s === 'za') lines.sort(coll.compare).reverse();
  else if (s === 'num') lines.sort(function (a, b) { return (RT.num(a) || 0) - (RT.num(b) || 0); });
  else if (s === 'len') lines.sort(function (a, b) { return a.length - b.length || coll.compare(a, b); });
  else if (s === 'rev') lines.reverse();
  else if (s === 'shuffle') { for (var i = lines.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = lines[i]; lines[i] = lines[j]; lines[j] = t; } }
  if (RT.$('#prefix').checked) lines = lines.map(function (l, i) { return (i + 1) + '. ' + l; });
  res.value = lines.join('\n');
  if (!txt.value) { res.value = ''; info.textContent = ''; return; }
  info.textContent = RT.fmt(inN, 0) + ' ' + T.in_lines + ' → ' + RT.fmt(lines.length, 0) + ' ' + T.out_lines + ' (' + RT.fmt(Math.max(0, inN - lines.length), 0) + ' ' + T.removed + ')';
}
RT.$('#clear').addEventListener('click', function () { txt.value = ''; run(); txt.focus(); });
RT.live(document.getElementById('tool'), run);
""",
    "article": {
        "it": """
<h2>Cosa fa questo strumento</h2>
<p>Prende un testo con una voce per riga e lo ripulisce secondo le opzioni scelte:</p>
<ul>
<li><strong>Rimuovi righe duplicate:</strong> conserva solo la prima occorrenza di ogni riga. Con «Ignora maiuscole/minuscole», <em>Mario</em> e <em>mario</em> vengono considerati la stessa voce.</li>
<li><strong>Rimuovi righe vuote</strong> e <strong>togli spazi</strong> a inizio e fine riga: sistemano gli elenchi copiati da fogli di calcolo, email o PDF.</li>
<li><strong>Ordinamento:</strong> alfabetico (A→Z o Z→A, con accenti e numeri gestiti in modo naturale: «file2» viene prima di «file10»), numerico, per lunghezza, invertito o casuale.</li>
<li><strong>Numerazione:</strong> aggiunge «1. », «2. »… davanti a ogni riga.</li>
</ul>
<h2>Esempi d'uso</h2>
<ul>
<li>Unire due liste di email per una newsletter senza inviare doppioni.</li>
<li>Mettere in ordine alfabetico un elenco di nomi per un registro o un'assemblea.</li>
<li>Ripulire una lista di codici prodotto o di parole chiave esportata da un programma.</li>
<li>Estrarre un sorteggio: incolla i partecipanti e scegli «Mescola».</li>
</ul>
<p>Il confronto tra righe è esatto: se due voci differiscono per uno spazio interno o un accento, restano entrambe. Il testo non viene inviato a nessun server.</p>
""",
        "en": """
<h2>What this tool does</h2>
<p>It takes a text with one item per line and cleans it according to the options you choose:</p>
<ul>
<li><strong>Remove duplicate lines:</strong> keeps only the first occurrence of each line. With "Ignore upper/lower case", <em>Mario</em> and <em>mario</em> count as the same item.</li>
<li><strong>Remove blank lines</strong> and <strong>trim spaces</strong> at the start and end of lines: they fix lists copied from spreadsheets, emails or PDFs.</li>
<li><strong>Sort:</strong> alphabetical (A→Z or Z→A, with accents and numbers handled naturally: "file2" comes before "file10"), numeric, by length, reversed or random.</li>
<li><strong>Numbering:</strong> adds "1. ", "2. "… in front of each line.</li>
</ul>
<h2>Example uses</h2>
<ul>
<li>Merge two email lists for a newsletter without sending duplicates.</li>
<li>Alphabetise a list of names for a register or a meeting.</li>
<li>Clean up a list of product codes or keywords exported from a program.</li>
<li>Run a draw: paste the participants and choose "Shuffle".</li>
</ul>
<p>Line comparison is exact: if two items differ by an inner space or an accent, both are kept. The text is not sent to any server.</p>
""",
    },
    "faq": {
        "it": [
            ("Le righe duplicate vengono contate?", "Sì: sotto il risultato vedi quante righe c'erano in ingresso, quante restano e quante sono state rimosse."),
            ("L'ordine alfabetico gestisce gli accenti?", "Sì: usa le regole della lingua, quindi «è» e «e» vengono ordinate insieme e i numeri dentro le parole seguono l'ordine naturale."),
            ("Posso ordinare numeri con la virgola?", "Sì: scegli «Numerico crescente». Vengono accettati sia 1,5 sia 1.5."),
        ],
        "en": [
            ("Are duplicate lines counted?", "Yes: under the result you can see how many lines came in, how many remain and how many were removed."),
            ("Does alphabetical sorting handle accents?", "Yes: it uses language rules, so \"é\" and \"e\" sort together and numbers inside words follow natural order."),
            ("Can I sort decimal numbers?", "Yes: choose \"Numeric ascending\". Both 1.5 and 1,5 are accepted."),
        ],
    },
}

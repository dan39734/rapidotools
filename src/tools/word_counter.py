TOOL = {
    "id": "word_counter",
    "cat": "text",
    "icon": "🔤",
    "slug": {"it": "conta-parole", "en": "word-counter"},
    "title": {"it": "Conta parole e caratteri", "en": "Word and character counter"},
    "short": {"it": "Parole, caratteri, frasi, paragrafi e tempo di lettura", "en": "Words, characters, sentences, paragraphs and reading time"},
    "keywords": {"it": ["contatore caratteri", "conta lettere", "numero di parole", "tempo di lettura", "battute"], "en": ["character counter", "letter count", "reading time", "word count"]},
    "meta": {
        "it": "Conta parole, caratteri (con e senza spazi), frasi e paragrafi di un testo in tempo reale, con tempo di lettura e di lettura ad alta voce. Gratis e senza registrazione.",
        "en": "Count words, characters (with and without spaces), sentences and paragraphs in real time, with reading and speaking time. Free, no sign-up.",
    },
    "intro": {
        "it": "Incolla o scrivi il testo: i conteggi si aggiornano mentre digiti. Perfetto per temi, tesi, post sui social, descrizioni e limiti di battute.",
        "en": "Paste or type your text: the counts update as you type. Perfect for essays, theses, social posts, descriptions and character limits.",
    },
    "strings": {
        "it": {
            "ph": "Scrivi o incolla qui il testo…", "words": "Parole", "chars": "Caratteri", "nospace": "Caratteri senza spazi", "sentences": "Frasi", "paragraphs": "Paragrafi",
            "read": "Tempo di lettura", "speak": "Lettura ad alta voce", "min": "min", "sec": "s", "clear": "Svuota", "top": "Parole più frequenti", "avg": "Lunghezza media parola",
            "limits": "Limiti comuni", "limit_tweet": "Post X/Twitter (280)", "limit_ig": "Didascalia Instagram (2.200)", "limit_meta": "Meta description (155)", "limit_sms": "SMS (160)", "left": "rimanenti", "over": "oltre il limite",
        },
        "en": {
            "ph": "Type or paste your text here…", "words": "Words", "chars": "Characters", "nospace": "Characters without spaces", "sentences": "Sentences", "paragraphs": "Paragraphs",
            "read": "Reading time", "speak": "Speaking time", "min": "min", "sec": "s", "clear": "Clear", "top": "Most frequent words", "avg": "Average word length",
            "limits": "Common limits", "limit_tweet": "X/Twitter post (280)", "limit_ig": "Instagram caption (2,200)", "limit_meta": "Meta description (155)", "limit_sms": "SMS (160)", "left": "left", "over": "over the limit",
        },
    },
    "ui": """
<div class="field"><textarea id="txt" placeholder="{{ph}}" rows="8" autofocus></textarea></div>
<div class="btns"><button class="btn small" type="button" data-copy="#txt" data-done="{{copied}}">{{copy}}</button><button class="btn small" type="button" id="clear">{{clear}}</button></div>
<div class="stats">
  <div class="stat"><b id="w">0</b><span>{{words}}</span></div>
  <div class="stat"><b id="c">0</b><span>{{chars}}</span></div>
  <div class="stat"><b id="cn">0</b><span>{{nospace}}</span></div>
  <div class="stat"><b id="s">0</b><span>{{sentences}}</span></div>
  <div class="stat"><b id="p">0</b><span>{{paragraphs}}</span></div>
  <div class="stat"><b id="avg">0</b><span>{{avg}}</span></div>
  <div class="stat"><b id="rt">0 {{sec}}</b><span>{{read}}</span></div>
  <div class="stat"><b id="st">0 {{sec}}</b><span>{{speak}}</span></div>
</div>
<div class="result" style="margin-top:14px">
  <div class="lbl">{{limits}}</div>
  <div class="table-wrap"><table id="limits"><tbody>
    <tr><td>{{limit_tweet}}</td><td data-lim="280"></td></tr>
    <tr><td>{{limit_sms}}</td><td data-lim="160"></td></tr>
    <tr><td>{{limit_meta}}</td><td data-lim="155"></td></tr>
    <tr><td>{{limit_ig}}</td><td data-lim="2200"></td></tr>
  </tbody></table></div>
  <div class="lbl" style="margin-top:12px">{{top}}</div>
  <p id="top" class="msg">–</p>
</div>
""",
    "js": r"""
var txt = RT.$('#txt');
var stop = RT.lang === 'it' ? 'di,a,da,in,con,su,per,tra,fra,il,lo,la,i,gli,le,un,uno,una,e,o,ma,che,non,si,del,della,dei,delle,al,alla,ai,alle,dal,dalla,nel,nella,è,sono,ho,hai,ha,come,più,anche,se,ci,mi,ti,questo,questa' : 'the,a,an,and,or,but,of,to,in,on,at,for,with,by,from,is,are,was,were,be,it,this,that,as,i,you,he,she,we,they,not,have,has,do,does,my,your,its';
stop = stop.split(',');
function fmtTime(sec) { if (sec < 60) return Math.round(sec) + ' ' + T.sec; var m = Math.floor(sec / 60), s = Math.round(sec % 60); return m + ' ' + T.min + (s ? ' ' + s + ' ' + T.sec : ''); }
function calc() {
  var v = txt.value;
  var words = v.trim() ? v.trim().split(/\s+/) : [];
  var chars = v.length, nospace = v.replace(/\s/g, '').length;
  var sentences = v.trim() ? (v.match(/[^.!?…]+[.!?…]+(\s|$)|[^.!?…]+$/g) || []).length : 0;
  var paragraphs = v.trim() ? v.split(/\n\s*\n/).filter(function (p) { return p.trim(); }).length : 0;
  var letters = words.join('').replace(/[^\p{L}\p{N}]/gu, '').length;
  RT.$('#w').textContent = RT.fmt(words.length, 0); RT.$('#c').textContent = RT.fmt(chars, 0); RT.$('#cn').textContent = RT.fmt(nospace, 0);
  RT.$('#s').textContent = RT.fmt(sentences, 0); RT.$('#p').textContent = RT.fmt(paragraphs, 0);
  RT.$('#avg').textContent = words.length ? RT.fmt(letters / words.length, 1) : '0';
  RT.$('#rt').textContent = fmtTime(words.length / 200 * 60); RT.$('#st').textContent = fmtTime(words.length / 130 * 60);
  RT.$$('#limits [data-lim]').forEach(function (td) { var lim = +td.getAttribute('data-lim'), left = lim - chars; td.innerHTML = left >= 0 ? RT.fmt(left, 0) + ' ' + T.left : '<span style="color:var(--bad)">' + RT.fmt(-left, 0) + ' ' + T.over + '</span>'; });
  var freq = {};
  words.forEach(function (w) { w = w.toLowerCase().replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, ''); if (w.length > 2 && stop.indexOf(w) < 0) freq[w] = (freq[w] || 0) + 1; });
  var top = Object.keys(freq).sort(function (a, b) { return freq[b] - freq[a]; }).slice(0, 8);
  RT.$('#top').textContent = top.length ? top.map(function (w) { return w + ' (' + freq[w] + ')'; }).join(' · ') : '–';
}
RT.$('#clear').addEventListener('click', function () { txt.value = ''; calc(); txt.focus(); });
txt.addEventListener('input', calc); calc();
""",
    "article": {
        "it": """
<h2>Cosa conta questo strumento</h2>
<ul>
<li><strong>Parole:</strong> le sequenze di caratteri separate da spazi o a capo. «L'acqua» conta come una parola, come nella maggior parte dei programmi di scrittura.</li>
<li><strong>Caratteri:</strong> tutti i segni, spazi compresi. È il numero che conta per i limiti dei social e dei moduli online. Nell'editoria si parla di «battute»: sono i caratteri spazi inclusi.</li>
<li><strong>Caratteri senza spazi:</strong> utile per tariffe di traduzione e per alcune norme redazionali.</li>
<li><strong>Frasi e paragrafi:</strong> le frasi terminano con punto, punto esclamativo o interrogativo; i paragrafi sono separati da una riga vuota.</li>
<li><strong>Tempo di lettura:</strong> stimato a 200 parole al minuto (lettura silenziosa) e 130 parole al minuto (ad alta voce, come in un discorso o un video).</li>
</ul>
<h2>Limiti da tenere a mente</h2>
<p>Un post su X/Twitter può avere al massimo 280 caratteri, un SMS classico 160, una didascalia di Instagram 2.200. La «meta description» di una pagina web viene di solito troncata da Google intorno ai 155 caratteri. Una cartella editoriale corrisponde a 1.800 battute; un tema di maturità tipico è tra le 600 e le 1.000 parole.</p>
<h2>Parole più frequenti</h2>
<p>La lista delle parole più usate (escluse quelle grammaticali come articoli e preposizioni) aiuta a scovare ripetizioni e a controllare che le parole chiave di un testo per il web compaiano davvero.</p>
<p>Il testo non lascia mai il tuo dispositivo: il conteggio avviene nel browser.</p>
""",
        "en": """
<h2>What this tool counts</h2>
<ul>
<li><strong>Words:</strong> sequences of characters separated by spaces or line breaks. "Don't" counts as one word, as in most word processors.</li>
<li><strong>Characters:</strong> every symbol, spaces included. This is the number that matters for social media and online form limits.</li>
<li><strong>Characters without spaces:</strong> useful for translation rates and some editorial guidelines.</li>
<li><strong>Sentences and paragraphs:</strong> sentences end with a full stop, exclamation or question mark; paragraphs are separated by a blank line.</li>
<li><strong>Reading time:</strong> estimated at 200 words per minute (silent reading) and 130 words per minute (out loud, as in a speech or a video).</li>
</ul>
<h2>Limits worth remembering</h2>
<p>A post on X/Twitter can have at most 280 characters, a classic SMS 160, an Instagram caption 2,200. A web page's "meta description" is usually truncated by Google at around 155 characters. A typical college essay is between 500 and 1,000 words; a standard manuscript page is about 250 words.</p>
<h2>Most frequent words</h2>
<p>The list of the most used words (excluding grammatical ones such as articles and prepositions) helps you spot repetition and check that the keywords of a web text actually appear.</p>
<p>Your text never leaves your device: the counting happens in the browser.</p>
""",
    },
    "faq": {
        "it": [
            ("Cosa sono le battute?", "Le battute sono i caratteri di un testo, spazi inclusi. Una cartella editoriale standard è di 1.800 battute (30 righe da 60 battute)."),
            ("Come viene calcolato il tempo di lettura?", "Dividendo il numero di parole per 200, la velocità media di un lettore adulto. Per la lettura ad alta voce si usano 130 parole al minuto."),
            ("Il conteggio corrisponde a quello di Word?", "Nella grande maggioranza dei casi sì: entrambi contano come parola ogni gruppo di caratteri separato da spazi. Piccole differenze possono nascere da simboli o numeri isolati."),
        ],
        "en": [
            ("How is reading time calculated?", "By dividing the number of words by 200, the average speed of an adult reader. Speaking time uses 130 words per minute."),
            ("Does the count match Microsoft Word?", "In the vast majority of cases yes: both count every group of characters separated by spaces as a word. Small differences can arise from isolated symbols or numbers."),
            ("Do characters include spaces?", "The \"Characters\" figure includes spaces; \"Characters without spaces\" excludes them. Social media limits count spaces."),
        ],
    },
}

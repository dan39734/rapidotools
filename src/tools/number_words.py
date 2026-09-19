TOOL = {
    "id": "number_words",
    "cat": "numbers",
    "icon": "🔤",
    "slug": {"it": "numeri-in-lettere", "en": "numbers-to-words"},
    "title": {"it": "Numeri in lettere", "en": "Numbers to words"},
    "seo_title": {"it": "Numeri in lettere: come si scrive un numero o un importo", "en": "Numbers to words: how to spell out a number or an amount"},
    "short": {"it": "Scrivi un numero o un importo in lettere, in italiano e in inglese", "en": "Spell out a number or an amount in words, in English and Italian"},
    "keywords": {"it": ["numeri in lettere", "come si scrive", "come si scrivono i numeri in lettere", "cifre in lettere", "importo in lettere", "milioni in lettere", "assegno", "convertitore numeri lettere", "numeri in inglese"], "en": ["number to words", "spell number", "amount in words", "cheque", "check writing", "numbers in italian"]},
    "meta": {
        "it": "Come si scrive un numero in lettere? Scrivi la cifra e ottieni subito la forma corretta: numeri, importi in euro, milioni e miliardi, formato per assegni, in italiano e in inglese.",
        "en": "Number to words converter: spells out any number or amount in words, in English and Italian, including the cheque format. With a table of the numbers from 1 to 100.",
    },
    "intro": {
        "it": "Scrivi la cifra e ottieni subito come si scrive in lettere: come numero, come importo in euro o nel formato per l'assegno, in italiano o in inglese. Funziona anche con i milioni e i miliardi.",
        "en": "Type a number (decimals too) and get it spelled out: as a number, as an amount of money or in cheque format. Choose English or Italian.",
    },
    "strings": {
        "it": {
            "number": "Numero", "lang": "Lingua", "it": "Italiano", "en": "Inglese", "mode": "Formato", "m_num": "Numero", "m_eur": "Importo in euro", "m_chk": "Assegno (euro/centesimi)",
            "m_usd": "Importo in dollari", "m_gbp": "Importo in sterline", "case": "Maiuscole", "c_low": "minuscolo", "c_cap": "Iniziale maiuscola", "c_up": "TUTTO MAIUSCOLO",
            "style": "Stile inglese", "s_us": "Americano (senza and)", "s_uk": "Britannico (con and)",
            "too_big": "Numero troppo grande: il massimo è 999.999.999.999,99.", "nan": "Scrivi un numero, per esempio 1234,56.",
            "table": "Numeri da 1 a 100 in lettere", "show": "Mostra la tabella", "hide": "Nascondi la tabella", "big": "Grandi numeri",
        },
        "en": {
            "number": "Number", "lang": "Language", "it": "Italian", "en": "English", "mode": "Format", "m_num": "Number", "m_eur": "Amount in euros", "m_chk": "Cheque (euros/cents)",
            "m_usd": "Amount in dollars", "m_gbp": "Amount in pounds", "case": "Capitalisation", "c_low": "lowercase", "c_cap": "Capitalised", "c_up": "ALL CAPS",
            "style": "English style", "s_us": "American (no and)", "s_uk": "British (with and)",
            "too_big": "Number too large: the maximum is 999,999,999,999.99.", "nan": "Type a number, for example 1234.56.",
            "table": "Numbers from 1 to 100 in words", "show": "Show the table", "hide": "Hide the table", "big": "Large numbers",
        },
    },
    "ui": """
<div class="row">
  <div class="field" style="flex:2 1 220px"><label for="num">{{number}}</label><input type="text" id="num" inputmode="decimal" value="1234,56" autocomplete="off"></div>
  <div class="field"><label for="lang">{{lang}}</label><select id="lang"><option value="it">{{it}}</option><option value="en">{{en}}</option></select></div>
  <div class="field"><label for="mode">{{mode}}</label><select id="mode"><option value="num">{{m_num}}</option><option value="eur">{{m_eur}}</option><option value="chk">{{m_chk}}</option><option value="usd">{{m_usd}}</option><option value="gbp">{{m_gbp}}</option></select></div>
</div>
<div class="row">
  <div class="field"><label for="case">{{case}}</label><select id="case"><option value="low">{{c_low}}</option><option value="cap">{{c_cap}}</option><option value="up">{{c_up}}</option></select></div>
  <div class="field hide" id="stylef"><label for="style">{{style}}</label><select id="style"><option value="us">{{s_us}}</option><option value="uk">{{s_uk}}</option></select></div>
</div>
<p class="msg bad hide" id="err"></p>
<div class="result" id="out">
  <div class="big" id="main" style="font-size:1.45rem;overflow-wrap:anywhere"></div>
  <div class="sub" id="sub"></div>
  <p class="btns"><button class="btn small" type="button" data-copy="#main" data-done="{{copied}}">{{copy}}</button></p>
</div>
<h2 style="font-size:1.1rem;margin-top:22px">{{table}}</h2>
<div class="table-wrap" id="tbl"></div>
""",
    "js": r"""
var num = RT.$('#num'), lang = RT.$('#lang'), mode = RT.$('#mode'), cas = RT.$('#case'), style = RT.$('#style'), stylef = RT.$('#stylef');
var main = RT.$('#main'), sub = RT.$('#sub'), err = RT.$('#err');
lang.value = RT.lang === 'it' ? 'it' : 'en';
// ---------- Italian ----------
var IT_U = ['', 'uno', 'due', 'tre', 'quattro', 'cinque', 'sei', 'sette', 'otto', 'nove', 'dieci', 'undici', 'dodici', 'tredici', 'quattordici', 'quindici', 'sedici', 'diciassette', 'diciotto', 'diciannove'];
var IT_T = ['', '', 'venti', 'trenta', 'quaranta', 'cinquanta', 'sessanta', 'settanta', 'ottanta', 'novanta'];
function itAccent(w) { return (w.length > 3 && /tre$/.test(w)) ? w.slice(0, -3) + 'tré' : w; }
function it100(n) {
  if (n < 20) return IT_U[n];
  var t = IT_T[Math.floor(n / 10)], u = n % 10;
  if (u === 1 || u === 8) t = t.slice(0, -1);
  return t + IT_U[u];
}
function it1000(n) {
  var h = Math.floor(n / 100), r = n % 100, s = '';
  if (h) s = (h === 1 ? 'cento' : IT_U[h] + 'cento');
  if (r) { var w = it100(r); if (h && w.charAt(0) === 'o') s = s.slice(0, -1); s += w; }
  return s;
}
function itWords(n) { // 0 .. 999 999 999 999
  if (n === 0) return 'zero';
  var parts = [];
  var bil = Math.floor(n / 1e9), mil = Math.floor(n % 1e9 / 1e6), rest = n % 1e6;
  if (bil) parts.push(bil === 1 ? 'un miliardo' : itAccent(it1000(bil)) + ' miliardi');
  if (mil) parts.push(mil === 1 ? 'un milione' : itAccent(it1000(mil)) + ' milioni');
  if (rest) {
    var k = Math.floor(rest / 1000), r = rest % 1000, s = '';
    if (k) s = k === 1 ? 'mille' : it1000(k) + 'mila';
    s += it1000(r);
    parts.push(itAccent(s));
  }
  return parts.join(' ');
}
// ---------- English ----------
var EN_U = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'];
var EN_T = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
function en100(n) { if (n < 20) return EN_U[n]; var u = n % 10; return EN_T[Math.floor(n / 10)] + (u ? '-' + EN_U[u] : ''); }
function en1000(n, uk) {
  var h = Math.floor(n / 100), r = n % 100, s = '';
  if (h) s = EN_U[h] + ' hundred';
  if (r) s += (h ? (uk ? ' and ' : ' ') : '') + en100(r);
  return s;
}
function enWords(n, uk) {
  if (n === 0) return 'zero';
  var parts = [], names = ['', ' thousand', ' million', ' billion'], i = 0, lastSmall = false;
  var groups = [];
  while (n > 0) { groups.push(n % 1000); n = Math.floor(n / 1000); }
  for (i = groups.length - 1; i >= 0; i--) {
    if (!groups[i]) continue;
    parts.push(en1000(groups[i], uk) + names[i]);
  }
  var s = parts.join(' ');
  // British: "one thousand and forty-two" (and before a final group < 100)
  if (uk && groups.length > 1 && groups[0] && groups[0] < 100) s = s.replace(/ (\S+)$/, ' and $1');
  return s;
}
function words(n, L, uk) { return L === 'it' ? itWords(n) : enWords(n, uk); }
function applyCase(s) { var c = cas.value; if (c === 'up') return s.toUpperCase(); if (c === 'cap') return s.charAt(0).toUpperCase() + s.slice(1); return s; }
function render() {
  var L = lang.value, uk = style.value === 'uk', m = mode.value;
  stylef.classList.toggle('hide', L !== 'en');
  var raw = num.value.trim(), v = RT.num(raw);
  if (!isFinite(v)) { err.textContent = T.nan; err.classList.remove('hide'); main.textContent = ''; sub.textContent = ''; return; }
  var neg = v < 0; v = Math.abs(v);
  var ip = Math.floor(v + 1e-9), cents = Math.round((v - ip) * 100);
  if (cents === 100) { ip += 1; cents = 0; }
  if (ip > 999999999999) { err.textContent = T.too_big; err.classList.remove('hide'); main.textContent = ''; sub.textContent = ''; return; }
  err.classList.add('hide');
  var s = '', subtxt = '';
  var minus = L === 'it' ? 'meno ' : 'minus ';
  if (m === 'num') {
    // decimals: keep what the user typed (up to 6 digits)
    var dec = '';
    var mm = raw.replace(/\s/g, '').match(/[.,](\d{1,6})$/);
    if (mm) dec = mm[1];
    s = words(ip, L, uk);
    if (dec && /[1-9]/.test(dec)) {
      if (L === 'it') s += ' virgola ' + (dec.charAt(0) === '0' ? dec.split('').map(function (d) { return d === '0' ? 'zero' : IT_U[+d]; }).join(' ') : itWords(+dec));
      else s += ' point ' + dec.split('').map(function (d) { return d === '0' ? 'zero' : EN_U[+d]; }).join(' ');
    }
    subtxt = RT.fmt(v, 6);
  } else if (m === 'chk') {
    s = (L === 'it' ? itWords(ip) : enWords(ip, uk)) + (L === 'it' ? '/' + RT.pad(cents) : ' and ' + RT.pad(cents) + '/100');
    subtxt = RT.money(v, 'EUR');
  } else {
    var cur = { eur: ['euro', 'euro', 'centesimo', 'centesimi', 'euro', 'euros', 'cent', 'cents', 'EUR'], usd: ['dollaro', 'dollari', 'centesimo', 'centesimi', 'dollar', 'dollars', 'cent', 'cents', 'USD'], gbp: ['sterlina', 'sterline', 'penny', 'pence', 'pound', 'pounds', 'penny', 'pence', 'GBP'] }[m];
    if (L === 'it') {
      var iw = ip === 1 ? 'un' : itWords(ip); if (/(milione|milioni|miliardo|miliardi)$/.test(iw)) iw += ' di';
      s = iw + ' ' + (ip === 1 ? cur[0] : cur[1]);
      if (cents) s += ' e ' + (cents === 1 ? 'un' : itWords(cents)) + ' ' + (cents === 1 ? cur[2] : cur[3]);
    } else {
      s = enWords(ip, uk) + ' ' + (ip === 1 ? cur[4] : cur[5]);
      if (cents) s += ' and ' + enWords(cents, uk) + ' ' + (cents === 1 ? cur[6] : cur[7]);
    }
    subtxt = RT.money(v, cur[8]);
  }
  if (neg) s = minus + s;
  main.textContent = applyCase(s);
  sub.textContent = subtxt;
}
function table() {
  var L = lang.value, uk = style.value === 'uk', rows = '';
  for (var i = 1; i <= 100; i++) rows += '<tr><td class="mono">' + i + '</td><td>' + words(i, L, uk) + '</td></tr>';
  var bigs = [200, 300, 1000, 2000, 10000, 100000, 1000000, 1000000000];
  var rows2 = bigs.map(function (b) { return '<tr><td class="mono">' + RT.fmt(b, 0) + '</td><td>' + words(b, L, uk) + '</td></tr>'; }).join('');
  RT.$('#tbl').innerHTML = '<div class="row" style="align-items:flex-start"><table style="flex:1 1 220px"><tbody>' + rows.split('</tr>').slice(0, 50).join('</tr>') + '</tr></tbody></table>' +
    '<table style="flex:1 1 220px"><tbody>' + rows.split('</tr>').slice(50, 100).join('</tr>') + '</tr></tbody></table></div>' +
    '<h3>' + T.big + '</h3><table><tbody>' + rows2 + '</tbody></table>';
}
RT.live(document.getElementById('tool'), render);
lang.addEventListener('change', table); style.addEventListener('change', table);
table();
""",
    "article": {
        "it": """
<h2>Quando servono i numeri in lettere</h2>
<p>La forma in lettere si usa dove un numero non deve poter essere alterato o frainteso: sugli <strong>assegni</strong> («milleduecentotrentaquattro/56»), nei contratti e negli atti notarili («euro millecento/00»), nelle ricevute, nelle fatture di alcuni paesi e nei documenti ufficiali. Il convertitore scrive il numero seguendo le regole dell'ortografia italiana, oppure quelle inglesi se scegli «Inglese», e ti lascia copiare il risultato con un clic.</p>
<h2>Come si scrive un importo in milioni di euro</h2>
<p>È la domanda più frequente, perché i milioni si comportano diversamente dalle migliaia: fino a 999.999 il numero si scrive tutto attaccato, da un milione in su <em>milioni</em> e <em>miliardi</em> restano parole a sé, e davanti alla valuta vuole il <em>di</em>. Qualche esempio scritto come lo produce il convertitore:</p>
<ul>
<li><strong>223.000.000 €</strong> → <em>duecentoventitré milioni di euro</em></li>
<li><strong>1.500.000 €</strong> → <em>un milione cinquecentomila euro</em> (niente <em>di</em>: il numero non finisce con «milioni»)</li>
<li><strong>2.350.000,50 €</strong> → <em>due milioni trecentocinquantamila euro e cinquanta centesimi</em></li>
<li><strong>1.000.000.000 €</strong> → <em>un miliardo di euro</em></li>
</ul>
<p>La regola pratica: se l'ultima parola del numero è <em>milione</em>, <em>milioni</em>, <em>miliardo</em> o <em>miliardi</em>, si scrive «di euro»; se dopo i milioni c'è altro (<em>…cinquecentomila</em>), il <em>di</em> sparisce.</p>
<h2>Le regole dell'italiano</h2>
<ul>
<li>I numeri si scrivono <strong>tutti attaccati</strong> fino alle migliaia: <em>duemilatrecentoquarantacinque</em>. Milioni e miliardi sono parole separate: <em>due milioni trecentomila</em>.</li>
<li>Le decine perdono la vocale finale davanti a <em>uno</em> e <em>otto</em>: <em>ventuno</em>, <em>ventotto</em>, <em>trentuno</em>; <em>cento</em> la perde davanti a <em>otto</em> e <em>ottanta</em>: <em>centotto</em>, <em>centottanta</em>.</li>
<li><em>Tre</em> in fine di parola composta prende l'accento: <em>ventitré</em>, <em>centotré</em>, <em>duemilatré</em>.</li>
<li><em>Mille</em> al plurale diventa <em>-mila</em>: <em>mille</em>, <em>duemila</em>, <em>centomila</em>. <em>Un milione</em>, <em>due milioni</em>; <em>un miliardo</em>, <em>due miliardi</em>.</li>
<li>Gli importi: <em>euro</em> è invariabile (<em>due euro</em>), i centesimi si scrivono <em>e cinquantasei centesimi</em>; sull'assegno si usa la barra: <em>/56</em>, oppure <em>/00</em> se non ci sono centesimi.</li>
</ul>
<h2>Le regole dell'inglese</h2>
<p>In inglese le parole restano separate e le decine composte prendono il trattino: <em>one thousand two hundred thirty-four</em>. Lo stile britannico aggiunge <em>and</em> dopo le centinaia (<em>two hundred and five</em>) e prima di un gruppo finale sotto cento (<em>one thousand and forty-two</em>); quello americano lo omette. Sugli assegni americani i centesimi si scrivono come frazione: <em>and 56/100</em>. I decimali si leggono cifra per cifra: <em>twelve point five six</em>.</p>
""",
        "en": """
<h2>When you need numbers in words</h2>
<p>The spelled-out form is used wherever a number must not be altered or misread: on <strong>cheques</strong> ("one thousand two hundred thirty-four and 56/100"), in contracts and deeds, on receipts and in official documents. The converter spells the number according to English spelling rules – or Italian rules if you choose "Italian" – and lets you copy the result with one click.</p>
<h2>English rules</h2>
<ul>
<li>Words stay separate and compound tens take a hyphen: <em>one thousand two hundred thirty-four</em>.</li>
<li><strong>British style</strong> adds <em>and</em> after the hundreds (<em>two hundred and five</em>) and before a final group below one hundred (<em>one thousand and forty-two</em>); <strong>American style</strong> leaves it out.</li>
<li>Amounts: <em>one euro</em>, <em>two euros</em>, <em>… and fifty-six cents</em>; on US cheques cents are written as a fraction: <em>and 56/100</em>.</li>
<li>Decimals are read digit by digit: <em>twelve point five six</em>.</li>
</ul>
<h2>Italian rules</h2>
<p>Italian writes numbers as a single word up to the thousands (<em>duemilatrecentoquarantacinque</em>); millions and billions are separate words (<em>due milioni trecentomila</em>). Tens drop their final vowel before <em>uno</em> and <em>otto</em> (<em>ventuno</em>, <em>ventotto</em>), a final <em>tre</em> takes an accent (<em>ventitré</em>), and <em>mille</em> becomes <em>-mila</em> in the plural (<em>duemila</em>). On Italian cheques the cents follow a slash: <em>milleduecentotrentaquattro/56</em>.</p>
""",
    },
    "faq": {
        "it": [
            ("Come si scrive 223 milioni di euro?", "Si scrive «duecentoventitré milioni di euro»: <em>milioni</em> resta parola separata e davanti alla valuta va il «di». Lo stesso vale per qualsiasi altro importo tondo in milioni o miliardi."),
            ("Come si scrivono i numeri in lettere in italiano?", "Tutto attaccato fino alle migliaia (<em>duemilatrecentoquarantacinque</em>), con milioni e miliardi come parole separate. Le decine perdono la vocale davanti a <em>uno</em> e <em>otto</em> (<em>ventuno</em>, <em>ventotto</em>) e il <em>tre</em> finale prende l'accento (<em>ventitré</em>). Scrivi la cifra qui sopra e il convertitore applica da solo tutte le regole."),
            ("Come si scrive un importo sull'assegno?", "Scegli il formato «Assegno»: ottieni la parte intera in lettere seguita dai centesimi dopo la barra, per esempio «millecento/00». Scrivi tutto attaccato e senza spazi, come chiedono le banche."),
            ("Qual è il numero più grande che posso convertire?", "Fino a 999.999.999.999,99, cioè quasi mille miliardi, con due decimali per gli importi e fino a sei per i numeri."),
            ("Posso scrivere i numeri in inglese?", "Sì: scegli «Inglese» nel menu Lingua e, se serve, lo stile britannico con «and». La tabella da 1 a 100 cambia lingua di conseguenza."),
        ],
        "en": [
            ("How do you write millions in words?", "Millions and billions stay separate words: 223,000,000 is <em>two hundred twenty-three million</em>. Type the figure above and the converter applies the rules for you, in English or Italian."),
            ("How do I write an amount on a cheque?", "Choose the \"Cheque\" format: you get the whole part in words followed by the cents as a fraction, for example \"one thousand one hundred and 00/100\"."),
            ("What is the largest number I can convert?", "Up to 999,999,999,999.99 – almost a trillion – with two decimals for amounts and up to six for plain numbers."),
            ("Can I get the Italian spelling?", "Yes: choose \"Italian\" in the Language menu. The table from 1 to 100 switches language too."),
        ],
    },
}

TOOL = {
    "id": "qr",
    "cat": "images",
    "icon": "▦",
    "libs": ["qr.js"],
    "slug": {"it": "generatore-codice-qr", "en": "qr-code-generator"},
    "title": {"it": "Generatore di codici QR", "en": "QR code generator"},
    "short": {"it": "QR per link, testo, Wi-Fi, telefono ed email, da scaricare in PNG o SVG", "en": "QR codes for links, text, Wi-Fi, phone and email, downloadable as PNG or SVG"},
    "keywords": {"it": ["crea qr code", "qr code gratis", "qr wifi", "qr code menu", "codice qr link"], "en": ["create qr code", "free qr code", "wifi qr", "qr code for link", "qr code png"]},
    "meta": {
        "it": "Crea codici QR gratuiti e senza scadenza per link, testo, rete Wi-Fi, numero di telefono o email. Scegli dimensione e colori, scarica in PNG o SVG. Generati nel browser, senza registrazione.",
        "en": "Create free QR codes that never expire for links, text, Wi-Fi networks, phone numbers or emails. Choose size and colours, download as PNG or SVG. Generated in your browser, no sign-up.",
    },
    "intro": {
        "it": "Scrivi un link o un testo, oppure compila i campi per Wi-Fi, telefono ed email: il codice QR compare subito e puoi scaricarlo in PNG (per stampe e social) o SVG (per grafica e loghi). Nessun account, nessuna scadenza.",
        "en": "Type a link or a text, or fill in the fields for Wi-Fi, phone and email: the QR code appears instantly and you can download it as PNG (for print and social) or SVG (for graphics and logos). No account, no expiry.",
    },
    "strings": {
        "it": {
            "t_url": "Link / testo", "t_wifi": "Wi-Fi", "t_tel": "Telefono", "t_mail": "Email", "t_sms": "SMS",
            "content": "Link o testo", "ph_url": "https://esempio.it oppure un testo qualsiasi", "ssid": "Nome della rete (SSID)", "pass": "Password", "enc": "Sicurezza", "hidden": "Rete nascosta",
            "tel": "Numero di telefono", "email": "Indirizzo email", "subject": "Oggetto (facoltativo)", "body": "Messaggio (facoltativo)", "sms_text": "Testo del messaggio (facoltativo)",
            "size": "Dimensione (px)", "ecc": "Correzione errori", "e_l": "Bassa (7%)", "e_m": "Media (15%)", "e_q": "Alta (25%)", "e_h": "Massima (30%)", "dark": "Colore", "light": "Sfondo",
            "png": "Scarica PNG", "svg": "Scarica SVG", "copy_img": "Copia immagine", "empty": "Inserisci un contenuto per generare il codice.", "too_long": "Testo troppo lungo per un codice QR (massimo circa 2.900 caratteri).", "info": "Versione {v} · {n}×{n} moduli · correzione {e}", "nopass": "Nessuna (rete aperta)",
        },
        "en": {
            "t_url": "Link / text", "t_wifi": "Wi-Fi", "t_tel": "Phone", "t_mail": "Email", "t_sms": "SMS",
            "content": "Link or text", "ph_url": "https://example.com or any text", "ssid": "Network name (SSID)", "pass": "Password", "enc": "Security", "hidden": "Hidden network",
            "tel": "Phone number", "email": "Email address", "subject": "Subject (optional)", "body": "Message (optional)", "sms_text": "Message text (optional)",
            "size": "Size (px)", "ecc": "Error correction", "e_l": "Low (7%)", "e_m": "Medium (15%)", "e_q": "Quartile (25%)", "e_h": "High (30%)", "dark": "Colour", "light": "Background",
            "png": "Download PNG", "svg": "Download SVG", "copy_img": "Copy image", "empty": "Enter some content to generate the code.", "too_long": "Text too long for a QR code (about 2,900 characters maximum).", "info": "Version {v} · {n}×{n} modules · error correction {e}", "nopass": "None (open network)",
        },
    },
    "ui": """
<div class="tabs">
  <button type="button" class="on" data-tab="url">{{t_url}}</button><button type="button" data-tab="wifi">{{t_wifi}}</button>
  <button type="button" data-tab="tel">{{t_tel}}</button><button type="button" data-tab="mail">{{t_mail}}</button><button type="button" data-tab="sms">{{t_sms}}</button>
</div>
<div id="tab-url"><div class="field"><label for="url">{{content}}</label><textarea id="url" rows="3" placeholder="{{ph_url}}">https://rapidotools.com</textarea></div></div>
<div id="tab-wifi" class="hide">
  <div class="row"><div class="field"><label for="ssid">{{ssid}}</label><input type="text" id="ssid"></div><div class="field"><label for="wpass">{{pass}}</label><input type="text" id="wpass"></div></div>
  <div class="row"><div class="field"><label for="enc">{{enc}}</label><select id="enc"><option value="WPA">WPA / WPA2 / WPA3</option><option value="WEP">WEP</option><option value="nopass">{{nopass}}</option></select></div>
  <label class="check"><input type="checkbox" id="whidden"> {{hidden}}</label></div>
</div>
<div id="tab-tel" class="hide"><div class="field"><label for="tel">{{tel}}</label><input type="tel" id="tel" placeholder="+39 333 1234567"></div></div>
<div id="tab-mail" class="hide">
  <div class="field"><label for="mail">{{email}}</label><input type="email" id="mail"></div>
  <div class="row"><div class="field"><label for="subj">{{subject}}</label><input type="text" id="subj"></div><div class="field"><label for="body">{{body}}</label><input type="text" id="body"></div></div>
</div>
<div id="tab-sms" class="hide">
  <div class="row"><div class="field"><label for="smsn">{{tel}}</label><input type="tel" id="smsn"></div><div class="field"><label for="smst">{{sms_text}}</label><input type="text" id="smst"></div></div>
</div>
<div class="row">
  <div class="field"><label for="size">{{size}}</label><select id="size"><option>256</option><option>512</option><option selected>1024</option><option>2048</option></select></div>
  <div class="field"><label for="ecc">{{ecc}}</label><select id="ecc"><option value="L">{{e_l}}</option><option value="M" selected>{{e_m}}</option><option value="Q">{{e_q}}</option><option value="H">{{e_h}}</option></select></div>
  <div class="field"><label for="dark">{{dark}}</label><input type="color" id="dark" value="#000000" style="height:42px"></div>
  <div class="field"><label for="light">{{light}}</label><input type="color" id="light" value="#ffffff" style="height:42px"></div>
</div>
<p class="msg bad hide" id="err"></p>
<div class="qr"><canvas id="cv" style="max-width:280px;width:100%;image-rendering:pixelated"></canvas></div>
<p class="msg" id="info" style="text-align:center"></p>
<div class="btns" style="justify-content:center"><button class="btn primary" type="button" id="png">⬇ {{png}}</button><button class="btn" type="button" id="svg">⬇ {{svg}}</button></div>
""",
    "js": r"""
var tab = 'url', tabs = RT.$$('.tabs button'), cv = RT.$('#cv'), err = RT.$('#err'), info = RT.$('#info'), current = null;
tabs.forEach(function (b) { b.addEventListener('click', function () { tab = b.getAttribute('data-tab'); tabs.forEach(function (x) { x.classList.toggle('on', x === b); }); ['url', 'wifi', 'tel', 'mail', 'sms'].forEach(function (k) { RT.$('#tab-' + k).classList.toggle('hide', k !== tab); }); render(); }); });
function escWifi(s) { return s.replace(/([\\;,:"])/g, '\\$1'); }
function payload() {
  if (tab === 'url') return RT.$('#url').value.trim();
  if (tab === 'wifi') { var ssid = RT.$('#ssid').value.trim(); if (!ssid) return ''; var enc = RT.$('#enc').value; return 'WIFI:T:' + enc + ';S:' + escWifi(ssid) + ';' + (enc !== 'nopass' ? 'P:' + escWifi(RT.$('#wpass').value) + ';' : '') + (RT.$('#whidden').checked ? 'H:true;' : '') + ';'; }
  if (tab === 'tel') { var t = RT.$('#tel').value.replace(/[\s().-]/g, ''); return t ? 'tel:' + t : ''; }
  if (tab === 'mail') { var m = RT.$('#mail').value.trim(); if (!m) return ''; var q = []; if (RT.$('#subj').value) q.push('subject=' + encodeURIComponent(RT.$('#subj').value)); if (RT.$('#body').value) q.push('body=' + encodeURIComponent(RT.$('#body').value)); return 'mailto:' + m + (q.length ? '?' + q.join('&') : ''); }
  if (tab === 'sms') { var n = RT.$('#smsn').value.replace(/[\s().-]/g, ''); if (!n) return ''; return 'SMSTO:' + n + ':' + RT.$('#smst').value; }
  return '';
}
function render() {
  var text = payload(); err.classList.add('hide'); current = null;
  if (!text) { err.textContent = T.empty; err.classList.remove('hide'); cv.getContext('2d').clearRect(0, 0, cv.width, cv.height); info.textContent = ''; return; }
  var qr = RTQR.encode(text, RT.$('#ecc').value, true);
  if (!qr) { err.textContent = T.too_long; err.classList.remove('hide'); info.textContent = ''; return; }
  current = qr;
  var size = +RT.$('#size').value, scale = Math.max(1, Math.floor(size / (qr.size + 8)));
  RTQR.draw(qr, cv, scale, 4, RT.$('#dark').value, RT.$('#light').value);
  info.textContent = T.info.replace('{v}', qr.version).replace(/\{n\}/g, qr.size).replace('{e}', qr.ecl);
}
function svgString() {
  var q = current, b = 4, n = q.size + b * 2, d = '';
  for (var y = 0; y < q.size; y++) for (var x = 0; x < q.size; x++) if (q.modules[y][x]) d += 'M' + (x + b) + ' ' + (y + b) + 'h1v1h-1z';
  return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + n + ' ' + n + '" shape-rendering="crispEdges"><rect width="100%" height="100%" fill="' + RT.$('#light').value + '"/><path d="' + d + '" fill="' + RT.$('#dark').value + '"/></svg>';
}
RT.$('#png').addEventListener('click', function () { if (!current) return; cv.toBlob(function (b) { RT.download(b, 'qr-code.png'); }, 'image/png'); });
RT.$('#svg').addEventListener('click', function () { if (!current) return; RT.download(new Blob([svgString()], { type: 'image/svg+xml' }), 'qr-code.svg'); });
RT.live(document.getElementById('tool'), render);
""",
    "article": {
        "it": """
<h2>Cosa puoi mettere in un codice QR</h2>
<ul>
<li><strong>Link:</strong> il caso più comune. Inquadrando il codice, il telefono propone di aprire la pagina: menu del ristorante, sito, profilo social, volantino, biglietto da visita, recensioni.</li>
<li><strong>Testo:</strong> qualsiasi testo, per esempio un codice sconto, un indirizzo o un messaggio.</li>
<li><strong>Wi-Fi:</strong> nome della rete, tipo di sicurezza e password: gli ospiti si collegano inquadrando il codice, senza digitare nulla. Perfetto per case vacanza, bar e uffici.</li>
<li><strong>Telefono, email, SMS:</strong> il telefono apre direttamente la chiamata, una nuova email (con oggetto e testo già compilati) o un messaggio.</li>
</ul>
<h2>Dimensione, colori e correzione errori</h2>
<p>Per la stampa scegli almeno <strong>1024 px</strong> o scarica l'<strong>SVG</strong>, che si ingrandisce all'infinito senza perdere nitidezza (ideale per grafici e tipografie). Il codice deve avere un buon contrasto: colore scuro su sfondo chiaro, mai il contrario, e lascia sempre un bordo bianco intorno (è già incluso). Con un lato di almeno 2 cm su carta si legge senza problemi da 20-30 cm di distanza.</p>
<p>La <strong>correzione errori</strong> permette di leggere il codice anche se è in parte rovinato o coperto: «Media» va bene quasi sempre; scegli «Alta» o «Massima» se prevedi di sovrapporre un logo al centro o di stampare su superfici che si usurano. Livelli più alti producono codici più fitti.</p>
<h2>Nessuna scadenza, nessun tracciamento</h2>
<p>I codici creati qui sono «statici»: il contenuto è scritto direttamente nel codice, quindi funzionano per sempre, non dipendono da un servizio esterno e non tracciano chi li inquadra. Il rovescio della medaglia è che non puoi cambiare il link dopo la stampa: se ti serve questa flessibilità, punta il QR a una pagina tua che potrai aggiornare.</p>
<h2>Consigli prima di stampare</h2>
<ul>
<li>Prova sempre il codice con due o tre telefoni diversi prima di stamparlo in grande.</li>
<li>Usa link brevi: meno caratteri significano un codice meno fitto e più facile da leggere.</li>
<li>Scrivi accanto al codice cosa succede inquadrandolo («Menu», «Wi-Fi gratis», «Prenota»).</li>
</ul>
""",
        "en": """
<h2>What you can put in a QR code</h2>
<ul>
<li><strong>Links:</strong> the most common case. When scanned, the phone offers to open the page: restaurant menu, website, social profile, flyer, business card, reviews.</li>
<li><strong>Text:</strong> any text, such as a discount code, an address or a message.</li>
<li><strong>Wi-Fi:</strong> network name, security type and password: guests connect by scanning, without typing anything. Perfect for holiday rentals, cafés and offices.</li>
<li><strong>Phone, email, SMS:</strong> the phone directly opens a call, a new email (with subject and text pre-filled) or a text message.</li>
</ul>
<h2>Size, colours and error correction</h2>
<p>For print choose at least <strong>1024 px</strong> or download the <strong>SVG</strong>, which scales infinitely without losing sharpness (ideal for designers and print shops). The code needs good contrast: dark colour on a light background, never the reverse, and always keep a white margin around it (already included). At 2 cm or more on paper it reads easily from 20-30 cm away.</p>
<p><strong>Error correction</strong> lets the code be read even if partly damaged or covered: "Medium" is fine almost always; pick "Quartile" or "High" if you plan to place a logo in the centre or print on surfaces that wear out. Higher levels produce denser codes.</p>
<h2>No expiry, no tracking</h2>
<p>Codes created here are "static": the content is written directly into the code, so they work forever, don't depend on an external service and don't track who scans them. The flip side is that you can't change the link after printing: if you need that flexibility, point the QR code to a page of your own that you can update.</p>
<h2>Tips before printing</h2>
<ul>
<li>Always test the code with two or three different phones before printing it large.</li>
<li>Use short links: fewer characters mean a less dense code that is easier to read.</li>
<li>Write next to the code what scanning it does ("Menu", "Free Wi-Fi", "Book now").</li>
</ul>
""",
    },
    "faq": {
        "it": [
            ("I codici QR creati qui scadono?", "No. Sono codici statici: il contenuto è dentro il codice stesso e funziona per sempre, senza abbonamenti o servizi esterni."),
            ("Posso cambiare il link dopo aver stampato il codice?", "No, in un codice statico il link è fisso. Se prevedi di cambiarlo, fai puntare il QR a una tua pagina web e aggiorna quella."),
            ("PNG o SVG?", "PNG per social, documenti Word e uso generale; SVG per grafici, tipografie e stampe grandi, perché non perde qualità ingrandendo."),
        ],
        "en": [
            ("Do QR codes created here expire?", "No. They are static codes: the content lives inside the code itself and works forever, with no subscriptions or external services."),
            ("Can I change the link after printing the code?", "No, in a static code the link is fixed. If you expect to change it, point the QR code to your own web page and update that instead."),
            ("PNG or SVG?", "PNG for social media, Word documents and general use; SVG for designers, print shops and large prints, because it doesn't lose quality when enlarged."),
        ],
    },
}

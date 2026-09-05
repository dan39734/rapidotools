TOOL = {
    "id": "resize",
    "cat": "images",
    "icon": "🖼️",
    "slug": {"it": "ridimensiona-comprimi-immagini", "en": "resize-compress-image"},
    "title": {"it": "Ridimensiona e comprimi immagini", "en": "Resize and compress images"},
    "short": {"it": "Riduci dimensioni e peso di foto JPG, PNG e WebP senza caricarle online", "en": "Shrink the size and weight of JPG, PNG and WebP photos without uploading them"},
    "keywords": {"it": ["ridurre peso foto", "comprimere immagine", "ridimensionare foto", "foto sotto 1 mb", "ridurre dimensioni jpg", "foto per concorso"], "en": ["reduce image size", "compress jpg", "shrink photo", "image under 1mb", "resize picture"]},
    "meta": {
        "it": "Ridimensiona e comprimi foto e immagini direttamente nel browser: scegli larghezza, altezza o percentuale, regola la qualità e scarica il file più leggero. Nessun caricamento su server.",
        "en": "Resize and compress photos and images right in your browser: choose width, height or percentage, adjust quality and download the lighter file. No upload to any server.",
    },
    "intro": {
        "it": "Carica una foto, scegli le nuove dimensioni e la qualità: l'immagine viene elaborata sul tuo dispositivo e puoi scaricarla subito, più leggera. Ideale per email, moduli online e concorsi con limiti di peso.",
        "en": "Load a photo, choose the new dimensions and quality: the image is processed on your device and you can download it right away, lighter. Ideal for emails, online forms and uploads with size limits.",
    },
    "strings": {
        "it": {
            "drop": "Trascina qui un'immagine o clicca per sceglierla", "formats": "JPG, PNG, WebP, GIF, BMP", "original": "Originale", "mode": "Ridimensiona per", "m_w": "Larghezza (px)", "m_h": "Altezza (px)", "m_p": "Percentuale (%)", "m_max": "Lato massimo (px)",
            "value": "Valore", "format": "Formato di uscita", "same": "Come l'originale", "quality": "Qualità", "apply": "Applica", "download": "Scarica", "result": "Risultato", "saving": "risparmio",
            "dims": "dimensioni", "size": "peso", "err": "File non riconosciuto come immagine. Nota: le foto HEIC/HEIF dell'iPhone vanno prima convertite in JPG dal telefono.", "presets": "Preset", "p_email": "Email (1600 px)", "p_web": "Web (1200 px)", "p_social": "Social (1080 px)", "p_thumb": "Anteprima (400 px)",
        },
        "en": {
            "drop": "Drag an image here or click to choose one", "formats": "JPG, PNG, WebP, GIF, BMP", "original": "Original", "mode": "Resize by", "m_w": "Width (px)", "m_h": "Height (px)", "m_p": "Percentage (%)", "m_max": "Longest side (px)",
            "value": "Value", "format": "Output format", "same": "Same as original", "quality": "Quality", "apply": "Apply", "download": "Download", "result": "Result", "saving": "saved",
            "dims": "dimensions", "size": "file size", "err": "File not recognised as an image. Note: iPhone HEIC/HEIF photos must be converted to JPG on the phone first.", "presets": "Presets", "p_email": "Email (1600 px)", "p_web": "Web (1200 px)", "p_social": "Social (1080 px)", "p_thumb": "Thumbnail (400 px)",
        },
    },
    "ui": """
<label class="dropzone" id="dz"><input type="file" id="file" accept="image/*"><strong>{{drop}}</strong><br><small>{{formats}}</small></label>
<p class="msg bad hide" id="err">{{err}}</p>
<div id="panel" class="hide">
  <div class="preview"><figure><img id="orig" alt=""><figcaption id="origcap"></figcaption></figure></div>
  <div class="inline" style="margin-top:12px"><span class="lbl">{{presets}}:</span>
    <button class="btn small" type="button" data-max="1600">{{p_email}}</button><button class="btn small" type="button" data-max="1200">{{p_web}}</button>
    <button class="btn small" type="button" data-max="1080">{{p_social}}</button><button class="btn small" type="button" data-max="400">{{p_thumb}}</button></div>
  <div class="row" style="margin-top:12px">
    <div class="field"><label for="mode">{{mode}}</label><select id="mode"><option value="max">{{m_max}}</option><option value="w">{{m_w}}</option><option value="h">{{m_h}}</option><option value="p">{{m_p}}</option></select></div>
    <div class="field"><label for="val">{{value}}</label><input type="number" id="val" value="1600" min="1" inputmode="numeric"></div>
    <div class="field"><label for="fmt">{{format}}</label><select id="fmt"><option value="">{{same}}</option><option value="image/jpeg">JPG</option><option value="image/png">PNG</option><option value="image/webp">WebP</option></select></div>
  </div>
  <div class="field"><label for="q">{{quality}}: <b id="qv">85</b>%</label><input type="range" id="q" min="30" max="100" value="85"></div>
  <div class="btns"><button class="btn primary" type="button" id="apply">{{apply}}</button></div>
  <div class="result hide" id="out">
    <div class="preview"><figure><img id="res" alt=""><figcaption id="rescap"></figcaption></figure></div>
    <div class="btns"><a class="btn primary" id="dl" download>⬇ {{download}}</a></div>
  </div>
</div>
""",
    "js": r"""
var file = RT.$('#file'), dz = RT.$('#dz'), panel = RT.$('#panel'), err = RT.$('#err'), img = new Image(), origFile = null, outBlob = null;
function fmtDims(w, h) { return w + ' × ' + h + ' px'; }
function load(f) {
  if (!f || !/^image\//.test(f.type)) { err.classList.remove('hide'); return; }
  err.classList.add('hide'); origFile = f;
  var url = URL.createObjectURL(f);
  img.onload = function () {
    RT.$('#orig').src = url; RT.$('#origcap').textContent = T.original + ': ' + fmtDims(img.naturalWidth, img.naturalHeight) + ' · ' + RT.bytes(f.size);
    panel.classList.remove('hide'); RT.$('#out').classList.add('hide');
    if (RT.$('#mode').value === 'max' && +RT.$('#val').value > Math.max(img.naturalWidth, img.naturalHeight)) RT.$('#val').value = Math.max(img.naturalWidth, img.naturalHeight);
    apply();
  };
  img.onerror = function () { err.classList.remove('hide'); };
  img.src = url;
}
file.addEventListener('change', function () { load(file.files[0]); });
['dragenter', 'dragover'].forEach(function (e) { dz.addEventListener(e, function (ev) { ev.preventDefault(); dz.classList.add('over'); }); });
['dragleave', 'drop'].forEach(function (e) { dz.addEventListener(e, function (ev) { ev.preventDefault(); dz.classList.remove('over'); }); });
dz.addEventListener('drop', function (ev) { if (ev.dataTransfer.files[0]) load(ev.dataTransfer.files[0]); });
document.addEventListener('paste', function (ev) { var items = ev.clipboardData && ev.clipboardData.items; if (!items) return; for (var i = 0; i < items.length; i++) if (items[i].type.indexOf('image') === 0) { load(items[i].getAsFile()); break; } });
RT.$('#q').addEventListener('input', function () { RT.$('#qv').textContent = RT.$('#q').value; });
RT.$$('[data-max]').forEach(function (b) { b.addEventListener('click', function () { RT.$('#mode').value = 'max'; RT.$('#val').value = b.getAttribute('data-max'); apply(); }); });
function target() {
  var W = img.naturalWidth, H = img.naturalHeight, v = +RT.$('#val').value || 1, m = RT.$('#mode').value, w, h;
  if (m === 'w') { w = v; h = Math.round(H * v / W); } else if (m === 'h') { h = v; w = Math.round(W * v / H); }
  else if (m === 'p') { w = Math.round(W * v / 100); h = Math.round(H * v / 100); }
  else { var s = Math.min(1, v / Math.max(W, H)); w = Math.round(W * s); h = Math.round(H * s); }
  return [Math.max(1, w), Math.max(1, h)];
}
function apply() {
  if (!origFile) return;
  var t = target(), type = RT.$('#fmt').value || (origFile.type === 'image/png' || origFile.type === 'image/webp' ? origFile.type : 'image/jpeg');
  if (type === 'image/gif' || type === 'image/bmp') type = 'image/png';
  var c = document.createElement('canvas'); c.width = t[0]; c.height = t[1];
  var ctx = c.getContext('2d');
  if (type === 'image/jpeg') { ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, c.width, c.height); }
  // step-down for quality when shrinking a lot
  var src = img, sw = img.naturalWidth, sh = img.naturalHeight;
  while (sw / 2 > t[0] && sh / 2 > t[1]) { var tmp = document.createElement('canvas'); tmp.width = Math.round(sw / 2); tmp.height = Math.round(sh / 2); tmp.getContext('2d').drawImage(src, 0, 0, tmp.width, tmp.height); src = tmp; sw = tmp.width; sh = tmp.height; }
  ctx.imageSmoothingQuality = 'high'; ctx.drawImage(src, 0, 0, c.width, c.height);
  c.toBlob(function (blob) {
    if (!blob) return; outBlob = blob;
    var url = URL.createObjectURL(blob); RT.$('#res').src = url;
    var saving = origFile.size ? Math.round((1 - blob.size / origFile.size) * 100) : 0;
    RT.$('#rescap').textContent = T.result + ': ' + fmtDims(c.width, c.height) + ' · ' + RT.bytes(blob.size) + (saving > 0 ? ' (−' + saving + '% ' + T.saving + ')' : '');
    var ext = type === 'image/png' ? 'png' : type === 'image/webp' ? 'webp' : 'jpg';
    var dl = RT.$('#dl'); dl.href = url; dl.download = origFile.name.replace(/\.[^.]+$/, '') + '-' + c.width + 'x' + c.height + '.' + ext;
    RT.$('#out').classList.remove('hide');
  }, type, +RT.$('#q').value / 100);
}
RT.$('#apply').addEventListener('click', apply);
""",
    "article": {
        "it": """
<h2>Come funziona</h2>
<p>Scegli un'immagine (o trascinala, o incollala con Ctrl+V), imposta le nuove dimensioni e la qualità, premi <strong>Applica</strong> e scarica il risultato. Tutto avviene nel browser grazie alle funzioni di disegno del tuo dispositivo: la foto non viene caricata su nessun server, quindi funziona anche offline ed è adatta a documenti e foto personali.</p>
<h2>Ridimensionare: quale opzione scegliere</h2>
<ul>
<li><strong>Lato massimo:</strong> il modo più semplice. Imposti quanti pixel deve avere il lato più lungo (1600 per un'email, 1200 per un sito, 1080 per i social) e le proporzioni restano identiche.</li>
<li><strong>Larghezza o altezza:</strong> quando un modulo richiede una misura precisa, per esempio 600 px di larghezza.</li>
<li><strong>Percentuale:</strong> per dimezzare (50%) o ridurre a un quarto (25%) qualsiasi immagine.</li>
</ul>
<p>Le foto dei telefoni moderni misurano 4000 × 3000 pixel o più: per lo schermo e per il web ne bastano 1200-1600, che pesano dieci volte meno senza differenze visibili.</p>
<h2>Comprimere: formato e qualità</h2>
<p>Il <strong>JPG</strong> è il formato giusto per le foto: con qualità 80-85 l'occhio non nota differenze e il file si riduce molto. Il <strong>WebP</strong> pesa circa il 25-30% meno del JPG a parità di qualità ed è supportato da tutti i browser recenti. Il <strong>PNG</strong> è senza perdita e conserva la trasparenza: perfetto per loghi, schermate e grafica, ma pesante per le foto (la qualità non ha effetto sul PNG).</p>
<h2>Limiti di peso comuni</h2>
<p>Moduli della pubblica amministrazione e concorsi chiedono spesso foto sotto 1 MB o 500 KB; molti portali accettano al massimo 2 MB; le foto per i documenti hanno formati precisi (per esempio 35 × 45 mm, 413 × 531 px). Con lato massimo 1200 px e qualità 80 una foto da 5 MB scende di solito sotto i 300 KB.</p>
""",
        "en": """
<h2>How it works</h2>
<p>Choose an image (or drag it in, or paste it with Ctrl+V), set the new dimensions and quality, press <strong>Apply</strong> and download the result. Everything happens in your browser using your device's own drawing functions: the photo is never uploaded to a server, so it works offline too and is safe for documents and personal photos.</p>
<h2>Resizing: which option to pick</h2>
<ul>
<li><strong>Longest side:</strong> the simplest way. Set how many pixels the longer side should have (1600 for email, 1200 for a website, 1080 for social media) and the proportions stay the same.</li>
<li><strong>Width or height:</strong> when a form requires an exact measure, for example 600 px wide.</li>
<li><strong>Percentage:</strong> to halve (50%) or quarter (25%) any image.</li>
</ul>
<p>Modern phone photos are 4000 × 3000 pixels or more: for screens and the web 1200-1600 is plenty, and weighs ten times less with no visible difference.</p>
<h2>Compressing: format and quality</h2>
<p><strong>JPG</strong> is the right format for photos: at quality 80-85 the eye sees no difference and the file shrinks a lot. <strong>WebP</strong> is about 25-30% smaller than JPG at the same quality and is supported by all recent browsers. <strong>PNG</strong> is lossless and keeps transparency: perfect for logos, screenshots and graphics, but heavy for photos (the quality slider has no effect on PNG).</p>
<h2>Common size limits</h2>
<p>Government forms and job applications often require photos under 1 MB or 500 KB; many portals accept 2 MB at most; ID photos have precise formats (for example 35 × 45 mm, 413 × 531 px). With a 1200 px longest side and quality 80, a 5 MB photo usually drops below 300 KB.</p>
""",
    },
    "faq": {
        "it": [
            ("Le mie foto vengono caricate da qualche parte?", "No. L'elaborazione avviene nel browser, sul tuo dispositivo: puoi usare lo strumento anche senza connessione."),
            ("Come porto una foto sotto 1 MB?", "Imposta «Lato massimo» a 1600 px, formato JPG e qualità 80, poi premi Applica: nella didascalia vedi il nuovo peso. Se serve, abbassa la qualità o le dimensioni."),
            ("Perché il PNG resta pesante?", "Il PNG è un formato senza perdita: la qualità non incide. Per le foto scegli JPG o WebP; usa il PNG solo per grafica, loghi e immagini con trasparenza."),
        ],
        "en": [
            ("Are my photos uploaded anywhere?", "No. Processing happens in the browser, on your device: you can use the tool even without a connection."),
            ("How do I get a photo under 1 MB?", "Set \"Longest side\" to 1600 px, format JPG and quality 80, then press Apply: the caption shows the new size. Lower the quality or dimensions if needed."),
            ("Why does PNG stay heavy?", "PNG is a lossless format: quality has no effect. For photos choose JPG or WebP; use PNG only for graphics, logos and images with transparency."),
        ],
    },
}

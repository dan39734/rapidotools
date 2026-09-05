TOOL = {
    "id": "convert_image",
    "cat": "images",
    "icon": "🔄",
    "slug": {"it": "converti-immagini", "en": "image-converter"},
    "title": {"it": "Converti immagini: PNG, JPG, WebP", "en": "Convert images: PNG, JPG, WebP"},
    "short": {"it": "Cambia formato a una o più immagini nel browser, anche in blocco", "en": "Change the format of one or more images in your browser, in batch too"},
    "keywords": {"it": ["png in jpg", "webp in jpg", "jpg in png", "convertire foto", "cambiare formato immagine"], "en": ["png to jpg", "webp to jpg", "jpg to png", "convert photo", "change image format"]},
    "meta": {
        "it": "Converti immagini da PNG, WebP, GIF o BMP a JPG, PNG o WebP direttamente nel browser, anche più file insieme. Senza caricamenti su server, gratis e senza registrazione.",
        "en": "Convert images from PNG, WebP, GIF or BMP to JPG, PNG or WebP right in your browser, several files at once. No server uploads, free and with no sign-up.",
    },
    "intro": {
        "it": "Scegli uno o più file, il formato di destinazione e, per JPG e WebP, la qualità: ogni immagine viene convertita sul tuo dispositivo e scaricata con un clic.",
        "en": "Pick one or more files, the target format and, for JPG and WebP, the quality: every image is converted on your device and downloaded with one click.",
    },
    "strings": {
        "it": {
            "drop": "Trascina qui le immagini o clicca per sceglierle", "formats": "PNG, JPG, WebP, GIF, BMP – anche più file insieme", "to": "Converti in", "quality": "Qualità (JPG/WebP)", "bg": "Sfondo per le trasparenze (JPG)",
            "convert": "Converti", "download": "Scarica", "all": "Scarica tutte", "err": "Nessuna immagine valida. Nota: i file HEIC/HEIF dell'iPhone vanno prima convertiti in JPG dal telefono.", "done": "Convertite", "file": "File", "before": "Prima", "after": "Dopo",
        },
        "en": {
            "drop": "Drag images here or click to choose them", "formats": "PNG, JPG, WebP, GIF, BMP – several files at once", "to": "Convert to", "quality": "Quality (JPG/WebP)", "bg": "Background for transparency (JPG)",
            "convert": "Convert", "download": "Download", "all": "Download all", "err": "No valid image. Note: iPhone HEIC/HEIF files must be converted to JPG on the phone first.", "done": "Converted", "file": "File", "before": "Before", "after": "After",
        },
    },
    "ui": """
<label class="dropzone" id="dz"><input type="file" id="file" accept="image/*" multiple><strong>{{drop}}</strong><br><small>{{formats}}</small></label>
<p class="msg bad hide" id="err">{{err}}</p>
<div class="row" style="margin-top:12px">
  <div class="field"><label for="fmt">{{to}}</label><select id="fmt"><option value="image/jpeg">JPG</option><option value="image/png">PNG</option><option value="image/webp">WebP</option></select></div>
  <div class="field"><label for="q">{{quality}}: <b id="qv">90</b>%</label><input type="range" id="q" min="30" max="100" value="90"></div>
  <div class="field"><label for="bg">{{bg}}</label><input type="color" id="bg" value="#ffffff" style="height:42px;width:80px"></div>
</div>
<div class="btns"><button class="btn primary" type="button" id="go" disabled>{{convert}}</button><button class="btn" type="button" id="all" disabled>{{all}}</button></div>
<div class="table-wrap hide" id="listwrap" style="margin-top:14px"><table><thead><tr><th>{{file}}</th><th>{{before}}</th><th>{{after}}</th><th></th></tr></thead><tbody id="list"></tbody></table></div>
""",
    "js": r"""
var file = RT.$('#file'), dz = RT.$('#dz'), err = RT.$('#err'), list = RT.$('#list'), go = RT.$('#go'), all = RT.$('#all');
var files = [], results = [];
RT.$('#q').addEventListener('input', function () { RT.$('#qv').textContent = RT.$('#q').value; });
function setFiles(fl) {
  files = Array.prototype.filter.call(fl, function (f) { return /^image\//.test(f.type); });
  err.classList.toggle('hide', files.length > 0); go.disabled = !files.length; all.disabled = true; results = [];
  list.innerHTML = files.map(function (f, i) { return '<tr id="r' + i + '"><td>' + f.name + '</td><td>' + RT.bytes(f.size) + '</td><td>–</td><td></td></tr>'; }).join('');
  RT.$('#listwrap').classList.toggle('hide', !files.length);
}
file.addEventListener('change', function () { setFiles(file.files); });
['dragenter', 'dragover'].forEach(function (e) { dz.addEventListener(e, function (ev) { ev.preventDefault(); dz.classList.add('over'); }); });
['dragleave', 'drop'].forEach(function (e) { dz.addEventListener(e, function (ev) { ev.preventDefault(); dz.classList.remove('over'); }); });
dz.addEventListener('drop', function (ev) { setFiles(ev.dataTransfer.files); });
function convertOne(f, type, q, bg) {
  return new Promise(function (resolve, reject) {
    var img = new Image(), url = URL.createObjectURL(f);
    img.onload = function () {
      var c = document.createElement('canvas'); c.width = img.naturalWidth; c.height = img.naturalHeight;
      var ctx = c.getContext('2d');
      if (type === 'image/jpeg') { ctx.fillStyle = bg; ctx.fillRect(0, 0, c.width, c.height); }
      ctx.drawImage(img, 0, 0); URL.revokeObjectURL(url);
      c.toBlob(function (b) { b ? resolve(b) : reject(); }, type, q);
    };
    img.onerror = reject; img.src = url;
  });
}
go.addEventListener('click', function () {
  var type = RT.$('#fmt').value, q = +RT.$('#q').value / 100, bg = RT.$('#bg').value, ext = type === 'image/png' ? 'png' : type === 'image/webp' ? 'webp' : 'jpg';
  go.disabled = true; results = [];
  var chain = Promise.resolve();
  files.forEach(function (f, i) {
    chain = chain.then(function () {
      return convertOne(f, type, q, bg).then(function (blob) {
        var name = f.name.replace(/\.[^.]+$/, '') + '.' + ext, url = URL.createObjectURL(blob);
        results.push({ url: url, name: name });
        var tr = RT.$('#r' + i); tr.children[2].textContent = RT.bytes(blob.size);
        tr.children[3].innerHTML = '<a class="btn small primary" download="' + name + '" href="' + url + '">⬇ ' + T.download + '</a>';
      }, function () { var tr = RT.$('#r' + i); tr.children[2].textContent = '✗'; });
    });
  });
  chain.then(function () { go.disabled = false; all.disabled = results.length < 2; });
});
all.addEventListener('click', function () { results.forEach(function (r, i) { setTimeout(function () { RT.download(r.url, r.name); }, i * 300); }); });
""",
    "article": {
        "it": """
<h2>Quale formato scegliere</h2>
<ul>
<li><strong>JPG</strong> – il formato universale per le foto: file leggeri, accettato da qualsiasi sito, modulo e programma. Non supporta la trasparenza: le aree trasparenti vengono riempite con il colore di sfondo che scegli (bianco per impostazione predefinita).</li>
<li><strong>PNG</strong> – senza perdita di qualità e con trasparenza: ideale per loghi, icone, schermate e grafica con testo. Per le fotografie produce file molto grandi.</li>
<li><strong>WebP</strong> – il formato moderno per il web: più leggero del JPG e del PNG, supporta la trasparenza. È letto da tutti i browser recenti, ma alcuni programmi e siti più vecchi non lo accettano: in quel caso convertilo in JPG o PNG.</li>
</ul>
<h2>Casi tipici</h2>
<ul>
<li><strong>WebP → JPG:</strong> hai scaricato un'immagine da un sito e il tuo programma non la apre.</li>
<li><strong>PNG → JPG:</strong> uno screenshot o una grafica da inviare via email o caricare dove il PNG è troppo pesante o non accettato.</li>
<li><strong>JPG → PNG:</strong> un modulo o un servizio che accetta solo PNG (la conversione non migliora la qualità, la mantiene).</li>
<li><strong>GIF/BMP → PNG o JPG:</strong> per aggiornare formati vecchi; delle GIF animate viene conservato solo il primo fotogramma.</li>
</ul>
<h2>Conversione in blocco</h2>
<p>Puoi selezionare più immagini insieme: vengono convertite una dopo l'altra e per ciascuna trovi il pulsante di download nella tabella, con il peso prima e dopo. «Scarica tutte» avvia i download in sequenza (il browser potrebbe chiedere il permesso per i download multipli). La conversione mantiene le dimensioni originali in pixel: se vuoi anche ridurle, usa lo strumento <a href="../ridimensiona-comprimi-immagini/">Ridimensiona e comprimi immagini</a>.</p>
""",
        "en": """
<h2>Which format to choose</h2>
<ul>
<li><strong>JPG</strong> – the universal format for photos: small files, accepted by any website, form and program. It has no transparency: transparent areas are filled with the background colour you pick (white by default).</li>
<li><strong>PNG</strong> – lossless and with transparency: ideal for logos, icons, screenshots and graphics with text. For photographs it produces very large files.</li>
<li><strong>WebP</strong> – the modern web format: lighter than JPG and PNG, with transparency support. All recent browsers read it, but some older programs and websites don't accept it: convert it to JPG or PNG in that case.</li>
</ul>
<h2>Typical cases</h2>
<ul>
<li><strong>WebP → JPG:</strong> you downloaded an image from a website and your program won't open it.</li>
<li><strong>PNG → JPG:</strong> a screenshot or graphic to email or upload where PNG is too heavy or not accepted.</li>
<li><strong>JPG → PNG:</strong> a form or service that only accepts PNG (conversion keeps the quality, it doesn't improve it).</li>
<li><strong>GIF/BMP → PNG or JPG:</strong> to update old formats; for animated GIFs only the first frame is kept.</li>
</ul>
<h2>Batch conversion</h2>
<p>You can select several images at once: they are converted one after another and each gets a download button in the table, with the size before and after. "Download all" starts the downloads in sequence (the browser may ask permission for multiple downloads). Conversion keeps the original pixel dimensions: to shrink them as well, use the <a href="../resize-compress-image/">Resize and compress images</a> tool.</p>
""",
    },
    "faq": {
        "it": [
            ("Posso convertire le foto HEIC dell'iPhone?", "Non direttamente: i browser non leggono l'HEIC. Sull'iPhone vai in Impostazioni › Fotocamera › Formati e scegli «Più compatibile», oppure condividi la foto: viene inviata come JPG."),
            ("La conversione peggiora la qualità?", "Da PNG a PNG o WebP senza perdita no. Verso JPG c'è una leggera compressione: con qualità 90 è invisibile. Convertire un JPG in PNG non recupera qualità già persa."),
            ("Le immagini restano sul mio dispositivo?", "Sì: la conversione avviene nel browser e nessun file viene caricato su un server."),
        ],
        "en": [
            ("Can I convert iPhone HEIC photos?", "Not directly: browsers can't read HEIC. On the iPhone go to Settings › Camera › Formats and choose \"Most Compatible\", or share the photo: it is sent as JPG."),
            ("Does conversion reduce quality?", "PNG to PNG or lossless WebP, no. To JPG there is slight compression: at quality 90 it is invisible. Converting a JPG to PNG doesn't recover quality already lost."),
            ("Do the images stay on my device?", "Yes: conversion happens in the browser and no file is uploaded to a server."),
        ],
    },
}

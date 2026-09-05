TOOL = {
    "id": "vat",
    "cat": "money",
    "icon": "🧾",
    "slug": {"it": "calcolo-iva", "en": "vat-calculator"},
    "title": {"it": "Calcolo IVA: aggiungi o scorpora l'IVA", "en": "VAT calculator: add or remove VAT"},
    "short": {"it": "Da imponibile a totale e viceversa, con aliquote 22, 10, 5 e 4%", "en": "From net to gross and back, with any rate"},
    "keywords": {"it": ["scorporo iva", "iva al 22", "calcolo imponibile", "prezzo con iva", "iva inclusa", "aliquote iva"], "en": ["vat inclusive", "vat exclusive", "reverse vat", "sales tax calculator", "net to gross"]},
    "meta": {
        "it": "Calcola l'IVA in un attimo: aggiungi l'IVA a un prezzo netto o scorporala da un prezzo lordo, con le aliquote italiane (22%, 10%, 5%, 4%) o una personalizzata.",
        "en": "Calculate VAT in a second: add VAT to a net price or remove it from a gross price, with common rates (20%, 19%, 21%, 22%) or a custom one.",
    },
    "intro": {
        "it": "Scrivi un importo e scegli l'aliquota: vedi imponibile, IVA e totale sia partendo dal netto («aggiungi IVA») sia dal prezzo finale («scorpora IVA»).",
        "en": "Enter an amount and choose the rate: see net, VAT and gross both starting from the net price (\"add VAT\") and from the final price (\"remove VAT\").",
    },
    "strings": {
        "it": {
            "mode": "Operazione", "add": "Aggiungi IVA (parto dal netto)", "remove": "Scorpora IVA (parto dal lordo)", "amount": "Importo", "rate": "Aliquota IVA",
            "custom": "Personalizzata", "net": "Imponibile (netto)", "vat": "IVA", "gross": "Totale (lordo)", "r22": "22% – ordinaria", "r10": "10% – ridotta", "r5": "5% – ridotta", "r4": "4% – super ridotta",
            "r20": "20%", "r19": "19%", "r21": "21%", "r23": "23%", "r25": "25%", "rate_custom": "Aliquota personalizzata %",
        },
        "en": {
            "mode": "Operation", "add": "Add VAT (start from net)", "remove": "Remove VAT (start from gross)", "amount": "Amount", "rate": "VAT rate",
            "custom": "Custom", "net": "Net (excluding VAT)", "vat": "VAT", "gross": "Gross (including VAT)", "r22": "22% – Italy", "r10": "10%", "r5": "5%", "r4": "4%",
            "r20": "20% – UK / France", "r19": "19% – Germany", "r21": "21% – Spain / Netherlands", "r23": "23% – Ireland / Poland", "r25": "25% – Sweden / Denmark", "rate_custom": "Custom rate %",
        },
    },
    "ui": """
<div class="row">
  <div class="field"><label for="mode">{{mode}}</label><select id="mode"><option value="add">{{add}}</option><option value="remove">{{remove}}</option></select></div>
  <div class="field"><label for="amt">{{amount}}</label><input type="text" inputmode="decimal" id="amt" value="100"></div>
</div>
<div class="row">
  <div class="field"><label for="rate">{{rate}}</label><select id="rate"></select></div>
  <div class="field hide" id="customf"><label for="crate">{{rate_custom}}</label><input type="text" inputmode="decimal" id="crate" value="22"></div>
</div>
<div class="result hide" id="out">
  <div class="stats">
    <div class="stat"><b id="net"></b><span>{{net}}</span></div>
    <div class="stat"><b id="vat"></b><span>{{vat}} <span id="rlbl"></span></span></div>
    <div class="stat" style="border-color:var(--accent)"><b id="gross"></b><span>{{gross}}</span></div>
  </div>
</div>
""",
    "js": r"""
var rate = RT.$('#rate'), customf = RT.$('#customf'), out = RT.$('#out');
var rates = RT.lang === 'it' ? [['22', T.r22], ['10', T.r10], ['5', T.r5], ['4', T.r4], ['20', T.r20], ['19', T.r19], ['21', T.r21], ['custom', T.custom]]
                             : [['20', T.r20], ['19', T.r19], ['21', T.r21], ['22', T.r22], ['23', T.r23], ['25', T.r25], ['10', T.r10], ['5', T.r5], ['custom', T.custom]];
rates.forEach(function (r) { var o = document.createElement('option'); o.value = r[0]; o.textContent = r[1]; rate.appendChild(o); });
function calc() {
  var isCustom = rate.value === 'custom'; customf.classList.toggle('hide', !isCustom);
  var p = isCustom ? RT.num(RT.$('#crate').value) : +rate.value, a = RT.num(RT.$('#amt').value);
  if (!isFinite(a) || !isFinite(p) || p < 0) { out.classList.add('hide'); return; }
  var net, gross;
  if (RT.$('#mode').value === 'add') { net = a; gross = a * (1 + p / 100); } else { gross = a; net = a / (1 + p / 100); }
  RT.$('#net').textContent = RT.money(net); RT.$('#vat').textContent = RT.money(gross - net); RT.$('#gross').textContent = RT.money(gross); RT.$('#rlbl').textContent = '(' + RT.fmt(p, 2) + '%)';
  out.classList.remove('hide');
}
RT.live(document.getElementById('tool'), calc);
""",
    "article": {
        "it": """
<h2>Come si calcola l'IVA</h2>
<p><strong>Aggiungere l'IVA</strong> a un imponibile: totale = netto × (1 + aliquota ÷ 100). Con IVA al 22%, 100 € di imponibile diventano 122 €.</p>
<p><strong>Scorporare l'IVA</strong> da un prezzo lordo: netto = lordo ÷ (1 + aliquota ÷ 100). Da 122 € si torna a 100 € di imponibile e 22 € di IVA. L'errore più comune è togliere il 22% dal lordo (122 − 22% = 95,16 €): è sbagliato, perché l'IVA è calcolata sul netto, non sul totale.</p>
<h2>Le aliquote IVA in Italia</h2>
<ul>
<li><strong>22%</strong> – aliquota ordinaria, per la maggior parte di beni e servizi.</li>
<li><strong>10%</strong> – aliquota ridotta: ristorazione e alberghi, molti alimentari, energia elettrica e gas per uso domestico, medicinali, ristrutturazioni edilizie.</li>
<li><strong>5%</strong> – aliquota ridotta: alcuni alimenti (erbe aromatiche, tartufi), servizi socio-sanitari delle cooperative, prodotti per l'infanzia e per l'igiene femminile.</li>
<li><strong>4%</strong> – aliquota super ridotta: pane, latte, frutta e verdura, libri, giornali, prima casa, ausili per disabili.</li>
</ul>
<p>Le aliquote possono cambiare con le leggi di bilancio: per fatture e dichiarazioni verifica sempre quella in vigore per il tuo prodotto.</p>
<h2>Quando serve lo scorporo</h2>
<p>Lo scorporo si usa quando conosci solo il prezzo al pubblico e devi ricavare l'imponibile: per registrare uno scontrino nella contabilità, per confrontare listini «IVA inclusa» e «IVA esclusa», per capire quanta IVA hai pagato su un acquisto o quanto puoi detrarre con la partita IVA.</p>
""",
        "en": """
<h2>How VAT is calculated</h2>
<p><strong>Adding VAT</strong> to a net amount: gross = net × (1 + rate ÷ 100). At 20% VAT, a net price of 100 becomes 120.</p>
<p><strong>Removing VAT</strong> from a gross price: net = gross ÷ (1 + rate ÷ 100). From 120 you get back to 100 net and 20 VAT. The most common mistake is to take 20% off the gross (120 − 20% = 96): that is wrong, because VAT is charged on the net amount, not on the total.</p>
<h2>Common VAT rates</h2>
<ul>
<li><strong>United Kingdom:</strong> 20% standard, 5% reduced (home energy, child car seats), 0% on most food, books and children's clothes.</li>
<li><strong>Germany:</strong> 19% standard, 7% reduced. <strong>France:</strong> 20% standard, 10% and 5.5% reduced.</li>
<li><strong>Italy:</strong> 22% standard, 10%, 5% and 4% reduced. <strong>Spain:</strong> 21%, 10% and 4%.</li>
<li><strong>Ireland:</strong> 23%. <strong>Sweden and Denmark:</strong> 25%. <strong>Switzerland:</strong> 8.1%.</li>
</ul>
<p>Rates change with budget laws: for invoices and tax returns always check the rate in force for your product and country. For US sales tax, which is added at checkout and varies by state and city, use the custom rate.</p>
<h2>When you need to remove VAT</h2>
<p>Reverse calculation is useful when you only know the retail price and need the net amount: to record a receipt in your books, to compare "VAT included" and "VAT excluded" price lists, or to see how much VAT you paid on a purchase and can reclaim if you are VAT-registered.</p>
""",
    },
    "faq": {
        "it": [
            ("Come si scorpora l'IVA al 22%?", "Dividi il prezzo lordo per 1,22. Esempio: 244 € ÷ 1,22 = 200 € di imponibile e 44 € di IVA."),
            ("Perché non posso semplicemente togliere il 22%?", "Perché l'IVA è il 22% del netto, non del lordo. Togliendo il 22% dal totale otterresti un imponibile troppo basso."),
            ("Quale aliquota si applica al mio prodotto?", "Dipende dalla categoria: la maggior parte dei beni ha il 22%, alimentari e ristorazione spesso il 10% o il 4%. In caso di dubbio consulta le tabelle dell'Agenzia delle Entrate o un commercialista."),
        ],
        "en": [
            ("How do I remove 20% VAT from a price?", "Divide the gross price by 1.20. Example: 240 ÷ 1.20 = 200 net and 40 VAT."),
            ("Why can't I just subtract 20%?", "Because VAT is 20% of the net amount, not of the gross. Subtracting 20% from the total gives a net figure that is too low."),
            ("Which rate applies to my product?", "It depends on the category and the country: most goods carry the standard rate, while food, books and energy often have reduced rates. When in doubt check your tax authority's tables or ask an accountant."),
        ],
    },
}

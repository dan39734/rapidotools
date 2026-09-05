# Static pages (about, privacy, contact) for Rapido Tools
from site_text import CONTACT_EMAIL

EMAIL_HTML = '<a href="mailto:%s">%s</a>' % (CONTACT_EMAIL, CONTACT_EMAIL)

PAGES = {
    "about": {
        "it": {
            "title": "Informazioni su Rapido Tools",
            "meta": "Cos'è Rapido Tools: una raccolta di strumenti online gratuiti, senza registrazione, che funzionano direttamente nel browser.",
            "html": """
<p>Rapido Tools è una raccolta di strumenti online gratuiti per le piccole esigenze di tutti i giorni: calcolatori, convertitori, generatori e utilità per testo e immagini. È un progetto indipendente, nato da un'idea semplice: molte cose che facciamo ogni giorno online richiedono un piccolo strumento, e quel piccolo strumento dovrebbe aprirsi subito, funzionare al primo colpo e non chiedere nulla in cambio.</p>
<h2>I principi</h2>
<ul>
<li><strong>Gratis e senza registrazione.</strong> Nessun account, nessuna email da lasciare, nessuna versione «premium».</li>
<li><strong>Veloce.</strong> Le pagine sono leggere, senza librerie pesanti, e funzionano bene anche dal telefono o con una connessione lenta.</li>
<li><strong>Rispettoso della privacy.</strong> I calcoli, le conversioni e l'elaborazione delle immagini avvengono interamente nel tuo browser: quello che scrivi o carichi non viene inviato a nessun server.</li>
<li><strong>Chiaro.</strong> Ogni strumento ha una breve guida con esempi e risposte alle domande più frequenti.</li>
</ul>
<h2>Come si sostiene</h2>
<p>Il sito è gratuito per chi lo usa. In futuro potrebbe mostrare qualche annuncio pubblicitario discreto per coprire i costi di dominio e sviluppo; in quel caso l'<a href="../privacy/">informativa sulla privacy</a> verrà aggiornata e ti verrà chiesto il consenso, come previsto dalla legge.</p>
<h2>Precisione dei risultati</h2>
<p>Gli strumenti sono realizzati con cura e verificati, ma vengono forniti «così come sono», senza garanzie. I risultati hanno scopo informativo: per decisioni importanti (mediche, fiscali, finanziarie o legali) rivolgiti sempre a un professionista.</p>
<h2>Suggerimenti</h2>
<p>Manca uno strumento che ti sarebbe utile? Hai trovato un errore? Scrivici dalla pagina <a href="../contatti/">Contatti</a>: le segnalazioni sono il modo migliore per far crescere il sito.</p>
""",
        },
        "en": {
            "title": "About Rapido Tools",
            "meta": "What Rapido Tools is: a collection of free online tools, with no sign-up, that run directly in your browser.",
            "html": """
<p>Rapido Tools is a collection of free online tools for everyday needs: calculators, converters, generators and utilities for text and images. It is an independent project built around a simple idea: many things we do online every day call for a small tool, and that small tool should open instantly, work the first time and ask for nothing in return.</p>
<h2>Principles</h2>
<ul>
<li><strong>Free, no sign-up.</strong> No account, no email to hand over, no "premium" tier.</li>
<li><strong>Fast.</strong> Pages are lightweight, with no heavy libraries, and work well on a phone or a slow connection.</li>
<li><strong>Privacy-friendly.</strong> Calculations, conversions and image processing happen entirely in your browser: what you type or upload is never sent to a server.</li>
<li><strong>Clear.</strong> Every tool comes with a short guide, examples and answers to common questions.</li>
</ul>
<h2>How it's funded</h2>
<p>The site is free to use. In the future it may show a few unobtrusive ads to cover domain and development costs; if that happens, the <a href="../privacy/">privacy policy</a> will be updated and you will be asked for consent, as required by law.</p>
<h2>Accuracy</h2>
<p>The tools are built with care and tested, but they are provided "as is", without warranties. Results are for information only: for important decisions (medical, tax, financial or legal) always consult a professional.</p>
<h2>Suggestions</h2>
<p>Missing a tool you would find useful? Spotted a mistake? Write to us through the <a href="../contact/">Contact</a> page: feedback is the best way to make the site grow.</p>
""",
        },
    },
    "privacy": {
        "it": {
            "title": "Informativa sulla privacy",
            "meta": "Come Rapido Tools tratta i tuoi dati: nessuna raccolta di dati personali, nessun tracciamento, elaborazione interamente nel browser.",
            "html": """
<p><em>Ultimo aggiornamento: settembre 2026.</em></p>
<p>Rapido Tools è progettato per non raccogliere dati personali. Questa pagina spiega in modo semplice cosa succede quando usi il sito.</p>
<h2>Cosa fanno gli strumenti con i tuoi dati</h2>
<p>Tutti gli strumenti funzionano interamente nel tuo browser. I testi che scrivi, i numeri che inserisci e le immagini che carichi vengono elaborati sul tuo dispositivo e <strong>non vengono mai inviati ai nostri server</strong>, né salvati da noi. Quando chiudi la pagina, i dati spariscono.</p>
<h2>Cookie e memoria locale</h2>
<p>Il sito non usa cookie di profilazione e non usa strumenti di analisi statistica. L'unica informazione salvata nel browser è la tua preferenza di lingua (italiano o inglese), memorizzata nella «memoria locale» del browser per riproporti la lingua giusta alla visita successiva. Puoi cancellarla in qualsiasi momento dalle impostazioni del browser.</p>
<h2>Hosting</h2>
<p>Il sito è ospitato su GitHub Pages (GitHub, Inc.). Come ogni servizio di hosting, GitHub può registrare nei propri log tecnici l'indirizzo IP di chi visita le pagine, per motivi di sicurezza e funzionamento del servizio. Rapido Tools non ha accesso a questi dati e non li usa. Per i dettagli consulta la <a href="https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">privacy statement di GitHub</a>.</p>
<h2>Pubblicità</h2>
<p>Al momento il sito non mostra annunci pubblicitari e non include script di terze parti a fini pubblicitari. Se in futuro verranno introdotti annunci (per esempio tramite Google AdSense), questa informativa verrà aggiornata prima dell'attivazione e ti verrà chiesto il consenso all'uso dei cookie pubblicitari tramite un apposito banner, come richiesto dalla normativa europea.</p>
<h2>Link esterni</h2>
<p>Alcune pagine possono contenere link a siti esterni, che hanno le proprie regole sulla privacy. Non siamo responsabili del loro contenuto o del loro trattamento dei dati.</p>
<h2>Titolare e contatti</h2>
<p>Il sito è gestito da un privato, senza finalità di raccolta dati. Per qualsiasi domanda o richiesta relativa alla privacy scrivi a %s.</p>
<h2>Modifiche</h2>
<p>Se il funzionamento del sito cambierà in modo rilevante per la privacy, questa pagina verrà aggiornata e la data in alto indicherà la versione in vigore.</p>
""" % EMAIL_HTML,
        },
        "en": {
            "title": "Privacy policy",
            "meta": "How Rapido Tools handles your data: no personal data collection, no tracking, processing entirely in your browser.",
            "html": """
<p><em>Last updated: September 2026.</em></p>
<p>Rapido Tools is designed not to collect personal data. This page explains in plain words what happens when you use the site.</p>
<h2>What the tools do with your data</h2>
<p>All tools run entirely in your browser. The text you type, the numbers you enter and the images you upload are processed on your device and <strong>are never sent to our servers</strong> or stored by us. When you close the page, the data is gone.</p>
<h2>Cookies and local storage</h2>
<p>The site uses no profiling cookies and no analytics tools. The only piece of information saved in your browser is your language preference (English or Italian), stored in the browser's "local storage" so the right language is shown on your next visit. You can delete it at any time from your browser settings.</p>
<h2>Hosting</h2>
<p>The site is hosted on GitHub Pages (GitHub, Inc.). Like any hosting service, GitHub may record the IP address of visitors in its technical logs for security and operational reasons. Rapido Tools has no access to that data and does not use it. See the <a href="https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub privacy statement</a> for details.</p>
<h2>Advertising</h2>
<p>At the moment the site shows no ads and includes no third-party advertising scripts. If ads are introduced in the future (for example through Google AdSense), this policy will be updated before they go live and you will be asked for consent to advertising cookies through a dedicated banner, as required by European law.</p>
<h2>External links</h2>
<p>Some pages may link to external websites, which have their own privacy rules. We are not responsible for their content or for how they handle data.</p>
<h2>Controller and contact</h2>
<p>The site is run by a private individual and has no data-collection purpose. For any question or request about privacy, write to %s.</p>
<h2>Changes</h2>
<p>If the way the site works changes in a way that matters for your privacy, this page will be updated and the date at the top will show the version in force.</p>
""" % EMAIL_HTML,
        },
    },
    "contact": {
        "it": {
            "title": "Contatti",
            "meta": "Scrivi a Rapido Tools per segnalare un errore, proporre un nuovo strumento o fare una domanda.",
            "html": """
<p>Hai trovato un errore, vuoi proporre un nuovo strumento o hai una domanda? Scrivici: rispondiamo appena possibile.</p>
<p class="result"><strong>Email:</strong> %s</p>
<h2>Cosa ci aiuta</h2>
<ul>
<li>Se segnali un errore, indica lo strumento, i valori inseriti e il risultato che ti aspettavi.</li>
<li>Se proponi uno strumento, descrivi in due righe a cosa ti servirebbe: le idee concrete sono le più facili da realizzare.</li>
</ul>
<p>Rapido Tools non raccoglie dati personali: le email ricevute vengono usate solo per rispondere.</p>
""" % EMAIL_HTML,
        },
        "en": {
            "title": "Contact",
            "meta": "Write to Rapido Tools to report a bug, suggest a new tool or ask a question.",
            "html": """
<p>Found a bug, want to suggest a new tool or have a question? Write to us: we reply as soon as we can.</p>
<p class="result"><strong>Email:</strong> %s</p>
<h2>What helps us</h2>
<ul>
<li>When reporting a bug, tell us which tool, the values you entered and the result you expected.</li>
<li>When suggesting a tool, describe in a couple of lines what you would use it for: concrete ideas are the easiest to build.</li>
</ul>
<p>Rapido Tools collects no personal data: emails we receive are used only to reply.</p>
""" % EMAIL_HTML,
        },
    },
}

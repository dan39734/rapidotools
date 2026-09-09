# Site-wide strings for Rapido Tools (it / en)

SITE_NAME = "Rapido Tools"
DOMAIN = "https://rapidotools.com"
YEAR = "2026"
CONTACT_EMAIL = "tartaruswarp@gmail.com"

LANGS = ["it", "en"]

TEXT = {
    "it": {
        "tagline": "Strumenti online gratuiti, veloci e senza registrazione",
        "home_title": "Rapido Tools – Strumenti online gratuiti: calcolatori, convertitori e utilità",
        "home_meta": "Calcolatori, convertitori e strumenti online gratuiti, senza registrazione e senza pubblicità invadente. Tutto funziona nel tuo browser: date, testo, numeri, scuola e lavoro, salute, soldi e immagini.",
        "home_h1": "Strumenti online gratuiti, veloci e senza registrazione",
        "home_sub": "Calcolatori, convertitori e piccole utilità che funzionano direttamente nel browser, anche dal telefono. Niente account, niente installazioni.",
        "search_ph": "Cerca uno strumento… (es. età, IVA, QR)",
        "search_empty": "Nessuno strumento trovato con questo nome.",
        "all_tools": "Strumenti",
        "lang_switch": "English",
        "lang_switch_code": "en",
        "home": "Home",
        "related": "Strumenti correlati",
        "faq": "Domande frequenti",
        "privacy_blurb": "Tutto avviene nel tuo browser: nessun dato viene inviato a un server.",
        "about": "Informazioni",
        "privacy": "Privacy",
        "contact": "Contatti",
        "footer_note": "Strumenti gratuiti che funzionano nel tuo browser.",
        "why_title": "Perché Rapido Tools",
        "why": [
            ("Gratis e senza registrazione", "Apri la pagina e usa lo strumento. Nessun account, nessuna email da lasciare."),
            ("Veloce, anche dal telefono", "Pagine leggere che si aprono in un istante e funzionano bene su ogni schermo."),
            ("I tuoi dati restano tuoi", "I calcoli e le conversioni avvengono nel browser: testi, numeri e immagini non vengono caricati su nessun server."),
        ],
        "home_seo_title": "Cosa trovi su Rapido Tools",
        "home_seo": "Rapido Tools raccoglie strumenti online gratuiti per le piccole esigenze di tutti i giorni: calcolare l'età o i giorni tra due date, sapere quanti giorni mancano a Natale o a una data qualsiasi, contare le parole di un testo, scrivere un numero in lettere, calcolare la media ponderata e il voto di laurea, la tredicesima o le ferie di una colf, generare una password sicura, calcolare percentuali, sconti, IVA e rata del mutuo, convertire unità di misura, ridimensionare e comprimere le foto o creare un codice QR. Ogni strumento ha una breve guida con esempi e risposte alle domande più comuni. Il sito è in italiano e in inglese e cresce nel tempo: se ti manca uno strumento, <a href=\"contatti/\">scrivici</a>.",
        "not_found_title": "Pagina non trovata",
        "not_found_text": "La pagina che cerchi non esiste o è stata spostata.",
        "go_home": "Vai agli strumenti",
        "copy": "Copia", "copied": "Copiato!", "download": "Scarica", "reset": "Azzera", "calculate": "Calcola",
        "result": "Risultato", "invalid": "Controlla i valori inseriti.",
        "cats": {
            "date": ("📅", "Date e tempo"),
            "text": ("✍️", "Testo"),
            "numbers": ("🔢", "Numeri e conversioni"),
            "work": ("🎓", "Scuola e lavoro"),
            "health": ("❤️", "Salute"),
            "money": ("💶", "Soldi"),
            "images": ("🖼️", "Immagini e QR"),
        },
    },
    "en": {
        "tagline": "Free online tools, fast and with no sign-up",
        "home_title": "Rapido Tools – Free online tools: calculators, converters and utilities",
        "home_meta": "Free online calculators, converters and utilities, no sign-up and no intrusive ads. Everything runs in your browser: dates, text, numbers, school and work, health, money and images.",
        "home_h1": "Free online tools, fast and with no sign-up",
        "home_sub": "Calculators, converters and small utilities that run right in your browser, on your phone too. No account, nothing to install.",
        "search_ph": "Search a tool… (e.g. age, VAT, QR)",
        "search_empty": "No tool matches that name.",
        "all_tools": "All tools",
        "lang_switch": "Italiano",
        "lang_switch_code": "it",
        "home": "Home",
        "related": "Related tools",
        "faq": "Frequently asked questions",
        "privacy_blurb": "Everything runs in your browser: no data is sent to any server.",
        "about": "About",
        "privacy": "Privacy",
        "contact": "Contact",
        "footer_note": "Free tools that run in your browser.",
        "why_title": "Why Rapido Tools",
        "why": [
            ("Free, no sign-up", "Open the page and use the tool. No account, no email to hand over."),
            ("Fast, on your phone too", "Lightweight pages that open instantly and work well on any screen."),
            ("Your data stays yours", "Calculations and conversions happen in your browser: text, numbers and images are never uploaded to a server."),
        ],
        "home_seo_title": "What you'll find on Rapido Tools",
        "home_seo": "Rapido Tools is a collection of free online tools for everyday needs: work out your age or the days between two dates, count down to Christmas or any date, count the words in a text, spell a number in words, work out a weighted grade average, generate a strong password, calculate percentages, discounts, VAT and loan payments, convert units, resize and compress photos or create a QR code. Every tool comes with a short guide, examples and answers to common questions. The site is available in English and Italian and keeps growing: if a tool you need is missing, <a href=\"contact/\">let us know</a>.",
        "not_found_title": "Page not found",
        "not_found_text": "The page you are looking for doesn't exist or has moved.",
        "go_home": "Go to the tools",
        "copy": "Copy", "copied": "Copied!", "download": "Download", "reset": "Reset", "calculate": "Calculate",
        "result": "Result", "invalid": "Please check the values you entered.",
        "cats": {
            "date": ("📅", "Dates & time"),
            "text": ("✍️", "Text"),
            "numbers": ("🔢", "Numbers & conversions"),
            "work": ("🎓", "School & work"),
            "health": ("❤️", "Health"),
            "money": ("💵", "Money"),
            "images": ("🖼️", "Images & QR"),
        },
    },
}

CAT_ORDER = ["date", "text", "numbers", "work", "health", "money", "images"]

# static page slugs per language
STATIC_SLUGS = {
    "about": {"it": "informazioni", "en": "about"},
    "privacy": {"it": "privacy", "en": "privacy"},
    "contact": {"it": "contatti", "en": "contact"},
}

# Rapido Tools – sorgente del sito

Questa cartella contiene il codice che genera il sito statico pubblicato nella radice del repository (GitHub Pages).

- `build.py` – genera tutte le pagine (italiano e inglese) nella cartella `../site` (nel repository: la radice).
- `site_text.py` – testi comuni del sito (menu, categorie, home, footer) nelle due lingue.
- `pages.py` – pagine Informazioni, Privacy e Contatti.
- `tools/` – un file per ogni strumento: testi, interfaccia (`ui`), script (`js`), guida (`article`) e FAQ, in italiano e inglese. L'ordine di visualizzazione è in `tools/__init__.py`.
- `assets/` – CSS, JavaScript condiviso (`site.js`), generatore di codici QR (`qr.js`), icone.
- `test_site.js` – controlli automatici con Playwright (carica tutte le pagine, prova ogni strumento, fa screenshot).
- `test_qr.js`, `test_qr_sweep.js` – verifica del generatore QR (i codici vengono decodificati con OpenCV).

## Come si aggiorna il sito

1. Modificare o aggiungere i file in `tools/` (per un nuovo strumento: nuovo file + nome nella lista `ORDER` di `tools/__init__.py`).
2. Alzare `VERSION` e `LASTMOD` in `build.py`.
3. Eseguire `python3 build.py`: la cartella `../site` viene rigenerata da zero.
4. Copiare il contenuto di `../site` nella radice del repository (insieme a questa cartella `src/`) e caricare su GitHub.

Per aggiungere gli annunci Google AdSense in futuro: nel template di `build.py` ci sono i segnaposto `<!-- AD:top -->` e `<!-- AD:bottom -->`; lo script AdSense (con il banner del consenso «Privacy & messaging») va inserito nell'`<head>` di `layout()`.

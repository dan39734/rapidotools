#!/usr/bin/env python3
"""Build the Rapido Tools static site into ../site from the tool definitions in tools/."""
import html
import importlib
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(os.path.dirname(HERE), "site")

from site_text import SITE_NAME, DOMAIN, YEAR, LANGS, TEXT, CAT_ORDER, STATIC_SLUGS  # noqa: E402
from pages import PAGES  # noqa: E402
import tools  # noqa: E402

VERSION = "1.3.0"
LASTMOD = "2026-09-19"

LOGO_SVG = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M13 2 4 14h6l-1 8 9-12h-6l1-8z" '
            'fill="currentColor"/></svg>')
SEARCH_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
              '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>')


def esc(s):
    return html.escape(s, quote=True)


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def tool_url(tool, lang):
    return "%s/%s/" % (lang, tool["slug"][lang])


def static_url(key, lang):
    return "%s/%s/" % (lang, STATIC_SLUGS[key][lang])


def layout(lang, *, title, meta, canonical_path, alternates, body, rel, scripts="", jsonld=None, noindex=False):
    """Wrap page body into the shared layout.
    rel: relative prefix to reach the site root from this page ('' , '../', '../../').
    alternates: dict lang -> path (relative to root), plus optional 'x-default'.
    """
    T = TEXT[lang]
    other = T["lang_switch_code"]
    other_path = alternates.get(other)
    alt_links = "".join(
        '<link rel="alternate" hreflang="%s" href="%s/%s">' % (k, DOMAIN, v) for k, v in alternates.items()
    )
    lang_link = ""
    if other_path is not None:
        lang_link = '<a class="lang" href="%s%s" data-setlang="%s" hreflang="%s" lang="%s">%s</a>' % (
            rel, other_path, other, other, other, T["lang_switch"])
    footer_links = " · ".join(
        '<a href="%s%s">%s</a>' % (rel, static_url(k, lang), T[k]) for k in ("about", "privacy", "contact")
    )
    jsonld_tag = ""
    if jsonld:
        jsonld_tag = '<script type="application/ld+json">%s</script>' % json.dumps(jsonld, ensure_ascii=False)
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(meta)}">
{robots}
<link rel="canonical" href="{DOMAIN}/{canonical_path}">
{alt_links}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(meta)}">
<meta property="og:url" content="{DOMAIN}/{canonical_path}">
<meta property="og:locale" content="{'it_IT' if lang == 'it' else 'en_US'}">
<meta name="theme-color" content="#d9480f">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{rel}assets/icon-180.png">
<link rel="stylesheet" href="{rel}assets/style.css?v={VERSION}">
{jsonld_tag}
</head>
<body>
<header class="site-header"><div class="container">
<a class="logo" href="{rel}{lang}/">{LOGO_SVG}<span>Rapido<em>Tools</em></span></a>
<nav class="nav"><a href="{rel}{lang}/">{T['all_tools']}</a>{lang_link}</nav>
</div></header>
{body}
<footer class="site-footer"><div class="container">
<span>© {YEAR} {SITE_NAME} · {T['footer_note']}</span>
<span class="spacer"></span>
<span>{footer_links}</span>
</div></footer>
<script src="{rel}assets/site.js?v={VERSION}"></script>
{scripts}
</body>
</html>
"""


def card(tool, lang, rel):
    T = TEXT[lang]
    search = (tool["title"][lang] + " " + tool["short"][lang] + " " + " ".join(tool.get("keywords", {}).get(lang, []))).lower()
    return '<a class="card" href="%s%s" data-search="%s"><div class="ic">%s</div><b>%s</b><span>%s</span></a>' % (
        rel, tool_url(tool, lang), esc(search), tool["icon"], esc(tool["title"][lang]), esc(tool["short"][lang]))


def build_home(lang, all_tools):
    T = TEXT[lang]
    rel = "../"
    sections = []
    for cat in CAT_ORDER:
        items = [t for t in all_tools if t["cat"] == cat and t.get("home", True)]
        if not items:
            continue
        icon, name = T["cats"][cat]
        sections.append('<section class="cat" id="cat-%s"><h2><span>%s</span> %s</h2><div class="grid">%s</div></section>' % (
            cat, icon, esc(name), "".join(card(t, lang, rel) for t in items)))
    why = "".join('<div class="stat"><b style="font-size:1.05rem">%s</b><span>%s</span></div>' % (esc(a), esc(b)) for a, b in T["why"])
    body = f"""
<main class="container">
<section class="hero">
<h1>{esc(T['home_h1'])}</h1>
<p>{esc(T['home_sub'])}</p>
<div class="search">{SEARCH_SVG}<input id="tool-search" type="search" placeholder="{esc(T['search_ph'])}" aria-label="{esc(T['search_ph'])}" autocomplete="off"></div>
</section>
{''.join(sections)}
<p class="empty">{esc(T['search_empty'])}</p>
<section class="cat"><h2>{esc(T['why_title'])}</h2><div class="stats">{why}</div></section>
<section class="article"><h2>{esc(T['home_seo_title'])}</h2><p>{T['home_seo']}</p></section>
</main>"""
    jsonld = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": DOMAIN + "/" + lang + "/", "inLanguage": lang}
    alternates = {l: l + "/" for l in LANGS}
    alternates["x-default"] = ""
    page = layout(lang, title=T["home_title"], meta=T["home_meta"], canonical_path=lang + "/", alternates=alternates,
                  body=body, rel=rel, jsonld=jsonld)
    write(lang + "/index.html", page)


def tool_strings(tool, lang):
    T = TEXT[lang]
    S = {k: T[k] for k in ("copy", "copied", "download", "reset", "calculate", "result", "invalid")}
    S.update(tool["strings"][lang])
    return S


def render_ui(tool, lang):
    S = tool_strings(tool, lang)
    def sub(m):
        key = m.group(1)
        if key not in S:
            raise KeyError("Missing string '%s' for tool %s (%s)" % (key, tool["id"], lang))
        return S[key]
    return re.sub(r"\{\{(\w+)\}\}", sub, tool["ui"])


def build_tool(tool, lang, all_tools):
    T = TEXT[lang]
    rel = "../../"
    cat_icon, cat_name = T["cats"][tool["cat"]]
    ui = render_ui(tool, lang)
    faq_html = ""
    faq = tool.get("faq", {}).get(lang) or []
    if faq:
        faq_html = '<h2>%s</h2><div class="faq">%s</div>' % (esc(T["faq"]), "".join(
            '<details><summary>%s</summary><p>%s</p></details>' % (esc(q), a) for q, a in faq))
    pool = [t for t in all_tools if t.get("home", True)]
    related = [t for t in pool if t["cat"] == tool["cat"] and t["id"] != tool["id"]]
    if len(related) < 3:
        related += [t for t in pool if t["cat"] != tool["cat"]][: 3 - len(related)]
    related_html = '<section class="related"><h2>%s</h2><div class="grid">%s</div></section>' % (
        esc(T["related"]), "".join(card(t, lang, rel) for t in related[:4]))
    strings = tool_strings(tool, lang)
    scripts = '<script>var T=%s;</script>\n' % json.dumps(strings, ensure_ascii=False)
    for extra in tool.get("libs", []):
        scripts += '<script src="%sassets/%s?v=%s"></script>\n' % (rel, extra, VERSION)
    scripts += "<script>\n(function(){\n%s\n})();\n</script>" % tool["js"]
    body = f"""
<main class="container">
<nav class="crumbs"><a href="{rel}{lang}/">{esc(T['home'])}</a> › <a href="{rel}{lang}/#cat-{tool['cat']}">{cat_icon} {esc(cat_name)}</a></nav>
<h1>{esc(tool['title'][lang])}</h1>
<p class="lead">{esc(tool['intro'][lang])}</p>
<!-- AD:top -->
<section class="tool" id="tool" aria-label="{esc(tool['title'][lang])}">
{ui}
</section>
<p class="msg">🔒 {esc(T['privacy_blurb'])}</p>
<article class="article">
{tool['article'][lang]}
{faq_html}
</article>
<!-- AD:bottom -->
{related_html}
</main>"""
    jsonld = [{
        "@context": "https://schema.org", "@type": "WebApplication", "name": tool["title"][lang],
        "url": "%s/%s" % (DOMAIN, tool_url(tool, lang)), "description": tool["meta"][lang],
        "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
        "inLanguage": lang, "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
    }]
    if faq:
        jsonld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]})
    alternates = {l: tool_url(tool, l) for l in LANGS}
    alternates["x-default"] = tool_url(tool, "en")
    # seo_title (optional): used only for <title>/og:title, so that the page can carry the
    # exact wording people search for without changing the H1 or the cards on the home page.
    seo = (tool.get("seo_title") or {}).get(lang)
    title = seo if seo else "%s – %s" % (tool["title"][lang], SITE_NAME)
    page = layout(lang, title=title, meta=tool["meta"][lang], canonical_path=tool_url(tool, lang), alternates=alternates,
                  body=body, rel=rel, scripts=scripts, jsonld=jsonld)
    write(tool_url(tool, lang) + "index.html", page)


def build_static(key, lang):
    T = TEXT[lang]
    rel = "../../"
    P = PAGES[key][lang]
    body = f"""
<main class="container">
<nav class="crumbs"><a href="{rel}{lang}/">{esc(T['home'])}</a> › {esc(P['title'])}</nav>
<h1>{esc(P['title'])}</h1>
<article class="article">{P['html']}</article>
</main>"""
    alternates = {l: static_url(key, l) for l in LANGS}
    alternates["x-default"] = static_url(key, "en")
    page = layout(lang, title="%s – %s" % (P["title"], SITE_NAME), meta=P["meta"], canonical_path=static_url(key, lang),
                  alternates=alternates, body=body, rel=rel)
    write(static_url(key, lang) + "index.html", page)


def build_root():
    # Language chooser / redirect
    it, en = TEXT["it"], TEXT["en"]
    body = f"""
<main class="container" style="text-align:center;padding-top:60px">
<h1>{SITE_NAME}</h1>
<p class="lead">{esc(it['tagline'])} · {esc(en['tagline'])}</p>
<p class="btns" style="justify-content:center"><a class="btn primary" href="it/" data-setlang="it">Italiano</a> <a class="btn" href="en/" data-setlang="en">English</a></p>
</main>
<script>
(function(){{
  try {{
    var pref = localStorage.getItem('rt-lang');
    if (!pref) {{ var nl = (navigator.languages && navigator.languages[0]) || navigator.language || 'en'; pref = /^it/i.test(nl) ? 'it' : 'en'; }}
    if (pref === 'it' || pref === 'en') location.replace(pref + '/');
  }} catch (e) {{ location.replace('en/'); }}
}})();
</script>"""
    alternates = {l: l + "/" for l in LANGS}
    alternates["x-default"] = ""
    page = layout("en", title="%s – %s" % (SITE_NAME, en["tagline"]), meta=en["home_meta"], canonical_path="",
                  alternates=alternates, body=body, rel="")
    write("index.html", page)
    # 404
    body = f"""
<main class="container" style="text-align:center;padding-top:60px">
<h1>404</h1>
<p class="lead">{esc(it['not_found_text'])}<br>{esc(en['not_found_text'])}</p>
<p class="btns" style="justify-content:center"><a class="btn primary" href="/it/">{esc(it['go_home'])}</a> <a class="btn" href="/en/">{esc(en['go_home'])}</a></p>
</main>"""
    page = layout("en", title="404 – %s" % SITE_NAME, meta=en["not_found_text"], canonical_path="404.html", alternates={},
                  body=body, rel="/", noindex=True)
    write("404.html", page)


def build_sitemap(all_tools):
    urls = []  # (path, alternates dict)
    urls.append(("", {l: l + "/" for l in LANGS}))
    for lang in LANGS:
        urls.append((lang + "/", {l: l + "/" for l in LANGS}))
        for t in all_tools:
            urls.append((tool_url(t, lang), {l: tool_url(t, l) for l in LANGS}))
        for k in STATIC_SLUGS:
            urls.append((static_url(k, lang), {l: static_url(k, l) for l in LANGS}))
    seen = set()
    entries = []
    for path, alts in urls:
        if path in seen:
            continue
        seen.add(path)
        links = "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s/%s"/>' % (l, DOMAIN, p) for l, p in alts.items())
        entries.append("<url><loc>%s/%s</loc><lastmod>%s</lastmod>%s</url>" % (DOMAIN, path, LASTMOD, links))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n%s\n</urlset>\n' % "\n".join(entries))
    write("sitemap.xml", xml)
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMAIN)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, "assets"), os.path.join(OUT, "assets"))
    all_tools = tools.load()
    ids = [t["id"] for t in all_tools]
    assert len(ids) == len(set(ids)), "duplicate tool ids"
    for lang in LANGS:
        build_home(lang, all_tools)
        for t in all_tools:
            build_tool(t, lang, all_tools)
        for k in STATIC_SLUGS:
            build_static(k, lang)
    build_root()
    build_sitemap(all_tools)
    # .nojekyll so GitHub Pages serves files as-is
    write(".nojekyll", "")
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print("Built %d tools x %d languages, %d files in %s" % (len(all_tools), len(LANGS), n, OUT))


if __name__ == "__main__":
    main()

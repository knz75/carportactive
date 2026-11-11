# python build.py --preview      podgląd kolejki w /podglad/ (noindex, bez sitemap)
# python build.py --publish 5    wydaje 5 artykułów z kolejki i przebudowuje stronę
# python build.py                tylko przebudowa (np. po zmianie szablonu)
import json, os, sys, glob, html, shutil, argparse, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(os.path.dirname(HERE), "static")
KOLEJKA = os.path.join(HERE, "kolejka")
WYDANE = os.path.join(HERE, "wydane")
SITE = "https://carportactive.pl"
FACTS = json.load(open(os.path.join(HERE, "facts.json"), encoding="utf-8"))
BASE_URLS = ["/", "/ai/", "/moduly/sportowy/", "/moduly/panel-narzedziowy/", "/moduly/ogrod-wertykalny/",
             "/moduly/plac-zabaw/", "/moduly/przechowalnia-rowerow/", "/moduly/solar-box/", "/dodatki/ca-stand/"]

def e(s): return html.escape(s, quote=True)

def load(d):
    out = [json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(d, "*.json"))]
    return out

HEAD = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;700&family=Barlow+Condensed:wght@700;800&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/css/pages.css">'''

NAV = '''<header class="top-nav">
  <a href="/" class="brand-logo">Carport<span>Active</span></a>
  <nav class="nav-links" aria-label="Główna nawigacja">
    <a href="/#moduly">Moduły</a>
    <a href="/poradnik/">Poradnik</a>
    <a href="/ai/">Wizualizacja AI</a>
    <a href="/#kontakt">Wycena</a>
  </nav>
</header>'''

FOOT = '''<footer>
  <div class="footer-brand">Carport<span>Active</span></div>
  <div class="footer-copy">© 2026 CarportActive - stalowe wiaty modułowe S235 - Polska</div>
  <div class="footer-links">
    <a href="/">Strona główna</a>
    <a href="/poradnik/">Poradnik</a>
    <a href="/ai/">Wizualizacja AI</a>
    <a href="/#kontakt">Kontakt</a>
  </div>
</footer>
<a class="ai-float" href="/ai/" aria-label="Zobacz wiatę na swoim podwórku - wizualizacja AI">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 8h3l2-3h8l2 3h3v12H3z"/><circle cx="12" cy="13" r="4"/></svg>
  Twoja wiata AI
</a>'''

def article(a, related, base, noindex):
    f = FACTS[a["link"]]
    url = f"{SITE}{base}{a['adres']}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": a["tytul"], "description": a["opis_meta"], "inLanguage": "pl",
         "datePublished": a.get("wydano", a["wygenerowano"]), "author": {"@type": "Organization", "name": "CarportActive"},
         "publisher": {"@type": "Organization", "name": "CarportActive"}, "mainEntityOfPage": url},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CarportActive", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Poradnik", "item": SITE + "/poradnik/"},
            {"@type": "ListItem", "position": 3, "name": a["tytul"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["pytanie"],
            "acceptedAnswer": {"@type": "Answer", "text": q["odpowiedz"]}} for q in a["faq"]]}]}
    body = "\n".join(f"<h2>{e(s['h2'])}</h2>\n" + "\n".join(f"<p>{e(p)}</p>" for p in s["akapity"]) for s in a["sekcje"])
    faq = "\n".join(f'<details class="faq-item"><summary>{e(q["pytanie"])}</summary><p>{e(q["odpowiedz"])}</p></details>' for q in a["faq"])
    rel = ""
    if related:
        rel = '<section class="sec sec-light"><div class="sec-inner"><h2>Podobne porady</h2><ul class="related">' + \
              "".join(f'<li><a href="{base}{r["adres"]}/">{e(r["tytul"])}</a></li>' for r in related) + "</ul></div></section>"
    robots = "noindex, nofollow" if noindex else "index, follow"
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(a["tytul"])} | CarportActive</title>
<meta name="description" content="{e(a["opis_meta"])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(a["tytul"])}">
<meta property="og:description" content="{e(a["opis_meta"])}">
<meta property="og:image" content="{SITE}{f["img"]}">
<meta property="og:locale" content="pl_PL">
{HEAD}
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
</head>
<body>
{NAV}
<main>
<nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a><span>/</span><a href="/poradnik/">Poradnik</a></nav>
<section class="art-head"><div class="art-head-inner">
<h1>{e(a["tytul"])}</h1>
<p class="art-lead">{e(a["wstep"])}</p>
</div></section>
<div class="art-wrap">
<article class="art-body">
{body}
</article>
<aside class="solution">
<img src="{f["img"]}" alt="{e(f["h1"])}" width="440" height="360" loading="lazy" decoding="async">
<div class="solution-text">
<h2>{e(f["h1"])}</h2>
<p>{e(a["rozwiazanie"])}</p>
<div class="p-actions"><a class="btn btn-green" href="{f["url"]}">Zobacz {e(f["name"].lower())}</a><a class="btn btn-line" href="{f["url"]}#kontakt">Zapytaj o wycenę</a></div>
</div>
</aside>
</div>
<section class="sec"><div class="sec-inner"><h2>Pytania</h2>
{faq}
</div></section>
{rel}
</main>
{FOOT}
</body>
</html>
'''

def index_page(arts, base, noindex):
    groups = {}
    for a in arts: groups.setdefault(a["link"], []).append(a)
    parts = []
    for k, items in groups.items():
        f = FACTS[k]
        parts.append(f'<div class="idx-group"><h2><a href="{f["url"]}">{e(f["name"])}</a></h2><ul class="related">' +
                     "".join(f'<li><a href="{base}{a["adres"]}/">{e(a["tytul"])}</a></li>' for a in items) + "</ul></div>")
    robots = "noindex, nofollow" if noindex else "index, follow"
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Poradnik - wiata, ogród, narzędzia, rowery | CarportActive</title>
<meta name="description" content="Praktyczne porady: jak przechowywać narzędzia, rowery i drewno, jak urządzić podjazd, kącik do ćwiczeń i plac zabaw przy domu.">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{SITE}{base}">
{HEAD}
</head>
<body>
{NAV}
<main>
<nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a><span>/</span>Poradnik</nav>
<section class="art-head"><div class="art-head-inner"><h1>Poradnik</h1>
<p class="art-lead">Praktyczne porady o podjeździe, ogrodzie i przechowywaniu rzeczy przy domu.</p></div></section>
<section class="sec"><div class="sec-inner">
{"".join(parts)}
</div></section>
</main>
{FOOT}
</body>
</html>
'''

def render(arts, folder, base, noindex):
    out = os.path.join(STATIC, folder)
    if os.path.isdir(out): shutil.rmtree(out)
    os.makedirs(out)
    arts = sorted(arts, key=lambda a: (a.get("wydano", ""), a["nr"]), reverse=True)
    for a in arts:
        rel = [r for r in arts if r["link"] == a["link"] and r is not a][:4]
        d = os.path.join(out, a["adres"]); os.makedirs(d)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(article(a, rel, base, noindex))
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(index_page(arts, base, noindex))
    return arts

def update_module_pages(arts):
    for k, f in FACTS.items():
        p = os.path.join(STATIC, f["url"].strip("/"), "index.html")
        if not os.path.exists(p): continue
        s = open(p, encoding="utf-8").read()
        a0, a1 = "<!--PORADNIKI:START-->", "<!--PORADNIKI:END-->"
        if a0 not in s or a1 not in s: continue
        items = [a for a in arts if a["link"] == k][:10]
        block = ""
        if items:
            block = '\n<section class="sec"><div class="sec-inner"><h2>Poradnik</h2><ul class="guides">' + \
                    "".join(f'<li><a href="/poradnik/{a["adres"]}/">{e(a["tytul"])}</a></li>' for a in items) + "</ul></div></section>\n"
        s = s[:s.index(a0) + len(a0)] + block + s[s.index(a1):]
        open(p, "w", encoding="utf-8").write(s)

def sitemap(arts):
    today = datetime.date.today().isoformat()
    rows = [f"  <url><loc>{SITE}{u}</loc></url>" for u in BASE_URLS]
    if arts:
        rows.append(f"  <url><loc>{SITE}/poradnik/</loc><lastmod>{today}</lastmod></url>")
        rows += [f"  <url><loc>{SITE}/poradnik/{a['adres']}/</loc><lastmod>{a['wydano']}</lastmod></url>" for a in arts]
    open(os.path.join(STATIC, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--publish", type=int, default=0)
    a = ap.parse_args()
    if a.preview:
        q = load(KOLEJKA)
        render(q, "podglad", "/podglad/", True)
        print("podgląd:", len(q), "artykułów -> https://carportactive.pl/podglad/")
        return
    os.makedirs(WYDANE, exist_ok=True)
    if a.publish:
        q = sorted(load(KOLEJKA), key=lambda x: x.get("kolejnosc", x["nr"]))
        today = datetime.date.today().isoformat()
        for x in q[:a.publish]:
            x["wydano"] = today
            json.dump(x, open(os.path.join(WYDANE, x["adres"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.remove(os.path.join(KOLEJKA, x["adres"] + ".json"))
            print("wydano:", x["adres"])
    arts = load(WYDANE)
    if arts:
        arts = render(arts, "poradnik", "/poradnik/", False)
    update_module_pages(arts)
    sitemap(arts)
    print("na stronie:", len(arts), "| w kolejce:", len(load(KOLEJKA)))

if __name__ == "__main__":
    main()

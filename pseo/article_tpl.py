from layout import *

def article_html(a, f, related, base="/poradnik/", robots="index, follow"):
    url = f"{SITE}{base}{a['adres']}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": a["tytul"], "description": a["opis_meta"], "inLanguage": "pl",
         "datePublished": a.get("wydano", a.get("wygenerowano", "")), "author": {"@type": "Organization", "name": "CarportActive"},
         "publisher": {"@type": "Organization", "name": "CarportActive"}, "mainEntityOfPage": url},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CarportActive", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Poradnik", "item": SITE + "/poradnik/"},
            {"@type": "ListItem", "position": 3, "name": a["tytul"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["pytanie"],
            "acceptedAnswer": {"@type": "Answer", "text": q["odpowiedz"]}} for q in a["faq"]]}]}
    body_html = "\n".join(f"<h2>{e(s['h2'])}</h2>\n" + "\n".join(f"<p>{e(p)}</p>" for p in s["akapity"]) for s in a["sekcje"])
    faq = "\n".join(f'<details class="faq-item"><summary>{e(q["pytanie"])}</summary><p>{e(q["odpowiedz"])}</p></details>' for q in a["faq"])
    rel = ""
    if related:
        rel = '<section class="art-sec sec-paper"><div class="wrap-narrow"><h2>Podobne porady</h2><ul class="link-list">' + \
              "".join(f'<li><a href="{base}{r["adres"]}/">{e(r["tytul"])}</a></li>' for r in related) + "</ul></div></section>"
    body = f'''{header("poradnik")}
<main>
<section class="art-head">
  <div class="wrap-narrow">
    <nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a> / <a href="/poradnik/">Poradnik</a></nav>
    <h1>{e(a["tytul"])}</h1>
    <p class="art-lead">{e(a["wstep"])}</p>
  </div>
</section>
<div class="wrap-narrow">
  <article class="art-body">
{body_html}
  </article>
  <aside class="solution">
    <img src="{f["img"]}" alt="{e(f["h1"])}" width="480" height="400" loading="lazy" decoding="async">
    <div class="solution-text">
      <h2>{e(f["h1"])}</h2>
      <p>{e(a["rozwiazanie"])}</p>
      <div class="actions"><a class="btn btn-green btn-small" href="{f["url"]}">Zobacz szczegóły</a><a class="btn btn-outline btn-small" href="{f["url"]}#kontakt">Zapytaj o wycenę</a></div>
    </div>
  </aside>
</div>
<section class="art-sec">
  <div class="wrap-narrow">
    <h2>Pytania</h2>
{faq}
  </div>
</section>
{rel}
</main>
{FOOTER}'''
    return page(a["tytul"] + " | CarportActive", a["opis_meta"], url, body, robots=robots, og_image=f["img"], og_type="article", ld=ld)

def index_html(arts, facts, base="/poradnik/", robots="index, follow"):
    groups = {}
    for a in arts: groups.setdefault(a["link"], []).append(a)
    parts = "".join(f'<div style="margin-bottom:40px"><h2 style="font-size:30px;margin-bottom:12px"><a href="{facts[k]["url"]}" style="color:inherit;text-decoration:none">{e(facts[k]["name"])}</a></h2><ul class="link-list">' +
                    "".join(f'<li><a href="{base}{a["adres"]}/">{e(a["tytul"])}</a></li>' for a in items) + "</ul></div>" for k, items in groups.items())
    body = f'''{header("poradnik")}
<main>
<section class="art-head">
  <div class="wrap-narrow">
    <nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a> / Poradnik</nav>
    <h1>Poradnik</h1>
    <p class="art-lead">Praktyczne porady o podjeździe, ogrodzie i przechowywaniu rzeczy przy domu.</p>
  </div>
</section>
<section class="art-sec"><div class="wrap-narrow">
{parts}
</div></section>
</main>
{FOOTER}'''
    return page("Poradnik - wiata, ogród, narzędzia, rowery | CarportActive",
                "Praktyczne porady: jak przechowywać narzędzia, rowery i drewno, jak urządzić podjazd, kącik do ćwiczeń i plac zabaw przy domu.",
                SITE + base, body, robots=robots)

def home_guides(arts):
    if not arts: return ""
    return ('\n<section class="sec sec-paper"><div class="wrap"><div class="narrow"><h2 class="sec-title">Poradnik</h2>'
            '<p class="sec-intro">Praktyczne porady o podjeździe, ogrodzie i przechowywaniu rzeczy przy domu.</p><ul class="link-list">' +
            "".join(f'<li><a href="/poradnik/{a["adres"]}/">{e(a["tytul"])}</a></li>' for a in arts[:6]) +
            '</ul><p style="margin-top:20px"><a href="/poradnik/" style="font-weight:600">Wszystkie porady</a></p></div></div></section>\n')

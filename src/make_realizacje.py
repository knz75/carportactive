import os
from layout import *

# (plik, podpis, slug strony realizacji lub None)
ALL = [
 ("r01-wiata-przesla-orzech", "Wiata dwustanowiskowa z przęsłami żaluzjowymi w kolorze orzech", None),
 ("r03-wiata-przesla-ciemny-orzech", "Wiata dwustanowiskowa z przęsłami w kolorze ciemny orzech - Serock", "wiata-serock"),
 ("r02-wiata-orzech-przy-domu", "Wiata przy domu z przęsłami w kolorze orzech", None),
 ("r13-przeslo-orzech-przy-domu", "Przęsło orzech przy wiacie i dopasowana osłona na ścianie domu", None),
 ("r04-wiata-przy-garazu", "Wiata dobudowana do garażu - Otwock Mały", "wiata-otwock-maly"),
 ("r05-wiata-z-oswietleniem", "Wiata na kampera przy garażu z oświetleniem - Chrzanów Mały", "wiata-chrzanow-maly"),
 ("r06-wiata-wielostanowiskowa", "Wiata wielostanowiskowa dla karetek - Warszawa", "wiata-warszawa"),
 ("r08-wiata-wzdluz-sciany", "Wiata wzdłuż ściany budynku - Żyrardów", "wiata-zyrardow"),
 ("r07-wiata-nad-wjazdem", "Wiata nad wjazdem od strony ulicy", None),
 ("r09-schowek-pod-wiata", "Wiata z zamykanym schowkiem - Piskórka", "wiata-piskorka"),
 ("r10-zabudowa-boczna", "Pełna zabudowa boczna wiaty - Piskórka", "wiata-piskorka"),
 ("r11-wiata-przeszklona", "Wiata z przeszkleniem i bramą garażową - Konstancin-Jeziorna", "wiata-konstancin-jeziorna"),
 ("r12-wiata-przeszklona-detal", "Przeszklona wiata z bliska - Konstancin-Jeziorna", "wiata-konstancin-jeziorna"),
 ("z03-wiata-zamknieta-z-brama-segmentowa", "Zamknięta wiata z bramą segmentową i ścianą z żaluzji", None),
 ("z02-wiata-przelotowa-dwie-bramy", "Wiata przelotowa z bramą z przodu i z tyłu", None),
 ("r14-zadaszenie-tarasu", "Zadaszenie tarasu w kolorze dopasowanym do domu", None),
]

CASES = [
 dict(slug="wiata-warszawa", town="Warszawa", h1="Wiata wielostanowiskowa dla karetek - Warszawa",
      lead="Wiata na kilka pojazdów służbowych - karetek pogotowia - ze ścianą tylną i boczną z przęseł żaluzjowych.",
      imgs=["r06-wiata-wielostanowiskowa"],
      done=["Długa wiata na kilka stanowisk dla karetek pogotowia", "Konstrukcja stalowa w kolorze antracyt RAL 7016", "Dach z blachy trapezowej", "Ściana tylna i boczna z przęseł żaluzjowych w kolorze antracyt"],
      module=("/moduly/przeslo-zaluzjowe/", "Przęsło żaluzjowe")),
 dict(slug="wiata-piskorka", town="Piskórka", h1="Wiata z zamykanym schowkiem - Piskórka",
      lead="Wiata z pełną zabudową ściany i zamykanym schowkiem z drzwiami pod tym samym dachem.",
      imgs=["r09-schowek-pod-wiata", "r10-zabudowa-boczna"],
      done=["Zamykany schowek z drzwiami pod wiatą", "Pełna zabudowa boczna w kolorze antracyt", "Oświetlenie pod dachem", "Rynny i odprowadzenie wody"],
      module=("/moduly/przechowalnia-rowerow/", "Przechowalnia rowerów i zamknięta strefa")),
 dict(slug="wiata-serock", town="Serock", h1="Wiata z przęsłami ciemny orzech - Serock",
      lead="Wiata dwustanowiskowa z płaskim dachem, osłonięta z boku i z tyłu przęsłami w kolorze ciemny orzech.",
      imgs=["r03-wiata-przesla-ciemny-orzech"],
      done=["Wiata dwustanowiskowa z płaskim dachem", "Konstrukcja w kolorze antracyt RAL 7016", "Przęsła żaluzjowe w kolorze ciemny orzech z boku i z tyłu", "Rynna i rura spustowa przy słupie"],
      module=("/moduly/przeslo-zaluzjowe/", "Przęsło żaluzjowe")),
 dict(slug="wiata-otwock-maly", town="Otwock Mały", h1="Wiata dobudowana do garażu - Otwock Mały",
      lead="Wiata przy domu, dostawiona do bryły garażu, z boczną ścianą z przęseł żaluzjowych.",
      imgs=["r04-wiata-przy-garazu"],
      done=["Wiata dostawiona do garażu przy domu", "Konstrukcja w kolorze antracyt RAL 7016", "Boczna ściana z przęseł żaluzjowych w kolorach antracyt i orzech"],
      module=("/moduly/przeslo-zaluzjowe/", "Przęsło żaluzjowe")),
 dict(slug="wiata-chrzanow-maly", town="Chrzanów Mały", h1="Wiata na kampera przy garażu - Chrzanów Mały",
      lead="Długa wiata obok garażu, pod którą mieści się kamper, z pełną ścianą boczną i tylną oraz oświetleniem pod dachem.",
      imgs=["r05-wiata-z-oswietleniem"],
      done=["Długa wiata dostawiona do garażu, wysokość dopasowana do kampera", "Ściana tylna i boczna z przęseł w ciemnym kolorze", "Oświetlenie pod dachem", "Konstrukcja w kolorze antracyt RAL 7016"],
      module=("/moduly/przeslo-zaluzjowe/", "Przęsło żaluzjowe")),
 dict(slug="wiata-konstancin-jeziorna", town="Konstancin-Jeziorna", h1="Przeszklona wiata garażowa - Konstancin-Jeziorna",
      lead="Wiata z przeszklonymi ścianami, bramą segmentową i lampami na słupach.",
      imgs=["r11-wiata-przeszklona", "r12-wiata-przeszklona-detal"],
      done=["Wiata z płaskim dachem na dwa stanowiska", "Ściany z przeszkleń", "Brama segmentowa od frontu", "Lampy na słupach konstrukcji"],
      module=None),
 dict(slug="wiata-zyrardow", town="Żyrardów", h1="Wiata wzdłuż ściany budynku - Żyrardów",
      lead="Wiata z płaskim dachem postawiona wzdłuż ściany budynku, na rzędzie słupów.",
      imgs=["r08-wiata-wzdluz-sciany"],
      done=["Wiata wzdłuż ściany budynku", "Płaski dach", "Konstrukcja w kolorze antracyt RAL 7016"],
      module=None),
]

CAPTION = {f: c for f, c, s in ALL}

def contact(town):
    return f'''<section class="sec sec-dark" id="kontakt">
  <div class="wrap contact-grid">
    <div>
      <h2 class="sec-title">Chcesz podobną wiatę?</h2>
      <p class="sec-intro">Montujemy w całej Polsce, także w okolicy miejscowości {e(town)}. Napisz, jaki rozmiar Cię interesuje i gdzie ma stanąć wiata. Odezwiemy się w ciągu 24 godzin.</p>
      <p style="color:#aab1b8">Masz zdjęcie podjazdu? <a href="/ai/" style="color:var(--green-hi)">Wizualizator AI pokaże wiatę na Twoim podwórku w 3 wariantach.</a></p>
    </div>
    <div>
    {form(MODULE_OPTIONS, placeholder=f"Wymiary (np. 4x6 m), miejscowość, pytania", button="Wyślij zapytanie o wycenę")}
    </div>
  </div>
</section>'''

def case_page(c):
    url = f"{SITE}/realizacje/{c['slug']}/"
    figs = "\n".join(f'      <figure><a href="/img/realizacje/{f}.jpg"><img src="/img/realizacje/{f}.jpg" alt="{e(CAPTION[f])}" width="1200" height="900" decoding="async"></a><figcaption>{e(CAPTION[f])}</figcaption></figure>' for f in c["imgs"])
    done = "\n".join(f"      <li>{e(x)}</li>" for x in c["done"])
    mod = f'\n    <p class="note">Zobacz więcej o tym rozwiązaniu: <a href="{c["module"][0]}">{e(c["module"][1])}</a>.</p>' if c["module"] else ""
    others = "".join(f'<li><a href="/realizacje/{o["slug"]}/">{e(o["h1"])}</a></li>' for o in CASES if o is not c)
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "CarportActive", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Realizacje", "item": SITE + "/realizacje/"},
        {"@type": "ListItem", "position": 3, "name": c["h1"], "item": url}]}
    body = f'''{header("realizacje")}
<main>
<section class="art-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a> / <a href="/realizacje/">Realizacje</a> / {e(c["town"])}</nav>
    <h1>{e(c["h1"])}</h1>
    <p class="art-lead" style="max-width:720px">{e(c["lead"])}</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="works case-photos">
{figs}
    </div>
  </div>
</section>
<section class="sec sec-zinc">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Co zrobiliśmy</h2>
    <ul class="problems">
{done}
    </ul>{mod}
  </div></div>
</section>
<section class="sec">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Inne realizacje</h2>
    <ul class="link-list">{others}<li><a href="/realizacje/">Wszystkie realizacje</a></li></ul>
  </div></div>
</section>
{contact(c["town"])}
</main>
{FOOTER}
{FORM_JS}'''
    return page(f'{c["h1"]} | CarportActive', f'{c["lead"]} Realizacja CarportActive, miejscowość {c["town"]}.', url, body,
                og_image=f'/img/realizacje/{c["imgs"][0]}.jpg', ld=ld)

def index_page():
    def fig(f, cap, slug):
        img = f'<img src="/img/realizacje/{f}.jpg" alt="{e(cap)}" width="800" height="600" loading="lazy" decoding="async">'
        link = f"/realizacje/{slug}/" if slug else f"/img/realizacje/{f}.jpg"
        return f'      <figure><a href="{link}">{img}</a><figcaption>{e(cap)}</figcaption></figure>'
    figs = "\n".join(fig(f, c, s) for f, c, s in ALL)
    towns = "".join(f'<li><a href="/realizacje/{c["slug"]}/">{e(c["h1"])}</a></li>' for c in CASES)
    body = f'''{header("realizacje")}
<main>
<section class="art-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a> / Realizacje</nav>
    <h1>Nasze realizacje</h1>
    <p class="art-lead" style="max-width:720px">Wiaty, które postawiliśmy u klientów: przy domu, przy garażu, nad wjazdem i na tarasie. Konstrukcja w kolorze antracyt RAL 7016, przęsła w kolorze orzech, ciemny orzech albo antracyt.</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="works">
{figs}
    </div>
  </div>
</section>
<section class="sec sec-zinc">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Realizacje według miejscowości</h2>
    <ul class="link-list">{towns}</ul>
  </div></div>
</section>
{contact("Twojej")}
</main>
{FOOTER}
{FORM_JS}'''
    body = body.replace("także w okolicy miejscowości Twojej.", "także w Twojej okolicy.")
    return page("Realizacje - stalowe wiaty garażowe i przęsła żaluzjowe | CarportActive",
                "Zdjęcia wiat CarportActive u klientów: Warszawa, Serock, Konstancin-Jeziorna, Otwock Mały, Żyrardów i okolice. Przęsła żaluzjowe, wiaty wielostanowiskowe, zadaszenie tarasu.",
                SITE + "/realizacje/", body, og_image="/img/realizacje/r01-wiata-przesla-orzech.jpg")

if __name__ == "__main__":
    os.makedirs("static/realizacje", exist_ok=True)
    open("static/realizacje/index.html", "w", encoding="utf-8").write(index_page())
    for c in CASES:
        d = f"static/realizacje/{c['slug']}"; os.makedirs(d, exist_ok=True)
        open(f"{d}/index.html", "w", encoding="utf-8").write(case_page(c))
    print("ok", len(CASES))

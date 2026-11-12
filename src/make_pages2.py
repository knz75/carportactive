import os
from layout import *
from make_moduly import M

def module_page(m):
    url = f"{SITE}/moduly/{m['slug']}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CarportActive", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Moduły", "item": SITE + "/#moduly"},
            {"@type": "ListItem", "position": 3, "name": m["name"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in m["faq"]]}]}
    problems = "\n".join(f"      <li>{e(p)}</li>" for p in m["problems"])
    parts = "\n".join(f'      <div class="part"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in m["parts"])
    faq = "\n".join(f'    <details class="faq-item"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in m["faq"])
    others = "\n".join(f'      <a class="tile" href="/moduly/{o["slug"]}/"><img src="/img/{o["img"]}" alt="{e(o["alt"])}" width="400" height="300" loading="lazy" decoding="async"><h3>{e(o["name"])}</h3></a>' for o in M if o is not m)
    gal = ""
    if m.get("gallery"):
        gal = '\n<section class="sec sec-zinc">\n  <div class="wrap">\n    <h2 class="sec-title">Nasze realizacje</h2>\n    <div class="works">\n' + "\n".join(
            f'      <figure><img src="/img/{g}" alt="{e(c)}" width="800" height="600" loading="lazy" decoding="async"><figcaption>{e(c)}</figcaption></figure>' for g, c in m["gallery"]) + \
            '\n    </div>\n    <p style="margin-top:20px"><a href="/realizacje/" style="font-weight:600">Wszystkie realizacje</a></p>\n  </div>\n</section>\n'
    extra = ""
    if m["slug"] == "panel-narzedziowy":
        extra = '\n    <p class="note">Nie masz wiaty albo potrzebujesz miejsca na narzędzia przy drzwiach lub na tarasie? Zobacz wolnostojące <a href="/dodatki/ca-stand/">stojaki na narzędzia CA-Stand</a> w tym samym stylu.</p>'
    body = f'''{header("moduly")}
<main>
<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a> / <a href="/#moduly">Moduły</a> / {e(m["name"])}</nav>
    <div>
      <p class="kicker">{e(m["cat"])}</p>
      <h1>{e(m["h1"])}</h1>
      <p class="lead">{e(m["lead"])}</p>
      <div class="actions">
        <a class="btn btn-green" href="#kontakt">Zapytaj o wycenę</a>
        <a class="btn btn-ghost" href="/ai/">Zobacz wiatę na swoim podwórku (AI)</a>
      </div>
    </div>
    <img src="/img/{m["img"]}" alt="{e(m["alt"])}" width="800" height="600" decoding="async" fetchpriority="high">
  </div>
</section>

<section class="sec">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Kiedy to się przydaje</h2>
    <ul class="problems">
{problems}
    </ul>
    <p class="answer">{e(m["answer"])}</p>
  </div></div>
</section>

<section class="sec sec-zinc">
  <div class="wrap">
    <h2 class="sec-title">Co wchodzi w skład</h2>
    <div class="parts">
{parts}
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap"><div class="narrow text-block">
    <h2 class="sec-title">Jak to działa z wiatą</h2>
    <p>Moduł mocujemy do słupów wiaty ze stali konstrukcyjnej S235. Słupy i fundament mają zapas nośności i przygotowane punkty montażowe, więc moduł możesz zamówić razem z wiatą albo dołożyć za rok, bez przeróbek i cięcia stali.</p>
    <p>Całość jest ocynkowana ogniowo i malowana proszkowo. Wiatę montujemy na stopach fundamentowych albo na istniejącej płycie lub kostce, a sam montaż zajmuje zazwyczaj 1 dzień roboczy.</p>
    <p class="note">{e(m["size"])} <a href="/#wymiary">Zobacz wymiary wiat</a></p>{extra}
  </div></div>
</section>

{gal}
<!--PORADNIKI:START-->
<!--PORADNIKI:END-->

<section class="sec">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Pytania</h2>
{faq}
  </div></div>
</section>

<section class="sec sec-zinc">
  <div class="wrap">
    <h2 class="sec-title">Inne moduły</h2>
    <div class="tiles-small">
{others}
    </div>
  </div>
</section>

<section class="sec sec-dark" id="kontakt">
  <div class="wrap contact-grid">
    <div>
      <h2 class="sec-title">Zapytaj o wiatę z tym modułem</h2>
      <p class="sec-intro">Napisz, jaki rozmiar Cię interesuje i gdzie ma stanąć wiata. Odezwiemy się w ciągu 24 godzin z propozycją techniczną i wyceną.</p>
      <p style="color:#aab1b8">Masz zdjęcie podjazdu? <a href="/ai/" style="color:var(--green-hi)">Wizualizator AI pokaże wiatę na Twoim podwórku w 3 wariantach.</a></p>
    </div>
    <div>
    {form(MODULE_OPTIONS, selected=m["opt"], button="Wyślij zapytanie o wycenę")}
    </div>
  </div>
</section>
</main>
{FOOTER}
{FORM_JS}'''
    return page(m["title"], m["desc"], url, body, og_image="/img/" + m["img"], ld=ld)

STAND_MODELS = [
 ("CA-Lite", "Panel ścienny", "ca-lite", None, "100-150 × 50 cm", "Przykręcany wkrętami lub kotwami do ściany albo ogrodzenia", "Garaż, komórka, ogrodzenie - wszędzie tam, gdzie można wiercić"),
 ("CA-Entry", "Niski stojak", "ca-entry", "ca-entry.jpg", "Wysokość 60-80 cm", "Wolnostojący, na stopach z płaskownika 100 × 4 mm", "Przy drzwiach wejściowych i schodach - łopata do śniegu, miotła, rękawice"),
 ("CA-Yard", "Szeroki stojak", "ca-yard", "ca-yard.jpg", "Szerokość 80-100 cm", "Wolnostojący, na stopach z płaskownika 100 × 4 mm", "Podwórko, patio, taras - komplet narzędzi ogrodowych"),
 ("CA-Hard", "Wzmocniony stojak", "ca-hard", "ca-hard.jpg", "Grubszy profil", "Wolnostojący, na stopach z płaskownika 100 × 4 mm", "Ciężkie narzędzia: młoty, kilofy, mokre węże, sprzęt budowlany"),
]
STAND_FAQ = [
 ("Czy trzeba wiercić w ścianie?", "Modele CA-Entry, CA-Yard i CA-Hard stoją same na szerokich stopach, więc nie wiercisz w elewacji ani w ociepleniu. Tylko panel CA-Lite przykręca się do ściany lub ogrodzenia."),
 ("Ile kosztuje stojak i kiedy mogę go dostać?", "Ceny wynoszą od 300 do 999 zł, zależnie od modelu i wyposażenia. Stojaki są w fazie prototypu i robimy je na zamówienie, więc dokładną cenę i termin ustalamy przy zamówieniu, zależnie od modelu i wyposażenia."),
 ("Jak wygląda dostawa?", "Dostawę ustalamy indywidualnie przy zamówieniu."),
 ("Czy stojak pasuje do wiaty?", "Tak. Stojaki CA-Stand robimy w tym samym stylu i kolorze co wiaty CarportActive. Stojak może stać obok wiaty, a jeśli wolisz, narzędzia mogą wisieć na samej wiacie, na panelu narzędziowym."),
 ("Czy mogę zamówić inny rozmiar albo inny układ uchwytów?", "Tak, stojaki robimy na zamówienie. Napisz, jakie narzędzia chcesz na nim trzymać, a dobierzemy rozmiar i uchwyty."),
]

def stand_page():
    url = f"{SITE}/dodatki/ca-stand/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CarportActive", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Stojaki CA-Stand", "item": url}]},
        {"@type": "Product", "name": "Stojak na narzędzia ogrodowe CA-Stand", "brand": {"@type": "Brand", "name": "CarportActive"},
         "description": "Metalowy stojak i panel na narzędzia ogrodowe: łopaty, grabie, miotły, rękawice. Modele wolnostojące i ścienne, na zamówienie.",
         "image": [SITE + "/img/ca-stand/ca-stand-linia.jpg"],
         "offers": {"@type": "AggregateOffer", "priceCurrency": "PLN", "lowPrice": "300", "highPrice": "999", "offerCount": "4", "availability": "https://schema.org/PreOrder", "url": SITE + "/dodatki/ca-stand/"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in STAND_FAQ]}]}
    cards = []
    for n, t, slug, img, dim, mnt, use in STAND_MODELS:
        pic = f'<img src="/img/ca-stand/{img}" alt="Stojak na narzędzia {n} - {e(t.lower())}" width="400" height="300" loading="lazy" decoding="async">' if img else '<div class="model-noimg">Panel ścienny - zdjęcie wkrótce</div>'
        cards.append(f'      <div class="model" id="{slug}">{pic}<div class="model-body"><h3>{n}</h3><div class="model-type">{e(t)}</div><dl><dt>Wymiar</dt><dd>{e(dim)}</dd><dt>Montaż</dt><dd>{e(mnt)}</dd><dt>Gdzie</dt><dd>{e(use)}</dd></dl></div></div>')
    opts = [f"{n} - {t.lower()}" for n, t, *_ in STAND_MODELS] + ["Nie wiem - pomóżcie dobrać"]
    faq = "\n".join(f'    <details class="faq-item"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in STAND_FAQ)
    body = f'''{header("stojaki")}
<main>
<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a> / Stojaki CA-Stand</nav>
    <div>
      <p class="kicker">Dodatki w stylu wiaty</p>
      <h1>Stojak na narzędzia ogrodowe CA-Stand</h1>
      <p class="lead">Łopata do śniegu, miotła, grabie i rękawice w jednym miejscu przy drzwiach albo na podwórku. Stojak stoi sam i nie trzeba wiercić w elewacji.</p>
      <div class="price-line"><p class="price"><small>od</small>300 zł</p><span class="price-note">do 999 zł zależnie od modelu, na zamówienie, dostawa do uzgodnienia</span></div>
      <div class="actions">
        <a class="btn btn-green" href="#kontakt">Zamów stojak</a>
        <a class="btn btn-ghost" href="#modele">Zobacz modele</a>
      </div>
    </div>
    <img src="/img/ca-stand/ca-stand-linia.jpg" alt="Trzy metalowe stojaki na narzędzia ogrodowe CA-Stand przy ścianie domu" width="1600" height="873" decoding="async" fetchpriority="high">
  </div>
</section>

<section class="sec">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Kiedy to się przydaje</h2>
    <ul class="problems">
      <li>Łopata do śniegu i miotła stoją oparte o ścianę przy drzwiach i co chwilę się przewracają.</li>
      <li>Narzędzia ogrodowe leżą w garażu na kupie i trzeba ich szukać.</li>
      <li>Elewacja jest ocieplona i nie chcesz w niej wiercić, żeby powiesić wieszak.</li>
    </ul>
    <p class="answer">Stojak CA-Stand daje każdemu narzędziu swoje miejsce. Stoi na szerokich stopach, więc nie przykręcasz go do domu, a w razie potrzeby przestawiasz w inne miejsce.</p>
  </div></div>
</section>

<section class="sec sec-zinc" id="modele">
  <div class="wrap">
    <h2 class="sec-title">Modele</h2>
    <div class="models">
{chr(10).join(cards)}
    </div>
    <p class="small-note">Stojaki są w fazie prototypu - zdjęcia pokazują projekt. Wykonanie i wyposażenie ustalamy przy zamówieniu.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap"><div class="narrow text-block">
    <h2 class="sec-title">W tym samym stylu co wiata</h2>
    <p>Stojaki robimy z tej samej stali i w tym samym kolorze co wiaty CarportActive. Stojak przy drzwiach, wiata przy wjeździe i panel narzędziowy na jej ścianie wyglądają jak jeden komplet, a nie jak rzeczy z różnych sklepów.</p>
    <p class="note">Masz albo planujesz wiatę? Narzędzia mogą wisieć na niej samej - zobacz <a href="/moduly/panel-narzedziowy/">panel narzędziowy do wiaty</a>.</p>
  </div></div>
</section>

<section class="sec sec-zinc">
  <div class="wrap">
    <h2 class="sec-title">Jak to wygląda</h2>
    <div class="gallery">
      <img src="/img/ca-stand/ca-stand-lopata.jpg" alt="Stojak na łopatę do śniegu, miotłę i rękawice przy ścianie domu" width="1200" height="670" loading="lazy" decoding="async">
      <img src="/img/ca-stand/ca-stand-rekawice.jpg" alt="Szeroki metalowy stojak na narzędzia z panelem perforowanym" width="1200" height="670" loading="lazy" decoding="async">
    </div>
  </div>
</section>

<!--PORADNIKI:START-->
<!--PORADNIKI:END-->

<section class="sec">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Pytania o stojaki</h2>
{faq}
  </div></div>
</section>

<section class="sec sec-dark" id="kontakt">
  <div class="wrap contact-grid">
    <div>
      <h2 class="sec-title">Zamów stojak CA-Stand</h2>
      <p class="sec-intro">Napisz, który model Cię interesuje i jakie narzędzia chcesz na nim trzymać. Odezwiemy się w ciągu 24 godzin z ceną, terminem i propozycją dostawy.</p>
    </div>
    <div>
    {form(opts, placeholder="Jakie narzędzia, gdzie ma stać, miejscowość dostawy", button="Wyślij zamówienie")}
    </div>
  </div>
</section>
</main>
{FOOTER}
{FORM_JS}'''
    return page("Stojak na narzędzia ogrodowe i łopaty CA-Stand - od 300 zł | CarportActive",
                "Metalowy stojak na narzędzia ogrodowe: łopaty, grabie, miotły i rękawice w jednym miejscu. Wolnostojący bez wiercenia albo panel na ścianę. Od 300 zł, na zamówienie.",
                url, body, og_image="/img/ca-stand/ca-stand-linia.jpg", ld=ld)

if __name__ == "__main__":
    for m in M:
        d = f"static/moduly/{m['slug']}"; os.makedirs(d, exist_ok=True)
        open(f"{d}/index.html", "w", encoding="utf-8").write(module_page(m))
    os.makedirs("static/dodatki/ca-stand", exist_ok=True)
    open("static/dodatki/ca-stand/index.html", "w", encoding="utf-8").write(stand_page())
    print("ok")

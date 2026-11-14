import os
from layout import *

# Rozdział "Inspiracje": wizualizacje koncepcyjne, NIE realizacje.
# Żeby dodać nowy typ: wrzuć zdjęcie do static/img/inspiracje/ i dopisz słownik do TYPES.
DISCLAIMER = "Wizualizacja koncepcyjna, wycena indywidualna."
IMG_DIR = "/img/inspiracje/"

# Wspólna lista "od czego zależy cena" - bez żadnych kwot
DEPENDS_COMMON = [
    "Wymiary wiaty i liczba stanowisk.",
    "Rodzaj i grubość stali oraz sposób wykończenia, np. malowanie proszkowe w kolorze RAL 7016.",
    "Fundamenty i rodzaj podłoża.",
    "Pokrycie dachu, odwodnienie i oświetlenie.",
    "Dodatki: podbitka, ściany boczne, przęsła, brama.",
]

TYPES = [
    dict(
        slug="wiata-wspornikowa",
        short="Wiata wspornikowa",
        h1="Wiata wspornikowa - nowoczesna wiata na samochód",
        title="Wiata wspornikowa - nowoczesna wiata na samochód | Inspiracje",
        desc="Wiata wspornikowa z drewnianą podbitką i oświetleniem LED: dach wysunięty nad samochód, bez słupów od strony wjazdu. Wizualizacja koncepcyjna, wycena indywidualna.",
        lead="Dach wysunięty daleko poza słupy, więc od strony samochodu nie stoi żaden słup. Poniżej koncepcja z drewnianą podbitką i oświetleniem w dachu.",
        imgs=[
            ("wiata-wspornikowa-podbitka-drewno-led.jpg",
             "Wiata wspornikowa z ciemnej stali z drewnianą podbitką i oświetleniem LED przy nowoczesnym domu",
             "Wiata wspornikowa z drewnianą podbitką i oświetleniem", 1600, 892),
        ],
        what=[
            "Słupy stoją z jednej strony, a dach wysuwa się nad miejsce parkingowe.",
            "Skośne podpory pomagają przenieść obciążenie na fundament.",
            "Pod dachem może być podbitka z drewna albo imitacji drewna oraz oświetlenie punktowe.",
            "Konstrukcja stalowa w ciemnym kolorze, np. antracyt RAL 7016, dobrze pasuje do nowoczesnych domów.",
        ],
        depends=[
            "Wysięg dachu: im dalej dach wysunięty poza słupy, tym cięższa konstrukcja i większy fundament.",
        ] + DEPENDS_COMMON,
        note="Przy dużym wysięgu dachu konstrukcja wymaga obliczeń statycznych, dlatego wycenę przygotowujemy indywidualnie.",
    ),
    dict(
        slug="wiata-ukosne-podpory",
        short="Wiata na ukośnych podporach",
        h1="Wiata na ukośnych podporach - nowoczesny carport",
        title="Wiata na ukośnych podporach - nowoczesny carport | Inspiracje",
        desc="Nowoczesna wiata z płaskim dachem na ukośnych podporach z oświetleniem LED w dachu. Pomysł na carport przy domu. Wizualizacja koncepcyjna, wycena indywidualna.",
        lead="Płaski, cienki dach i ukośne podpory zamiast typowych pionowych słupów. Pomysł dla osób, które szukają wiaty o wyrazistym wyglądzie.",
        imgs=[
            ("wiata-ukosne-podpory-antracyt-led.jpg",
             "Nowoczesna wiata z antracytowej stali na ukośnych podporach z oświetleniem LED w dachu, na kostce granitowej",
             "Wiata na ukośnych podporach z oświetleniem w dachu", 1600, 892),
        ],
        what=[
            "Dach płaski i lekki w odbiorze, oparty na ukośnych podporach.",
            "Pod dachem pasy oświetlenia LED.",
            "Całość w ciemnym kolorze stali, np. antracyt RAL 7016.",
            "To wizualizacja koncepcyjna: dokładny kształt podpór i wymiary ustalamy po rozmowie o Twoim miejscu.",
        ],
        depends=[
            "Kąt i przekrój podpór: od tego zależy ilość stali.",
        ] + DEPENDS_COMMON,
        note="Konstrukcja o takim kształcie wymaga projektu i obliczeń statycznych, dlatego wycena jest indywidualna.",
    ),
]

TYPE_OPTIONS = [t["short"] + " (inspiracja)" for t in TYPES] + ["Inna wiata nietypowa - omówię szczegóły"]


def check_imgs():
    for t in TYPES:
        for f, *_ in t["imgs"]:
            if not os.path.exists("static" + IMG_DIR + f):
                print("UWAGA: brak zdjęcia static" + IMG_DIR + f)


def contact(sel=""):
    return f'''<section class="sec sec-dark" id="kontakt">
  <div class="wrap contact-grid">
    <div>
      <h2 class="sec-title">Podoba Ci się taki pomysł?</h2>
      <p class="sec-intro">Napisz, jakiej wiaty szukasz, jakie mniej więcej wymiary i gdzie ma stanąć. Odezwiemy się w ciągu 24 godzin. {e(DISCLAIMER)}</p>
    </div>
    <div>
    {form(TYPE_OPTIONS, selected=sel, placeholder="Co chcesz zbudować, wymiary (np. 3x6 m), miejscowość", button="Wyślij zapytanie")}
    </div>
  </div>
</section>'''


def type_page(t):
    url = f"{SITE}/inspiracje/{t['slug']}/"
    figs = "\n".join(
        f'      <figure><a href="{IMG_DIR}{f}"><img src="{IMG_DIR}{f}" alt="{e(alt)}" width="{w}" height="{h}" decoding="async"></a><figcaption>{e(cap)}. {e(DISCLAIMER)}</figcaption></figure>'
        for f, alt, cap, w, h in t["imgs"])
    what = "\n".join(f"      <li>{e(x)}</li>" for x in t["what"])
    dep = "\n".join(f"      <li>{e(x)}</li>" for x in t["depends"])
    others = "".join(f'<li><a href="/inspiracje/{o["slug"]}/">{e(o["h1"])}</a></li>' for o in TYPES if o is not t)
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "CarportActive", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Inspiracje", "item": SITE + "/inspiracje/"},
        {"@type": "ListItem", "position": 3, "name": t["h1"], "item": url}]}
    body = f'''{header("inspiracje")}
<main>
<section class="art-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a> / <a href="/inspiracje/">Inspiracje</a> / {e(t["short"])}</nav>
    <h1>{e(t["h1"])}</h1>
    <p class="art-lead" style="max-width:720px">{e(t["lead"])}</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="works case-photos">
{figs}
    </div>
    <p class="note">{e(DISCLAIMER)} To pomysł, a nie nasza zrealizowana wiata. Gotowe realizacje zobaczysz w zakładce <a href="/realizacje/">Realizacje</a>.</p>
  </div>
</section>
<section class="sec sec-zinc">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Na czym polega ta konstrukcja</h2>
    <ul class="problems">
{what}
    </ul>
  </div></div>
</section>
<section class="sec">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Od czego zależy cena</h2>
    <ul class="problems">
{dep}
    </ul>
    <p class="answer">{e(t["note"])} {e(DISCLAIMER)}</p>
  </div></div>
</section>

<!--PORADNIKI:START-->
<!--PORADNIKI:END-->

<section class="sec sec-zinc">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Więcej inspiracji</h2>
    <ul class="link-list">{others}<li><a href="/inspiracje/">Wszystkie inspiracje</a></li><li><a href="/#wymiary">Wiaty z naszej oferty: wymiary i ceny</a></li></ul>
  </div></div>
</section>
{contact(t["short"] + " (inspiracja)")}
</main>
{FOOTER}
{FORM_JS}'''
    return page(t["title"], t["desc"], url, body, og_image=IMG_DIR + t["imgs"][0][0], ld=ld)


def index_page():
    def fig(t):
        f, alt, cap, w, h = t["imgs"][0]
        return (f'      <figure><a href="/inspiracje/{t["slug"]}/"><img src="{IMG_DIR}{f}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"></a>'
                f'<figcaption>{e(t["short"])}. {e(DISCLAIMER)}</figcaption></figure>')
    figs = "\n".join(fig(t) for t in TYPES)
    links = "".join(f'<li><a href="/inspiracje/{t["slug"]}/">{e(t["h1"])}</a></li>' for t in TYPES)
    body = f'''{header("inspiracje")}
<main>
<section class="art-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a> / Inspiracje</nav>
    <h1>Inspiracje: pomysły na nowoczesną wiatę</h1>
    <p class="art-lead" style="max-width:720px">Szukasz pomysłu na wiatę garażową albo carport przy domu? Tu zbieramy koncepcje nietypowych wiat: wspornikowe, na ukośnych podporach, z drewnianą podbitką i oświetleniem. {e(DISCLAIMER)}</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="works">
{figs}
    </div>
    <p class="note">To pomysły i wizualizacje koncepcyjne, a nie zdjęcia gotowych obiektów. Wiaty, które już stoją u klientów, są w zakładce <a href="/realizacje/">Realizacje</a>.</p>
  </div>
</section>
<section class="sec sec-zinc">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Typy wiat</h2>
    <ul class="link-list">{links}</ul>
  </div></div>
</section>
{contact()}
</main>
{FOOTER}
{FORM_JS}'''
    return page("Inspiracje - pomysły na nowoczesną wiatę garażową i carport | CarportActive",
                "Pomysły na nowoczesną wiatę garażową: wiata wspornikowa, wiata na ukośnych podporach, drewniana podbitka i oświetlenie LED. Wizualizacje koncepcyjne, wycena indywidualna.",
                SITE + "/inspiracje/", body, og_image=IMG_DIR + TYPES[0]["imgs"][0][0])


if __name__ == "__main__":
    check_imgs()
    os.makedirs("static/inspiracje", exist_ok=True)
    open("static/inspiracje/index.html", "w", encoding="utf-8").write(index_page())
    for t in TYPES:
        d = f"static/inspiracje/{t['slug']}"
        os.makedirs(d, exist_ok=True)
        open(f"{d}/index.html", "w", encoding="utf-8").write(type_page(t))
    print("ok", len(TYPES))

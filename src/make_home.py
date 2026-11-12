import os, sys
from layout import *

MODS = [
 ("sportowy", "sport.jpg", "Moduł sportowy", "Drabinka szwedzka, drążek i poręcze na słupach wiaty. Zadaszone miejsce do treningu przy domu."),
 ("panel-narzedziowy", "diy.jpg", "Panel narzędziowy", "Panel perforowany na bocznej ścianie. Łopaty, klucze i przedłużacze na hakach pod dachem."),
 ("ogrod-wertykalny", "garden.jpg", "Ogród wertykalny", "Zioła, kwiaty albo pnącza na bocznym panelu. Zielona ściana zamiast gołej stali."),
 ("plac-zabaw", "kids.jpg", "Plac zabaw", "Ścianka wspinaczkowa, siatka i liny pod dachem. Dzieci bawią się także w deszczu."),
 ("przechowalnia-rowerow", "rower.jpg", "Przechowalnia rowerów", "Wieszaki i stojaki na rowery, hulajnogi i box dachowy. Garaż zostaje wolny."),
 ("solar-box", "solar.jpg", "Solar Box (PV)", "Wzmocniona wiata pod 6-12 paneli PV i gotowość pod Wallbox."),
 ("przeslo-zaluzjowe", "realizacje/r03-wiata-przesla-ciemny-orzech.jpg", "Przęsło żaluzjowe", "Boczna osłona od sąsiada, ulicy i wiatru. Orzech, ciemny orzech albo antracyt."),
 ("zamknieta-wiata", "realizacje/z03-wiata-zamknieta-z-brama-segmentowa.jpg", "Zamknięta wiata", "Ściany i brama zamiast blaszaka. Także wersja przelotowa z bramą z dwóch stron."),
]

WORKS = [
 ("r01-wiata-przesla-orzech", "Wiata dwustanowiskowa z przęsłami w kolorze orzech", None),
 ("r04-wiata-przy-garazu", "Wiata dobudowana do garażu - Otwock Mały", "wiata-otwock-maly"),
 ("r06-wiata-wielostanowiskowa", "Wiata wielostanowiskowa dla karetek - Warszawa", "wiata-warszawa"),
 ("r03-wiata-przesla-ciemny-orzech", "Wiata z przęsłami ciemny orzech - Serock", "wiata-serock"),
 ("r11-wiata-przeszklona", "Przeszklona wiata garażowa - Konstancin-Jeziorna", "wiata-konstancin-jeziorna"),
 ("r14-zadaszenie-tarasu", "Zadaszenie tarasu w kolorze dopasowanym do domu", None),
]

FAQ = [
 ("Czy na wiatę garażową potrzebne jest pozwolenie na budowę?",
  "Zazwyczaj nie*. Zgodnie z polskim Prawem Budowlanym wiaty o powierzchni zabudowy do 35 m² (a na działkach z budynkiem mieszkalnym nawet do 50 m²) nie wymagają pozwolenia na budowę. Modele 3 × 6 m (18 m²) i 4 × 6 m (24 m²) mieszczą się w limicie 35 m². Model 6 × 6 m (36 m²) go przekracza, więc zasady dla niego sprawdź w lokalnym urzędzie. *Zasady zależą od lokalizacji i miejscowego planu zagospodarowania - zawsze zweryfikuj je w lokalnym urzędzie (urząd gminy lub starostwo powiatowe)."),
 ("Czy mogę zamówić samą wiatę, a moduły dokupić w przyszłości?",
  "Tak. Każda wiata CarportActive ma zunifikowane otwory montażowe i zapas wytrzymałości konstrukcyjnej. Możesz zamontować samo zadaszenie dziś, a moduł sportowy, ściankę dla dzieci czy panel narzędziowy dokręcić w kolejnym sezonie."),
 ("Jak wygląda przygotowanie podłoża i montaż?",
  "Wiatę montujemy na stopach fundamentowych (punktowych) albo na istniejącej płycie betonowej lub kostce z odpowiednim podbudowaniem. Sam montaż gotowej, ocynkowanej konstrukcji na działce klienta zajmuje zazwyczaj 1 dzień roboczy."),
]

def build(robots="index, follow", guides_html=""):
    tiles = "\n".join(f'''      <a class="tile" href="/moduly/{s}/">
        <img src="/img/{img}" alt="Wiata CarportActive - {e(n.lower())}" width="800" height="600" loading="lazy" decoding="async">
        <h3>{e(n)}</h3>
        <p>{e(d)}</p>
        <span class="more">Zobacz moduł</span>
      </a>''' for s, img, n, d in MODS)

    works = "\n".join(f'      <figure><a href="{("/realizacje/" + sl + "/") if sl else ("/img/realizacje/" + f + ".jpg")}"><img src="/img/realizacje/{f}.jpg" alt="{e(c)}" width="800" height="600" loading="lazy" decoding="async"></a><figcaption>{e(c)}</figcaption></figure>' for f, c, sl in WORKS)
    strip = "\n      ".join(f'<a href="/moduly/{s}/">{e(n)}</a>' for s, img, n, d in MODS) + '\n      <a href="/dodatki/ca-stand/">Stojaki na narzędzia</a>'
    faq = "\n".join(f'    <details class="faq-item"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": SITE + "/#organization", "name": "CarportActive", "url": SITE + "/",
         "description": "Producent stalowych wiat modułowych i carportów fotowoltaicznych ze stali konstrukcyjnej S235.", "areaServed": "PL"},
        {"@type": "Product", "name": "Modułowa Wiata Garażowa CarportActive S235",
         "description": "Stalowa wiata samochodowa (carport) ocynkowana ogniowo z możliwością rozbudowy o moduł fotowoltaiczny Solar Box, moduł sportowy, warsztat, ogród wertykalny i plac zabaw.",
         "brand": {"@type": "Brand", "name": "CarportActive"}, "material": "Stal konstrukcyjna S235 ocynkowana ogniowo",
         "image": [SITE + "/img/realizacje/r01-wiata-przesla-orzech.jpg"],
         "offers": {"@type": "AggregateOffer", "priceCurrency": "PLN", "lowPrice": "16500", "highPrice": "21949", "offerCount": "3",
                    "availability": "https://schema.org/MadeToOrder", "url": SITE + "/#wymiary"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    body = f'''{header()}
<main>
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="hero-kicker">Stalowe wiaty garażowe z modułami</p>
      <h1>Wiata, która robi więcej</h1>
      <p class="hero-sub">Wiata ze stali S235, do której dokręcasz to, czego potrzebujesz: drabinkę, panel na narzędzia, plac zabaw, przechowalnię rowerów albo panele PV. Od razu albo za rok.</p>
      <div class="actions">
        <a class="btn btn-green" href="#kontakt">Zapytaj o wycenę</a>
        <a class="btn btn-ghost" href="/ai/">Zobacz wiatę na swoim podwórku (AI)</a>
      </div>
    </div>
    <figure class="hero-photo">
      <img src="/img/realizacje/r01-wiata-przesla-orzech.jpg" alt="Stalowa wiata CarportActive w kolorze antracyt z przęsłami żaluzjowymi orzech" width="1600" height="1201" decoding="async" fetchpriority="high">
      <figcaption>Nasza realizacja: wiata z przęsłami w kolorze orzech</figcaption>
    </figure>
  </div>
  <nav class="mod-strip" aria-label="Moduły">
    <div class="wrap">
      {strip}
    </div>
  </nav>
</section>

<section class="sec" id="moduly">
  <div class="wrap">
    <h2 class="sec-title">Jedna wiata, wiele zastosowań</h2>
    <p class="sec-intro">Każdy moduł mocujemy do słupów tej samej wiaty. Możesz zacząć od samego zadaszenia i dołożyć moduł w kolejnym sezonie.</p>
    <div class="tiles">
{tiles}
    </div>
  </div>
</section>

<section class="sec sec-zinc" id="realizacje">
  <div class="wrap">
    <h2 class="sec-title">Nasze realizacje</h2>
    <p class="sec-intro">Wiaty, które postawiliśmy u klientów. Konstrukcja w kolorze antracyt RAL 7016, przęsła i dodatki dopasowane do domu.</p>
    <div class="works">
{works}
    </div>
    <p style="margin-top:24px"><a class="btn btn-outline" href="/realizacje/">Zobacz wszystkie realizacje</a></p>
  </div>
</section>

<section class="sec" aria-label="Konstrukcja" style="border-bottom:1px solid var(--line)">
  <div class="wrap specs">
    <div class="spec"><h3>Stal S235</h3><p>Pełna stal konstrukcyjna, spawana, a nie cienka profilówka z marketu.</p></div>
    <div class="spec"><h3>Ocynk ogniowy</h3><p>Ocynk i malowanie proszkowe, które nie łuszczą się po pierwszej zimie.</p></div>
    <div class="spec"><h3>Zapas nośności</h3><p>Słupy i fundament liczone tak, żeby dołożyć moduł bez przeróbek i cięcia stali.</p></div>
    <div class="spec"><h3>Montaż w 1 dzień</h3><p>Projektujemy, spawamy i montujemy w całej Polsce.</p></div>
  </div>
</section>

<section class="sec sec-dark" id="ai">
  <div class="wrap ai-grid">
    <div>
      <h2 class="sec-title">Zobacz wiatę na swoim podwórku</h2>
      <p class="sec-intro">Nie musisz sobie wyobrażać, jak to będzie wyglądać. Wizualizator AI pokaże wiatę na zdjęciu Twojego podjazdu.</p>
      <a class="btn btn-green" href="/ai/">Wgraj zdjęcie podjazdu</a>
    </div>
    <ol class="steps">
      <li><div><strong>Zrób zdjęcie podjazdu</strong><span>Wystarczy zwykłe zdjęcie z telefonu.</span></div></li>
      <li><div><strong>Zaznacz miejsce na wiatę</strong><span>Na siatce pokazujesz, gdzie mają stanąć słupy.</span></div></li>
      <li><div><strong>Dostajesz 3 warianty</strong><span>Porównujesz je i wysyłasz nam ten, który pasuje.</span></div></li>
    </ol>
  </div>
</section>

<section class="sec" id="wymiary">
  <div class="wrap">
    <h2 class="sec-title">Wymiary</h2>
    <p class="sec-intro">Trzy sprawdzone rozmiary bazowe, wysokość 2,7 m, słupy z profilu 100 x 100 x 3 mm. Każdy wymiar możemy też zrobić indywidualnie.</p>
    <div class="table-scroll">
    <table class="sizes">
      <thead><tr><th>Wymiar</th><th>Wariant</th><th>Cena brutto*</th><th>Dla kogo</th></tr></thead>
      <tbody>
        <tr><td class="dim">3 × 6 m</td><td class="name">Jednostanowiskowa<br><small>18 m²</small></td><td class="price-cell">16 500 zł</td><td class="desc">Jeden samochód osobowy, wąskie podjazdy i mniejsze działki.</td></tr>
        <tr><td class="dim">4 × 6 m</td><td class="name">Jednostanowiskowa szeroka<br><small>24 m²</small></td><td class="price-cell">17 605 zł</td><td class="desc">Duży SUV i miejsce z boku na moduł sportowy, rowery albo warsztat.</td></tr>
        <tr><td class="dim">6 × 6 m</td><td class="name">Dwustanowiskowa<br><small>36 m²</small></td><td class="price-cell">21 949 zł</td><td class="desc">Dwa samochody i duża połać pod Solar Box, do 12 paneli PV.</td></tr>
      </tbody>
    </table>
    </div>
    <p class="footnote">*Ceny bazowe konstrukcji, bez fundamentów i montażu. To projekty policzone przez inżyniera - każdy inny wymiar i układ liczymy indywidualnie po pomiarze na miejscu. Jak liczymy fundamenty i montaż, opisujemy na stronie <a href="/montaz/">Montaż wiat</a>.</p>
    <p class="footnote">Wiaty do 35 m² zazwyczaj nie wymagają pozwolenia na budowę. Zasady zależą od lokalizacji i miejscowego planu zagospodarowania - zawsze zweryfikuj je w urzędzie gminy lub starostwie powiatowym.</p>
  </div>
</section>

<section class="sec sec-zinc">
  <div class="wrap split">
    <img src="/img/ca-stand/ca-stand-linia.jpg" alt="Metalowe stojaki na narzędzia ogrodowe CA-Stand" width="1600" height="873" loading="lazy" decoding="async">
    <div>
      <h2 class="sec-title">Stojaki na narzędzia CA-Stand</h2>
      <p class="sec-intro" style="margin-bottom:16px">Łopata do śniegu, miotła i grabie w jednym miejscu przy drzwiach albo na podwórku. Stoją same, bez wiercenia w elewacji, w tym samym stylu co wiata.</p>
      <p class="price"><small>od</small>300 zł</p>
      <a class="btn btn-outline" href="/dodatki/ca-stand/">Zobacz modele</a>
    </div>
  </div>
</section>

<!--PORADNIK-HOME:START-->{guides_html}<!--PORADNIK-HOME:END-->

<section class="sec" id="faq">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Pytania</h2>
{faq}
  </div></div>
</section>

<section class="sec sec-dark" id="kontakt">
  <div class="wrap contact-grid">
    <div>
      <h2 class="sec-title">Zaprojektujmy Twoją wiatę</h2>
      <p class="sec-intro">Napisz, jaki rozmiar i moduł Cię interesują. Odezwiemy się w ciągu 24 godzin z propozycją techniczną i wyceną.</p>
      <p style="color:#aab1b8">Masz zdjęcie podjazdu? <a href="/ai/" style="color:var(--green-hi)">Wizualizator AI pokaże wiatę na Twoim podwórku w 3 wariantach.</a></p>
    </div>
    <div>
    {form(MODULE_OPTIONS, button="Wyślij zapytanie o wycenę")}
    </div>
  </div>
</section>
</main>
{FOOTER}
{FORM_JS}'''
    return page("CarportActive - Nowoczesne Wiaty Garażowe i Modułowe Carporty Stalowe",
                "Stalowe wiaty garażowe S235 ocynkowane ogniowo. Modułowa konstrukcja: carport pod fotowoltaikę (Solar Box), moduł sportowy, warsztat, plac zabaw i ogród wertykalny. Sprawdź wizualizację AI!",
                SITE + "/", body, robots=robots, ld=ld, og_image="/img/realizacje/r01-wiata-przesla-orzech.jpg")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "static/index.html"
    rob = "noindex, nofollow" if "podglad" in out else "index, follow"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(build(rob))
    print("ok", out)

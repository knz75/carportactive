import os, math, re, unicodedata
from layout import *
from make_realizacje import CASES, CAPTION
from make_moduly import M

BASE = ("Pruszków", 52.1706, 20.8119)
TOWNS = [
 ("Pruszków", 52.1706, 20.8119), ("Warszawa", 52.2297, 21.0122), ("Piastów", 52.1846, 20.8395),
 ("Ożarów Mazowiecki", 52.2104, 20.7967), ("Brwinów", 52.1427, 20.7170), ("Michałowice", 52.1650, 20.8700),
 ("Raszyn", 52.1556, 20.9265), ("Nadarzyn", 52.0950, 20.8050), ("Grodzisk Mazowiecki", 52.1094, 20.6328),
 ("Milanówek", 52.1240, 20.6680), ("Błonie", 52.1993, 20.6170), ("Stare Babice", 52.2510, 20.8350),
 ("Izabelin", 52.3000, 20.8167), ("Łomianki", 52.3340, 20.8870), ("Leszno", 52.2580, 20.5880),
 ("Lesznowola", 52.0656, 20.9396), ("Piaseczno", 52.0814, 21.0236), ("Konstancin-Jeziorna", 52.0931, 21.1166),
 ("Józefów", 52.1360, 21.2350), ("Otwock", 52.1053, 21.2614), ("Marki", 52.3270, 21.1060),
 ("Ząbki", 52.2930, 21.1060), ("Zielonka", 52.3060, 21.1600), ("Kobyłka", 52.3390, 21.1950),
 ("Wołomin", 52.3400, 21.2420), ("Sulejówek", 52.2450, 21.2800), ("Legionowo", 52.4000, 20.9260),
 ("Jabłonna", 52.3800, 20.9100), ("Nowy Dwór Mazowiecki", 52.4330, 20.7160), ("Serock", 52.5103, 21.0590),
 ("Radzymin", 52.4150, 21.1840), ("Halinów", 52.2270, 21.3540), ("Żyrardów", 52.0490, 20.4460),
 ("Jaktorów", 52.0870, 20.5520), ("Mszczonów", 51.9750, 20.5200), ("Tarczyn", 51.9800, 20.8350),
 ("Prażmów", 51.9650, 21.0620), ("Góra Kalwaria", 51.9770, 21.2150), ("Grójec", 51.8650, 20.8670),
 ("Sochaczew", 52.2290, 20.2380), ("Kampinos", 52.2660, 20.4660), ("Karczew", 52.0790, 21.2510),
]
CASE_POS = {"wiata-warszawa": (52.2297, 21.0122), "wiata-piskorka": (51.990, 21.025), "wiata-serock": (52.5103, 21.0590),
            "wiata-otwock-maly": (52.035, 21.255), "wiata-chrzanow-maly": (52.100, 20.660),
            "wiata-konstancin-jeziorna": (52.0931, 21.1166), "wiata-zyrardow": (52.0490, 20.4460)}

def km(a, b):
    R = 6371; la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def r5(x):
    return max(5, int(round(x / 5.0)) * 5)

def dist_txt(d, name):
    return "w tej samej miejscowości" if d < 3 else f"ok. {r5(d)} km od miejscowości {e(name)}"

def slug(t):
    t = t.replace('ł', 'l').replace('Ł', 'l')
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')

def town_page(t):
    name, lat, lon = t
    s = slug(name); url = f"{SITE}/okolice/{s}/"
    d_base = km((lat, lon), BASE[1:])
    cases = sorted(CASES, key=lambda c: km((lat, lon), CASE_POS[c["slug"]]))[:3]
    near = sorted([x for x in TOWNS if x[0] != name], key=lambda x: km((lat, lon), x[1:]))[:6]
    if name == "Pruszków":
        where = "Nasza baza jest w Pruszkowie - stąd wyjeżdżamy na pomiary i montaże w całej okolicy."
    else:
        where = f"Jesteśmy z Pruszkowa, ok. {r5(d_base)} km w linii prostej od miejscowości {name}. Przyjeżdżamy na pomiar, robimy fundamenty i montujemy wiaty na miejscu."
    figs = "\n".join(
        f'''      <figure><a href="/realizacje/{c["slug"]}/"><img src="/img/realizacje/{c["imgs"][0]}.jpg" alt="{e(CAPTION[c["imgs"][0]])}" width="800" height="600" loading="lazy" decoding="async"></a><figcaption><a href="/realizacje/{c["slug"]}/" style="color:inherit">{e(c["h1"])}</a><br>{dist_txt(km((lat, lon), CASE_POS[c["slug"]]), name)}</figcaption></figure>''' for c in cases)
    mods = "".join(f'<li><a href="/moduly/{m["slug"]}/">{e(m["h1"])}</a></li>' for m in M)
    nearby = "".join(f'<li><a href="/okolice/{slug(x[0])}/">Wiaty garażowe - {e(x[0])}</a></li>' for x in near)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": f"Wiaty garażowe i montaż - {name}", "areaServed": {"@type": "Place", "name": name},
         "provider": {"@type": "Organization", "name": "CarportActive", "url": SITE + "/", "address": {"@type": "PostalAddress", "addressLocality": "Pruszków", "addressCountry": "PL"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CarportActive", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Obszar działania", "item": SITE + "/okolice/"},
            {"@type": "ListItem", "position": 3, "name": name, "item": url}]}]}
    body = f'''{header()}
<main>
<section class="art-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a> / <a href="/okolice/">Obszar działania</a> / {e(name)}</nav>
    <h1>Wiaty garażowe - {e(name)} i okolice</h1>
    <p class="art-lead" style="max-width:720px">{e(where)} Stalowe wiaty z fundamentami poniżej strefy przemarzania, w kolorze antracyt RAL 7016, z modułami i przęsłami.</p>
    <div class="actions" style="margin-top:24px"><a class="btn btn-green" href="#kontakt">Zapytaj o termin i wycenę</a><a class="btn btn-outline" href="/realizacje/">Wszystkie realizacje</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <h2 class="sec-title">Najbliższe realizacje</h2>
    <p class="sec-intro">Wiaty, które postawiliśmy najbliżej miejscowości {e(name)}.</p>
    <div class="works">
{figs}
    </div>
  </div>
</section>

<section class="sec sec-zinc">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Ceny bazowe</h2>
    <table class="sizes"><thead><tr><th>Wymiar</th><th>Wariant</th><th>Cena brutto*</th></tr></thead><tbody>
      <tr><td class="dim">3 × 6 m</td><td class="name">Jednostanowiskowa</td><td class="price-cell">16 500 zł</td></tr>
      <tr><td class="dim">4 × 6 m</td><td class="name">Jednostanowiskowa szeroka</td><td class="price-cell">17 605 zł</td></tr>
      <tr><td class="dim">6 × 6 m</td><td class="name">Dwustanowiskowa</td><td class="price-cell">21 949 zł</td></tr>
    </tbody></table>
    <p class="footnote">*Ceny konstrukcji bez fundamentów i montażu. Montaż z fundamentami od ok. 4 000 zł - <a href="/montaz/">jak liczymy montaż</a>. Inne wymiary liczymy po pomiarze na miejscu.</p>
  </div></div>
</section>

<section class="sec">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Jak pracujemy</h2>
    <ul class="problems">
      <li>Najpierw kontakt: zdjęcia miejsca, wymiary i ustalenie terminu. Pracujemy według grafiku, nie na jutro.</li>
      <li>Pomiar na miejscu i wycena całości.</li>
      <li>Fundamenty pod słupy poniżej strefy przemarzania, potem 2-4 tygodnie na dojrzewanie betonu.</li>
      <li>Montaż konstrukcji - wiata do 8 słupów stoi w 1 dzień.</li>
    </ul>
  </div></div>
</section>

<section class="sec sec-paper">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Co możemy postawić</h2>
    <ul class="link-list">{mods}<li><a href="/dodatki/ca-stand/">Stojaki na narzędzia CA-Stand</a></li></ul>
    <h2 class="sec-title" style="margin-top:48px">Pobliskie miejscowości</h2>
    <ul class="link-list">{nearby}<li><a href="/okolice/">Cały obszar działania</a></li></ul>
  </div></div>
</section>

<section class="sec sec-dark" id="kontakt">
  <div class="wrap contact-grid">
    <div>
      <h2 class="sec-title">Zapytaj o wiatę - {e(name)}</h2>
      <p class="sec-intro">Napisz, jaki rozmiar Cię interesuje i gdzie ma stanąć wiata. Odezwiemy się w ciągu 24 godzin z wolnym terminem na pomiar.</p>
      <p style="color:#aab1b8">Masz zdjęcie podjazdu? <a href="/ai/" style="color:var(--green-hi)">Wizualizator AI pokaże wiatę na Twoim podwórku w 3 wariantach.</a></p>
    </div>
    <div>
    {form(MODULE_OPTIONS, placeholder=f"{name}: wymiary, podłoże, pytania", button="Wyślij zapytanie o wycenę")}
    </div>
  </div>
</section>
</main>
{FOOTER}
{FORM_JS}'''
    return page(f"Wiaty garażowe {name} - montaż, fundamenty, ceny | CarportActive",
                f"Stalowe wiaty garażowe - {name} i okolice. Firma z Pruszkowa: pomiar, fundamenty i montaż. Najbliższe realizacje, ceny od 16 500 zł brutto.",
                url, body, og_image=f'/img/realizacje/{cases[0]["imgs"][0]}.jpg', ld=ld)

def hub():
    rows = sorted(TOWNS, key=lambda x: km(x[1:], BASE[1:]))
    items = "".join(f'<li><a href="/okolice/{slug(n)}/">{e(n)} <span style="color:var(--muted);font-weight:400">ok. {r5(km((la, lo), BASE[1:])) if n != "Pruszków" else 0} km</span></a></li>' for n, la, lo in rows)
    body = f'''{header()}
<main>
<section class="art-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a> / Obszar działania</nav>
    <h1>Obszar działania</h1>
    <p class="art-lead" style="max-width:720px">Jesteśmy z Pruszkowa i montujemy wiaty w Warszawie i na Mazowszu. Poniżej miejscowości, do których dojeżdżamy najczęściej, z odległością od naszej bazy w linii prostej. Nie ma Twojej miejscowości? Napisz - dalsze dojazdy też ustalamy.</p>
  </div>
</section>
<section class="sec"><div class="wrap"><div class="narrow">
  <ul class="link-list">{items}</ul>
</div></div></section>
</main>
{FOOTER}'''
    return page("Obszar działania - wiaty garażowe Warszawa i Mazowsze | CarportActive",
                "Firma z Pruszkowa: wiaty garażowe z montażem w Warszawie i na Mazowszu. Lista miejscowości z odległością od naszej bazy i najbliższymi realizacjami.",
                SITE + "/okolice/", body)

if __name__ == "__main__":
    os.makedirs("static/okolice", exist_ok=True)
    open("static/okolice/index.html", "w", encoding="utf-8").write(hub())
    for t in TOWNS:
        d = f"static/okolice/{slug(t[0])}"; os.makedirs(d, exist_ok=True)
        open(f"{d}/index.html", "w", encoding="utf-8").write(town_page(t))
    print("ok", len(TOWNS))

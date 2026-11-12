import os
from layout import *
FAQ = [
 ("Czy możecie zamontować wiatę kupioną gdzie indziej?", "Tak. Montujemy wiaty z zestawów różnych producentów i z marketów. Przyślij zdjęcia miejsca, wymiary i nazwę zestawu, a powiemy, co trzeba zrobić i ile to będzie kosztować."),
 ("Dlaczego nie montujecie od razu?", "Pracujemy według grafiku, który jest zwykle zajęty na kilka tygodni do przodu. Do tego beton pod słupami musi dojrzeć 2-4 tygodnie, zanim postawimy konstrukcję. Termin ustalamy przy pierwszym kontakcie."),
 ("Ile kosztuje montaż?", "Montaż z fundamentami zaczyna się od ok. 4 tys. zł. Dokładna cena zależy od liczby słupów, podłoża i dodatków, dlatego podajemy ją po zdjęciach i wymiarach."),
 ("Czy wiatę można przykręcić do kostki zamiast robić fundamenty?", "Nie polecamy. Lekka konstrukcja przykręcona do kostki albo płyt może przy wichurze odlecieć i narobić szkód. Dlatego słupy kotwimy w fundamentach poniżej strefy przemarzania."),
]
def build():
    faq = "\n".join(f'    <details class="faq-item"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": "Montaż wiat garażowych", "areaServed": "Mazowsze", "provider": {"@type": "Organization", "name": "CarportActive", "url": SITE + "/"},
         "offers": {"@type": "Offer", "priceCurrency": "PLN", "price": "4000", "description": "Montaż wiaty z fundamentami - cena od"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    body = f'''{header("montaz")}
<main>
<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a> / Montaż wiat</nav>
    <div>
      <p class="kicker">Mazowsze</p>
      <h1>Montaż wiat garażowych</h1>
      <p class="lead">Fundamenty, montaż konstrukcji i dodatki. Montujemy nasze wiaty i wiaty z zestawów kupionych gdzie indziej. Zawsze najpierw kontakt i termin - pracujemy według grafiku.</p>
      <div class="price-line"><p class="price"><small>od ok.</small>4 000 zł</p><span class="price-note">montaż z fundamentami, dokładna cena po zdjęciach</span></div>
      <div class="actions">
        <a class="btn btn-green" href="#kontakt">Zapytaj o termin i wycenę</a>
        <a class="btn btn-ghost" href="/realizacje/">Zobacz realizacje</a>
      </div>
    </div>
    <img src="/img/realizacje/r05-wiata-z-oswietleniem.jpg" alt="Wiata zamontowana przy garażu, z oświetleniem i ścianą z przęseł" width="1600" height="1200" decoding="async" fetchpriority="high">
  </div>
</section>

<section class="sec">
  <div class="wrap ai-grid" style="align-items:start">
    <div>
      <h2 class="sec-title">Jak wygląda montaż</h2>
      <p class="sec-intro">Montaż wiaty na fundamentach to dwa przyjazdy ekipy, bo beton pod słupami musi dojrzeć.</p>
    </div>
    <ol class="steps steps-light">
      <li><div><strong>Kontakt, zdjęcia i wymiary</strong><span>Przysyłasz zdjęcia miejsca i wymiary albo nazwę zestawu, który masz.</span></div></li>
      <li><div><strong>Wycena i termin</strong><span>Podajemy cenę i wolny termin z grafiku. Nie montujemy na jutro.</span></div></li>
      <li><div><strong>Fundamenty</strong><span>Pod każdy słup dół ok. 50 x 50 x 80 cm, poniżej strefy przemarzania. Do 8 słupów - 1 dzień dla 2 osób, powyżej - 2 dni i więcej.</span></div></li>
      <li><div><strong>2-4 tygodnie przerwy</strong><span>Beton dojrzewa. To czas, którego nie da się skrócić bez ryzyka.</span></div></li>
      <li><div><strong>Montaż konstrukcji</strong><span>Wiata do 8 słupów stoi w 1 dzień. Słupy kotwimy w fundamentach.</span></div></li>
      <li><div><strong>Dodatki</strong><span>Kostka wokół słupów, prąd i oświetlenie, ściany i przęsła - jeśli są w zamówieniu.</span></div></li>
    </ol>
  </div>
</section>

<section class="sec sec-zinc">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Od czego zależy cena</h2>
    <ul class="problems">
      <li>Liczba słupów, czyli liczba dołów i ilość betonu.</li>
      <li>Liczba dni pracy dwóch osób: do 8 słupów fundament to 1 dzień, większe wiaty 2 dni i więcej.</li>
      <li>Wywóz ziemi z wykopów.</li>
      <li>Rozebranie i ułożenie z powrotem kostki brukowej wokół słupów.</li>
      <li>Prąd i oświetlenie, ściany boczne i przęsła.</li>
      <li>Dwa przyjazdy ekipy: na fundamenty i na montaż.</li>
    </ul>
    <p class="answer">Montaż z fundamentami zaczyna się od ok. 4 tys. zł. W cenie są też podatki i ryzyko, które bierze na siebie firma. Dokładną kwotę podajemy po zdjęciach i wymiarach.</p>
  </div></div>
</section>

<section class="sec">
  <div class="wrap"><div class="narrow text-block">
    <h2 class="sec-title">Dlaczego nie na kostce</h2>
    <p>Wiaty z marketu często stoją przykręcone do betonowych płyt albo kostki. Przy wichurze lekka konstrukcja może polecieć jak trampolina i narobić szkód u sąsiada. Dlatego słupy zawsze kotwimy w fundamentach poniżej strefy przemarzania. To droższe i trwa dłużej, ale wiata stoi latami.</p>
    <p class="note">Interesuje Cię cała wiata, a nie tylko montaż? Zobacz <a href="/#wymiary">wymiary i ceny</a> albo <a href="/realizacje/">nasze realizacje</a>.</p>
  </div></div>
</section>

<!--PORADNIKI:START-->
<!--PORADNIKI:END-->

<section class="sec">
  <div class="wrap"><div class="narrow">
    <h2 class="sec-title">Pytania o montaż</h2>
{faq}
  </div></div>
</section>

<section class="sec sec-dark" id="kontakt">
  <div class="wrap contact-grid">
    <div>
      <h2 class="sec-title">Zapytaj o termin i wycenę</h2>
      <p class="sec-intro">Napisz, gdzie ma stanąć wiata, ile ma słupów albo jaki masz zestaw. Najlepiej dołącz w wiadomości opis podłoża. Odezwiemy się w ciągu 24 godzin z wolnym terminem.</p>
    </div>
    <div>
    {form(MODULE_OPTIONS, selected="Montaż wiaty z zestawu", placeholder="Miejscowość, rozmiar wiaty, liczba słupów, podłoże (trawa, kostka, beton)", button="Wyślij zapytanie")}
    </div>
  </div>
</section>
</main>
{FOOTER}
{FORM_JS}'''
    return page("Montaż wiat garażowych Mazowsze - fundamenty i montaż od ok. 4000 zł | CarportActive",
                "Montaż wiat garażowych na Mazowszu, także z zestawów innych producentów. Fundamenty poniżej strefy przemarzania, montaż konstrukcji, kostka i prąd. Od ok. 4000 zł.",
                SITE + "/montaz/", body, og_image="/img/realizacje/r05-wiata-z-oswietleniem.jpg", ld=ld)
if __name__ == "__main__":
    os.makedirs("static/montaz", exist_ok=True)
    open("static/montaz/index.html", "w", encoding="utf-8").write(build()); print("ok")

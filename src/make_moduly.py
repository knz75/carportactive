import json, html, os

SITE = "https://carportactive.pl"

M = [
 dict(slug="sportowy", img="sport.jpg", name="Moduł sportowy", opt="Moduł sportowy (drabinka, drążek)",
  title="Wiata garażowa z drabinką szwedzką i drążkiem - moduł sportowy | CarportActive",
  desc="Stalowa wiata z modułem sportowym: drabinka szwedzka, drążek do podciągania i poręcze na słupach wiaty. Zadaszone miejsce do treningu przy domu.",
  cat="Dla aktywnych", h1="Wiata z modułem sportowym",
  lead="Drabinka szwedzka, drążek do podciągania i poręcze przykręcone do słupów wiaty. Masz zadaszone miejsce do treningu przy domu, a w ogrodzie nie stoi osobna konstrukcja.",
  alt="Stalowa wiata garażowa z modułem sportowym - drabinka szwedzka i drążek",
  problems=["Chcesz ćwiczyć w domu, ale w budynku nie ma miejsca na siłownię.",
            "Osobny drążek albo zestaw do ćwiczeń zajmuje kawałek ogrodu.",
            "Ćwiczysz na dworze i deszcz co chwilę przerywa trening."],
  answer="Wiata i tak stoi przy wjeździe. Jej słupy są ze stali konstrukcyjnej, więc mogą przy okazji służyć jako rama do ćwiczeń - pod dachem, obok samochodu.",
  parts=[("Drabinka szwedzka","Rozciąganie, ćwiczenia na brzuch i plecy, rozgrzewka przed bieganiem."),
         ("Drążek","Podciąganie i zwisy na stalowym drążku zamocowanym między słupami."),
         ("Poręcze","Pompki na poręczach i ćwiczenia z ciężarem własnego ciała."),
         ("Ocynk ogniowy","Stal stoi na zewnątrz cały rok, dlatego jest ocynkowana i malowana proszkowo.")],
  size="Najwygodniej przy wiacie 4 × 6 m - obok samochodu zostaje miejsce na trening.",
  faq=[("Czy moduł sportowy można dołożyć później?","Tak. Słupy i fundament wiaty CarportActive mają zapas nośności i przygotowane punkty montażowe, więc moduł możesz zamontować od razu albo w kolejnym sezonie."),
       ("Czy samochód może stać pod wiatą, kiedy ćwiczę?","Tak. Przyrządy montujemy przy słupach z boku, tak żeby nie wchodziły w miejsce parkowania. Dokładne ustawienie dobieramy do rozmiaru wiaty i podjazdu."),
       ("Czy mogę zamówić inne przyrządy niż w zestawie?","Tak, zestaw ustalamy indywidualnie. Napisz, czego potrzebujesz, na przykład kółek gimnastycznych albo uchwytu na worek, a dobierzemy mocowanie.")]),
 dict(slug="panel-narzedziowy", img="diy.jpg", name="Panel narzędziowy", opt="Panel narzędziowy / warsztat",
  title="Wiata z panelem narzędziowym - miejsce na narzędzia przy podjeździe | CarportActive",
  desc="Stalowa wiata z panelem perforowanym na narzędzia: łopaty, grabie, klucze i przedłużacze na hakach pod dachem. Porządek przy wjeździe i miejsce do drobnych napraw.",
  cat="Dla majsterkowiczów", h1="Wiata z panelem narzędziowym",
  lead="Stalowy panel perforowany na bocznej ścianie wiaty. Łopaty, grabie, klucze i przedłużacze wiszą na hakach pod dachem, a podjazd staje się miejscem do drobnych napraw.",
  alt="Wiata samochodowa z panelem narzędziowym i warsztatem",
  problems=["Narzędzia ogrodowe stoją oparte o ścianę domu albo leżą w garażu na kupie.",
            "Zamiast naprawiać, szukasz klucza.",
            "Nie masz garażu ani komórki, gdzie można trzymać narzędzia."],
  answer="Boczna ściana wiaty to gotowe miejsce na panel. Każde narzędzie ma swój hak, wszystko widać od razu i wszystko jest pod dachem, tam gdzie pracujesz.",
  parts=[("Panel perforowany","Stalowa płyta z otworami - haki przekładasz, jak chcesz, i zmieniasz układ, kiedy zmieniają się narzędzia."),
         ("Haki i uchwyty","Na łopaty, grabie, węże ogrodowe, przedłużacze i narzędzia ręczne."),
         ("Skrzynki","Na drobne części, śruby i rzeczy, które łatwo zgubić.")],
  size="Panel pasuje do każdego rozmiaru wiaty. Na wiacie 4 × 6 m z boku zostaje też miejsce na stanowisko pracy.",
  extra='<p class="size-note">Nie masz wiaty albo potrzebujesz miejsca na narzędzia przy drzwiach lub na tarasie? Zobacz wolnostojące <a href="/dodatki/ca-stand/">stojaki na narzędzia CA-Stand</a> w tym samym stylu.</p>',
  faq=[("Czy narzędzia nie zamokną?","Panel jest pod dachem wiaty, więc deszcz nie pada na niego bezpośrednio. Przy silnym wietrze i zacinającym deszczu ściana osłania tylko częściowo - to nie jest zamknięte pomieszczenie."),
       ("Czy panel można zamontować do już stojącej wiaty?","Do wiaty CarportActive tak, ma przygotowane punkty montażowe. Przy wiacie innego producenta prześlij zdjęcia konstrukcji, a sprawdzimy, czy da się go zamocować."),
       ("Czy układ haków można dopasować do moich narzędzi?","Tak. Panel jest perforowany, więc haki i uchwyty ustawiasz sam, a zestaw dobieramy przy wycenie.")]),
 dict(slug="ogrod-wertykalny", img="garden.jpg", name="Ogród wertykalny", opt="Ogród wertykalny",
  title="Wiata z ogrodem wertykalnym - zielona ściana przy wjeździe | CarportActive",
  desc="Stalowa wiata z pionowym ogrodem na bocznym panelu: zioła, kwiaty lub pnącza. Zielona ściana osłania samochód od słońca i wiatru. Opcja nawadniania.",
  cat="Dla zielonych", h1="Wiata z ogrodem wertykalnym",
  lead="Pionowy ogród na bocznym panelu wiaty: zioła, kwiaty albo pnącza. Zielona ściana osłania samochód od słońca i wiatru i wygląda lepiej niż goła stal.",
  alt="Nowoczesny carport z ogrodem wertykalnym na bocznej ścianie",
  problems=["Masz mały ogród i brakuje miejsca na grządki.",
            "Wiata od strony ulicy albo sąsiada wygląda jak goła konstrukcja.",
            "Chcesz mieć zioła blisko kuchni, a nie na końcu działki."],
  answer="Boczna ściana wiaty zajmuje mało miejsca, a ma kilka metrów kwadratowych powierzchni. Wystarczy obsadzić ją roślinami zamiast zostawiać pustą.",
  parts=[("Moduły roślinne","Pojemniki na bocznym panelu wiaty, ustawione jeden nad drugim."),
         ("Opcja nawadniania","W pionie ziemia wysycha szybciej niż na grządce, dlatego można dodać nawadnianie."),
         ("Dowolna roślinność","Zioła, kwiaty sezonowe albo pnącza - zależnie od strony świata i Twojego czasu.")],
  size="Ogród wertykalny pasuje do każdego rozmiaru wiaty. Najlepiej sprawdza się na ścianie od strony słońca albo od strony ulicy.",
  faq=[("Jakie rośliny wybrać?","Zależy od strony świata i tego, ile czasu chcesz poświęcić na pielęgnację. Pnącza są najmniej wymagające, zioła potrzebują słońca i regularnego podlewania."),
       ("Czy trzeba codziennie podlewać?","W upały moduły pionowe wysychają szybciej niż zwykła grządka. Dlatego proponujemy opcję nawadniania - jej zakres ustalamy indywidualnie."),
       ("Czy wilgoć nie zaszkodzi konstrukcji?","Stal wiaty jest ocynkowana ogniowo i malowana proszkowo, czyli przygotowana na deszcz i wilgoć przez cały rok.")]),
 dict(slug="plac-zabaw", img="kids.jpg", name="Plac zabaw", opt="Plac zabaw dla dzieci",
  title="Wiata z placem zabaw - ścianka wspinaczkowa pod dachem | CarportActive",
  desc="Stalowa wiata z zadaszonym placem zabaw: ścianka wspinaczkowa, siatka linowa, liny i mata amortyzująca. Dzieci bawią się w każdą pogodę, trawnik zostaje wolny.",
  cat="Dla rodzin", h1="Wiata z placem zabaw",
  lead="Ścianka wspinaczkowa, siatka linowa i liny gimnastyczne pod dachem wiaty. Dzieci bawią się także w deszczu, a trawnik zostaje wolny.",
  alt="Wiata garażowa z zadaszonym placem zabaw i ścianką wspinaczkową dla dzieci",
  problems=["Klasyczny plac zabaw zajmuje dużą część ogrodu.",
            "Po deszczu dzieci nie mogą wyjść, bo wszystko jest mokre.",
            "Latem zabawki w pełnym słońcu nagrzewają się tak, że nie da się ich dotknąć."],
  answer="Pod dachem wiaty jest sucho i jest cień. Ścianka i liny mocowane do słupów nie zajmują dodatkowego miejsca w ogrodzie.",
  parts=[("Ścianka wspinaczkowa","Chwyty na panelu przy słupie wiaty, ustawione na wysokość dzieci."),
         ("Siatka linowa","Do wspinania i zabawy w zwisach."),
         ("Liny","Liny gimnastyczne zawieszone na stalowej konstrukcji."),
         ("Mata amortyzująca","Miękkie podłoże pod strefą wspinania.")],
  size="Strefę zabaw planujemy z boku, poza miejscem parkowania. Najwięcej miejsca daje wiata 4 × 6 m albo 6 × 6 m.",
  faq=[("Czy dzieci mogą się bawić, kiedy samochód stoi pod wiatą?","Strefę zabaw ustawiamy z boku, poza miejscem parkowania. Mimo to zabawa obok samochodu wymaga uwagi dorosłych, dlatego ustawienie omawiamy przy projekcie."),
       ("Co jest pod ścianką?","Pod strefą wspinania kładziemy matę amortyzującą."),
       ("Co zrobić, kiedy dzieci dorosną?","Mocowania na słupach zostają. Zamiast ścianki możesz zamontować moduł sportowy albo panel narzędziowy.")]),
 dict(slug="przechowalnia-rowerow", img="rower.jpg", name="Przechowalnia rowerów", opt="Przechowalnia rowerów",
  title="Wiata na rowery i samochód - przechowalnia rowerów pod dachem | CarportActive",
  desc="Stalowa wiata z przechowalnią rowerów: wieszaki i stojaki na rowery, hulajnogi i boxy dachowe przykręcone do konstrukcji. Garaż i przedpokój zostają wolne.",
  cat="Dla rowerzystów", h1="Wiata z przechowalnią rowerów",
  lead="Rowery, hulajnogi, boxy dachowe i sprzęt sportowy pod dachem wiaty. Wieszaki i stojaki są przykręcone do konstrukcji, więc garaż i przedpokój zostają wolne.",
  alt="Wiata z zamykaną przechowalnią rowerów i sprzętu sportowego",
  problems=["Rowery stoją w przedpokoju albo blokują garaż.",
            "Box dachowy i sprzęt sezonowy nie mają swojego miejsca.",
            "Rower zostawiony na dworze moknie i rdzewieje."],
  answer="Pod wiatą jest miejsce nie tylko na samochód. Rowery wiszą na ścianie i łańcuch nie rdzewieje na deszczu.",
  parts=[("Wieszaki na rowery","Rowery wiszą na ścianie wiaty i nie zajmują miejsca na podłodze."),
         ("Stojaki","Na rowery dzieci, hulajnogi i rzeczy, które wygodniej postawić."),
         ("Zamknięta strefa","Jeśli chcesz, część wiaty można wydzielić i zamykać.")],
  size="Ile rowerów się zmieści, zależy od rozmiaru wiaty i układu wieszaków. Najwięcej miejsca z boku daje wiata 4 × 6 m.",
  gallery=[("realizacje/r09-schowek-pod-wiata.jpg","Zamykany schowek z drzwiami pod wiatą"),
           ("realizacje/r10-zabudowa-boczna.jpg","Pełna zabudowa boczna wiaty w kolorze antracyt")],
  faq=[("Czy rowery są zabezpieczone przed kradzieżą?","Rower można przypiąć do stalowej konstrukcji wiaty. Jeśli chcesz więcej, można zamówić zamkniętą strefę - jej wykonanie ustalamy przy wycenie."),
       ("Ile rowerów się zmieści?","Napisz, ile masz rowerów i jakich, a dobierzemy wieszaki i stojaki do rozmiaru wiaty."),
       ("Czy można tam też naprawiać rowery?","Tak. Przechowalnię łatwo połączyć z panelem narzędziowym, wtedy narzędzia wiszą obok rowerów.")]),
 dict(slug="solar-box", img="solar.jpg", name="Solar Box (PV)", opt="Solar Box (konstrukcja pod fotowoltaikę PV)",
  title="Carport fotowoltaiczny Solar Box - wiata pod panele PV | CarportActive",
  desc="Solar Box - wzmocniona stalowa wiata pod panele fotowoltaiczne. Od 6 do 12 paneli PV, gotowość pod Wallbox. Miejsce parkingowe produkuje prąd dla domu i auta.",
  cat="Dla oszczędnych", h1="Solar Box - wiata pod fotowoltaikę",
  lead="Wzmocniona wiata, której dach jest konstrukcją pod panele PV. Miejsce parkingowe zaczyna produkować prąd dla domu i samochodu elektrycznego.",
  alt="Carport fotowoltaiczny Solar Box - wiata garażowa pod panele słoneczne PV",
  problems=["Dach domu jest za mały, źle ustawiony albo nie chcesz go dziurawić.",
            "Planujesz samochód elektryczny i chcesz ładować go w domu.",
            "Chcesz zadaszony podjazd i fotowoltaikę w jednej konstrukcji."],
  answer="Dach wiaty i tak jest potrzebny nad samochodem. W wersji Solar Box ma wzmocnioną konstrukcję, która uniesie panele.",
  parts=[("Konstrukcja pod PV","Dach wiaty przygotowany do montażu paneli fotowoltaicznych."),
         ("Od 6 do 12 paneli","Liczba paneli zależy od rozmiaru wiaty."),
         ("Wzmocnione słupy","Słupy i fundament liczone na dodatkowy ciężar paneli."),
         ("Gotowość pod Wallbox","Miejsce na ładowarkę samochodu elektrycznego przy słupie wiaty.")],
  size="Największa połać daje wiata dwustanowiskowa 6 × 6 m - zmieści się na niej do 12 paneli.",
  faq=[("Ile paneli zmieści się na wiacie?","Od 6 do 12, zależnie od rozmiaru. Na wiacie 6 × 6 m zmieści się do 12 paneli."),
       ("Czy mogę postawić wiatę teraz, a panele dołożyć później?","Tak, jeśli zamówisz wersję Solar Box ze wzmocnioną konstrukcją. Panele można zamontować w kolejnym sezonie."),
       ("Kto robi instalację elektryczną?","Zakres prac przy panelach, falowniku i podłączeniu ustalamy przy wycenie. Napisz, czy masz już instalatora, czy szukasz całego rozwiązania.")]),
 dict(slug="przeslo-zaluzjowe", img="realizacje/r03-wiata-przesla-ciemny-orzech.jpg", name="Przęsło żaluzjowe", opt="Przęsło żaluzjowe (osłona boczna)",
  title="Przęsło żaluzjowe do wiaty - osłona boczna orzech lub antracyt | CarportActive",
  desc="Przęsła żaluzjowe do stalowej wiaty: boczna osłona od sąsiada, ulicy i wiatru. Kolor orzech, ciemny orzech albo antracyt RAL 7016, w stylu wiaty.",
  cat="Dla prywatności", h1="Wiata z przęsłami żaluzjowymi",
  lead="Przęsła z poziomymi lamelami między słupami wiaty. Zasłaniają samochód i podjazd od sąsiada i ulicy, a z boku nie wieje tak jak pod samym dachem.",
  alt="Wiata CarportActive z przęsłami żaluzjowymi w kolorze ciemny orzech",
  problems=["Sąsiad albo ulica widzą wszystko, co dzieje się na podjeździe.",
            "Wiatr wdmuchuje pod wiatę deszcz i śnieg z boku.",
            "Goła konstrukcja nie pasuje do drewnianej bramy garażowej albo elewacji."],
  answer="Przęsła montujemy między słupami tej samej wiaty, na jednym boku albo na kilku. Kolor dobierasz do domu: drewniany orzech, ciemny orzech albo antracyt jak sama konstrukcja.",
  parts=[("Lamele żaluzjowe","Poziome lamele zasłaniają z boku, a między nimi przechodzi powietrze."),
         ("Orzech","Ciepły kolor drewna, pasuje do drewnianych bram i elementów elewacji."),
         ("Ciemny orzech","Ciemniejszy odcień drewna, spokojniejszy przy szarych elewacjach."),
         ("Antracyt RAL 7016","Ten sam kolor co konstrukcja wiaty - jednolita, nowoczesna bryła.")],
  size="Przęsła pasują do każdego rozmiaru wiaty. Liczbę i miejsce przęseł ustalamy przy wycenie.",
  gallery=[("realizacje/r01-wiata-przesla-orzech.jpg","Wiata dwustanowiskowa z przęsłami w kolorze orzech"),
           ("realizacje/r02-wiata-orzech-przy-domu.jpg","Wiata przy domu z przęsłami w kolorze orzech"),
           ("realizacje/r13-przeslo-orzech-przy-domu.jpg","Przęsło orzech przy wiacie i dopasowana osłona na ścianie domu")],
  faq=[("Czy przęsła można dołożyć do stojącej wiaty?","Do wiaty CarportActive tak, montujemy je między słupami. Przy wiacie innego producenta prześlij zdjęcia, a sprawdzimy, czy da się je zamocować."),
       ("Czy mogę zasłonić tylko jeden bok?","Tak. Przęsła możesz zamówić na jeden bok, na tył albo na kilka stron - zależnie od tego, skąd chcesz się zasłonić."),
       ("Jakie kolory są dostępne?","Orzech, ciemny orzech i antracyt RAL 7016. Kolor dobieramy przy wycenie, także pod bramę garażową czy elewację.")]),
 dict(slug="zamknieta-wiata", img="realizacje/z01-wiata-zamknieta-brama-od-srodka.jpg", name="Zamknięta wiata", opt="Zamknięta wiata (ściany i brama)",
  title="Zamknięta wiata zamiast blaszaka - ściany, brama, wersja przelotowa | CarportActive",
  desc="Stalowa wiata obudowana ścianami i zamykana bramą segmentową lub roletową. Ściany z żaluzji bez szczelin, blachy falistej albo płyty PIR. Także wersja przelotowa.",
  cat="Zamiast blaszaka", h1="Zamknięta wiata zamiast blaszaka",
  lead="Ta sama stalowa konstrukcja co wiata, tylko obudowana ścianami i zamykana bramą. Wygląda jak część domu, a nie jak blaszak z ogłoszenia.",
  alt="Zamknięta wiata z bramą segmentową - widok od środka na otwartą bramę",
  problems=["Blaszak nie pasuje do nowoczesnego domu, a zwykła wiata nie zamyka się na klucz.",
            "Pod otwartą wiatę wchodzą kuny, koty i nawiewa liście.",
            "Potrzebujesz przejazdu na tył działki, a nie ma miejsca na drugi wjazd."],
  answer="Zamknięta wiata stoi na fundamentach jak każda nasza wiata. Ściany dobierasz do potrzeb, a bramę można dać z jednej albo z dwóch stron - wtedy po otwarciu przejeżdżasz na wylot.",
  parts=[("Żaluzja bez szczelin","Ściana z lamel ułożonych tak, że nie ma prześwitów - szczelna jak blacha falista, a wygląda nowocześnie. Kuna nie wejdzie."),
         ("Blacha falista","Najprostsza i najtańsza obudowa ścian."),
         ("Płyta PIR 5 cm","Płyta z izolacją - tam, gdzie ma być schowek albo mniej skraplania na ścianach."),
         ("Brama segmentowa lub roletowa","Montujemy bramy segmentowe (np. Hörmann) i roletowe (np. Portos), także z napędem."),
         ("Wersja przelotowa","Brama z przodu i z tyłu - po otwarciu obu można przejechać na wylot."),
         ("Dach z antykondensatem","Blacha dachowa z powłoką antykondensacyjną, żeby z sufitu nie kapało.")],
  size="Zamkniętą wiatę liczymy indywidualnie: wymiar, rodzaj ścian, liczba bram, pomieszczenie gospodarcze. Wycena po pomiarze na miejscu.",
  gallery=[("realizacje/z02-wiata-przelotowa-dwie-bramy.jpg","Wiata przelotowa - brama z przodu i z tyłu, widok na wylot"),
           ("realizacje/z03-wiata-zamknieta-z-brama-segmentowa.jpg","Zamknięta wiata z bramą segmentową i ścianą z żaluzji"),
           ("realizacje/z04-sciana-zaluzja-bez-szczelin.jpg","Ściana z żaluzji bez szczelin - kuna nie wejdzie")],
  faq=[("Czym zamknięta wiata różni się od garażu blaszanego?","Konstrukcją i wykonaniem. U nas słupy 100 x 100 x 3 mm stoją w fundamentach poniżej strefy przemarzania, a ściany i brama są dobrane do domu. Blaszak to zwykle cienka blacha na lekkim profilu, często przykręcony do podłoża."),
       ("Czy w środku nie będzie się skraplać woda?","Dach ma powłokę antykondensacyjną. Ściany z samej blachy mogą się pocić w chłodne dni, dlatego tam, gdzie ma być schowek, proponujemy płytę PIR."),
       ("Czy można zrobić bramę z dwóch stron?","Tak. W wersji przelotowej brama jest z przodu i z tyłu, więc po otwarciu można przejechać na tył działki."),
       ("Ile kosztuje zamknięta wiata?","To projekt indywidualny: cena zależy od wymiaru, ścian, liczby i rodzaju bram. Podajemy ją po pomiarze na miejscu.")]),
]

def e(s): return html.escape(s, quote=True)

HEAD_FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;700&family=Barlow+Condensed:wght@700;800&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/css/pages.css">'''

FORM_JS = '''<script>
async function submitForm(e) {
  e.preventDefault();
  const name = document.getElementById('f-name').value.trim();
  const contact = document.getElementById('f-contact').value.trim();
  const rodo = document.getElementById('f-rodo').checked;
  if (!name || !contact || !rodo) return;
  const btn = document.querySelector('.cta-submit');
  const fd = new FormData();
  fd.append('name', name);
  fd.append('contact', contact);
  fd.append('module', document.getElementById('f-module').value);
  fd.append('msg', document.getElementById('f-msg').value.trim());
  btn.disabled = true;
  try {
    const r = await fetch('/wizualizacja/api/contact', { method: 'POST', body: fd });
    if (!r.ok) throw new Error();
    document.querySelector('.cta-form').style.display = 'none';
    document.getElementById('form-ok').style.display = 'block';
  } catch {
    btn.disabled = false;
    alert('Nie udało się wysłać zapytania. Sprawdź połączenie i spróbuj ponownie.');
  }
}
</script>'''

ALL_OPTS = [m["opt"] for m in M] + ["Kilka modułów - omówię szczegóły"]

def page(m):
    url = f"{SITE}/moduly/{m['slug']}/"
    ld = {"@context":"https://schema.org","@graph":[
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"CarportActive","item":SITE+"/"},
            {"@type":"ListItem","position":2,"name":"Moduły","item":SITE+"/#moduly"},
            {"@type":"ListItem","position":3,"name":m["name"],"item":url}]},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,
            "acceptedAnswer":{"@type":"Answer","text":a}} for q,a in m["faq"]]}]}
    problems = "\n".join(f"      <li>{e(p)}</li>" for p in m["problems"])
    parts = "\n".join(f'      <div class="part"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t,d in m["parts"])
    faq = "\n".join(f'    <details class="faq-item"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in m["faq"])
    others = "\n".join(f'      <a class="other" href="/moduly/{o["slug"]}/"><img src="/img/{o["img"]}" alt="{e(o["alt"])}" width="400" height="300" loading="lazy" decoding="async"><span>{e(o["name"])}</span></a>' for o in M if o is not m)
    opts = "\n".join(f'        <option{" selected" if o==m["opt"] else ""}>{e(o)}</option>' for o in ALL_OPTS)
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(m["title"])}</title>
<meta name="description" content="{e(m["desc"])}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(m["h1"])} | CarportActive">
<meta property="og:description" content="{e(m["desc"])}">
<meta property="og:image" content="{SITE}/img/{m["img"]}">
<meta property="og:locale" content="pl_PL">
{HEAD_FONTS}
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>

<header class="top-nav">
  <a href="/" class="brand-logo">Carport<span>Active</span></a>
  <nav class="nav-links" aria-label="Główna nawigacja">
    <a href="/#moduly">Moduły</a>
    <a href="/#wymiary">Wymiary</a>
    <a href="/ai/">Wizualizacja AI</a>
    <a href="#kontakt">Wycena</a>
  </nav>
</header>

<main>
<nav class="crumbs" aria-label="Ścieżka"><a href="/">CarportActive</a><span>/</span><a href="/#moduly">Moduły</a><span>/</span>{e(m["name"])}</nav>

<section class="p-hero">
  <div class="p-hero-text">
    <div class="p-cat">{e(m["cat"])}</div>
    <h1>{e(m["h1"])}</h1>
    <p class="p-lead">{e(m["lead"])}</p>
    <div class="p-actions">
      <a class="btn btn-green" href="#kontakt">Zapytaj o wycenę</a>
      <a class="btn btn-line" href="/ai/"><span class="dot"></span>Zobacz wiatę na swoim podwórku (AI)</a>
    </div>
  </div>
  <div class="p-hero-img"><img src="/img/{m["img"]}" alt="{e(m["alt"])}" width="800" height="560" decoding="async"></div>
</section>

<section class="sec">
  <div class="sec-inner">
    <h2>Kiedy to się przydaje</h2>
    <ul class="problems">
{problems}
    </ul>
    <p class="problems-answer">{e(m["answer"])}</p>
  </div>
</section>

<section class="sec sec-light">
  <div class="sec-inner">
    <h2>Co wchodzi w skład</h2>
    <div class="parts">
{parts}
    </div>
  </div>
</section>

<section class="sec">
  <div class="sec-inner text-block">
    <h2>Jak to działa z wiatą</h2>
    <p>Moduł mocujemy do słupów wiaty ze stali konstrukcyjnej S235. Słupy i fundament mają zapas nośności i przygotowane punkty montażowe, więc moduł możesz zamówić razem z wiatą albo dołożyć za rok, bez przeróbek i cięcia stali.</p>
    <p>Całość jest ocynkowana ogniowo i malowana proszkowo. Wiatę montujemy na stopach fundamentowych albo na istniejącej płycie lub kostce, a sam montaż zajmuje zazwyczaj 1 dzień roboczy.</p>
    <p class="size-note">{e(m["size"])} <a href="/#wymiary">Zobacz wymiary wiat</a></p>
    {m.get("extra","")}
  </div>
</section>

<!--PORADNIKI:START-->
<!--PORADNIKI:END-->

<section class="sec sec-light">
  <div class="sec-inner">
    <h2>Pytania o {e(m["name"].lower())}</h2>
{faq}
  </div>
</section>

<section class="sec">
  <div class="sec-inner">
    <h2>Inne moduły</h2>
    <div class="others">
{others}
    </div>
  </div>
</section>

<section class="cta-section" id="kontakt">
  <div class="cta-left">
    <h2>Zapytaj o wiatę z tym modułem</h2>
    <p>Napisz, jaki rozmiar Cię interesuje i gdzie ma stanąć wiata. Odezwiemy się w ciągu 24 godzin z propozycją techniczną oraz wyceną.</p>
    <p style="margin-top:16px">Masz zdjęcie podjazdu? <a class="ai-link" href="/ai/">Wgraj je - wizualizator AI pokaże wiatę na Twoim podwórku w 3 wariantach</a>.</p>
  </div>
  <div>
    <form class="cta-form" onsubmit="submitForm(event)">
      <input type="text" id="f-name" name="name" placeholder="Imię i nazwisko" aria-label="Imię i nazwisko" required>
      <input type="text" id="f-contact" name="contact" placeholder="Telefon lub e-mail" aria-label="Telefon lub e-mail" required>
      <select id="f-module" name="module" aria-label="Wybierz moduł">
        <option value="">Wybierz główny moduł / wariant</option>
{opts}
      </select>
      <textarea id="f-msg" name="msg" placeholder="Wymiary (np. 4x6 m), lokalizacja montażu, dodatkowe pytania" aria-label="Wiadomość"></textarea>
      <label class="rodo-label">
        <input type="checkbox" id="f-rodo" required>
        <span>Zgadzam się na przetwarzanie moich danych osobowych w celu przygotowania wyceny i kontaktu w sprawie oferty.</span>
      </label>
      <button type="submit" class="cta-submit">Wyślij zapytanie o wycenę</button>
    </form>
    <div class="form-ok" id="form-ok">Dziękujemy! Odezwiemy się w ciągu 24 godzin.</div>
  </div>
</section>
</main>

<footer>
  <div class="footer-brand">Carport<span>Active</span></div>
  <div class="footer-copy">© 2026 CarportActive - stalowe wiaty modułowe S235 - Polska</div>
  <div class="footer-links">
    <a href="/">Strona główna</a>
    <a href="/ai/">Wizualizacja AI</a>
    <a href="/#wymiary">Wymiary</a>
    <a href="#kontakt">Kontakt</a>
  </div>
</footer>

<a class="ai-float" href="/ai/" aria-label="Zobacz wiatę na swoim podwórku - wizualizacja AI">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 8h3l2-3h8l2 3h3v12H3z"/><circle cx="12" cy="13" r="4"/></svg>
  Twoja wiata AI
</a>

{FORM_JS}
</body>
</html>
'''

if __name__ == "__main__":
  for m in M:
    d = f"static/moduly/{m['slug']}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html","w",encoding="utf-8").write(page(m))
  print("ok", [m["slug"] for m in M])

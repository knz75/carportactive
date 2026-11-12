import html, json, os

SITE = "https://carportactive.pl"
def e(s): return html.escape(s, quote=True)

HEAD = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/css/site.css">'''

def header(active=""):
    items = [("/#moduly", "Moduły", "moduly"), ("/realizacje/", "Realizacje", "realizacje"), ("/montaz/", "Montaż", "montaz"), ("/dodatki/ca-stand/", "Stojaki", "stojaki"),
             ("/poradnik/", "Poradnik", "poradnik"), ("/ai/", "Wizualizacja AI", "ai")]
    links = "\n      ".join(f'<a href="{u}"{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for u, t, k in items)
    return f'''<header class="site-head">
  <div class="wrap">
    <a class="logo" href="/">Carport<span>Active</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu" onclick="var m=document.getElementById('menu');var o=m.classList.toggle('open');this.setAttribute('aria-expanded',o);this.textContent=o?'Zamknij':'Menu'">Menu</button>
    <nav class="menu" id="menu" aria-label="Główna nawigacja">
      {links}
      <a class="btn btn-green btn-small" href="/#kontakt">Wycena</a>
    </nav>
  </div>
</header>'''

FOOTER = '''<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="/">Carport<span>Active</span></a>
        <p style="margin-top:12px;max-width:360px">Stalowe wiaty modułowe ze stali S235. Projektujemy, spawamy i montujemy w całej Polsce.</p>
      </div>
      <div>
        <h3>Moduły</h3>
        <ul>
          <li><a href="/moduly/sportowy/">Moduł sportowy</a></li>
          <li><a href="/moduly/panel-narzedziowy/">Panel narzędziowy</a></li>
          <li><a href="/moduly/ogrod-wertykalny/">Ogród wertykalny</a></li>
          <li><a href="/moduly/plac-zabaw/">Plac zabaw</a></li>
          <li><a href="/moduly/przechowalnia-rowerow/">Przechowalnia rowerów</a></li>
          <li><a href="/moduly/solar-box/">Solar Box (PV)</a></li>
          <li><a href="/moduly/przeslo-zaluzjowe/">Przęsło żaluzjowe</a></li>
        </ul>
      </div>
      <div>
        <h3>Strona</h3>
        <ul>
          <li><a href="/realizacje/">Realizacje</a></li>
          <li><a href="/montaz/">Montaż wiat</a></li>
          <li><a href="/dodatki/ca-stand/">Stojaki CA-Stand</a></li>
          <li><a href="/poradnik/">Poradnik</a></li>
          <li><a href="/ai/">Wizualizacja AI</a></li>
          <li><a href="/#wymiary">Wymiary</a></li>
          <li><a href="/#kontakt">Kontakt i wycena</a></li>
        </ul>
      </div>
    </div>
    <div class="copy">© 2026 CarportActive - stalowe wiaty modułowe S235 - Polska</div>
  </div>
</footer>'''

FORM_JS = '''<script>
async function submitForm(e) {
  e.preventDefault();
  const name = document.getElementById('f-name').value.trim();
  const contact = document.getElementById('f-contact').value.trim();
  const rodo = document.getElementById('f-rodo').checked;
  if (!name || !contact || !rodo) return;
  const btn = document.querySelector('.form button[type=submit]');
  const fd = new FormData();
  fd.append('name', name);
  fd.append('contact', contact);
  fd.append('module', document.getElementById('f-module').value);
  fd.append('msg', document.getElementById('f-msg').value.trim());
  btn.disabled = true;
  try {
    const r = await fetch('/wizualizacja/api/contact', { method: 'POST', body: fd });
    if (!r.ok) throw new Error();
    document.querySelector('.form').style.display = 'none';
    document.getElementById('form-ok').style.display = 'block';
  } catch {
    btn.disabled = false;
    alert('Nie udało się wysłać zapytania. Sprawdź połączenie i spróbuj ponownie.');
  }
}
</script>'''

def form(options, selected="", placeholder="Wymiary (np. 4x6 m), miejscowość, pytania", button="Wyślij zapytanie"):
    opts = "\n".join(f'        <option{" selected" if o == selected else ""}>{e(o)}</option>' for o in options)
    return f'''<form class="form" onsubmit="submitForm(event)">
      <input type="text" id="f-name" name="name" placeholder="Imię i nazwisko" aria-label="Imię i nazwisko" required>
      <input type="text" id="f-contact" name="contact" placeholder="Telefon lub e-mail" aria-label="Telefon lub e-mail" required>
      <select id="f-module" name="module" aria-label="Co Cię interesuje">
        <option value="">Co Cię interesuje?</option>
{opts}
      </select>
      <textarea id="f-msg" name="msg" placeholder="{e(placeholder)}" aria-label="Wiadomość"></textarea>
      <label class="rodo"><input type="checkbox" id="f-rodo" required><span>Zgadzam się na przetwarzanie moich danych osobowych w celu przygotowania wyceny i kontaktu w sprawie oferty.</span></label>
      <button type="submit" class="btn btn-green">{e(button)}</button>
    </form>
    <div class="form-ok" id="form-ok">Dziękujemy! Odezwiemy się w ciągu 24 godzin.</div>'''

MODULE_OPTIONS = ["Moduł sportowy (drabinka, drążek)", "Solar Box (konstrukcja pod fotowoltaikę PV)",
                  "Panel narzędziowy / warsztat", "Ogród wertykalny", "Plac zabaw dla dzieci",
                  "Przechowalnia rowerów", "Przęsło żaluzjowe (osłona boczna)", "Stojak na narzędzia CA-Stand", "Montaż wiaty z zestawu", "Kilka modułów - omówię szczegóły"]

def page(title, desc, canonical, body, robots="index, follow", og_image="/img/solar.jpg", og_type="website", ld=None, extra_head=""):
    ldj = f'<script type="application/ld+json">\n{json.dumps(ld, ensure_ascii=False)}\n</script>' if ld else ""
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:locale" content="pl_PL">
{HEAD}
{ldj}{extra_head}
</head>
<body>
{body}
</body>
</html>
'''

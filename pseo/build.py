# python build.py --preview      podgląd kolejki w /podglad/ (noindex, bez sitemap)
# python build.py --publish 5    wydaje 5 artykułów z kolejki i przebudowuje stronę
# python build.py                tylko przebudowa (np. po zmianie szablonu)
import json, os, sys, glob, html, shutil, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(os.path.dirname(HERE), "static")
KOLEJKA = os.path.join(HERE, "kolejka")
WYDANE = os.path.join(HERE, "wydane")
SITE = "https://carportactive.pl"
FACTS = json.load(open(os.path.join(HERE, "facts.json"), encoding="utf-8"))
BASE_URLS = ["/", "/ai/", "/moduly/sportowy/", "/moduly/panel-narzedziowy/", "/moduly/ogrod-wertykalny/",
             "/moduly/plac-zabaw/", "/moduly/przechowalnia-rowerow/", "/moduly/solar-box/", "/moduly/przeslo-zaluzjowe/", "/moduly/zamknieta-wiata/", "/dodatki/ca-stand/", "/realizacje/", "/montaz/", "/okolice/"]

def e(s): return html.escape(s, quote=True)

def load(d):
    out = [json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(d, "*.json"))]
    return out

from article_tpl import article_html, index_html, home_guides
import urllib.request

INDEXNOW_KEY = "37f97a6be16daeadecd4856bbbbde7c3"

def indexnow(urls):
    """Wysyła adresy do Bing i innych wyszukiwarek przez IndexNow. Błąd nie zatrzymuje budowania."""
    if not urls:
        return "brak adresów"
    data = json.dumps({"host": "carportactive.pl", "key": INDEXNOW_KEY,
                       "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt", "urlList": urls[:10000]}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=data,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return f"IndexNow: {r.status} ({len(urls)} adresów)"
    except Exception as ex:
        return f"IndexNow: błąd {ex}"

def render(arts, folder, base, noindex):
    out = os.path.join(STATIC, folder)
    if os.path.isdir(out): shutil.rmtree(out)
    os.makedirs(out)
    arts = sorted(arts, key=lambda a: (a.get("wydano", ""), a["nr"]), reverse=True)
    for a in arts:
        rel = [r for r in arts if r["link"] == a["link"] and r is not a][:4]
        d = os.path.join(out, a["adres"]); os.makedirs(d)
        robots = "noindex, nofollow" if noindex else "index, follow"
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(article_html(a, FACTS[a["link"]], rel, base, robots))
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(index_html(arts, FACTS, base, "noindex, nofollow" if noindex else "index, follow"))
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
            block = '\n<section class="sec sec-paper"><div class="wrap"><div class="narrow"><h2 class="sec-title">Poradnik</h2><ul class="link-list">' + \
                    "".join(f'<li><a href="/poradnik/{a["adres"]}/">{e(a["tytul"])}</a></li>' for a in items) + "</ul></div></div></section>\n"
        s = s[:s.index(a0) + len(a0)] + block + s[s.index(a1):]
        open(p, "w", encoding="utf-8").write(s)
    p = os.path.join(STATIC, "index.html")
    s = open(p, encoding="utf-8").read()
    a0, a1 = "<!--PORADNIK-HOME:START-->", "<!--PORADNIK-HOME:END-->"
    if a0 in s and a1 in s:
        s = s[:s.index(a0) + len(a0)] + home_guides(arts) + s[s.index(a1):]
        open(p, "w", encoding="utf-8").write(s)

def sitemap(arts):
    today = datetime.date.today().isoformat()
    extra = sorted(f"/{sec}/" + os.path.basename(os.path.dirname(x)) + "/" for sec in ("realizacje", "okolice") for x in glob.glob(os.path.join(STATIC, sec, "*", "index.html")))
    rows = [f"  <url><loc>{SITE}{u}</loc></url>" for u in BASE_URLS + extra]
    if arts:
        rows.append(f"  <url><loc>{SITE}/poradnik/</loc><lastmod>{today}</lastmod></url>")
        rows += [f"  <url><loc>{SITE}/poradnik/{a['adres']}/</loc><lastmod>{a['wydano']}</lastmod></url>" for a in arts]
    open(os.path.join(STATIC, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--publish", type=int, default=0)
    ap.add_argument("--indexnow-all", action="store_true")
    a = ap.parse_args()
    if a.preview:
        q = load(KOLEJKA)
        render(q, "podglad", "/podglad/", True)
        print("podgląd:", len(q), "artykułów -> https://carportactive.pl/podglad/")
        return
    os.makedirs(WYDANE, exist_ok=True)
    wydane_teraz = []
    if a.publish:
        q = sorted(load(KOLEJKA), key=lambda x: x.get("kolejnosc", x["nr"]))
        today = datetime.date.today().isoformat()
        for x in q[:a.publish]:
            wydane_teraz.append(x)
            x["wydano"] = today
            json.dump(x, open(os.path.join(WYDANE, x["adres"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.remove(os.path.join(KOLEJKA, x["adres"] + ".json"))
            print("wydano:", x["adres"])
    arts = load(WYDANE)
    if arts:
        arts = render(arts, "poradnik", "/poradnik/", False)
    update_module_pages(arts)
    sitemap(arts)
    w_kolejce = len(load(KOLEJKA))
    if a.indexnow_all:
        import re as _re
        urls = _re.findall(r"<loc>(.*?)</loc>", open(os.path.join(STATIC, "sitemap.xml"), encoding="utf-8").read())
        print(indexnow(urls))
    inx = ""
    if a.publish and wydane_teraz:
        urls = [f"{SITE}/poradnik/{x['adres']}/" for x in wydane_teraz] + [f"{SITE}/poradnik/", f"{SITE}/"] + \
               sorted(set(SITE + FACTS[x["link"]]["url"] for x in wydane_teraz))
        inx = indexnow(sorted(set(urls)))
        print(inx)
    print("na stronie:", len(arts), "| w kolejce:", w_kolejce)
    if a.publish:
        head = f"Poradnik CarportActive: +{len(wydane_teraz)} | na stronie: {len(arts)} | w kolejce: {w_kolejce}"
        if inx:
            head += "\n" + inx
        if not wydane_teraz:
            head += "\nKolejka jest pusta - nic nie wydano."
        body = "\n\n".join(f"{x['tytul']}\n{SITE}/poradnik/{x['adres']}/" for x in wydane_teraz)
        open(os.path.join(HERE, "ostatni.txt"), "w", encoding="utf-8").write(head + ("\n\n" + body if body else ""))

if __name__ == "__main__":
    main()

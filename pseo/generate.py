# Generuje artykuły do kolejki: python generate.py --limit 10
# Poprawka cen: python generate.py --redo-ceny  (przepisuje artykuły o wiacie, w których cena nie pasuje do tematu)
import csv, json, os, sys, time, re, argparse, datetime
from pydantic import BaseModel
from google import genai
from google.genai import types

MODEL = "gemini-3.8-flash"
HERE = os.path.dirname(os.path.abspath(__file__))
KOLEJKA = os.path.join(HERE, "kolejka")
WYDANE = os.path.join(HERE, "wydane")
FACTS = json.load(open(os.path.join(HERE, "facts.json"), encoding="utf-8"))

class Sekcja(BaseModel):
    h2: str
    akapity: list[str]

class Pytanie(BaseModel):
    pytanie: str
    odpowiedz: str

class Artykul(BaseModel):
    tytul: str
    opis_meta: str
    wstep: str
    sekcje: list[Sekcja]
    rozwiazanie: str
    faq: list[Pytanie]

PROMPT = """Napisz artykuł poradnikowy po polsku na stronę firmy CarportActive (stalowe wiaty garażowe z modułami).

Temat (to wpisuje człowiek w Google): {temat}

Czytelnik ma konkretny problem i szuka praktycznej odpowiedzi. Najpierw daj mu tę odpowiedź, uczciwie i konkretnie, tak jakby tłumaczył doświadczony monter, który widział wiele podwórek. Dopiero na końcu, w polu "rozwiazanie", krótko pokaż, jak ten problem rozwiązuje: {produkt}.

Fakty o produkcie (używaj tylko tych, nic nie dopisuj):
{fakty}
{notatki}
Zasady:
- Prosty, naturalny język, zdania krótkie, zwracaj się do czytelnika na "Ty".
- Artykuł ma pomóc także komuś, kto nic nie kupi. Większość tekstu to porady ogólne, nie reklama.
- Nie wymyślaj cen, liczb, statystyk, norm, nazw firm ani przepisów. Ceny i liczby podawaj tylko te, które są w faktach albo w notatkach montera. Nie pisz o pozwoleniach na budowę ani o prawie budowlanym.
- Nie obiecuj niczego, czego nie ma w faktach o produkcie.
- Nie używaj długiej pauzy (—) ani półpauzy (–), tylko zwykły łącznik (-).
- Bez wykrzykników, bez słów typu "rewolucyjny", "idealny", "niesamowity".

Struktura:
- tytul: tytuł artykułu, bliski tematowi, do 70 znaków.
- opis_meta: opis do Google, 130-155 znaków.
- wstep: 2-3 zdania, od razu do rzeczy.
- sekcje: 3-5 sekcji, każda z nagłówkiem h2 i 1-3 akapitami po 2-5 zdań.
- rozwiazanie: 2-4 zdania o produkcie, tylko na podstawie faktów.
- faq: 3 krótkie pytania i odpowiedzi związane z tematem.
"""

def load_topics():
    rows = list(csv.DictReader(open(os.path.join(HERE, "tematy.csv"), encoding="utf-8-sig"), delimiter=";"))
    by = {}
    for r in rows:
        by.setdefault(r["link do"], []).append(r)
    order = []  # na zmianę z każdego modułu
    while any(by.values()):
        for k in list(by):
            if by[k]:
                order.append(by[k].pop(0))
    for i, r in enumerate(order):
        r["k"] = i
    return order

def clean(s):
    return re.sub(r"\s*[—–]\s*", " - ", s).strip()

def notes_for(r, f):
    n = list(f.get("notatki", []))
    if r["adres"] in f.get("ceny_tematy", []):
        n += f.get("notatki_ceny", [])
    if not n:
        return ""
    return ("\nNotatki montera z naszych montaży (to najcenniejsza część: wykorzystaj konkrety, które pasują do tematu, "
            "opisz je własnymi słowami jako doświadczenie z montaży, nie cytuj wszystkich na siłę):\n" +
            "\n".join("- " + x for x in n) + "\n")

def gen_one(client, cfg, r):
    f = FACTS[r["link do"]]
    prompt = PROMPT.format(temat=r["temat"], produkt=f["h1"], fakty="\n".join("- " + x for x in f["facts"]), notatki=notes_for(r, f))
    for proba in range(4):
        try:
            resp = client.models.generate_content(model=MODEL, contents=prompt, config=cfg)
            art = Artykul.model_validate_json(resp.text)
            break
        except Exception as e:
            print("  powtórka", proba + 1, type(e).__name__, str(e)[:120]); time.sleep(10 * (proba + 1))
    else:
        return None
    d = art.model_dump()
    for k in ("tytul", "opis_meta", "wstep", "rozwiazanie"):
        d[k] = clean(d[k])
    for s in d["sekcje"]:
        s["h2"] = clean(s["h2"]); s["akapity"] = [clean(p) for p in s["akapity"]]
    for q in d["faq"]:
        q["pytanie"] = clean(q["pytanie"]); q["odpowiedz"] = clean(q["odpowiedz"])
    txt = json.dumps(d, ensure_ascii=False).lower()
    uwagi = [w for w in ("pozwoleni", "prawo budowlane", "!") if w in txt]
    uwagi += sorted(set(re.findall(r"\d[\d ,.]*\s?(?:tys\.\s?)?zł", txt)))
    d.update({"nr": int(r["nr"]), "kolejnosc": r["k"], "temat": r["temat"], "adres": r["adres"], "link": r["link do"],
              "wygenerowano": datetime.date.today().isoformat(), "uwagi": uwagi})
    return d

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--redo-ceny", action="store_true")
    a = ap.parse_args()
    os.makedirs(KOLEJKA, exist_ok=True); os.makedirs(WYDANE, exist_ok=True)
    topics = load_topics()
    client = genai.Client()
    cfg = types.GenerateContentConfig(response_mime_type="application/json", response_schema=Artykul, temperature=0.7)

    if a.redo_ceny:
        by = {r["adres"]: r for r in topics}
        fixed = 0
        for d in (KOLEJKA, WYDANE):
            for fn in sorted(os.listdir(d)):
                if not fn.endswith(".json"): continue
                p = os.path.join(d, fn); old = json.load(open(p, encoding="utf-8"))
                f = FACTS.get(old["link"], {})
                if not f.get("ceny_tematy") or old["adres"] in f["ceny_tematy"]: continue
                if not any("zł" in u for u in old.get("uwagi", [])): continue
                new = gen_one(client, cfg, by[old["adres"]])
                if not new:
                    print("POMINIĘTO", old["adres"]); continue
                new["kolejnosc"] = old.get("kolejnosc", new["kolejnosc"])
                if "wydano" in old: new["wydano"] = old["wydano"]
                json.dump(new, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                fixed += 1
                print("POPRAWIONO", ("(wydany) " if d == WYDANE else "") + old["adres"], ("UWAGA: " + ", ".join(new["uwagi"])) if new["uwagi"] else "")
        print("poprawiono:", fixed)
        return

    done = set(f[:-5] for d in (KOLEJKA, WYDANE) for f in os.listdir(d) if f.endswith(".json"))
    todo = [r for r in topics if r["adres"] not in done and not FACTS[r["link do"]].get("pending")]
    made = 0
    for r in todo[:a.limit]:
        d = gen_one(client, cfg, r)
        if not d:
            print("POMINIĘTO", r["adres"]); continue
        json.dump(d, open(os.path.join(KOLEJKA, r["adres"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        made += 1
        print("OK", r["adres"], ("UWAGA: " + ", ".join(d["uwagi"])) if d["uwagi"] else "")
    print("gotowe:", made, "| w kolejce:", len(os.listdir(KOLEJKA)))

if __name__ == "__main__":
    main()

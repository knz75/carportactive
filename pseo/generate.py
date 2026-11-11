# Generuje artykuły do kolejki: python generate.py --limit 10
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

Zasady:
- Prosty, naturalny język, zdania krótkie, zwracaj się do czytelnika na "Ty".
- Artykuł ma pomóc także komuś, kto nic nie kupi. Większość tekstu to porady ogólne, nie reklama.
- Nie wymyślaj cen, liczb, statystyk, norm, nazw firm ani przepisów. Nie pisz o pozwoleniach na budowę ani o prawie budowlanym.
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
    return order

def clean(s):
    return re.sub(r"\s*[—–]\s*", " - ", s).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    a = ap.parse_args()
    os.makedirs(KOLEJKA, exist_ok=True); os.makedirs(WYDANE, exist_ok=True)
    done = set(f[:-5] for d in (KOLEJKA, WYDANE) for f in os.listdir(d) if f.endswith(".json"))
    topics = load_topics()
    for i, r in enumerate(topics): r["k"] = i
    todo = [r for r in topics if r["adres"] not in done and not FACTS[r["link do"]].get("pending")]
    client = genai.Client()
    cfg = types.GenerateContentConfig(response_mime_type="application/json", response_schema=Artykul, temperature=0.7)
    made = 0
    for r in todo[:a.limit]:
        f = FACTS[r["link do"]]
        prompt = PROMPT.format(temat=r["temat"], produkt=f["h1"], fakty="\n".join("- " + x for x in f["facts"]))
        for proba in range(4):
            try:
                resp = client.models.generate_content(model=MODEL, contents=prompt, config=cfg)
                art = Artykul.model_validate_json(resp.text)
                break
            except Exception as e:
                print("  powtórka", proba + 1, type(e).__name__, str(e)[:120]); time.sleep(10 * (proba + 1))
        else:
            print("POMINIĘTO", r["adres"]); continue
        d = art.model_dump()
        d["tytul"] = clean(d["tytul"]); d["opis_meta"] = clean(d["opis_meta"]); d["wstep"] = clean(d["wstep"]); d["rozwiazanie"] = clean(d["rozwiazanie"])
        for s in d["sekcje"]:
            s["h2"] = clean(s["h2"]); s["akapity"] = [clean(p) for p in s["akapity"]]
        for q in d["faq"]:
            q["pytanie"] = clean(q["pytanie"]); q["odpowiedz"] = clean(q["odpowiedz"])
        txt = json.dumps(d, ensure_ascii=False).lower()
        uwagi = [w for w in ("zł", "pozwoleni", "prawo budowlane", "!") if w in txt]
        d.update({"nr": int(r["nr"]), "kolejnosc": r["k"], "temat": r["temat"], "adres": r["adres"], "link": r["link do"],
                  "wygenerowano": datetime.date.today().isoformat(), "uwagi": uwagi})
        json.dump(d, open(os.path.join(KOLEJKA, r["adres"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        made += 1
        print("OK", r["adres"], ("UWAGA: " + ", ".join(uwagi)) if uwagi else "")
    print("gotowe:", made, "| w kolejce:", len(os.listdir(KOLEJKA)))

if __name__ == "__main__":
    main()

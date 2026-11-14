#!/usr/bin/env python3
"""Landing: base sizes 3x6 / 4x6 / 6x6 m + asterisk note about permits.
Usage: python3 ~/patch_sizes.py
All-or-nothing: if any place is not found exactly once, nothing is written."""
import os, shutil, sys

PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/sites/carportactive/static/index.html")
NOTE = ('*Zasady zależą od lokalizacji i miejscowego planu zagospodarowania - zawsze zweryfikuj je '
        'w lokalnym urzędzie (urząd gminy lub starostwo powiatowe).')

R = [
 # FAQ structured data (JSON-LD)
 ('nie wymagają pozwolenia na budowę — wystarczy proste zgłoszenie w urzędzie lub budowa bez formalności zgodnie z aktualnym Prawem Budowlanym.',
  'nie wymagają pozwolenia na budowę* — wystarczy proste zgłoszenie w urzędzie lub budowa bez formalności zgodnie z aktualnym Prawem Budowlanym. ' + NOTE),
 ('(3 × 5 m)', '(3 × 6 m)'),
 ('(4 × 5 m)', '(4 × 6 m)'),
 ('(6 × 5 m)', '(6 × 6 m)'),
 # sizes section
 ('Wszystkie modele budujemy w oparciu o ten sam system modułowy bez konieczności uzyskiwania pozwolenia na budowę (do 35 m²).',
  'Wszystkie modele budujemy w oparciu o ten sam system modułowy. Wiaty do 35 m² zazwyczaj nie wymagają pozwolenia na budowę*.<br><small>' + NOTE + '</small>'),
 ('<div class="size-dims">3 × 5 m</div>', '<div class="size-dims">3 × 6 m</div>'),
 ('<div class="size-dims">4 × 5 m</div>', '<div class="size-dims">4 × 6 m</div>'),
 ('<div class="size-dims">6 × 5 m</div>', '<div class="size-dims">6 × 6 m</div>'),
 ('Powierzchnia: 15 m²', 'Powierzchnia: 18 m²'),
 ('Powierzchnia: 20 m²', 'Powierzchnia: 24 m²'),
 ('Powierzchnia: 30 m²', 'Powierzchnia: 36 m²'),
 # visible FAQ answer
 ('Nie. Zgodnie z polskim Prawem Budowlanym wiaty o powierzchni zabudowy do 35 m² (a na działkach z budynkiem mieszkalnym nawet do 50 m²) nie wymagają pozwolenia na budowę. Wszystkie nasze standardowe modele (15 m², 20 m² oraz 30 m²) mieszczą się w tym limicie.',
  'Zazwyczaj nie*. Zgodnie z polskim Prawem Budowlanym wiaty o powierzchni zabudowy do 35 m² (a na działkach z budynkiem mieszkalnym nawet do 50 m²) nie wymagają pozwolenia na budowę. Modele 3 × 6 m (18 m²) i 4 × 6 m (24 m²) mieszczą się w limicie 35 m². Model 6 × 6 m (36 m²) go przekracza, więc zasady dla niego sprawdź w lokalnym urzędzie.<br><small>' + NOTE + '</small>'),
 # contact form hint
 ('np. 4x5 m', 'np. 4x6 m'),
]

s = open(PATH, encoding="utf-8").read()
bad = [(i + 1, old[:60]) for i, (old, new) in enumerate(R) if s.count(old) != 1]
if bad:
    for i, o in bad:
        print(f"NOT FOUND exactly once: #{i}: {o}...")
    sys.exit("Nothing written.")
for old, new in R:
    s = s.replace(old, new)
if PATH.endswith("static/index.html"):
    shutil.copy(PATH, os.path.expanduser("~/index.html.bak-sizes"))
open(PATH, "w", encoding="utf-8").write(s)
print(f"OK: {len(R)} replacements. Backup: ~/index.html.bak-sizes")

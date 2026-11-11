#!/bin/bash
# Codziennie z cron: wydaje N artykułów z kolejki, przebudowuje stronę i zapisuje w git.
# Użycie: publish.sh 3
N=${1:-3}
cd /home/ubuntu/sites/carportactive/pseo || exit 1
echo "=== $(date '+%F %T') publish $N" >> publish.log
venv/bin/python build.py --publish "$N" >> publish.log 2>&1 || { echo "BLAD build.py" >> publish.log; exit 1; }
cd /home/ubuntu/sites/carportactive || exit 1
git add static pseo >> pseo/publish.log 2>&1
git commit -qm "Poradnik: +$N $(date +%F)" >> pseo/publish.log 2>&1
git push -q >> pseo/publish.log 2>&1 || echo "BLAD git push" >> pseo/publish.log

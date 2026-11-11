#!/bin/bash
# Codziennie z cron: wydaje N artykułów z kolejki, przebudowuje stronę, zapisuje w git i wysyła raport do Telegram.
# Użycie: publish.sh 3
N=${1:-3}
cd /home/ubuntu/sites/carportactive/pseo || exit 1
set -a; . ./.env; set +a
tg() {
  [ -n "$TG_TOKEN" ] && [ -n "$TG_CHAT" ] || return 0
  curl -s -o /dev/null --data-urlencode "chat_id=$TG_CHAT" --data-urlencode "text=$1" \
    -d disable_web_page_preview=true "https://api.telegram.org/bot$TG_TOKEN/sendMessage"
}
echo "=== $(date '+%F %T') publish $N" >> publish.log
rm -f ostatni.txt
if ! venv/bin/python build.py --publish "$N" >> publish.log 2>&1; then
  echo "BLAD build.py" >> publish.log
  tg "Poradnik CarportActive: BLAD przy wydawaniu
$(tail -6 publish.log)"
  exit 1
fi
cd /home/ubuntu/sites/carportactive || exit 1
git add static pseo >> pseo/publish.log 2>&1
git commit -qm "Poradnik: +$N $(date +%F)" >> pseo/publish.log 2>&1
MSG="$(cat pseo/ostatni.txt)"
if ! git push -q >> pseo/publish.log 2>&1; then
  echo "BLAD git push" >> pseo/publish.log
  MSG="$MSG

Uwaga: git push nie przeszedł (strona działa, brak kopii na GitHub)."
fi
tg "$MSG"

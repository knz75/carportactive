# carportactive.pl - README для нового чата (12.11.2026)

## Что это
Сайт стальных вят CarportActive (это тот же продукт, что viaty.pl напарника). Был лендингом, за один день стал сайтом: модули, реализации, монтаж, 42 города, раздел статей Poradnik с автогенерацией (pSEO). Цель: трафик по узким и местным запросам, заявки в Telegram. Свой продукт Сергея - стойки CA-Stand (и в будущем сварные модули).

## Сервер
- VPS Ubuntu (OVH), nginx отдаёт статику из `~/sites/carportactive/static/`. Git-репозиторий в `~/sites/carportactive/` (push на GitHub).
- `.gitignore`: `pseo/.env`, `pseo/venv/`, `pseo/*.log`.
- Визуализатор AI - отдельный сервис `~/carport_ai/` (страницы /ai/ и /wizualizacja/ для viaty.pl). Его НЕ трогаем. Формы сайта шлют заявки в `/wizualizacja/api/contact` -> Telegram.
- Команды Сергею - по одной строке, с `#` в конце.

## Страницы (static/)
| URL | Что | Генератор |
|---|---|---|
| `/` | главная: hero, 8 модулей, реализации, AI-блок, размеры и цены, стойки, Poradnik, FAQ, форма | `src/make_home.py` |
| `/moduly/<slug>/` | 8 модулей: sportowy, panel-narzedziowy, ogrod-wertykalny, plac-zabaw, przechowalnia-rowerow, solar-box, przeslo-zaluzjowe, zamknieta-wiata | `src/make_pages2.py` (данные в `src/make_moduly.py`, список `M`) |
| `/dodatki/ca-stand/` | стойки CA-Stand, od 300 do 999 zł | `src/make_pages2.py` |
| `/montaz/` | монтаж Мазовше, od ok. 4000 zł, "сначала контакт и термин" | `src/make_montaz.py` |
| `/realizacje/` + 7 страниц городов | реальные объекты (Warszawa-karetki, Piskórka, Serock, Otwock Mały, Chrzanów Mały-kamper, Konstancin-Jeziorna, Żyrardów) | `src/make_realizacje.py` |
| `/okolice/` + 42 города | "Wiaty garażowe - <город> i okolice": расстояние от Pruszkowa по прямой, 3 ближайшие реализации, цены, соседние города | `src/make_okolice.py` |
| `/poradnik/<slug>/` | статьи из очереди | `pseo/build.py` |

Общие шапка/подвал/форма - `layout.py`. **Он лежит в двух местах: `src/layout.py` и `pseo/layout.py` - после правки копировать в оба.**

Запуск генераторов (из `~/sites/carportactive/`): `python3 src/make_home.py` и т.д. **После любого генератора обязательно `cd pseo && venv/bin/python build.py`** - он заново вставляет списки статей в маркеры `<!--PORADNIKI:START/END-->` (модули, стойки, монтаж) и `<!--PORADNIK-HOME:START/END-->` (главная) и пересобирает sitemap.

## Дизайн
- `static/css/site.css`. Цвет RAL 7016 (`#383e42`) - шапка, hero, тёмные блоки, подвал. Зелёный `#3f7f33` - кнопки/ссылки. Фоны светлые холодные (не кремовые). Шрифты: Barlow Condensed (заголовки), IBM Plex Sans (текст).
- Меню: Moduły, Realizacje, Montaż, Stojaki, Poradnik, Wizualizacja AI + кнопка Wycena; на ширине до 960 px - кнопка Menu.
- Проверять каждую правку на 360/393/768/1280 (без вылезания за экран). Скриншоты Сергею не нужны.
- Фавикон: вята с машиной по его рисунку, парус зелёный (`favicon.svg/.ico`, `apple-touch-icon.png`).
- Старый `static/css/pages.css` больше не используется.

## pSEO (pseo/)
- `tematy.csv` - темы (`nr;link do;temat;adres;status`). `link do` = ключ из facts.json (`wiata`, `montaz`, `moduly/...`, `dodatki/ca-stand`). Всего 285 тем.
- `facts.json` - факты по каждому ключу + `notatki` (заметки монтажника - главное сырьё) + `notatki_ceny` и `ceny_tematy` (цены получают только темы про цену). `pending: true` у `moduly/drewutnia` и `moduly/oslona-na-kosze` (30 тем ждут своих страниц и картинок).
- `generate.py` - Gemini `gemini-3.8-flash`, ключ в `pseo/.env` (GEMINI_API_KEY, тот же что у carport_ai; там же TG_TOKEN, TG_CHAT). Запуск в фоне: `export $(cat .env) && nohup venv/bin/python -u generate.py --limit 100 > genN.log 2>&1 &`. Флаги: `--redo-ceny`, `--redo ceny-wiata` или `--redo slug1,slug2` (переписать статью на том же адресе, дата выпуска сохраняется).
- `build.py`: `--preview` (папка /podglad/, noindex), `--publish N`, без флага - просто пересборка, `--indexnow-all` (все адреса в Bing). Sitemap собирается сам (включая realizacje/* и okolice/*).
- `publish.sh N` - cron `0 9 * * *` по 3 статьи: выпуск, git push, IndexNow, отчёт в Telegram (ссылки, "IndexNow: 202"). Лог `pseo/publish.log`.
- Состояние на 12.11: на сайте 9 статей, в очереди 246 (по 3 в день - примерно до конца января).
- Проверка цен после генерации: `grep -ohE "[0-9]+ ?zł" kolejka/*.json | sort | uniq -c`.
- Gemini: был случай, когда кончилась предоплата - тогда ломается и визуализатор. Пополнять в AI Studio (можно автопополнение / отдельный ключ для pseo).

## Поиск
- Google Search Console: подтверждено файлом google*.html в static (не удалять). Sitemap отправлен. Product-разметка: главная (AggregateOffer 16 500-21 949, MadeToOrder) и стойки (300-999, 4 модели). Отзывы/рейтинг НЕ добавлять, пока нет настоящих.
- Bing Webmaster: импорт из GSC, sitemap прочитан. IndexNow-ключ `static/37f97a6be16daeadecd4856bbbbde7c3.txt` (не удалять). Данные IndexNow в Bing появляются с задержкой.

## Факты бизнеса (для текстов)
- База в Pruszkowie, работают по Мазовше. Напарник - партнёр Marciniak (монтируют их вяты). **Marciniak на сайте не называть и не критиковать.**
- Цены (как у viaty.pl, брутто, БЕЗ фундамента и монтажа): 3x6 - 16 500, 4x6 - 17 605, 6x6 - 21 949 zł. Столбы 100x100x3, S235, ocynk + proszek, RAL 7016. Большие проекты до 60-70 тыс.
- Монтаж: яма 50x50x80 под столб, до 8 столбов фундамент 1 день на 2 человек, 2-4 недели на бетон, монтаж конструкции 1 день; от ~4000 zł; работа по графику, "не на завтра".
- Przęsła: орех, тёмный орех, RAL 7016. Zamknięta wiata: żaluzja без щелей (от куниц), blacha falista, PIR 5 см, ворота Hörmann/Portos ("np.", без статуса дилера), проезжая версия.
- Концепция вяты-"деревья" - только концепция, НЕ реализация. Консоль на 2 столбах: примерная прикидка (~830 кг стали, фундамент 1,2 м³ на столб; со столбами на 1 м внутрь - заметно легче) - чертёж konsola-1-auto.svg, только для оценки.
- В текстах не писать о законе/разрешениях (кроме формулы "zweryfikuj w urzędzie" на главной), не выдумывать цифры.

## Открытые вопросы / что ждём от Сергея
- Политика конфиденциальности (RODO) и "кто стоит за сайтом" (телефон/фирма/NIP) - решить с напарником, от чьего имени сайт. Идея: свой eSIM-номер, потом "пропущенный звонок -> голосовая почта -> текст в Telegram".
- Google Business Profile (упирается в тот же вопрос).
- Метка страницы в заявке (с какой страницы пришла) и ежедневная сводка посещений из логов nginx в Telegram - не сделано.
- Фото: первый гараж из PIR (по этапам + заметки), drewutnia, osłona na kosze, настенный CA-Lite, свои фото zamknięta wiata (сейчас 4 фото с viaty.pl), новые объекты с городами.
- Через 3-4 недели: Search Console - дотягивать страницы на позициях 8-20.
- Калькуляторы цены/бетона - решили НЕ делать (будут споры с клиентами).

## Файлы в этом архиве
- `src/` - генераторы страниц (на сервере их ещё нет). Положить в `~/sites/carportactive/src/` и добавить в git.

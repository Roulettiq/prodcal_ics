# Производственный календарь (ICS)

Скрипт для генерации производственного календаря России в формате `.ics`.

Данные берутся с [xmlcalendar.ru](https://xmlcalendar.ru).

## Быстрый старт

```bash
git clone https://github.com/Roulettiq/prodcal_ics
cd prodcal_ics
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python3 prodcal_ics.py -o prodcal.ics
```

Файл `prodcal.ics` можно импортировать в любой календарь: macOS, iOS, Google Calendar, Outlook.

## Импорт в macOS Календарь

Файл → Импорт → выбрать `prodcal.ics`

## Импорт в Google Calendar

Перейти на `calendar.google.com` → шестерёнка → Настройки → Импорт и экспорт → Импортировать.

## Как поднять у себя на сервере (живая подписка)

1. Установить зависимости:
```bash
pip3 install -r requirements.txt
```

2. Настроить автообновление через cron:
```bash
0 1 * * * python3 /path/to/prodcal_ics.py -o /var/www/html/prodcal.ics
```

3. Отдавать `prodcal.ics` через любой веб-сервер (nginx, caddy и т.д.)

4. Подписаться на URL в приложении Календарь.

## Параметры

| Параметр | По умолчанию | Описание |
|---|---|---|
| `-o` | `prodcal.ics` | Путь к выходному файлу |
| `--start-year` | текущий год | Начальный год |
| `--end-year` | текущий год | Конечный год |

Пример — сгенерировать календарь за несколько лет:
```bash
.venv/bin/python3 prodcal_ics.py --start-year=2025 --end-year=2026 -o prodcal.ics
```

## Разработка

Валидатор ICS: https://icalendar.org/validator.html

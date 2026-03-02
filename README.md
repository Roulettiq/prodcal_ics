# Производственный календарь (ICS)

Скрипт для генерации производственного календаря России в формате `.ics`.

Данные берутся с [xmlcalendar.ru](https://xmlcalendar.ru).

## Подписка на календарь

Ссылка для подписки (обновляется автоматически 1-го числа каждого месяца):

```
https://roulettiq.github.io/prodcal_ics/prodcal.ics
```

### macOS

В приложении Календарь: Файл → Новая подписка на календарь → вставить ссылку выше.

### Google Calendar

Перейти на `calendar.google.com` → Другие календари → Добавить по URL → вставить ссылку выше.

## Локальная генерация

```bash
git clone https://github.com/Roulettiq/prodcal_ics
cd prodcal_ics
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python3 prodcal_ics.py -o prodcal.ics
```

Файл `prodcal.ics` можно импортировать в любой календарь: macOS, iOS, Google Calendar, Outlook.

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

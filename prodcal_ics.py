#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from icalendar import Calendar, Event
import requests

from datetime import datetime, timedelta
import argparse
import logging
import hashlib
import more_itertools as mit


def get_holidays_grouped_by_months(year):
    url = f"https://xmlcalendar.ru/data/ru/{year}/calendar.json"

    logging.info(url)

    response = requests.get(url)

    if response.status_code == 404:
        return None

    response.raise_for_status()

    data = response.json()
    holidays = []

    for month_data in data["months"]:
        days_raw = month_data["days"].split(",")
        holiday_days = []
        for d in days_raw:
            d = d.strip()
            # * means a working day transferred from a weekend — skip it
            if d.endswith("*"):
                continue
            # + means a transferred holiday — still a day off
            d = d.rstrip("+")
            holiday_days.append(int(d))
        holidays.append(sorted(holiday_days))

    return holidays


def create_dayoff_event(year, month, day_start, day_end):
    event = Event()
    event.add("summary", "Выходной")
    event.add("dtstart", datetime(year, month, day_start, 0, 0, 0).date())
    event.add(
        "dtend", datetime(year, month, day_end, 0, 0, 0).date() + timedelta(days=1)
    )

    # UID is REQUIRED https://tools.ietf.org/html/rfc5545#section-3.6.1
    uid = hashlib.sha512(
        f"{year}{month}{day_start}{day_end}".encode("ascii")
    ).hexdigest()
    event.add("uid", uid)

    return event


def generate_events(year, holidays_by_months):
    events = []

    for month, holidays in enumerate(holidays_by_months, start=1):
        holidays_groups = [list(group) for group in mit.consecutive_groups(holidays)]

        for g in holidays_groups:
            e = create_dayoff_event(year, month, g[0], g[-1])
            events.append(e)

    return events


def parse_args():
    parser = argparse.ArgumentParser(
        description="This script fetches data about production calendar and generates .ics file with it."
    )

    default_output_file = "prodcal.ics"
    parser.add_argument(
        "-o",
        dest="output_file",
        metavar="out",
        default=default_output_file,
        help="output file (default: {0})".format(default_output_file),
    )

    parser.add_argument(
        "--start-year",
        metavar="yyyy",
        type=int,
        default=datetime.today().year,
        help="year calendar starts (default: current year)",
    )

    parser.add_argument(
        "--end-year",
        metavar="yyyy",
        type=int,
        default=datetime.today().year,
        help="year calendar ends (default: current year)",
    )

    parser.add_argument("--log-level", metavar="level", default="INFO")

    return parser.parse_args()


def generate_calendar(events):
    cal = Calendar()
    cal.add("prodid", "-//Roulettiq//prodcal_ics//")
    cal.add("version", "2.0")
    cal.add("NAME", "Производственный календарь")
    cal.add("X-WR-CALNAME", "Производственный календарь")

    for e in events:
        cal.add_component(e)

    return cal


def setup_logging(log_level):
    logging_level = getattr(logging, log_level.upper(), None)

    if not isinstance(logging_level, int):
        raise ValueError("Invalid log level: {0}".format(log_level))

    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="[%d/%m/%Y:%H:%M:%S %z]",
    )


if __name__ == "__main__":
    args = parse_args()
    setup_logging(args.log_level)

    events = []

    # (args.end_year + 1) because range() function doesn't include right margin
    for year in range(args.start_year, args.end_year + 1, 1):
        holidays_by_months = get_holidays_grouped_by_months(year)

        if not holidays_by_months:
            break

        events += generate_events(year, holidays_by_months)

    cal = generate_calendar(events)

    with open(args.output_file, "w") as f:
        f.write(cal.to_ical().decode("utf-8"))

    logging.info(f"Saved to {args.output_file}")

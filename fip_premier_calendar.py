import csv
from ics import Calendar, Event


def csv_to_ics(csv_file, ics_file):
    calendar = Calendar()

    with open(csv_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            event = Event()
            event.name = row["country_flag"] + " " + row["tournament"]
            event.begin = row["start_date"]
            event.end = row["end_date"]
            # event.description = row['description']
            event.location = row["country"]
            calendar.events.add(event)

    with open(ics_file, "w", encoding="utf-8") as icsfile:
        icsfile.writelines(calendar)


if __name__ == "__main__":
    csv_file = "fip_premier_tournaments_2025.csv"
    ics_file = "fip_premier_calendar.ics"
    csv_to_ics(csv_file, ics_file)

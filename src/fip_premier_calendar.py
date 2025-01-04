import csv
from ics import Calendar, Event


def main(csv_file, ics_file):

    # read source data
    with open(csv_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

    # create calendar
    calendar = Calendar()

    for row in reader:
        event = Event()
        event.name = row["country_flag"] + " " + row["tournament"]
        event.begin = row["start_date"]
        event.end = row["end_date"]
        event.location = row["country"]
        calendar.events.add(event)

    # save ics calendar
    with open(ics_file, "w", encoding="utf-8") as icsfile:
        icsfile.writelines(calendar)


if __name__ == "__main__":
    csv_file = "../data/fip_premier_tournaments_2025.csv"
    ics_file = "../export/fip_premier_calendar.ics"
    main(csv_file, ics_file)

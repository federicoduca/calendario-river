import requests
import re
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime, timedelta


def request_url(url):

    response = requests.get(url)

    # Check
    if response.status_code == 200:
        html_content = response.text
        return html_content
    else:
        print("No se pudo obtener el HTML. Código de estado:", response.status_code)
        exit()


def get_matches(html_content):

    # Parseamos el HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Lista para almacenar los datos de cada partido
    matches = []

    # Bucle para cada <ul> de clase "l_calendario", representan las tablas para cada mes
    for month_calendar in soup.find_all("ul", class_="l_calendario"):

        # Iteramos por cada fila, que representa cada partido del mes
        for match_row in month_calendar.find_all("li"):

            print(match_row)

            teams = (
                match_row.find("b", class_="text-uppercase")
                .get_text()
                .replace("  ", " ")
                .replace("River Plate", "RIVER")
            )

            match_info = match_row.find("p").get_text(strip=True)
            competition = match_info.split("• ")[0]
            datetime_start = re.findall(r"\d{2}/\d{2}/\d{4}", match_info)[0]
            datetime_start = datetime.strptime(datetime_start, "%d/%m/%Y").strftime("%Y-%m-%d")

            new_match = {"teams": teams, "competition": competition, "datetime_start": datetime_start}
            print(f"{new_match=}")

            matches.append(new_match)

    return matches


def main(fixture_url, ics_file):

    html_content = request_url(url=fixture_url)

    matches = get_matches(html_content)

    # new events
    calendar = Calendar()

    for match in matches:

        # Create new event
        event = Event()
        event.name = "⚽ " + match["teams"].replace("River Plate", "RIVER")
        event.begin = match["datetime_start"]
        event.last_modified = datetime.now()
        event.description = match["competition"]

        # Add match to calendar
        calendar.events.add(event)

    # Save the content to an .ics file)
    with open(ics_file, "w", encoding="utf-8") as icsfile:
        icsfile.writelines(calendar)


if __name__ == "__main__":
    ics_file = "river_calendar.ics"
    fixture_url = "https://www.cariverplate.com.ar/calendario-de-partidos"
    main(fixture_url, ics_file)

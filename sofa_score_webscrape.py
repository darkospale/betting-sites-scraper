import csv
from bs4 import BeautifulSoup
from requests import get


def main():
    URL = "https://www.sofascore.com/"

    # Make an HTTP GET request to the URL and get the HTML response.
    response = get(URL)

    # Parse the response as HTML using BeautifulSoup.
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all table rows (`tr`) in the HTML that contain data.
    data_rows = soup.find_all("tr", {"class": "event-winner"})

    # Open a new CSV file in write mode.
    with open("rezultati/sofascore.com.csv", "w") as csvfile:
        # Create a CSV writer object.
        writer = csv.writer(csvfile)

        # Write the column headers to the CSV file.
        writer.writerow(["Home Team", "Score", "Away Team"])

        # Iterate over the data rows.
        for row in data_rows:
            # Get the columns (`td` elements) from the row.
            columns = row.find_all("td")

            # Get the text from the columns and strip leading/trailing whitespace.
            home_team = columns[0].get_text().strip()
            score = columns[1].get_text().strip()
            away_team = columns[2].get_text().strip()

            # Write the data to the CSV file.
            writer.writerow([home_team, score, away_team])


if __name__ == "__main__":
    main()
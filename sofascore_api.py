import requests
import json
import datetime
import xlsxwriter
from datetime import date
from datetime import timedelta
from bs4 import BeautifulSoup as bs


def main():
    # Get today's date
    today = date.today()

    # Yesterday date
    yesterday = today - timedelta(days = 1)

    year = yesterday.year
    month = yesterday.month
    day = yesterday.day

    t = datetime.datetime(year, month, day)
    yesterday_date = t.strftime('%Y-%m-%d')

    url = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/" + yesterday_date

    result = requests.get(url, stream=True)

    filename = 'rezultati/sofascore-scores.json'

    if result.status_code == 200:
        with result as r:
            r.raise_for_status()
            with open(filename, 'wb') as f_out:
                for chunk in r.iter_content(chunk_size=8192):
                    f_out.write(chunk)

        # Workbook() takes one, non-optional, argument
        # which is the filename that we want to create.
        workbook = xlsxwriter.Workbook('rezultati/scores ' + yesterday_date + '.xlsx')

        # The workbook object is then used to add new
        # worksheet via the add_worksheet() method.
        worksheet = workbook.add_worksheet()

        worksheet.write('A' + str(1), 'Liga')
        worksheet.write('B' + str(1), 'Domaci')
        worksheet.write('C' + str(1), 'Domaci golovi')
        worksheet.write('D' + str(1), 'Gosti golovi')
        worksheet.write('E' + str(1), 'Gosti')

        with open(filename) as f:
            json_data = json.load(f)

            n = 3
            for game in json_data['events']:
                if 'display' in game['homeScore']:
                    homescore = game['homeScore']['display']

                if 'display' in game['awayScore']:
                    awayscore = game['awayScore']['display']

                league = game['tournament']['name']
                homename = game['homeTeam']['name']
                awayname = game['awayTeam']['name']

                sum_of_scores = homescore + awayscore

                if (sum_of_scores >= 7):
                    # Use the worksheet object to write
                    # data via the write() method.
                    worksheet.write('A' + str(n), league)
                    worksheet.write('B' + str(n), homename)
                    worksheet.write('C' + str(n), homescore)
                    worksheet.write('D' + str(n), awayscore)
                    worksheet.write('E' + str(n), awayname)

                    n = n + 1

            workbook.close()


if __name__ == "__main__":
    main()
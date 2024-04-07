import requests
import json

from datetime import date
from datetime import timedelta
import datetime

# import xlsxwriter module
import xlsxwriter
 
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

payload={}
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Referer': 'https://www.sofascore.com/',
  'Origin': 'https://www.sofascore.com/',
  'Connection': 'keep-alive',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'If-None-Match': 'W/""bc58f42093""',
  'Cache-Control': 'max-age=0',
  'TE': 'trailers'
}

response = requests.request("GET", url, headers=headers, data=payload)

# Workbook() takes one, non-optional, argument
# which is the filename that we want to create.
workbook = xlsxwriter.Workbook('scores ' + yesterday_date + '.xlsx')
 
# The workbook object is then used to add new
# worksheet via the add_worksheet() method.
worksheet = workbook.add_worksheet()

jsonString = json.dumps(response.text)

with open('scores.json', 'w') as f:
    f.write(jsonString)
    f.close()

n = 1
for game in jsondata['events']:
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


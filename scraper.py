#!/usr/bin/python3
# add local libraries
# mkdir lib
# pip3 install pandas bs4 -t lib/

# import local libraries
import sys
# change to your path - absolute path please
sys.path.append('/opt/spotscraper/lib')

# import scraper libs
import pandas as pd
import requests
from bs4 import BeautifulSoup

# import time lib
import datetime

# import json lib
import json

# get dates
today = datetime.date.today()
tomorrow = datetime.date.today() + datetime.timedelta(days=1)

d1 = today.strftime("%Y-%m-%d")
d2 = tomorrow.strftime("%Y-%m-%d")

# set headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

# set epexspot URL
url='https://www.epexspot.com/en/market-data?market_area=BE&auction=MRC&trading_date=' + d1 + '&delivery_date=' + d2 + '&underlying_year=&modality=Auction&sub_modality=DayAhead&product=60&data_mode=table&period='

# get url
r = requests.get(url, headers=headers)
html = r.text
soup = BeautifulSoup(html, "html.parser")

# find the wanted table
table = soup.find('table', {"class": "table-01 table-length-1"})
# select data to filter
rows = table.find_all('tr')

data = []
for row in rows[6:]: #suppress first 6 lines
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

# print the data
result = pd.DataFrame(data, columns=['Buy Volume', 'Sell Volume', 'Volume', 'Price'])
result.reset_index(inplace=False)
result.drop('Buy Volume', inplace=True, axis=1)
result.drop('Sell Volume', inplace=True, axis=1)
result.drop('Volume', inplace=True, axis=1)
#print(result)

resultjson = result.to_json(orient="split")
parsed = json.loads(resultjson)
print(json.dumps(parsed, indent=4))

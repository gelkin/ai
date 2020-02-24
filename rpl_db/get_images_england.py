import requests
import shutil
from shutil import copyfile
import os

import urllib.request, urllib.error, urllib.parse

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

folder_0 = "1000"
folder_1 = "2000"

def download_players():
    dire_0 = folder_0
    if not os.path.exists(dire_0):
        os.mkdir(dire_0)
    dire_1 = folder_1
    if not os.path.exists(dire_1):
        os.mkdir(dire_1)

    url = 'https://premierliga.ru/players/?cur_cc=1&curPos='
    start_pos = 0
    end_pos = 100
    for pos in range(start_pos, end_pos, 20):
        cur_url = url + str(pos)
        response = urllib.request.urlopen(cur_url)
        webContent = response.read()
        html = webContent
        # print(str(html))
        # todo parser
        parsed_html = BeautifulSoup(html, "html5lib")
        table = parsed_html.body.find('div', attrs={'class':'search-result'})
        rows = table.find("tbody").find_all("tr")
        for row in rows[1:]:
            cells = row.find_all("td")
            # img
            img_url = cells[0].find("a").find("img")["src"]

            is_title_rf = cells[1].find("p").find("a").find("img")["title"] == "Российская Федерация"
            is_russian = True if is_title_rf else False
            if is_russian:
                urllib.request.urlretrieve(img_url, folder_1 + "/" + img_url.split("/")[-1])
            else:
                urllib.request.urlretrieve(img_url, folder_0 + "/" + img_url.split("/")[-1])
            print(img_url)
            print(img_url.split("/")[-1])
            print(is_russian)
            # print(len(cells))
            rn = cells[1].get_text()
            print(rn)

url_epl = 'https://www.premierleague.com/players'
response = urllib.request.urlopen(url_epl)
webContent = response.read()
html = webContent
print(html[:10])
parsed_html = BeautifulSoup(html, "html5lib")
table = parsed_html.body.find('div', attrs={'class':'table playerIndex'})
print(table)
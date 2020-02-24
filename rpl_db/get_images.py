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

def train_valid():
    pass

from sklearn.model_selection import train_test_split
X = []
y = []

for f in os.listdir(folder_0):
    X.append(f)
    y.append(folder_0)
for f in os.listdir(folder_1):
    X.append(f)
    y.append(folder_1)

print(X[:10])
print(y[:10])

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=1)
print(len(X_train))
print(len(y_train))

def copy_to_dir(dir_name, X, y):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    if not os.path.exists(dir_name + "/" + folder_0):
        os.mkdir(dir_name + "/" + folder_0)
    if not os.path.exists(dir_name + "/" + folder_1):
        os.mkdir(dir_name + "/" + folder_1)

    for x_row, y_row in zip(X, y):
        filename = y_row + "/" + x_row
        copyfile(filename, dir_name + "/" + filename)

copy_to_dir("train", X_train, y_train)
copy_to_dir("valid", X_val, y_val)

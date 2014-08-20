#!/usr/bin/env python
import os

import requests
from bs4 import BeautifulSoup
from datetime import datetime

LOC = os.path.dirname(__file__)


def main():
    date = datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(LOC, date + ".md")

    with open(filename, "w") as e:
        e.write("###" + date + "\n")

    scrape("python", filename)
    scrape("go", filename)
    scrape("cpp", filename)
    scrape("javascript", filename)
    scrape("coffeescript", filename)

    cmd = "cd " + LOC + ";git add --all; git commit -m '" + date + "'; git push"
    os.system(cmd)


def scrape(language, filename):
    req = requests.get("https://github.com/trending?l=" + language)
    soup = BeautifulSoup(req.content)

    with open(filename, "a") as e:
        e.write("\n####" + language + "\n")
        for item in soup.find_all("li", class_="leaderboard-list-item"):

            title = item.h2.a.text
            try:
                description = item.p.text
            except:
                description = ""
            url = "https://github.com" + item.h2.a.get("href")
            line = "* [" + title + "](" + url + "): " + description + "\n"
            e.write(line.encode('ascii', 'ignore'))

if __name__ == '__main__':
    main()

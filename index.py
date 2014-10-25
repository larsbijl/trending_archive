#!/usr/bin/env python
import os
from os.path import join, dirname, exists

import requests
from bs4 import BeautifulSoup
from datetime import datetime

LOC = dirname(__file__)


def main():
    month = datetime.now().strftime("%Y-%m")
    date = datetime.now().strftime("%Y-%m-%d")
    file_location = join(LOC, month)
    filename = join(file_location, date + ".md")
    if not exists(file_location):
        os.makedirs(file_location)

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
        for item in soup.find_all("li", class_="repo-list-item"):

            title = item.h3.a.get("href")[1:]
            try:
                description = item.p.text.rstrip().lstrip()
            except:
                description = ""
            url = "https://github.com" + item.h3.a.get("href")
            line = "* [" + title + "](" + url + "): " + description + "\n"
            e.write(line.encode('ascii', 'ignore'))

if __name__ == '__main__':
    main()

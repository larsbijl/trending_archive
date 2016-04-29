#!/usr/bin/env python
import os
from os.path import join, dirname, exists

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

LOC = dirname(__file__)


def main():

    # yesterdays file.
    yesterday = datetime.now() - timedelta(days=1)
    ymonth = yesterday.strftime("%Y-%m")
    ydate = yesterday.strftime("%Y-%m-%d")
    yfilename = join(LOC, ymonth, ydate + ".md")
    with open(yfilename) as e:
        yfilecontents = e.read()

    month = datetime.now().strftime("%Y-%m")
    date = datetime.now().strftime("%Y-%m-%d")
    file_location = join(LOC, month)
    filename = join(file_location, date + ".md")
    if not exists(file_location):
        os.makedirs(file_location)

    with open(filename, "w") as e:
        e.write("###" + date + "\n")
        e.write("diff between today and yesterday\n")

    scrape("python", filename, yfilecontents)
    scrape("go", filename, yfilecontents)
    scrape("cpp", filename, yfilecontents)
    scrape("javascript", filename, yfilecontents)
    scrape("coffeescript", filename, yfilecontents)

    cmd = "cd " + LOC + ";git add --all; git commit -m '" + date + "'; git push"
    os.system(cmd)


def scrape(language, filename, yfilecontents):
    req = requests.get("https://github.com/trending?l=" + language)
    soup = BeautifulSoup(req.content)

    with open(filename, "a") as e:
        e.write("\n####" + language + "\n")
        for item in soup.find_all("li", class_="repo-list-item"):

            url = "https://github.com" + item.h3.a.get("href")
            if url in yfilecontents:
                continue

            title = item.h3.a.get("href")[1:]
            try:
                description = item.p.text.rstrip().lstrip().split("\n")[0]
            except:
                description = ""

            line = "* [" + title + "](" + url + "): " + description + "\n"
            e.write(line.encode('ascii', 'ignore'))

if __name__ == '__main__':
    main()

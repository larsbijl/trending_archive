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
    if os.path.exists(yfilename):
        with open(yfilename) as e:
            yfilecontents = e.read()
    else:
        yfilecontents = ""

    month = datetime.now().strftime("%Y-%m")
    date = datetime.now().strftime("%Y-%m-%d")
    file_location = join(LOC, month)
    filename = join(file_location, date + ".md")
    filename_short = join(file_location, date + "_short.md")
    if not exists(file_location):
        os.makedirs(file_location)

    with open(filename, "w") as e:
        e.write("### " + date + "\n")

    with open(filename_short, "w") as e:
        e.write("### " + date + "\n")
        e.write("diff between today and yesterday\n")

    scrape("python", filename, filename_short, yfilecontents)
    scrape("go", filename, filename_short, yfilecontents)
    scrape("rust", filename, filename_short, yfilecontents)
    scrape("cpp", filename, filename_short, yfilecontents)
    scrape("javascript", filename, filename_short, yfilecontents)
    scrape("typescript", filename, filename_short, yfilecontents)

    cmd = "cd " + LOC + ";git add --all; git commit -m '" + date + "'; git push"
    print(cmd)
    os.system(cmd)


def scrape(language, filename, filename_short, yfilecontents):
    req = requests.get("https://github.com/trending?l=" + language)
    soup = BeautifulSoup(req.content, "html.parser")


    e = open(filename, "a")
    d = open(filename_short, "a")

    e.write("\n#### " + language + "\n")
    d.write("\n#### " + language + "\n")

    for item in soup.find_all("article", class_="Box-row"):
        url = "https://github.com" + item.h1.a.get("href")

        title = item.h1.a.get("href")[1:]
        try:
            description = item.p.text.rstrip().lstrip().split("\n")[0]
        except:
            description = ""

        line = "* [" + title + "](" + url + "): " + description + "\n"
        e.write(line.encode('ascii', 'ignore'))

        if url in yfilecontents:
            continue

        d.write(line.encode('ascii', 'ignore'))

    e.close()
    d.close()


if __name__ == '__main__':
    main()

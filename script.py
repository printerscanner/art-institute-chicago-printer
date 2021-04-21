#!/usr/bin/env python3

import json
import re
import sys
import time
import urllib

from parsel import Selector

# Code taken from user computerval on reddit
# Taken from
# https://github.com/django/django/blob/c7cc7526d5ee7d38a6ee1af03610f1aba1ea0c78/django/utils/text.py#L219
# (via
# https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename)
def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def scrape(start, end):
    for i in range(start, end + 1):
        api_page = f"https://www.artic.edu/collection/more?is_public_domain=1&page={i}"
        print(f"Visiting {api_page}")
        html_page = json.loads(urllib.request.urlopen(api_page).read())['html']
        sel  = Selector(html_page)
        works = sel.css("li.m-listing")
        print(f"{len(works)} works on this page")
        for work in works:
            img = work.css("span.m-listing__img ::attr(data-iiifid)").get()
            fullsize_img = img + "/full/full/0/default.jpg"
            info_img = img + "/info.json"
            label = " ".join(
                " ".join(work.css("span.m-listing__meta ::text").getall()).split()
            )
            img_filename = get_valid_filename(label + ".jpg")
            info_filename = get_valid_filename(label + ".info.json")
            print(f"Saving {fullsize_img} to {img_filename}")
            try:
                with open(f"{img_filename}", 'xb') as fh:
                    fh.write(urllib.request.urlopen(fullsize_img).read())
                # Be a little bit nicer to the site
                time.sleep(1.0)
            except FileExistsError:
                print("Image already downloaded, skipping")
            try:
                with open(f"{info_filename}", 'xb') as fh:
                    fh.write(urllib.request.urlopen(info_img).read())
                time.sleep(1.0)
            except FileExistsError:
                print("Info JSON already downloaded, skipping")


def main():
    if len(sys.argv) != 3:
        sys.exit(f"Usage: {sys.argv[0]} <start page> <end page>")

    start = int(sys.argv[1])
    end = int(sys.argv[2])

    scrape(start, end)


if __name__=="__main__":
    main()
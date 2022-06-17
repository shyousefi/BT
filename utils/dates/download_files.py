#!/usr/bin/python

import requests
import argparse
import json
import os
from pathlib import Path
from bs4 import BeautifulSoup

BASE_URL = "https://www.bundestag.de"

def collect_links():
    
    print("Fetching URLs...")

    limit = 10
    urls = {}
    offset = None
    while offset is None or len(urls) - offset >= limit:
        offset = len(urls)
        params = {"limit": limit, "noFilterSet": "true", "offset": offset }
        res = requests.get(f"{BASE_URL}/ajax/filterlist/de/services/opendata/488214-488214", params=params)
        if not res.status_code == 200:
            print("[-] Error fetching download page:", res.status_code, res.reason)
            exit()

        soup = BeautifulSoup(res.text, "html.parser")
        tds = soup.find_all("td")
        for td in tds:
            title = td.find("strong").text.strip()
            url = td.find("a")["href"]
            urls[url] = title
    
    return urls

def download_zips(urls, directory):

    if not os.path.isdir(args.directory):
        os.mkdir(args.directory)

    for url, title in urls.items():
        file_name = os.path.basename(url)
        destination = os.path.join(directory, file_name)
        if not os.path.isfile(destination) or os.stat(destination).st_size == 0:
            print(f"Downloading {title} to {destination}...")
            res = requests.get(BASE_URL + url)
            if res.status_code == 200:
                with open(destination, "wb") as f:
                    f.write(res.content)
            else:
                print("Error while downloading file:", res.status_code, res.reason)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Bundestag Plenarprotokolle download script')
    parser.add_argument('-d', '--directory',
                        default='/ukp-storage-1/krause/Thesis/data/Bundestagsprotokolle',
                        dest='directory',
                        help='Destination directory',
                        type=str)


    args = parser.parse_args()
    Path(args.directory).mkdir(parents=True, exist_ok=True)
    links = collect_links()
    download_zips(links, args.directory)
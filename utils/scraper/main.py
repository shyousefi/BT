import os.path

from bs4 import BeautifulSoup
from pathlib import Path
import requests
import re

url = "http://www.hansard-archive.parliament.uk/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")

href_list = soup.find_all("li", {"class": "mainPanelListItem"})
print(href_list)

for i in href_list:
    href = i.find("a")["href"]
    match = re.findall("([1-3][0-9]{3})", href)
    if len(match) == 2:
        href = "http:" + href
        newpage = requests.get(href)
        directory = "data/" + match[0] + "-" + match[1]
        Path(directory).mkdir(parents=True, exist_ok=True)

        new_soup = BeautifulSoup(newpage.content, "lxml")
        table = new_soup.find("table", {"class": "normaltext"})

        pages = table.find_all("tr")[-1]
        new_pages = pages.findNext().find_all("a")

        for j in range(len(new_pages) + 1):
            zip_refs = table.find_all("a")
            for zip_ref in zip_refs:
                temp_dir = directory + "/" + zip_ref.text
                if os.path.exists(temp_dir) or not zip_ref.text.__contains__(".zip"):
                    continue
                zip_url = zip_ref["href"]
                zip_response = requests.get("http:" + zip_url)
                with open(temp_dir, "wb") as handle:
                    handle.write(zip_response.content)

            if j != len(new_pages):
                page = new_pages[j]["href"]

                input_data = new_soup.find_all("input", {"type": "hidden"})
                regex = re.match("^javascript:__doPostBack\('(.*)',''\)$", page)[1]

                postdata = {"__EVENTTARGET" : regex}
                for date in input_data:
                    postdata[date["id"]] = date["value"]

                page_response = requests.post(href, data=postdata)
                new_soup = BeautifulSoup(page_response.content, "lxml")
                table = new_soup.find("table", {"class": "normaltext"})


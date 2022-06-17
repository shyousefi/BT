from bs4 import BeautifulSoup
import os
import zipfile
import re
import pandas as pd
from pathlib import Path

# change these accordingly---
HANSARD_PATH = "/ukp-storage-1/krause/Thesis/data/Hansard/"
CSV_PATH = os.path.join(HANSARD_PATH, "csv")
# ---
HOUSE_COMMONS = "housecommons"
HOUSE_LORDS = "houselords"
DEBATES = "debates"
DATE = "date"
FORMAT = "format"
SECTION = "section"
TITLE = "title"
MEMBER = "member"


def read_houses(houses, path):
    year_range = re.search("\d{4}-\d{4}", path)[0]
    if not year_range:
        pass
    curr_year = year_range[0].split("-")[0]
    for house in houses:
        dates = house.find_all(DATE)
        debates = house.find_all(DEBATES)
        curr_year = write_to_csv(dates, debates, curr_year)


def write_to_csv(dates, debates, curr_year):
    for date in dates:
        date_string = date[FORMAT]
        year = curr_year if not date_string else int(date_string.split("-")[0])
        year_int = int(year)
        if year_int > 1980 or year_int < 1803:
            continue
        for debate in debates:
            date_list = []
            debate_list = []
            title_list = []
            sections = debate.find_all(SECTION)
            for section in sections:
                texts = section.find_all("p")
                for text in texts:
                    date_list.append(date_string)
                    debate_list.append(text.text)
                    title_list.append(section.find("title").text)

            df = pd.DataFrame({DEBATES: debate_list, DATE: date_list, TITLE: title_list})
            csv_name = get_path(year) + ".csv"
            csv_dir = os.path.join(CSV_PATH, csv_name)
            if not os.path.isfile(csv_dir):
                df.to_csv(csv_dir, mode='w', header=True, index=False, sep="\t")
            df.to_csv(csv_dir, mode='a', header=False, index=False, sep="\t")
        return year


def get_path(year):
    last_digit = year % 10
    beginning_year = year - last_digit + 1 if last_digit > 0 else year - 9
    beginning_year = beginning_year if year > 1810 else 1803
    csv = str(beginning_year) + "-" + str(beginning_year + 9)
    if beginning_year == 1803:
        csv = str(beginning_year) + "-1810"
    return csv


Path(CSV_PATH).mkdir(parents=True, exist_ok=True)
for file in os.listdir(HANSARD_PATH):
    zip_path = os.path.join(HANSARD_PATH, file)
    if not os.path.isdir(zip_path):
        continue
    for zip_file in os.listdir(zip_path):
        zip_file_path = os.path.join(zip_path, zip_file)
        if zipfile.is_zipfile(zip_file_path):
            archive = zipfile.ZipFile(zip_file_path, "r")
            for xml_file in archive.filelist:
                xml = archive.read(xml_file.filename)
                soup = BeautifulSoup(xml, "lxml")
                house_lords = soup.find_all(HOUSE_LORDS)
                house_commons = soup.find_all(HOUSE_COMMONS)

                read_houses(house_lords, zip_path)
                read_houses(house_commons, zip_path)